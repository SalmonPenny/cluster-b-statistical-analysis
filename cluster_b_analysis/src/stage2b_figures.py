"""Render compatible result panels and a separate matrix of evidence counts."""

from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np


def save(fig, directory, stem):
    for extension in ("png", "svg"):
        metadata = {"Date": None} if extension == "svg" else {}
        fig.savefig(directory / f"{stem}.{extension}", dpi=170, metadata=metadata)
    plt.close(fig)


def bio_panel(rows, directory):
    targets = ("HMRU-R", "HMRU-I", "HMRU-T")
    tasks = ("Dynamic incremental", "Dynamic updating", "Proactive alignment", "Temporal reasoning",
             "Single-session", "Multi-session")
    cells = {}
    for row in rows:
        if (row["paper_id"], row["table_id"], row["metric"]) == ("biomem", "Table 4", "QA Score"):
            key = row["target_source_row"], row["task"]
            if key in cells:
                raise ValueError(f"Ambiguous BioMem figure cell {key}")
            cells[key] = row
    values = np.array([[cells[a, t]["cohort_balanced_mean"] if (a, t) in cells else np.nan
                        for t in tasks] for a in targets])
    palette = plt.get_cmap("RdBu").copy()
    palette.set_bad("#e6e9ec")
    bound = np.nanmax(np.abs(values)) or 1
    fig, ax = plt.subplots(figsize=(9, 3.3), layout="constrained")
    heat = ax.imshow(values, cmap=palette, norm=TwoSlopeNorm(vcenter=0, vmin=-bound, vmax=bound), aspect="auto")
    ax.set_xticks(range(len(tasks)), [t.replace(" ", "\n", 1) for t in tasks], fontsize=9)
    ax.set_yticks(range(len(targets)), targets)
    for i, target in enumerate(targets):
        for j, task in enumerate(tasks):
            cell = cells.get((target, task))
            val = values[i, j]
            label = "—" if cell is None else f"{val:+.2f}\n{cell['n_cohorts']} cohort"
            ax.text(j, i, label, ha="center", va="center", fontsize=8.5,
                    color="white" if abs(val) > bound * .65 else "#18232d")
    fig.colorbar(heat, ax=ax, label="Change in QA score (percentage points)")
    ax.set_title("RealMem medical subset · HMRU variants versus A-Mem\nBioMem Table 4 · HuatuoGPT-3-27B, GPT-4o-mini judge",
                 loc="left", fontsize=11)
    save(fig, directory, "stage2b_failure_mode_heatmap")


def coverage_panel(rows, directory):
    counts = defaultdict(set)
    for row in rows:
        counts[row["target_architecture"], row["failure_mode"]].update(row["cohorts"])
    systems = sorted({system for system, _ in counts}, key=str.casefold)
    modes = sorted({mode for _, mode in counts})
    values = np.array([[len(counts[system, mode]) for mode in modes] for system in systems], dtype=float)
    values[values == 0] = np.nan
    palette = plt.get_cmap("YlGnBu").copy()
    palette.set_bad("#e9edf0")
    fig, ax = plt.subplots(figsize=(max(10, len(modes) * .52), max(4.5, len(systems)*.27 + 2.3)),
                           layout="constrained")
    image = ax.imshow(values, cmap=palette, vmin=0, vmax=max(1, np.nanmax(values)), aspect="auto")
    ax.set_xticks(range(len(modes)), modes, rotation=55, ha="right", fontsize=8)
    ax.set_yticks(range(len(systems)), systems, fontsize=8)
    for i, row in enumerate(values):
        for j, count in enumerate(row):
            ax.text(j, i, "—" if np.isnan(count) else str(int(count)), ha="center", va="center", fontsize=7,
                    color="white" if count > .75 * np.nanmax(values) else "#263846")
    fig.colorbar(image, ax=ax, label="Distinct cohort labels")
    ax.set_title("Failure-mode evidence coverage by target system label\nCounts combine eligibility across strata. Dashes mark no eligible target cell.",
                 loc="left", fontsize=11)
    save(fig, directory, "stage2b_failure_mode_coverage")


def weighting_panel(rows, directory):
    selection = {row["reference_source_row"].split(" | ")[-1]: row for row in rows
                 if (row["paper_id"], row["table_id"], row["benchmark"], row["metric"], row["comparison_type"])
                 == ("rmm", "Table 1", "LongMemEval", "Accuracy", "matched retriever pipeline contrast")}
    names = ("Contriever", "Stella", "GTE")
    y = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(7.2, 3.25), layout="constrained")
    for position, name in enumerate(names):
        row = selection[name]
        ax.text(max(row["cohort_balanced_mean"], row["observation_weighted_mean"]) + .16, position,
                f"{row['n_protocols']} block · {row['n_cohorts']} cohort", va="center", fontsize=8.5)
    ax.scatter([selection[n]["observation_weighted_mean"] for n in names], y,
               color="#1b6769", marker="o", s=79, label="Observation-weighted")
    ax.scatter([selection[n]["cohort_balanced_mean"] for n in names], y,
               marker="x", color="#d97a3a", s=47, zorder=4, label="Cohort-balanced")
    ax.set(xlim=(0, 9), ylim=(2.6, -.6), yticks=y, yticklabels=names,
           xlabel="RMM minus RAG accuracy (percentage points)")
    ax.legend(loc="lower left", frameon=False)
    ax.set_title("Weighting comparison within the RMM matched-retriever panel\nEach retriever remains a separate estimand",
                 loc="left", fontsize=10.5)
    save(fig, directory, "stage2b_weighting_comparison")


def sirin_panel(rows, directory):
    selected = [row for row in rows if (row["paper_id"], row["target_architecture"], row["metric"],
                                         row["contrast_kind"]) ==
                ("sirin", "Mem0", "Strict unfaithfulness", "baseline_relative")]
    selected.sort(key=lambda row: row["target_source_row"])
    names = [row["target_source_row"].removeprefix("Mem0 | ").replace(" | + ", " · ") for row in selected]
    values = [row["cohort_balanced_mean"] for row in selected]
    fig, ax = plt.subplots(figsize=(7.5, 3.45), layout="constrained")
    ax.barh(names, values, color=["#bf5f43" if x < 0 else "#176a70" for x in values], height=.53)
    ax.axvline(0, color="#44525b", linewidth=.8)
    for i, value in enumerate(values):
        ax.text(value + (.25 if value >= 0 else -.25), i, f"{value:+.1f}", va="center",
                ha="left" if value >= 0 else "right", fontsize=8.5)
    ax.set_xlim(min(values) - 2.2, max(values) + 2.2)
    ax.invert_yaxis()
    ax.set_xlabel("Reduction in strict unfaithfulness among served answers (percentage points)")
    ax.set_title("SIRIN-gated Mem0 versus ungated Mem0 · LongMemEval\nOne shared cohort and panel. Gates can change which answers are served.",
                 loc="left", fontsize=10.5)
    save(fig, directory, "stage2b_selected_profile")


def render(failure_profiles, benchmark_profiles, directory):
    # Stable SVG element IDs support reproducible artifacts.
    with matplotlib.rc_context({"svg.hashsalt": "cluster-b-stage2b"}):
        bio_panel(failure_profiles, directory)
        coverage_panel(failure_profiles, directory)
        weighting_panel(benchmark_profiles, directory)
        sirin_panel(failure_profiles, directory)
