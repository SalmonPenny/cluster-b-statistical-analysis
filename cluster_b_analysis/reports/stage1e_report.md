# Cluster B Stage 1E · Final literature extraction and integration

The assessment now covers **24 of 24 screened publications**. The 20 previous extraction dispositions remain intact. This batch reviews the last four sources against the same inclusion rules, with distinct treatment for printed results, plot estimates, imports and outcomes outside the architecture estimand. All 24 dispositions, source panels and remaining source-level caveats are recorded in the extraction status. [Extraction status](../data/extraction_status.csv)

| Source | Reviewed comparative evidence | Raw | Verified | Retained original |
|---|---|---:|---:|---:|
| LOCCO | Figures 3–9 and §4.3, PDF pp. 6–8. Delayed recall, forgetting, dialogue density and replay under sequential LoRA. Seventeen printed annotations are selective and remain outside synthesis. | 355 | 17 | 0 |
| MemGPT | Tables 2–3 and Figures 5 and 7, PDF pp. 5–7. Complete MSC retrieval and opener tables, plus auxiliary document QA and nested retrieval curves. Only Table 2 has verified matched architecture outcomes. | 71 | 24 | 12 |
| MemoryRewardBench | Tables 3 and 5–9, PDF pp. 5 and 16–17. Reward-model accuracy, presentation-order consistency, prompt structure and perturbation diagnostics. All 412 values concern the evaluator. Twelve rounded repeats link to their source anchors. | 412 | 412 | 0 |
| Oracle Agent Memory | Figures 4–7, Tables 3–4 and accompanying text, PDF pp. 12–16. LongMemEval, ChromAtlas-ND, threshold demo and BEAM. Two imported Mem0 values and four derived or joint source values stay excluded. Retained diagnostics still require comparison-specific eligibility. | 52 | 52 | 46 |

LOCCO figure estimates use source-image pixels and axis ticks. Nine overlapped marks have no recoverable point value. MemGPT auxiliary estimates use PDF vector paths and horizontal gridlines. All 376 digitized points are unverified and excluded. Their graph-reading precision conveys no sampling uncertainty. Oracle and MemoryRewardBench plots without separate point labels did not supply exact transcriptions. Related tables cover several of those panels. Oracle threshold-band endpoints and definitions remain unavailable at numerical precision. [Raw results](../data/raw_results.csv) · [Verified results](../data/validated_results.csv)

## Coverage and comparison structure

| Measure | Stage 1D | Stage 1E |
|---|---:|---:|
| Assessed publications with detailed extraction | 20 | 24 |
| Raw records | 4,058 | 4,948 |
| Verified numerical observations | 3,814 | 4,319 |
| Retained original observations | 3,110 | 3,168 |
| Configurations with verified observations | 1,028 | 1,126 |
| Eligible matched contrasts | 4,364 | 4,370 |
| Baseline-relative contrasts | 707 | 713 |
| Protocol blocks contributing matched contrasts | 137 | 140 |
| Potentially dependent cohorts contributing matched contrasts | 27 | 28 |
| Strict graph nodes / edges / components | 60 / 190 / 14 | 63 / 191 / 16 |
| Relaxed graph nodes / edges / components | 60 / 313 / 3 | 63 / 315 / 4 |
| Largest strict / relaxed component | 35 / 49 | 36 / 50 |

The new strict edge links MemGPT and Conversation Summary within MSC DMR. Oracle Agent Memory and Flat History are isolated in the strict projection. They form one new relaxed component through the conditional ChromAtlas-ND comparison. The strict graph's larger main component therefore coexists with more isolated labels. Exactly one potentially dependent workload group supplies the six new matched effects. No aligned cross-study replication was confirmed. [Protocol blocks](../data/comparison_blocks.csv) · [Graph components](../data/comparison_graph_components.csv) · [Failure-mode map](../data/benchmark_failure_mode_mapping.csv)

## What the additional evidence establishes

- **MemGPT on MSC deep memory retrieval.** Compared with a lossy conversational summary under the same reader, MemGPT's judged accuracy rises from 38.7% to 66.9% for GPT-3.5 Turbo, 32.1% to 92.5% for GPT-4, and 35.3% to 93.4% for GPT-4 Turbo. ROUGE-L recall rises from 0.394 to 0.629, 0.296 to 0.814, and 0.359 to 0.827. Each complete-system comparison favors MemGPT on both objectives, including at all five tested tolerances. Sensitivity converts the bounded ROUGE-L proportion to a 0–100 scale and preserves the source scale in Pareto and rank outputs. No paired uncertainty is reported. Evidence access, prompts and retrieval differ across conditions. The endpoints characterize recall and consistency with a reference, so the QA error complement cannot establish a reduction in hallucination.
- **LOCCO adds distinct forgetting and replay evidence.** The trained consistency scorer evaluates user-dialogue facts under sequential training. Openchat-3.5-0106 is reported to forget 85.27% of its initial measured recall by T2 despite a 0.455 initial score. Figure 5 changes the QA set with each period and therefore measures new-dialogue recall. Density, lag and replay comparisons share the source corpus and cannot replicate episodic QA architecture contrasts.
- **Oracle adds long-horizon diagnostics.** The 93.8% LongMemEval result is 469 of 500 questions in one high-accuracy setup. ChromAtlas-ND reports 48 Oracle preferences, 13 flat-history preferences and 19 ties across one 80-turn script, alongside approximate final-turn input estimates of 1,300 and 13,900 tokens. The gpt-5.4 judge combines four answer qualities, and the generator settings are insufficiently specified for a strict comparison. No measured provider cost or open-answer hallucination rate follows. Under stricter BEAM ordering, the reported 1M accuracy is 0.630 versus 0.680 under event-presence scoring. The 10M stress test reports 0.510, with multi-session reasoning at 0.17. Keep the scales and scoring regimes separate.
- **MemoryRewardBench measures a separate stage of an agent system.** Judgment accuracy and order-swap consistency characterize a reward model's evaluation of candidate memory outputs or trajectories. This adds evidence about judge failure modes and evaluation design. The memory systems used to construct examples do not supply comparative downstream assistant outcomes in these tables.

These results extend retention, historical fact retrieval, persona use, event ordering, evidence expansion and preference-judgment diagnostics. They add no directly matched free-answer hallucination result. Prior HaluMem, SIRIN, BioMem and IMLogic interpretations continue to apply under their documented protocols.

## Discrepancies and computation checks

MemGPT Figure 7 shows nesting levels 0–3 while the prose discusses 0–4. The Table 3 model labels omit the MemGPT suffix, which the caption and section establish. Human SIM-H is a self-reference. The reward study's Table 3 and Table 7 captions and Table 5 GLM label are preserved with qualifications. Oracle's 9.5× token figure subtitle conflicts with its 10.7× prose and approximately 13,900 versus 1,300 endpoints. The claimed 10k-trigger minimum is unresolved because an unlabeled point appears lower. BEAM retains 0.630 and 0.510 as printed, alongside the fractional aggregate scores, which reconcile only at two decimal places. Earlier MemBook attribution and MRAgent F1 exclusions were preserved. [Discrepancy log](../data/discrepancies.csv)

All **31 tests passed**. The rebuilt raw and verified databases, comparison and block tables, and every prior numerical Stage 2 output reproduced their previous rows exactly. Stage 2B has **1,605 benchmark profiles** and **1,374 failure-mode profiles**, with zero cross-study or cross-cohort matches among 713 baseline-relative scopes. Stage 2C has **nine panels, 46 vectors and 131 pairs**. Stage 2D retained all 36 prior tolerance-robust dominance relations and added three. It reproduced the 798 effect transformation checks and 14 SIRIN denominator illustrations. No new confidence intervals or model estimates were generated.

## Statistical feasibility

The paired unit and estimand remain local to a stated protocol. The three MemGPT reader blocks reuse the same MSC DMR workload. Judge correctness and ROUGE-L recall assess the same generated answers. Their agreement provides endpoint triangulation in one study. RMM instead measures MSC next-response generation. Oracle's LongMemEval headline and other papers' LongMemEval panels differ in reader, retrieval budget, benchmark-version documentation or judge. The same benchmark name establishes a candidate protocol audit, with no newly confirmed aligned independent replication.

Cohort-balanced summaries remain descriptive within exact strata. A single compatible cohort contributes each current baseline-relative stratum. The number of protocol blocks and conservative cohort labels measures inventory and potential dependence. It does not identify effective sample size for a pooled architecture effect. Likewise, pairwise comparisons created from shared scores do not supply independent outcomes.

Regularized and Bayesian Bradley–Terry models remain unsupported as estimators of a pooled architecture ranking. A connected comparison design with a reference constraint can identify relative abilities only for a shared outcome and a sufficiently comparable design. The projected graph collapses heterogeneous system variants, tasks, evaluators and baselines. Borrowing an edge through a common system label cannot separate architecture ability from protocol effects. Treating derived wins or shared-question cells as independent would overstate information. Penalties or priors can produce finite estimates while leaving cross-protocol contrasts dependent on model assumptions. The available evidence does not establish equality of architecture performance. Local point comparisons, frontiers and scope-specific sensitivity analyses remain informative.

## Panels for a narrower head-to-head evaluation

| Evidence role | Panel | Why it is informative | Limit to carry forward |
|---|---|---|---|
| Primary direct hallucination rubric | HaluMem v3 QA, original Medium and Long splits analyzed separately | Multiple competing systems, common generator and GPT-4o scoring, and jointly reported accuracy, omission and hallucination. | The hallucination category includes incorrect and fabricated answers. Keep fixed split, memory operations and retrieval settings explicit. Preserve the Long-split Memobase nonclosure restriction. |
| Selective unfaithfulness intervention | SIRIN Table 8, separately within the Mem0 and LightMem frameworks | Matched gate variants, served correctness, answer coverage, strict unfaithfulness and published paired uncertainty for selected accuracy contrasts. | Unfaithfulness is conditional on serving. Scorer inclusion and denominator alignment must be established before estimating all-question event frequency. |
| Controlled failure-mode panel | Original LongMemEval Tables 3, 4 and 8 | Explicit reader and retrieval variants, S/M distinction and tasks for preferences, temporal reasoning, updating and multi-session evidence. | QA accuracy and retrieval recall are memory-performance proxies. Maintain variant, item set, reader, top-k and judge matching. The Oracle headline is a separate configuration with no matched comparator. |
| Complementary trade-off panel | IMLogic Table 5 and BioMem Table 4, analyzed as separate workloads | IMLogic pairs accuracy with distinct forced-choice trap outcomes. BioMem offers controlled updating and retrieval variants plus reported paired error analysis on its medical subset. | Forced-choice fabrication distractors differ from free-answer hallucination. The medical subset has a domain-specific rubric and a single cohort. |
| Secondary historical retrieval control | MemGPT Table 2, MSC deep memory retrieval | Three fixed-reader contrasts compare summary-only context with paginated access to full history, using two scores on the same answers. | The study reuses one workload and does not isolate access to evidence from memory mechanism. Neither endpoint estimates hallucination rates. |

Choose panels based on shared experimental conditions, endpoint relevance and available uncertainty. Architecture selection remains a separate task. A new confirmatory head-to-head would benefit from matched item-level outcomes, predeclared scorer rubrics and a common budget before applying pairwise inference.

## Reproduction

The canonical raw CSV preserves source transcriptions and inclusion decisions. The local PDFs, literature review and page index remain unchanged. From the repository root with the existing scientific Python environment available:

```bash
python -B cluster_b_analysis/src/build_database.py
python -B cluster_b_analysis/src/coverage.py
python -B -m unittest discover -s cluster_b_analysis/tests
python -B -m cluster_b_analysis.src.effect_sizes
python -B -m cluster_b_analysis.src.failure_mode_analysis
python -B -m cluster_b_analysis.src.stage2c_analysis
python -B -m cluster_b_analysis.src.sensitivity
```
