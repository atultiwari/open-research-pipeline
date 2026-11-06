---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** ClinicalBench (KDD '26, [doi:10.1145/3770855.3818831](https://doi.org/10.1145/3770855.3818831); [arXiv:2411.06469](https://arxiv.org/abs/2411.06469)).
  - Inputs are age, sex, and the visit's ICD diagnosis titles, ICD procedure titles and drug classes. There are **no labs, vitals or notes** (confirmed in `clinicalbench/config.py`).
  - Inputs cover the **whole stay**, and diagnosis codes are assigned after discharge.
  - Models are 2024-era open LLMs, up to Llama3-70B and Meditron-70B.
  - Metrics are F1 and AUROC only: no calibration and no subgroup analysis.
- **The register's premise needs a correction.** "Add labs to ClinicalBench" is no longer a clean gap. Three groups have already compared LLMs with gradient boosting on MIMIC-IV structured data that includes labs or physiology:
  - **[Peng et al., JAMIA 2026](https://doi.org/10.1093/jamia/ocag146)** ("Less can be better", [PMC13552356](https://pmc.ncbi.nlm.nih.gov/articles/PMC13552356/)): 22,254 MIMIC-IV admissions that also had a chest X-ray and a radiology report.
    - Inputs: vitals and routine labs from 6 h before to 24 h after admission, summarised as mean/min/max/SD and written as text.
    - Models: Llama-3.1-8B, gpt-oss-20B, Gemma-3-27B, Meditron, MedGemma (zero-shot, 5-shot, 4-bit LoRA) against XGBoost, for in-hospital mortality and length of stay.
    - Findings: structured data alone gave the best risk prediction (mortality AUROC 0.849). Narrative text format beat key–value format by 0.001–0.022 AUROC.
    - Not covered: readmission, reference ranges or flags, labs-only versus codes contrasts, and any link to ClinicalBench.
  - **[ClinicRealm, npj Digit Med 2026](https://doi.org/10.1038/s41746-026-02539-z)** (Zhu et al., vol 9, 319; code [yhzhu99/ehr-llm-benchmark](https://github.com/yhzhu99/ehr-llm-benchmark), no licence file): LLMs, BERT models and 11 conventional methods on MIMIC-IV structured EHR plus notes, and on TJH (COVID-19 blood tests).
    - Its MIMIC-IV structured set comes from [PKU-AICare/mimic_preprocessor](https://github.com/PKU-AICare/mimic_preprocessor): **17 chartevents variables** (vitals, GCS, capillary refill, FiO2, glucose, pH, height, weight). **No CBC, electrolytes, renal or liver panel.**
    - Finding: specialised models win with ample data; leading LLMs win in data-scarce settings.
    - The register asked us to cite it. It is now peer-reviewed.
  - **[Zhu et al., arXiv:2402.01713](https://arxiv.org/abs/2402.01713)** (2024): zero-shot prompting on MIMIC-IV and TJH with **units and reference ranges** added to each feature. Better prompts raised scores and beat ML in few-shot settings.
- **Leakage evidence that undermines ClinicalBench's headline:** [Ramadan et al., JAMA Netw Open 2025](https://doi.org/10.1001/jamanetworkopen.2025.50454) ([PMC12743287](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12743287/)).
  - ICD codes alone predicted MIMIC-IV in-hospital mortality with AUROC about 0.97 (logistic regression, random forest, XGBoost). The top predictors were codes such as cardiac arrest, brain death, palliative-care encounter and DNR status.
  - 40% of 92 MIMIC same-admission models in their literature review used ICD codes as features.
  - ClinicalBench's bag-of-codes mortality set-up (XGBoost AUROC 95.97 on MIMIC-III, README) fits this pattern, and its prompts give LLMs the same hindsight codes. **No paper found tests whether "ML beats LLMs" still holds once that leakage is removed.**
- **Other related work:**
  - [Ge et al., JAMIA Open 2026](https://doi.org/10.1093/jamiaopen/ooag199): numeric features beat LLM-embedding features on MIMIC-III (mortality AUROC 0.901 vs 0.835), and the two fail on different patients.
  - [Lovon et al., arXiv:2504.20547](https://arxiv.org/abs/2504.20547): fine-tuned text models compete with tabular classifiers on MIMIC-IV mortality; zero-shot LLMs struggle.
  - [Kobayashi et al., arXiv:2512.00479](https://arxiv.org/abs/2512.00479): LLMs do not use informative missingness (for example, a rare lab being ordered) without steering.
  - [Gao et al., arXiv:2408.11854](https://arxiv.org/abs/2408.11854): raw numeric features beat LLM embeddings.
  - [Ravichandran et al., arXiv:2607.15380](https://arxiv.org/abs/2607.15380): fine-tuning on serialised text matches multimodal baselines (MIMIC-III).
  - Shinohara & Kawazoe, JMIR preprint 2026 ([doi:10.2196/preprints.113569](https://doi.org/10.2196/preprints.113569)): Qwen3 and Gemma 4 sort lab values against given reference ranges well, but make errors near the boundaries.

**Searches run on 2026-11-06:**
- **OpenAlex:** HTTP 429 (daily budget used up), **not checked**.
- **Semantic Scholar** (paper lookup and citations of arXiv:2411.06469): HTTP 429 / empty, **rate-limited, not checked**.
- **arXiv API** (one search, newest 60): `(abs:"language model" OR abs:LLM) AND (abs:MIMIC OR abs:EHR) AND (abs:laboratory OR abs:"lab values" OR abs:"lab tests" OR abs:tabular) AND (abs:XGBoost OR abs:"gradient boosting" OR abs:ClinicalBench)`. Four hits; Ravichandran 2026 and Gao 2024 were relevant. Abstracts of other arXiv papers were read through DataCite.
- **Europe PMC** (2025-01-01 to 2026-11-06, newest 40 each):
  1. LLM + laboratory + XGBoost/ML + mortality/readmission/length of stay;
  2. "ClinicalBench";
  3. LLM + MIMIC-IV + laboratory + prediction + zero-shot/serialisation/gradient boosting;
  4. LLM + structured EHR/tabular + XGBoost + clinical prediction;
  5. ClinicRealm/ClinicalBench/LLM + MIMIC-IV + readmission + LOS + XGBoost.

  These found Peng 2026, Ge 2026, ClinicRealm, and a citing paper (DxDirector, Nat Commun 2026) that is unrelated to labs.
- **Crossref** (from 2025-01-01, 25 rows each): (a) LLM lab values clinical prediction MIMIC-IV XGBoost; (b) LLM serialisation, lab reference range, zero-shot mortality; (c) ClinicalBench LLM vs traditional ML; (d) ICD codes, label leakage, discharge, mortality, LLM. These found Ramadan 2025 and the Shinohara preprint.
- **Web search** (3 queries): ClinicalBench + MIMIC-IV labs vs XGBoost 2026; LLM lab reference-range flags serialisation for MIMIC mortality; ClinicalBench label-leakage critique. **No critique or lab extension of ClinicalBench was found.**
- **Inside this repo:** `find_dupes.py` matched only this study. Other MIMIC studies: `cirrhosis-sepsis-icu` (logistic nomogram, MIMIC-IV v3.1) and `ap-icu-mortality` (XGBoost reimplementation, MIMIC-IV to eICU). Neither involves LLMs, so there is no overlap. Reuse their DUA wording and their v3.1 SQL know-how, but note this study must use **v2.2**.

### Gap 1: Hindsight codes versus admission-time data. Is "ML beats LLMs" a leakage effect?

- **Evidence:**
  - ClinicalBench uses discharge-assigned ICD codes and whole-stay procedures and drugs (`config.py`, PyHealth task functions).
  - Its limitations section names ICD codes as a weakness, but treats it as affecting all models equally.
  - Ramadan et al. show these codes leak same-admission mortality. Bag-of-codes classifiers can exploit a few near-deterministic codes better than a zero-shot LLM reading 30 titles, so the leakage may **favour ML specifically**. Nobody has tested this.
- **Novelty check:** no paper found that removes leaky codes or switches ClinicalBench to admission-time inputs (Europe PMC queries 2 and 5, Crossref (c) and (d), web query 3). Peng 2026 uses an admission window but has no hindsight arm and no ClinicalBench split. **Novel as of 2026-11-06.**
- **Open data:** `mimic-iv` v2.2 (`hosp`: diagnoses_icd, procedures_icd, prescriptions, labevents, admissions).
- **Design sketch:**
  - *Hypothesis:* moving from hindsight codes to admission-time inputs lowers every model's AUROC, and lowers ML's more than the LLMs', so the ML–LLM gap shrinks.
  - *Set-up:* same patients and the same published v2.2 splits (indices 0–4). Four input arms:
    - **A** ClinicalBench original;
    - **B** A with a pre-registered list of outcome-proximal codes removed (cardiac arrest, brain death, palliative care, DNR, and the Ramadan top list);
    - **C** admission-time only: age, sex, admission type and location, drugs started within 24 h, and labs (Gap 2);
    - **E** A plus labs (the register's original question).
  - *Models:* XGBoost and logistic regression on identical information; LLMs below.
  - *Metrics:* AUROC, AUPRC, F1 with invalid rate. The main estimate is the change in the ML–LLM AUROC gap between arms, with a paired bootstrap across 5 splits.
  - *Reporting guideline:* TRIPOD+AI, plus TRIPOD-LLM.
- **Rating:** feasibility 3 (credentialing wait, v2.2 lab-itemid mapping, manual HF gates for the anchor models), novelty 4, RunPod, about 3 weeks after data access.

### Gap 2: Routine admission labs (CBC, chemistry, renal, liver, coagulation, lactate) as the predictor set

- **Evidence:**
  - ClinicalBench has no labs.
  - ClinicRealm's MIMIC-IV set has only glucose and pH among labs.
  - Peng 2026 used vitals plus labs in a CXR sub-cohort (22k), and reported mortality and LOS only.
  - No study runs a **labs-only** arm (plus age and sex), which is the pathologist's question: how much prognosis sits in the first routine panel?
- **Novelty check:** Peng 2026 partly covers labs + LLM + XGBoost at 24 h (Europe PMC queries 1, 3, 5). Labs-only, readmission, and the ClinicalBench cohort are not covered. **Partly novel.**
- **Open data:** `mimic-iv` v2.2 `labevents`.
  - Take the **first value within −6 h to +24 h of `admittime`**, matched by `subject_id`, so that ED draws whose `hadm_id` is null are included.
  - Use mimic-code `complete_blood_count`, `blood_differential`, `chemistry`, `enzyme`, `coagulation` and `bg` itemids, checked against v2.2 `d_labitems`.
- **Design sketch:**
  - *Panel:* Hb, WBC, platelets, neutrophil and lymphocyte %, RDW, Na, K, Cl, HCO3, anion gap, urea, creatinine, glucose, Ca, albumin, bilirubin, ALT, AST, ALP, INR, PT, lactate.
  - *Missingness:* record "not done" explicitly. The ordering pattern carries information (Kobayashi 2025).
  - *Arms:* labs-only (D), labs + admission data (C), and codes + labs (E).
  - *Readmission:* also add the last panel before discharge, since readmission is predicted at discharge.
  - *Rating:* feasibility 4, novelty 3, laptop SQL + RunPod, 2 weeks.

### Gap 3: How labs are shown to an LLM: raw numbers, a lab-report format, or flags only

- **Evidence:** MIMIC-IV `labevents` stores `ref_range_lower`, `ref_range_upper` and `flag` for each result (mimic-code `create.sql`), so the hospital's own reference intervals are available.
  - Zhu 2024 added units and ranges but did not test flags against raw values.
  - Peng 2026 compared narrative with key–value format only.
  - Shinohara 2026 shows LLMs misclassify values near range boundaries, on synthetic data.
- **Novelty check:** web query 2 and Crossref (b) found no head-to-head test of raw versus range + H/L flag versus flags-only formats for outcome prediction on real EHR data. **Novel in its specific form**, though it is a smaller contribution.
- **Design sketch:** three formats for the same labs:
  - **F1** `Hb 7.9 g/dL`;
  - **F2** `Hb 7.9 g/dL (ref 13.5–17.5) LOW`, like a printed lab report;
  - **F3** `Hb LOW` only.

  F3 tests whether LLMs use magnitude at all. Use paired comparisons on the same patients, the small cohort (index 6, 500 test visits) for every model, and the full test sets for the two best models. XGBoost gets matching numeric or flag-only features.
- **Rating:** feasibility 5, novelty 3, RunPod, 1 week.

### Gap 4: 2026 open models, calibration and subgroups

- **Evidence:** ClinicalBench's newest models are mid-2024 (Llama3, Gemma2, Qwen2). It reports F1/AUROC only, with no calibration (its training sets are rebalanced), and no sex, age or race subgroups.
- **Novelty check:** ClinicRealm and Peng use newer models, but not on this cohort. Calibration of LLM risk scores on MIMIC is covered by Kobayashi 2025 only in a different set-up. **Partly novel.**
- **Design sketch:**
  - *Models:* Qwen3.5-9B, Gemma 4 12B, gpt-oss-20b and MedGemma 1.5 4B, plus anchors Llama3-8B, Gemma2-9B and Meditron-7B. All run locally; licences are in `replication.md`.
  - *Scoring:* logits with `--token_id_mode auto`, giving a probability for every prompt.
  - *Calibration:* Brier score, calibration slope and intercept, and decision curves, before and after Platt scaling on validation.
  - *Subgroups:* AUROC by sex, age band and race/ethnicity.
  - *Fine-tuning:* optional LoRA of one model (Gemma 4 12B) on arm C, with the same 20-epoch, best-on-validation rule as the baselines.
- **Rating:** feasibility 4, novelty 3, RunPod 60–100 GPU-h, 2 weeks.

### Gap 5: A pathologist's error taxonomy of lab-driven predictions

- **Evidence:** ClinicalBench's error analysis stops at confusion matrices (Figure 2). Nobody has checked whether LLM errors on lab inputs come from misreading values (unit or magnitude errors), ignoring critical values (K 6.8, lactate 6), or over-weighting mild abnormalities.
- **Novelty check:** none of the papers above does an expert, case-level review of LLM reasoning over lab panels for outcome prediction. **Novel, but small on its own.**
- **Design sketch:**
  - Atul reviews a stratified sample of discordant cases (LLM wrong and XGBoost right, and the reverse), for example 150 cases from gpt-oss-20b chain-of-thought outputs on arm D/F2.
  - Codes: critical value missed; normal value called abnormal; magnitude or unit misread; correct lab reading but wrong prognosis; other.
  - **The review runs locally:** Atul reads outputs on his own machine; only the counts are shared.
- **Rating:** feasibility 4, novelty 3, laptop, 1 week.

### Gap 6 (not recommended now): external validation on eICU-CRD

- **Evidence:** the paper's second limitation is single-centre data. `eicu-crd` (already in `datasets/`) has a `lab` table and a diagnosis table, but no ClinicalBench split, a different coding system and ICU-only patients.
- **Why not now:** it doubles the SQL work and breaks comparability with the published split. Keep it as a follow-up. Feasibility 3, novelty 3.

## Recommended extension

**Gaps 1 + 2 together, with 3–5 as secondary analyses:** "Do routine admission labs, or leaky discharge codes, decide LLM versus ML performance? A leakage-aware re-test of ClinicalBench (MIMIC-IV v2.2, published splits) with admission CBC and chemistry panels, lab-report formatting and 2026 local open-weight LLMs."

Why this one:
- **It turns a weakened premise into a sharper question.** Adding labs alone is now partly done (Peng 2026, ClinicRealm, Zhu 2024). The open question is whether a KDD '26 benchmark's headline holds once its inputs are limited to what is known at admission. The data to test that, routine lab panels, is a pathologist's home ground.
- **Clean design.** Same patients, the published split, matched information for ML and LLMs, and four pre-registered input arms. Each arm answers one question: leakage (A vs B), real-time use (C), labs alone (D), and the register's original question (E).
- **Feasible on open data.** One credentialed dataset Atul needs anyway (shared with `cirrhosis-sepsis-icu`), MIT-licensed code with shipped splits, local open-weight models only (DUA-compliant), and about 60–100 GPU-h.
- **Good fit for Atul (4/5).** He chooses the lab panel and its timing, sets reference-range and critical-value logic, writes the leaky-code list, and does the error taxonomy (Gap 5). The SQL and the runs are routine.
- **A useful answer either way.** If the ML advantage shrinks without hindsight codes, ClinicalBench's conclusion needs qualifying. If ML still wins on labs, that gives a clear, leakage-free statement that LLMs do not yet use numeric lab data as well as gradient boosting.

**Main risks:**
- Peng 2026 overlaps on labs + LLM + XGBoost. Mitigation: frame around leakage and the ClinicalBench cohort, cite Peng, add readmission and labs-only arms.
- Low mortality prevalence (3.5%, 200 deaths per test split) gives wide AUROC intervals. Mitigation: pool 5 splits, AUPRC, paired bootstrap.
- v2.2 itemid differences. Mitigation: map against v2.2 `d_labitems`.
- RunPod use under the DUA. Mitigation: private pod, encrypted volume, wipe afterwards, or run on a local GPU; confirm with PhysioNet if in doubt.

Expected time: about 10 weeks to a preprint (credentialing 1–2, SQL 2, runs 3, analysis and writing 3). Preprint on medRxiv or arXiv (cs.CL). Candidate zero-APC journals:
- Journal of Biomedical Informatics (free route: verify);
- International Journal of Medical Informatics (free route: verify);
- Journal of Medical Systems (subscription route).
