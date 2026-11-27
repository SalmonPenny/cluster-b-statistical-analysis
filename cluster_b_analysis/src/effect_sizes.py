"""Compute descriptive matched effects and regenerate the Stage 2A outputs.

Run from the repository root with python -m cluster_b_analysis.src.effect_sizes.
"""

import csv
import json
from dataclasses import dataclass
from decimal import Decimal

from .data_loading import ROOT, SOURCE_FIELDS, load_matched_pairs, read_score


@dataclass(frozen=True)
class Score:
    value: Decimal | float | int | None
    unit: str


def score_values(target, reference):
    if not target.unit or target.unit != reference.unit:
        raise ValueError("Scores must use the same known unit")
    values = read_score(target.value), read_score(reference.value)
    ceiling = {"percent": 100, "proportion": 1}.get(target.unit)
    if ceiling is not None and any(v is not None and not 0 <= v <= ceiling for v in values):
        raise ValueError("Rate scores must fall within their unit bounds")
    return values


def absolute_difference(target, reference, direction):
    """Direction-adjusted difference in the original unit, positive if better."""
    a, b = score_values(target, reference)
    if a is None or b is None or direction not in {"higher", "lower"}:
        return None
    return a - b if direction == "higher" else b - a


def percentage_point_difference(target, reference, direction):
    delta = absolute_difference(target, reference, direction)
    if delta is None or target.unit not in {"percent", "proportion"}:
        return None
    return delta * (100 if target.unit == "proportion" else 1)


def relative_improvement(target, baseline, direction, *, ratio_scale):
    """Relative performance change as a fraction on an explicitly supported scale."""
    delta = absolute_difference(target, baseline, direction)
    a, b = score_values(target, baseline)
    if not ratio_scale or delta is None or b <= 0 or a < 0:
        return None
    return delta / b


def relative_error_reduction(target, baseline, *, error_complement):
    """Relative reduction of 1 − correctness on a bounded correctness rate."""
    delta = percentage_point_difference(target, baseline, "higher")
    if not error_complement or delta is None:
        return None
    _, b = score_values(target, baseline)
    remaining = (100 - b) if target.unit == "percent" else (1 - b) * 100
    return delta / remaining if remaining > 0 else None


def relative_event_reduction(target, baseline, *, direct_undesirable_rate):
    """Relative reduction of a directly measured, lower-is-better event rate."""
    if not direct_undesirable_rate or target.unit not in {"percent", "proportion"}:
        return None
    return relative_improvement(target, baseline, "lower", ratio_scale=True)


# These source-specific accuracy metrics have a documented correctness denominator.
CORRECTNESS_METRICS = {
    ("rmm", "Accuracy"), ("longmemeval", "Accuracy"), ("memguard", "Accuracy"),
    ("halumem", "Accuracy"), ("mragent", "LLM-Judge"), ("telemem", "LLM-Judge"),
    ("telemem", "QA Accuracy"), ("sirin", "Served accuracy"),
}


def effect_row(pair):
    reference, target = pair.left, pair.right
    baseline_relative = (reference["role"] == "baseline") != (target["role"] == "baseline")
    if baseline_relative and target["role"] == "baseline":
        reference, target = target, reference
    a, b = (Score(read_score(row["score"]), row["unit"]) for row in (target, reference))
    direction = target["direction"]
    identification = (target["paper_id"], target["metric"])
    correctness = direction == "higher" and identification in CORRECTNESS_METRICS
    direct_bad_event = direction == "lower" and all(
        row["hallucination_measurement"] == "direct"
        and row["metric"] in {"Hallucination rate", "Strict unfaithfulness"}
        for row in (target, reference)
    )
    ratio_scale = correctness or a.unit in {"tokens", "thousands of tokens", "seconds"}
    relative = error = event = None
    if baseline_relative:
        relative = relative_improvement(a, b, direction, ratio_scale=ratio_scale)
        error = relative_error_reduction(a, b, error_complement=correctness)
        event = relative_event_reduction(a, b, direct_undesirable_rate=direct_bad_event)
    return {
        "contrast_kind": "baseline_relative" if baseline_relative else "pairwise",
        "baseline_observation_id": reference["observation_id"] if baseline_relative else "",
        "comparison_type": pair.comparison["evidence_type"],
        "comparison_reason": pair.comparison["reason"],
        "protocol_block": pair.protocol_block,
        "cohort": pair.cohort,
        **{key: target[key] for key in ("paper_id", "table_id", "benchmark", "benchmark_version",
                                        "split", "task", "metric", "unit", "direction")},
        "absolute_difference": absolute_difference(a, b, direction),
        "difference_pp": percentage_point_difference(a, b, direction),
        "relative_performance_improvement_pct": None if relative is None else relative * 100,
        "relative_error_reduction_pct": None if error is None else error * 100,
        "relative_undesirable_event_reduction_pct": None if event is None else event * 100,
        **{f"{side}_{field}": row[field] for side, row in (("reference", reference), ("target", target))
           for field in SOURCE_FIELDS},
    }


def rmm_example(rows):
    """Select Table 1 LongMemEval accuracy contrasts with matched retrievers."""
    panel = {}
    for row in rows:
        if (row["paper_id"], row["table_id"], row["benchmark"], row["metric"],
                row["comparison_type"], row["contrast_kind"]) != (
                    "rmm", "Table 1", "LongMemEval", "Accuracy",
                    "matched retriever pipeline contrast", "baseline_relative"):
            continue
        retriever = json.loads(row["reference_source_details"])["retriever"]
        if retriever in panel:
            raise ValueError(f"Duplicate RMM example contrast for {retriever}")
        panel[retriever] = row
    gte = panel["GTE"]
    if (Decimal(gte["reference_score"]), Decimal(gte["target_score"]), gte["difference_pp"]) != (
            Decimal("63.6"), Decimal("70.4"), Decimal("6.8")):
        raise ValueError("RMM GTE worked example disagrees with the expected source values")
    return panel


def plot_example(panel, destination):
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    names = list(panel)
    differences = [float(row["difference_pp"]) for row in panel.values()]
    fig, ax = plt.subplots(figsize=(6.1, 2.9), layout="constrained")
    ax.barh(names, differences, height=.48, color="#16716c")
    ax.invert_yaxis()
    for i, value in enumerate(differences):
        ax.text(value + .09, i, f"{value:+.1f} pp", va="center")
    ax.set(xlim=(0, max(differences) + 1.4),
           xlabel="RMM minus RAG accuracy (percentage points)")
    ax.set_title("LongMemEval accuracy by matched retriever\nRMM Table 1 · descriptive contrasts",
                 loc="left", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(destination, dpi=170)
    plt.close(fig)


def main():
    rows = [effect_row(pair) for pair in load_matched_pairs()]
    panel = rmm_example(rows)
    path = ROOT / "results" / "matched_effect_sizes.csv"
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    plot_example(panel, ROOT / "figures" / "matched_effect_sizes_example.png")
    baseline_count = sum(row["contrast_kind"] == "baseline_relative" for row in rows)
    print(f"{len(rows)} eligible contrasts; {baseline_count} baseline-relative; "
          f"{len(rows) - baseline_count} pairwise; "
          f"{len({row['cohort'] for row in rows})} cohort groups.")


if __name__ == "__main__":
    main()
