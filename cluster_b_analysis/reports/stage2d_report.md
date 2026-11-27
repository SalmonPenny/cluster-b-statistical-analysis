# Cluster B Stage 2D · Sensitivity and robustness

## Scope and interpretation

The analysis starts from the five reviewed Stage 2C panels, 29 configurations and 73 unordered within-panel pairs. Panel boundaries, original scores, objective definitions and configuration IDs stay in place. The saved Stage 2A table supplies alternative effect sizes for the same matched comparisons. All exercises are descriptive. Tolerance changes test analytical conventions, weight changes test preferences, and evidence exclusions test eligibility. Sampling uncertainty is a separate question. Neither a change across scenarios nor a sampled preference share is a confidence interval or a posterior probability.

## Practical-equivalence tolerances

For oriented differences \(d_j=z_j(A)-z_j(B)\), classify each objective as a win when \(d_j>t\), a loss when \(d_j<-t\), and otherwise a tie, including the boundaries. The directed tolerance relation \(A\to_t B\) requires all \(d_j\ge -t\) and at least one \(d_j>t\). At zero this is ordinary Pareto dominance. The five panels use percent-reported objectives, so 0, 0.5, 1, 2 and 5 are percentage-point thresholds on the displayed scales. They are exploratory practical tolerances with no validation as equivalence margins.

| Panel | Directed edges at 0 / 0.5 / 1 / 2 / 5 pp |
|---|---|
| BioMem medical | 5 / 5 / 5 / 5 / 3 |
| SIRIN Mem0 | 2 / 2 / 4 / 5 / 5 |
| SIRIN LightMem | 5 / 6 / 6 / 6 / 7 |
| HaluMem Medium | 10 / 11 / 11 / 9 / 10 |
| HaluMem Long | 5 / 6 / 7 / 7 / 8 |

Twenty of the original 27 directed edges survive all tested thresholds. Seven depend on threshold. A positive threshold can hide a small deficit and create an edge, or absorb a small advantage and remove one. The relation can cycle, as verified synthetically. No cycles occur on this grid. HaluMem Long at 5 pp nevertheless contains a non-transitive chain: Zep → Mem0-Graph → Mem0, while Zep ↛ Mem0. The direct Zep versus Mem0 deficit in reduced hallucination is 5.22 pp. Successive fronts use zero-tolerance dominance only. [Tolerance table](../results/tolerance_sensitivity.csv) · [Threshold-grid figure](../figures/stage2d_tolerance.png)

## Objectives and preferences

Each objective was omitted in turn, with at least two objectives required to recompute a front. Twelve omissions were evaluated. The two BioMem omissions leave single-objective comparisons, so they are recorded as skipped. MemOS remains the sole front member under every omission in both HaluMem splits. SIRIN front membership changes. Removing coverage drops ungated from both fronts, and dropping strict unfaithfulness adds Mem0's Judge answerability gate to the front. The results show dependence on whether the decision prioritizes serving answers, correct served answers, or fewer flagged served answers. [Objective omissions](../results/objective_selection_sensitivity.csv)

For an explicitly exploratory linear preference model, higher-is-better objectives use \(u=x/100\), and lower-is-better objectives use \(u=(100-x)/100\). This uses the natural percent reporting scale and keeps the same utility endpoints across systems in each panel. It assumes linear marginal utility in displayed points. A point in one rubric need not have the same practical significance as a point in another. Weights are nonnegative and sum to one. The two-objective analysis solves pairwise line intersections for the first weight \(w\in[0,1]\), evaluates the upper envelope on each interval, and splits exact co-winner share. Three-objective panels use 4,000 reproducible Dirichlet(1,1,1) draws with seed 27 and split numerical ties. These shares describe a hypothetical preference distribution and can change with utility scaling or weight distribution.

HMRU-R wins for every positive updating weight and ties A-Mem and HMRU-I when the weight on updating is exactly zero. MemOS wins every sampled weighting in both splits. SIRIN shares (ungated / Judge faithfulness / Judge both gates) are **50.70% / 32.58% / 16.73%** for Mem0 and **50.03% / 18.73% / 31.25%** for LightMem. The other gates have no winning sampled weights. Nondominated points need not maximize a linear score on a region of positive weight. [Preference table](../results/objective_weight_sensitivity.csv) · [SIRIN preference figure](../figures/stage2d_objective_weights.png)

## Effect scale and SIRIN denominator checks

Raw scores and recorded directions establish the point-estimate fronts. Strictly increasing transformations of an objective preserve them. For each Stage 2A transformation, the effect comparison uses the identical eligible pair of contrasts on both scales. The 795 within-stratum checks match study, source table, benchmark, task, outcome definitions, units, evidence class, system labels, backbones and judges. All preserve the raw effect ordering. The three extra rows are a labeled cross-framework normalization illustration using two separately matched Table 8 contrasts. LightMem's Judge both-gates served-accuracy gain of +14.3 pp exceeds Mem0's +13.2 pp, but the corresponding relative performance gains are 28.49% and 34.92%. The order reverses because references differ (50.2% and 37.8%). Relative judged-error reduction gives LightMem 28.71% versus Mem0 21.22%. These are effect magnitudes on their respective served subsets. They cannot rank frameworks or quantify hallucination reduction. [Effect-scale checks](../results/effect_size_sensitivity.csv)

For a common scored population and consistent weighting, \(P(\mathrm{serve}\cap\mathrm{unfaithful})=P(\mathrm{serve})P(\mathrm{unfaithful}\mid\mathrm{serve})\). The saved Table 8 records establish a nominal 500-query cohort per framework and exact configurations. They do not establish the served-answer denominator or absence of scorer filtering and weighting differences. Ungated systems report full coverage and 35.1% or 33.1% strict unfaithfulness. A binary count over 500 answers advances in 0.2 pp increments and cannot yield those values at the printed one-decimal precision. This does not diagnose the cause, but it precludes assuming an all-500 unweighted count.

The empirical all-query frequency therefore remains blank. The product is shown solely as an assumption-conditional scenario from rounded rates. For Mem0 Judge both versus Judge faithfulness, the conditional rates are 28.7% versus 23.2%, while the scenario products are 17.79% versus 18.56% because coverage falls from 80% to 62%. The scenario counts unfaithful answers emitted per query. It cannot tell how a system would have answered abstained queries and gives those queries no correctness credit. The reported paired bootstrap intervals are for served-accuracy contrasts, including Mem0 both Judge gates versus ungated (+13.2 pp, 95% interval +10.1 to +16.4). They remain available unchanged. There is no joint uncertainty for the products, their differences or the three objectives. [Denominator scenarios](../results/sirin_denominator_sensitivity.csv) · [Scenario figure](../figures/stage2d_sirin_denominators.png) · [Original paired intervals](../results/pareto_reported_uncertainty.csv)

## Evidence inclusion and seminar findings

- **HaluMem MemOS is locally robust.** In both splits its 9 combined dominance edges against strictly eligible alternatives persist over all thresholds. Every two-objective omission leaves MemOS alone on the first front. Adding conditionally comparable Long Memobase leaves this frontier unchanged. Its category nonclosure and method-specific 500-token retrieval cap remain explicit. QA accuracy, fabricated-or-incorrect answers and missing-memory omissions share the same questions and are strongly related.
- **BioMem distinguishes intervention variants.** HMRU-T remains dominated by the other three variants at every tested tolerance; temporal reasoning and dynamic updating are its prominent weaknesses. HMRU-R's 3.03 pp updating edge over A-Mem and HMRU-I becomes a tie at 5 pp. Their temporal scores are equal as printed. The comparison is confined to the medical subset and reported reader.
- **SIRIN depends on coverage preferences and denominators.** Gated and ungated winners differ with the weight set. Better served accuracy alone does not settle the policy choice. The all-query scenario can reverse a conditional-rate comparison, but cannot establish the empirical all-query rate or its uncertainty.
- **Evidence removal limits rather than replicates the conclusions.** Keeping only the direct rubric endpoints leaves one objective in HaluMem and SIRIN and none in BioMem. Their selected QA, service and omission objectives measure distinct aspects. A multi-objective direct-only frontier is unavailable. Removing each panel's only study, benchmark or cohort removes its evidence. Stage 2B found no aligned pooled estimate for leave-one-out robustness. Incompatible cross-study candidates were not introduced to create one.

The strongest presentation points are the persistence of MemOS's local dominance, the different robustness of HMRU-R and HMRU-T, and the SIRIN service-versus-conditional-evaluation trade-off. Each is panel-specific. [Evidence eligibility](../results/evidence_selection_sensitivity.csv) · [Claims and source observation IDs](../results/robust_findings.csv)

## Reproduction and verification

Run from the repository root with the existing NumPy and Matplotlib environment.

```bash
python -B -m unittest discover -s cluster_b_analysis/tests
python -B -m cluster_b_analysis.src.sensitivity
```

All 31 tests passed, including all 24 earlier tests. The run produced 365 pair-threshold records, 14 objective-omission records, 29 weight-share estimates, 798 matched transformation checks or illustrative comparisons, and 14 denominator scenarios. Independent checks reproduced the tolerance results and preference calculations and verified byte-identical regeneration of the seven CSVs and six figure files. Earlier results were read as inputs.

## Stage 1D follow-up

The Stage 1D rebuild preserves the preceding results and adds four publications. See the updated counts, evidence limits and downstream verification in the [Stage 1D report](stage1d_report.md).
