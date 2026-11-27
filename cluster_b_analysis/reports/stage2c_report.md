# Cluster B Stage 2C · Within-panel Pareto comparisons

## Eligibility and estimand

This analysis compares printed point estimates for specific system configurations under reviewed source protocols. Each objective vector is joined by the Stage 1 configuration ID within a source study, table and block. Only original, verified, synthesis-eligible source cells are used. Benchmark, version, split and generation backbone must agree within each panel. Scorer, definition and units must agree across configurations for each objective. Every retained pair is checked against the Stage 1 within-block evidence for every objective. SIRIN Table 8 abstention has one narrow exception: Stage 1 excludes this comparison because there is no declared direction, and the panel explicitly takes higher answer coverage as its operational objective. This uses the same abstention measurements with minimization equivalent to maximizing \(100-\mathrm{abstention}\) on the percent scale. No other incompatibility is overridden.

Five reviewed panels contribute 29 complete vectors out of 32 candidate configurations, covering 73 of 92 possible within-panel configuration pairs. SIRIN's oracle is excluded in both Table 8 panels because of its privileged information and absent strict-unfaithfulness objective. The HaluMem Long Memobase configuration is excluded from all its objectives because Stage 1 flags a category nonclosure and deems its comparisons conditional. Eligible, excluded and rejected scopes are recorded with reasons. Whole and medical RealMem, cross-split HaluMem, cross-framework SIRIN, incompatible cost denominators and LoCoMo versus LoCoMo-Plus have no common front. MemoryBench feedback has a single outcome in the matched panel. Retriever and scale sweeps were not spliced into the chosen objective vectors. [Eligibility and pair coverage](../results/pareto_eligibility.csv)

BioMem uses intervention variants of A-Mem with a frozen HuatuoGPT-3-27B reader; the two QA rubric outcomes target dynamic updating and temporal reasoning in the RealMem medical subset. SIRIN uses separate Mem0 and LightMem gate panels for served accuracy, strict unfaithfulness among served answers, and coverage. HaluMem uses separate Medium and Long complete-system QA comparisons on accuracy, benchmark-labeled hallucination, and omission. The last three outcomes share a denominator and are nearly a partition. An accuracy and omission advantage must therefore be interpreted together with incorrect-or-fabricated answers. The source-specific comparison classes appear in the pair output. [Source classes and pairwise outcomes](../results/dominance_relations.csv)

## Mathematical conventions

For objective \(j\), orient each reported score \(x_j\) as \(z_j=x_j\) for higher-is-better and \(z_j=-x_j\) for lower-is-better. Weak dominance means \(z_j(A)\geq z_j(B)\) on every objective, including identical vectors. Standard Pareto dominance adds a strict inequality on at least one objective. Strict dominance requires better scores on every objective. The first front consists of all complete vectors with no standard dominator. Further fronts apply the same rule after removing the preceding front. Identical vectors stay on the same front. Each strictly increasing change of an original objective scale preserves its ordering and ties, so standard Pareto membership needs no common numerical scale. Decimal comparisons use the displayed precision. There is no tolerance adjustment because the panels do not establish a practical equivalence margin.

Per-objective competition rank is one plus the number of configurations with a better oriented score. Exact ties share a rank and occupy its positions, for example 1, 1, 3. A reversal is a pair with opposite preferences on two objectives; a tie alone cannot produce one. Win, tie and loss counts describe objectives within a pair. The resulting 27 standard-dominance pairs, 45 pairs with opposing objectives and one identical pair share systems and cohorts. There are 82 objective-pair reversals across the five panels. These counts describe the observed design and are not independent evidence or sampling uncertainty. [Ranks](../results/within_panel_rankings.csv) · [Reversals and linked Stage 2B contrasts](../results/failure_mode_tradeoffs.csv)

## Empirical fronts and RQ3 trade-offs

| Panel | First front at printed point estimates | Systems |
|---|---|---:|
| BioMem medical | HMRU-R | 4 |
| SIRIN Mem0 | Ungated, Probe answerability, Probe both gates, Judge faithfulness, Judge both gates | 7 |
| SIRIN LightMem | Ungated and all three Judge variants | 7 |
| HaluMem Medium | MemOS | 6 |
| HaluMem Long | MemOS among the strictly eligible systems | 5 |

**BioMem.** HMRU-R reaches 94.95% on dynamic updating and 91.67% on temporal reasoning. The base A-Mem and HMRU-I both score 91.92% and 91.67%. On these objectives HMRU-R **standard-dominates** the base and HMRU-I through updating while tying temporal reasoning. HMRU-T drops to 79.80% and 66.67%, behind all three configurations. HMRU-R and HMRU-T are separate variants. The two selected QA objectives show a weakness and no strict rank reversal on this panel. Other QA or recall endpoints can change the objective set. [BioMem Pareto figure](../figures/stage2c_biomem_pareto.png)

**SIRIN.** For Mem0, Judge both gates raises served accuracy from 42.8% to 51.0% relative to Judge faithfulness alone, while strict unfaithfulness rises from 23.2% to 28.7% and coverage falls from 80% to 62%. For LightMem, the same gate change increases served accuracy from 56.2% to 64.5%, ties conditional unfaithfulness at 22.1%, and reduces coverage from 80% to 63.6%. An ungated system can remain on the first front because it serves every query. Gate changes alter the subset whose correctness and faithfulness are scored. The conditional unfaithfulness rates cannot establish unconditional hallucination reduction over all questions. No combined unconditional rate was inferred from the summary table. [Coverage and served outcomes](../figures/stage2c_sirin_coverage.png)

**HaluMem.** MemOS dominates each other retained configuration on all three objectives within each split. Rival systems exhibit trade-offs. On Long, Mem0-Graph versus Mem0 improves accuracy (32.44% versus 28.11%) and lowers omission (45.74% versus 54.60%), while benchmark-labeled hallucination rises (21.82% versus 17.29%). The rubric category pools fabricated and other incorrect answers. Medium and Long reuse source users. The conclusion concerns evaluated systems under their reported settings and does not imply independent replication or an effect of the architecture family. [Medium ranks](../figures/stage2c_halumem_rank_reversals.png) · [All front layers and source IDs](../results/pareto_fronts.csv)

## Evidence limits and verification

The fronts are relative to the evaluated system set, selected endpoints and displayed values. They convey descriptive dominance and do not establish statistical dominance. The reported SIRIN Table 8 paired intervals are preserved separately: four author-reported served-accuracy gain estimates with intervals, and four Probe-minus-Judge intervals without printed point estimates. For example, the Mem0 judge both-gates served-accuracy gain against ungated is +13.2 points, with a reported 95% interval of +10.1 to +16.4. This supports the specified served-accuracy contrast only. It is not a joint interval for coverage, unfaithfulness and served accuracy. No new uncertainty was calculated. [Reported paired intervals](../results/pareto_reported_uncertainty.csv)

For the seminar, the BioMem result illustrates variant-specific weaknesses; the SIRIN panels show why service coverage and faithfulness must be discussed together; and HaluMem demonstrates that an accuracy advantage can coincide with a higher benchmark error subtype. These are locally supported RQ3 conclusions. Missing matched outcome sets, incompatible protocols and unresolved dependence still limit broader ranking.

From the repository root, run:

```bash
python -B -m unittest discover -s cluster_b_analysis/tests
python -B -m cluster_b_analysis.src.stage2c_analysis
```

All 24 tests passed, including all 19 earlier tests. Synthetic fixtures verified weak, standard and strict dominance, exact ties, non-dominated and successive fronts, missing objectives, incompatible panels, lower-is-better objectives, rank reversals, system-order invariance and monotone-transform invariance. The pipeline produced six CSVs and three figures in PNG and SVG. Independently computed fronts and pair counts matched the pipeline. An independent rerun reproduced all 12 CSV and figure files byte-for-byte.

## Stage 1D follow-up

The Stage 1D rebuild preserves the preceding results and adds four publications. See the updated counts, evidence limits and downstream verification in the [Stage 1D report](stage1d_report.md).

## Stage 1E follow-up

Three matched MemGPT reader panels raise the total to nine panels, 46 vectors and 131 within-panel pairs. All prior results reproduce. [Stage 1E report](stage1e_report.md)
