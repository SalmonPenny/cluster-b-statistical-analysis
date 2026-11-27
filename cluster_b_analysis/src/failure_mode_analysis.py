"""Build protocol-specific failure-mode evidence from the saved Stage 2A contrasts.

Run from the repository root: python -m cluster_b_analysis.src.failure_mode_analysis
"""

from collections import defaultdict
import csv
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

from .aggregation import aggregate
from .data_loading import ROOT, load_matched_pairs, read_csv, read_score


@dataclass(frozen=True)
class FailureMode:
    label: str
    mapping_task: str
    mapping_metric: str = ""


def failure_mode(benchmark, task, metric):
    """Map reviewed outcome/task combinations to the Stage 1 benchmark crosswalk."""
    task_key = " ".join(task.casefold().replace("-", " ").split())
    metric_key = metric.casefold()
    if benchmark == "LoCoMo":
        if metric_key not in {"accuracy", "llm-judge", "answer f1", "constraint-consistency judge score"}:
            return None
        if task_key == "overall" and metric_key == "answer f1":
            # Only the explicitly feedback-conditioned panel is mapped by the caller.
            return FailureMode("Factual recall and response revision", "MemoryBench full LoCoMo feedback experiment")
        return {
            "single hop": FailureMode("Single-hop recall", "Single-hop"),
            "multi hop": FailureMode("Multi-hop evidence synthesis", "Multi-hop"),
            "temporal": FailureMode("Temporal reasoning", "Temporal"),
            "open domain": FailureMode("Dialogue grounding and external knowledge", "Open-domain"),
            "adversarial": FailureMode("False-premise rejection", "Adversarial"),
        }.get(task_key)
    if benchmark == "LoCoMo-Plus" and task_key == "cognitive awareness" and metric_key == "constraint-consistency judge score":
        return FailureMode("Latent constraint application", "Causal, state, goal and value constraints")
    if benchmark == "LongMemEval":
        if metric_key.startswith("recall@"):
            return FailureMode("Evidence retrieval", "Overall and evidence retrieval")
        if metric_key == "strict unfaithfulness":
            return FailureMode("Unsupported or contradictory answers", "Selective prediction among served answers",
                               "Strict unfaithfulness")
        if metric_key not in {"accuracy", "llm-judge", "served accuracy"}:
            return None
        scope = {
            "single": FailureMode("Single-session recall", "Single-session user; single-session assistant"),
            "single session user": FailureMode("Single-session recall", "Single-session user; single-session assistant"),
            "single session assistant": FailureMode("Single-session recall", "Single-session user; single-session assistant"),
            "single session preference": FailureMode("Preference retention and use", "Single-session preference"),
            "multi": FailureMode("Cross-session reasoning", "Multi-session"),
            "multi session": FailureMode("Cross-session reasoning", "Multi-session"),
            "temporal": FailureMode("Temporal reasoning", "Temporal reasoning"),
            "temporal reasoning": FailureMode("Temporal reasoning", "Temporal reasoning"),
            "knowledge update": FailureMode("Memory updating", "Knowledge update"),
            "abstention": FailureMode("False-premise rejection", "Abstention"),
        }.get(task_key)
        if scope and metric_key == "served accuracy":
            return FailureMode(scope.label, "Selective prediction among served answers", "Served accuracy; abstain rate")
        return scope
    if benchmark == "MemBench" and metric_key == "memory accuracy":
        labels = {
            "preference": "Preference retention and use", "emotion": "Emotional state recall",
            "single hop": "Single-hop recall", "multi hop": "Multi-hop evidence synthesis",
            "comparative": "Comparative memory reasoning", "aggregative": "Memory aggregation",
            "post processing": "Post-processing of retrieved information", "knowledge update": "Memory updating",
            "single session assistant": "Single-session recall", "multi session assistant": "Cross-session reasoning",
        }
        if task_key in labels:
            return FailureMode(labels[task_key], "MemBench annotated subtypes")
    if benchmark == "ES-MemEval":
        if metric_key in {"answer f1", "bertscore", "llm-judge"}:
            labels = {
                "information extraction": "Recall of personal disclosures", "temporal reasoning": "Temporal reasoning",
                "conflict detection": "Conflicting-memory detection", "abstention": "Abstention under unavailable evidence",
                "user modeling": "Personalized user-state modeling",
            }
            if task_key in labels:
                return FailureMode(labels[task_key], "Emotional support memory QA")
        if task_key == "dialogue generation" and metric_key in {"observation recall", "observation weighted score",
                                                                  "long-term memory rating", "personalization rating"}:
            return FailureMode("Personal disclosures used in support dialogue", "Observation and personalization in support dialogue")
    if benchmark == "IMLogic":
        return {
            "preference trap rate": FailureMode("Semantic deflection by recalled preferences", "IMLogic distractor choices", "Preference trap rate"),
            "generic trap rate": FailureMode("Failure to personalize from evidence", "IMLogic distractor choices", "Generic trap rate"),
            "fabrication trap rate": FailureMode("Fabricated alternative selection", "IMLogic distractor choices", "Fabrication trap rate"),
            "accuracy": FailureMode("Implicit logical memory utilization", "Memory and conversation MCQ"),
        }.get(metric_key)
    if benchmark == "TWIST":
        return {
            "contradiction recall": FailureMode("Missed contradictions", "Validated draft alignment"),
            "grounded contradiction recall": FailureMode("Missed evidence-grounded contradictions", "Validated draft alignment"),
            "hard-negative specificity": FailureMode("Restraint on aligned hard negatives", "Validated draft alignment"),
            "aligned specificity": FailureMode("Restraint on aligned drafts", "Validated draft alignment"),
            "conditional attribution accuracy": FailureMode("Evidence attribution on flagged drafts", "Validated draft alignment"),
        }.get(metric_key)
    if benchmark == "HaluMem":
        if task_key == "memory extraction":
            if metric_key in {"extraction accuracy", "false memory resistance"}:
                return FailureMode("Unsupported writes and distractor memories", "Memory extraction",
                                   "Extraction Accuracy; False Memory Resistance")
            if metric_key == "target precision":
                return FailureMode("Target-matched write correctness", "Memory extraction",
                                   "Target Memory Precision")
            if metric_key == "weighted recall":
                return FailureMode("Reference memory retention", "Memory extraction", "Weighted Recall")
            if metric_key in {"recall", "f1"}:
                return FailureMode("Memory extraction and retention", "Memory extraction",
                                   "Memory Recall; Extraction F1")
        if task_key == "memory updating":
            if metric_key == "hallucination rate":
                return FailureMode("Incorrect or hallucinated memory changes", "Memory updating",
                                   "Updating Hallucination Rate")
            if metric_key in {"accuracy", "omission rate"}:
                return FailureMode("Memory updating", "Memory updating", "Updating Accuracy; Omission Rate")
        if task_key == "question answering":
            return {
                "hallucination rate": FailureMode("Benchmark-defined incorrect or fabricated answers", "Memory QA",
                                                  "QA Hallucination Rate"),
                "omission rate": FailureMode("Missing answer evidence", "Memory QA", "QA Accuracy; Omission Rate"),
            }.get(metric_key)
    if benchmark == "PerLTQA" and task_key == "question answering" and metric_key == "accuracy":
        return FailureMode("Personalized memory recall", "Personalized long-term QA")
    if benchmark == "RealMem":
        if metric_key == "memory recall" or metric_key.startswith(("recall@", "ndcg@")):
            return FailureMode("Evidence retrieval", "Project-based interaction")
        if metric_key == "qa score":
            return {
                "question answering": FailureMode("Project-state tracking", "Project-based interaction"),
                "dynamic incremental": FailureMode("Project-state accumulation", "Project-based interaction"),
                "dynamic updating": FailureMode("Memory updating", "Project-based interaction"),
                "proactive alignment": FailureMode("Proactive alignment", "Project-based interaction"),
                "temporal reasoning": FailureMode("Temporal reasoning", "Project-based interaction"),
                "single session": FailureMode("Single-session reasoning", "Project-based interaction"),
                "multi session": FailureMode("Cross-session reasoning", "Project-based interaction"),
            }.get(task_key)
    if benchmark == "Mem-α validation set" and task_key == "memory consolidation transition":
        return {
            "hallucination rate": FailureMode("Unsupported memory construction", "Memory consolidation transition",
                                              "Hallucination rate"),
            "omission rate": FailureMode("Missing memory evidence", "Memory consolidation transition",
                                         "Omission rate; corruption rate"),
            "corruption rate": FailureMode("Memory corruption", "Memory consolidation transition",
                                           "Omission rate; corruption rate"),
        }.get(metric_key)
    return None


def mapped_failure(row):
    """Keep broad endpoints outside the failure-specific matrix."""
    mode = failure_mode(row["benchmark"], row["task"], row["metric"])
    if not mode:
        return None
    if mode.label == "Factual recall and response revision" and row["paper_id"] != "memorybench":
        return None
    if row["benchmark"] == "RealMem" and row["paper_id"] == "biomem":
        return FailureMode(mode.label, "Medical subset, dynamic increment and updating, proactive alignment and temporal reasoning")
    return mode


def mapping_metadata(mode, benchmark, crosswalk):
    if mode is None:
        return {"failure_mode": "", "mapping_source": "", "mapping_interpretation": "", "taxonomy": ""}
    candidates = [
        row for row in crosswalk if row["benchmark"] == benchmark and row["task_or_subset"] == mode.mapping_task
        and (not mode.mapping_metric or row["metric"] == mode.mapping_metric)
    ]
    if len(candidates) != 1:
        raise ValueError(f"Expected a single crosswalk entry for {benchmark}: {mode}")
    item = candidates[0]
    return {"failure_mode": mode.label, "mapping_source": item["source_locator"],
            "mapping_interpretation": item["interpretation"], "taxonomy": item["taxonomy"]}


def scope(target, reference):
    if (target["role"] == "baseline") != (reference["role"] == "baseline"):
        return "baseline_relative"
    mode = mapped_failure(target)
    paired_abstention = (target["benchmark"] == "LoCoMo" and mode
                         and mode.label == "False-premise rejection"
                         and target["hallucination_measurement"] == reference["hallucination_measurement"] == "direct")
    if (target["architecture"] != reference["architecture"] and mode is not None
            and (target["benchmark"] in {"HaluMem", "LoCoMo-Plus", "RealMem", "IMLogic", "TWIST", "MemBench", "ES-MemEval"} or paired_abstention)):
        return "source_ordered_pair"
    return ""


def measurement(target, reference, mode):
    source_classes = {target["hallucination_measurement"], reference["hallucination_measurement"]}
    if source_classes == {"direct"}:
        if target["metric"].casefold() in {"hallucination rate", "strict unfaithfulness"}:
            return "direct hallucination or unfaithfulness rubric"
        return "direct task diagnostic"
    if "direct" in source_classes:
        return "mixed source classification"
    return "memory-performance proxy" if mode or "proxy" in source_classes else "other outcome"


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stratum_id(context):
    """Digest of the full compatibility key, with context also persisted in the CSV."""
    return hashlib.sha256(encode(context).encode()).hexdigest()


def context_for(effect, target, reference, mode, kind):
    """Keep each exact, documented comparison context intact.

    No Stage 1 designation establishes compatibility beyond its source protocol.
    Configuration IDs identify actual versions and conditions inside that protocol.
    """
    context = {k: effect[k] for k in ("paper_id", "table_id", "benchmark", "benchmark_version", "split", "task",
                                      "metric", "unit", "direction", "comparison_type", "protocol_block")}
    context.update(contrast_kind=kind, measurement_scope=measurement(target, reference, mode))
    for side, row in (("target", target), ("reference", reference)):
        for field in ("architecture", "configuration_id", "architecture_version", "rq2_category",
                      "metric_definition", "backbone", "judge", "hallucination_measurement",
                      "judging_protocol", "retrieval_budget", "memory_budget", "context_budget", "mechanisms"):
            context[f"{side}_{field}"] = row[field]
        context[f"{side}_source_row"] = row["source_row"]
        details = json.loads(row.get("source_details") or "{}")
        context[f"{side}_protocol_modifiers"] = {
            field: details[field] for field in ("retriever", "retriever_model", "detector", "feedback_condition")
            if field in details
        }
    return context


def effect_value(row):
    """Use the reported-unit contrast, preferring percentage points on a rate scale."""
    unit = "percentage points" if row["difference_pp"] else row["unit"]
    number = read_score(row["difference_pp"] or row["absolute_difference"])
    return unit, None if number is None else float(number)


def load_profiles(data_dir, effect_path):
    crosswalk = list(read_csv(data_dir / "benchmark_failure_mode_mapping.csv",
                             ("benchmark", "task_or_subset", "metric", "taxonomy", "source_locator", "interpretation")))
    pairs = {frozenset((p.left["observation_id"], p.right["observation_id"])): p
             for p in load_matched_pairs(data_dir)}
    matched = []
    evidence = []
    metadata = {}
    seen = set()
    for effect in read_csv(effect_path, ("target_observation_id", "reference_observation_id",
                                        "contrast_kind", "protocol_block", "cohort", "absolute_difference",
                                        "difference_pp", "baseline_observation_id")):
        ids = frozenset((effect["target_observation_id"], effect["reference_observation_id"]))
        if ids in seen or ids not in pairs:
            raise ValueError(f"Duplicate or ineligible Stage 2A source pair {sorted(ids)}")
        seen.add(ids)
        pair = pairs[ids]
        observations = {r["observation_id"]: r for r in (pair.left, pair.right)}
        target, reference = (observations[effect[f"{side}_observation_id"]] for side in ("target", "reference"))
        if (effect["protocol_block"], effect["cohort"], effect["comparison_type"]) != (
                pair.protocol_block, pair.cohort, pair.comparison["evidence_type"]):
            raise ValueError(f"Stale Stage 2A comparison labels for {sorted(ids)}")
        for side, row in (("target", target), ("reference", reference)):
            if any(effect[k] != row[k] for k in ("paper_id", "benchmark", "benchmark_version", "split",
                                                "task", "metric", "unit", "direction")):
                raise ValueError(f"Stale {side} outcome fields for {sorted(ids)}")
            if any(effect[f"{side}_{k}"] != row[k] for k in ("score", "role", "configuration_id", "architecture")):
                raise ValueError(f"Stale {side} observation for {sorted(ids)}")
        mode = mapped_failure(target)
        kind = scope(target, reference)
        expected_kind = "baseline_relative" if kind == "baseline_relative" else "pairwise"
        expected_baseline = reference["observation_id"] if kind == "baseline_relative" else ""
        if (effect["contrast_kind"], effect["baseline_observation_id"]) != (expected_kind, expected_baseline):
            raise ValueError(f"Inconsistent Stage 2A orientation for {sorted(ids)}")
        if kind == "baseline_relative" and reference["role"] != "baseline":
            raise ValueError(f"Explicit baseline must be the reference for {sorted(ids)}")
        if expected_kind == "pairwise" and target["observation_id"] != pair.right["observation_id"]:
            raise ValueError(f"Pairwise contrast reverses Stage 2A source order for {sorted(ids)}")
        if not kind:
            continue
        context = context_for(effect, target, reference, mode, kind)
        effect_unit, value = effect_value(effect)
        outcome = mapping_metadata(mode, effect["benchmark"], crosswalk)
        context.update(effect_unit=effect_unit, **outcome)
        stratum = stratum_id(context)
        metadata[stratum] = context
        pair_fields = {
            "stratum": stratum, "study": effect["paper_id"], "cohort": effect["cohort"],
            "protocol": effect["protocol_block"], "endpoint": stratum, "effect": value,
            "target_observation_id": target["observation_id"], "reference_observation_id": reference["observation_id"],
        }
        matched.append(pair_fields)
        evidence.append({
            **effect, "profile_stratum": stratum, "profile_effect_unit": effect_unit,
            "profile_effect": value, "profile_contrast_kind": kind,
            "profile_measurement_scope": context["measurement_scope"], **outcome,
            "profile_status": "eligible" if value is not None else "missing estimate",
        })
    if seen != pairs.keys():
        raise ValueError("Saved Stage 2A table does not cover all eligible source pairs")
    return matched, evidence, metadata


def compatibility_audit(rows, metadata):
    """Test whether dropping locality IDs exposes candidate matches, without pooling them."""
    excluded = {"paper_id", "table_id", "protocol_block", "target_configuration_id",
                "reference_configuration_id", "target_source_row", "reference_source_row",
                "mapping_source", "mapping_interpretation"}
    buckets = defaultdict(list)
    for row in rows:
        context = metadata[row["stratum"]]
        if context["contrast_kind"] == "baseline_relative" and row["effect"] is not None:
            key = encode({k: v for k, v in context.items() if k not in excluded})
            buckets[key].append(row)
    return {
        "candidate_scopes": len(buckets),
        "multicontrast_scopes": sum(len(group) > 1 for group in buckets.values()),
        "cross_cohort_scopes": sum(len({r["cohort"] for r in group}) > 1 for group in buckets.values()),
        "cross_study_scopes": sum(len({r["study"] for r in group}) > 1 for group in buckets.values()),
    }


def coverage_exceptions(data_dir, included_ids):
    """Expose documented unavailable candidates without numerical substitution."""
    raw = {row["observation_id"]: row for row in read_csv(data_dir / "raw_results.csv",
            ("observation_id", "benchmark", "task", "metric", "paper_id", "role", "architecture",
             "configuration_id", "synthesis_exclude", "provenance", "verification"))}
    for row in read_csv(data_dir / "comparability.csv", ("comparison_level", "left_observation",
                                                        "right_observation", "status", "reason")):
        if row["comparison_level"] != "within_block":
            continue
        ids = row["left_observation"], row["right_observation"]
        if frozenset(ids) in included_ids:
            continue
        left, right = (raw[i] for i in ids)
        target, reference = (right, left) if left["role"] == "baseline" else (left, right)
        kind = scope(target, reference)
        if kind == "source_ordered_pair":
            target, reference = right, left
        mode = mapped_failure(target)
        if not kind or not mode:
            continue
        status = row["status"]
        reason = row["reason"]
        if status == "Directly comparable":
            status = "Source ineligible"
            reason = "; ".join(
                f"{obs['observation_id']}: {obs['verification']}/{obs['provenance']}/exclude={obs['synthesis_exclude']}"
                for obs in (target, reference)
            )
        yield {"coverage_status": status, "failure_mode": mode.label, "contrast_kind": kind,
               **{key: target[key] for key in ("paper_id", "table_id", "benchmark", "benchmark_version", "split", "task", "metric")},
               "protocol_block": row["left_block"] if row["left_block"] == row["right_block"] else
                                 f"{row['left_block']} | {row['right_block']}",
               "target_architecture": target["architecture"], "reference_architecture": reference["architecture"],
               "target_configuration_id": target["configuration_id"],
               "reference_configuration_id": reference["configuration_id"], "comparison_reason": reason,
               "target_observation_id": target["observation_id"], "reference_observation_id": reference["observation_id"]}


def write_rows(path, rows):
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: encode(v) if isinstance(v, (tuple, list, dict)) else v
                          for key, v in row.items()} for row in rows)


def run(data_dir=ROOT / "data", results_dir=ROOT / "results", figures_dir=ROOT / "figures"):
    from .stage2b_figures import render

    matched, evidence, metadata = load_profiles(Path(data_dir), Path(results_dir) / "matched_effect_sizes.csv")
    protocols, cohorts, profiles = aggregate(matched)
    profiles = [
        {**metadata[row["stratum"]], **row,
         "aggregation_method": "equal protocols within cohort, then equal observed cohorts",
         "evidence_strength": ("single protocol panel" if row["n_protocols"] == 1 else
                               "multiple protocols, single cohort" if row["n_cohorts"] == 1 else
                               "multiple potentially dependent cohorts")}
        for row in profiles
    ]
    failure_profiles = [row for row in profiles if row["failure_mode"]]
    observed_ids = {frozenset((r["target_observation_id"], r["reference_observation_id"]))
                    for r in evidence if r["profile_status"] == "eligible"}
    coverage_keys = (
        "stratum", "failure_mode", "contrast_kind", "paper_id", "benchmark", "benchmark_version", "split",
        "task", "metric", "protocol_block", "target_architecture", "reference_architecture",
        "target_configuration_id", "reference_configuration_id", "measurement_scope", "n_observations",
        "n_source_observations", "n_protocols", "n_studies", "n_cohorts", "observation_pairs",
    )
    coverage = [{**{key: row[key] for key in coverage_keys}, "coverage_status": "Available"}
                for row in failure_profiles]
    coverage.extend(coverage_exceptions(Path(data_dir), observed_ids))
    weighting_keys = (
        "stratum", "benchmark", "task", "metric", "failure_mode", "target_architecture",
        "reference_architecture", "effect_unit", "n_observations", "n_protocols", "n_studies", "n_cohorts",
        "observation_weighted_mean", "protocol_weighted_mean", "study_balanced_mean", "cohort_balanced_mean",
    )
    weighting = [{key: row[key] for key in weighting_keys} for row in profiles]
    for name, rows in (
        ("protocol_level_summary", [{**metadata[r["stratum"]], **r} for r in protocols]),
        ("cohort_level_summary", [{**metadata[r["stratum"]], **r} for r in cohorts]),
        ("benchmark_performance_profiles", profiles),
        ("architecture_failure_mode_profiles", failure_profiles),
        ("failure_mode_evidence_coverage", coverage),
        ("weighting_comparison", weighting),
        ("stage2b_source_contrasts", evidence),
    ):
        write_rows(Path(results_dir) / f"{name}.csv", rows)
    render(failure_profiles, profiles, Path(figures_dir))
    print("Locality-free compatibility audit:", compatibility_audit(matched, metadata))
    print(f"{len(evidence)} selected contrasts, {len(profiles)} benchmark profiles, "
          f"{len(failure_profiles)} failure-mode profiles, {len(coverage)} coverage entries.")


if __name__ == "__main__":
    run()
