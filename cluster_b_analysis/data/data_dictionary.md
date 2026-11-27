# Stage 1 data dictionary

## Observation tables

`raw_results.csv` has one record per extracted publication table or figure cell, including printed dashes. `validated_results.csv` contains the subset with a verified numerical transcription. Verification establishes what a source reports. It can coexist with a duplicate, unresolved definition, protocol limitation or conflicting source attribution. For a provisional set of distinct original cells, require `provenance=original` and `synthesis_exclude=no`, then apply the comparability criteria for the intended contrast.

| Columns | Meaning |
|---|---|
| `observation_id` | Stable hash of paper ID, physical PDF page and the table, row and column locator. Two printed locations get different IDs even if they report the same result. |
| `paper_id`, `paper_title`, `publication_id`, `pdf_filename`, `publication_version`, `source_url` | Local manifest key, title, official publication identifier, local file, version of the local file and source landing page. Physical pages are one-based. |
| `pdf_page`, `table_id`, `source_row`, `source_column` | Source locator. Grouped headers are joined by `|` or `/`. Figure labels identify explicitly printed values. Supplementary digitization from unlabeled plots appears in the raw table only, with the estimate, coordinate method and readability noted. A graphically hidden mark has no point estimate. |
| `architecture`, `architecture_version`, `rq2_category`, `mechanisms`, `role` | Harmonized display label, reported implementation/version if known, existing RQ2 assignment where available, mechanisms and source role. The TeleMem value records its existing scope flag. Same name can denote different implementations. |
| `backbone`, `judge`, `judging_protocol` | Reported language models, scoring model if used and scoring procedure. Distinct models can build, retrieve, generate and judge. |
| `retrieval_budget`, `memory_budget`, `context_budget` | Documented settings. A reported average history length differs from a model context-window limit. |
| `block_id`, `configuration_id` | Source-specific comparison grouping and system × evaluation setup ID. Configurations are shared across metrics or subsets in an experimental setup. Some records represent ablation variants, reference conditions or diagnostics. A configuration is a bookkeeping unit and can share data, judged predictions or runs with other configurations. |
| `benchmark`, `benchmark_version`, `split`, `task` | Harmonized benchmark name, reported variant, split or evaluated scope, and outcome subset. No full benchmark edition is inferred from the name alone. |
| `metric`, `metric_definition`, `direction` | Source measurement, operational definition and better direction. Matching names can have different implementations. |
| `score`, `score_as_printed`, `unit` | Numerical point value on the original scale, source token when captured with all its formatting and the original unit. Dashes are missing. Numeric zero is a value. |
| `normalized_score`, `normalized_unit` | Percentages converted to proportions and thousands of tokens converted to tokens. Values on the proportion scale are preserved. Percentage-point changes remain on their reported scale. Unit conversion conveys no measurement equivalence. |
| `sample_size`, `independent_runs`, `sd`, `se`, `ci_lower`, `ci_upper` | Reported counts and dispersion or interval endpoints. Some sample sizes are nominal benchmark counts, identified in `source_details`. Dispersion uses the original score scale. A missing dispersion value is unknown. |
| `failure_mode`, `hallucination_measurement` | Relevant capability or failure and whether the metric is `direct`, a `proxy`, or `n/a` for other outcomes such as cost. HaluMem’s QA hallucination category includes incorrect as well as fabricated answers under its rubric. |
| `provenance`, `original_source`, `verification` | `original` indicates in-study evaluation, `imported` indicates reproducible values from a separate source, and `unclear` indicates insufficient provenance. A cell is `verified`, `unverified`, or `missing`. |
| `duplicate_of`, `discrepancy`, `synthesis_exclude` | Source reference of repeated or conflicting cells, machine-readable flag where present, and explicit exclusion of duplicates, conflicts, inconsistent metric definitions and selected derived values. Use provenance jointly with the exclusion field. |
| `comparability_status`, `limitations`, `source_details` | Highest available within-block pair status for the observation, explanatory caveats, and additional reported fields represented as a JSON object, such as retriever, model size, and basis of sample size. The actual pair classification is in `comparability.csv`. |

The continuation stores the authors’ per-cell display values in `score_as_printed` when available. An out-of-range printed percent with an explicit discrepancy and synthesis exclusion retains its raw score and has no normalized score. Paired interval endpoints apply to the listed effect estimate and unit. Additional interval-only evidence and source note fields appear in `source_details`.

Stage 1E preserves reward-model evaluations as a separate evaluand. A verified reward-model cell can carry a synthesis exclusion even when the reward configuration and score are fully identified.

Blank CSV cells represent unreported, unavailable or inapplicable fields. No imputation is performed. Uncertainties and sample sizes apply to a row only at the scope described by the paper and any recorded note.

## Related files

- `comparability.csv` holds candidate pairs per source panel, benchmark, split, task, metric and unit, and separate cross-study protocol screens. For cross-study protocol rows, observation IDs and outcome fields are blank. Direct means a documented within-panel protocol supports a descriptive contrast, with evaluated system and controlled component contrasts identified in `evidence_type`. Conditional means a judge, backbone, baseline origin, oracle intervention or other protocol modifier limits inference. Incompatible includes mismatched definitions and attribution conflicts. Missing covers absent or unverified cells. A repeated anchor can be used within a reported ablation without counting the score twice in analysis.
- `discrepancies.csv` records known deviations between source tables, formulas, prose and the project’s preliminary extraction index. Multiple cells can share an issue.
- `architecture_benchmark_coverage.csv` and `architecture_metric_coverage.csv` count distinct configurations with at least one retained original cell for the column. Zero denotes absent coverage under that filter. Metrics are benchmark-qualified to keep distinct constructs separate.
- `comparison_graph_edges.csv` links headline architecture pairs to within-study panels and documented statuses. `comparison_graph_components.csv` enumerates connected components of the strict and relaxed projections onto architecture labels.
- `comparison_blocks.csv` records direct source-block and table combinations, their reported outcomes and whether the block provides strict headline graph edges. `cohort_group` conservatively groups panels that share or may share evaluation items. Distinct group identifiers provide an upper bound, not a verified count of independent replicates.
- `comparison_sensitivity.csv` gives strict and relaxed connectivity after removal of each graph-contributing study or benchmark while keeping the observed architecture labels fixed.
- `benchmark_failure_mode_mapping.csv` links tasks and metrics to failure modes and their source definitions. `extraction_status.csv` records the screening and extraction disposition of every paper. `pdf_page_index.csv` counts search term hits per physical page to guide further reading. Matches in citations or references are only search hits.
