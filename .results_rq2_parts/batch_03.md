### LLM-Augmenter (Peng 2023) — Check Your Facts and Try Again: Improving Large Language Models with External Knowledge and Automated Feedback
- **Venue/Year:** arXiv 2023 (Microsoft Research)
- **Benchmarks:** DSTC7 Track 2 (News Chat), DSTC11 Track 5 (Customer Service), OTT-QA (Wiki QA, open-domain multi-hop)
- **Baselines:** Vanilla ChatGPT (closed-book), ChatGPT + BM25 retrieval without feedback, ChatGPT + golden knowledge without feedback
- **Key results:**
  - News Chat (DSTC7) KF1: 36.41 (LLM-Augmenter w/ BM25 + Feedback) vs. 26.71 (ChatGPT); with golden knowledge, KF1 60.76 vs. 57.44 without feedback
  - Customer Service (DSTC11) KF1: 37.41 (LLM-Augmenter w/ BM25 + Feedback) vs. 31.33 (ChatGPT); BLEU 3.86, chrF 30.90, METEOR 14.74 vs. ChatGPT 4.70/27.14/12.83
  - KF1 gain from Knowledge Consolidator alone: ~+10 (News Chat) and ~+6 (Customer Service) over ChatGPT
  - Wiki QA (OTT-QA): absolute +10 F1 over closed-book ChatGPT
  - Human eval (Customer Service): Usefulness 45.07 vs. 34.07; Humanness 35.22 vs. 30.92 (p<0.05)
- **Ablation highlight:** Feedback adds ~3.3 KF1 (News Chat) and ~7.2 KF1 (Customer Service) on top of golden knowledge.

### CoALA (Sumers 2023) — Cognitive Architectures for Language Agents
- **Venue/Year:** TMLR 02/2024 (arXiv Sep 2023)
- **Evaluation:** N/A — position/conceptual framework paper
- **Summary:** Proposes CoALA, a framework drawing on cognitive-science architectures (Soar-style) to organize LLM agents along memory modules (working, episodic, semantic, procedural), action space (internal reasoning/retrieval/learning; external grounding), and a decision cycle. Used retrospectively to survey existing agents and prospectively to identify design gaps.

### LongMem (Wang & Dong 2023) — Augmenting Language Models with Long-Term Memory
- **Venue/Year:** NeurIPS 2023 (arXiv Jun 2023)
- **Benchmarks:** PG-22 (5 length splits 5K–1M tokens), ArXiv subset of the Pile, ChapterBreak AO3 (zero-shot suffix ID), SST-2, MR, Subj, SST-5, MPQA (in-context NLU), SQuAD (3-shot open-ended QA)
- **Baselines:** GPT-2* (407M), Memorizing Transformer (MemTRM), GPT-2-XL, GPT-3 (175B), LocalTRM, RoutingTRM, BigBird
- **Key results:**
  - PG-22 perplexity: LongMem 21.29 / 23.01 / 22.55 / 23.35 / 16.71 (5 splits) vs. GPT-2* 22.78/24.39/24.12/24.97/18.07 and MemTRM 21.77/23.56/23.23/24.16/17.39
  - ArXiv perplexity: 10.05 vs. 11.05 (GPT-2*) and 10.81 (MemTRM)
  - ChapterBreak AO3 accuracy: 37.7%/39.4%/40.5% (ctx 4K/6K/8K) vs. 28.3%/28.7%/28.7% (MemTRM), 28% (GPT-3 175B)
  - 20-shot NLU average: 66.7 vs. 58.7 (GPT-2*) and 58.6 (MemTRM), +8.0 avg
  - SQuAD 3-shot: EM 26.77 / F1 35.70 vs. 22.28 / 30.78 (GPT-2*), +4.5 EM
- **Ablation highlight:** Chunk-size csz=2 best for fine-grained NLU; memory size should match doc length (msz=16K optimal for 8K–50K books).

### LLM Agent Survey (Wang 2023) — A Survey on Large Language Model based Autonomous Agents
- **Venue/Year:** Frontiers of Computer Science 2025 (arXiv Aug 2023, v7 Mar 2025)
- **Evaluation:** N/A — survey paper
- **Summary:** Reviews 100+ LLM agent systems with a unified construction framework (profiling, memory, planning, action modules), applications (social science, natural science, engineering), and evaluation strategies (subjective/objective). Memory sub-taxonomy covers unified vs. hybrid structures; language/embedding/database/list formats; reading/writing/reflection operations.

### Knowledge Conflicts (Xie 2023) — Adaptive Chameleon or Stubborn Sloth: Revealing the Behavior of Large Language Models in Knowledge Conflicts
- **Venue/Year:** ICLR 2024 (arXiv May 2023)
- **Benchmarks:** PopQA (entity-centric Wikidata QA), StrategyQA (multi-step reasoning). 5-step framework: elicitation, counter-memory construction, NLI entailment check, answer consistency, evidence preference.
- **Baselines / models evaluated:** ChatGPT, GPT-4, PaLM2, Qwen-7B, Llama2-7B, Llama2-70B, Vicuna-7B, Vicuna-33B. Counter-memory method comparison: entity-substitution (prior) vs. LLM-generated coherent counter-memory (proposed).
- **Key results:**
  - Closed-book PopQA correct: GPT-4 50.8%, ChatGPT 44.6%, Llama2-70B 43.0%, PaLM2 32.9%, Llama2-7B 24.1%; StrategyQA: GPT-4 77.3%, PaLM2 67.9%, ChatGPT 67.4%
  - Single-source receptiveness: with generation-based counter-memory, LLMs flip to counter-answer far more than with entity substitution (e.g., Llama2-7B ~90%+ Ctr-Ans on Gen vs. very low on Subs)
  - Multi-source confirmation bias (memorization ratio on PopQA at 1/2:1/2 evidence): ChatGPT 43.0, GPT-4 65.4, PaLM2 56.8, Llama2-7B 58.4, Vicuna-33B 51.7
  - GPT-4 memorization ratio ~80% on most-popular entities (strong popularity-driven confirmation bias)
  - Order sensitivity: most models show >5% swing in memorization ratio by evidence order; PaLM2 and Llama2-7B swing >30%
- **Ablation highlight:** Replacing entity-substitution counter-memory with LLM-generated coherent counter-memory flips the "stubborn LLM" finding — in single-source settings LLMs become highly receptive.
