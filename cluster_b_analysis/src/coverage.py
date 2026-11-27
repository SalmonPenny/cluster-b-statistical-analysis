"""Construct descriptive coverage and architecture comparison graphs."""
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
import networkx as nx

from build_database import ROOT, details, eligible, read_csv, write_csv


# These panels document comparisons of complete evaluated systems.
HEADLINE_TABLES = {
    "membook": {"Table 1", "Table 3"}, "rmm": {"Table 1"},
    "mragent": {"Table 1", "Table 5"}, "telemem": {"Table 1", "Table 3"},
}
PROPOSED = {"MemBook", "RMM", "MRAgent", "TeleMem", "MemGuard", "TRUSTMEM", "Synthius-Mem"}
BENCHMARK_ORDER = ("LongMemEval", "LoCoMo", "HaluMem", "MSC", "ZH-4O")
DIRECT = "Directly comparable"
CONDITIONAL = "Conditionally comparable"


def label_order(name):
    return name not in PROPOSED, name.casefold()


def reportable(row):
    return (
        (row["table_id"] in HEADLINE_TABLES.get(row["paper_id"], ())
         or details(row).get("graph_include") is True)
        and (row["role"] in {"baseline", "proposed"} or details(row).get("graph_include") is True)
        and row["verification"] == "verified"
    )


def evidence_graphs(observations, comparisons):
    nodes = {row["architecture"] for row in observations.values() if reportable(row)}
    strict, relaxed = nx.Graph(), nx.Graph()
    strict.add_nodes_from(sorted(nodes, key=label_order))
    relaxed.add_nodes_from(strict)
    graph_records = {}
    for contrast in comparisons:
        if contrast["comparison_level"] != "within_block" or contrast["status"] not in {DIRECT, CONDITIONAL}:
            continue
        left, right = (observations[contrast[field]] for field in ("left_observation", "right_observation"))
        if not all(reportable(row) and eligible(row) and row["provenance"] == "original" for row in (left, right)):
            continue
        a, b = sorted((left["architecture"], right["architecture"]))
        if a == b:
            continue
        block = left["block_id"]
        edge = (a, b, left["paper_id"], left["benchmark"], block, contrast["status"])
        graph_records.setdefault(edge, set()).add(left["metric"])
        relaxed.add_edge(a, b)
        if contrast["status"] == DIRECT:
            strict.add_edge(a, b)
    return strict, relaxed, graph_records


def write_matrices(data, observations):
    by_benchmark = defaultdict(set)
    by_metric = defaultdict(set)
    metrics = set()
    architectures = set()
    for row in observations:
        architecture = row["architecture"]
        architectures.add(architecture)
        outcome = f'{row["benchmark"]} | {row["metric"]}'
        metrics.add(outcome)
        by_benchmark[architecture, row["benchmark"]].add(row["configuration_id"])
        by_metric[architecture, outcome].add(row["configuration_id"])
    benchmarks = {bench for _, bench in by_benchmark}
    columns_by_benchmark = (*[bench for bench in BENCHMARK_ORDER if bench in benchmarks],
                            *sorted(benchmarks.difference(BENCHMARK_ORDER)))
    result = []
    for name, columns, counts in (
        ("architecture_benchmark_coverage.csv", columns_by_benchmark, by_benchmark),
        ("architecture_metric_coverage.csv", sorted(metrics), by_metric),
    ):
        rows = []
        for a in sorted(architectures, key=label_order):
            rows.append({"architecture": a, **{column: len(counts[a, column]) for column in columns}})
        write_csv(data / name, ["architecture", *columns], rows)
        result.append(rows)
    return result[0], columns_by_benchmark


def plot_coverage(coverage, benchmarks, path):
    labels = [row["architecture"] for row in coverage]
    data = [[row[b] for b in benchmarks] for row in coverage]
    categories = [[0 if n == 0 else 1 if n < 3 else 2 if n < 6 else 3 for n in row] for row in data]
    fig, ax = plt.subplots(figsize=(max(8, len(benchmarks) * 1.4 + 2), max(6.6, len(labels) * .31 + 1.6)), layout="constrained")
    ax.imshow(categories, cmap=ListedColormap(["#eff2f5", "#c8e5e0", "#77b9af", "#256f68"]),
              vmin=0, vmax=3, aspect="auto")
    ax.set_xticks(range(len(benchmarks)), benchmarks)
    ax.set_yticks(range(len(labels)), labels)
    ax.xaxis.tick_top()
    ax.tick_params(length=0, pad=7)
    for i, row in enumerate(data):
        for j, n in enumerate(row):
            ax.text(j, i, str(n) if n else "·", ha="center", va="center",
                    color="#ffffff" if categories[i][j] == 3 else "#14313e")
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.suptitle("Architecture coverage by benchmark", x=.02, ha="left", fontsize=16, weight="bold")
    ax.set_title("Verified configurations with at least one retained original score", loc="left", fontsize=10, pad=16)
    fig.savefig(path, dpi=170, facecolor="white")
    plt.close(fig)


def plot_adjacency(strict, relaxed, path):
    components = sorted(nx.connected_components(strict), key=lambda group: (-len(group), sorted(group)))
    labels = [label for group in components for label in sorted(group, key=label_order)]
    fig, axes = plt.subplots(1, 2, figsize=(18, 10), layout="constrained")
    for ax, graph, title in zip(axes, (strict, relaxed), ("Strict", "Relaxed")):
        cells = [[2 if strict.has_edge(a, b) else 1 if graph.has_edge(a, b) else 0
                  for b in labels] for a in labels]
        ax.imshow(cells, cmap=ListedColormap(["#edf1f3", "#b6784b", "#0e6561"]), vmin=0, vmax=2)
        ax.set_xticks(range(len(labels)), labels, rotation=90, fontsize=7)
        ax.set_yticks(range(len(labels)), labels, fontsize=7)
        ax.tick_params(length=0)
        ax.set_title(f"{title} · {nx.number_connected_components(graph)} components", loc="left", weight="bold")
        border = 0
        for component in components:
            border += len(component)
            if len(component) > 1 and border < len(labels):
                ax.axhline(border - .5, color="white", linewidth=1)
                ax.axvline(border - .5, color="white", linewidth=1)
    fig.suptitle("Architecture comparison networks", fontsize=17, weight="bold")
    fig.legend(handles=[Line2D([0], [0], color="#0e6561", linewidth=5, label="Direct within protocol"),
                        Line2D([0], [0], color="#b6784b", linewidth=5, label="Conditional within study")],
               loc="outside lower center", ncol=2, frameon=False)
    fig.savefig(path, dpi=155, facecolor="white")
    plt.close(fig)


def plot_network(strict, relaxed, path):
    if len(relaxed) > 24:
        plot_adjacency(strict, relaxed, path)
        return
    labels = list(relaxed)
    positions = nx.circular_layout(labels, scale=1)
    fig, axes = plt.subplots(1, 2, figsize=(13.6, 7.2), layout="constrained")
    for ax, graph, title in zip(axes, (strict, relaxed), ("Strict", "Relaxed")):
        direct_edges = [edge for edge in graph.edges if strict.has_edge(*edge)]
        conditional_edges = [edge for edge in graph.edges if not strict.has_edge(*edge)]
        nx.draw_networkx_edges(graph, positions, edgelist=direct_edges, edge_color="#3e7977",
                               alpha=.29, width=1.15, ax=ax)
        nx.draw_networkx_edges(graph, positions, edgelist=conditional_edges, edge_color="#ad693b",
                               style="dashed", alpha=.37, width=1.2, ax=ax)
        nx.draw_networkx_nodes(graph, positions, node_size=64,
                               node_color=["#0e5454" if n in PROPOSED else "#637687" for n in labels],
                               edgecolors="white", linewidths=.7, ax=ax)
        for n, (x, y) in positions.items():
            ax.text(1.13 * x, 1.13 * y, n, ha="left" if x >= .09 else "right" if x <= -.09 else "center",
                    va="center", fontsize=8.4, color="#162c3a", weight="bold" if n in PROPOSED else "normal")
        ax.set(xlim=(-1.62, 1.62), ylim=(-1.3, 1.3), aspect="equal")
        ax.set_title(f"{title} · {nx.number_connected_components(graph)} components",
                     loc="left", fontsize=13, weight="bold", pad=3)
        ax.set_axis_off()
    fig.suptitle("Documented architecture comparisons", x=.025, ha="left", fontsize=17, weight="bold")
    fig.legend(handles=[
        Line2D([0], [0], color="#3e7977", label="Direct within protocol"),
        Line2D([0], [0], color="#ad693b", linestyle="--", label="Conditional within study"),
    ], loc="outside lower center", ncol=2, frameon=False)
    fig.text(.025, .057, "Shared names are projected across protocols. The graph records evidence coverage and cannot establish pooled comparability.",
             fontsize=9, color="#465968")
    fig.savefig(path, dpi=165, facecolor="white")
    plt.close(fig)


def write_blocks(data, observations, comparisons):
    blocks = defaultdict(lambda: {"metrics": set(), "configurations": set(), "graph_eligible": False})
    for contrast in comparisons:
        if contrast["comparison_level"] != "within_block" or contrast["status"] != DIRECT:
            continue
        left, right = (observations[contrast[field]] for field in ("left_observation", "right_observation"))
        paper = left["paper_id"]
        benchmark = left["benchmark"]
        cohort = details(left).get("independent_group") or f"{paper}:{benchmark}"
        if left["block_id"] != right["block_id"]:
            group = details(left).get("comparison_family") or details(right).get("comparison_family")
            if not group:
                raise ValueError(f'No documented comparison family for {contrast}')
        else:
            group = left["block_id"]
        block = blocks[paper, benchmark, str(cohort), group, left["table_id"]]
        block["metrics"].add(left["metric"])
        block["configurations"].update((left["configuration_id"], right["configuration_id"]))
        block["graph_eligible"] |= (left["architecture"] != right["architecture"]
                                    and all(reportable(row) and eligible(row) for row in (left, right)))
    fields = ("paper_id", "benchmark", "cohort_group", "block_id", "table_id")
    write_csv(data / "comparison_blocks.csv", [*fields, "metrics", "configurations", "graph_eligible"], (
        {**dict(zip(fields, block)), "metrics": "; ".join(sorted(info["metrics"])),
         "configurations": len(info["configurations"]),
         "graph_eligible": "yes" if info["graph_eligible"] else "no"}
        for block, info in sorted(blocks.items())
    ))


def write_sensitivity(data, nodes, records):
    regimes = [("all", "")]
    for label, index in (("study", 2), ("benchmark", 3)):
        regimes.extend((label, value) for value in sorted({record[index] for record in records}))

    def summaries():
        for label, value in regimes:
            for mode in ("strict", "relaxed"):
                graph = nx.Graph()
                graph.add_nodes_from(nodes)
                for a, b, paper, benchmark, _, status in records:
                    if (label, value) in {("study", paper), ("benchmark", benchmark)}:
                        continue
                    if mode == "relaxed" or status == DIRECT:
                        graph.add_edge(a, b)
                yield {"removed_type": label, "removed_value": value, "graph": mode,
                       "edges": graph.number_of_edges(), "components": nx.number_connected_components(graph),
                       "largest_component": max(map(len, nx.connected_components(graph))),
                       "isolated": len(list(nx.isolates(graph)))}

    write_csv(data / "comparison_sensitivity.csv",
              ["removed_type", "removed_value", "graph", "edges", "components", "largest_component", "isolated"],
              summaries())


def main():
    data = ROOT / "data"
    rows = read_csv(data / "validated_results.csv")
    observations = {row["observation_id"]: row for row in rows}
    comparisons = read_csv(data / "comparability.csv")
    strict, relaxed, records = evidence_graphs(observations, comparisons)
    write_blocks(data, observations, comparisons)
    write_sensitivity(data, list(relaxed), records)
    fields = ("architecture_a", "architecture_b", "paper_id", "benchmark", "block_id", "status")
    write_csv(data / "comparison_graph_edges.csv", [*fields, "metrics"], (
        {**dict(zip(fields, edge)), "metrics": "; ".join(sorted(metrics))}
        for edge, metrics in sorted(records.items())
    ))
    component_rows = []
    for name, graph in (("strict", strict), ("relaxed", relaxed)):
        components = sorted((sorted(c, key=label_order) for c in nx.connected_components(graph)),
                            key=lambda nodes: (-len(nodes), nodes))
        for index, nodes in enumerate(components, 1):
            component_rows.extend({"graph": name, "component": index, "architecture": node}
                                  for node in nodes)
        print(f"{name}: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges, "
              f"components {components}")
    write_csv(data / "comparison_graph_components.csv", ["graph", "component", "architecture"], component_rows)
    coverage, benchmarks = write_matrices(data, (row for row in rows if eligible(row) and row["provenance"] == "original"))
    plot_coverage(coverage, benchmarks, ROOT / "figures" / "benchmark_coverage.png")
    plot_network(strict, relaxed, ROOT / "figures" / "comparison_network.png")


if __name__ == "__main__":
    main()
