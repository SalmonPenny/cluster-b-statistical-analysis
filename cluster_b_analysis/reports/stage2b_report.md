# Cluster B Stage 2B · Cohort-balanced failure-mode profiles

## Estimand and eligibility

The estimand is a **direction-adjusted contrast for a specified evaluated configuration against a specified reference configuration**, on one outcome under a documented comparison protocol. A positive sign favors the target. When several endpoints can legitimately enter the same estimand, averaging describes the observed protocols or cohorts under the stated weights. The data are observational across protocols. A difference between evaluated systems can reflect several design changes, and even a source-labeled controlled variant inherits the limits of the reported intervention.

The pipeline joins the saved Stage 2A effect table to Stage 1 observations by source IDs and reuses the strict Stage 2A eligibility loader. It checks pair orientation, source identity, outcome metadata, protocol, and cohort. The 3,243 eligible Stage 2A rows are the input universe. The profile design uses the following subsets.

- **Explicit baseline comparisons.** All 384 baseline-relative contrasts enter benchmark profiles. A failure-mode profile additionally requires a reviewed mapping from benchmark, task and outcome. Broad overall outcomes, mixed task scores, and resource metrics stay in benchmark profiles. MSC similarity outcomes stay there because they cannot isolate retention.
- **Source-ordered comparisons.** A separate evidence design uses directly comparable distinct-architecture pairs with mapped outcomes from HaluMem, LoCoMo-Plus and RealMem, plus LoCoMo adversarial pairs explicitly tagged as direct task diagnostics on both sides. These 401 contrasts preserve Stage 2A source order and name the other system as the comparison target. Baseline-relative metrics are kept separate.
- **Comparison types.** Complete-system, matched-backbone, controlled, scaling and matched-retriever types keep their Stage 1 labels. The selected set has 610 evaluated-system, 151 controlled-variant and 24 matched-retriever contrasts. The matched-backbone and scaling classes outside this scope remain accessible in Stage 2A.
- **Compatibility.** A profile stratum keys on benchmark and version, split, task, metric and definitions, direction, effect unit, measurement scope, evidence design, exact oriented configuration IDs and their settings, source study, table and protocol. There is no documented cross-protocol equivalence to authorize pooling under common architecture labels. Retrieval, context, prompts, gate and feedback conditions, reader and judge remain attached, including when some fields are unreported. Each row preserves the evaluated architecture labels and available RQ2 categories. An architecture category denotes taxonomy, not an estimated effect for that family.

The [locality-free audit](#empirical-support) tests whether the conservatism of the grouping conceals candidate cross-cohort matches. [Stage 1 mapping](../data/benchmark_failure_mode_mapping.csv) · [Stage 2A eligibility](stage2a_report.md)

## Hierarchical estimators

Write \(d_{p,i}\) for a direction-adjusted contrast from distinct eligible endpoint \(i\) in protocol \(p\). A protocol identifier is qualified by study. For each compatible stratum, define \(m_p=\sum_i d_{p,i}/n_p\), where \(n_p\) is the number of retained endpoint contrasts; \(P\) is the set of observed protocols. For study \(s\) and cohort \(c\), \(P_s\) and \(P_c\) are the protocols in that study or cohort. The four descriptive estimates are:

| Weighting | Formula | Equal contribution |
|---|---|---|
| Observation-weighted | \(\sum_{p\in P} n_p m_p / \sum_{p\in P} n_p\) | Each distinct matched endpoint |
| Protocol-balanced | \(\sum_{p\in P}m_p/\lvert P\rvert\) | Each protocol mean |
| Study-balanced | \(\frac{1}{S}\sum_s \frac{1}{\lvert P_s\rvert}\sum_{p\in P_s}m_p\) | Each study mean, equal protocols inside each study |
| Cohort-balanced | \(\frac{1}{C}\sum_c \frac{1}{\lvert P_c\rvert}\sum_{p\in P_c}m_p\) | Each cohort mean, equal protocols inside each cohort |

The numerator of each mean gives a matched contrast the weight implied by its nested denominators. For the cohort-balanced estimator the weight is \(1/(C\lvert P_c\rvert n_p)\). Cohorts can span studies. Balancing limits the influence of heavily reported protocols in admissible strata. It leaves dependence, confounding and selection of reported results in place.

Exact duplicate directed source pairs contribute once. Multiple source pairs representing an identical protocol-local endpoint and effect can share one contribution with all provenance retained. Conflicting effects or reversed copies within a stratum fail validation. Different valid contrasts sharing a source remain visible, with no independence claim. Marginal and subgroup metrics, different scoring objectives and different treatment variants cannot substitute for replication. Counts distinguish retained matched endpoints (`n_observations`), original source pairs and distinct numerical source cells. Blank effects contribute neither a value nor a denominator. Exact observed zero is retained.

## Units and normalization

The main estimate uses the Stage 2A direction-adjusted difference, presented in percentage points where available and in the native reported unit elsewhere. A 10-point decrease in a lower-is-better reported rate is a positive 10-point improvement. A reported rubric difference stays a rubric difference. Metric definitions and units stay in the compatibility key, so identical numeric ranges cannot make distinct constructs exchangeable.

The source table preserves Stage 2A relative performance, relative error and directly measured undesirable-event reductions where the original applicability conditions are met. Relative performance and event reduction require a positive reference denominator. For a higher-is-better outcome with a defensible attainable ceiling \(u\), available improvement is \(g=(s-b)/(u-b)\). At \(b=u\) it is undefined. At \(b=0<u\) it can be defined even when a ratio to baseline performance is undefined. For \(s<b\) it is negative and can be below −1 near the ceiling. Its magnitude depends on the starting score. At the justified accuracy ceiling \(u=100\) the RMM GTE example is \(6.8/36.4\approx0.1868\), identical to the relative reduction in judged error. The available-improvement helper is reusable and tested. The profiles retain raw differences because published rubric scales, suitability of ceilings and starting conditions differ. QA error reduction conveys a different endpoint from hallucination reduction.

## Empirical support

| Output or support category | Count |
|---|---:|
| Benchmark profiles | 785 |
| Mapped failure-mode profiles | 614 |
| Explicit baseline failure-mode profiles | 213 |
| Source-ordered failure-mode profiles | 401 |
| Studies / protocol blocks / potentially dependent cohorts in the failure matrix | 11 / 35 / 13 |
| Memory-performance proxy / direct hallucination or unfaithfulness rubric / direct task diagnostic cells | 555 / 38 / 21 |

All 785 estimates have one retained contrast, protocol, study and cohort per row. All weighting schemes therefore coincide. To check for candidates without this locality restriction, the pipeline drops study, source table and row, protocol and configuration IDs from the 384 explicit baseline keys while preserving benchmark, metric, oriented architectures, definitions and reported modifiers. It still finds 384 distinct semantic scopes, with zero multi-contrast, cross-study or cross-cohort matches. A still coarser independent audit before the version and budget refinements found 220 scopes and 56 with multiple rows, and zero cross-cohort and cross-study scopes. Among the 384 baseline contrasts, 71 reference observation IDs are reused. A shared source is evidence of dependence within those contrasts.

The [coverage table](../results/failure_mode_evidence_coverage.csv) records 614 available rows, 1,559 conditional candidates, 387 missing, 330 incompatible and three source-ineligible. An available row links to its estimate by `stratum`. Unavailable rows have identifiable source observations and reasons where Stage 1 supplied a candidate pair. An absent combination indicates no eligible evidence in the declared scope. The coverage figure counts distinct cohort labels by **target label** and failure mode. It does not combine numerical effects across those strata, and a coverage count does not represent independent replications.

## Interpretation for RQ3 and the seminar

- **BioMem, RealMem medical subset.** HMRU-R versus its A-Mem anchor with HuatuoGPT-3-27B gives **+3.03 points** on dynamic updating and **+3.20** on multi-session QA. HMRU-T versus that anchor gives **−25.00 points** on temporal reasoning (91.67 to 66.67) and **−12.12** on dynamic updating. These are directional rubric differences for controlled variants in one cohort. The differences illustrate how variants can help one memory operation while degrading another. They cannot establish performance on full RealMem. [QA heatmap](../figures/stage2b_failure_mode_heatmap.png)
- **SIRIN, gated Mem0.** Judge faithfulness-only versus ungated Mem0 reduces reported strict unfaithfulness among served answers from 35.1% to 23.2%, a **+11.9-point** effect. The judge answerability-only gate gives **−5.8 points** on the same measure. Gates can change which responses are served, so these differences concern the served-answer denominator in one cohort. [Selected profile](../figures/stage2b_selected_profile.png)
- **RMM versus RAG.** GTE, Stella and Contriever remain separate matched-retriever accuracy comparisons. The weights coincide on each. This is an illustration of within-protocol evidence and the limited scope of balancing, with no averaging across retriever strengths. [Weighting comparison](../figures/stage2b_weighting_comparison.png)
- **Failure-mode scope.** LoCoMo-Plus supports latent constraint application as a whole. Neither separate causal, state, goal and value effects nor isolated forgetting effects are inferred. HaluMem separates fabricated-or-incorrect QA from omission. Its extraction and updating candidates are documented in coverage, while this strict matrix has no eligible cross-architecture effects for those operation panels. LoCoMo false-premise diagnostics can reflect generic refusal and are distinguished from direct hallucination measurements. Project-state, updating, and temporal retrieval proxies stay apart from both direct categories. [Coverage matrix](../figures/stage2b_failure_mode_coverage.png)

## Uncertainty, unsupported aggregation and reproducibility

Source SD, SE, CI, sample counts and limitation fields are copied to the source contrast table where reported. There are 40 selected contrasts with marginal SDs on both sides and no selected marginal confidence bounds. For example, the published SIRIN paired served-accuracy gain intervals remain in the Stage 1 validated data and Stage 2A references. They apply to their own effect estimates, so they cannot serve as intervals for the profile estimates. This stage calculates no pooled intervals or significance tests. Weight-scheme agreement is a property of support and cannot establish sampling precision. Dependence-relevant gaps include aligned independent protocol replications, broader evidence for memory extraction and updating, denominators at matching coverage, and matched item-level predictions.

Pooling unlike metrics, benchmarks, baselines or architecture categories was rejected because the needed measurement or design alignment is absent. A global ranking would obscure the locally documented changes in direction.

Run from the repository root with Python 3.10+, Matplotlib and NumPy.

```bash
python -B -m unittest discover -s cluster_b_analysis/tests -v
python -B -m cluster_b_analysis.src.failure_mode_analysis
```

All **19 tests** passed, including the six original Stage 2A tests. Synthetic verification covered unequal support, shared baselines, duplicate direction and endpoint conflicts, missing and zero effects, ceiling gain, order invariance, outcome incompatibility and mapping. Independent review reproduced the production counts, the locality-free audit and the weighting identities. All four figures were generated in PNG and SVG. The Stage 1 source files and saved Stage 2A contrast table were preserved.

The main joins are through the stable `stratum` key in the [protocol summaries](../results/protocol_level_summary.csv), [cohort summaries](../results/cohort_level_summary.csv), [benchmark profiles](../results/benchmark_performance_profiles.csv), [failure-mode profiles](../results/architecture_failure_mode_profiles.csv), [weighting estimates](../results/weighting_comparison.csv) and [source contrasts](../results/stage2b_source_contrasts.csv). Source contrasts include both publication locators and the original numerical observation IDs.

## Stage 1D follow-up

The Stage 1D rebuild preserves the preceding results and adds four publications. See the updated counts, evidence limits and downstream verification in the [Stage 1D report](stage1d_report.md).
