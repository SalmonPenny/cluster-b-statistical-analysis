# Cluster B Stage 2A · Matched effect sizes

## Eligibility and analysis units

The loader joins `comparability.csv` to `validated_results.csv` by explicit left and right observation IDs. Both sources must be verified, original and marked `synthesis_exclude=no`. Only directly comparable within-block pairs are eligible. The loader checks agreement on the outcome, experimental identifiers, units and direction, and validates the protocol block and cohort against `comparison_blocks.csv`. When Stage 1 identifies a comparison family across distinct source block IDs, the output retains both source IDs alongside the shared protocol block.

Of 2,748 directly comparable within-block pairs in Stage 1, 2,704 met the source eligibility criteria. The 44 omitted pairs include at least one source failing that filter. The eligible pairs span 70 protocol blocks and 18 cohort groups. These groups can share questions, users, histories, judges or runs. The 2,704 pairs provide descriptive contrasts and do not establish 2,704 independent experiments.

| Stage 1 comparison type | Eligible pairs |
|---|---:|
| Evaluated systems | 1,078 |
| Controlled variants | 927 |
| Controlled scaling variants | 595 |
| Matched backbone systems | 80 |
| Matched retriever pipeline contrasts | 24 |

The [results table](../results/matched_effect_sizes.csv) has 342 baseline-relative rows, where exactly one member is explicitly labeled `baseline`. That member becomes the reference. The 2,362 other contrasts retain source order and are marked `pairwise`. These include comparisons between two baseline-role systems and between two variants. Their ratios are blank. A positive direction-adjusted difference favors the target.

## Effect definitions

Let *t* and *b* be the target and reference values in the same reported unit, and let *s* be +1 for higher-is-better metrics and −1 for lower-is-better metrics.

| Effect | Definition and applicability |
|---|---|
| Direction-adjusted absolute difference | *s(t − b)* in the reported unit. The sign indicates the better outcome. |
| Percentage-point difference | *s(t − b)* for scores reported as percentages, or *100s(t − b)* for proportions. Existing changes in percentage points remain on their reported scale in the absolute-difference column. |
| Relative performance improvement | *100s(t − b)/b* percent for an explicit baseline with *b > 0* and a meaningful ratio scale. Enabled for documented correctness rates, elapsed seconds and token counts. |
| Relative error reduction | *100(pₜ − pᵦ)/(1 − pᵦ)* percent for a documented higher-is-better correctness fraction *p*. Requires baseline correctness below 100%. For judge-scored QA this measures reduction in judged incorrectness. That category can include misses, misunderstandings and other non-hallucination errors. |
| Relative undesirable-event reduction | *100(eᵦ − eₜ)/eᵦ* percent for an explicit baseline with *eᵦ > 0*, and a directly measured lower-is-better event rate. Stage 2A enables it for explicitly labeled hallucination rates and strict unfaithfulness. The source rubric and denominator determine what the rate measures. |

Missing scores or directions, unsupported scientific interpretations and undefined ratios yield blank effects. A zero raw score remains a valid observation. At a zero baseline the correctness-error complement can still be meaningful. At perfect baseline correctness there is no baseline error to divide by. Unit disagreement and out-of-range bounded scores raise validation errors. Decimal calculation preserves input precision. Extra digits in calculated ratios describe arithmetic, not measurement precision.

## Worked example and limitations

RMM Table 1 holds the named retriever fixed for each comparison, while RMM and RAG differ in the rest of their pipelines. The GTE contrast moves LongMemEval QA accuracy from **63.6% to 70.4%**, a gain of **6.8 percentage points**. It gives **10.69% relative performance improvement** and **18.68% relative reduction in judged QA error**. The same table gives gains of 2.4 and 3.4 points for Contriever and Stella. These are descriptive complete-pipeline contrasts. [Matched retriever figure](../figures/matched_effect_sizes_example.png)

Reported sample sizes, run counts, SD, SE and confidence bounds are copied for each source when available, along with source details about their scope. They remain annotations to the individual source values. The paired uncertainty generally depends on covariance and run or item alignment. For example, RMM Table 1 supplies means over three runs and no dispersion. This analysis computes no new intervals. SIRIN unfaithfulness effects are conditional on answers served and can reflect changes in coverage. Overall and subgroup scores, repeated comparisons involving one reference, and evaluation variants sharing the same cohort must be kept together in any future inference.

## Reproduction

Run from the repository root using Python 3.10 or later and Matplotlib for the figure. The pipeline uses the three Stage 1 CSV inputs and does not need the source PDFs.

```bash
python -B -m unittest discover -s cluster_b_analysis/tests -v
python -B -m cluster_b_analysis.src.effect_sizes
```

All six focused tests passed. The pipeline completed once and produced the results CSV and PNG.

## Stage 1C rerun

The existing Stage 2A pipeline ran against the 16-paper evidence base without changes to its statistical modules. It produced **3,243 eligible contrasts**, including **384 baseline-relative** and **2,859 other pairwise** contrasts, spanning **90 protocol blocks** and **22 potentially dependent cohorts**. All 2,704 earlier effect records reproduced exactly, including their source identifiers, effect sizes and limitations. All six existing tests passed. The updated result and example figure are linked above.

## Stage 1D follow-up

The Stage 1D rebuild preserves the preceding results and adds four publications. See the updated counts, evidence limits and downstream verification in the [Stage 1D report](stage1d_report.md).
