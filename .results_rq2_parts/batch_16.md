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
