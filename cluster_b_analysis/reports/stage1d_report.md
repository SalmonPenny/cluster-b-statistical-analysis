# Cluster B Stage 1D · Targeted expansion and integration

## Selection and validation

Detailed extraction now covers **20 of 24** screened publications. Selection prioritized matched mechanisms, new failure modes, reported uncertainty and potential multi-objective outcomes. Results were verified against the local publications with table, cell and configuration provenance.

| Paper | Selected panels and rationale | Added verified point values |
|---|---|---:|
| MemBench | Tables 3–5 and 10–12 compare common-backbone mechanisms on factual and reflective memory, question subtypes, and read/write efficiency. | 330 |
| ES-MemEval | Tables 3–9 measure emotional-support memory through QA, retrieval, summaries, dialogue generation and scorer checks. | 412 |
| Towards Root Memory | Tables 4–7, Figure 6 and reported Recall@30 values provide matched retrieval and conversation arms plus explicit diagnostic traps. | 167 |
| TWIST | Validated Track B Table 3 plus the two multi-ingest summaries supply contradiction detection, restraint and evidence attribution, with reported uncertainty. | 64 |

The four remaining papers answer narrower or less aligned questions. LOCCO could materially improve **forgetting** and history-length coverage, but its long-context conditions offer limited comparability to evaluated memory systems here. MemGPT adds original architecture evidence on MSC, document QA and nested key–value retrieval. Its task and scoring differences would need resolution before comparing it with the earlier MSC panels. MemoryRewardBench evaluates reward models and therefore supplies a separate evaluand. Oracle Agent Memory adds an informative system and a high-accuracy LongMemEval setup, with limited matched controls on that benchmark. These papers can improve local coverage. None currently appears likely to establish the aligned independent replications needed for pooled ranking.

| Measure | Before | After |
|---|---:|---:|
| Raw records | 3,019 | 4,058 |
| Verified numerical observations | 2,841 | 3,814 |
| Retained original observations | 2,266 | 3,110 |
| Verified configurations | 747 | 1,028 |
| Eligible matched contrasts | 3,243 | 4,364 |
| Baseline-relative contrasts | 384 | 707 |
| Protocol blocks in matched effects | 90 | 137 |
| Potentially dependent cohorts in matched effects | 22 | 27 |
| Strict nodes / edges / components | 42 / 81 / 15 | 60 / 190 / 14 |
| Relaxed nodes / edges / components | 42 / 205 / 2 | 60 / 313 / 3 |

The largest strict component grew from 25 to 35 labels and the largest relaxed component from 41 to 49. The separate IMLogic memory-level retrieval cluster explains why additional relaxed evidence can increase the component count. Graph edges are projections of source-local comparisons. They do not establish an aligned independent comparison path. The IMLogic five-user subset belongs to the parent cohort, and its two judges rate the same generated answers. TWIST reuses LoCoMo histories with a new draft-alignment task. [Coverage](coverage_report.md) · [Extraction status](../data/extraction_status.csv) · [Comparison blocks](../data/comparison_blocks.csv)

## What changes scientifically

- **IMLogic adds a matched four-objective panel.** All 11 Table 5 configurations use GPT-4o-mini for memory, GPT-5.1 to answer, and top-30 retrieval on the shared benchmark. At printed values, the first front includes three RootMem-augmented configurations and four controls. MemOS + RootMem has the highest accuracy (51.04%). TACITREE has the lowest preference-trap rate (14.12%) and much lower accuracy (30.46%). Omitting preference-trap rate removes four first-front configurations. Sixteen of 19 zero-tolerance edges survive the five thresholds. This supports a trade-off between recovering implicit logic and avoiding distinct distractors. Forced-choice fabrication is a diagnostic outcome with rare selections and does not estimate open-answer hallucination.
- **ES-MemEval and MemBench broaden failure-mode support.** The matrix now includes personal-disclosure recall, conflict detection, abstention and user-state modeling, plus MemBench's factual and reflective subtypes. In ES-MemEval, GPT-4o under RAG improves the overall semantic rating from 1.25 to 1.33, while the abstention rating falls from 1.67 to 1.30 on the paper's 0–2 scale. This qualifies any broad claim that retrieval helps every memory task. Dialogue ratings from the simulated-user setup have ceiling effects, and cross-table trajectory equivalence has not been verified.
- **TWIST supplies conditional evidence on intervention trade-offs.** The GPT-4o MindTwin configuration shows high hard-negative specificity (0.98) and lower contradiction recall (0.42) and grounded recall (0.18). Flat RAG has 0.57, 0.97 and 0.55 respectively under a different evidence and prompt regime. The new records preserve 23 Wilson intervals and two reported hierarchical multi-ingest intervals. They characterize the reported endpoints. The Wilson intervals do not account for clustered histories; the multi-ingest summaries use three stochastic ingests and a partially completed run. No strict architecture effect or independent replication follows. Correct restraint on aligned drafts differs from retention of superseded beliefs.

MemBench source labels for observation context length conflict, and several accuracy blocks repeat exactly. Confirmed duplicates were retained with provenance and excluded. Uncertain repetitions remain flagged. The 40 printed timing bounds below 0.001 seconds are stored with no point estimate. ES-MemEval same-paper repeats and Root Memory duplicate analysis cells were also traced. Those limitations preclude splicing uneven timing and scoring columns into new vectors. [New discrepancy entries](../data/discrepancies.csv) · [Failure-mode mapping](../data/benchmark_failure_mode_mapping.csv)

## Pipeline rerun and remaining feasibility

All **31 existing tests** passed. The Stage 1 rebuild and Stages 2A–2D ran. All previous rows in the source databases, comparability and block tables, and numerical Stage 2 outputs were reproduced exactly. The new Pareto panel raises the totals from five to **six panels**, 29 to **40 configurations**, and 73 to **128 pairs**. The updated sensitivity analysis keeps all prior results, including the 20 original dominance relationships that persist through the tolerance grid. Updated matrices, graphs and figures are in the existing directories.

Stage 2B now has **1,599 benchmark profiles** and **1,368 failure-mode profiles**, up from 785 and 614. Its locality-free audit still finds all 707 baseline-relative scopes distinct and zero aligned cross-study or cross-cohort matches. Cohort balancing continues to leave the point estimates unchanged. Regularized and Bayesian Bradley–Terry models remain premature: more edges and outcomes add local comparisons, but do not align judges, tasks, baselines or cohort units. Regularization or priors could stabilize a fit without establishing a defensible pooled estimand.

The rebuild uses the updated canonical raw CSV and unchanged mathematical modules. From the repository root:

```bash
python -B cluster_b_analysis/src/build_database.py
python -B cluster_b_analysis/src/coverage.py
python -B -m unittest discover -s cluster_b_analysis/tests
python -B -m cluster_b_analysis.src.effect_sizes
python -B -m cluster_b_analysis.src.failure_mode_analysis
python -B -m cluster_b_analysis.src.stage2c_analysis
python -B -m cluster_b_analysis.src.sensitivity
```
