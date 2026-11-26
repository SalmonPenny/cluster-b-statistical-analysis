# Results: RQ2 Papers — Benchmarks & Evaluation Outcomes

**Scope:** 82 PDFs in `papers/RQ2/` (some content-duplicates noted inline).
**Contents:** For each paper — benchmarks/datasets used, baselines, key quantitative results, ablation highlight. Surveys/position papers marked "Evaluation: N/A" with a one-line scope summary.
**Generated:** 2026-11-26 via 16 parallel extraction agents reading each PDF.

**Duplicate PDFs detected (deduplicated in this doc):**
- `2024_Li_Mei_RAG_DDR_...pdf` == `2024_Li_RAGDDR.pdf` (RAG-DDR, batch 07)
- `2024_Kortukov_ContextMemoryConflicts.pdf` == `2024_Kortukov_Rubinstein_...pdf` (batch 06)
- `2026_Wu_MemGraphRAG.pdf` == `2026_Wu_Xiang_MemGraphRAG_...pdf` (batch 15)
- `2026_Zhou_CogitoRAG.pdf` == `2026_Zhou_Li_Understand_Then_Memory_...pdf` (batch 16)

---

## Benchmark Overlap Across RQ2 Papers

Benchmarks used by **≥2** papers, sorted by usage count. Shows where the field has converged on common evaluation surfaces and where papers go their own way.

| # | Benchmark | Used by | Papers |
|---|-----------|---------|--------|
| 16 | **Natural Questions (NQ)** | open-domain QA | MemGPT, ChainOfNote, Lookback Lens, Kortukov, ContextFaithful-MemStrength, RAG-DDR, ReEval, Yu MHM, CK-PLUG, Amber, DRAG, DMP, TCR, FIDES, CogitoRAG, ParamMute (via CoFaithfulQA) |
| 13 | **HotpotQA** | multi-hop QA | Kortukov, RAG-DDR, AssistRAG, CK-PLUG, Amber, DRAG, PORAG+ATLAS, LSTM-MAS, MemGraphRAG, TCR, CogitoRAG, TrustMem (via Mem-alpha), ParamMute (via CoFaithfulQA) |
| 11 | **TriviaQA** | open-domain QA | Self-RAG, ChainOfNote, RC-RAG (RC-TQ), Kortukov, RAG-DDR, DRAG, DMP, Amber, TCR (ConflictTQA), FIDES (CF-RAG), ParamMute (via CoFaithfulQA) |
| 8 | **PopQA** | long-tail entity QA | Self-RAG, Xie (Knowledge Conflicts), CRAG, ContextFaithful-MemStrength, DRAG, TCR (ConflictPQA), FIDES (CF-RAG), CogitoRAG |
| 8 | **SQuAD / SQuAD v2** | reading comprehension | LongMem, Kortukov, Amber, DMP, Arteaga, SIRIN, TrustMem (via Mem-alpha), ParamMute (via CoFaithfulQA) |
| 7 | **2WikiMultihopQA** | multi-hop QA | FLARE, AssistRAG, Amber, DRAG, LSTM-MAS, MemGraphRAG, CogitoRAG |
| 7 | **LongMemEval** | long-term conv memory | RMM, OracleAgent, SIRIN, MemBook, MRAgent, Agent-Native Memory Survey, TrustMem (via MemoryAgentBench) |
| 4 | **TruthfulQA** | truthful generation | Rowen, Yu MHM, IMAE, SAFE |
| 4 | **StrategyQA** | commonsense reasoning | FLARE, Xie (Knowledge Conflicts), Rowen, DRAG |
| 4 | **LoCoMo** | long-term conv memory | TeleMem, Synthius-Mem, MRAgent, Agent-Native Memory Survey |
| 3 | **MuSiQue** | multi-hop QA | LSTM-MAS, MemGraphRAG, CogitoRAG |
| 3 | **HaluEval** | hallucination QA | CEG, DMP, IMAE |
| 3 | **FActScore / Biography** | long-form factuality | Self-RAG, Tao WikiAtomic, CRAG |
| 3 | **MMLU** | knowledge benchmark | Multi-Agent Debate, Arteaga, HGU (MMLU subsets) |
| 3 | **WoW / Wizard of Wikipedia** | grounded dialogue | FLARE, RAG-DDR, CK-PLUG (via KILT) |
| 3 | **HaluMem-Medium / Long** | agent memory CRUD | HaluMem (introduces), MemBook, TrustMem |
| 2 | **T-REx** | slot filling | RAG-DDR, CK-PLUG (via KILT) |
| 2 | **FEVER** | fact verification | CK-PLUG (via KILT), TCR |
| 2 | **PubHealth** | true/false factuality | Self-RAG, CRAG |
| 2 | **ARC-Challenge** | science MCQ | Self-RAG, CRAG |
| 2 | **CNN/DM** | summarization | Lookback Lens, RAGTruth |
| 2 | **RealTimeQA** | up-to-date QA | ChainOfNote, ReEval |
| 2 | **ConFiQA** | counterfactual RAG | CK-PLUG, ParamMute |
| 2 | **MSC (Multi-Session Chat)** | long-term dialogue | MemGPT, RMM |
| 2 | **RAGTruth** | RAG hallucination corpus | RAGTruth (introduces), SIRIN |
| 2 | **WikiBio** | biography factuality | Larimar-Scaling, CEG |

### Takeaways

1. **The open-domain QA trio dominates.** NQ (16), HotpotQA (13), TriviaQA (11), PopQA (8) and SQuAD (8) carry most method evaluations. If a new RQ2 method skips all five, it's an outlier — usually because it's a memory-architecture paper evaluated on dialogue/long-term benchmarks instead.
2. **Multi-hop reasoning has three canonical datasets.** HotpotQA, 2WikiMultihopQA, MuSiQue — several papers (CogitoRAG, MemGraphRAG, LSTM-MAS, Amber, DRAG) report all three together as a cluster.
3. **Long-term memory systems converged on LongMemEval + LoCoMo.** Every 2025+ agent-memory paper that benchmarks episodic memory uses at least one of these. LongMemEval (7 papers) is slightly more common than LoCoMo (4).
4. **Hallucination-specific benchmarks are fragmented.** TruthfulQA (4), HaluEval (3), FActScore (3), WikiBio (2), RAGTruth (2), HaluMem (3), ConFiQA (2) — no single benchmark is a de-facto standard for hallucination evaluation.
5. **KILT suite (T-REx, FEVER, WoW)** appears mainly via two papers (CK-PLUG, RAG-DDR) rather than being broadly adopted.
6. **Knowledge-conflict benchmarks are proliferating.** ConFiQA, NQ-Swap, ConflictBank, ConflictTQA/PQA, CoFaithfulQA, MQuAKE, Wikidata-Conflict-5K — most appear in exactly one paper. The taxonomy of benchmarks here is still ahead of reuse.
7. **Many methods ship their own new benchmark** (HaluMem, MCPHallu, WikiAtomic, Concept-7, CoFaithfulQA, RC-TQ/NQ, KnowHalBench, FiFA, ZH-4O, GraphBench, PRISM, Rubric Feedback Bench, MemoryAgentBench) — a sign that general benchmarks under-cover specific failure modes the authors care about.
8. **Multimodal, domain-specific, and agent-execution benchmarks are singletons.** POPE/CHAIR/MME (MemVR), MMCU/CMB (TC-RAG), BioASQ (SAFE), PubMedQA (PORAG+ATLAS), RiTeK/MIMIC (BioMem), ALFWorld/ScienceWorld/AppWorld (WikiTrace), TOFU/MUSE/WMDP (HGU), LCQUAD/QALD (PGMR), Gorilla (PORAG+ATLAS) — each belongs to one paper.

---

## Batch 01

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

---

## Batch 02

### Gao RAG Survey — Retrieval-Augmented Generation for Large Language Models: A Survey
- **Venue/Year:** arXiv 2023 (v5 Mar 2024)
- **Evaluation:** N/A — survey/position paper
- **Summary:** Comprehensive survey of RAG for LLMs covering three paradigms (Naive RAG, Advanced RAG, Modular RAG) and the tripartite foundation of Retrieval, Generation, and Augmentation. Reviews ~100 RAG studies, 26 downstream tasks, ~50 datasets, evaluation objectives/metrics, benchmarks, and tools. No original empirical evaluation.

### Huang Hallucination Survey — A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions
- **Venue/Year:** ACM TOIS 2024 (Vol. 1, Article 1)
- **Evaluation:** N/A — survey/taxonomy paper
- **Summary:** Proposes a redefined taxonomy of LLM hallucinations split into factuality hallucination and faithfulness hallucination (with sub-types: instruction, context, logical inconsistency). Categorizes causes across data, training, and inference stages; surveys detection methods, benchmarks, and mitigation strategies including RAG.

### FLARE — Active Retrieval Augmented Generation
- **Venue/Year:** EMNLP 2023
- **Benchmarks:** 2WikiMultihopQA (multihop QA), StrategyQA (commonsense reasoning), ASQA / ASQA-hint (long-form QA), WikiAsp (open-domain summarization). Also tested on Wizard of Wikipedia and ELI5 (limitations).
- **Baselines:** No retrieval; Single-time retrieval; Previous-window retrieval (RETRO/IC-RALM/KNN-LM style, l=16); Previous-sentence retrieval (IRCoT-style); Question decomposition (self-ask); FLARE_instruct. Base LM: GPT-3.5 (text-davinci-003).
- **Key results:**
  - 2WikiMultihopQA: EM 51.0 / F1 59.7 / Prec 59.1 / Rec 62.6 (FLARE_direct) vs. single-time EM 39.4, best baseline (question decomposition) EM 47.8
  - StrategyQA: EM 77.3 (FLARE) vs. 72.9 no-retrieval, 68.6 single-time, 71.2 previous-window
  - ASQA: EM 41.3 / D-F1 28.2 / R-L 34.3 / DR 31.1 (FLARE) vs. single-time EM 40.2
  - ASQA-hint: EM 46.2 / D-F1 36.7 / R-L 37.7 / DR 37.2 (FLARE) vs. single-time EM 43.2
  - WikiAsp: UniEval 53.4 / entity-F1 18.9 / R-L 27.6 (FLARE) vs. single-time UniEval 52.4
- **Ablation highlight:** Using the generated next sentence as the retrieval query beats using the previous sentence (2WikiMultihopQA EM 48.8 vs. 39.0); retrieval triggered for 40-80% of sentences gives best performance.

### MemGPT — MemGPT: Towards LLMs as Operating Systems
- **Venue/Year:** arXiv 2023 (v2 Feb 2024); later ICLR 2024
- **Benchmarks:** Multi-Session Chat (MSC) — Deep Memory Retrieval (DMR) + Conversation Opener task; Document QA on NaturalQuestions-Open (Wikipedia retriever-reader setup); Nested Key-Value (KV) retrieval (new task, 140 UUID pairs, 0-4 nesting levels).
- **Baselines:** Fixed-context GPT-3.5 Turbo, GPT-4, GPT-4 Turbo; human-authored conversation openers; truncation-based document retrieval.
- **Key results:**
  - DMR Accuracy: GPT-4 + MemGPT 92.5% vs. GPT-4 alone 32.1%; GPT-4 Turbo + MemGPT 93.4% vs. 35.3%; GPT-3.5 + MemGPT 66.9% vs. 38.7%
  - DMR ROUGE-L: 0.827 (GPT-4 Turbo + MemGPT) vs. 0.359 baseline
  - Conversation opener SIM-1/SIM-3 (human reference 0.800/0.800): GPT-4 + MemGPT 0.868/0.843 (exceeds human); SIM-H 0.817 (GPT-3.5 + MemGPT) vs. human 1.000
  - Nested KV retrieval: MemGPT (GPT-4) ≈100% accuracy up to 4 nesting levels; GPT-3.5/GPT-4/GPT-4 Turbo baselines drop to near 0% by 2-3 nesting levels
  - Document QA: MemGPT accuracy unaffected by number of retrieved documents (up to 200); fixed-context GPT-4/GPT-3.5 degrade significantly beyond ~25 documents
- **Ablation highlight:** MemGPT with GPT-4 outperforms MemGPT with GPT-4 Turbo on nested KV (weaker function-calling in Turbo variant), showing underlying model's function-calling ability drives performance.

### Generative Agents — Generative Agents: Interactive Simulacra of Human Behavior
- **Venue/Year:** UIST 2023
- **Benchmarks:** Controlled evaluation via author-designed interview protocol (5 categories: self-knowledge, memory, plans, reactions, reflections) with 100 Prolific human evaluators (within-subjects ranking). End-to-end evaluation: 2-day simulation of 25 agents in Smallville sandbox measuring information diffusion, relationship formation, and coordination.
- **Baselines:** Ablations (No Reflection; No Reflection+Plan; No Reflection+Plan+Observation) and a Human Crowdworker condition. Base LLM: ChatGPT (gpt-3.5-turbo).
- **Key results:**
  - TrueSkill believability ratings: Full architecture mu=29.89 (sigma=0.72); No Reflection mu=26.88; No Reflection/Plan mu=25.64; Human Crowdworker mu=22.95; Fully ablated (no memory/plan/reflection) mu=21.21
  - Cohen's d = 8.16 (Full vs. fully ablated, ≈8 std deviations effect size)
  - Kruskal-Wallis H(4)=150.29, p<0.001; all pairwise Dunn post-hoc differences significant (p<0.001) except crowdworker vs. fully ablated
  - Information diffusion over 2 game days: mayoral candidacy awareness grew 4% (1 agent) → 32% (8 agents); Valentine's party awareness 4% → 52% (13 agents); 1.3% (n=6/453) hallucination rate in agent responses
  - Relationship formation: network density grew from 0.167 to 0.74; 5 of 12 invited agents actually attended the Valentine's party
- **Ablation highlight:** Each memory component (observation, reflection, planning) contributes significantly — removing any one degrades believability monotonically.

---

## Batch 03

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

---

## Batch 04

### ChainOfNote — Chain-of-Note: Enhancing Robustness in Retrieval-Augmented Language Models
- **Venue/Year:** EMNLP 2024 (arXiv 2311.09210)
- **Benchmarks:** NQ, TriviaQA, WebQ, RealTimeQA (for unknown-robustness)
- **Baselines:** QA fine-tune w/o IR, SAIL (Luo et al. 2023), Retrieve-Read (REPLUG, Shi et al. 2023c), Chain-of-Thought prompting; backbones: LLaMa-2 7B and GPT-4
- **Key results:**
  - LLaMa-2 7B Retrieve-Read + CoN avg EM/F1: 50.46 / 58.78 vs Retrieve-Read 48.49 / 56.97 (+1.97 EM / +1.81 F1 avg across NQ/TriviaQA/WebQ)
  - NQ EM: 48.92 (CoN) vs 47.39 (Retrieve-Read); TriviaQA EM: 76.27 vs 74.92; WebQ EM: 32.33 vs 29.58
  - GPT-4 + CoN avg accuracy: 65.7 vs Retrieve-Read 63.1 (+2.6); beats CoT (64.4) by +1.3
  - Noise robustness (100% noise): avg EM 47.66 (CoN) vs 39.72 (Retrieve-Read), +7.94 EM / +7.63 F1
  - RealTimeQA (unknown robustness): Reject Rate 13.0 (CoN) vs 6.1 (Retrieve-Read), +10.5 RR; EM 15.7 vs 15.6
- **Ablation highlight:** Hybrid training (50% standard RALM + 50% CoN) keeps inference time ~0.61s (vs 12.02s with full CoN) while retaining most robustness gains.

### Zhang-HalluSurvey — Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models
- **Venue/Year:** arXiv 2309.01219 (Tencent AI Lab et al., v3 Sept 2024/2025)
- **Evaluation:** N/A — survey/position paper
- **Summary:** Surveys LLM hallucination (input-, context-, fact-conflicting), catalogs benchmarks (TruthfulQA, FActScore, HaluEval, FACTOR, FactualityPrompt, SAFE, SimpleQA, FELM, Pinocchio, HaluEval 2.0, Lynx, FactCHD, KoLA-KC), sources (pre-training→SFT→RLHF→inference), and mitigation strategies; no original experiments.

### Agrawal-KG-Survey — Can Knowledge Graphs Reduce Hallucinations in LLMs?: A Survey
- **Venue/Year:** NAACL 2024 (Volume 1: Long Papers, pp. 3947–3960)
- **Evaluation:** N/A — survey/position paper
- **Summary:** Proposes a taxonomy of KG-augmented LLM methods in three categories: Knowledge-Aware Inference (KG-augmented Retrieval/Reasoning/Controlled Generation), Knowledge-Aware Learning (pre-training & fine-tuning), and Knowledge-Aware Validation. Reports secondhand numbers from cited works (e.g., RoG raises ChatGPT accuracy from 66.8% to 85.7%; MindMap reaches 88.2% on clinical reasoning); conducts no original experiments.

### Arteaga-BatchEnsemble — Hallucination Detection in LLMs: Fast and Memory-Efficient Fine-Tuned Models
- **Venue/Year:** Proceedings of the 6th Northern Lights Deep Learning Conference (NLDL), PMLR 265, 2025 (arXiv 2409.02976, Dec 2024)
- **Benchmarks:** SQuAD and SQuAD v2 (faithfulness hallucination + OOD), MMLU (factual hallucination); backbone Mistral-7B-Instruct-v0.2
- **Baselines:** Single Model (LoRA fine-tune), Sample-Based uncertainty (stochastic sampling, temp=0.5, top-p=0.99, top-k=5), LoRA Ensemble (Wang et al. regularization), plus their BatchEnsemble+NI (noise injection) variant
- **Key results:**
  - Faithfulness hallucination detection top-1 accuracy: 97.8% (BatchEnsemble) vs 92.5 (LoRA Ensemble), 92.1 (Sample-Based), 96.5 (BatchEnsemble+NI)
  - Factual hallucination (MMLU) accuracy: 73.9% (LoRA Ensemble, best) vs 68.0 (BatchEnsemble), 69.6 (Sample-Based), 66.9 (BatchEnsemble+NI)
  - OOD detection accuracy: 63.3% (LoRA Ensemble) vs 62.4 (BatchEnsemble), 62.2 (Sample-Based), 61.9 (BatchEnsemble+NI)
  - Predictive performance: SQuAD EM/F1 = 85.9 / 93.4 (BatchEnsemble) vs 85.1 / 92.1 (Single Model); MMLU accuracy 56.7 (BatchEnsemble) vs 56.3 (Single Model); LoRA Ensemble degrades to 68.4 / 84.4 EM/F1 and 44.6 MMLU
- **Ablation highlight:** All experiments run on a single A40 GPU; BatchEnsemble parameter growth is negligible vs linear growth in vanilla ensembles.

### Bechard-RAG-Structured — Reducing Hallucination in Structured Outputs via Retrieval-Augmented Generation
- **Venue/Year:** NAACL 2024 Industry Track, pp. 228–238 (ServiceNow)
- **Benchmarks:** Internal ServiceNow workflow-generation dataset (NL → JSON workflow) — Train 2,867 / Dev 318 / Test 798 / Human Eval 157; plus 5 OOD splits (OOD1–OOD5, 42–429 examples)
- **Baselines:** No-Retriever variants of StarCoderBase (1B/3B/7B/15.5B); With-Retriever variants of same StarCoderBase sizes, plus CodeLlama-7B and Mistral-7B-v0.1; retriever encoders compared: GTR-T5 (base/large/xl/xxl) vs all-mpnet-base-v2 with Random/BM25/ANCE/All negative sampling
- **Key results:**
  - StarCoderBase-7B without retriever: Trigger EM 0.547, BofS 0.669, Hallucinated Steps 0.137, Hallucinated Tables 0.206
  - StarCoderBase-7B with RAG: Trigger EM 0.664, BofS 0.672, Hallucinated Steps 0.019, Hallucinated Tables 0.042 (hallucinated steps drop from 13.7% → 1.9%)
  - StarCoderBase-15.5B with RAG: Trigger EM 0.667, BofS 0.667, HS 0.040, HT 0.016
  - StarCoderBase-1B with RAG: HS drops from 15.7% → 7.2%, HT from 19.2% → 4.4%
  - OOD avg (RAG StarCoderBase-7B): Trigger EM 0.647, BofS 0.714, HS 0.018, HT 0.066
  - Retriever: fine-tuned all-mpnet-base-v2 (110M) + all negative strategies achieves Step Recall@15 = 0.743, Table Recall@10 = 0.766, beating much larger GTR-T5-xxl (4.8B) at 0.561/0.489
- **Ablation highlight:** 3B RAG-fine-tuned model is competitive with 15.5B no-RAG on Trigger EM / Bag-of-Steps while keeping hallucination low — RAG enables deploying substantially smaller LLMs.

---

## Batch 05

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

---

## Batch 06

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

---

## Batch 07

### KELDaR — A Framework of Knowledge Graph-Enhanced Large Language Model Based on Question Decomposition and Atomic Retrieval
- **Venue/Year:** Findings of EMNLP 2024
- **Benchmarks:** WebQSP (WebQuestionsSP), CWQ (ComplexWebQuestions) — both KGQA over Freebase
- **Baselines:** Training-based: KV-Mem, GraftNet, PullNet, EmbedKGQA, TransferNet, NSM, KGT5, SR+NSM+E2E, TIARA, KD-CoT, UniKGQA, ReasoningLM, DecAF, RoG. Reasoning-based: StructGPT, KB-BINDER, ToG, IO, CoT, CoT+SC (all with GPT-3.5-turbo)
- **Key results (Exact Match %):**
  - 79.4 on WebQSP, 53.6 on CWQ (KELDaR-rel* — best configuration, with golden topics)
  - 75.5 on WebQSP, 41.9 on CWQ (KELDaR without golden topics)
  - +14.6 EM on WebQSP and +19.2 EM on CWQ vs. IO prompting baseline
  - +5.0 EM on WebQSP and +12.0 EM on CWQ vs. previous best reasoning-based method
  - Second-best on CWQ behind only RoG* (69.0); competitive with most training-based baselines without any fine-tuning
- **Ablation highlight:** Relation-based extraction strategy (KELDaR-rel*) outperforms triple/quadruple-based (KELDaR*) on CWQ (53.6 vs 50.7).

### RAG-DDR — RAG-DDR: Optimizing Retrieval-Augmented Generation Using Differentiable Data Rewards
- **Venue/Year:** ICLR 2025
- **Note:** `2024_Li_Mei_RAG_DDR_Differentiable_Data_Rewards_RAG.pdf` and `2024_Li_RAGDDR.pdf` are the SAME paper (arXiv:2410.13509v2 — same authors, abstract, tables).
- **Benchmarks:** NQ, TriviaQA, MARCO QA (open-domain QA), HotpotQA (multi-hop), T-REx (slot filling), Wizard of Wikipedia/WoW (dialogue)
- **Baselines:** LLM w/o RAG, Vanilla RAG, REPLUG, Self-RAG, RA-DIT (with MiniCPM-2.4B and Llama3-8B backbones)
- **Key results (Llama3-8B, RAG-DDR w/ 2-Round):**
  - NQ: 52.1 Acc (vs Vanilla RAG 46.2, RA-DIT 46.2)
  - TriviaQA: 89.6 (vs Vanilla RAG 84.0)
  - MARCO QA: 27.3 Rouge-L (vs Vanilla RAG 20.6)
  - HotpotQA: 39.0 Acc (vs Vanilla RAG 30.1, RA-DIT 34.9)
  - T-REx: 40.6 (RA-DIT 41.7 — second-best here)
  - WoW: 16.8 F1 (vs Vanilla RAG 12.5)
  - ~7% average improvement over Vanilla RAG
- **Ablation highlight:** Training only the generation module (V_Gen) drives most of the gains; training only knowledge refinement (V_KR) gives only marginal improvements.

### Self-Familiarity — Zero-Resource Hallucination Prevention for Large Language Models
- **Venue/Year:** Findings of EMNLP 2024
- **Benchmarks:** Concept-7 (newly proposed: 192 basic concepts, 451 basic instructions, 180 test concepts — 106 real + 74 fictional, 515 test instructions from seven expert domains)
- **Baselines:** Greedy-Perplexity, Greedy-AvgLogP, Greedy-MinLogP, Sample-BERTScore, Sample-SentenceScore, Self-Detection, Forward-Inference, Forward-Self
- **Key results (Self-Familiarity best AUC across all 5 LLMs):**
  - Vicuna-13b-v1.3: AUC 0.927, ACC 0.868, F1 0.854 (best baseline Sample-BERTScore AUC 0.872)
  - Llama-2-13b-chat: AUC 0.909, ACC 0.835, F1 0.812 (best baseline Greedy-Perplexity AUC 0.885)
  - Falcon-7b-instruct: AUC 0.926, ACC 0.882, F1 0.822 (best baseline AUC 0.697)
  - mpt-7b-instruct: AUC 0.921, ACC 0.850, F1 0.817
  - Alpaca-7b: AUC 0.918, ACC 0.866, F1 0.848
  - Human-annotated validation (Vicuna-13b-v1.3): AUC 0.892, ACC 0.827, F1 0.813 (best)
- **Ablation highlight:** All three concept-processing steps (Grouping, Filtering, Ranking) contribute; weighted averaging aggregation beats Minimal-Only (F1 0.767) and Most-Infrequent-Only (F1 0.858).

### RAGTruth — RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models
- **Venue/Year:** ACL 2024 (Volume 1: Long Papers)
- **Benchmarks:** RAGTruth corpus (newly proposed: ~18,000 annotated responses across QA (MS MARCO), Data-to-text Writing (Yelp Open Dataset), News Summarization (CNN/DM + recent news); 2,965 instances, 17,790 responses, word-level hallucination annotations; responses from 6 LLMs: GPT-4-0613, GPT-3.5-turbo-0613, Mistral-7B-Instruct, Llama-2-7B/13B/70B-chat)
- **Baselines (detection methods):** Prompt_GPT-3.5-turbo, Prompt_GPT-4-turbo, SelfCheckGPT_GPT-3.5-turbo, LMvLM_GPT-4-turbo, Finetuned Llama-2-13B (proposed)
- **Key results:**
  - Response-level detection overall F1: Finetuned Llama-2-13B 78.7 vs. GPT-4-turbo Prompt 63.4, SelfCheckGPT 58.8, GPT-3.5-turbo Prompt 52.9, LMvLM 36.2
  - Finetuned Llama-2-13B per-task F1: QA 68.2, Data-to-text 88.1, Summarization 59.1 (all best)
  - Span-level overall F1: Finetuned Llama-2-13B 52.7 vs. GPT-4-turbo Prompt 28.3, GPT-3.5-turbo Prompt 12.8
  - Hallucination suppression (sampling best-of-two using detector): -42.9% hallucination for GPT-3.5-Turbo, -51.0% for GPT-4; -21.6% / -63.2% for Llama-2-7B-chat / Mistral-7B
  - Hallucination density per 100 words: GPT-4-0613 0.08 (lowest), GPT-3.5-turbo 0.12, Llama-2-70B-chat (4-bit) 0.26, Llama-2-13B-chat 0.48, Mistral-7B-Instruct 0.86, Llama-2-7B-chat 1.27 (highest)
- **Ablation highlight:** Fine-tuned 13B open-source model beats prompt-based GPT-4-turbo for hallucination detection (78.7 vs 63.4 F1).

---

## Batch 08

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

---

## Batch 09

### Yu MHM — Mechanistic Understanding and Mitigation of Language Model Non-Factual Hallucinations
- **Venue/Year:** Findings of EMNLP 2024
- **Benchmarks:** ParaRel (diagnostic dataset for mechanistic analysis), Natural Questions, TruthfulQA
- **Baselines:** Vanilla SFT, 5-shot ICL, MEND (knowledge editing), DoLa (contrastive decoding)
- **Key results:**
  - Natural Questions (Llama-2-7B-chat): MHM 47.6 Effectiveness / 95.5 Specificity vs. SFT 41.8 / 82.3 and DoLa 27.0 / 69.6
  - TruthfulQA (Llama-2-7B-chat): MHM 48.2 Eff. / 95.6 Spec. vs. DoLa 43.4 / 81.0 and MEND 33.7 / 40.5
  - Natural Questions (Pythia-6.9B): MHM 46.9 / 92.4 vs. SFT 37.9 / 89.9
  - Natural Questions (GPT-J): MHM 43.8 / 89.4 vs. SFT 34.4 / 86.0
  - TruthfulQA (GPT-J): MHM 49.7 / 95.8 vs. DoLa 37.9 / 90.0
- **Ablation highlight:** MHM preserves >90% of baseline performance on left-out specificity questions; MEND struggles specifically on TruthfulQA due to distractor confusion.

### ReEval — ReEval: Automatic Hallucination Evaluation for Retrieval-Augmented Large Language Models via Transferable Adversarial Attacks
- **Venue/Year:** Findings of NAACL 2024
- **Benchmarks:** Natural Questions (NQ, MRQA version), RealTimeQA (newly perturbed via answer-swapping and context-enriching attacks)
- **Baselines:** Zero-shot open-book, Faithful Prompt (opinion-based prompt from Zhou et al. 2023); evaluated LLMs: Alpaca-7B, ChatGPT, Claude 2, PaLM, GPT-4
- **Key results:**
  - NQ Category 1 (answer-swapping), GPT-4 zero-shot: 54.11 EM / 68.50 F1 / 81.29 Entailment; Faithful Prompt raises Entail to 82.51
  - NQ Category 2 (context-enriching), GPT-4 zero-shot: 37.68 EM / 67.27 F1 / 68.39 Entail — large drop across all models
  - RealTimeQA Category 1, GPT-4: 66.97 EM / 77.81 F1 / 88.59 Entail (most robust model)
  - Alpaca-7B NQ Category 1 zero-shot: 18.71 EM / 56.65 Entail (very vulnerable)
  - Human readability of generated adversarial evidence: 90.8% (Cat 1), 92.4% / 88.8% (Cat 2 variants)
- **Ablation highlight:** Adversarial examples generated by ChatGPT (pivot) transfer across all tested LLMs including GPT-4; Faithful Prompt yields no consistent improvements.

### AssistRAG — Boosting the Potential of Large Language Models with an Intelligent Information Assistant
- **Venue/Year:** NeurIPS 2024
- **Benchmarks:** HotpotQA, 2WikiMultiHopQA, Bamboogle (500 validation Qs each)
- **Baselines:** CloseBook, Naive RAG, ReAct, IRCoT, Self-Ask, Self-RAG (7B), LLMLingua
- **Key results:**
  - HotpotQA (ChatGPT-3.5): AssistRAG 34.4 EM / 44.8 F1 / 46.5 Prec vs. best baseline Self-RAG 31.0 / 42.4 / 42.3 and Naive RAG 24.6 / 33.0 / 34.5
  - 2Wiki (ChatGPT-3.5): AssistRAG 39.6 / 45.6 / 45.7 vs. Self-RAG 35.0 / 40.7 / 42.6
  - Bamboogle (ChatGPT-3.5): AssistRAG 34.6 / 41.4 / 41.1 vs. Self-RAG 29.8 / 35.5 / 37.8
  - HotpotQA (LLaMA2-chat 7B): AssistRAG 32.4 EM vs. Naive RAG 18.2
  - HotpotQA (ChatGLM-6B): AssistRAG 33.0 EM vs. Naive RAG 21.8
- **Ablation highlight:** AssistRAG confers larger gains on less advanced foundation models (LLaMA2-chat 7B gains ~14 EM on HotpotQA).

### MemVR — Look Twice Before You Answer: Memory-Space Visual Retracing for Hallucination Mitigation in Multimodal Large Language Models
- **Venue/Year:** ICML 2025 (PMLR 267)
- **Benchmarks:** POPE, CHAIR, MME (incl. MME-Hall subset), MMBench, MM-Vet, VizWiz-VQA, LLaVA-Bench (in-the-wild), HallusionBench
- **Baselines:** Vanilla greedy/sample decoding, OPERA, VCD, ICD (on LLaVA-1.5, Qwen-VL, GLM4V backbones)
- **Key results:**
  - POPE (A-OKVQA, LLaVA-1.5-7B): MemVR 91.10 Acc / 90.83 F1 (Random) vs. baseline 83.45 / 82.56 — up to +7.0% accuracy and +7.5% F1 on average
  - CHAIR (LLaVA-1.5): CHAIR_S 46.6 (-3.4) and CHAIR_I 13.0 (-2.4) vs. 50.0 / 15.4 baseline; Recall 80.8 (+3.7)
  - MME total (LLaVA-1.5): 1896.72 vs. 1864.68 baseline (+32.2 marks)
  - HallusionBench aACC (LLaVA-1.5): 42.5 (+1.0 over baseline 36.7)
  - Latency: MemVR 68.32 ms/token (x1.06) vs. OPERA 240.59 (x3.66) and VCD 144.62 (x2.20) — far more efficient
- **Ablation highlight:** Dynamic (uncertainty-triggered) VR beats all static-layer strategies; optimal injection ratio alpha 5-35% and threshold gamma ~0.75.

### FiFA / MaRS — Forgetful but Faithful: A Cognitive Memory Architecture and Benchmark for Privacy-Aware Generative Agents
- **Venue/Year:** arXiv preprint, December 2025
- **Benchmarks:** FiFA (newly introduced multi-agent simulation benchmark) with metrics Narrative Coherence, Goal Completion Rate, Social Recall Accuracy, Privacy Preservation, Cost Efficiency, Composite score; 6 policies x 5 budgets x 10 seeds = 300 runs across five scenario types
- **Baselines:** Six forgetting policies — FIFO, LRU, Priority Decay, Reflection-Summary, Random-Drop, and Hybrid
- **Key results (Table 2 — note: inconsistent with abstract's "Hybrid ~0.911" claim):**
  - Composite: Random Drop 0.635 ± 0.024 (best) > FIFO 0.602 > Priority Decay 0.601 > LRU 0.590 > Hybrid 0.589
  - Narrative Coherence: Random Drop 0.667; Hybrid 0.590 vs. FIFO 0.529, LRU 0.501
  - Goal Completion: Random Drop 0.078; Priority Decay 0.071; Hybrid 0.069; FIFO 0.061
  - Social Recall Accuracy: FIFO/LRU/Random all 1.000 (ceiling); Hybrid 0.999; Priority 0.990
  - Privacy Preservation: LRU 0.780 (best); Hybrid 0.768; FIFO 0.752; Random 0.722
  - Cost Efficiency: FIFO 0.941 (best); Random Drop 0.935; LRU 0.887; Priority 0.825; Hybrid 0.730
  - ANOVA: policy effect highly significant for NC, GCR, CE, Composite (p < 0.0001); non-significant for SRA (p=0.238) and PP (p=0.485)
- **Ablation highlight:** Budget independence over 2K-32K tokens — larger budgets reduce eviction trigger frequency but not qualitative policy ranking; policy choice dominates capacity as the primary design lever.

---

## Batch 10

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

---

## Batch 11

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

---

## Batch 12

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

---

## Batch 13

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

---

## Batch 14

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

---

## Batch 15

### BioMem — BioMem: Agentic Memory for Biomedical LLM Agents
- **Venue/Year:** arXiv preprint, Nov 2026 (arXiv:2611.13426)
- **Benchmarks:** RiTeK-PharmKG, RiTeK-ADInt (biomedical knowledge reasoning); MIMIC-III Mortality, MIMIC-III Readmission, TCGA-Reports, MIMIC-IV OOD (clinical prediction); RealMem medical subset (long-term conversational memory — dynamic incremental, dynamic updating, proactive alignment, temporal reasoning, single/multi-session)
- **Baselines:** A-MEM, MemZero (Mem0), LightMem, NaiveRAG, FullContext
- **Key results:**
  - HMRU average relative improvement: +8.6% across biomedical QA + conversational memory benchmarks
  - Conversational answer errors reduced by 24.9%; closes 48.0% of gap to full-context inference
  - A-MEM with HuatuoGPT-3-27B: EM-F1 = 39.27 (RiTeK-PharmKG) and 52.94 (RiTeK-ADInt), vs. NaiveRAG 39.04 / 51.63 and FullContext 26.80 / 36.83
  - A-MEM on TCGA-Reports (HuatuoGPT-3-27B): AUPRC 99.06 / AUROC 99.93
  - NaiveRAG on MIMIC-IV OOD (HuatuoGPT-3-27B): AUPRC 15.61 / AUROC 85.47 (vs. A-MEM 4.94 / 82.16)
  - RealMem (HuatuoGPT-3-27B): FullContext QA/Recall = 97.98 / 98.23 on dynamic updating; A-MEM with Qwen3-30B on proactive alignment: QA 78.90 / Recall 82.00 (beats FullContext by +4.90 / +8.00)
- **Ablation highlight:** Iterative A-MEM memory evolution yields source-unsupported content — on MIMIC-IV OOD, unsupported context rises from ~12% (initial) to 44% (after evolution); memories rewritten 5+ times reach ~80% unsupported.

### Luo-MemorySurvey — From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms
- **Venue/Year:** Findings of ACL 2026 (pp. 41622–41652)
- **Evaluation:** N/A — survey/position paper
- **Summary:** Proposes a three-stage evolutionary framework for LLM agent memory mechanisms: Storage (linear/vector/structured), Reflection (introspection/environment/coordination), Experience (explicit/implicit/hybrid cross-trajectory abstraction). Structured by a "Why-How-What" logic. Outlines future directions: active memory perception, working-memory organization, Experience-stage benchmarks, distributed shared memory, multimodal memory.

### MemGraphRAG — MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation
- **Venue/Year:** KDD 2026 (Proc. of the 32nd ACM SIGKDD, Jeju, Korea, Aug 9-13, 2026)
- **Note:** `2026_Wu_MemGraphRAG.pdf` and `2026_Wu_Xiang_MemGraphRAG_Memory_Multi_Agent_Graph_RAG.pdf` are the SAME paper (Wu, Xiang, Tang, Chen, Zhang, Su — Xiamen University; arXiv:2606.00610).
- **Benchmarks:** HotpotQA, 2WikiMultiHopQA, MuSiQue, G-Bench (Medical), G-Bench (Novel)
- **Baselines:** Zero-shot (Llama3-8B/13B, GPT-3.5-Turbo, GPT-4o-mini); Vanilla RAG (Top-1/3/5); Graph-RAG: KGP, G-Retriever, RAPTOR, MS-GraphRAG, LazyGraphRAG, LightRAG, HippoRAG, HippoRAG2, E²GraphRAG, GFM-RAG, LogicRAG, LinearRAG
- **Key results:**
  - Overall average accuracy: MemGraphRAG = 59.25 vs. strongest baseline HippoRAG2 55.79 (+3.46); +28.26 over GPT-4o-mini zero-shot
  - HotpotQA: Str-Acc 67.20 / LLM-Acc 71.60
  - 2WikiMultiHopQA: Str-Acc 70.30 / LLM-Acc 69.80
  - MuSiQue: Str-Acc 34.40 / LLM-Acc 37.90
  - G-Medical: LLM-Acc 68.40; G-Novel: LLM-Acc 57.41
  - G-Bench Medical retrieval: Fact Retrieval Recall 89.56 / Relevance 88.53; Complex Reasoning 90.42 / 82.64
  - Retrieval latency: 0.061 s per query (vs. LightRAG 11.052 s, HippoRAG 1.586 s)
  - Llama-3-70B backbone: avg 58.41 vs. HippoRAG2 55.41; 2Wiki Containment-Acc 69.40 / LLM-Acc 66.80
- **Ablation highlight:** Removing Conflict Resolution causes the largest drop on HotpotQA (69.40 -> 66.95); removing Schema Filter hurts 2Wiki (-> 68.10) and G-Medical (-> 65.92).

### PRISM — PRISM: Probing Reasoning, Instruction, and Source Memory in LLM Hallucinations
- **Venue/Year:** arXiv preprint v2, Apr 2026 (arXiv:2604.16909)
- **Benchmarks:** PRISM (self-constructed; 9,448 instances, 65 sub-tasks, 4 failure dimensions — KE, KM, RE, IFE)
- **Baselines:** 24 LLMs — Proprietary (GPT-5.2, GPT-5.1, GPT-4o, Gemini-3-Pro/Flash, Gemini-2.5-Pro/Flash, Claude-Opus/Sonnet/Haiku-4.5, Grok-4.1, Grok-4-0709) and Open-source (DeepSeek-V3.2, DeepSeek-R1, R1-Distill-32B, Qwen3-235B-Instruct, Qwen2.5-72B-Instruct, GLM-4.5, GLM-4, Llama-4-Scout, Llama-3.3-70B, Llama-3.1-8B, Llama-3-70B-8192, Llama-3-8B)
- **Key results (hallucination rate %, lower is better; H-Score = macro-avg of KE/KM/RE/IFE):**
  - Claude-Opus-4.5: H-Score 13.90 (KE 13.80 / KM 6.35 / RE 19.68 / IFE 15.77) — best overall
  - Gemini-3-Pro: H-Score 14.29; Gemini-3-Flash: 15.55
  - Best open-source: Qwen3-235B-Instruct H-Score 17.03; DeepSeek-V3.2 17.14; DeepSeek-R1 17.25
  - Worst: Llama-3-8B-Instruct H-Score 32.03 (RE 54.02, IFE 32.53)
  - Lowest KM: GPT-5.2 at 5.57%
- **Ablation highlight:** Mitigation trade-offs on Llama-3.1-8B: Reasoning SFT improves RE (94.99 -> 89.09) but degrades KE (43.15 -> 67.02) and KM (11.95 -> 29.56). No single strategy wins across all dimensions.

---

## Batch 16

### TrustMem — TRUSTMEM: Learning Trustworthy Memory Consolidation for LLM Agents with Long-Term Memory
- **Venue/Year:** arXiv preprint, Jun 2026 (Samsung AI Center + University of Notre Dame)
- **Benchmarks:** MemoryAgentBench; HaluMem (HaluMem-Medium); Mem-alpha validation set (SQuAD, HotpotQA, PerLTQA, TREC-C, NLU, PubMed, BookSum)
- **Baselines:** Long-Context, RAG-Top2, MemAgent, MEM1, Mem-T, Mem-alpha, AtomMem, Mem0, Memobase, Supermemory, Zep
- **Key results:**
  - Mem-alpha validation avg: 66.3 (TrustMem) vs 61.9 (Mem-alpha, strongest baseline) — +4.4 pts
  - MemoryAgentBench avg: 65.7 vs Mem-alpha 59.2 (+6.5 pts); best Single-Doc 83.0, TREC-C 85.0, Banking77 84.0
  - HaluMem Memory Extraction F1: 69.45 vs Mem0 57.31 — +12.14 F1 pts
  - Transition-level error reduction vs strongest baseline per type: Omission 40.1% (8.08% vs 13.48%), Corruption 79.1% (0.14% vs 0.67%), Hallucination 50.0% (0.01% vs 0.02%)
- **Ablation highlight:** Removing R_act drops overall from 66.3 to 54.0; removing Transition Verifier (R_ver) drops to 58.7; PRM-style GRPO 60.3 vs Transition-Ranked GRPO 66.3.

### TCR — Seeing through the Conflict: Transparent Knowledge Conflict Handling in Retrieval-Augmented Generation
- **Venue/Year:** AAAI 2026
- **Benchmarks:** Wikidata-Conflict-5K (detection); ConflictTQA (TriviaQA); ConflictPQA (PopQA); NQ, HotpotQA, FEVER, ConflictBank; biomedical/financial cross-domain
- **Baselines:** Prompt, KAFT, IRCAN, RAAT, Parenting, CD^2, Astute RAG, InstructRAG, Self-Route
- **Key results:**
  - Conflict detection F1 84.3 / AUROC 0.901 (TCR) vs IRCAN 79.1 / 0.845 (+5 to +18 F1)
  - ConflictTQA (Llama-3-8B): KGRR 69.2 / MCOR 61.9 (TCR) vs Prompt 42.4 / 19.5 — KGRR +21.4 pp, MCOR −29.3 pp
  - Natural Questions (Llama-3-8B, single Google top-1 doc): 54.8% vs Astute RAG 51.2 / Self-Route 46.5
  - 30% distractor noise: EM drop only 7.2 (TCR) vs Prompt 18.4 / RAAT 16.1
  - Efficiency: 0.3% extra params (21M); 26.7 tok/s vs 28.3 for Prompt
- **Ablation highlight:** Removing self-answerability drops MCOR/KGRR ~18/26 pp; removing signal integration collapses by 55/53 pp.

### FIDES — FIDES: Faithful Inference via Deep Evidence Signals for Retrieval-Memory Conflict in RAG
- **Venue/Year:** arXiv preprint, Jun 2026
- **Benchmarks:** NQ-Swap (n=8000), PopQA CF-RAG (n=8000), TriviaQA CF-RAG (n=8000), non-conflict NQ control
- **Baselines:** Standard RAG, DoLa, CAD, AdaCAD, COIECD, DeCoRe, DVD, CLEAR (trained reference)
- **Key results:**
  - LLaMA3-8B / NQ-Swap: CF 88.23 vs AdaCAD 84.23 (+4.0); EM 43.43; F1 53.84
  - LLaMA3-8B / PopQA: CF 90.58 vs AdaCAD 86.70 (+3.88); EM 44.13; F1 50.19
  - Qwen3-8B / NQ-Swap: CF 89.63, EM 49.82, F1 55.27
  - LLaMA3-70B / NQ-Swap: CF 92.45 (+5.6 over AdaCAD); F1 surges to 61.82
  - Overall: +14 to +28 CF over Standard RAG; +3 to +13 CF over AdaCAD across 18 model-dataset settings; answer-token adaptive weight alpha=0.842 vs 0.252 function words (3.3x); selectivity AUROC 0.923
- **Ablation highlight:** Replacing adaptive alpha_t with fixed alpha=1.0 hurts EM most; removing any single signal (Opposition/Shift/Noise) lowers CF.

### HGU — Hallucination-Guided Unlearning: Using Hallucination Traces to Reveal Overfitted Memories
- **Venue/Year:** NeurIPS 2026
- **Benchmarks:** TOFU (forget01/05/10, plus SepS mixed-prompt protocol); MUSE; WMDP (Bio/Cyber/Chem + MMLU subsets Physics/Law/Economics); PKU-SafeRLHF
- **Baselines:** GA+GD/KL, NPO+GD/KL, DPO+GD/KL, IDK+GD, ULD, LLM-Eraser, RapidUn, RMU, FALCON, LUNAR, UNLEARN, Ethos
- **Key results:**
  - TOFU standard Avg: 0.7879 (forget01), 0.7221 (forget05), 0.7699 (forget10) — best across all three (vs next-best GA+GD 0.7469 forget10)
  - TOFU SepS H-Avg: 0.5497 / 0.4382 / 0.4715 — highest harmonic mean across splits
  - WMDP (Zephyr-7B): Forget 14.6 Physics / 15.3 Law / 14.2 Economics (vs RMU 27.0/27.8/27.3); Retain 37.2/48.9/52.7; MMLU 58.9/56.8/57.2 — strongest forgetting while preserving utility
- **Ablation highlight:** Channel intervention sensitivity shows traced-set channels cluster in high-hallucination-reduction / low-utility-drift region with p<10^-3.

### Agent-Native Memory Survey — Are We Ready For An Agent-Native Memory System?
- **Venue/Year:** arXiv preprint, Jun 2026 (Shanghai Jiao Tong + Tsinghua + MemTensor)
- **Benchmarks:** LoCoMo; LongMemEval (MemoryAgentBench); LifeLongAgentBench (DB-Bench); LongBench — 11 datasets across 5 workloads
- **Baselines:** Long Context, Embedding RAG; evaluates 12 memory systems: MemoChat, Mem0, MEM1, MemAgent, MemTree, Zep, Mem0^g, Cognee, LightMem, SimpleMem, MemOS, MemoryOS, A-MEM, Letta
- **Key results:**
  - LongMemEval: Zep best LLM Judge Accuracy 48.0; Cognee 35.3 ROUGE-L F1
  - LoCoMo: MemOS 11.5 EM; DB-Bench: Long Context 48.20 EM, MemoChat Task Success 55.40
  - LongMemEval Knowledge Update robustness: Zep 44.4 Substring EM / 36.8 ROUGE-L F1 (strongest)
  - LoCoMo backbone robustness (Answer F1 on Qwen3-8B / DeepSeek / GPT-5.4-mini / GPT-5.4): MemOS 32.2/41.2/38.6/41.2 (most stable)
- **Evaluation:** Systematic benchmarking study (not a new method). Core finding: no single architecture dominates; effectiveness depends on alignment between memory structure and workload bottleneck.

### CogitoRAG — Understand Then Memory: A Cognitive Gist-Driven RAG Framework with Global Semantic Diffusion
- **Venue/Year:** arXiv preprint v2, Mar 2026 (NUS, Tsinghua, NTU, BUPT)
- **Note:** `2026_Zhou_CogitoRAG.pdf` and `2026_Zhou_Li_Understand_Then_Memory_Cognitive_Gist_RAG_Framework.pdf` are the SAME paper (content-identical, same tables/figures, arXiv v2 Mar 2026).
- **Benchmarks:** NQ, PopQA, MuSiQue, 2WikiMultihopQA, HotpotQA, GraphBench (Novel + Medical, FR/CR/CS)
- **Baselines:** None (parametric only), NV-Embed-v2 (7B), GraphRAG, LightRAG, RAPTOR, HippoRAG, HippoRAG2, ToG2, ComoRAG
- **Key results:**
  - NQ: EM 51.55 / F1 63.76 vs HippoRAG2 43.40 / 60.00 (+8.15 EM)
  - PopQA: EM 50.94 / F1 59.94 vs ComoRAG 45.80 / 61.00
  - MuSiQue: EM 43.20 / F1 53.95 vs HippoRAG2 35.00 / 49.30 (+8.20 EM)
  - 2WikiMultiHopQA: EM 69.90 / F1 76.20 vs HippoRAG2 60.50 / 69.70 (+9.40 EM)
  - HotpotQA: EM 61.62 / F1 75.00 vs HippoRAG2 56.30 / 71.10
  - GraphBench Novel: FR 62.44 / CR 56.27 / CS 70.99 (best); Medical: FR 72.57 / CR 74.40 / CS 75.51 (best)
- **Ablation highlight:** MuSiQue: removing Entity Diffusion Module drops EM 43.2 → 35.0 (largest drop); removing CogniRank → 36.5; removing Query Decomposition → 41.7.

---

