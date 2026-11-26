### IMAE (Kadotani et al.) — Learning from Hallucinations: Mitigating Hallucinations in LLMs via Internal Representation Intervention
- **Venue/Year:** IJCNLP-AACL 2025
- **Benchmarks:** TruthfulQA (MC1/MC2/MC3 evaluation); HaluEval (10k hallucinated QA pairs for training)
- **Baselines:** Llama2-7B-Chat baseline, ICD (anti-expert, upper bound), ITI, DoLa, CD
- **Key results:**
  - MC1: 40.02 (IMAE) vs. 36.96 (baseline) vs. 46.32 (ICD upper bound) on TruthfulQA (Llama2-7B-Chat)
  - MC2: 57.12 (IMAE) vs. 54.62 (baseline); MC3: 28.96 vs. 27.95
  - Llama3.1-8B-Instruct + IMAE: MC1 43.08 vs. 40.88 baseline; MC2 63.62 vs. 59.90
  - Llama3.2-3B-Instruct + IMAE: MC1 38.19 vs. 35.25 baseline
  - Efficiency: GPU memory 1.4x baseline (vs. 2.2x for ICD); latency 1.2x (vs. 1.9x for ICD)
- **Ablation highlight:** Removing Lanti, Lexpert, or Lgate each drops MC1 to near-baseline (~36–37); MLPanti saturates at intermediate size 4096.

### Lamba et al. — Hallucinations in LLMs: A Lifecycle-Based Survey of Causes, Detection, Mitigation, and Prevention
- **Venue/Year:** arXiv 2026 (Sharda University / UMBC)
- **Evaluation:** N/A — survey/position paper
- **Summary:** Proposes a lifecycle framework with 3 LLM pipeline stages (Data/Training/Inference) × 4 aspects (Cause/Detection/Mitigation/Prevention) = 13 analytical dimensions. PRISMA review of 30 papers from 157 candidates; benchmarks evaluated on a 15-criteria suitability matrix.

### Li et al. — Mitigating Hallucination in LLMs: A Capability-Oriented Survey on RAG, Reasoning, and Agentic Systems
- **Venue/Year:** ACM Computing Surveys 2025 (submitted; arXiv:2510.24476)
- **Evaluation:** N/A — survey/position paper
- **Summary:** Capability-enhancement perspective splitting hallucinations into knowledge-based vs. logic-based. Three mitigation pillars: (1) RAG (Pipeline-Level, Precise Retrieval, Broad Retrieval); (2) Reasoning (CoT, Tool-Augmented, Symbolic); (3) Agentic Systems (Reasoning-Augmented Retrieval, Multi-Agent, Iterative).

### Amber (Qin, Luo et al.) — Towards Adaptive Memory-Based Optimization for Enhanced Retrieval-Augmented Generation
- **Venue/Year:** arXiv 2025 (Sep 2025, v4)
- **Benchmarks:** SQuAD v1.1, Natural Questions, TriviaQA (single-hop); 2WikiMultiHopQA, HotpotQA (multi-hop); ASQA (long-form, 948 queries via ALCE)
- **Baselines:** NoR; Single-time RAG — Vanilla, Self-Refine, Self-Rerank, Chain-of-note; Adaptive RAG — ReAct, Self-RAG, FLARE, Adaptive-RAG, Adaptive-Note. Tested on Qwen2-7B, Llama3-8B, GPT-3.5.
- **Key results (Amber with Llama3-8B vs. strongest adaptive baseline):**
  - Natural Questions: acc 44.2 / F1 50.49 (Amber) vs. 40.0 / 45.38 (Adaptive-Note)
  - TriviaQA: acc 63.6 / F1 62.79 vs. 59.6 / 59.72 (Adaptive-Note)
  - 2WikiMQA: acc 43.8 / F1 43.5 vs. 38.2 / 42.8 (FLARE)
  - HotpotQA: acc 45.8 / F1 53.72 vs. 44.4 / 52.56 (Adaptive-RAG)
  - ASQA: str-em 44.7 / str-hit 18.8 vs. 42.1 / 15.8 (Adaptive-RAG)
  - SQuAD (Qwen2-7B): acc 47.8 / F1 49.84 vs. 34.4 / 39.05 (Chain-of-note)
  - Content-filter classifier: >90% accuracy on useful passages; excludes >40% of negative retrievals
- **Ablation highlight:** On 2WikiMQA (Llama3-8B) removing both content-filter levels drops F1 from 52.73 to 48.39; removing Agent-based Memory Updater drops to 41.63. Optimal at max_iter=3.

### DRAG (Hu et al.) — Removal of Hallucination on Hallucination: Debate-Augmented RAG
- **Venue/Year:** arXiv May 2025 (HK PolyU / Sichuan University)
- **Benchmarks:** NQ, TriviaQA, PopQA (open-domain QA); 2WikiMultihopQA, HotpotQA (multi-hop); StrategyQA (commonsense) — 500 examples each
- **Baselines:** Naive Gen, MAD (no retrieval); Naive RAG, IRCoT, Iter-RetGen, FLARE, Self-RAG, SuRe. Base LLM Llama-3.1-8B-Instruct; retriever E5-base-v2 on Dec 2018 Wikipedia.
- **Key results (EM / F1):**
  - 2WikiMultihopQA: EM 28.80 / F1 36.97 (DRAG) vs. Iter-RetGen 22.80 / 31.19 (+6 EM)
  - HotpotQA: EM 30.80 / F1 41.74 vs. Iter-RetGen 27.80 / 38.93 (+3 EM)
  - StrategyQA: EM 69.20 (DRAG) vs. MAD 66.20 (best baseline)
  - NQ: EM 36.80 / F1 50.38 (DRAG) vs. Iter-RetGen 40.80 / 52.31 (second-tier)
  - TriviaQA: EM 60.80 / F1 69.93 vs. Iter-RetGen 63.00 / 72.23
  - PopQA: EM 38.60 / F1 46.50 vs. SuRe 41.80 / 48.99
  - Queries where gold answer is missing from retrieval: ResDebate lifts Avg EM from 3.60→5.04 (NQ), 12.50→28.98 (TriviaQA), 7.10→19.23 (2Wiki), 9.32→17.36 (HotpotQA)
- **Ablation highlight:** Removing information asymmetry drops performance across all datasets; excessive debate rounds cause "problem drift" (TriviaQA EM 62.40 → 60.20 going from ResIter=1 to ResIter=2).
