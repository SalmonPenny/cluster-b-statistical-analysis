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
