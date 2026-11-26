### KG-Hallucination-Survey — Can Knowledge Graphs Reduce Hallucinations in LLMs?: A Survey
- **Venue/Year:** arXiv 2023 (v2 Mar 2024); Agrawal, Kumarage, Alghamdi, Liu (Arizona State University)
- **Evaluation:** N/A — survey/position paper
- **Summary:** Reviews KG-augmentation methods for reducing hallucinations in LLMs via a three-part taxonomy: (1) Knowledge-Aware Inference (KG-augmented Retrieval, Reasoning, Controlled Generation — e.g., KAPING, StructGPT, IRCoT, MindMap, RoG, KB-Binder); (2) Knowledge-Aware Training (pre-training with knowledge-enhanced models, guided masking, fusion, probing; fine-tuning — e.g., ERNIE, SKEP, JointLK, SKILL, KGLM); (3) Knowledge-Aware Validation (Fact-aware LM, SURGE, FOLK).

### Augmenting-LLMs-Knowledge-Survey — Augmenting LLMs with Knowledge: A Survey on Hallucination Prevention
- **Venue/Year:** arXiv Sep 2023 (student project, TU Delft); Andriopoulos & Pouwelse
- **Evaluation:** N/A — survey/position paper
- **Summary:** Covers background (generative LMs, Transformers, beam search, text corpora, vector DBs/FAISS/MIPS, triplestores, GCN/R-GCN) and knowledge-base augmented generation methods including RAG, REALM, Fusion-in-Decoder (FiD), plus retrieval/tool-augmented approaches. Argues non-parametric memory access is a promising route to mitigate hallucinations, un-grounded responses, and scalability issues.

### Self-RAG — Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection
- **Venue/Year:** ICLR 2024 (arXiv Oct 2023); Asai, Wu, Wang, Sil, Hajishirzi
- **Benchmarks:** PubHealth, ARC-Challenge, PopQA, TriviaQA-unfiltered, Biography generation (FactScore), ALCE-ASQA
- **Baselines:** Llama2-7B/13B, Alpaca-7B/13B, Llama2-chat-13B, ChatGPT, Ret-ChatGPT, Ret-Llama2-chat, Perplexity.ai, Toolformer-6B, SAIL-7B, Llama2-FT-7B, CoVE-65B
- **Key results (Self-RAG 13B vs. best non-proprietary baselines):**
  - PopQA: 55.8 acc (vs. Alpaca-13B 46.7, Ret-Llama2-13B 51.8)
  - TriviaQA: 69.3 acc (vs. Alpaca-13B 61.3)
  - PubHealth: 74.5 acc (vs. Alpaca-13B 55.5)
  - ARC-Challenge: 73.1 acc (vs. Alpaca-13B 54.9)
  - Bio FactScore: 81.2 (7B) / 80.2 (13B) vs. Alpaca-13B 57.6, CoVE-65B 71.2
  - ASQA citation precision 70.3 / recall 71.3 (vs. Alpaca-13B 2.0 / 3.8); beats ChatGPT (65.1) on citation precision
- **Ablation highlight:** Self-RAG 7B/13B outperforms ChatGPT on PubHealth, PopQA, bio, and ASQA (Rouge/MAUVE); reflection tokens enable test-time control of retrieval frequency and support/citation trade-offs.

### Bruno-Hallucinations — Insights into Classifying and Mitigating LLMs' Hallucinations
- **Venue/Year:** CEUR Workshop Proceedings 2023 (arXiv Nov 2023); Bruno, Mazzeo, Chetouani, Tliba, Kerkouri
- **Evaluation:** N/A — survey/position paper
- **Summary:** Classifies hallucinations across six LLM task families (MT, Q&A, Dialog, Summarization, KG+LLM, Visual QA) with a dataset reference table (IWSLT2014, WMT2018, FLORES-200, TruthfulQA, HotpotQA, NQ, MEDMCQA, WoW, CNN/DM, XSum, WebNLG, MSCOCO, etc.). Reviews hallucination detection (grey-box token-probability vs. black-box proxy-LLM; Varshney et al. 88% recall on GPT-3.5) and mitigation families: fine-tuning, knowledge graphs, memory augmentation, context prompts, preemptive strategies (Self-Familiarity).

### Multi-Agent-Debate — Improving Factuality and Reasoning in Language Models through Multiagent Debate
- **Venue/Year:** arXiv May 2023 (ICML 2024); Du, Li, Torralba, Tenenbaum, Mordatch (MIT CSAIL / Google Brain)
- **Benchmarks:** Arithmetic (6 two-digit terms), GSM8K, Chess Move Prediction (BIG-Bench Chess-State Tracking), Biographies (new 524 computer-scientist dataset), MMLU, Chess Move Validity
- **Baselines:** Single Agent (zero-shot), Single Agent (Reflection), Multi-Agent (Majority voting)
- **Key results (3 agents, 2 rounds, ChatGPT):**
  - Arithmetic: 81.8% (Debate) vs. 67.0% (Single), 72.1% (Reflection), 69.0% (Majority)
  - GSM8K: 85.0% vs. 77.0% / 75.0% / 81.0%
  - Chess (ΔPS): 122.9 vs. 91.4 / 102.1 / 102.2
  - Biographies: 73.8% vs. 66.0% / 68.3%
  - MMLU: 71.1% vs. 63.9% / 57.7%
  - Chess Move Validity: 45.2% vs. 29.3% / 38.8%
- **Ablation highlight:** Performance scales monotonically with number of agents (up to ~7) and debate rounds (up to ~4); longer debate prompts, peer-response summarization, and combining with CoT further improve results (GSM8K: 74%→85% with CoT + debate).
