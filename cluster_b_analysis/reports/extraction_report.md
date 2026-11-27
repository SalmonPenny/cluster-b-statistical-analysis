# Cluster B Stage 1 extraction report

## Continuation batch

The continuation reused the original screening and added comparison panels from the eight publications below. Selection prioritized links through shared controls, source provenance, matched evaluation settings and useful uncertainty. Oracle Agent Memory remained eligible. Its LongMemEval headline has limited same-benchmark controls, whereas these panels connect named baselines or clarify how the benchmark was measured.

| Paper | Selected evidence and reason | Raw | Verified | Original retained |
|---|---|---:|---:|---:|
| LongMemEval | Tables 3, 4, 8. Original S/M, explicit reader and judge settings, indexing and temporal query-expansion controls. | 208 | 208 | 208 |
| LoCoMo | Tables 2–3. Original lexical QA controls with explicit context and retrieval variants. | 198 | 192 | 185 |
| Synthius-Mem | QA Tables 2–6. Shared system labels, original controlled category panels and visible benchmark/provenance differences. | 96 | 49 | 30 |
| Agent-Native Memory | Figures 7(a–f), 8(a), 9 and 12, Tables 2–5. Five-system LoCoMo comparisons within stated backbones and a LongMemEval-derived workload. | 311 | 311 | 302 |
| HaluMem | Tables 3–4. Original shared controls for three focal papers and a direct hallucination rubric. | 180 | 168 | 168 |
| MemGuard | Tables 1–3 and 7. Three priority benchmarks, paired retrieval variants and matched A-Mem reruns. | 298 | 225 | 88 |
| TRUSTMEM | Tables 1–4 and Figure 2. Shared HaluMem controls, matched Qwen policy comparisons and transition-level diagnostics. | 243 | 239 | 183 |
| SIRIN | LongMemEval Tables 5 and 8 and Table 8 caption. Matched selective-prediction interventions and paired uncertainty. | 172 | 160 | 160 |
| **Added** | **Eight previously unextracted papers** | **1,706** | **1,552** | **1,324** |
| **Cumulative** | **Twelve papers with detailed extraction** | **2,409** | **2,250** | **1,746** |

The 698 prior verified observations remain present. Distinct verified configurations increased from 173 to 581, and retained original configurations increased from 148 to 543. The cumulative database contains 83 printed missing cells and 76 unverified cited numeric values retained in raw data. Forty-seven MemGuard utility and 29 Synthius-Mem values could be transcribed from the citing tables only. Verified means the reported value is traceable to the relevant source. Original retained further filters source repeats, unresolved numerical or metric conflicts and derived summaries. The source records preserve table, physical PDF page, exact row and column, and qualification.

### Targeted discrepancy checks

**MemBook HaluMem-Long.** All 12 disputed values were matched again to the local HaluMem Table 4, arXiv:2511.03506v3. The arXiv listing identifies v1 and v2 in November 2025 and v3 on 5 January 2026. MemBook’s proceedings paper cites the unversioned identifier and gives no row-level run identifiers; its main Table 1 and HaluMem-Medium typewise cells share correctly labeled controls with the v3 source. The affected Long triples match Zep under MemBook’s Mem0 label, Memobase under Mem0-Graph, Mem0 under Supermemory and Mem0-Graph under Memobase. The Zep triple is starred because it uses update-task memories only. The primary database now includes the v3 results with their correct source labels. The MemBook values remain as printed and excluded. The evidence establishes the cross-source attribution conflict; the historical version or process responsible remains unknown. [HaluMem version history](https://arxiv.org/abs/2511.03506)

**MRAgent F1.** Appendix D.3 defines precision as C/M and recall as C/N for C binary judge positives, M returned answers and N questions. F1 = 2C/(M+N) is at least C/N when M ≤ N. This also holds when both rates are averaged with the same nonnegative weights across matched strata or runs. Changing weights, exclusions or denominators could reverse the inequality, but the paper does not document such a change. The authors’ linked code at commit `7441506db984b7c4da32e8dbeb2527f2e351270a` instead averages per-answer stemmed token-overlap F1 within each category and computes binary semantic accuracy separately. For example, a semantic judge may accept “NYC” for “New York City” while token overlap is zero. This directly explains how lower F1 can occur under the public implementation. Table outputs, exact run membership and implementation lineage remain unverified, so the 76 scores retain their transcriptions and exclusions. [Token F1 implementation](https://github.com/Ji-shuo/MRAgent/blob/7441506db984b7c4da32e8dbeb2527f2e351270a/eval/evaluation.py) · [Evaluation entry point](https://github.com/Ji-shuo/MRAgent/blob/7441506db984b7c4da32e8dbeb2527f2e351270a/eval/evaluate_reasoning.py)

The local LoCoMo v1 source really does describe 50 conversations and 7,512 QA items. The pinned MRAgent artifact instead contains 10 conversations and 1,986 QA items, of which 1,540 are non-adversarial. That count agrees with TeleMem, while table-run item membership and scorers are still distinct concerns. The prior LoCoMo discrepancy was revised accordingly. [MRAgent evaluation artifact](https://github.com/Ji-shuo/MRAgent/blob/7441506db984b7c4da32e8dbeb2527f2e351270a/data/dataset_locomo.json)

New flags cover the original LoCoMo printed 247.4% retrieval recall, Synthius controlled Overall aggregation, repeated Agent-Native F1 values, the MemGuard sampled cohort and category totals, and TRUSTMEM category and macro-average inconsistencies. Printed values remain visible with source locators and exclusion decisions. [Discrepancy log](../data/discrepancies.csv)

### Remaining evidence

Twelve papers remain eligible for detailed extraction. MemBench, LOCCO, RealMem, ES-MemEval, Towards Root Memory, LoCoMo-Plus, MemoryBench, MemoryRewardBench, TWIST, MemGPT, BioMem and Oracle Agent Memory are listed in the extraction status. Further extraction could materially improve **local** inference, especially a second explicitly aligned LoCoMo or LongMemEval cohort with paired outputs or an independent replication of the HaluMem judging protocol. Papers that mainly add new endpoints or unrelated cohorts improve coverage with limited impact on pooled identifiability. The remaining batch and statistical implementation require authorization. [Extraction status](../data/extraction_status.csv)

## Initial batch record

## Batch and evidence

All 24 local papers were screened across 534 physical PDF pages with PyMuPDF. Screening combined first-page identity, page-level terms, targeted evaluation sections and the repository’s preliminary `results_rq2.md` index. Benchmark mentions were distinguished from experimental use. The manifest lists 12 benchmark papers, 11 method papers and one survey with experiments. The full index and screening disposition are in [extraction_status.csv](../data/extraction_status.csv) and [pdf_page_index.csv](../data/pdf_page_index.csv).

The formerly flagged LongMemEval file is the ICLR 2025 paper with arXiv imprint 2410.10813v2 on its first page. The RMM file is the ACL 2025 Long Papers proceedings version, pages 8416–8439, identifier 2025.acl-long.413. First-page titles and authors agree with the metadata, and both SHA-256 hashes match the files in the existing download log. The records and PDFs were preserved.

No reliable live weekly Codex allowance was available. The four papers were selected for overlap and comparison design. MRAgent bridges LoCoMo and LongMemEval, TeleMem contributes independently run LoCoMo baselines, MemBook bridges LongMemEval and HaluMem, and RMM adds matched retriever contrasts on LongMemEval along with MSC results. Extractors verified both proposed and control rows, including unfavorable outcomes. The coordinator rechecked 553 headline table cells against their ordered source rows and inspected rendered layouts where grouped headers or source attribution required it. HaluMem original tables were checked for baseline provenance without performing detailed extraction of that paper.

| Paper | Completed scope in this batch | Raw cells | Verified |
|---|---|---:|---:|
| MemBook | Tables 1–4b, pp. 6–8, all settings and both HaluMem and LongMemEval panels | 241 | 241 |
| RMM | Tables 1–7, pp. 7–9, and explicit labels in Figures 4–5, p. 8 | 132 | 128 |
| MRAgent | Tables 1–3 and 5–6, pp. 7, 20–21, and numeric results in Figure 6(b) | 244 | 244 |
| TeleMem | Tables 1–3, pp. 7, 9, including the ZH-4O scaling grid and LoCoMo baselines | 86 | 85 |
| **Total** | **Four papers, with original-comparison and diagnostic panels** | **703** | **698** |

There are 173 distinct configuration IDs with a verified cell. The retained original subset contains 422 cells across 148 configuration IDs before pair-specific comparability checks. These are counts of published cells and configured runs or conditions, and can share histories, questions, retrieved evidence, judges or generated outputs. Five printed dashes remain in raw data only. RMM’s actual zero for no-history QA is verified. Among verified rows, 135 carry a repeat or source-link reference, including 12 conflicting cross-source attributions. Forty-eight MRAgent judge-subset cells report SD. The batch contains no reported SE or confidence interval.

## Verification decisions

- MemBook prints 68 values with matching system attribution in the HaluMem source. Its HaluMem-Long typewise table also carries 12 values that match different labels in the original. The database preserves printed values, source rows and exclusions. A-Mem and GAM numbers in the HaluMem tables have unclear provenance. The Qwen and GPT-4o-mini LongMemEval panels have separate configuration IDs, with the judging protocol and variant unresolved.
- RMM repeats several performance cells across main, ablation, backbone and budget tables. Source links maintain a single anchor per documented result. The GTE RMM pipeline raises LongMemEval QA accuracy from 63.6% to 70.4% relative to RAG with GTE. This contrast varies the full pipeline, including reranking and retrieval budget. On the same benchmark, Table 4 reports 56.6% for Long Context with Gemini-1.5-Pro versus 57.4% with Flash, contrary to its broad prose claim.
- MRAgent’s 35 Table 2 values repeat Table 5. Its 76 F1 values are verified transcriptions and remain excluded from synthesis because their relation to the judge scores conflicts with the reported formula under a common denominator. The LoCoMo cohort and metric interpretation were revisited in the continuation above.
- TeleMem’s temporal LoCoMo judge score is 78.47%, behind Long Context at 84.66%. Its 20.56% multi-hop score trails all five baselines. The proposed backbone is underreported in the headline panels. ZH-4O Table 2’s printed 14B-reader marginal differs from the mean of its displayed component cells, and the 8B/8B value may repeat the headline result.

Full issue and source locators appear in [discrepancies.csv](../data/discrepancies.csv). Unlabeled plot points were left unextracted. Repeated scores and unresolved definitions remain visible for traceability.

## Reproduction

From the repository root, use the existing Python installation. The database builder regenerates verification state, normalization and comparability outputs from the saved raw CSV. The PDF index is rebuilt from local files. The coverage script regenerates the matrices, edge and component lists, and both PNGs. Python includes no fitted models in this stage.

```bash
export PYTHONPATH=/workspace/.cluster-b-python/lib/python3.12/site-packages
export MPLCONFIGDIR=/tmp/cluster-b-mpl
python -B cluster_b_analysis/src/pdf_index.py
python -B cluster_b_analysis/src/build_database.py
python -B cluster_b_analysis/src/coverage.py
```

Twenty screened papers awaited detailed extraction at the end of the initial batch. MemGuard is a candidate bridge across the three focus benchmarks. The original benchmark papers and the agent-native survey are candidates for protocol controls, independent reruns and further provenance. Remaining figures and diagnostics from the selected papers remain eligible when they add distinct evidence. Author clarification or evaluation artifacts would help resolve dataset membership, judging, metric definitions and uncertain baseline provenance. Further extraction and model implementation require authorization.

## Stage 1C targeted expansion

Detailed extraction now covers **16 of the 24 papers**. Selection favored matched controls and additional outcome types. MemoryBench adds a within-system feedback contrast and item-level dispersion. LoCoMo-Plus extends evaluation to latent conversational constraints under a common rubric. RealMem adds shared-reader and shared-judge project-state comparisons. BioMem adds medical-subset controls and interventions on a frozen reader. All four source publications were already in the collection.

| Paper | Scope | Raw | Verified |
|---|---|---:|---:|
| MemoryBench | LoCoMo cells from Tables 13–14 and full Table 17 | 26 | 25 |
| LoCoMo-Plus | Complete Tables 1 and 3, including the judge-sensitivity panel and derived gaps | 154 | 154 |
| RealMem | Complete Tables 2–4, including reference conditions and missing session cells | 124 | 106 |
| BioMem | RealMem medical-subset Tables 2 and 4, plus exact reported paired outcomes from Figures 5a, 7a and 7c | 306 | 306 |
| **Added** | | **610** | **591** |

The cumulative raw count is 3,019. Verified observations increased from **2,250 to 2,841**, verified configurations from **581 to 747**, and retained original observations from **1,746 to 2,266**. The 19 new missing cells remain in raw data. Both earlier evidence databases and all prior comparison decisions were reproduced row-for-row.

- MemoryBench Table 17 reports a combination of feedback, additional dialogue and a second response. A-Mem gained 0.0280 F1 and MemoryOS fell 0.0014. Printed differences are retained as derived diagnostics. The Tables 13–14 SDs describe items, not repeated experiments. The effects group pairs within their original table, so continuation-table cross-system pairs are not counted.
- LoCoMo-Plus factual aggregates remain conditional. One common category weighting cannot reproduce the table averages at the reported precision, and the Qwen3-8B judge-sensitivity aggregate is 56.89 versus 56.86 in the headline table. The primary judge identity for the headline panel is unreported. Matched GPT-4o category contrasts use the paper's shared rubric.
- RealMem's Graph Memory session QA leadership applies to the GPT-4o-mini column. LightMem leads the non-oracle GPT-4o session column. RealMem Table 4 omits the specific answer generator and context construction. Keep these category outcomes conditional.
- BioMem's 12 lower-precision Table 2 A-MEM observations repeat the more precise Table 4 anchor and remain excluded from synthesis. The 325-question perfect-answer panels are diagnostics. Within the HuatuoGPT-3-27B comparison, HMRU-R fixed 26 A-MEM outcomes and broke 10, with published paired McNemar p=0.011. This descriptive paired evidence is specific to that cohort and endpoint. It supplies no additional replication of the mean rubric-score comparisons.

Eight papers remain eligible for detailed extraction: MemBench, LOCCO, ES-MemEval, Towards Root Memory, MemoryRewardBench, TWIST, MemGPT and Oracle Agent Memory. [Extraction status](../data/extraction_status.csv) · [Discrepancy log](../data/discrepancies.csv)

## Stage 1D follow-up

The Stage 1D rebuild preserves the preceding results and adds four publications. See the updated counts, evidence limits and downstream verification in the [Stage 1D report](stage1d_report.md).

## Stage 1E follow-up

The last four publications are assessed and all 24 extraction dispositions are complete. The new sources add 505 verified observations and six eligible matched contrasts. [Stage 1E report](stage1e_report.md)
