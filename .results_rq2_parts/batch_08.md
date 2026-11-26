### Rowen — Rowen: Adaptive Retrieval-Augmented Generation for Hallucination Mitigation in LLMs
- **Venue/Year:** SIGIR-AP 2025 (arXiv Feb 2024, v3 Oct 2025)
- **Benchmarks:** TruthfulQA (generation task), StrategyQA (500 sampled multi-step yes/no reasoning)
- **Baselines:** Vanilla ChatGPT (gpt-3.5-turbo); self-improvement methods (CoVe, Multi-agent Debate, Self-Reflection); retrieval-augmented methods (Factool, Detect-and-Mitigate); adaptive retrieval methods (FLARE, Adaptive-Retrieval, Self-RAG, Adaptive-RAG, LUQ)
- **Key results:**
  - GPT-Judge: 59.34 on TruthfulQA (Rowen-Hybrid) vs. 55.08 LUQ (prior SOTA) and 47.92 vanilla ChatGPT (+16.74 over vanilla; +4.26 over LUQ)
  - BLEU: 15.27 on TruthfulQA (Rowen-Hybrid) vs. 10.17 vanilla ChatGPT
  - Rouge-L: 31.15 on TruthfulQA (Rowen-Hybrid) vs. 31.31 vanilla ChatGPT
  - Accuracy: 75.60 on StrategyQA (Rowen-Hybrid) vs. 71.00 LUQ and 61.40 vanilla ChatGPT (+14.20)
- **Ablation highlight:** Rowen-Hybrid (cross-language + cross-model consistency) outperforms Rowen-CL alone (57.39 GPT-Judge) and Rowen-CM alone (56.29 GPT-Judge).

### Sahoo Survey — A Comprehensive Survey of Hallucination in Large Language, Image, Video and Audio Foundation Models
- **Venue/Year:** Findings of EMNLP 2024
- **Evaluation:** N/A — survey/position paper
- **Summary:** Holistic multimodal survey of hallucination detection and mitigation across language, image, video, and audio foundation models. Introduces a 4-type hallucination taxonomy (contextual disconnection, semantic distortion, content hallucination, factual inaccuracy) and a technique taxonomy covering detection (automatic evaluation, inference classifier, self-evaluation, evidence retrieval) and mitigation (data augmentation, CoT enhancement, alignment/fine-tuning, self-verification, prompt engineering) per modality.

### Tao WikiAtomic — When Context Leads but Parametric Memory Follows in Large Language Models
- **Venue/Year:** EMNLP 2024
- **Benchmarks:** WikiAtomic (new dataset: 200 Wikipedia articles, 4,000 topic-context instances, k=2–50 atomic sentences); FActScore; INFUSE NLI entailment framework
- **Baselines:** Nine LLMs compared against each other — GPT-4o, Claude 3 Opus/Sonnet/Haiku, Llama 3 70B/8B, Mixtral 8x22B, Mistral 7B, Phi-3 (analysis paper, not a method proposal)
- **Key results:**
  - Contextual/parametric knowledge ratio converges to ~67/33 across all models at k=50 (overall ~70% contextual, ~30% parametric)
  - At k=50, per-model contextual/parametric: GPT-4o 0.67/0.33; Claude 3 Opus 0.72/0.28; Llama 3 70B 0.72/0.28; Phi-3 inverted at 0.49/0.51
  - FActScore rises from ~80 (small context) to 95+ for larger models (GPT-4o, Claude Opus/Sonnet/Haiku, Llama 3 70B, Mixtral 8x22B) as context grows to k=50
  - Context-recall quartile (GPT-4o): first-quartile ~85% at k=10 vs. ~70% at k=50; fourth-quartile drops ~85%→~60%, showing selective attention to earlier context
  - GPT-4o atomic-sentence extraction accuracy: 98.8%
- **Ablation highlight:** Prompt-sensitivity study — a "strict" prompt pushes models to rely almost entirely on contextual knowledge.

### Wang Factuality Survey — Factuality of Large Language Models: A Survey
- **Venue/Year:** EMNLP 2024
- **Evaluation:** N/A — survey/position paper
- **Summary:** Survey of LLM factuality covering evaluation and improvement across language and vision modalities. Categorizes benchmarks into four types (open-ended generation, yes/no, short-form/list, multi-choice QA), reviews automatic fact-checker pipelines (claim processor + retriever + verifier, e.g. FactScore, FacTool, Factcheck-GPT), and organizes mitigation techniques across the LLM lifecycle (pre-training, SFT/RLXF, inference-time decoding like CAD and DoLa, ICL/self-reasoning, retrieval augmentation).

### CRAG — Corrective Retrieval Augmented Generation
- **Venue/Year:** arXiv Jan 2024 (v3 Oct 2024)
- **Benchmarks:** PopQA (short-form, accuracy), Biography (long-form, FactScore), PubHealth (true/false, accuracy), Arc-Challenge (multiple choice, accuracy)
- **Baselines:** LLaMA2-7B/13B, Alpaca-7B/13B, CoVE-65B, LLaMA2-chat-13B, ChatGPT, Ret-ChatGPT, Ret-LLaMA2-chat-13B, Perplexity.ai, SAIL, standard RAG, Self-RAG (backbones: LLaMA2-hf-7B and SelfRAG-LLaMA2-7B)
- **Key results:**
  - PopQA accuracy: Self-CRAG 61.8 vs. Self-RAG 54.9 (+6.9); CRAG 54.9 vs. RAG 50.5 (+4.4) on LLaMA2-hf-7B
  - Biography FactScore: Self-CRAG 86.2 vs. Self-RAG 81.2 (+5.0); Self-CRAG 69.1 vs. reproduced Self-RAG* 32.2 on LLaMA2-hf-7B
  - PubHealth accuracy: CRAG 75.6 vs. RAG 39.0 (+36.6) with SelfRAG-LLaMA2-7B; 59.5 vs. 48.9 on LLaMA2-hf-7B
  - Arc-Challenge accuracy: CRAG 68.6 vs. RAG 53.2 (+15.4) with SelfRAG-LLaMA2-7B; 53.7 vs. 43.4 on LLaMA2-hf-7B
  - Retrieval evaluator (T5-based) accuracy on PopQA: 84.3 vs. ChatGPT 58.0, ChatGPT-CoT 62.4, ChatGPT-few-shot 64.7
- **Ablation highlight:** Removing any single triggered action (Correct/Incorrect/Ambiguous) or knowledge-utilization operation degrades accuracy; e.g. Self-CRAG on PopQA drops from 61.8 to 24.9 without external knowledge selection.
