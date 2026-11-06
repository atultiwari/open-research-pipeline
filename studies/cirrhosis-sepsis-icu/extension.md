---
enriched: true
---
## Where the field stands (checked 2026-11-06)

Mortality prediction in cirrhosis with sepsis on MIMIC-IV is a **very crowded** topic. At least seven development papers have appeared since 2024, and four of them already validate in eICU-CRD:

| Paper | Data | Predictors / model | External AUROC |
| --- | --- | --- | --- |
| Lin et al., *Sci Rep* 2024 ([doi:10.1038/s41598-024-60305-1](https://doi.org/10.1038/s41598-024-60305-1)) | MIMIC-IV, n = 1,696 | 9 variables (age, HR, bilirubin, glucose, sodium, anion gap, fungal infection, ventilation, vasopressin) | none (apparent 0.805) |
| **Source:** Xu Z et al., *Front Med* 2026 | MIMIC-IV (temporal) + eICU (n = 657) + Shenzhen | 13 variables, logistic | eICU 0.777 |
| Xu X et al., *BMC Gastroenterol* 2026 ([doi:10.1186/s12876-026-04620-z](https://doi.org/10.1186/s12876-026-04620-z)) | MIMIC-IV, n = 1,615; MIMIC-III and eICU | **6 variables** (age, WBC, bilirubin, glucose, INR, lactate); 28-day mortality | eICU 0.745; MIMIC-III 0.756 |
| Hu et al., *Sci Rep* 2026 ([doi:10.1038/s41598-026-43991-x](https://doi.org/10.1038/s41598-026-43991-x)) | MIMIC-IV 7:3 random split; eICU n = 352 | LASSO nomogram; compared only with SAPS II | eICU 0.745 |
| Cao et al., *Scand J Gastroenterol* 2026 ([doi:10.1080/00365521.2026.2625822](https://doi.org/10.1080/00365521.2026.2625822)) | MIMIC-IV alcoholic cirrhosis + sepsis | XGBoost, 15 variables | temporal only |
| Chen et al., Research Square preprint 2026 ([doi:10.21203/rs.3.rs-10717154/v1](https://doi.org/10.21203/rs.3.rs-10717154/v1)) | MIMIC-IV + Wuhan (n = 237) | XGBoost | Wuhan 0.776 |
| Zhang L et al., Research Square preprint 2026 ([doi:10.21203/rs.3.rs-9866786/v1](https://doi.org/10.21203/rs.3.rs-9866786/v1)) | MIMIC-IV + Chinese cohort | "Parsimonious" ML model, transportability | `verify` (abstract truncated) |

Related work:
- **MELD 3.0 and CLIF-C ACLF in ICU cirrhosis.** Yeo et al., *Clin Mol Hepatol* 2025 ([doi:10.3350/cmh.2025.0573](https://doi.org/10.3350/cmh.2025.0573)) built ML models for ACLF with ≥ 2 organ failures (5,994 ICU cirrhosis patients; database `verify`). The models beat CLIF-C ACLF and MELD 3.0, but this is an ACLF population, not sepsis. Zhu et al., *Sci Rep* 2025 ([doi:10.1038/s41598-025-27731-1](https://doi.org/10.1038/s41598-025-27731-1)) combined PIV with MELD 3.0 in all critically ill cirrhosis patients in MIMIC-IV (AUC about 0.69).
- **Dynamic and lactate-based scores.** MELD-lactate with lactate clearance in cirrhosis and sepsis (Shabbir et al., *Am J Gastroenterol* 2026, [doi:10.14309/ajg.0000000000003934](https://doi.org/10.14309/ajg.0000000000003934); private US and APASL-AARC data). Dynamic prediction of extrahepatic organ failure, MIMIC-IV → eICU (Yeo et al., *eGastroenterology* 2026, [doi:10.1136/egastro-2026-100463](https://doi.org/10.1136/egastro-2026-100463)). Serial versus updated MELD with landmarks in cirrhosis and sepsis (Huang et al., *BMC Gastroenterol* 2026, [doi:10.1186/s12876-026-05364-6](https://doi.org/10.1186/s12876-026-05364-6); no abstract available, data `verify`).
- **Machine learning versus CLIF-SOFA/MELD in MIMIC-IV cirrhotic sepsis.** An EASL 2026 abstract (Lasington et al., [EMJ Hepatology](https://www.emjreviews.com/hepatology/abstract/machine-learning-for-mortality-prediction-in-cirrhotic-sepsis-moving-beyond-meld-sofa-and-clif-sofa-j07126/)) used 1,612 patients and had no MELD 3.0 comparator.

**What none of these do:**
1. Validate the *competing published models* against each other in one common external cohort.
2. Add MELD 3.0, CLIF-C AD and APACHE IVa to that comparison.
3. Report calibration slope and intercept, recalibration, and hospital-to-hospital spread across eICU's 208 hospitals.

Every paper develops its own model and compares it only with generic scores. This "yet another nomogram" pattern is exactly what an independent head-to-head validation can address.

**Novelty searches** (2026-11-06; hit lists saved in the scratchpad `cirrhosis/`). OpenAlex refused all `search=` calls (HTTP 429: the shared daily budget was used up), so the skill's fallback order was followed: Europe PMC, Crossref, then web search.

| # | Source and query | Result |
| --- | --- | --- |
| 1 | OpenAlex `search=` × 5 (MELD 3.0 cirrhosis sepsis ICU; MELD 3.0 MIMIC; MELD 3.0 eICU; CLIF-C AD/ACLF MIMIC; cirrhosis sepsis eICU external validation) | **Rate-limited, not checked** |
| 2 | Europe PMC citations of the source (PMID 41737385) | 0 citing papers. No independent validation yet |
| 3 | Europe PMC title search: cirrho* AND (sepsis OR septic OR infection*) AND (ICU OR intensive care OR critically ill OR abstract MIMIC/eICU), 2019–2026 | 38 hits. The models in the table above, plus single-biomarker papers (lactate/albumin, RDW/albumin, ALBI, NLR, chloride, coagulopathy score) |
| 4 | Europe PMC: cirrho* (title) AND "MELD 3.0" AND (ICU terms or MIMIC/eICU) | 1 hit (Zhu 2025). **No MELD 3.0 evaluation in cirrhosis with sepsis** |
| 5 | Europe PMC full text: "MELD 3.0" AND (MIMIC OR eICU) | 35 hits. Relevant: Yeo 2025 (ACLF), Lin Y 2026 (coagulopathy nomogram vs MELD 3.0, MIMIC-IV only), Zhu 2025, Shao 2026 (PNI vs MELD). None in sepsis |
| 6 | Europe PMC full text: ("CLIF-C AD" OR "CLIF-C ACLF" OR "CLIF-SOFA") AND (MIMIC OR eICU) AND cirrho* | 92 hits, mostly reviews and congress books. No CLIF-C AD evaluation in a MIMIC or eICU sepsis cohort found |
| 7 | Europe PMC full text: "MELD 3.0" AND ("CLIF-C" OR "CLIF-SOFA") AND ICU terms | 44 hits. Yeo 2025 is the only ICU head-to-head (ACLF ≥ 2 organ failures) |
| 8 | Europe PMC: cirrho* (title) AND eICU (abstract) | 20 hits. Four cirrhosis–sepsis models validated in eICU (table above); none compares published models |
| 9 | Europe PMC: cirrhosis ICU validation AND ("existing models" OR "published models" OR "head-to-head") | 0 relevant |
| 10 | Europe PMC: cirrhosis sepsis AND (resource-limited OR low-resource OR "without lactate" OR simplified OR bedside OR India*), 2018–2026 | No reduced bedside score for low-resource ICUs |
| 11 | Europe PMC: eICU AND (hospital-level OR between-hospital OR internal-external) AND cirrhosis/liver | 0 hits |
| 12 | Crossref `MELD 3.0 cirrhosis sepsis intensive care unit mortality` (2022-06+) | Source; Huang 2026 serial MELD landmark study; nothing on MELD 3.0 in sepsis |
| 13 | Crossref `CLIF-C AD score cirrhosis sepsis ICU MIMIC eICU` (2019+) | CLIF-C AD studies in non-ICU or bleeding cohorts; Sun 2026 *BMC Nephrol* (admission vs historical creatinine for AKI in MIMIC-IV/eICU) |
| 14 | Crossref `cirrhosis sepsis in-hospital mortality nomogram eICU external validation` (2023+) | Hu 2026, Lin 2024, Tang 2024 (*World J Hepatol*, all ICU cirrhosis) |
| 15 | Web search ×2: MELD 3.0 vs CLIF-C AD in cirrhotic sepsis (MIMIC/eICU); head-to-head external validation of published cirrhosis–sepsis models | No head-to-head found; Lasington EASL 2026 abstract found |
| 16 | arXiv, Semantic Scholar | Not checked (topic is clinical; Europe PMC covers medRxiv/Research Square) |

### Gap 1: No independent replication or head-to-head of competing models

- **Evidence.**
  - The source compares its model only with generic scores (Results, Figure 4).
  - At least four other cirrhosis–sepsis models exist (table above), and each was tested only by its own authors.
  - The source has 0 citations so far (search 2).
  - The authors ask for validation in "larger, more diverse" populations (Discussion, second limitation).
- **Novelty check.** Searches 2, 3, 8, 9, 14 and 15. **No head-to-head external validation of the published cirrhosis–sepsis models was found.**
- **Open data:** `mimic-iv` (temporal set 2017–2022 as a shared hold-out), `eicu-crd`.
- **Design.**
  - *Hypothesis:* once applied with locked coefficients to the same external cohort, the published models have similar discrimination (within about 0.03 AUROC) but differ widely in calibration. A liver-specific score (MELD 3.0 or CLIF-C AD) comes close in discrimination.
  - *Methods:*
    - Reimplement each model that publishes a full equation. The source's Table 2 has one. For Lin 2024, Hu 2026 and Xu X 2026, check whether the intercept and coefficients are printed (`verify`). Models without an intercept are tested for discrimination only, and this is stated.
    - Apply each model unchanged to MIMIC-IV 2017–2022 (temporal) and to eICU.
    - Use one harmonised cohort definition, plus sensitivity analyses for the cirrhosis and Sepsis-3 definitions (replication.md, step 7).
  - *Metrics:* AUROC; calibration-in-the-large and slope; flexible calibration curves; Brier score; net benefit (decision curves) at 10–50% thresholds. Then simple recalibration (intercept and slope update) as a separate step.
  - *Reporting:* TRIPOD+AI for validation, plus RECORD.
- **Rating:** feasibility 4 (credentialing; depends on published equations), novelty 3, laptop, 6–7 weeks.

### Gap 2: MELD 3.0, CLIF-C AD and APACHE IVa missing as comparators; CLIF-C ACLF used outside its population

- **Evidence.**
  - The comparator list (Methods) includes MELD and MELD-Na, but not MELD 3.0 (Kim et al., *Gastroenterology* 2021, [doi:10.1053/j.gastro.2021.08.050](https://doi.org/10.1053/j.gastro.2021.08.050)).
  - It includes CLIF-C ACLF, but not CLIF-C AD (Jalan et al., *J Hepatol* 2015, [doi:10.1016/j.jhep.2014.11.012](https://doi.org/10.1016/j.jhep.2014.11.012)).
  - Table 1 gives CLIF-C ACLF for the whole cohort, although the score is only defined for patients with ACLF.
  - eICU ships APACHE IVa predicted hospital mortality (`apachepatientresult`) as a ready-made, calibrated-in-the-USA comparator, but it was not used.
- **Novelty check.** Searches 4–7, 12, 13 and 15. MELD 3.0 has been compared with CLIF-C ACLF in ICU **ACLF** patients (Yeo 2025) and combined with PIV in **all** critically ill cirrhosis patients (Zhu 2025). **No evaluation of MELD 3.0 or CLIF-C AD in cirrhosis with sepsis was found.**
- **Open data:** `mimic-iv`, `eicu-crd`.
- **Feasibility in eICU** (checked against the official table docs at [eicu.mit.edu](https://eicu.mit.edu/eicutables/lab/) and the eicu-code `pivoted-lab.sql`):

  | Input | eICU source | Available? |
  | --- | --- | --- |
  | Bilirubin, INR, creatinine, sodium, albumin, WBC | `lab` (names `total bilirubin`, `PT - INR`, `creatinine`, `sodium`, `albumin`, `WBC x 1000`); APACHE worst values in `apacheapsvar` | Yes. Albumin has more missing values (`verify` the rate) |
  | Sex, age | `patient` (age "> 89" capped) | Yes |
  | Dialysis (MELD 3.0 creatinine rule) | `apacheapsvar.dialysis`, `treatment`, `intakeoutput.dialysistotal` | Yes (proxy for "dialysis twice in the past week") |
  | Vasopressors (CLIF-OF circulation) | `infusiondrug.drugname` | Yes |
  | Ventilation, PaO2/FiO2 or SpO2/FiO2 (respiration) | `apachepredvar` (ventDay1, pao2, fio2), `respiratorycare`, `lab` ABG, `nursecharting` SpO2 | Yes |
  | Hepatic encephalopathy grade (brain) | No West Haven field; GCS (`nursecharting`, `apacheapsvar`) or diagnosisstring "encephalopathy" | **Proxy only** |
  | ACLF status (which of CLIF-C AD or ACLF applies) | Derived from CLIF-OF organ failures | Derived |
  | APACHE IVa predicted hospital mortality | `apachepatientresult` | Yes (eICU only) |

- **Design.** Classify every patient by EASL-CLIF ACLF grade. Report CLIF-C AD in patients without ACLF and CLIF-C ACLF in those with it, and MELD 3.0, MELD-Na, SOFA, CLIF-SOFA and APACHE IVa in everyone. Show discrimination and calibration (after logistic recalibration, since raw scores are not probabilities). Run a sensitivity analysis on the GCS → HE grade mapping. Reporting guideline: TRIPOD+AI.
- **Rating:** feasibility 4, novelty 3, laptop, 2 weeks on top of Gap 1 (same pipeline).

### Gap 3: Single pooled AUROC in eICU hides hospital-to-hospital variation

- **Evidence.** eICU contains 208 hospitals. The source reports one pooled AUROC (0.777) and one non-significant NRI (Table 4), with no breakdown by site or region.
- **Novelty check.** Search 11 found 0 cirrhosis papers with hospital-level validation in eICU.
- **Open data:** `eicu-crd` (`patient.hospitalid`; the [`hospital`](https://eicu.mit.edu/eicutables/hospital/) table has `region`, `numbedscategory` and `teachingstatus`).
- **Design.** Compute AUROC and the calibration intercept for each hospital (or each region, or each pooled bed-size or teaching stratum where hospitals have too few events). Pool them with random-effects meta-analysis (`metafor`), and report the 95% prediction interval (Riley-style "internal–external" heterogeneity). Never name or describe hospitals beyond the eICU categories (DUA). Reporting guideline: TRIPOD+AI (clustering item).
- **Rating:** feasibility 3 (many hospitals will have < 10 events; group them), novelty 3, laptop, 1 week extra.

### Gap 4: A lactate-light bedside variant for low-resource ICUs

- **Evidence.**
  - Lactate (p = 0.24), creatinine (p = 0.26) and WBC (p = 0.085) were not significant in the final model (Table 2). They were kept because LASSO selected them.
  - Point-of-care lactate is often unavailable in Indian district and secondary ICUs (the register's motivation; no open Indian ICU data exist to test this).
  - Xu X 2026 already has a 6-variable model, but it still needs lactate and glucose.
- **Novelty check.** Search 10 found no reduced or low-resource score for cirrhosis with sepsis. The "parsimonious" Zhang 2026 preprint's variables are `verify` (abstract truncated).
- **Open data:** `mimic-iv` (develop), `eicu-crd` (validate).
- **Design.** A pre-specified reduced model: age, heart rate, respiratory rate, temperature, SpO2, GCS, vasopressor use, urine output < 400 mL, bilirubin and INR, with optional creatinine. **No lactate, no ABG.** Refit on MIMIC-IV 2008–2016 with shrinkage, then validate temporally and in eICU. Compare with the full 13-variable model as a non-inferiority question (ΔAUROC margin 0.02, pre-specified) and on calibration. Simulate missing lactate in the full model to show what happens if clinicians impute "normal".
  - **Indian relevance is a framing, not a validation.** The paper must say that the model has not been tested in India. Testing on Atul's institutional cirrhosis data would be a separate, ethics-approved, non-open study.
  - Reporting guideline: TRIPOD+AI.
- **Rating:** feasibility 4, novelty 2–3, laptop, 1–2 weeks extra.

### Gap 5: 90-day mortality is available in MIMIC-IV but was not used

- **Evidence.** The paper says only 28-day mortality was available in MIMIC-IV (Primary outcome). Since v3.0, MIMIC-IV includes out-of-hospital death up to one year after discharge (PhysioNet release notes, checked 2026-11-06). The 90-day horizon is the standard one for ACLF and CLIF scores.
- **Novelty check.** Searches 3 and 5. Zhu 2025 used 365-day mortality with MELD 3.0 in all cirrhosis patients, not sepsis. Not systematically searched further.
- **Open data:** `mimic-iv` only (eICU has no follow-up after discharge).
- **Design.** Temporal-cohort validation of all models and scores for 90-day mortality. Discharge to hospice is a competing-risk issue; state how it is handled.
- **Rating:** feasibility 5, novelty 2, laptop, < 1 week extra. Secondary analysis only.

### Gap 6 (considered, not pursued): dynamic or time-updated models

The authors' own future-work statement (Discussion, last limitation) is partly filled by Yeo 2026 (dynamic organ-failure prediction, MIMIC-IV → eICU) and Huang 2026 (serial MELD landmarks in cirrhosis with sepsis). It would also need much more SQL and compute. Not pursued.

### Optional pathologist add-on: how fragile is each score to laboratory measurement error?

Most of the predictors are laboratory values: bilirubin, INR, creatinine and lactate. Jaffe creatinine methods are prone to bilirubin interference, and INR depends on the reagent ISI. Neither method is recorded in MIMIC or eICU, so this cannot be measured directly. A Monte Carlo analysis can perturb each value within published analytical and biological variation (EFLM database, exact CVs `verify`). It then reports how often a patient's risk class (around the 0.238 threshold) or MELD 3.0 band flips. This is a small, novel, lab-medicine section (not searched separately; rerun the novelty check before the protocol).

## Recommended extension

**Gaps 1 + 2 as the core, with Gaps 3 and 4 as secondary aims.** Working title: *Which score for cirrhosis with sepsis in the ICU? Independent reimplementation and head-to-head external validation of published cirrhosis–sepsis models against MELD 3.0, CLIF-C AD/ACLF and APACHE IVa in MIMIC-IV and 208 eICU hospitals, with a lactate-free bedside variant.*

1. Reimplement the Xu Z 2026 model exactly and reproduce its numbers (replication.md).
2. Add every other published cirrhosis–sepsis model with a usable equation, plus MELD 3.0, MELD-Na, CLIF-C AD (no ACLF), CLIF-C ACLF (ACLF only), CLIF-SOFA, SOFA and APACHE IVa (eICU).
3. Validate all of them, locked, on MIMIC-IV 2017–2022 and on eICU: discrimination, calibration slope and intercept, recalibration, and decision curves. Report the spread between hospitals in eICU with a meta-analytic prediction interval.
4. Fit and validate a lactate-free reduced model (Gap 4). Add 90-day mortality in MIMIC-IV as a secondary endpoint (Gap 5).
5. Release the SQL/R pipeline openly (also required by the PhysioNet DUA when results are published).

**Why this one:**
- **Novelty:** the field is saturated with single-team nomograms. The useful contribution now is an honest comparison showing which model, or which simple liver score, holds up. MELD 3.0 and CLIF-C AD have not been evaluated in this population.
- **Feasibility:** open (credentialed) data, a laptop, and reusable mimic-code concepts.
- **Fit:** moderate for a pathologist. The strengths are the lab-heavy predictors and the measurement add-on. The weak spot is the critical-care SQL work, which Claude can do.
- **Journals:** an Indian/APASL framing (low-resource variant, MELD 3.0 vs CLIF) suits the Journal of Clinical and Experimental Hepatology, the Indian Journal of Gastroenterology and Hepatology International, all with zero-APC subscription routes.

**Rating:** feasibility 4, novelty 3, fit 3, laptop, 7 weeks (including 1–2 weeks waiting for credentialing).

**Novelty-check status:** two independent sources (Europe PMC, Crossref) plus web search were checked for each gap. OpenAlex, arXiv and Semantic Scholar were not checked. **Rerun OpenAlex `cites:` and `search=` before the protocol**, because new MIMIC cirrhosis papers appear almost weekly.
