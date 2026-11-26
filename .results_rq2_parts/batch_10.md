### CK-PLUG — Parameters vs. Context: Fine-Grained Control of Knowledge Reliance in Language Models
- **Venue/Year:** arXiv preprint, Mar 2025 (Bi et al.)
- **Benchmarks:** NQ (Natural Questions), ConFiQA, MQuAKE (counterfactual RAG); KILT suite — HotpotQA, FEVER, T-REx, ELI5, WoW (adaptive-enhancement eval); Wikipedia corpus with BGE-base-v1.5 retriever
- **Baselines:** Vanilla RAG per model (LLaMA2-7B-Chat, LLaMA3-8B-Instruct, Mistral-v0.3-7B, Qwen2.5-7B-Instruct); comparisons across alpha = 0.0, 0.5, 1.0
- **Key results:**
  - Memory Recall (MR) on NQ, LLaMA3-8B: adjustable 9.9% (alpha=0.0) to 71.9% (alpha=1.0) vs baseline 43.5%
  - MR on NQ, LLaMA2-7B: 12.3% (alpha=0) vs 71.5% (alpha=1.0) vs baseline 50.2%
  - MR on ConFiQA, LLaMA3-8B: 14.9% (alpha=0) vs 62.5% (alpha=1.0) vs baseline 29.2%
  - MR on MQuAKE, Qwen2.5-7B: 20.6% (alpha=0) vs 62.4% (alpha=1.0) vs baseline 28.8%
  - Adaptive mode, LLaMA3-8B KILT: NQ 46.5 (vs w/ RAG 45.2), HotpotQA 46.7 (vs 45.1), T-REx 52.3 (vs 51.5), FEVER 86.1 (vs 86.4)
- **Ablation highlight:** Removing Conflict Detection (ConD) causes sharp hit-rate drops under extreme alpha (LLaMA2-7B 30.7% at alpha=0 vs 74.8% with ConD).

### HaluMem — HaluMem: Evaluating Hallucinations in Memory Systems of Agents
- **Venue/Year:** arXiv preprint, Jan 2026 (Chen et al., MemTensor / China Telecom Research Institute)
- **Benchmarks:** HaluMem-Medium (~160k-token context/user, 30,073 turns, 14,948 memory points, 3,467 QA) and HaluMem-Long (~1M-token context/user, 53,516 turns) — both newly introduced
- **Baselines (evaluated memory systems):** Mem0, Mem0-Graph, Memobase, MemOS, Supermemory, Zep (GPT-4o as answer generator)
- **Key results:**
  - Memory Extraction F1 (Medium): Mem0 57.85%, Mem0-Graph 57.31%, MemOS 37.48%, Memobase 25.13%, Supermemory 56.90%
  - Memory Extraction Accuracy (Medium): Memobase 80.78% (best), Mem0 60.86%, MemOS 59.55%, Supermemory 51.77%
  - Memory Updating Correct Rate (Medium): MemOS 62.11% (best), Memobase 5.20%, Supermemory 16.37%
  - QA Accuracy (Medium): MemOS 67.23% (best), Supermemory 54.07%, Memobase 35.33%, Mem0 28.11%
  - QA Accuracy on Long: MemOS 64.44% (best); Mem0 28.11%, Mem0-Graph 32.44%, Memobase 33.60% — most systems collapse
  - Typewise accuracy (Long): MemOS leads with Event 70.92% / Persona 68.35% / Relationship 71.68%
- **Ablation highlight:** All systems achieve hallucination rates below 2% on updating only because coverage of pre-update memories is poor (omission rates above 50%) — extraction-to-update linkage is the main bottleneck.

### Memory-as-a-Tool — Distilling Feedback into Memory-as-a-Tool
- **Venue/Year:** MemAgents Workshop, ICLR 2026 (Gallego, Komorebi AI Technologies)
- **Benchmarks:** Rubric Feedback Bench (new, 42 scenarios across 5 task categories: creative writing, analytical, behavioral, ethical reasoning, visual writing); long-horizon mixed-task experiment with H=12 tasks
- **Baselines:** Base model (zero-shot), Self-Critique (inference-time), Memory + Feedback (proposed)
- **Key results:**
  - Models: Claude Sonnet 4.5, GPT-5.1, Gemini 3 Pro
  - Continual learning (H=3): Memory+Feedback (Claude Sonnet 4.5) rises from ~0.6 to ~0.98 mean score by example 2
  - Long-horizon mixed-task (H=12, Claude Sonnet 4.5): Memory+Feedback 0.78 ± 0.10 vs baseline 0.52 ± 0.25
  - Cost-score Pareto (Claude Sonnet 4.5): Memory+Feedback ~$0.04/task (score ~0.78) vs Self-Critique ~$0.07/task (similar score); baseline ~$0.03 (score ~0.5)
  - Per-task jump after first feedback cycle: 0/10 -> 9.2/10 on a review task
- **Ablation highlight:** Agent accumulates 8 memory files across 12 heterogeneous tasks, showing cross-domain consolidation without interference.

### DMP — Decoding Memories: An Efficient Pipeline for Self-Consistency Hallucination Detection
- **Venue/Year:** arXiv preprint, Aug 2025 (Gao, Liu, Wang, Lu, Yin; NC State / Oak Ridge National Lab)
- **Benchmarks:** TriviaQA, NQ Open, SQuAD, HaluEval (400 test examples each); SciQ in appendix; models LLaMA2-7B-Chat and Mistral-7B-Instruct (plus LLaMA2-13B-Chat, Falcon-7B in appendix)
- **Baselines:** LN-Entropy, Lexical Similarity, Semantic Entropy, Semantic Entropy-B, SelfCheckGPT, EigenScore, EigenScore-B — each paired with +DMP
- **Key results:**
  - AUROC: Semantic Entropy on LLaMA2-7B TriviaQA 86.4 baseline vs 85.4 +DMP; Mistral-7B TriviaQA 84.6 vs 84.8 +DMP (max single-trial AUROC reduction 2.9%; mean reduction 0.5%)
  - Semantic Entropy LLaMA2-7B HaluEval: 77.9 vs 77.2 +DMP; SQuAD 82.5 vs 81.5 +DMP
  - Runtime (LLaMA2-7B TriviaQA): 1778s -> 627s (2.8× speedup)
  - Runtime (Mistral-7B TriviaQA): 1124s -> 442s (2.5×); SQuAD 1932s -> 1022s (1.9×); HaluEval 2148s -> 904s (2.4×)
  - Reuse ratio up to 66.8% (TriviaQA, LLaMA2-7B)
- **Ablation highlight:** On TriviaQA (LLaMA2-7B): Baseline AUROC 70.1 -> +Selective Inference 70.2 -> +Hard Decoding 67.7 (56.9% reuse) -> +Annealed Decoding 69.7 (66.8% reuse); annealing recovers AUROC lost from hard decoding.

### ParamMute — ParamMute: Suppressing Knowledge-Critical FFNs for Faithful Retrieval-Augmented Generation
- **Venue/Year:** NeurIPS 2025 (Huang et al., Northeastern University / Tsinghua / MSR Asia / CMU)
- **Benchmarks:** CoFaithfulQA (new, consistency-filtered from HotpotQA, NewsQA, NQ, SearchQA, SQuAD, TriviaQA); ConFiQA (QA, Multi-hop Reasoning, Multi-Conflicts subsets); FaithEval (OOD)
- **Baselines:** Vanilla-RAG, Attr_prompt, O&I_prompt, COIECD, SFT, KAFT, Context-DPO (C-DPO), DDR — on LLaMA3-8B-Instruct backbone
- **Key results:**
  - Headline: +6.17% average ConR on CoFaithfulQA and +54.63% on ConFiQA vs Vanilla-RAG
  - CoFaithfulQA HotpotQA: ParamMute ConR 71.06 / MemR 6.17 / MR 7.99 vs Vanilla-RAG 60.34 / 13.88 / 18.70
  - CoFaithfulQA SearchQA: ConR 78.76 / MemR 6.04 / MR 7.12 vs 66.76 / 10.55 / 13.64
  - CoFaithfulQA SQuAD: ConR 80.58 / MemR 4.04 / MR 4.78 vs 77.93 / 6.79 / 8.01
  - ConFiQA QA: ConR 81.20 / MemR 3.69 / MR 4.35 vs 26.24 / 38.51 / 59.47
  - ConFiQA Multi-Conflicts: ConR 65.20 / MemR 9.29 / MR 12.47 vs 4.49 / 13.53 / 75.09
- **Ablation highlight:** Suppressing FFNs beats MHA, parameter-level, or whole layers (FFN ConR 69.54 vs MHA 68.35, Layer 62.52); bottom-layer FFN suppression collapses ConR to 62.29 while UA-FFNs (mid-to-deep) stay at 69.54.
