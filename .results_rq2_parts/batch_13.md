### SIRIN — SIRIN: A Unified Toolkit for Detecting Contextual Hallucinations in Retrieval-Augmented and Memory-Grounded LLM Systems
- **Venue/Year:** arXiv preprint, Jul 2026 (Sber AI Lab)
- **Benchmarks:** RAGTruth (QA, Summarization, Data-to-Text), SQuAD 2.0, PsiloQA (English span-level), LongMemEval (used with SimpleMem / Mem0 / LightMem memory systems), Mu-SHROOM (for UI gallery)
- **Baselines:** LM-Polygraph, RAGAS, DeepEval, UpTrain, TruLens, LettuceDetect; detector-level: ModernBERT-large, DeBERTa-v3-large, Qwen3-4B (zero-shot and LoRA), GPT-5.4-mini, MeanTokenEntropy, RAUQ, Focus, Lookback Lens / attention-pooling probes, CatBoost probes
- **Key results:**
  - RAGTruth QA: Qwen3-4B LoRA judge 93.5 AUROC / 71.4 F1 (best); attention-pool probe 86.9 AUROC / 60.6 F1
  - RAGTruth Summary: Qwen3-4B LoRA judge 91.8 AUROC / 71.6 F1
  - RAGTruth Data-to-Text: Qwen3-4B LoRA judge 93.4 AUROC / 91.0 F1
  - SQuAD 2.0: Qwen3-4B judge 87.0 AUROC / 70.2 F1; query answerability 95.7 AUROC / 89.2 F1
  - PsiloQA span-level: attention-pool probe 76.0 AUROC (best); Qwen3-4B LoRA 74.8 F1 / 69.3 IoU
  - LongMemEval + SimpleMem: served accuracy 62.4% baseline to 79.3% (SIRIN Judge + both gates); strict unfaithfulness 20.2% to 9.8%
  - Mem0: 37.8% to 51.0% (+13.2 pts); LightMem: 50.2% to 64.5% (+14.3 pts)
- **Ablation highlight:** Combined UE fused score adds only +1.6 AUROC over the best single uncertainty estimator on SQuAD 2.0 (69.0 vs. 67.4).

### MemBook — MemBook: A Hierarchical Reasoning-based Memory Framework for Hallucination-Resistant LLM Agents
- **Venue/Year:** Findings of ACL: EMNLP 2026
- **Benchmarks:** HaluMem-Medium, HaluMem-Long, LongMemEval
- **Baselines:** Mem0, Mem0-Graph, A-Mem, Supermemory, Memobase, GAM; plus RAG, LangMem, MemGPT on LongMemEval
- **Key results:**
  - HaluMem-Medium: Extraction F1 79.21% (best), QA Acc 67.82%, Halluc 12.78%, Omission 19.39% (Mem0 QA 53.02%, A-Mem 55.31%)
  - HaluMem-Long: Extraction F1 79.69% (vs. Mem0's 6.22% collapse), QA Acc 68.37%, Halluc 12.84%
  - LongMemEval (GPT-4o-mini): Overall 69.4% (vs. Supermemory 58.4%, MemGPT 55.4%, A-Mem 53.8%); Temporal 59.4%, Multi-Session 57.9%, Single-User 94.3%
  - LongMemEval (Qwen3-30B-A3B): Overall 73.2% (vs. A-Mem 65.2%, Mem0 39.5%)
  - Typewise HaluMem-Long: Event 55.85% / Persona 54.83% / Relationship 53.74% (baselines mostly single digits)
- **Ablation highlight:** Removing the Pending Filter drops HaluMem-Long extraction F1 from 79.69% to 31.24%.

### HaluMem (Chen Niu 2026) — HaluMem: Evaluating Hallucinations in Memory Systems of Agents
- **Venue/Year:** arXiv preprint, Jan 2026 (China Telecom Research Institute / MemTensor)
- **Benchmarks:** Introduces HaluMem-Medium (~160K-token avg context) and HaluMem-Long (~1M-token avg context); 15K memory points, 3,467 QA pairs
- **Baselines (systems evaluated):** Mem0, Mem0-Graph, Memobase, MemOS, Supermemory, Zep
- **Key results (Medium):**
  - Memory Extraction F1: MemOS 62.11% (best), Mem0 57.85%, Supermemory 56.90%; all extraction Accuracy <62%
  - Memory Updating Accuracy: MemOS 65.25% (best); all systems hallucinate <2% but omission rates mostly >50%
  - QA Accuracy: MemOS 67.23% (best), Mem0 53.02%, Supermemory 54.07%
- **Key results (Long):**
  - Extraction F1 collapses for most: Mem0 6.22%, Mem0-Graph 4.36%, Memobase 11.55%; MemOS retains 82.11%, Supermemory 65.54%
  - QA Accuracy: MemOS 64.44%, Supermemory 53.77%; Mem0 drops to 28.11%
  - Typewise (Long) Persona accuracy: MemOS 68.35% vs. Mem0 3.01%
- **Ablation highlight:** N/A — benchmark paper; headline finding is that extraction-stage hallucinations propagate into updating and QA.

### TeleMem — TeleMem: Building Long-Term and Multimodal Memory for Agentic AI
- **Venue/Year:** arXiv preprint, Jan 2026 (TeleAI, China Telecom)
- **Benchmarks:** ZH-4O (Chinese role-playing, 28 sessions avg 600 turns, 1,068 multiple-choice questions), LoCoMo (English, 10 sessions, 1,540 QA pairs; adversarial subset excluded)
- **Baselines:** RAG, Long Context LLM, Mem0, A-Mem, Memobase, MOOM
- **Key results:**
  - ZH-4O QA Accuracy: TeleMem 86.33% (best), Long Context LLM 84.92%, Memobase 76.78%, A-Mem 73.78%, MOOM 72.60%, Mem0 70.20%, RAG 62.45% (+19 pts over Mem0)
  - LoCoMo Overall: Long Context LLM 70.71% (best), TeleMem 61.49%, Memobase 57.59%, Mem0 52.01%, A-Mem 48.57%, RAG 39.03%
  - LoCoMo Temporal: TeleMem 78.47% (best, +19.5 pts over Memobase 58.97%)
  - Efficiency: 43% token reduction and 2.1x speedup vs. Mem0 baseline
- **Ablation highlight:** Read-write scaling law — scaling the reader LLM yields larger gains than scaling the writer; best 32B-write x 14B-read combo reaches 87.55% QA Acc on ZH-4O.

### Synthius-Mem — Synthius-Mem: Brain-Inspired Hallucination-Resistant Persona Memory Achieving 94.4% Memory Accuracy and 99.6% Adversarial Robustness on LoCoMo
- **Venue/Year:** Synthius.ai technical report, April 2026
- **Benchmarks:** LoCoMo (ACL 2024; 10 conversations, 20 participants, 1,813 questions)
- **Baselines:** Published memory systems on LoCoMo (MemMachine, ENGRAM, TiMem, MemOS, Mem0, Mem0-Graph, MemoryOS, MemPalace, LangMem, ChatGPT Memory, A-MEM); controlled baselines (Full Context, Sliding Window, Summarization, Embedding RAG) all judged by GPT-4.1-mini
- **Key results:**
  - Overall LoCoMo accuracy: Synthius-Mem 94.37% (vs. MemMachine 91.69%, Human 87.9 F1, ENGRAM 77.55%, TiMem 75.30%, MemOS 69.24%, Mem0 66.9%)
  - Per-category vs. best competitor: Single-hop 96.73% vs. 94.65%; Multi-hop 94.34% vs. 87.59%; Temporal 89.32% vs. 77.63% (TiMem); Open-domain 77.33% vs. 72.92% (ENGRAM); Adversarial 99.55%
  - Knowledge-type: Adversarial 99.55% (442 false-premise questions), Core Memory Fact 98.64%, Temporal Precision 94.40%, Open Inference 78.26%, Peripheral Detail 57.66%
  - Controlled baselines (same judge): Synthius-Mem 94.37% vs. Full Context 85.46%, Embedding RAG 57.74%, Sliding Window 31.26%, Summarization 27.86%
  - Efficiency: ~5x fewer tokens than full-context replay at N=500 messages; 21.79 ms mean retrieval latency
- **Ablation highlight:** vs. Embedding RAG, structured temporal metadata yields a +67.4 pp gap on temporal questions (94.2% vs. 26.8%).
