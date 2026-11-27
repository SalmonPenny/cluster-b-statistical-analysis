# Cluster B · Seminar findings

## 1. Research question and evidence

Which approaches to long-term episodic memory help with specific hallucination or memory failures? We assessed 24 publications and verified 4,319 numerical observations, of which 3,168 are retained originals. There are 4,370 eligible matched contrasts, 713 explicit baseline contrasts, 140 protocol blocks and 28 recorded cohort labels. Shared users, histories, generated answers and baselines rule out treating these counts as independent experiments.

## 2. What the analyses show

- **Matched effects** preserve outcome direction and source units. RMM versus GTE RAG moves LongMemEval QA from 63.6% to 70.4%. That is +6.8 percentage points and 18.68% relative reduction in judged QA error.
- **Protocol and cohort weighting** changes no estimate across 1,605 singleton compatible profiles. This is evidence of sparse compatible replication.
- **Pareto and sensitivity** show where differences favor a system on every selected endpoint and where the answer depends on trade-offs. Nine panels contribute 39 dominance edges that persist over the tested practical tolerances. These are descriptive comparisons on printed scores.

## 3. Three head-to-head panels

| Panel | Result to present | Qualification |
|---|---|---|
| HaluMem QA · Table 3 | MemOS reports 15.17% vs Mem0 19.17% on Medium, and 16.61% vs 17.29% on Long, with favorable accuracy and omission as well. | Rubric includes incorrect and fabricated responses. Splits share users. The benchmark and MemOS teams share authors. Retrieval settings and memory APIs vary by system. MemOS shows weak distractor rejection in the separate extraction diagnostic. |
| SIRIN · Table 8 | Judge faithfulness-only improves served-answer unfaithfulness by 11.9 pp on Mem0 and 11.0 pp on LightMem. | Both give up 20 pp of answer coverage. Retrospective thresholds are unverified in deployment. Published intervals refer to served accuracy for selected contrasts. |
| Original LongMemEval-M · Tables 3–4 | Session plus fact keys improve fixed-reader QA from .670 to .714. Applying GPT-4o expansion with fact keys improves temporal Recall@5 from .639 to .722 versus plain keys. | Shared question lineage and local workflow. These are proxy and diagnostic outcomes. |

## 4. Architecture-specific follow-ups

TRUSTMEM versus Mem-T gives a 0.04 pp transition-hallucination reduction on one consolidation protocol. RootMem additions have robust gains against their individual bases on IMLogic, whose forced-choice questions reuse HaluMem histories. BioMem HMRU-R improves medical updating QA by 3.03 pp while HMRU-T loses 25.00 pp on temporal QA and gains 12.50 pp on temporal recall. MemGPT has strong historical-fact recovery versus lossy summaries under three backbones sharing one workload, with different evidence access and answer instructions.

The strongest answer to RQ3 is scope-specific. MemOS merits a HaluMem QA follow-up, SIRIN merits a prospective selective-answering study, and TRUSTMEM merits a consolidation study. None is a demonstrated general-purpose winner. The broad literature map explains metric and protocol heterogeneity, and the head-to-head panels make the exact local choices transparent. A pooled ranking would require aligned independent replications, explicit configuration matching, consistent denominators and paired uncertainty.

## Figures for the talk

- [HaluMem · strict QA hallucination rates](../figures/stage2e_halumem_head_to_head.png)
- [SIRIN · coverage versus served unfaithfulness](../figures/stage2c_sirin_coverage.png)
- [BioMem · updating and temporal QA front](../figures/stage2c_biomem_pareto.png)
- [RMM · matched retriever effects](../figures/matched_effect_sizes_example.png)
- [Evidence coverage by outcome type](../figures/stage2e_matched_evidence_coverage.png)

[Task-specific claims and original source locations](../results/final_claim_verification.csv) · [Final audited summary](final_cluster_b_summary.md)
