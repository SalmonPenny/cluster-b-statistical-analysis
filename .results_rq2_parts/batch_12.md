### SAFE — SAFE: A Sparse Autoencoder-Based Framework for Robust Query Enrichment and Hallucination Mitigation in LLMs
- **Venue/Year:** arXiv 2503.03032 (March 2025)
- **Benchmarks:** TruthfulQA, BioASQ, WikiDoc
- **Baselines:** Vanilla Gemma2-9b, Vanilla Llama3-8b (base models without SAFE enrichment)
- **Key results:**
  - TruthfulQA accuracy (Llama3-8b): 31.64 -> 40.96 (+29.45% relative improvement)
  - BioASQ accuracy (Llama3-8b): 31.11 -> 34.17 (+9.84%)
  - WikiDoc accuracy (Llama3-8b): 41.41 -> 42.97 (+3.77%)
  - TruthfulQA accuracy (Gemma2-9b): 63.63 -> 65.40 (+2.80%)
  - BioASQ accuracy (Gemma2-9b): 41.77 -> 43.04 (+3.04%)
  - WikiDoc accuracy (Gemma2-9b): 38.34 -> 38.85 (+0.81%)
- **Ablation highlight:** Best hyperparameters are entropy threshold phi=0.6 and density delta=0.05; removing SAE feature selection substantially degrades performance.

### PGMR — Reducing Hallucinations in Language Model-based SPARQL Query Generation Using Post-Generation Memory Retrieval
- **Venue/Year:** arXiv 2502.13369 (Jan 2026)
- **Benchmarks:** LCQUAD 2.0 (original split), LCQUAD 2.0 (unknown URI split), QALD-10
- **Baselines:** Direct Generation (T5-Small FT, Llama 3.1 8B PEFT, GPT-4o 25-shot) and RAG variants of each
- **Key results:**
  - LCQUAD 2.0 (Llama 3.1 8B PGMR): F1 88.73, SQM 87.84%, URI Hallucination 0.0% (vs. Direct 89.84% hallucination, RAG 7.23%)
  - LCQUAD 2.0 unknown URI split (Llama 3.1 8B PGMR): F1 84.47, SQM 83.33%, URI Hallucination 0.0%
  - QALD-10 (Llama 3.1 8B PGMR): F1 39.41, SQM 25.63%, URI Hallucination 0.0%
  - Avg SQM gain over direct generation: ~61.35% on LCQUAD2 original; ~16.61% over RAG
  - Near-complete elimination of URI hallucinations (RAG avg 8.71% -> PGMR ~0%)
- **Ablation highlight:** Memory scaling to 9x original size yields only ~4% SQM drop (Llama 3.1 8B); confidence threshold ~0.85 optimally balances refusal accuracy and SQM.

### PORAG+ATLAS — Scaling Test-Time Inference with Policy-Optimized, Dynamic Retrieval-Augmented Generation via KV Caching and Decoding
- **Venue/Year:** arXiv 2504.01281 (May 2025) — preliminary preprint
- **Benchmarks:** HotpotQA, Gorilla (API-call generation), PubMedQA
- **Baselines:** RAG-base, PORAG-only, GRPO+ATLAS, PORAG+DRAGIN, RAG+ATLAS, RAFT+ATLAS
- **Key results:**
  - HotpotQA Joint EM/F1 (Qwen2.5-3B): 45.29 / 71.32 vs. RAG-base 34.88 / 49.10 (+10.41 EM / +22.22 F1)
  - HotpotQA Answer EM/F1: 65.37 / 78.40; Supporting Facts EM/F1: 60.21 / 82.01
  - Gorilla: 76.38% accuracy, 5.31% hallucination error, 4.98% wrong API error (vs. RAG-base 62.12% / 10.70% / 9.58%)
  - PubMedQA: 78.35% accuracy, 74.56% F1 vs. RAG-base 60.70% / 59.30% (+17.65 / +15.26)
- **Ablation highlight:** Optimal ATLAS params alpha0=0.8, tau_p=0.5; removing dual reward (PORAG-NF) drops HotpotQA Joint F1 71.32 -> 65.24; GRPO outperforms PPO variant.

### RMM — In Prospect and Retrospect: Reflective Memory Management for Long-term Personalized Dialogue Agents
- **Venue/Year:** ACL 2025 (Vol. 1: Long Papers, pp. 8416-8439)
- **Benchmarks:** MSC (Multi-Session Chat), LongMemEval
- **Baselines:** No History, Long Context, RAG (Contriever/Stella/GTE), MemoryBank, LD-Agent
- **Key results:**
  - MSC (RMM + GTE): METEOR 33.4%, BERT 57.1% vs. best RAG baseline 27.5% / 52.1%
  - LongMemEval (RMM + GTE): Recall@5 69.8%, Accuracy 70.4% vs. best RAG baseline 62.4% / 63.6%
  - Memory contributes to quality improvements in 100% of LongMemEval cases and 86% of MSC cases
  - Top-K=50, Top-M=10 further boosts LongMemEval Accuracy to 73.8% (GTE)
- **Ablation highlight:** Prospective Reflection alone (+PR) raises MSC METEOR 24.8 -> 28.6; adding reranker (+RR) brings full RMM to 30.8.

### OracleAgent Memory — Oracle Agent Memory as an Enterprise Memory Substrate for Long-Horizon AI Agents
- **Venue/Year:** arXiv 2607.13157 (July 2026) — Oracle technical report
- **Benchmarks:** LongMemEval (500 questions); ChromAtlas-ND scripted 80-turn conversation for token-cost analysis
- **Baselines:** Flat-history baseline (full verbatim transcript); published external baselines referenced qualitatively
- **Key results:**
  - LongMemEval overall accuracy: 93.8% (469/500) using gpt-5.5 + nomic-embed-v1.5 + DB HNSW, top-K=200
  - Category breakdown: Single-session assistant 100.0%, Temporal reasoning 96.2%, Knowledge update 94.9%, Single-session user 94.3%, Single-session preference 93.3%, Multi-session reasoning 88.0%
  - Token efficiency: ~1,300 input tokens per request at turn 80 vs. ~13,900 for flat-history (~10.7x fewer tokens)
  - Pairwise LLM-judge (gpt-5.4) on 80-turn conversation: Agent Memory wins 48 turns, flat history wins 13, 19 ties (~3.7x win ratio)
- **Ablation highlight:** Summarization-trigger sweep shows lowest token mean (121,268 tokens) at 10k-token trigger vs. 306,823 for flat-history.
