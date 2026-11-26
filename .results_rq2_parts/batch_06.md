### Larimar-Scaling — Generation Constraint Scaling Can Mitigate Hallucination
- **Venue/Year:** arXiv 2407.16908, July 2024 (IBM Research, T. J. Watson Research Center)
- **Benchmarks:** WikiBio (238 GPT-3-generated Wikipedia-like biographies, hallucination benchmark from Manakul et al. 2023)
- **Baselines:** GRACE (Hartvigsen et al. 2022, model editing method on GPT2-XL); vanilla Larimar (no readout scaling); Larimar "ideal case" (z_write = z_readout)
- **Key results:**
  - RougeL: 0.72 ± 0.14 (Larimar with scaling s=4) vs. 0.49 ± 0.18 (GRACE) on WikiBio — 46.9% relative improvement over GRACE
  - RougeL: 0.39 ± 0.14 (base Larimar, s=1) vs. 0.49 ± 0.18 (GRACE) on WikiBio — unscaled Larimar underperforms
  - RougeL (ideal case, z_write=z_readout): 0.79 ± 0.13 on WikiBio (upper bound)
  - Jaccard similarity: 0.33 (Larimar base) to 0.69 (f=0.75 partial input) vs. 0.44 (GRACE) on WikiBio
  - Runtime: 3.1 sec/entry for Larimar vs. 162.5 sec/entry (37.8 sec amortized) for GRACE — 1-2 orders of magnitude speedup
  - Model sizes: Larimar 1.3B params vs. GRACE 1.56B params
- **Ablation highlight:** Scaling factor s sweep: RougeL peaks at s=4 (0.72), degrades to 0.59 at s=7.

### Kortukov-ParametricBias — Studying Large Language Model Behaviors Under Context-Memory Conflicts With Real Documents
- **Venue/Year:** COLM 2024 (arXiv 2404.16032v2, Oct 2024)
- **Note:** `2024_Kortukov_ContextMemoryConflicts.pdf` and `2024_Kortukov_Rubinstein_Context_Memory_Conflicts_Real_Documents_RAG.pdf` are the SAME paper (same arXiv ID, authors, title, content).
- **Benchmarks:** 6 open-book QA datasets from MrQA 2019 shared task: Natural Questions (NQ), SQuAD, NewsQA, TriviaQA, SearchQA, HotpotQA. Metric: BEM (BERT Matching, learned semantic equivalence).
- **Baselines:** Analysis/diagnostic study (no competing method). Models evaluated: Llama2-7B, Llama2-70B, Mistral-7B, Mixtral-8x7B, GPT-3.5-Turbo. Framed vs. prior synthetic-conflict studies (Longpre et al. 2021, Xie et al. 2024).
- **Key results:**
  - Retention of parametric answer P(R) in realistic conflicts: only 1.6% (Llama2-7B avg) and 2.2% (Mixtral-8x7B avg) across 6 datasets — contradicts prior "over-reliance" claims (up to 20%/75% in Longpre et al.)
  - Correct update rate P(U_c): 77.0% (Llama2-7B avg), 77.4% (Mixtral-8x7B avg) across 6 datasets
  - Parametric bias: presence of incorrect parametric answer in context increases failure rate by +4.0 to +10.7 pp (Llama2-7B) and +2.1 to +10.0 pp (Mixtral-8x7B); statistically significant (p<0.05) on all 6 datasets
  - Intervention — adding parametric answer to context as "Unrelated text": raises P(R) by +11.1 pp on NQ and +11.6 pp on SQuAD (Llama2-7B)
  - Masking parametric-answer tokens: drops P(R) by up to 1.6 pp (Llama2-7B), 0.4 pp (Mistral-7B), 1.8 pp (Mixtral-8x7B)
- **Ablation highlight:** Model scaling partially reduces parametric bias but doesn't eliminate it even for Llama2-70B/Mixtral-8x7B; task-specific finetuning also only partially mitigates.

### CEG — Citation-Enhanced Generation for LLM-based Chatbots
- **Venue/Year:** ACL 2024 (Proceedings of the 62nd Annual Meeting of the ACL, Volume 1: Long Papers, pp. 1451–1466)
- **Benchmarks:** WikiBio GPT-3 (238 biographies, 1,908 sentences / 1,392 nonfactual + 516 factual segments), FELM WorldKnowledge subset, HaluEval (2,000 QA samples), WikiRetr-GPT3 & WikiRetr-GPT4 (newly constructed, 1,000 rewritten passages each)
- **Baselines:** HalluDetector (Wang et al. 2023b), Focus (LLaMA-30B/65B variants), SelfCheckGPT (w/BERTScore, w/NLI, w/Prompt); FELM baselines: Vanilla, CoT, Link, Doc prompting with Vicuna-33B/ChatGPT/GPT-4; HaluEval baselines: Vanilla, CoT, Pre-RAG
- **Key results:**
  - WikiBio GPT-3: CEG (top-k=6) achieves 92.31 AUC-PR Nonfactual, 70.24 AUC-PR Factual, 77.59 Balanced Acc — best Balanced Acc and best AUC-PR Factual
  - FELM WorldKnowledge (GPT-4 backbone): CEG achieves 69.9 Balanced Acc vs. best baseline CoT 68.4; +11.4 pp vs. Vanilla (58.5); CEG Nonfact 54.4 / Factual 85.5
  - HaluEval QA (regeneration): CEG w/GPT-3.5-Turbo-Instruct achieves 69.45% accuracy vs. Vanilla 63.40%, w/CoT 68.55%, w/Pre-Retrieval 61.35% — +8.10% over pre-hoc retrieval
  - Retrieval: SimCSE BERT achieves Recall@10 of 76.8% on WikiRetr-GPT3 vs. 68% for All-mpnet-base-v2, 9.6% for Sentence BERT
- **Ablation highlight:** Removing Retrieval Augmentation drops GPT-4 Balanced Acc on FELM from 69.9 to 61.9 (−8.0 pp); k≈4-6 optimal.

### ContextFaithful-MemoryStrength — Investigating Context Faithfulness in Large Language Models: The Roles of Memory Strength and Evidence Style
- **Venue/Year:** arXiv 2409.10955v2 (uploaded Jul 2025; Iowa State University)
- **Benchmarks:** popQA (1,000 questions, entity-based long-tail QA), Natural Questions (NQ; 1,667 questions from Longpre et al. 2021 context-faithfulness test set)
- **Baselines:** Direct Evidence (1 sentence) baseline; compared against Direct Evidence (2-3 sentences, simple repetition), Direct + Paraphrase evidence, Indirect Evidence, Direct + Indirect combinations. LLMs tested: LLaMA2-7B, LLaMA2-70B, LLaMA3.2-3B, ChatGPT, GPT-4, Claude 3.5.
- **Key results:**
  - GPT-4 answers ~50% of NQ high-memory-strength questions using internal memory despite given conflicting evidence — contradicts prior claim that LLMs are >95% receptive to coherent counter-evidence
  - popQA Direct Evidence (1 sentence) MA ratio R_m (lower = more context-faithful): LLaMA2-7B 0.44%, LLaMA2-70B 0.44%, LLaMA3.2-3B 7.69%, ChatGPT 3.32%, GPT-4 13.29%, Claude3.5 0.65%
  - Paraphrasing cuts MA ratio by >50%: popQA Direct Evidence (3 sent.) vs. Direct+Paraphrase (3 sent.), LLaMA3.2-3B R_m 7.16 → 1.28; GPT-4 R_m 2.14 → 1.29
  - NQ Group 1 Direct+Paraphrase (3 sent.) vs. Direct (1 sent.): GPT-4 R_m 47.99 → 27.28; ChatGPT R_m 50.04 → 9.55
  - Clear positive correlation between memory strength and MA ratio across all 6 LLMs
- **Ablation highlight:** Simple repetition of direct evidence is NOT effective for older/smaller models, but paraphrasing is highly effective across all models; combining direct + indirect further enhances persuasiveness.
