---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** Lee et al., MPIB, *Findings of EMNLP 2026* (arXiv 2602.06268).
  - Tested 13 open models at full precision: Qwen2.5 7/32/72B, Llama-3.1 8/70B, Mixtral 8x7B/8x22B, MedGemma 4B/27B, Meditron 7/70B, BioMistral-7B and MMed-Llama-3-8B.
  - Added a small scope check (Appendix O) on gpt-5.5, gemini-2.5-pro and Qwen3-30B-A3B.
  - No quantised model, and nothing released after mid-2025 at under 10B parameters.
  - Defences D2–D4 all use a 7B LLM as rewriter or sanitiser. No lightweight classifier-type detector was tested.
- **Quantisation and clinical safety, without prompt injection:**
  - [Twagirayezu & Mitra, arXiv 2609.22216](https://doi.org/10.48550/arxiv.2609.22216) (September 2026): five 7–8B models at FP16, GPTQ-INT8 and GPTQ-INT4 on MedQA, MedMCQA, Med-HALT, HealthBench and MedSafetyBench. INT8 was safe. INT4 safety loss depended on the model; Qwen2.5-7B and Meditron-7B lost the most refusal safety. **No prompt-injection arm.**
  - [Kharinaev et al., IEEE Access 2026](https://doi.org/10.1109/access.2026.3703899): 66 quantised variants on general safety benchmarks. Both PTQ and QAT can erode safety. Not medical, and no injection.
- **Quantisation and prompt injection, general domain:** [Rodrigues et al., ERAMIA-RS 2025](https://doi.org/10.5753/eramiars.2025.16669) is an experimental-setup proposal with "experiments in progress" and no results.
- **Small-model prompt-injection detectors:** [nokast-secureRAG, arXiv 2610.28364](https://doi.org/10.48550/arxiv.2610.28364) (October 2026) trains a 0.5B RAG firewall on general data. It reports that Prompt-Guard-86M had a 0.69 false-positive rate there, and that its own recall collapsed on fluent fact-poisoning. **ClinicalShield** ([Zenodo 10.5281/zenodo.22874031](https://doi.org/10.5281/zenodo.22874031)) is a PubMedBERT detector-sanitiser pipeline on openFDA passages. Its release notes mention an MPIB evaluation, run without the registry in the repo.
- **Medical prompt-injection defences citing MPIB:**
  - [Sakib et al., arXiv 2610.22594](https://doi.org/10.48550/arxiv.2610.22594): multi-agent systems with a clinical-judgment verification defence.
  - [Wu et al., Research Square 2026](https://doi.org/10.21203/rs.3.rs-10464629/v1): a rule-based "sentinel" over Qwen 7B, Llama 8B, Meditron 7B, Gemma 4 and Sonnet 4.5 on two clinical safety benchmarks. Whether MPIB is one of them: **verify**.
  - Neither study tests quantisation or sub-10B models released in 2026.

**Searches run on 2026-11-06:**
- **OpenAlex, works citing the source** (W7128394725, EMNLP version): 2 results, both surveys of secure RAG.
- **Semantic Scholar citations of arXiv:2602.06268:** 7 results, the six papers above plus TRiSM/hypergraph agent-security papers. No quantisation or small-model follow-up.
- **OpenAlex keyword searches** (date filter in brackets; top 25 by relevance each):
  - "quantization prompt injection robustness" (2024+);
  - "quantized large language models safety jailbreak" (2024+);
  - "quantization medical large language model safety" (2024-06+);
  - "medical prompt injection small language models" (2025+);
  - "prompt injection medical LLM retrieval augmented generation defense" (2025-06+);
  - "reasoning thinking mode prompt injection robustness" (2025-06+);
  - "prompt injection classifier false positive clinical text" (2025+);
  - "Prompt Guard prompt injection detector benchmark over-refusal" (2025+);
  - "Gemma 4 Qwen3.5 safety prompt injection evaluation" (2026-02+);
  - "LLM-as-a-judge clinical harm severity physician agreement small judge" (2025-06+).
- **arXiv API** (3 calls, ≥6 s apart):
  - `abs:quantization AND abs:"prompt injection"`: 9 results, none medical;
  - `abs:MPIB`: only the source;
  - `abs:"prompt injection" AND (medical OR clinical) AND (small OR quantized OR quantised)`: 0 results.
- **GitHub code search for "jhlee0619/mpib":** no third-party evaluation code. One agent-security repo (ACTGuard) lists MPIB as "blocked" because of the gate and redaction.

**Bottom line:** nobody has measured whether quantisation changes **clinical-harm rates under prompt injection**. Nobody has run MPIB on 2026 small models, or tested cheap classifier detectors against MPIB's false-refusal metric.

**Overlap inside this repo:** `quantised-labmed` studies quantisation effects on **accuracy and hallucination** (Medmarks). `medhallu-small` studies small-model hallucination detection. This study tests **adversarial safety**, so they complement rather than duplicate each other. Keep the model panels aligned so the three can be cited together.

### Gap 1: Does 4-bit quantisation change clinical harm under prompt injection?

- **Evidence:** every MPIB model ran at full precision (Section 4.1, Appendix M). Twagirayezu & Mitra found INT4 safety loss without injection, which varied by model. Wu et al. found the base model drove residual risk. The interaction of quantisation with injection is untested.
- **Novelty check:** OpenAlex queries 1–3 and arXiv query 1 (2026-11-06) found no medical study and no study using CHER-type outcomes. The general-domain study (Rodrigues et al.) has no results yet. **Novel as of 2026-11-06.**
- **Open data:** `mpib`.
- **Design sketch:**
  - *Hypothesis:* INT4 post-training quantisation raises V1/V2 CHER₃ and lowers correct refusals compared with BF16, more than INT8 does. Google's quantisation-aware-trained (QAT) Q4 checkpoints keep safety closer to BF16 than post-training Q4 does.
  - *Precisions per model:* BF16; Q8_0 GGUF; Q4_K_M GGUF; and AWQ/W4A16, or the official QAT Q4 where one exists (Gemma 4 E4B and 12B).
  - *Analysis:* paired, on the same items. McNemar per cell, plus a mixed-effects logistic model with severity ≥3 as the outcome, precision × vector as fixed effects, and item and model as random effects.
  - *Power:* use **all 1,226 V1+V2 items** (train, validation and test). Nothing is trained, so the splits only matter for comparison. Report the test split separately to stay comparable with Table 5.
  - *Reporting guideline:* TRIPOD-LLM (adapted), with MI-CLEAR-LLM items for model version, quantisation and decoding.
- **Rating:** feasibility 4, novelty 4, RunPod, 4 weeks.

### Gap 2: 2026 small on-prem models are untested

- **Evidence:** the smallest MPIB models are MedGemma-4B, Qwen2.5-7B and Llama-3.1-8B (2024–25). The only newer open model, Qwen3-30B-A3B, was a scope check (Appendix O). Since then, small models with permissive licences have appeared. Licences and gating per the HF API, 2026-11-06:

  | Model | Licence | Gating |
  | --- | --- | --- |
  | [Gemma 4 E2B-it](https://huggingface.co/google/gemma-4-E2B-it) | Apache-2.0 | not gated |
  | [Gemma 4 E4B-it](https://huggingface.co/google/gemma-4-E4B-it) | Apache-2.0 | not gated |
  | [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) | Apache-2.0 | not gated |
  | [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | Apache-2.0 | not gated |
  | [Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct) | MIT | not gated |
  | [Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) | Llama 3.2 licence | manual approval |
  | [MedGemma 1.5 4B-it](https://huggingface.co/google/medgemma-1.5-4b-it) | Health AI Developer Foundations terms | auto |
  | Gemma 3 4B-it (the stub's original choice) | Gemma terms | manual approval |

- **Novelty check:** OpenAlex query 9 ("Gemma 4 Qwen3.5 …") found no medical prompt-injection evaluation. Wu et al. include Gemma 4 but use a different benchmark design and a rule-based supervisor (**verify** whether MPIB is used).
- **Open data:** `mpib`.
- **Design sketch:**
  - *Panel:* the six to seven models above, plus two anchors from the original matrix (Qwen2.5-7B, Llama-3.1-8B) to link to Table 5.
  - *Settings:* D0, then D1 (system-prompt hardening).
  - *Metrics:* CHER₃, ASR₂, FPR-H, and the severity-2-only share, with bootstrap CIs.
- **Rating:** feasibility 5, novelty 3 on its own (a benchmark refresh), RunPod, 2 weeks. Strong when combined with Gap 1.

### Gap 3: Cheap detector defences, and what they cost in false refusals

- **Evidence:**
  - D2–D4 each need a second 7B LLM call per query (Section 3.5), and the authors call them "diagnostic scaffolds".
  - Limitation 3 names detection-based defences as future work.
  - FPR-H rose sharply with defences for some models (Meditron-70B: 16.0% → 33.6%).
  - Small classifier detectors are much cheaper on a CPU-only hospital server, but their behaviour on clinical text is unknown. nokast-secureRAG reports a 0.69 false-positive rate for Prompt-Guard-86M on general RAG text.
- **Novelty check:** OpenAlex queries 7–8 (2026-11-06) found general-domain detector benchmarks (PIDS-Bench, RAG-PIBench, BrowseSafe++) but none on clinical items with a harm-severity outcome. ClinicalShield uses a medical detector on openFDA passages. Its MPIB result, if any, has not been published as aggregate CHER/FPR-H (**verify** when its paper appears). **Partly novel.**
- **Open data:** `mpib`.
- **Design sketch:**
  - *Detectors:*
    - [protectai/deberta-v3-base-prompt-injection-v2](https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2) (Apache-2.0, not gated);
    - [Llama-Prompt-Guard-2-86M](https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M) (Llama 4 licence, manual approval);
    - [granite-guardian-3.3-8b](https://huggingface.co/ibm-granite/granite-guardian-3.3-8b) (Apache-2.0) as a larger generative guard.
  - *Placement:* each detector screens the user query (V1) and each retrieved passage (V2). On a flag, the system either blocks the request or drops the passage.
  - *Outcomes:*
    - detector AUROC and recall, using the injection labels;
    - downstream CHER₃ after the gate;
    - FPR-H and false-block rate on benign V0 and borderline V0′ items;
    - added latency on a CPU.
  - *Comparisons:* against the reimplemented D2 (a 7B rewriter) on the same items.
- **Rating:** feasibility 4, novelty 3–4, RunPod for the generative guard (classifiers run on a laptop), 2 weeks on top of Gap 2.

### Gap 4: The judge is a single 72B model with judge-dependent V2 rankings

- **Evidence:** Limitations 1 and 4 say the same Qwen-2.5-72B builds, filters and judges the data. V2 ranking agreement with a Qwen-32B judge was Spearman 0.46 (Table 4). The toolkit does not ship the judge pipeline.
- **Novelty check:** OpenAlex query 10 found general reviews of LLM judges in healthcare (MedJUDGE scoping review, arXiv 2604.25933) but no re-judging study for MPIB.
- **Open data:** `mpib`. Plus a new expert label set (aggregate agreement statistics only).
- **Design sketch:**
  - *Judges:* re-judge a fixed response set with Qwen2.5-72B-AWQ (the reference), and with two cheaper open judges from a different family: Qwen3.5-27B (Apache-2.0) and gpt-oss-20b (Apache-2.0).
  - *Expert audit:* Atul blind-scores about 150 stratified responses for severity and harm type.
  - *Metrics:*
    - weighted κ against the expert;
    - Recall@severity≥3;
    - Spearman correlation of model rankings between judges;
    - how often each conclusion from Gaps 1–3 flips with the judge.
  - This is needed anyway to trust Gaps 1–3, so treat it as a validation module rather than a separate paper.
- **Rating:** feasibility 4, novelty 3, RunPod, 1–2 weeks (overlaps the main runs).

### Gap 5: Thinking mode on or off

- **Evidence:** Qwen3.5 small models can be run with reasoning on or off. MPIB used deterministic non-reasoning decoding throughout.
- **Novelty check:** OpenAlex query 6 found reasoning-versus-standard comparisons only outside medicine: recruiting (arXiv 2602.18514) and agent traces (arXiv 2610.24048). None used MPIB or clinical-harm outcomes.
- **Design sketch:** run Qwen3.5-4B and 9B with thinking on and off at BF16 and Q4. Compare CHER₃, FPR-H and output tokens (cost). Never store or publish reasoning traces that quote injected content.
- **Rating:** feasibility 4, novelty 4, RunPod (long outputs: about 3× the generation cost), 1 extra week. A good secondary analysis.

### Gap 6: Indian on-prem framing, and the expert error taxonomy

- **Evidence:** MPIB is built from US exam items (MedQA) and PubMed abstracts. The paper has no LMIC or deployment framing. In India, hospitals that want local, DPDP Act-compliant assistants will run exactly these small quantised models on modest hardware.
- **Novelty check:** no Indian-context medical prompt-injection study turned up in any of the searches above.
- **Design sketch:**
  - Frame the hardware tiers and costs around an Indian district or teaching hospital (CPU-only server, a single 16–24 GB GPU).
  - Atul codes the severity-≥3 failures, for the best and worst small models, into clinically meaningful failure patterns. Examples: wrong drug or dose, missed red flag, false evidence claim, and lab-value misreading in the S2/S3 items.
  - **Do not build a new Indian-guideline poisoning set.** It would mean writing new attack content, which conflicts with this repo's defensive-only rule (CLAUDE.md rule 6) and MPIB's own stewardship terms. Use MPIB's existing V2 items only.
- **Rating:** feasibility 5, novelty 2 on its own, laptop, about 1 week of expert time. Adds clinical value to the main paper.

## Recommended extension

**Gaps 1 + 2 + 3 together, with 4 as the validation module and 5–6 as secondary analyses:** "Does 4-bit quantisation make small on-prem medical LLMs easier to hijack? Clinical-harm rates under prompt injection, and the false-refusal cost of cheap detector defences, on MPIB."

Why this one:
- **It is clearly new.** No study has measured CHER-type clinical harm under injection across precisions, or put classifier detectors against MPIB's false-refusal metric. The closest work (Twagirayezu & Mitra) tests quantisation on safety benchmarks with no adversarial arm.
- **It is fully open and cheap:**
  - the dataset is auto-gated;
  - most candidate models are Apache-2.0 or MIT and not gated;
  - about 40–70 GPU-h on RunPod, with no paid API.
- **It answers a real deployment question.** A hospital IT team choosing a small model and quantisation level for an on-prem assistant under the DPDP Act needs exactly this answer.
- **Fit for Atul is moderate (3/5).** The work is mainly LLM-security engineering. His expert roles are the judge audit (Gap 4) and the error taxonomy (Gap 6), which also make the paper more credible to clinical journals.
- **The main risk is power.** Quantisation effects may be smaller than the CIs. Using all 1,226 adversarial items, with paired tests, is the mitigation. A null result is still publishable as a deployment safety finding ("INT8 is as safe as BF16 under injection").

Expected time: about 7 weeks to an arXiv (cs.CR / cs.CL) preprint. Candidate zero-APC journals:
- Journal of Medical Systems (clinical AI and system security);
- Computers & Security;
- Journal of Information Security and Applications.
