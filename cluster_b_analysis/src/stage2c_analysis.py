"""Build reviewed Stage 2C comparisons. Run as a module from the repository root."""
import csv
import json
from dataclasses import dataclass
from itertools import combinations

from .data_loading import ROOT, read_score
from .failure_mode_analysis import write_rows
from .pareto import comparison_coverage, complete_panel, fronts, relation
from .ranking import pair_outcomes, rank_reversals, rankings


@dataclass(frozen=True)
class Panel:
    id: str
    paper: str
    table: str
    block: str
    objectives: tuple
    kind: str
    note: str


BIO = (("Dynamic updating", "QA Score", "higher"), ("Temporal reasoning", "QA Score", "higher"))
GATES = (("Overall", "Served accuracy", "higher"), ("Overall", "Strict unfaithfulness", "lower"),
         ("Overall", "Abstain rate", "lower"))
HALU = (("Question answering", "Accuracy", "higher"), ("Question answering", "Hallucination rate", "lower"),
        ("Question answering", "Omission rate", "lower"))
IMLOGIC = (("Conversation-level MCQ", "Accuracy", "higher"),
           ("Conversation-level MCQ", "Preference trap rate", "lower"),
           ("Conversation-level MCQ", "Generic trap rate", "lower"),
           ("Conversation-level MCQ", "Fabrication trap rate", "lower"))
PANELS = (
    *(Panel(f"memgpt-msc-dmr-{backbone}", "memgpt", "Table 2", f"memgpt-msc-dmr-{backbone}",
            (("Deep memory retrieval", "Accuracy", "higher"), ("Deep memory retrieval", "ROUGE-L Recall", "higher")),
            "matched backbone systems",
            "Same reader and DMR questions. Judge correctness and lexical recall score the same answers."
            " The memory access and source evidence differ between treatments.")
      for backbone in ("gpt-3-5-turbo", "gpt-4", "gpt-4-turbo")),
    Panel("imlogic-conversation", "root_memory", "Table 5", "root-memory-imlogic-conversation-level-full",
          IMLOGIC, "evaluated systems and controlled additions",
          "Full IMLogic: GPT-4o-mini memory backbone, GPT-5.1 answerer, top-30. Four dependent answer categories."),
    Panel("biomem-medical", "biomem", "Table 4", "biomem-realmem-medical-huatuogpt-3-27b", BIO,
          "controlled variants", "Frozen HuatuoGPT-3-27B; GPT-4o-mini judge. QA rubric by task; overlapping cohort."),
    *(Panel(f"sirin-{name}", "sirin", "Table 8", f"sirin-longmemeval-{name}", GATES, "controlled variants",
            "Same base memory framework and Table 8 evaluation. Maximize answer coverage; minimize abstention as its exact complement.")
      for name in ("mem0", "lightmem")),
    *(Panel(f"halumem-{name}", "halumem", "Table 3", f"halumem-{name}-original", HALU, "evaluated systems",
            "Shared original split and GPT-4o QA protocol. Correct, hallucination and omission categories share questions.")
      for name in ("medium", "long")),
)

REJECTIONS = (
    ("oracle-chromatlas-nd", "Backbone matching is unverified and pairwise preferences and estimated tokens have distinct sampling units."),
    ("memoryrewardbench-preferences", "Reward-model judgment is a distinct evaluand from answering with memory."),
    ("locco-forgetting", "Exact values cover selected annotations. Unlabeled plot estimates are ineligible."),
    ("msc-cross-study", "MemGPT deep memory retrieval and RMM next-response generation use distinct tasks and scorers."),
    ("twist-track-b", "Validated comparison key is shared within backends, but prompt, call and evidence conditions remain conditional."),
    ("membench-accuracy-efficiency", "Several times are left-censored and some cross-task accuracy rows have unresolved result lineage."),
    ("es-memeval-dialogue-objectives", "Observation-based and judge outcomes use separate reported tables and protocols; no verified strict cross-table objective vector was added."),
    ("sirin-cross-framework", "Mem0 and LightMem are separate source protocols; no common frontier."),
    ("sirin-table-5", "SimpleMem Table 5 uses a different question filter and label protocol from Table 8."),
    ("realmem-full-vs-medical", "Different split, scorer and rubric; cannot combine objectives."),
    ("halumem-extraction-updating", "System-specific write/update protocols and missing outcomes limit direct compatibility."),
    ("halumem-cross-split", "Medium and Long are separate splits; overlapping source users and protocols."),
    ("memorybench-feedback", "Matched response revision has one reported outcome; no multi-objective vector."),
    ("locomo-vs-locomo-plus", "Different factual and latent-constraint questions and scoring."),
    ("cross-study-cost", "Context tokens, generator completion tokens and runtime use different denominators and protocols."),
    ("cross-retriever-and-scaling", "Retriever and scaling settings alter the intervention. No joint common objective set selected."),
)


def read(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def objective(task, metric):
    return f"{task} / {metric}"


def build_panel(panel, observed, comparisons):
    requested = {(task, metric): direction for task, metric, direction in panel.objectives}
    directions = {objective(*k): v for k, v in requested.items()}
    cells, configurations, excluded = {}, {}, {}
    for row in observed:
        if (row["paper_id"], row["table_id"], row["block_id"]) != (panel.paper, panel.table, panel.block):
            continue
        key = (row["task"], row["metric"])
        if key not in requested:
            continue
        name = row["configuration_id"]
        configurations.setdefault(name, row)
        if row["role"] == "oracle":
            excluded[name] = "Oracle information makes the comparator ineligible"
        elif row["verification"] != "verified" or row["provenance"] != "original" or row["synthesis_exclude"] != "no":
            excluded[name] = "Source eligibility flag or missing measurement"
        elif row["discrepancy"]:
            excluded[name] = f"Stage 1 source flag: {row['discrepancy']}"
        else:
            label = objective(*key)
            if (name, label) in cells:
                raise ValueError(f"Duplicate source cells in {panel.id}: {name}, {label}")
            if row["direction"] != requested[key] and not (
                    panel.paper == "sirin" and key[1] == "Abstain rate" and not row["direction"]):
                raise ValueError(f"Invalid source direction in {panel.id}: {label}")
            cells[name, label] = row

    candidates = {name: {label: cells[name, label]["score"] for label in directions if (name, label) in cells}
                  for name in configurations if name not in excluded}
    vector_context = {(row["benchmark"], row["benchmark_version"], row["split"], row["backbone"])
                      for (name, _), row in cells.items() if name in candidates}
    if len(vector_context) != 1 or not next(iter(vector_context))[-1]:
        raise ValueError(f"Unmatched panel context: {panel.id}")

    def compatible(a, b):
        for label in directions:
            left, right = cells[a, label], cells[b, label]
            if (left["unit"], left["metric_definition"], left["judge"]) != (
                    right["unit"], right["metric_definition"], right["judge"]):
                return False
            check = comparisons.get(frozenset((left["observation_id"], right["observation_id"])))
            if not check:
                return False
            if check["status"] == "Directly comparable":
                continue
            if not (panel.paper == "sirin" and left["metric"] == "Abstain rate"
                    and check["reason"] == "A shared metric orientation is unspecified."):
                return False
        return True

    vectors, incomplete = complete_panel(candidates, directions, compatible)
    if len(vectors) < 2:
        raise ValueError(f"Insufficient compatible vectors in {panel.id}")
    excluded.update(incomplete)
    return vectors, directions, cells, configurations, excluded


def run(root=ROOT):
    dataset = read(root / "data/validated_results.csv")
    comparisons = {
        frozenset((r["left_observation"], r["right_observation"])): r
        for r in read(root / "data/comparability.csv") if r["comparison_level"] == "within_block"
    }
    prior = {(r["target_observation_id"], r["reference_observation_id"]): r
             for r in read(root / "results/stage2b_source_contrasts.csv")}
    eligibility, front_rows, relations, rank_rows, tradeoffs = [], [], [], [], []
    plot_panels = {}
    for panel in PANELS:
        vectors, directions, cells, configurations, excluded = build_panel(panel, dataset, comparisons)
        ranks = rankings(vectors, directions)
        layers = {name: index for index, layer in enumerate(fronts(vectors, directions), 1) for name in layer}
        labels = {name: row["source_row"] for name, row in configurations.items()}
        common = {"panel": panel.id, "paper_id": panel.paper, "source_table": panel.table,
                  "protocol_block": panel.block, "evidence_type": panel.kind}
        eligibility.append({**common, "status": "Eligible", **comparison_coverage(configurations, vectors),
                            "objectives": directions, "reason": panel.note})
        for name, reason in sorted(excluded.items()):
            eligibility.append({**common, "status": "Excluded configuration", "configuration_id": name,
                                "system": labels[name], "reason": reason})
        for name, vector in sorted(vectors.items()):
            source = configurations[name]
            front_rows.append({
                **common, "configuration_id": name, "system": labels[name], "architecture": source["architecture"],
                "benchmark": source["benchmark"], "benchmark_version": source["benchmark_version"],
                "split": source["split"], "backbone": source["backbone"],
                "cohort": json.loads(source["source_details"] or "{}").get("independent_group")
                          or f"{panel.paper}:{source['benchmark']}",
                "front": layers[name], "non_dominated": layers[name] == 1,
                "scores_in_original_units": vector, "units": {key: cells[name, key]["unit"] for key in vector}, "source_observation_ids": {
                    key: cells[name, key]["observation_id"] for key in vector},
                "answer_coverage_percent": str(100 - read_score(vector["Overall / Abstain rate"]))
                    if panel.paper == "sirin" else "",
            })
            for key, rank in ranks.items():
                cell = cells[name, key]
                rank_rows.append({**common, "configuration_id": name, "system": labels[name],
                                  "objective": key, "direction": directions[key],
                                  "original_score": cell["score"], "unit": cell["unit"], "rank": rank[name],
                                  "observation_id": cell["observation_id"], "metric_definition": cell["metric_definition"],
                                  "judge": cell["judge"]})
        for a, b in combinations(sorted(vectors), 2):
            wins, ties, losses = pair_outcomes(vectors[a], vectors[b], directions)
            ab, ba = relation(vectors[a], vectors[b], directions), relation(vectors[b], vectors[a], directions)
            relations.append({**common, "left_configuration": a, "right_configuration": b,
                              "left_system": labels[a], "right_system": labels[b],
                              **{f"{side}_{kind}": flag for side, flags in (("left", ab), ("right", ba))
                                 for kind, flag in zip(("weak", "pareto", "strict"), flags)},
                              "per_objective_source_class": {
                                  key: comparisons[frozenset((cells[a, key]["observation_id"],
                                                              cells[b, key]["observation_id"]))]["evidence_type"]
                                  for key in directions},
                              "wins": len(wins), "ties": len(ties), "losses": len(losses),
                              "win_objectives": wins, "tie_objectives": ties, "loss_objectives": losses})
        for a, b, win, loss in rank_reversals(vectors, directions):
            tradeoffs.append({**common, "type": "rank reversal", "left_system": labels[a], "right_system": labels[b],
                              "left_configuration": a, "right_configuration": b,
                              "left_favored": win, "right_favored": loss,
                              "left_scores": {key: vectors[a][key] for key in (win, loss)},
                              "right_scores": {key: vectors[b][key] for key in (win, loss)}})
        for target in vectors:
            for reference in vectors:
                for key in directions:
                    t, r = cells[target, key], cells[reference, key]
                    record = prior.get((t["observation_id"], r["observation_id"]))
                    if record:
                        tradeoffs.append({
                            **common, "type": "Stage 2B matched effect", "left_system": labels[target],
                            "right_system": labels[reference], "left_configuration": target,
                            "right_configuration": reference, "objective": key,
                            "effect": record["profile_effect"], "unit": record["profile_effect_unit"],
                            "stratum": record["profile_stratum"], "left_observation_id": t["observation_id"],
                            "right_observation_id": r["observation_id"]})
        plot_panels[panel.id] = (vectors, labels, layers)
    for name, reason in REJECTIONS:
        eligibility.append({"panel": name, "status": "Rejected", "reason": reason})

    uncertainty = [
        {k: row[k] for k in ("paper_id", "table_id", "configuration_id", "source_row", "observation_id",
                              "metric", "score", "unit", "ci_lower", "ci_upper", "limitations", "source_details")}
        for row in dataset if row["paper_id"] == "sirin" and row["table_id"] == "Table 8 caption"
        and row["metric"] == "Paired served accuracy change" and row["ci_lower"] and row["ci_upper"]
    ]
    for row in dataset:
        if (row["paper_id"], row["table_id"], row["task"], row["metric"]) != (
                "sirin", "Table 8", "Overall", "Served accuracy"):
            continue
        details = json.loads(row["source_details"] or "{}")
        interval = details.get("paired_probe_minus_judge_ci95_pp")
        if interval:
            uncertainty.append({
                "paper_id": "sirin", "table_id": "Table 8 caption", "source_row": row["source_row"],
                "configuration_id": row["configuration_id"], "observation_id": row["observation_id"],
                "metric": "Probe minus Judge paired served-accuracy change",
                "unit": "percentage_points", "ci_lower": interval[0], "ci_upper": interval[1],
                "limitations": details["paired_probe_minus_judge_source"],
            })
    for name, rows in (("pareto_eligibility", eligibility), ("pareto_fronts", front_rows),
                       ("dominance_relations", relations), ("within_panel_rankings", rank_rows),
                       ("failure_mode_tradeoffs", tradeoffs), ("pareto_reported_uncertainty", uncertainty)):
        write_rows(root / "results" / f"{name}.csv", rows)
    from .stage2c_figures import render
    render(plot_panels, root / "figures")
    print(f"{len(PANELS)} panels, {len(front_rows)} vectors, {len(relations)} within-panel pairs, "
          f"{sum(r['type'] == 'rank reversal' for r in tradeoffs)} objective reversals, {len(uncertainty)} source intervals")


if __name__ == "__main__":
    run()
