"""Visual summaries for Stage 2D. Each panel preserves its own comparison scope."""
from collections import defaultdict

from .stage2b_figures import plt, save


def render(directory, tolerance_rows, weights, events):
    with plt.rc_context({"svg.hashsalt": "cluster-b-stage2d"}):
        fig, ax = plt.subplots(figsize=(7.4, 4), layout="constrained")
        by_panel = defaultdict(dict)
        for r in tolerance_rows:
            by_panel[r["panel"]][float(r["tolerance_pp"])] = r["edge_count"]
        ticks = [0, .5, 1, 2, 5]
        for p, values in by_panel.items():
            ax.plot(range(len(ticks)), [values[t] for t in ticks], marker="o", label=p)
        ax.set(xticks=range(len(ticks)), xticklabels=[str(t) for t in ticks],
               xlabel="Exploratory practical tolerance (percentage points)",
               ylabel="Directed dominance edges")
        ax.set_title("Dominance depends on the practical tolerance", loc="left")
        ax.legend(frameon=False, ncol=2)
        save(fig,directory,"stage2d_tolerance")

        fig, axes = plt.subplots(1,2,figsize=(10,4.4),sharex=True,layout="constrained")
        for panel, ax in zip(("sirin-mem0","sirin-lightmem"),axes):
            rows = sorted((r for r in weights if r["panel"]==panel),key=lambda r:r["share"])
            names = [r["system"].split(" | ",1)[-1].replace("SIRIN ","") for r in rows]
            ax.barh(names,[100*r["share"] for r in rows],color="#216e71")
            ax.set(xlim=(0,100),xlabel="Share of sampled preference weights (%)",title=panel.split("-")[1])
        fig.suptitle("Sensitivity to objective preferences · SIRIN Table 8\nUniform simplex sample, 4,000 draws per framework")
        save(fig,directory,"stage2d_objective_weights")

        fig, axes = plt.subplots(1,2,figsize=(9.5,4.4),sharey=True,layout="constrained")
        for panel, ax in zip(("sirin-mem0","sirin-lightmem"),axes):
            rows=[r for r in events if r["panel"]==panel and
                  ("Memory baseline" in r["system"] or "SIRIN Judge" in r["system"])]
            for r in rows:
                x=float(r["coverage_pct"])
                u=float(r["conditional_unfaithful_pct"])
                product=float(r["assumption_conditional_unfaithful_answer_pct_all_queries"])
                label=r["system"].split(" | ")[-1].replace("+ ","").replace(" gate","")
                ax.plot([x,x],[product,u],color="#8a9ca3",linewidth=1)
                ax.scatter(x,u,c="#a65a3b",marker="o")
                ax.scatter(x,product,c="#216e71",marker="D")
                ax.annotate(label,(x,u),xytext=(-3 if x==100 else 4,7),textcoords="offset points",
                            ha="right" if x==100 else "left",fontsize=8)
            ax.set(title=panel.split("-")[1],xlim=(55,105),ylim=(9,47),xlabel="Answer coverage (%)")
        axes[0].set_ylabel("Strict unfaithfulness rate (%)")
        fig.suptitle("SIRIN Table 8 · served-answer rates (circles) and all-query scenario (diamonds)\n"
                     "Products assume consistently weighted scorer coverage")
        save(fig,directory,"stage2d_sirin_denominators")
