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
