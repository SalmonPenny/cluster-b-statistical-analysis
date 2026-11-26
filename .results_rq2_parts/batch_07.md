### KELDaR — A Framework of Knowledge Graph-Enhanced Large Language Model Based on Question Decomposition and Atomic Retrieval
- **Venue/Year:** Findings of EMNLP 2024
- **Benchmarks:** WebQSP (WebQuestionsSP), CWQ (ComplexWebQuestions) — both KGQA over Freebase
- **Baselines:** Training-based: KV-Mem, GraftNet, PullNet, EmbedKGQA, TransferNet, NSM, KGT5, SR+NSM+E2E, TIARA, KD-CoT, UniKGQA, ReasoningLM, DecAF, RoG. Reasoning-based: StructGPT, KB-BINDER, ToG, IO, CoT, CoT+SC (all with GPT-3.5-turbo)
- **Key results (Exact Match %):**
  - 79.4 on WebQSP, 53.6 on CWQ (KELDaR-rel* — best configuration, with golden topics)
  - 75.5 on WebQSP, 41.9 on CWQ (KELDaR without golden topics)
  - +14.6 EM on WebQSP and +19.2 EM on CWQ vs. IO prompting baseline
  - +5.0 EM on WebQSP and +12.0 EM on CWQ vs. previous best reasoning-based method
  - Second-best on CWQ behind only RoG* (69.0); competitive with most training-based baselines without any fine-tuning
- **Ablation highlight:** Relation-based extraction strategy (KELDaR-rel*) outperforms triple/quadruple-based (KELDaR*) on CWQ (53.6 vs 50.7).

### RAG-DDR — RAG-DDR: Optimizing Retrieval-Augmented Generation Using Differentiable Data Rewards
- **Venue/Year:** ICLR 2025
- **Note:** `2024_Li_Mei_RAG_DDR_Differentiable_Data_Rewards_RAG.pdf` and `2024_Li_RAGDDR.pdf` are the SAME paper (arXiv:2410.13509v2 — same authors, abstract, tables).
- **Benchmarks:** NQ, TriviaQA, MARCO QA (open-domain QA), HotpotQA (multi-hop), T-REx (slot filling), Wizard of Wikipedia/WoW (dialogue)
- **Baselines:** LLM w/o RAG, Vanilla RAG, REPLUG, Self-RAG, RA-DIT (with MiniCPM-2.4B and Llama3-8B backbones)
- **Key results (Llama3-8B, RAG-DDR w/ 2-Round):**
  - NQ: 52.1 Acc (vs Vanilla RAG 46.2, RA-DIT 46.2)
  - TriviaQA: 89.6 (vs Vanilla RAG 84.0)
  - MARCO QA: 27.3 Rouge-L (vs Vanilla RAG 20.6)
  - HotpotQA: 39.0 Acc (vs Vanilla RAG 30.1, RA-DIT 34.9)
  - T-REx: 40.6 (RA-DIT 41.7 — second-best here)
  - WoW: 16.8 F1 (vs Vanilla RAG 12.5)
  - ~7% average improvement over Vanilla RAG
- **Ablation highlight:** Training only the generation module (V_Gen) drives most of the gains; training only knowledge refinement (V_KR) gives only marginal improvements.

### Self-Familiarity — Zero-Resource Hallucination Prevention for Large Language Models
- **Venue/Year:** Findings of EMNLP 2024
- **Benchmarks:** Concept-7 (newly proposed: 192 basic concepts, 451 basic instructions, 180 test concepts — 106 real + 74 fictional, 515 test instructions from seven expert domains)
- **Baselines:** Greedy-Perplexity, Greedy-AvgLogP, Greedy-MinLogP, Sample-BERTScore, Sample-SentenceScore, Self-Detection, Forward-Inference, Forward-Self
- **Key results (Self-Familiarity best AUC across all 5 LLMs):**
  - Vicuna-13b-v1.3: AUC 0.927, ACC 0.868, F1 0.854 (best baseline Sample-BERTScore AUC 0.872)
  - Llama-2-13b-chat: AUC 0.909, ACC 0.835, F1 0.812 (best baseline Greedy-Perplexity AUC 0.885)
  - Falcon-7b-instruct: AUC 0.926, ACC 0.882, F1 0.822 (best baseline AUC 0.697)
  - mpt-7b-instruct: AUC 0.921, ACC 0.850, F1 0.817
  - Alpaca-7b: AUC 0.918, ACC 0.866, F1 0.848
  - Human-annotated validation (Vicuna-13b-v1.3): AUC 0.892, ACC 0.827, F1 0.813 (best)
- **Ablation highlight:** All three concept-processing steps (Grouping, Filtering, Ranking) contribute; weighted averaging aggregation beats Minimal-Only (F1 0.767) and Most-Infrequent-Only (F1 0.858).

### RAGTruth — RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models
- **Venue/Year:** ACL 2024 (Volume 1: Long Papers)
- **Benchmarks:** RAGTruth corpus (newly proposed: ~18,000 annotated responses across QA (MS MARCO), Data-to-text Writing (Yelp Open Dataset), News Summarization (CNN/DM + recent news); 2,965 instances, 17,790 responses, word-level hallucination annotations; responses from 6 LLMs: GPT-4-0613, GPT-3.5-turbo-0613, Mistral-7B-Instruct, Llama-2-7B/13B/70B-chat)
- **Baselines (detection methods):** Prompt_GPT-3.5-turbo, Prompt_GPT-4-turbo, SelfCheckGPT_GPT-3.5-turbo, LMvLM_GPT-4-turbo, Finetuned Llama-2-13B (proposed)
- **Key results:**
  - Response-level detection overall F1: Finetuned Llama-2-13B 78.7 vs. GPT-4-turbo Prompt 63.4, SelfCheckGPT 58.8, GPT-3.5-turbo Prompt 52.9, LMvLM 36.2
  - Finetuned Llama-2-13B per-task F1: QA 68.2, Data-to-text 88.1, Summarization 59.1 (all best)
  - Span-level overall F1: Finetuned Llama-2-13B 52.7 vs. GPT-4-turbo Prompt 28.3, GPT-3.5-turbo Prompt 12.8
  - Hallucination suppression (sampling best-of-two using detector): -42.9% hallucination for GPT-3.5-Turbo, -51.0% for GPT-4; -21.6% / -63.2% for Llama-2-7B-chat / Mistral-7B
  - Hallucination density per 100 words: GPT-4-0613 0.08 (lowest), GPT-3.5-turbo 0.12, Llama-2-70B-chat (4-bit) 0.26, Llama-2-13B-chat 0.48, Mistral-7B-Instruct 0.86, Llama-2-7B-chat 1.27 (highest)
- **Ablation highlight:** Fine-tuned 13B open-source model beats prompt-based GPT-4-turbo for hallucination detection (78.7 vs 63.4 F1).
