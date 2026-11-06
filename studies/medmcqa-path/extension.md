---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** Sadanandan and Behzadan, [arXiv:2603.25960](https://arxiv.org/abs/2603.25960). It tests **one model family** (MedGemma 4B and 27B). It reports accuracy over all 21 MedMCQA subjects pooled, with no per-subject results and no human check of the items. Its own Discussion names two limits: other models are untested (Section 5.7), and a clinical severity taxonomy of prompt-induced errors was left out of scope. Reading the code adds a third: the answer parser takes the first A–D character anywhere in the output, so the CoT, few-shot and position-bias numbers may be partly parsing artefacts (see `replication.md`, Known pitfalls).
- **Closest prior work on answer order and prompt sensitivity:**
  - **Medmarks** ([arXiv:2605.01417](https://arxiv.org/abs/2605.01417), May 2026; already in this repo as `medmarks`). It runs 61 models and reports that small models are the most sensitive to answer order. Its MedMCQA environment has a `--shuffle-answers` option (environment README, GitHub, 2026-11-06). **Multi-model answer-order sensitivity on MedMCQA as a whole is therefore no longer new.** Exactly how Medmarks measured order effects (which datasets, how many shuffles) is **verify**; the repo's `quantised-labmed` entry summarises it.
  - **Prompt sensitivity of small open models for clinical QA in low-resource settings** ([arXiv:2603.00917](https://arxiv.org/abs/2603.00917), March 2026, v1–v3 with different model lists). Five small open models, five prompt styles, MedQA, MedMCQA and PubMedQA, run on a consumer CPU. Consistency and accuracy turned out to be largely independent. It changes prompt wording, not option order, and has no item audit. Read from the abstract via web search only (**verify** details).
  - **Prompt-variation sensitivity in healthcare LLMs** ([arXiv:2606.07237](https://arxiv.org/abs/2606.07237), June 2026). Lexical and syntactic perturbations on MedMCQA for GPT-3.5, Llama 3 and BERT-family models. Older models, no option-order permutation, no subject slice (abstract-level only, **verify**).
  - **Polish medical exams re-assessed** ([arXiv:2606.12250](https://arxiv.org/abs/2606.12250), 2026). Six physicians annotated 200 items per exam set to separate true competence from bias-driven performance, and they discarded invalid items. This is the closest design precedent for expert adjudication, but it uses a different exam and has no permutation consensus (abstract-level only).
  - **Methods:** Zheng et al., *Large Language Models Are Not Robust Multiple Choice Selectors* ([arXiv:2309.03882](https://arxiv.org/abs/2309.03882), ICLR 2024), on token-level selection bias and PriDe debiasing. Tamba, *Position Bias is Hidden Behind Ceiling Effects* ([arXiv:2607.20864](https://arxiv.org/abs/2607.20864), July 2026), on exhaustive permutations with chi-squared/Cramér's V, showing bias is only measurable between about 60% and 95% accuracy (MMLU, not medical). Guided Permutation Scoring ([Findings of EMNLP 2026](https://doi.org/10.18653/2026.findings-emnlp.1290)). *Right Answer, Wrong Score* ([Findings of ACL 2025](https://doi.org/10.18653/v1/2025.findings-acl.950)), on answer-extraction errors in MCQ evaluation, which is exactly the source's parser problem.
  - **Medical answer position:** Gupta and Chong, *Answer Positioning Biases in LLM Responses to Medical MCQs* ([SIIM 2024 abstract](https://siim.org/wp-content/uploads/2024/08/Answer-Positioning-Biases_Gupta.pdf); MedQA, four repositionings). A knowledge-graph distractor paper ([arXiv:2506.00612](https://arxiv.org/abs/2506.00612)) found shuffling changed MedMCQA-style accuracy by under 1 point for its models, which contradicts the source's 20–27 point drops.
- **Closest prior work on answer keys and item quality:**
  - MedQA was relabelled by clinicians for Med-Gemini ([Google-Health/med-gemini-medqa-relabelling](https://github.com/Google-Health/med-gemini-medqa-relabelling)).
  - MMLU-Redux re-annotated MMLU with a two-level error taxonomy, separating unclear questions from wrong keys ([arXiv:2406.04127](https://arxiv.org/abs/2406.04127)).
  - Medmarks Appendix P (physician review) found unclear or wrong MedMCQA items, but did not audit a subject slice systematically.
  - A Brazilian ENAMED 2026 study (JMIR Medical Education, per web search; citation **verify**) reported that frontier-model consensus flagged one inconsistent official key.
  - **No MedMCQA re-annotation, pathology answer-key audit, or validated "model consensus finds wrong keys" study was found.**
- **Pathology-specific LLM MCQ work** is older and uses other question banks: Koga, ChatGPT vs Bard on 150 pathology board-style questions ([medRxiv 2023](https://doi.org/10.1101/2023.08.03.23293401)), and a medRxiv comparison with pathology trainees ([doi:10.1101/2024.07.10.24310093](https://doi.org/10.1101/2024.07.10.24310093)). Neither looks at prompt or order robustness, or at MedMCQA.

**Searches run on 2026-11-06:**
- **OpenAlex:** refused (shared free daily budget used up, no key). **Not checked.**
- **Semantic Scholar** keyword search: HTTP 429. **Not checked.**
- **arXiv:** the export API returned "Rate exceeded" twice (metadata fetch and a search for `abs:MedMCQA AND (permutation OR order OR position OR shuffl* OR robustness OR sensitivity OR consistency)`). Two arXiv web pages were read: the source abstract page and 2607.20864. Budget of four calls reached. **arXiv listing search not checked.**
- **Crossref** (from 2024-06-01, top 25 each), used in place of OpenAlex:
  - "MedMCQA option order position bias permutation";
  - "medical multiple choice LLM answer order sensitivity shuffling";
  - "MedMCQA prompt sensitivity chain-of-thought";
  - "pathology multiple choice questions large language model accuracy error analysis";
  - "MedMCQA answer key errors label noise audit";
  - "cloze scoring log-probability multiple choice medical LLM";
  - "MedMCQA subject-wise performance pathology microbiology biochemistry".

  Relevant hits: the source's Research Square version, GPS, *Right Answer, Wrong Score*, the SIIM/SSRN answer-position abstract, a 2025 comparison of CoT prompting methods for medical QA (Computers in Biology and Medicine, [doi:10.1016/j.compbiomed.2025.110614](https://doi.org/10.1016/j.compbiomed.2025.110614)), and the pathology-trainee preprint.
- **Europe PMC** (2024-06-01 to 2026-11-06, top 25 each):
  - `"MedMCQA"` (172 hits; titles read);
  - LLM + option/answer order or position/selection bias + medical;
  - LLM + pathology + MCQ + error/taxonomy;
  - permutation/shuffle + LLM + medical exam;
  - NEET-PG/AIIMS/FMGE/INI-CET + LLM;
  - answer key/flawed items/label errors + LLM + medical benchmark.

  Nothing matched a MedMCQA pathology audit or permutation-consensus key check. Adjacent work: confidence and abstention in small models on psychiatric questions (Research Square 2026), sycophancy and diagnostic instability (Artif Intell Med 2026), and NEET-PG ChatGPT comparisons (Cureus 2024).
- **Web search** (7 queries): MedMCQA shuffling/permutation robustness 2026; pathology MedMCQA subject-wise error analysis and key audit; MedMCQA label errors and relabelling; multi-model prompt-sensitivity flip rates; MedMCQA redux/cleaned subset; LLM consensus to detect wrong answer keys; the source's proceedings venue. Found 2603.00917, 2606.07237, 2606.12250, 2607.20864, MMLU-Redux, the Med-Gemini MedQA relabelling and the ENAMED consensus report. No MedMCQA key audit was found.
- **Not confirmed:** the register stub cited "arXiv 2604.10535" (repeated-sampling consistency). A web search did not find it and arXiv could not be queried, so it is not used here (**verify**).
- **Inside this repo:** `find_dupes.py` matched only this study. Related study: `quantised-labmed` (same dataset). See the comparison below.

**How this study differs from its two siblings:**
- `quantised-labmed` asks whether **4-bit quantisation** changes answers. It uses the same 630 MedMCQA lab-slice items, but only as one outcome among five datasets, with fixed prompts and original option order.
- `medhallu-small` asks whether small models can **detect hallucinated answers** (MedHallu/PubMedQA) under retrieval.
- This study asks **whether the item or the model is at fault**. It looks at prompt format, option order and answer extraction on pathology, microbiology and biochemistry items, all at full precision, with a pathologist auditing the answer keys and item flaws.
- Shared pieces should be reused, not repeated: the slice ids, the 2026 model panel (keep it aligned with `quantised-labmed` and `mpib-small-llm`), and Atul's pathology key audit. `quantised-labmed` Gap 5 plans the same key audit, so do it once (here) and cite it there.

### Gap 1: One model family, and a parser that may drive the headline effects

- **Evidence:** only MedGemma is tested (Sections 3.1 and 5.7). The parser returns the first A–D character in the output (`src/evaluation/metrics.py`, `parse_mcq_answer`). CoT is capped at 256 tokens (Table 1), and the worked example was truncated. Unexplained mismatches remain: the distractor-swap drop is −8.9 points in the text but 0.0 in Table 6, and the 27B and voting results use 1,000-item subsets.
- **Novelty check:** Medmarks already covers many models with order shuffling, and 2603.00917 covers prompt styles on small models. A **re-analysis with a strict parser** showing how much of "CoT backfires" survives is not published (Crossref, Europe PMC and web searches). **Partly novel**: a strong methods note, thin as a paper on its own.
- **Open data:** `medmcqa` (full validation split plus the 630-item slice).
- **Design sketch:** run MedGemma-4B/27B with the source code. Re-score the raw outputs with the original and with a strict parser. Re-run CoT with a 2,048-token budget and final-answer extraction. Report how much of each headline effect remains. Reporting guideline: TRIPOD-LLM plus MI-CLEAR-LLM items for prompts, decoding and parsing.
- **Rating:** feasibility 5, novelty 3, RunPod, 1–2 weeks. **Folded into the recommended study as its first module.**

### Gap 2: No pathologist audit of the answer keys or item quality

- **Evidence:** MedMCQA keys are known to be noisy (Medmarks Appendix P). The source treats every key as correct, so a wrong key counts a correct model as wrong under every prompt and ordering. Its Discussion leaves a clinical severity taxonomy out of scope. The 630-item slice contains item types that make "correct" ambiguous: 175 `multi` items, 129 negative stems, and 43 with "all/none of the above"-type options (aggregate counts, `replication.md`).
- **Novelty check:** Crossref "MedMCQA answer key errors label noise audit", Europe PMC answer-key/flawed-item queries, and web searches for MedMCQA relabelling or redux all came up empty. Precedents exist for MedQA (Med-Gemini relabelling) and MMLU (MMLU-Redux), not for MedMCQA or Indian entrance-exam pathology. **Novel as of 2026-11-06** (OpenAlex, Semantic Scholar and arXiv listings not checked).
- **Open data:** `medmcqa` (630 slice items; the dataset's own explanations exist for 338 of them).
- **Design sketch:**
  - Atul rates every item using an MMLU-Redux-style taxonomy:
    - key correct;
    - key wrong (with the correct option);
    - more than one defensible answer;
    - no defensible answer;
    - outdated by current guidelines or nomenclature (for example WHO tumour classification updates);
    - unclear stem;
    - position-anchored or multi-statement format;
    - needs a missing image or table.
  - A second pathologist or microbiologist/biochemist re-rates a stratified 30% (about 190 items) blind. Report Cohen's kappa.
  - Release only item ids and audit labels (MedMCQA is Apache-2.0/MIT), in the study's own repo or on Zenodo, not in this catalogue.
- **Rating:** feasibility 4 (about 20–25 hours of expert time plus a second rater), novelty 4, laptop, 2 weeks.

### Gap 3: Order sensitivity is measured with permutations that break some items, and never by item type

- **Evidence:** the source's shuffler moves every option, including "all of the above"-type options (43 slice items, 335 in the full split). Its random shuffle uses a single seed in Table 6, and it reports flip rates without separating flawed items from sound ones. Tamba (2607.20864) shows that one shuffle confounds bias with noise and recommends exhaustive permutations.
- **Novelty check:** Medmarks shuffles answers, and GPS, PriDe and Tamba propose permutation methods, but none of the papers found restricts permutations to keep anchored options in place. None asks whether order flips concentrate in items an expert judges ambiguous or wrongly keyed. **Partly novel**: the method is known, the item-quality link is new.
- **Open data:** `medmcqa` slice plus the Gap 2 labels.
- **Design sketch:**
  - All 24 orderings per item. For anchored items, permute only the free options (6 orderings).
  - Per item and model: flip rate, Cramér's V for position preference, and order-invariant accuracy (correct under every ordering).
  - Mixed-effects logistic model: correct ~ item-flaw class × ordering + (1 | item) + (1 | model).
  - *Hypothesis:* items with ambiguous or wrong keys account for a disproportionate share of flips. If so, "position bias" estimated on noisy benchmarks is inflated.
- **Rating:** feasibility 5, novelty 4, RunPod, 1 week.

### Gap 4: Permutation consensus as a flag for wrong keys and as an abstention signal

- **Evidence:** the source proposes the cross-ordering agreement rate (70%) as "a calibrated abstention signal" (Section 5.6), but never tests calibration. Model consensus has flagged single wrong keys (ENAMED report), but no detection rate has been measured against expert labels.
- **Novelty check:** web search "LLM consensus disagreement to detect wrong answer keys", Europe PMC answer-key queries and Crossref audit queries found single-item anecdotes and adjacent "disagreement predicts model error" work (JMIR AI preprint 2026, on other datasets). No study scores consensus against expert-adjudicated keys. **Novel as of 2026-11-06.**
- **Open data:** `medmcqa` slice plus the Gap 2 labels as the reference standard.
- **Design sketch:**
  - *Key-error detector:* per item, the share of (model × ordering) votes that disagree with the key, and cloze-probability mass on non-key options. AUROC and precision at fixed review budgets (top 5%, 10%, 20%) against Atul's "key wrong or ambiguous" label. Report as a diagnostic-accuracy study (STARD-style items) alongside TRIPOD-LLM.
  - *Abstention:* risk-coverage curves and AURC for permutation agreement, cloze margin and verbalised confidence, per model. Score these on the original keys and on the corrected keys.
  - *Re-ranking:* how model rankings and accuracy change once the keys are corrected.
- **Rating:** feasibility 5, novelty 4, RunPod, 1 week on top of Gaps 2–3.

### Gap 5: Cloze versus generation across 2026 thinking models, on a subject slice

- **Evidence:** the source's cloze result for 27B (64.5%) uses 1,000 items, and only MedGemma was tested. The cloze advantage may simply reflect the parser problem in Gap 1. Thinking models (Qwen3.5, gpt-oss, Gemma 4) put the answer after long reasoning, where first-token cloze is undefined.
- **Novelty check:** the Crossref query "cloze scoring log-probability multiple choice medical LLM" found only confidence-estimation papers. Medmarks does generation only (environment README). **Partly novel.**
- **Open data:** `medmcqa` slice.
- **Design sketch:** compare cloze (letter log-probability after a fixed "Answer:" prefix, thinking disabled), direct generation, and thinking-mode generation for every model. Report the cloze–generation gap per subject and per item-flaw class.
- **Rating:** feasibility 5, novelty 3, RunPod, 0.5 week. **Secondary analysis.**

### Gap 6 (not recommended here): PubMedQA context truncation

- **Evidence:** the source's largest single effect (front versus back truncation, Appendix E).
- **Why not:** it is not pathology, and retrieval-quality effects sit closer to `medhallu-small`. Novelty 2 for this catalogue.

## Recommended extension

**Gaps 2 + 3 + 4, built on a corrected Gap 1 and with Gap 5 as a secondary analysis:** "Wrong key or wrong model? A pathologist-adjudicated, order-robust re-evaluation of the 630 MedMCQA pathology, microbiology and biochemistry items across 2026 open-weight LLMs, with permutation consensus tested as a detector of faulty answer keys and as an abstention signal."

**Model panel** (HF API, 2026-11-06; all run at BF16 on vLLM, greedy decoding, strict parser):

| Model | Licence | Gating | Role |
| --- | --- | --- | --- |
| `google/medgemma-4b-it`, `google/medgemma-27b-text-it` | Health AI Developer Foundations terms | auto | anchors to the source |
| `google/medgemma-1.5-4b-it` | Health AI Developer Foundations terms | auto | current medical small model |
| `google/gemma-4-E4B-it`, `google/gemma-4-12B-it`, `google/gemma-4-31B-it` | Apache-2.0 | not gated | general 2026 family, three sizes |
| `Qwen/Qwen3.5-4B`, `Qwen/Qwen3.5-9B`, `Qwen/Qwen3.5-27B` | Apache-2.0 | not gated | thinking toggle, three sizes |
| `microsoft/Phi-4-mini-instruct` | MIT | not gated | small baseline |
| `openai/gpt-oss-20b` (optionally `gpt-oss-120b`) | Apache-2.0 | not gated | reasoning model |

Optional: one or two frontier APIs, on original order plus four cyclic orders only, to test whether consensus improves with stronger models (about US$20–40). Skip if the budget is tight. The study stands on open models.

Why this one:
- **It turns the known weakness of MedMCQA into the finding.** Every MedMCQA robustness paper assumes the keys are right. A pathologist's audit of the pathology, microbiology and biochemistry items is something an ML group cannot easily do, and nothing like it was found for MedMCQA.
- **It answers a sharper question than "is the model order-sensitive?"** Medmarks and others have shown that already. This study asks how much of that sensitivity and of the "CoT backfires" effect comes from bad items and bad parsing, and whether model disagreement can point a busy examiner to the items worth re-checking. That last point is useful to Indian exam setters and coaching faculty.
- **Fully open and cheap:** one open dataset; 11 open models, 8 of them not gated (the three MedGemma models are auto-gated). About 30–50 GPU-h on RunPod, no paid API needed.
- **Fit for Atul: 5/5.** The expert audit and error taxonomy are the core of the study, not an add-on.
- **A useful answer either way.** If flips concentrate in flawed items, published position-bias numbers are inflated and benchmarks need cleaning first. If they do not, order fragility is a real model property, now shown on 2026 models with a clean key.

**Main risks:**
- Expert time (about 25 hours plus a second rater). Mitigation: audit in batches, stratified by subject.
- Consensus can be confidently wrong on items that all models learned wrongly from the same coaching sources. Mitigation: report consensus only as a review-triage aid, and never overturn a key without expert agreement.
- 2026 models may be near ceiling on old items. Tamba's 60–95% detection band applies. Mitigation: report results by model size, and include the 4B models.

Expected time: about 6 weeks to an arXiv (cs.CL) or medRxiv preprint. Candidate zero-APC journals (subscription route):
- Journal of Medical Systems;
- Journal of Biomedical Informatics (free route: verify);
- International Journal of Medical Informatics (free route: verify).
