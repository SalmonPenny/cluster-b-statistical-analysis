"""Stage 2E descriptive evidence inventory and configuration-level selection."""
from collections import defaultdict
from decimal import Decimal
from itertools import combinations
import json

from .data_loading import ROOT, read_score
from .failure_mode_analysis import mapped_failure, write_rows
from .ranking import rankings
from .stage2c_analysis import read

HALLUCINATION = "direct hallucination"
UNFAITHFULNESS = "direct unfaithfulness"
DIAGNOSTIC = "specific failure-mode diagnostic"
PROXY = "general memory-performance proxy"
OTHER = "ancillary outcome"
EVIDENCE_CLASSES = (HALLUCINATION, UNFAITHFULNESS, DIAGNOSTIC, PROXY)


def evidence_class(row):
    """A legacy 'direct' flag alone does not establish a hallucination endpoint."""
    metric = row["metric"].casefold()
    if row["unit"] in {"seconds", "tokens", "thousands of tokens"}:
        return OTHER
    marker = row["hallucination_measurement"]
    if marker == "direct" and metric == "hallucination rate":
        return HALLUCINATION
    if marker == "direct" and metric == "strict unfaithfulness":
        return UNFAITHFULNESS
    if row["paper_id"] == "memoryrewardbench" or row["role"] == "derived summary":
        return OTHER
    task = row["task"].casefold()
    if metric == "omission rate" or row["paper_id"] == "locco":
        return DIAGNOSTIC
    if metric == "abstain rate":
        return OTHER
    if marker == "direct" or mapped_failure(row) and task not in {"overall", "question answering"}:
        return DIAGNOSTIC
    if row["failure_mode"] and task not in {"overall", "question answering", "next response generation",
                                         "scripted conversation", "dialogue generation"}:
        return DIAGNOSTIC
    return PROXY if marker == "proxy" else OTHER


def panel_key(row):
    return (row["paper_id"], row["table_id"], row["block_id"])


def system_key(row):
    return f'{row["paper_id"]}:{row["block_id"]}:{row["configuration_id"]}'


def distinct(rows, field):
    return sorted({row[field] for row in rows if row[field]})


def identity(rows):
    row = rows[0]
    paper, architecture, source = row["paper_id"], row["architecture"], row["source_row"]
    variants = distinct(rows, "architecture_version")
    source_details = [json.loads(cell["source_details"] or "{}") for cell in rows]
    family, intervention = architecture, ""
    if paper == "sirin" and "SIRIN " in source:
        intervention = " | ".join(source.split(" | ")[1:])
    elif paper == "biomem" and architecture == "HMRU":
        family, intervention = "A-Mem", source
    elif architecture.endswith(" + RootMem"):
        family, intervention = architecture.removesuffix(" + RootMem"), "RootMem addition"
    elif architecture == "Mem0-Graph":
        family, intervention = "Mem0", "Graph variant"
    elif "ablation" in distinct(rows, "role"):
        intervention = "Source-labelled controlled variant"
    return {
        "registry_id": system_key(row), "paper_id": paper, "configuration_id": row["configuration_id"],
        "system_label": architecture, "design_lineage_label": family,
        "rq2_categories": distinct(rows, "rq2_category"), "implementation_versions": variants,
        "intervention": intervention, "backbones": distinct(rows, "backbone"), "judges": distinct(rows, "judge"),
        "answering_models": sorted({details["answering_model"] for details in source_details
                                    if details.get("answering_model")}),
        "benchmarks": distinct(rows, "benchmark"), "benchmark_versions": distinct(rows, "benchmark_version"),
        "roles": distinct(rows, "role"), "source_rows": distinct(rows, "source_row"),
        "protocol_blocks": distinct(rows, "block_id"), "mechanisms": distinct(rows, "mechanisms"),
        "retrieval_budgets": distinct(rows, "retrieval_budget"), "memory_budgets": distinct(rows, "memory_budget"),
        "context_budgets": distinct(rows, "context_budget"), "source_observation_ids": distinct(rows, "observation_id"),
    }


def loc(row):
    return {key: row[key] for key in ("observation_id", "paper_id", "publication_id", "publication_version",
                                      "pdf_page", "table_id", "source_row", "source_column", "source_url")}


def outcome(row):
    return {"registry_id": system_key(row), "configuration_id": row["configuration_id"],
            "system_label": row["architecture"], "source_label": row["source_row"],
            "score": row["score"], "score_as_printed": row["score_as_printed"], "unit": row["unit"], "role": row["role"],
            "provenance": row["provenance"], "synthesis_exclude": row["synthesis_exclude"],
            "backbone": row["backbone"], "judge": row["judge"],
            "metric_definition": row["metric_definition"], "judging_protocol": row["judging_protocol"],
            "reported_uncertainty": {field: row[field] for field in
                                     ("sample_size", "independent_runs", "sd", "se", "ci_lower", "ci_upper") if row[field]},
            "limitations": row["limitations"], "source_details": json.loads(row["source_details"] or "{}"),
            "source": loc(row)}


def descriptors(row):
    mode = mapped_failure(row)
    return {
        "paper_id": row["paper_id"], "source_table": row["table_id"], "protocol_block": row["block_id"],
        "benchmark": row["benchmark"], "benchmark_version": row["benchmark_version"], "split": row["split"],
        "task": row["task"], "metric": row["metric"], "unit": row["unit"],
        "failure_mode": mode.label if mode else row["failure_mode"], "metric_definition": row["metric_definition"],
        "denominator_scope": ("served answers only" if row["metric"] in {"Strict unfaithfulness", "Served accuracy"}
                              else "all queries (coverage)" if row["metric"] == "Answer coverage" else "source metric scope"),
    }


def matched_entry(effect, observations):
    target, reference = (observations[effect[f"{side}_observation_id"]] for side in ("target", "reference"))
    if panel_key(target)[:2] != panel_key(reference)[:2]:
        raise ValueError("Expected source-local matched effects")
    if any(row["provenance"] != "original" or row["synthesis_exclude"] != "no" or
           row["verification"] != "verified" for row in (target, reference)):
        raise ValueError("Unexpected ineligible source")
    classes = {evidence_class(target), evidence_class(reference)}
    category = classes.pop() if len(classes) == 1 else "mixed measurement classification"
    value = read_score(effect["absolute_difference"])
    return {**descriptors(target), "protocol_block": effect["protocol_block"],
            "target_source_block": target["block_id"], "reference_source_block": reference["block_id"],
            "evidence_class": category, "cohort": effect["cohort"],
            "status": "matched", "comparison_type": effect["comparison_type"],
            "contrast_kind": effect["contrast_kind"], "baseline_observation_id": effect["baseline_observation_id"],
            "target": outcome(target), "reference": outcome(reference),
            "absolute_difference": effect["absolute_difference"], "difference_pp": effect["difference_pp"],
            "direction": effect["direction"], "directional_result": "favors target" if value > 0 else
            "favors reference" if value < 0 else "equal at printed precision", "reason": effect["comparison_reason"]}


def inventory(observations, matrix, missing=()):
    by_system = defaultdict(list)
    by_evidence = defaultdict(list)
    matched_classes = defaultdict(set)
    linked = set()
    for row in observations.values():
        by_system[system_key(row)].append(row)
    for entry in matrix:
        for side in ("target", "reference"):
            cell = entry[side]
            key = cell["registry_id"], entry["evidence_class"]
            by_evidence[key].append((entry, side))
            matched_classes[key[0]].add(key[1])
            linked.add(cell["source"]["observation_id"])
    registry, profiles, supplements = [], [], []
    for key, rows in sorted(by_system.items()):
        registry.append(identity(rows))
        groups = defaultdict(list)
        for row in rows:
            groups[evidence_class(row)].append(row)
            if row["observation_id"] not in linked:
                status = ("published outside matching" if row["provenance"] == "original"
                          and row["synthesis_exclude"] == "no" else "excluded or imported")
                supplements.append({**descriptors(row), "evidence_class": evidence_class(row),
                                    "status": status, "target": outcome(row),
                                    "reason": row["discrepancy"] or row["comparability_status"]})
        extra_classes = (groups.keys() | matched_classes[key]) - set(EVIDENCE_CLASSES)
        for category in (*EVIDENCE_CLASSES, *sorted(extra_classes)):
            source, matches = groups[category], by_evidence[key, category]
            retained_count = sum(row["provenance"] == "original" and row["synthesis_exclude"] == "no" for row in source)
            status = ("matched" if matches else "retained without eligible match" if retained_count
                      else "excluded or imported only" if source else "no verified observation")
            if not source and not matches:
                supplements.append({"paper_id": rows[0]["paper_id"], "evidence_class": category,
                                    "status": status, "target": {"registry_id": key,
                                    "configuration_id": rows[0]["configuration_id"], "system_label": rows[0]["architecture"]},
                                    "reason": "No verified endpoint in this evidence class for this configuration."})
            keys = {tuple(entry[f] for f in ("paper_id", "source_table", "protocol_block")) for entry, _ in matches}
            wins = sum(read_score(entry["absolute_difference"]) * (1 if side == "target" else -1) > 0
                       for entry, side in matches)
            ties = sum(read_score(entry["absolute_difference"]) == 0 for entry, _ in matches)
            profiles.append({"registry_id": key, "paper_id": rows[0]["paper_id"], "system_label": rows[0]["architecture"],
                             "evidence_class": category, "status": status, "verified_cells": len(source),
                             "retained_original_cells": retained_count,
                             "matched_contrast_count": len(matches), "favorable_contrasts": wins,
                             "unfavorable_contrasts": len(matches) - wins - ties, "ties": ties,
                             "matched_panels": sorted(keys), "cohorts": distinct([e for e, _ in matches], "cohort"),
                             "source_observation_ids": distinct(source, "observation_id"),
                             "matched_observation_pairs": [
                                 [entry[s]["source"]["observation_id"] for s in ("target", "reference")] for entry, _ in matches]})
    for row in missing:
        if system_key(row) in by_system:
            supplements.append({**descriptors(row), "evidence_class": evidence_class(row),
                                "status": "source value unavailable", "target": outcome(row),
                                "reason": row["discrepancy"] or row["limitations"] or "No numerical source value."})
    return registry, profiles, supplements


# Reviewed recommendation scopes. Select by study, source panel and configuration, never by the printed winner.
# Output counts describe the evidence anchor for the stated recommendation, not a score.
SCOPES = (
    ("halumem-memos", "local hallucination candidate", "halumem", "Table 3", "halumem-halu-", "-memos",
     "Direct QA rubric. Locally robust across the two linked splits. Extraction and updating are separate protocols."),
    ("sirin-mem0-faithfulness", "specialized selective intervention; trade-off", "sirin", "Table 8",
     "sirin-longmemeval-mem0:", "SIRIN Judge:+ Faithfulness gate", "Conditional unfaithfulness with lower coverage."),
    ("sirin-lightmem-faithfulness", "specialized selective intervention; trade-off", "sirin", "Table 8",
     "sirin-longmemeval-lightmem:", "SIRIN Judge:+ Faithfulness gate", "Conditional unfaithfulness with lower coverage."),
    ("sirin-mem0-both", "specialized selective intervention; trade-off", "sirin", "Table 8",
     "sirin-longmemeval-mem0:", "SIRIN Judge:+ Both gates", "Coverage and unfaithfulness can favor other gates."),
    ("sirin-lightmem-both", "specialized selective intervention; trade-off", "sirin", "Table 8",
     "sirin-longmemeval-lightmem:", "SIRIN Judge:+ Both gates", "Served accuracy improves over Judge faithfulness with lower coverage."),
    ("sirin-simplemem-both", "specialized selective intervention; distinct protocol", "sirin", "Table 5",
     "sirin-longmemeval-simplemem:", "SIRIN Judge:+ Both gates", "Matched served accuracy. Strict unfaithfulness uses the probe training label and remains conditional."),
    ("trustmem-consolidation", "specialized memory-write candidate", "trustmem", "Figure 2",
     "trustmem-mem-alpha-transition-errors-", "-trustmem", "Direct transition hallucination in Mem-α; no verified matched downstream HaluMem benefit."),
    ("memos-rootmem", "specialized implicit logic candidate", "root_memory", "Table 5", "root-memory-imlogic-", "-memos-rootmem",
     "Matched addition; forced-choice diagnostic. Preference trap remains a trade-off."),
    ("lightmem-rootmem", "specialized implicit logic candidate", "root_memory", "Table 5", "root-memory-imlogic-",
     "-lightmem-rootmem", "Largest matched accuracy gain among the RootMem additions; first-front membership depends on generic traps."),
    ("evermemos-rootmem", "specialized implicit logic candidate", "root_memory", "Table 5", "root-memory-imlogic-",
     "-evermemos-rootmem", "Improves over its own base; first-front membership depends on preference traps."),
    ("biomem-hmru-r", "specialized medical updating candidate", "biomem", "Table 4", "biomem-realmem-medical-", "-hmru-r",
     "Updating edge is tolerance-sensitive; proactive alignment can favor the baseline."),
    ("biomem-hmru-i", "specialized medical alignment candidate; trade-off", "biomem", "Table 4",
     "biomem-realmem-medical-", "-hmru-i", "Proactive-alignment recall improves; corresponding QA declines and updating QA ties."),
    ("biomem-hmru-t", "consistent local disadvantage on two selected QA objectives", "biomem", "Table 4",
     "biomem-realmem-medical-", "-hmru-t", "Updating and temporal QA disadvantage persists; some recall endpoints improve."),
    ("rmm-retrieval", "specialized long-history QA candidate", "rmm", "Table 1", "rmm-", "",
     "Only matched-retriever RMM–RAG pairs anchor this recommendation."),
    ("memgpt-retrieval", "specialized historical fact retrieval candidate", "memgpt", "Table 2", "memgpt-msc-dmr-", "-memgpt",
     "Three reader blocks share one workload. Full-history access and prompting differ from lossy summaries."),
    ("memguard-hop-expansion", "trade-off; insufficient matched evidence for downstream mitigation", "memguard", "Table 1",
     "memguard-halu-medium-memguard-", "-2-hop", "Internal comparison; the extra hop worsens reported QA and update hallucination rates."),
)


def shortlist(matrix, fronts, intervals, observations):
    selections = []
    for label, decision, paper, table, prefix, suffix, limitation in SCOPES:
        matched = []
        configurations = set()
        for entry in matrix:
            if (entry["paper_id"], entry["source_table"]) != (paper, table):
                continue
            if paper == "rmm" and entry["comparison_type"] != "matched retriever pipeline contrast":
                continue
            for side in ("target", "reference"):
                cell = entry[side]
                config = cell["configuration_id"]
                if not config.startswith(prefix) or not config.endswith(suffix):
                    continue
                if paper == "rmm" and cell["system_label"] != "RMM":
                    continue
                configurations.add(config)
                matched.append(entry)
                break
        if not matched:
            raise ValueError(f"Missing candidate anchor {label}")
        panels = sorted({entry["protocol_block"] for entry in matched})
        related_fronts = [{"panel": row["panel"], "configuration_id": row["configuration_id"], "front": row["front"]}
                          for row in fronts if row["paper_id"] == paper and row["configuration_id"] in configurations]
        selected_intervals = [row["observation_id"] for row in intervals
                              if row["paper_id"] == paper and (row["configuration_id"] in configurations
                              or ("Probe minus Judge" in row["metric"] and
                                  row["configuration_id"].replace("SIRIN Probing:", "SIRIN Judge:") in configurations))]
        if label == "biomem-hmru-r":
            selected_intervals.extend(row["observation_id"] for row in observations.values()
                                      if row["paper_id"] == paper and row["table_id"] == "Figure 7c"
                                      and "Exact paired McNemar" in row["source_details"])
        selections.append({"candidate_id": label, "decision": decision, "paper_id": paper, "source_table": table,
                           "configuration_ids": sorted(configurations), "benchmarks": distinct(matched, "benchmark"),
                           "evidence_classes": distinct(matched, "evidence_class"),
                           "n_anchor_panels": len(panels), "anchor_protocol_blocks": panels,
                           "n_cohort_labels": len(distinct(matched, "cohort")), "cohort_labels": distinct(matched, "cohort"),
                           "pareto_fronts": related_fronts, "reported_paired_statistics_source_ids": sorted(set(selected_intervals)),
                           "anchor_observation_pairs": [[entry[s]["source"]["observation_id"]
                                                        for s in ("target", "reference")] for entry in matched],
                           "anchor_observation_ids": sorted({entry[side]["source"]["observation_id"]
                                                             for entry in matched for side in ("target", "reference")}),
                           "limitations": limitation})
    return selections


HEAD_TO_HEAD = {
    "longmemeval-qa": "longmemeval-m-t3-session-GPT-4o-k5",
    "longmemeval-temporal": "longmemeval-m-temporal-session-k5",
    "halumem-medium": "halumem-medium-original",
    "halumem-long": "halumem-long-original",
    "sirin-mem0": "sirin-longmemeval-mem0",
    "sirin-lightmem": "sirin-longmemeval-lightmem",
}


def coverage_cell(row):
    if row["metric"] != "Abstain rate" or row["unit"] != "percent":
        raise ValueError("Coverage requires the published percent abstention outcome")
    abstention = read_score(row["score"])
    if abstention is None or not 0 <= abstention <= 100:
        raise ValueError("Invalid abstention rate")
    return {**outcome(row), "score": str(Decimal(100) - abstention), "score_as_printed": "",
            "source_abstention_score_as_printed": row["score_as_printed"],
            "metric_definition": "Percentage of queries served, computed as 100 minus published abstention.",
            "reported_uncertainty": {key: row[key] for key in ("sample_size", "independent_runs") if row[key]}}


def head_to_head(matrix, observations, fronts, ranks, dominance, intervals):
    complete_configs = defaultdict(set)
    for row in fronts:
        complete_configs[row["panel"]].add(row["configuration_id"])
    local_ranks = {(row["panel"], row["observation_id"]): row["rank"] for row in ranks}
    front_lookup = {(row["panel"], row["configuration_id"]): row["front"] for row in fronts}
    relationships = {(row["panel"], frozenset(row[f"{side}_configuration"] for side in ("left", "right"))): row
                     for row in dominance}

    def annotations(panel, target, reference):
        target_cfg, reference_cfg = (cell["configuration_id"] for cell in (target, reference))
        ids = (target["source"]["observation_id"], reference["source"]["observation_id"])
        relation = relationships.get((panel, frozenset((target_cfg, reference_cfg))))
        pair_result = ""
        if relation:
            leaders = [relation[f"{side}_configuration"] for side in ("left", "right")
                       if relation[f"{side}_pareto"] == "True"]
            pair_result = ("target dominates" if target_cfg in leaders else "reference dominates"
                           if leaders else "identical vectors" if not (int(relation["wins"]) or int(relation["losses"]))
                           else "trade-off")
        return {"target_rank": local_ranks.get((panel, ids[0]), ""), "reference_rank": local_ranks.get((panel, ids[1]), ""),
                "target_pareto_front": front_lookup.get((panel, target_cfg), ""),
                "reference_pareto_front": front_lookup.get((panel, reference_cfg), ""), "pareto_relationship": pair_result}

    result = []
    for panel, block in HEAD_TO_HEAD.items():
        selected = []
        for entry in matrix:
            if entry["protocol_block"] != block:
                continue
            if panel in complete_configs:
                cells = (entry["target"], entry["reference"])
                if any(cell["configuration_id"] not in complete_configs[panel] or
                       (panel, cell["source"]["observation_id"]) not in local_ranks for cell in cells):
                    continue
            selected.append(entry)
        if not selected:
            raise ValueError(f"Empty head-to-head panel {panel}")
        if panel not in complete_configs:
            vectors, directions = defaultdict(dict), {}
            for entry in selected:
                metric = entry["metric"]
                directions[metric] = entry["direction"]
                for side in ("target", "reference"):
                    cell = entry[side]
                    vectors[cell["configuration_id"]][metric] = cell["score"]
            for entry in selected:
                configs = {entry[side]["configuration_id"] for side in ("target", "reference")}
                recorded = {frozenset(e[side]["configuration_id"] for side in ("target", "reference"))
                            for e in selected if e["metric"] == entry["metric"]}
                if len(configs) != 2 or len(recorded) != len(vectors) * (len(vectors) - 1) // 2:
                    raise ValueError(f"Incomplete comparison set for {panel}")
            rank_grid = rankings(vectors, directions)
            for entry in selected:
                for side in ("target", "reference"):
                    cell = entry[side]
                    local_ranks[panel, cell["source"]["observation_id"]] = rank_grid[entry["metric"]][cell["configuration_id"]]

        for entry in selected:
            target, reference = entry["target"], entry["reference"]
            pair_intervals = []
            if panel.startswith("sirin-") and entry["metric"] == "Served accuracy":
                for row in intervals:
                    if row["configuration_id"] not in {target["configuration_id"], reference["configuration_id"]}:
                        continue
                    other = reference if row["configuration_id"] == target["configuration_id"] else target
                    if row["metric"] == "Paired served accuracy change" and other["role"] != "baseline":
                        continue
                    if row["metric"] == "Probe minus Judge paired served-accuracy change":
                        if other["configuration_id"] != row["configuration_id"].replace("SIRIN Probing:", "SIRIN Judge:"):
                            continue
                    pair_intervals.append({
                        **{field: row[field] for field in ("observation_id", "source_row", "metric", "score",
                                                          "ci_lower", "ci_upper", "unit", "limitations", "source_details")},
                        "reported_target_configuration_id": row["configuration_id"],
                        "reported_reference_configuration_id": other["configuration_id"],
                    })
            result.append({"panel": panel, **entry, **annotations(panel, target, reference),
                           "reported_paired_statistics": pair_intervals})
        if panel.startswith("sirin-"):
            rows = [row for row in observations.values() if row["block_id"] == block
                    and (panel, row["observation_id"]) in local_ranks and row["metric"] == "Abstain rate"]
            if len(rows) != len(complete_configs[panel]):
                raise ValueError(f"Incomplete coverage evidence for {panel}")
            for reference_row, target_row in combinations(rows, 2):
                target, reference = coverage_cell(target_row), coverage_cell(reference_row)
                delta = read_score(target["score"]) - read_score(reference["score"])
                result.append({"panel": panel, **descriptors(target_row), "metric": "Answer coverage",
                               "metric_definition": target["metric_definition"], "direction": "higher",
                               "denominator_scope": "all queries (coverage)", "evidence_class": OTHER,
                               "cohort": selected[0]["cohort"], "status": "Stage 2C coverage objective",
                               "comparison_type": "controlled variants", "contrast_kind": "source ordered",
                               "target": target, "reference": reference, "absolute_difference": str(delta),
                               "difference_pp": str(delta), **annotations(panel, target, reference),
                               "reason": "Stage 2C takes the complement of published abstention. No new interval inferred."})
    return result


def plot_hallucination(head_to_head_rows, figures):
    import matplotlib.pyplot as plt

    from .stage2b_figures import save

    panels = ("halumem-medium", "halumem-long")
    systems = sorted({row[side]["system_label"] for row in head_to_head_rows
                      if row["panel"] in panels for side in ("target", "reference")})
    fig, axes = plt.subplots(1, 2, sharey=True, sharex=True, figsize=(9, 3.7), layout="constrained")
    for ax, panel in zip(axes, panels):
        values = {row[side]["system_label"]: float(row[side]["score"]) for row in head_to_head_rows
                  if row["panel"] == panel and row["metric"] == "Hallucination rate" for side in ("target", "reference")}
        for i, system in enumerate(systems):
            if system not in values:
                ax.text(2, i, "Conditional comparison", va="center", fontsize=8, color="#626c77")
                continue
            value = values[system]
            ax.scatter(value, i, color="#097369" if system == "MemOS" else "#657985", s=41)
            ax.annotate(f"{value:.2f}", (value, i), xytext=(6, 0), textcoords="offset points", va="center", fontsize=8)
        ax.set(title=panel.split("-")[1].title(), xlabel="Incorrect or fabricated answers (%)", xlim=(0, 38))
        ax.set_yticks(range(len(systems)), systems)
        ax.grid(axis="x", color="#e4e9eb", linewidth=.7)
        ax.set_axisbelow(True)
    axes[0].invert_yaxis()
    fig.suptitle("HaluMem Table 3 · QA hallucination rubric\nLinked splits · points show published scores")
    with plt.rc_context({"svg.hashsalt": "cluster-b-stage2e"}):
        save(fig, figures, "stage2e_halumem_head_to_head")


def plot_evidence_coverage(matrix, figures):
    import matplotlib.pyplot as plt

    from .stage2b_figures import save

    fig, ax = plt.subplots(figsize=(8.4, 3.3), layout="constrained")
    for i, category in enumerate(EVIDENCE_CLASSES):
        rows = [row for row in matrix if row["evidence_class"] == category]
        panels = len({(row["paper_id"], row["source_table"], row["protocol_block"]) for row in rows})
        cohorts = len(distinct(rows, "cohort"))
        for count, offset, color, label in ((panels, -.14, "#336c92", "Protocol × source table"),
                                             (cohorts, .14, "#9b5527", "Potentially dependent cohort labels")):
            ax.scatter(count, i + offset, color=color, s=40, label=label if i == 0 else None)
            ax.annotate(str(count), (count, i + offset), xytext=(6, 0), textcoords="offset points",
                        va="center", color=color, fontsize=9)
    ax.set_yticks(range(len(EVIDENCE_CLASSES)), [label.capitalize() for label in EVIDENCE_CLASSES])
    ax.set(xlabel="Distinct labels within evidence class", xlim=(0, ax.get_xlim()[1] * 1.13))
    ax.invert_yaxis()
    ax.grid(axis="x", color="#e4e9eb", linewidth=.7)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="upper right", fontsize=8)
    ax.set_title("Coverage of matched evidence\nPanel and cohort counts are descriptive",
                 loc="left", fontsize=12)
    with plt.rc_context({"svg.hashsalt": "cluster-b-stage2e"}):
        save(fig, figures, "stage2e_matched_evidence_coverage")


def run(root=ROOT):
    data, results = root / "data", root / "results"
    observations = {row["observation_id"]: row for row in read(data / "validated_results.csv")}
    effects = read(results / "matched_effect_sizes.csv")
    matrix = [matched_entry(effect, observations) for effect in effects]
    missing = [row for row in read(data / "raw_results.csv") if row["verification"] == "missing"]
    registry, profiles, supplements = inventory(observations, matrix, missing)
    fronts, ranks, dominance, intervals = (read(results / f"{name}.csv") for name in (
        "pareto_fronts", "within_panel_rankings", "dominance_relations", "pareto_reported_uncertainty"))
    selected = shortlist(matrix, fronts, intervals, observations)
    head = head_to_head(matrix, observations, fronts, ranks, dominance, intervals)
    write_rows(data / "architecture_registry.csv", registry)
    for name, rows in (("architecture_evidence_profiles", profiles), ("candidate_shortlist", selected),
                       ("final_failure_mode_matrix", matrix + supplements), ("head_to_head_benchmark_comparisons", head)):
        write_rows(results / f"{name}.csv", rows)
    plot_hallucination(head, root / "figures")
    plot_evidence_coverage(matrix, root / "figures")
    print(f"{len(registry)} configuration records; {len(matrix)} matched contrasts; {len(matrix + supplements)} matrix entries; "
          f"{len(selected)} reviewed decisions; {len(head)} head-to-head rows.")


if __name__ == "__main__":
    run()
