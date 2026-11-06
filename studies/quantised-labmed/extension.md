---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** Warner et al., Medmarks ([arXiv:2605.01417](https://arxiv.org/abs/2605.01417)). Its quantisation analysis (Section 3.10) covers **one 30B mixture-of-experts family** (Qwen3-30B-A3B Instruct/Thinking 2507) at BF16, FP8 and AWQ 8/4-bit, on H100s with vLLM. It reports win-rate changes only. It has no small dense models, no GGUF/llama.cpp or CPU runs, no QAT checkpoints (footnote 12 says the authors could not test them), no calibration, no memory or speed on consumer hardware, and no per-item analysis of which answers flip.
- **Closest prior work:**
  - [Twagirayezu & Mitra, arXiv 2609.22216](https://arxiv.org/abs/2609.22216) (September 2026): five 7–8B models (2024-era, including BioMistral, Meditron and Qwen2.5-7B) at FP16, GPTQ-INT8 and GPTQ-INT4 on MedQA, **MedMCQA**, **Med-HALT**, HealthBench and MedSafetyBench. INT8 was safe. INT4 losses depended on the model and were largest on MedMCQA, while Med-HALT was "largely unaffected". GPU GPTQ only; no calculations, no QAT, no GGUF/CPU, no calibration. **This already covers "does INT4 hurt MedMCQA and Med-HALT?" for older models.**
  - [MedPsy, arXiv 2611.02011](https://arxiv.org/abs/2611.02011) (November 2026): new 1.7B/4B medical models, with GGUF variants on laptop and smartphone. Q4_K_M stayed within 1 point of BF16 on its aggregate score. It tests only the authors' own models, and the abstract does not name MedCalc-Bench, MedHallu or MEDEC.
  - [Rasmussen & Qin, arXiv 2608.03854](https://arxiv.org/abs/2608.03854): calibration of FP16/INT8/INT4 Mistral-7B variants on medical-abstract sentence classification. They found the scoring rule can flip calibration conclusions. One task, not QA, not lab medicine.
  - [Lazem & Teahan, arXiv 2610.26937](https://arxiv.org/abs/2610.26937): a statistical certificate for when a quantised model may stand in for BF16, on 7–72B models with private clinical-verification decisions.
  - [Kim et al., arXiv 2609.24799](https://arxiv.org/abs/2609.24799): W4A4 PTQ can keep accuracy but weaken rationales on medical MCQ.
  - [Zhan et al., arXiv 2509.04534](https://arxiv.org/abs/2509.04534): 12 models on biomedical NER, relation extraction, classification and QA. Quantisation largely preserved performance.
- **Nothing found** on quantisation and MedCalc-Bench (numerical clinical calculations), MedHallu, MEDEC, QAT versus PTQ in medicine, or an Indian or LMIC laptop-deployment framing.

**Searches run on 2026-11-06:**
- **OpenAlex:** rate-limited (shared daily budget exhausted; no API key used), **not checked**.
- **Semantic Scholar** (citations of arXiv:2605.01417 and paper lookup): HTTP 429, rate-limited, **not checked**.
- **arXiv API** (3 successful calls, ≥6 s apart; a 4th was refused with "Rate exceeded"):
  1. `abs:quantization AND (abs:medical OR abs:clinical) AND abs:"language model"`, newest 60: the six papers above are the only relevant ones;
  2. id lookup of those six papers plus two others (abstracts read);
  3. `(quantization OR quantized OR GGUF OR 4-bit) AND (MedCalc OR MedHallu OR MEDEC OR Medmarks OR quantization-aware+medical)`: 10 results, all medical-imaging segmentation or classification. None on LLMs.
- **Europe PMC** (4 queries, newest 25 each): quantisation + LLM + medical + benchmark (2025–26); GGUF/llama.cpp/4-bit + clinical; quantisation + LMIC/India + clinical; quantisation + calibration/hallucination + clinical. Only a general survey of small medical LMs turned up (Comput Sci Rev 2026); no matching evaluation.
- **Web search** (3 queries): "quantized LLM MedCalc-Bench GGUF 4-bit"; "QAT versus PTQ medical LLM Gemma"; "quantization hallucination detection MedHallu Med-HALT llama.cpp". No study found. Only blog posts on Gemma QAT, with no medical tasks.
- **Inside this repo:** `find_dupes.py` matched only this study. Related studies:
  - `mpib-small-llm` tests whether quantisation changes **adversarial clinical harm under prompt injection** (MPIB). This study covers **benign accuracy, numerical calculation and hallucination**. The two share the same 2026 model panel and precisions on purpose, so their results can be read together. Neither duplicates the other.
  - `medmcqa-path` (prompt sensitivity and answer-order bias on MedMCQA pathology) and `medhallu-small` (small-model hallucination detection at full precision) use the same datasets. This study must not repeat their main questions: it uses MedMCQA and MedHallu only as quantisation outcomes.

### Gap 1: Numerical lab calculations under 4-bit quantisation

- **Evidence:** Medmarks Section 3.10 reports quantisation only as win-rate changes for one model. MedCalc-Bench was run once, with no tools (Section 3.3, footnote 6). Twagirayezu & Mitra have no calculation task. Lab calculations (anion gap, corrected calcium, eGFR, FENa, osmolality) are the most common arithmetic a pathologist or clinician would ask a local assistant to do, and arithmetic chains are where low-bit rounding is most likely to show.
- **Novelty check:** arXiv query 3 and web query 1 found no quantisation study on MedCalc-Bench. **Novel as of 2026-11-06.**
- **Open data:** `medcalc-bench`: 380 "lab test" items (19 calculators × 20), plus the other 720 items as a non-lab comparison.
- **Design sketch:**
  - *Hypothesis:* Q4 quantisation lowers accuracy more on multi-step equation calculators (delta ratio, albumin-corrected delta gap, FENa, CKD-EPI) than on rule-based scores. The loss is mainly arithmetic slips, not wrong formulas.
  - *Comparisons:* BF16 versus Q8_0 versus Q4_K_M versus QAT-Q4_0, paired on the same items, greedy decoding.
  - *Error types (Atul codes a stratified sample of flipped items):* wrong formula or units, wrong value pulled from the note, arithmetic slip, rounding, refusal or format failure.
  - *Secondary:* the same with the harness's calculator tool (`--add-calculator-tool`), to test whether a tool removes the quantisation penalty.
  - *Reporting guideline:* TRIPOD-LLM, plus MI-CLEAR-LLM items for model version, quantisation format, engine build and decoding.
- **Rating:** feasibility 5, novelty 4, RunPod, 2 weeks.

### Gap 2: QAT versus post-training quantisation at the same bit width

- **Evidence:** Medmarks footnote 12 expects QAT models to degrade less but could not test it. Google now publishes official QAT Q4_0 GGUFs for Gemma 4 (`google/gemma-4-E4B-it-qat-q4_0-gguf`, `google/gemma-4-12B-it-qat-q4_0-gguf`, Apache-2.0, not gated). ggml-org publishes ordinary post-training Q4_0 and Q8_0 GGUFs of the same models. That gives a clean natural experiment: same format and same size, with and without QAT. gpt-oss-20b ships natively in MXFP4 (12.1 GB GGUF), as a second QAT-style case.
- **Novelty check:** web query 2 and arXiv query 3 found no medical QAT-versus-PTQ comparison, only general blog claims about perplexity. **Novel as of 2026-11-06.**
- **Open data:** the full slice (`medcalc-bench`, `medmcqa`, `med-halt`, `medhallu`, `medec`).
- **Design sketch:** Gemma 4 E4B and 12B at BF16, PTQ Q8_0, PTQ Q4_0, QAT Q4_0 and PTQ Q4_K_M, on llama.cpp with one pinned build. Analysis: paired McNemar per dataset, plus a mixed-effects logistic model (item and model as random effects, precision × task as fixed effects). The key contrast is QAT-Q4_0 versus PTQ-Q4_0.
- **Rating:** feasibility 5, novelty 4, RunPod, 1 week on top of Gap 1.

### Gap 3: Small 2026 laptop models, real laptop hardware, cost in India

- **Evidence:** Medmarks ran everything on H100s and estimated cost at US$2 per H100-hour (Table 5). Its smallest models are 2025 releases (MedGemma 4B/1.5 4B, Gemma 3 4B, Qwen3 4B), and it reports no memory or speed figures. A district hospital or a pathologist's laptop in India runs on a CPU or Apple silicon, with 8–16 GB of RAM.
- **Novelty check:** MedPsy reports laptop and phone RAM for its own models. Twagirayezu & Mitra report GPU GPTQ only. No study pairs a lab-medicine slice with CPU tokens per second, peak RAM and cost per 1,000 questions across 2026 open models. **Partly novel** (the deployment framing is the new part).
- **Open data:** the full slice.
- **Design sketch:**
  - *Panel* (HF API, 2026-11-06):

    | Model | Licence | Gating | Why |
    | --- | --- | --- | --- |
    | Gemma 4 E4B-it, Gemma 4 12B-it | Apache-2.0 | not gated | official QAT Q4_0 available |
    | Qwen3.5-4B, Qwen3.5-9B | Apache-2.0 | not gated | strong small models; community GGUF (unsloth) |
    | Phi-4-mini-instruct | MIT | not gated | 3.8B baseline |
    | MedGemma 1.5 4B-it | Health AI Developer Foundations terms | auto | medical fine-tune; anchor to Medmarks |
    | gpt-oss-20b | Apache-2.0 | not gated | native MXFP4, fits 16 GB |

    Community GGUFs of MedGemma (unsloth) are not gated, but the HAI-DEF terms still apply.
  - *Hardware:* GPU runs for accuracy. A fixed 200-item timing subset on a real laptop (Atul's machine, CPU-only and Apple Metal, if available) and on a RunPod CPU pod, recording prompt and generation tokens per second, peak RAM and energy where measurable.
  - *Cost:* rupees per 1,000 questions, from laptop power draw and an Indian electricity tariff, against the cheapest API model in Medmarks Table 5.
- **Rating:** feasibility 4 (needs physical laptop timing runs), novelty 3, laptop + RunPod, 1.5 weeks.

### Gap 4: Does quantisation change hallucination and abstention, not just accuracy?

- **Evidence:** Medmarks reports MedHallu and Med-HALT as accuracy and win rate only. Twagirayezu & Mitra found Med-HALT "largely unaffected" by INT4, on older models, and did not use MedHallu's "unsure" option. MEDEC asks whether a model can spot an error in a clinical note, the reverse direction of hallucination. Rasmussen & Qin show that calibration conclusions can depend on the scoring rule.
- **Novelty check:** web query 3 and Europe PMC query 4 found nothing on quantisation with MedHallu or MEDEC. **Partly novel**: Med-HALT under INT4 is already covered.
- **Open data:** `medhallu` (2,000 items), `med-halt` (577 FCT + 577 NOTA lab items), `medec` (597 notes).
- **Design sketch:**
  - *Outcomes:*
    - MedHallu F1 and "unsure" rate;
    - MEDEC error-flag accuracy and error-sentence accuracy;
    - Med-HALT balanced accuracy;
    - expected calibration error and Brier score for multiple-choice items, from answer-letter log-probabilities (llama-server returns token probabilities);
    - a matched comparison on the same MedMCQA stems answered directly, as NOTA and as FCT. **Med-HALT reuses MedMCQA stems, so this is a within-question test of whether 4-bit models confidently endorse wrong answers more often.**
- **Rating:** feasibility 5, novelty 3, RunPod, 1 week.

### Gap 5: A pathologist's error taxonomy of answers that flip under quantisation

- **Evidence:** no study in the novelty check looks at *which* items change between BF16 and 4-bit, or why. Medmarks' own physician review (Appendix P) found poor items in MedMCQA, so some apparent quantisation losses may sit on broken items.
- **Novelty check:** none of the papers found does an expert, item-level analysis of quantisation flips. **Novel**, but small on its own.
- **Design sketch:** Atul reviews every BF16-correct → Q4-wrong and Q4-correct → BF16-wrong item in the MedMCQA pathology and MedCalc lab subsets (expected to be a few hundred items). He codes them as knowledge loss, reasoning or arithmetic slip, format failure, or broken item/key, and separately audits the 337 pathology answer keys. Report net flips with and without broken items.
- **Rating:** feasibility 5, novelty 3, laptop (expert time), 1 week.

### Gap 6 (not recommended): retrain or fine-tune to recover the 4-bit loss

- **Evidence:** Medmarks-T (Section 3.12) offers RL environments, and Twagirayezu & Mitra tried QLoRA recovery.
- **Why not:** it needs much more compute and moves away from the deployment question. Recovery has already been tried, with mixed results. Novelty 2, feasibility 3.

## Recommended extension

**Gaps 1 + 2 + 3 together, with 4 and 5 as secondary analyses:** "Is a 4-bit model on a laptop safe for lab-medicine questions? Paired BF16 versus Q8/Q4 versus quantisation-aware Q4 evaluation of 2026 small open LLMs on a pathology and lab slice of Medmarks, with laptop speed, memory and cost for Indian deployment."

Why this one:
- **It fixes the old premise and targets the real gaps.** Medmarks did test quantisation, but only on one 30B model on H100s. The parts that remain open are numerical lab calculations under quantisation (Gap 1), QAT versus PTQ at the same format (Gap 2, which the authors explicitly could not test), and real laptop deployment (Gap 3). Twagirayezu & Mitra already showed INT4 hurts MedMCQA on older 7–8B models. This study builds on that rather than repeating it.
- **Fully open and cheap:**
  - every dataset is open and not gated;
  - six of the seven models are Apache-2.0 or MIT and not gated (MedGemma is auto-gated);
  - about 30–50 GPU-h on RunPod plus laptop timing, with no paid API.
- **Good fit for Atul (4/5).** The slice is his own field: anion gap, corrected calcium, eGFR and FENa calculators, and MedMCQA pathology, biochemistry and microbiology. His expert work, the flip taxonomy (Gap 5) and the pathology key audit, is what makes it more than a benchmark run.
- **A useful answer either way.** If QAT-Q4 matches BF16 on lab calculations, a hospital or teaching department can run a 5 GB model on an ordinary laptop with confidence. If calculations break at 4-bit while MCQ accuracy holds, that is a concrete safety warning for local deployment.
- **Clearly different from `mpib-small-llm`.** That study tests adversarial harm; this one tests benign accuracy and hallucination. Using the same model panel and precisions lets both papers cite each other.

**Main risks:**
- Quantisation effects may be smaller than the confidence intervals. Mitigations: paired greedy runs, all 380 lab calculations (plus 720 non-lab calculations), and a mixed-effects model across tasks.
- Chat-template and engine differences can look like quantisation effects. Mitigation: one engine per comparison, and template checks.

Expected time: about 6 weeks to an arXiv (cs.CL) or medRxiv preprint. Candidate zero-APC journals:
- Journal of Medical Systems (subscription route);
- International Journal of Medical Informatics (free route: verify);
- Journal of Biomedical Informatics (free route: verify).
