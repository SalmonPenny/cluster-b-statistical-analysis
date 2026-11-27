# Cluster B coverage and comparison networks

## Benchmark overlap after the continuation

| Benchmark | Contributing papers | Verified cells | Verified configurations | Retained original configurations |
|---|---:|---:|---:|---:|
| LongMemEval | 7 | 778 | 283 | 282 |
| LoCoMo | 6 | 616 | 129 | 127 |
| HaluMem | 4 | 574 | 63 | 41 |
| MSC | 1 | 53 | 18 | 18 |
| ZH-4O | 1 | 55 | 55 | 42 |
| Mem-α validation set | 1 | 83 | 15 | 15 |
| MemoryAgentBench | 1 | 80 | 8 | 8 |
| PerLTQA | 1 | 11 | 10 | 10 |

Counts include controlled variants and diagnostics. LongMemEval includes separately labeled adapted workloads and SIRIN gates, and HaluMem includes source-attributed prior baseline cells. The statistical unit depends on the question. One configuration can contribute several outcomes, and multiple configurations can share the same questions, histories and scorer. [Benchmark matrix](../data/architecture_benchmark_coverage.csv) · [Metric matrix](../data/architecture_metric_coverage.csv) · [Coverage figure](../figures/benchmark_coverage.png)

- **LongMemEval** grew from three to seven paper panels. The original benchmark adds controlled indexing, reader and temporal-retrieval comparisons with explicit S/M distinctions. The Agent-Native derived workload, RMM judge, MRAgent’s LongMemEval-S, SIRIN’s served subset and unidentified MemBook release are distinct protocols. Heterogeneity remains substantial even where method names repeat.
- **LoCoMo** grew from two to six. Direct links come from the Agent-Native same-backbone panels, the Synthius control rows and MemGuard versus rerun A-Mem under matched utility protocols. The historical 50-conversation preprint evaluates lexical overlap and includes adversarial items. Later studies use different 10-conversation slices and semantic or lexical scorers. The original LoCoMo and Synthius adversarial tests ascertain false-premise rejection, with generic refusal as a possible confound.
- **HaluMem** grew from one to four. The HaluMem v3 QA controls share GPT-4o scoring, generator and reporting split. The system APIs, retrieval limits and write mechanisms vary. MemGuard and TRUSTMEM comparisons to imported source baselines have heterogeneous judges, exposure and lineage. The HaluMem operation labels are supplementary Cluster B evidence under the unchanged RQ1 Category 3-C assignment. [Failure-mode map](../data/benchmark_failure_mode_mapping.csv)

## Before and after

| Projection | Initial nodes | Current nodes | Initial edges | Current edges | Initial components | Current components | Largest component |
|---|---:|---:|---:|---:|---:|---:|---:|
| Strict | 19 | 38 | 36 | 67 | 8 | 15 | 12 → 21 |
| Relaxed | 19 | 38 | 63 | 191 | 3 | 2 | 17 → 37 |

The strict network now contains components of 21, 3 and 2 labels, plus 12 isolated labels. Holding the original 19 labels fixed, the strict component count falls from eight to six and the largest component increases from 12 to 14. HaluMem links formerly isolated Mem0-Graph and Supermemory with established controls. The relaxed network leaves MOOM isolated. The extra strict components reflect additional evaluated labels with conditional or absent strict links. [Edges by source panel](../data/comparison_graph_edges.csv) · [Component membership](../data/comparison_graph_components.csv) · [Adjacency figure](../figures/comparison_network.png)

Each strict edge requires some retained original contrast with a shared reported protocol. The relaxed projection adds conditional original comparisons within studies. Imports, unresolved source transcriptions, oracle rows and separate diagnostic or component panels cannot bridge architectures on their own. A paper’s approved headline plot can contain evaluation conditions, such as a fixed-backbone facet of Figure 9. Graph labels project across specific configurations, so a path through RAG or Mem0 can join distinct backbones, judges or outcomes. Same-study score differences therefore compare evaluated systems unless the intervention actually isolates a component.

## Effective comparison blocks and sensitivity

Strict headline evidence increased from **7 to 28 distinct protocol block IDs**. The updated dataset has 32 block × source-table records with strict headline edges and 15 conservative cohort groups supporting them, up from six study–benchmark cohorts in the initial batch. Including within-architecture and other direct design panels gives 70 unique block IDs and 18 conservative cohort groups. These groups combine same-study panels where questions, users or runs are shared or their independence is unresolved. They are an upper bound on the number of independent groups for any single synthesis. Cross-study overlap, benchmark subsets, metric definitions and setting differences leave **zero replicated independent blocks verified for a common pooling estimand across the full network**. The effective sample size for any proposed narrower rank model remains unidentified from the printed averages. [Block inventory](../data/comparison_blocks.csv)

Fixed-node leave-one-out analysis shows which bridges depend on a particular source. Removing HaluMem reduces the strict largest component from 21 to 18, removing RMM reduces it to 17, and removing all LoCoMo panels reduces it to 17. These results concern edge availability. They leave numerical rankings and uncertainty within each source panel unchanged. [Sensitivity results](../data/comparison_sensitivity.csv)
