"""Figures for the reviewed Stage 2C panels."""
from .data_loading import read_score
from .ranking import rankings
from .stage2b_figures import save, plt
from .stage2c_analysis import BIO, HALU, objective


def coordinates(vector, *keys):
    return tuple(float(read_score(vector[k])) for k in keys)


def render(panels, directory):
    with plt.rc_context({"svg.hashsalt": "cluster-b-stage2c"}):
        vectors, labels, layers = panels["biomem-medical"]
        fig, ax = plt.subplots(figsize=(7.2, 4), layout="constrained")
        xy = {}
        for name, vector in vectors.items():
            xy.setdefault(coordinates(vector, *(objective(t, m) for t, m, _ in BIO)), []).append(name)
        for (x, y), names in xy.items():
            ax.scatter(x, y, c="#197174" if layers[names[0]] == 1 else "#8f98a1", s=65)
            label = " / ".join("A-Mem" if labels[n] == "Base Method" else labels[n] for n in names)
            ax.annotate(label, (x, y), xytext=(0, 9), textcoords="offset points", ha="center")
        ax.set(xlim=(76, 98), ylim=(63, 97), xlabel="Dynamic updating QA score (%)",
               ylabel="Temporal reasoning QA score (%)")
        ax.set_title("BioMem Table 4 · RealMem medical subset\nHuatuoGPT-3-27B · teal marks the first front",
                     loc="left")
        save(fig, directory, "stage2c_biomem_pareto")

        fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), layout="constrained")
        for system, ax in zip(("mem0", "lightmem"), axes):
            vectors, labels, layers = panels[f"sirin-{system}"]
            for name, vector in vectors.items():
                abstain, unfaith, accuracy = coordinates(
                    vector, "Overall / Abstain rate", "Overall / Strict unfaithfulness", "Overall / Served accuracy")
                x = 100 - abstain
                short = labels[name].split(" | ")
                label = "Ungated" if "Memory baseline" in labels[name] else (
                    ("Probe" if "Probing" in short[1] else "Judge") + " " +
                    ("both" if "Both" in short[2] else "answer" if "Answerability" in short[2] else "faith"))
                offsets = {
                    "mem0": {"Judge faith": (6, -14), "Probe faith": (6, 7), "Judge both": (-6, 8),
                             "Probe both": (9, -12), "Judge answer": (6, 8), "Probe answer": (6, 8),
                             "Ungated": (-6, 8)},
                    "lightmem": {"Judge faith": (6, -13), "Probe faith": (6, -6),
                                 "Judge both": (-6, -14), "Probe both": (-6, 8),
                                 "Judge answer": (5, 12), "Probe answer": (5, -16), "Ungated": (-6, -15)},
                }
                dx, dy = offsets[system][label]
                ax.scatter(x, unfaith, c="#197174" if layers[name] == 1 else "#a5aab1", s=40 + 2*accuracy)
                ax.annotate(f"{label} ({accuracy:g})", (x, unfaith), xytext=(dx, dy),
                            textcoords="offset points", ha="right" if dx < 0 else "left", fontsize=7.5)
            ax.set(xlim=(46, 109), ylim=(17, 45), xlabel="Answer coverage (%)",
                   title="Mem0" if system == "mem0" else "LightMem")
        axes[0].set_ylabel("Strict unfaithfulness among served answers (%)")
        fig.suptitle("SIRIN Table 8 · separate LongMemEval gate panels\nLabels include served accuracy (%). Teal marks the three-objective first front.",
                     fontsize=11)
        save(fig, directory, "stage2c_sirin_coverage")

        vectors, labels, _ = panels["halumem-medium"]
        ranks = rankings(vectors, {objective(t, m): d for t, m, d in HALU})
        fig, ax = plt.subplots(figsize=(7.3, 3.9), layout="constrained")
        for name in sorted(vectors):
            y = [r[name] for r in ranks.values()]
            line, = ax.plot(range(3), y, marker="o")
            ax.text(2.07, y[-1], labels[name].split(" | ")[-1], va="center", color=line.get_color())
        ax.set(xticks=range(3), xticklabels=["Accuracy ↑", "Hallucination rate ↓", "Omission rate ↓"],
               xlim=(-.16, 2.62), yticks=range(1, 7), ylim=(6.35, .65), ylabel="Within-panel competition rank")
        ax.set_title("HaluMem Table 3 · Medium QA rank reversals\nGPT-4o QA evaluation · categories share the same questions", loc="left")
        save(fig, directory, "stage2c_halumem_rank_reversals")
