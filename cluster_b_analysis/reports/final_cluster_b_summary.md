# Cluster B · Final audited research summary

RQ3 asks which memory architectures help mitigate specific failures in long-term episodic memory. The 24-publication evidence base supports local comparisons for named implementations and interventions. It does not identify a benchmark-independent winner on hallucination.

## Evidence and methods

| Corpus measure | Audited count |
|---|---:|
| Assessed publications | 24 |
| Verified numerical observations | 4,319 |
| Retained original observations | 3,168 |
| Eligible matched contrasts | 4,370 |
| Baseline-relative contrasts | 713 |
| Protocol blocks | 140 |
| Recorded dependence-cohort labels | 28 |
| Profiles / failure-mode profiles | 1,605 / 1,374 |
| Reviewed Pareto panels / edges robust over the tolerance grid | 9 / 39 |

Analysis uses direction-adjusted matched effects, exact-stratum hierarchical weighting, failure-mode profiles, within-panel competition ranks and Pareto dominance, and sensitivity to thresholds, objectives, preferences, transformations and evidence inclusion. Cohort balancing is descriptive. Each compatible profile has one endpoint, one protocol and one recorded cohort, so all four weights coincide. The 28 labels are bookkeeping for potentially dependent evidence. HaluMem and IMLogic, SIRIN and LongMemEval, and BioMem and RealMem share underlying histories or questions.

## Final answer to RQ3

- **MemOS** is the strongest local candidate for HaluMem QA. It leads on accuracy, incorrect-or-fabricated answers and omission in the two linked strict panels. Relative to Mem0 its hallucination category is lower by 4.00 pp on Medium and 0.68 pp on Long. The smaller difference is within a 1 pp exploratory tolerance. The study is developer-linked, so an external replication remains essential. Weak distractor rejection and reordering on memory-operation outcomes prevent broader claims.
- **SIRIN** merits prospective evaluation for selective answering. Judge faithfulness-only lowers strict unfaithfulness among served answers by 11.9 pp on Mem0 and 11.0 pp on LightMem, with 20 pp less coverage in both. Paired intervals concern served accuracy for specific policies. No all-query unfaithfulness reduction was established.
- **TRUSTMEM** is a localized consolidation candidate. On the reported matched-backbone Mem-T comparison, unsupported writes fall from 0.05% to 0.01% per transition. The very small absolute difference, unknown transition counts, and rule-based outcome scope constrain interpretation.
- **RootMem** additions improve local implicit-logic diagnostics. **BioMem HMRU-R** improves medical updating QA with a tolerance-sensitive margin, while **HMRU-T** loses on temporal and updating QA despite some recall gains. **RMM** helps judged QA within retriever choices, and **MemGPT** helps recover historical facts relative to summarization controls. These findings describe distinct proxies or diagnostics.

HaluMem QA, SIRIN Table 8 and original LongMemEval-M are the most useful narrow comparison panels. They answer different questions and should be shown separately. The broad review explains which findings transfer poorly and what kinds of evidence are missing. A narrow head-to-head makes the local contrasts, conditions and caveats directly inspectable. Neither resolves the lack of aligned independent replication for a pooled ranking. [Seminar findings](seminar_findings.md)

## Audit disposition

No critical issue invalidating an important conclusion was found in the targeted scope. Six major findings concerned retrieval-budget attribution, overlapping data lineage, developer-linked evaluation, the treatment of repeated-anchor ablations, the classification of resource metrics and notebook file discovery. Three minor findings concerned SIRIN scorer attribution, coverage metadata and rank terminology. Source numerical values and existing scientific estimands were preserved. Corrections affect documentation, the Stage 2E evidence categories, provenance metadata and notebook verification. [Scientific audit](final_scientific_audit.md) · [Mathematical audit](final_mathematical_audit.md) · [Claim evidence](../results/final_claim_verification.csv)

## Recovery and closeout

Both independent reviewers delivered final findings before the interruption. The mathematical checks, targeted comparison of 416 primary-source cells and eight published paired intervals, corrections, four reports and 12-claim ledger were recovered. The post-correction test and notebook logs were also intact. Closeout verified that the logs follow the latest code edits, the changed artifacts reflect the corrections, the claim ledger and report links are complete, and the original tables match their pre-audit checksums.

All 37 tests passed in the recovered final run. The executed notebook and HTML reconcile 26 regenerated artifacts without treating the audit claim table as a generated Stage 2 output. A relocated-checkout smoke test confirmed the documented launch directories. Full execution after a clean installation on a separate machine and a source-by-source audit of the remaining cells were outside the verified scope. Independent replication across protocols, all-query SIRIN unfaithfulness, and method-specific TRUSTMEM transition counts remain unresolved.

The project is ready for a final GitHub checkpoint with these qualifications. The audit deliverables and corrections remain local.
