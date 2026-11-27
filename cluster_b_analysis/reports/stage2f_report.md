# Cluster B Stage 2F · Notebook execution and reproducibility

The executed notebook integrates the 12 requested research and teaching sections. It covers the 24-publication Stage 1E database, comparability, effect sizes, cohort weighting, failure-mode profiles, Pareto and sensitivity analysis, candidate selection, benchmark-specific comparisons, and why the evidence cannot support pooled ranking. Mathematical notation, worked examples and nine captioned figures appear alongside the regenerated results.

## Execution checks

- **Fresh kernel.** Executed all 13 code cells sequentially using the configured Python 3.12 environment and retained their outputs. The notebook schema validated successfully and the saved notebook has no error outputs.
- **Tests.** All 37 existing tests passed via `python -B -m unittest discover -s cluster_b_analysis/tests`.
- **Reproduction.** Stages 2A–2E ran through the existing modules in an isolated temporary copy. The regenerated headers and complete row multisets matched all 26 checked CSV artifacts, including the architecture registry. The notebook also checked 24 assessed publications, 4,319 verified observations, 3,168 retained originals, 4,370 matched effects, 713 baseline-relative effects, and 39 dominance relations robust to the tolerance grid. All 1,605 weighting profiles reproduced exactly across the four weighting schemes.
- **Preservation.** The notebook reads the reviewed Stage 1E inputs and uses the regenerated tables in its displays. It deletes the working copy at the end. Source datasets, earlier results, reports and figures are preserved. The corpus extraction and source locator decisions remain sourced to Stage 1E.
- **HTML.** Verified that the export includes all 12 sections, numerical outputs and embedded research figures. The default HTML template uses MathJax for equation rendering and reports that the nine displayed images lack formal alternative text. Each has an accompanying visible caption.

The first notebook execution exposed a string-escaping issue in a generated cell. After correction the code passed the fresh-kernel run. HTML export required the configured cloud prefix on `JUPYTER_PATH` so nbconvert could locate its template resources. The mathematical markup was then checked in the HTML. Presentation edits to LaTeX after the run preserved the executed code and outputs.

## Files

- [Executed notebook](../notebooks/cluster_b_analysis.ipynb)
- [HTML reading copy](../notebooks/cluster_b_analysis.html)
- [Reproduction guide](../README.md)
- [Pinned dependencies](../requirements.txt)

This stage checks computational reconciliation with saved results. The unresolved scientific limits remain those reported in Stages 1E and 2E, including the absence of aligned independent replication, missing paired uncertainty for most contrasts, and incompatible hallucination or unfaithfulness denominators. [Stage 1E](stage1e_report.md) · [Stage 2E](stage2e_report.md)

## Stage 3 follow-up

The final audit corrected the notebook’s artifact manifest and reran it with the independent claim ledger present. The revised Stage 2E resource classification and coverage metadata reproduce. [Mathematical audit](final_mathematical_audit.md)
