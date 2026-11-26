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
