# Cluster B · Long-term episodic memory

This directory contains the experimental database and statistical analysis for RQ3 of the AI Research Seminar. The integrated computational document explains the methods, reproduces the numerical results, and presents configuration-specific comparisons and candidate decisions. [Executed notebook](notebooks/cluster_b_analysis.ipynb) · [HTML export](notebooks/cluster_b_analysis.html) · [Execution report](reports/stage2f_report.md)

## Directory structure

| Path | Contents |
|---|---|
| `data/` | Corpus manifest, PDF index, source observations, verification, discrepancy log, pair comparability, protocol blocks, graphs and architecture registry |
| `papers/` | Local source PDFs used for extraction and Stage 1 provenance checks |
| `src/` | Reusable evidence, statistics and visualization modules |
| `results/` | Matched effects, cohort summaries, failure-mode profiles, fronts and ranks, sensitivity results and candidate selection |
| `figures/` | Scientific figures from the pipeline |
| `tests/` | Automated tests for the statistical modules and candidate selection |
| `notebooks/` | Executed Jupyter notebook and HTML export |
| `reports/` | Scientific methodology, stage reports and source-level qualifications |

Start with [the data dictionary](data/data_dictionary.md). Each source cell has a stable observation ID and a publication, page, table, row and column locator. `raw_results.csv` includes missing, digitized, imported and duplicate records. `validated_results.csv` contains verified numerical scores. Directional synthesis additionally requires retained original observations and a directly comparable matched protocol. `comparison_blocks.csv` and the matched effects preserve dependence cohort labels. The final matrix uses source IDs, configurations and benchmark-specific outcomes to distinguish matched effects, published context and evidence gaps.

## Install and run

From the repository root, install the pinned dependencies into a Python 3.12 virtual environment.

```bash
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r cluster_b_analysis/requirements.txt
```

Optional interactive frontend: install JupyterLab with `python -m pip install jupyterlab` and launch `jupyter lab`. Select the Python kernel for the environment above, open `cluster_b_analysis/notebooks/cluster_b_analysis.ipynb`, and run all cells. The notebook resolves the analysis root from the repository, analysis directory or notebook directory. On a machine where the default Python environment is read-only, use an installed environment on a writable path. The project cloud instance already contains the additional packages under `/workspace/.cluster-b-python/lib/python3.12/site-packages`; add that directory to `PYTHONPATH` only when using that specific installation. For HTML export in that cloud environment, also set `JUPYTER_PATH=/workspace/.cluster-b-python/share/jupyter` so nbconvert can find the installed templates. If the default Jupyter config path is read-only, set `JUPYTER_CONFIG_DIR` to a writable directory.

Fresh-kernel execution and export from the repository root:

```bash
python -m nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=180 cluster_b_analysis/notebooks/cluster_b_analysis.ipynb
python -m nbconvert --to html --output-dir=cluster_b_analysis/notebooks cluster_b_analysis/notebooks/cluster_b_analysis.ipynb
```

The notebook rebuilds Stages 2A–2E in a temporary directory. It compares regenerated CSV headers and complete row multisets against the validated saved outputs, then removes the temporary directory. Figures shown inside it are embedded in the HTML export. Math rendering in the default HTML export uses MathJax.

## Run the pipelines directly

The following commands regenerate the Stage 2 outputs **in the analysis directory**. The notebook is the read-only option for checking the preserved results.

```bash
python -B -m unittest discover -s cluster_b_analysis/tests
python -B -m cluster_b_analysis.src.effect_sizes
python -B -m cluster_b_analysis.src.failure_mode_analysis
python -B -m cluster_b_analysis.src.stage2c_analysis
python -B -m cluster_b_analysis.src.sensitivity
python -B -m cluster_b_analysis.src.candidate_selection
```

Stage 1 rebuilds use the reviewed canonical raw CSV and local PDFs. Keep source files at the paths recorded in the manifest. The following utilities rebuild the validated database, comparison tables and coverage figures from the saved sources.

```bash
python -B cluster_b_analysis/src/build_database.py
python -B cluster_b_analysis/src/coverage.py
```

The [Stage 1E report](reports/stage1e_report.md) lists extraction dispositions and unresolved provenance issues. The [Stage 2E report](reports/stage2e_report.md) explains how the evidence supports local recommendations and why the corpus cannot support a pooled architecture ranking.
