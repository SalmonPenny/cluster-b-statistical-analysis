### RC-RAG (Chen 2024) — Controlling Risk of Retrieval-augmented Generation: A Counterfactual Prompting Framework
- **Venue/Year:** Findings of EMNLP 2024
- **Benchmarks:** RC-TQ (built from TriviaQA, 7,785 questions) and RC-NQ (built from Natural Questions, 3,610 questions); evaluated with four risk-aware metrics: risk, carefulness, alignment, coverage
- **Baselines:** If-or-Else (IoE) prompting, Calibration-based framework, Priori judgment framework; backbones Mistral-7B and ChatGPT (gpt-3.5-turbo-0301); dense + sparse retrievers
- **Key results:**
  - On RC-TQ with Mistral: risk 19.00 (vs. 24.88 IoE / 24.79 Calibration / 21.95 Priori); carefulness 52.87 (vs. 20.97/20.92/33.87)
  - On RC-NQ with Mistral: risk 38.22 (vs. 45.59/45.65/42.61); carefulness 52.98; alignment 63.60 (best)
  - On RC-TQ with ChatGPT: risk 14.94 (lowest), carefulness 65.37 (best)
  - On RC-NQ with ChatGPT: risk 35.22 (lowest), carefulness 62.86 (best)
  - Average across 4 settings: -2.88% risk, +14.77% carefulness vs. baselines
- **Ablation highlight:** CF-quality prompt alone gives lowest risk (10.48) but lower coverage (52.5); CF-usage alone gives higher coverage (71.0) but higher risk (18.31); full fusion balances the two (risk 13.56, coverage 59.0).

### Lookback Lens (Chuang 2024) — Lookback Lens: Detecting and Mitigating Contextual Hallucinations in Large Language Models Using Only Attention Maps
- **Venue/Year:** EMNLP 2024
- **Benchmarks:** CNN/DM (summarization, 1,000 examples), Natural Questions (QA, 2,655 examples), XSum (mitigation), MT-Bench (multi-turn)
- **Baselines:** Text-based NLI (DeBERTa-v3 fine-tuned; SoTA Vectara NLI), Hidden-states classifiers (layers 24/28/32 of LLaMA-2-7B-Chat), Greedy decoding
- **Key results:**
  - Detection AUROC (predefined span, source→target transfer): Lookback Lens 91.2 (QA→Sum) / 88.8 (Sum→QA) vs. NLI 55.1 / 71.0 and hidden-state (28th layer) 91.4 / 83.3
  - XSum mitigation: 58.6 correctness vs. greedy 49.0 (+9.6 pts); hallucinated examples 510 → 414 (18.8% reduction)
  - NQ mitigation: 74.2 vs. greedy 71.2 (+3%)
  - MT-Bench (hallu.): 6.27 vs. greedy 6.08
  - Cross-model transfer (7B → 13B) on XSum: 56.1 vs. greedy 52.9
- **Ablation highlight:** Lookback Lens trained on only 1k examples matches SoTA NLI trained on 731k; top-100 attention heads largely recover full-model performance.

### GraphRAG (Edge 2024) — From Local to Global: A GraphRAG Approach to Query-Focused Summarization
- **Venue/Year:** arXiv preprint 2024 (Microsoft Research; v2 Feb 2025)
- **Benchmarks:** Podcast transcripts (~1M tokens, 1,669 chunks) and News articles (~1.7M tokens, 3,197 chunks); 125 LLM-generated global sensemaking questions per dataset; Claimify-based claim extraction (47,075 unique claims)
- **Baselines:** Vector/semantic-search RAG (SS), Text-summarization map-reduce over source texts (TS); GraphRAG at four community levels C0 (root) / C1 / C2 / C3 (leaf); judge = GPT-4
- **Key results (head-to-head win rates vs. vector RAG SS):**
  - Podcast comprehensiveness: C3 79% / C2 78% / C1 75% / C0 72% (p<.001)
  - Podcast diversity: C3 81% / C2 81% / C1 75% / C0 77% (p<.001)
  - News comprehensiveness: 72–83% win (p<.001); News diversity: 62–71% win (p<.01)
  - Token efficiency: C0 uses 26,657 tokens vs. TS 1,014,611 (97% fewer); C3 uses 26–33% fewer tokens than TS
- **Ablation highlight:** Intermediate-level (C2 podcast) and low-level (C3 news) community summaries win over source-text summarization at 57% (p=.036) and 60% (p<.001); root-level C0 retains large advantage over vector RAG at 9–43× fewer tokens per query.

### RefChecker (Hu 2024) — Knowledge-Centric Hallucination Detection
- **Venue/Year:** EMNLP 2024
- **Benchmarks:** KnowHalBench (300 examples across 3 context settings — Zero Context/NQ, Noisy Context/MS MARCO, Accurate Context/databricks-dolly-15k); 2,100 responses from 7 LLMs with 11k human-annotated claim-triplets (95% IAA); also the SelfCheckGPT dataset
- **Baselines:** SelfCheckGPT, FActScore, FacTool; checker baselines RoBERTa-NLI, AlignScore, GPT-4
- **Key results:**
  - SelfCheckGPT dataset: Mistral-SFT+GPT-4 Pearson 80.98 / Spearman 83.92 vs. SelfCheckGPT 78.32 / 78.30
  - KnowHalBench (avg Pearson r / Spearman ρ): GPT-4+GPT-4 RefChecker 83.95 / 82.35 vs. best prior FacTool 46.35 / 38.69 — 18.2 to 27.2 pt improvement
  - Granularity: triplet-level checking +10 pts macro-F1 over response-level, +5 over sentence-level
  - Mistral-SFT extractor: P 90.5 / R 84.8 / F1 86.4 (vs. GPT-4 92.4/88.6/89.3) at ~5× faster inference
  - Best Mistral-based checker (RepC-LE-nn): 81.27 accuracy / 60.80 macro-F1 average (vs. GPT-4 74.77 / 59.80)
- **Ablation highlight:** Claim-triplet granularity outperforms response/sentence/sub-sentence by 4–9 pts macro-F1.

### TC-RAG (Jiang 2024) — TC-RAG: Turing-Complete RAG's Case Study on Medical LLM Systems
- **Venue/Year:** arXiv preprint 2024 (v3 Sep 2026)
- **Benchmarks:** MMCU-Medical, CMB-Exam, CMB-Clin; metrics EM (multiple-choice medical Q), ROUGE-R, BLEU-1, BLEU-4 for open-domain Q&A
- **Baselines:** 12 baselines in 4 categories — Base + CoT (no RAG); Naive RAG (SR-RAG, FL-RAG, FS-RAG); Advanced RAG (CoK, SuRe, HyKGE); Adaptive RAG (ReACT, Self-RAG, FLARE, DRAGIN); backbones Qwen-32B and Pretrained-Medical Qwen-32B
- **Key results (Pretrained Qwen-32B):**
  - TC-RAG-uct: CMB EM 87.95, MMCU EM 93.15, CMB-Clin BLEU-1 25.89 / BLEU-4 57.29 / ROUGE 56.59
  - TC-RAG-cppl: CMB EM 87.33, MMCU EM 92.80, CMB-Clin BLEU-1 24.65 / BLEU-4 56.94 / ROUGE 57.46
  - Best Adaptive RAG baseline (FLARE): CMB EM 85.14, MMCU EM 87.37
  - Avg accuracy gain of up to 7.20% over baselines; EM +2.60–5.62%, BLEU-4 +8.23–13.72%
  - Efficiency: avg time 50.91s (vs. DRAGIN 167.95s, Self-RAG 507.98s), fewer interactions (4.78) and retrievals (5.87)
- **Ablation highlight:** Removing the State Monitor causes the largest drop (CMB EM 83.75 / MMCU EM 88.79 on Qwen-32B).
