### Huang Survey — A Survey of Agent Memory in the Second Half: Towards Self-Evolving and Long-Horizon Agents
- **Venue/Year:** TMLR (Transactions on Machine Learning Research), 07/2026
- **Evaluation:** N/A — survey/position paper
- **Summary:** Unified three-dimensional taxonomy of foundation agent memory along (1) memory substrate (internal parametric state vs. external retrieval-augmented stores), (2) cognitive mechanism (sensory, working, episodic, semantic, procedural), and (3) memory subject (user-centric personalization vs. agent-centric experience). Analyzes memory operations in single- and multi-agent topologies, learning policies over memory, and reviews evaluation benchmarks/metrics for memory utility.

### MRAgent — Memory is Reconstructed, Not Retrieved: Graph Memory for LLM Agents
- **Venue/Year:** ICML 2026 (PMLR 306), Seoul, South Korea
- **Benchmarks:** LoCoMo, LongMemEval
- **Baselines:** RAG, A-Mem, MemoryOS, LangMem, Mem0
- **Key results:**
  - Overall LLM-Judge (J) on LoCoMo (Gemini backbone): 84.21 vs. best baseline Mem0 68.31 (+23.3% relative gain)
  - Overall J on LoCoMo (Claude backbone): 88.32 vs. best baseline A-Mem 68.45 (+12.4% relative)
  - Multi-hop F1 on LoCoMo (Claude): 56.72 vs. baseline best 48.66 (Mem0)
  - LongMemEval Overall (Gemini): MRAgent 72.95 vs. best baseline MemoryOS 54.92 (+32% relative); MRAgent* 86.76
  - Token consumption on LongMemEval: 118k (MRAgent) vs. 245k–3,268k for baselines (Mem0 245k, A-Mem 632k, LangMem 3,268k)
- **Ablation highlight:** Removing semantic memory layer or reasoning causes clear degradation; multi-turn reasoning raises multi-hop cumulative recall by >30%.

### LSTM-MAS — LSTM-MAS: A Long Short-Term Memory Inspired Multi-Agent System for Long-Context Understanding
- **Venue/Year:** IEEE Transactions on Knowledge and Data Engineering, 2026 (arXiv v2, Apr 2026)
- **Benchmarks:** NarrativeQA, Qasper, HotpotQA, 2WikiMQA, MuSiQue (Q&A); GovReport, QMSum (summarization); SAMSum (few-shot learning) — 8 datasets, from LongBench
- **Baselines:** Vanilla, LightRAG, LONGAGENT, CoA (Chain-of-Agents)
- **Key results (vs. CoA SOTA, Qwen2.5-7B, 8K window):**
  - NarrativeQA F1: +97.97% improvement (LSTM-MAS 20.51 vs. CoA 10.36)
  - Qasper F1: +65.75% (37.89 vs. 22.86)
  - HotpotQA F1: +122.19% (42.75 vs. 19.24)
  - 2WikiMQA F1: +39.61% (31.44 vs. 22.52)
  - MuSiQue F1: +10.80% (15.39 vs. 13.89)
  - Summarization (Qwen2.5-7B): GovReport +79.22%, QMSum +113.10% vs. Vanilla(8K); SAMSum +134.99% vs. Vanilla, +7.73% vs. CoA
  - Narrows gap between small (7B) and large (32B) models within Qwen2.5 series from ~44% to 4.7%
  - Needle-in-a-Haystack tested up to 1500K tokens
- **Ablation highlight:** Removing Manager Agent causes the largest performance drop (avg -18.36 on Qwen2.5-0.5B, -16.73 on Qwen2.5-14B), followed by Filter and Judge agents.

### MCPHallu — MCPHallu: Benchmarking Reasoning, Execution, and Memory Hallucinations in MCP Agents
- **Venue/Year:** Preprint, Nov 2026 (arXiv:2611.07689)
- **Benchmarks:** MCPHallu (new benchmark — 358 tasks, 36 production MCP servers, 5 capability domains: General, Coding, Analytics, Productivity, Financial; 4 hallucination subtypes: Branch Collapse, Context Forgetting, Unreachable Goal, Tool Misuse)
- **Baselines:** 14 frontier LLMs from 8 vendors: GPT-4o, GPT-5-chat, Claude Haiku 4.5, Claude Sonnet 4.5/4.6, Claude Opus 4.5/4.6, Gemini 3 Flash, Doubao-Seed-1.8, DeepSeek-V3.1/V4, Qwen3.5-397B, GLM-5.1, Kimi-K2.6
- **Key results:**
  - Mean overall score across 14 models: 0.642 (range [0,1]); pass rate 47.8%
  - Best model Claude Opus 4.6: 0.728 overall (Branch Collapse 0.755, Context Forgetting 0.730, Unreachable Goal 0.576, Tool Misuse 0.885)
  - Unreachable Goal hardest subtype: average 0.458; only 23.2% pass rate
  - Unreachable Goal pass rate drops from 65.0% with 0 tool calls to 0% with 4+ calls
  - Tool Misuse: correct tool alone yields 84.7% pass rate; mixed with confusion tools drops to 32.3%
- **Ablation highlight:** Deterministic components (outcome + dependency + early-stop + confusion scores) dominate: judge-only ranking correlates with full score at r=0.86 vs. 0.97 for deterministic-only.

### WikiTrace — Don't Just Trust Your Memory: Evidence-Linked Memory Reduces Memory-Induced Degradation in LLM Agents
- **Venue/Year:** Preprint, Nov 2026 (arXiv:2611.14320)
- **Benchmarks:** 8 suites across 5 benchmarks: ALFWorld (Seen/Unseen), ScienceWorld, PlanCraft (Seen/Unseen), tau^3-bench Retail, AppWorld (Normal/Challenge)
- **Baselines:** No Memory, AWM, ReasoningBank, ExpeL, Insights Only
- **Key results (deepseek-v4-flash backbone, avg over 8 suites):**
  - WikiTrace Avg: 90.2 vs. No Memory 79.5 (+10.7 pts), Insights Only 87.0, ExpeL 80.3, AWM 81.6, ReasoningBank 81.7
  - Per-suite: ALFWorld Seen 98.7 / Unseen 98.8; ScienceWorld 96.1; PlanCraft Seen 93.3 / Unseen 81.3; tau^3 Retail 88.2; AppWorld Normal 89.5 / Challenge 75.8
  - Regression (memory-induced failure rate): 4.5% (WikiTrace) vs. 6.5% (Insights Only), 9.7% (rerun baseline)
  - Generalization with GLM-5.3-flash: WikiTrace Avg 92.7 vs. No Memory 71.2, Insights Only 90.9
  - Test-time cost: 1.17x Insights Only while improving by 3.2 pts
- **Ablation highlight:** Advantage over Insights Only concentrates in Descent runs (+16.4 on Hard tasks) and after a blocked attempt (+10.4); 52% of memory-induced failures trace to a wrong memory item.
