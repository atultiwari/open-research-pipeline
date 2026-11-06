---
enriched: true
---
## What the original study did

Hao, Qin, Zhang, Chen, Li, Wan and Ye (emergency and critical care medicine, Shanghai Pudong New Area People's Hospital and Seventh People's Hospital of Shanghai University of TCM) built an XGBoost model to predict death in adults with **acute pancreatitis (AP) admitted to the ICU**. The development cohort was MIMIC-IV v3.1 (n = 1,362; 163 deaths, 12.0%). External validation used eICU-CRD v2.0 (n = 742; 35 deaths, 4.7%). **The endpoints differ between cohorts:** the model was trained on 28-day all-cause mortality in MIMIC-IV but tested on in-hospital mortality in eICU. A three-step pipeline reduced 45 candidates to 14 first-24-hour features: univariable screening at p < 0.10, then LASSO-logistic, then an XGBoost gain filter. Two features were force-added: glucose coefficient of variation and the triglyceride–glucose (TyG) index. Raw XGBoost outputs were recalibrated with isotonic regression. The model was compared with SOFA and BISAP using AUC, NRI, IDI and decision curves. The authors also added SHAP, day-1 to day-14 landmarking, subgroup "fairness" tests, a diabetes-stratified glycaemic classification and a 9-item integer bedside score (AP-METRIC).

**Source:** Research Square preprint, version 1, posted 28 August 2026, [doi:10.21203/rs.3.rs-10464724/v1](https://doi.org/10.21203/rs.3.rs-10464724/v1). Licence CC BY 4.0. The page shows the paper under review at *BMC Medical Informatics and Decision Making* (In Review). The authors' Zenodo README says it was submitted to *JMIR*, so it may have been moved between journals. As of 2026-11-06, no journal version was found in Crossref (only v1 exists; v2 and v3 return 404), Europe PMC (preprint PPR1307596, 0 citations) or OpenAlex (W7204496872, 0 citations). The full PDF was read on 2026-11-06.

**Code: released.** The Zenodo record [doi:10.5281/zenodo.20768793](https://doi.org/10.5281/zenodo.20768793) (concept DOI; latest version 21465873, 21 July 2026) is under the **MIT licence**. It holds the complete Python analysis script (`run_gold_standard_v6_METABOLIC_SENSITIVITY_FINAL.py`), run logs, aggregate CSVs and figures, and no patient data. **The cohort-extraction SQL is not included.** The script starts from two analysis-ready CSVs that cannot be shared under the DUA. The cohort and its variables must therefore be rebuilt from the paper's Methods.

**Directly replicable?** Yes, in principle. Both datasets are credentialed open data. Exact numbers will depend on rebuilding the authors' cohort without their SQL.

## Data

| Dataset | Version | Role | Access |
| --- | --- | --- | --- |
| `mimic-iv` | v3.1 (current; released 11 Oct 2024) | Development (28-day mortality) | [PhysioNet](https://physionet.org/content/mimiciv/3.1/), credentialed |
| `eicu-crd` | v2.0 (current; released 15 Apr 2019) | External validation (in-hospital mortality) | [PhysioNet](https://physionet.org/content/eicu-crd/2.0/), credentialed |

**Access (both datasets, checked 2026-11-06).** This is the same process as for `cirrhosis-sepsis-icu`, and one credential covers both studies.
- Licence: PhysioNet Credentialed Health Data License 1.5.0, with the [Credentialed Health Data Use Agreement 1.5.0](https://physionet.org/content/mimiciv/view-dua/3.1/).
- Training: CITI "Data or Specimens Only Research".
- Steps: create a PhysioNet account, apply for credentialing (needs a referee), upload the CITI report, then sign the DUA on each dataset page. Allow **1–2 weeks** (`verify` the current turnaround).
- Download size is not shown on the public pages (`verify` after login). Build local PostgreSQL or DuckDB copies with the official [mimic-code](https://github.com/MIT-LCP/mimic-code) and [eicu-code](https://github.com/MIT-LCP/eicu-code) scripts (both MIT licence). Keep the data under a gitignored `data/` folder outside this repo.

**DUA rules that shape this project.**
- **Never send MIMIC or eICU rows to an external LLM API.** That includes ChatGPT, the Claude API and this Claude Code session. PhysioNet's [notice on GPT-style services](https://physionet.org/news/post/gpt-responsible-use) says the DUA forbids sharing data through third-party APIs. Claude writes the SQL and Python. Atul runs them locally and pastes back only aggregate outputs (counts, AUCs, calibration tables, plots without individual points).
- Do not redistribute derived row-level files. Commit code and aggregate tables only. The authors did the same.
- Do not try to identify individuals or institutions. eICU hospitals stay as anonymous `hospitalid` values.
- The DUA asks that code behind published results be shared openly. Publish the SQL and Python pipeline at preprint time.

**Optional:** [MIMIC-IV-Note v2.2](https://physionet.org/content/mimic-iv-note/2.2/) (`mimic-iv-note`, same credential and DUA, separate signature). It holds 2.3 million radiology reports and could ascertain the **pleural effusion** item of BISAP from imaging text. Any text mining must run on local tools only (regex or a local model). Never use an API.

## Environment

The authors used Python 3.12 with XGBoost 2.1.4, SHAP 0.49.1, scikit-learn 1.6.1 and LightGBM 4.6.0, plus pandas, numpy, scipy and matplotlib (paper Methods; Zenodo README). Fixed seed 789.

Suggested stack:
- PostgreSQL 15+ or DuckDB with the mimic-code concepts. The useful ones are `score/sofa.sql`, `score/sirs.sql`, `firstday/first_day_gcs.sql`, `firstday/first_day_lab.sql`, `measurement/chemistry.sql` (BUN = itemid 51006), `measurement/enzyme.sql` (amylase 50867) and `measurement/vitalsign.sql`. Lipase is not in `enzyme.sql`; find its itemid in `d_labitems` (`verify`).
- eicu-code `concepts/pivoted/` scripts (`pivoted-lab.sql` maps `BUN`, `-bands`, `WBC x 1000`, `lactate`, `total bilirubin`, `albumin`, `glucose`, `bedside glucose`; plus `pivoted-gcs.sql`, `pivoted-vital.sql`, `pivoted-treatment-vasopressor.sql`, `pivoted-score.sql`).
- Python 3.12, xgboost 2.1.4, scikit-learn 1.6.1, shap 0.49.1. For the extension, add `statsmodels` and the R package `pmcalibration` or Python `pycaleva` for logistic calibration slope and intercept, plus `dcurves`.

## Step-by-step replication

1. **Build the databases** locally and run the concept scripts.
2. **MIMIC-IV cohort** (paper, Cohort definition; Figure 1).
   - AP: ICD-9 577.0 or ICD-10 K85.x in any diagnosis position. The paper says "577.x", but the README says 577.0. 577.1 is chronic pancreatitis, so use **577.0**.
   - Index time is ICU admission. Age ≥ 18. Keep the first AP episode, and the first ICU stay per hospital stay.
   - The paper requires imaging confirmation and lipase or amylase ≥ 3× ULN "where available" (Figure 1 excludes 89 for no imaging and 112 for no enzyme rise). How imaging confirmation was ascertained in MIMIC is not stated (`verify`; probably ICD procedure codes or not at all). Record each exclusion step as a count.
   - Exclude stays missing more than 3 candidate predictors.
   - Target: 2,847 ICU stays with AP → 1,362 (Figure 1).
3. **Outcome.** 28-day all-cause mortality from ICU admission, using `patients.dod`, which includes out-of-hospital deaths since v3.0. Figure 1 excludes 201 MIMIC patients for "missing outcome". That should be impossible with `dod`, so note it as an unexplained step.
4. **Predictors (first 24 h after ICU admission):** age; minimum albumin; any vasopressor; maximum BUN; Charlson index; glucose CV (%); minimum haemoglobin; maximum lactate; minimum MAP; minimum SpO2; admission glucose ≥ 140 mg/dL flag; maximum total bilirubin; TyG index (ln[TG × glucose / 2], admission values, not fasting); maximum WBC. Keep units as in the paper (mg/dL, g/dL, mmol/L).
5. **eICU cohort.** AP from `diagnosis.icd9code`/`diagnosisstring` and `patient.apacheadmissiondx` (pancreatitis). The paper does not say which source it used (`verify`). Outcome: `patient.hospitaldischargestatus = 'Expired'`. Ages "> 89" become 90. **MAP:** combine `vitalperiodic.systemicmean` (arterial line) with `vitalaperiodic.noninvasivemean` (cuff). The paper reports 71.6% missing MAP in eICU (Limitations), which suggests only the arterial-line field was used. Vasopressors come from `infusiondrug` and `medication`. The authors' first release had `any_vasopressor = 0` for all 742 eICU patients, corrected on 20 July 2026 (Zenodo README). Charlson in eICU must come from `pasthistory` and the ICU-documented `diagnosis` table. The source's eICU Charlson median is 1 against 5 in MIMIC (Table 1), which is a definitional shift in the top-ranked feature.
6. **Preprocessing as in the script.** Winsorise at the 1st and 99th percentiles. Use chained-equation imputation for variables with 1–30% missing and median imputation otherwise. **The script fits winsorisation limits, the imputer and the medians separately on the eICU data.** For a faithful replication, copy this. For the extension, lock everything to MIMIC (see pitfalls).
7. **Run the authors' script** on your two CSVs, with the column names listed in the README and script (`death_28d`, `survival_time_28d`, `in_hospital_death`, `bisap_score`, `sofa_total`, and so on). Compare with `RESULTS_SUMMARY.txt` on Zenodo.
8. **BISAP and SOFA.** SOFA comes from mimic-code `first_day_sofa`. BISAP needs the five items in the table below. The paper defines impaired mental status as GCS < 15 and takes the worst or initial 24-hour value. Pleural-effusion ascertainment is not described (`verify`).

**BISAP item availability (checked 2026-11-06 against the eicu.mit.edu table docs, eicu-code and mimic-code):**

| BISAP item | MIMIC-IV | eICU-CRD | Status |
| --- | --- | --- | --- |
| BUN > 25 mg/dL | `labevents` itemid 51006 (mimic-code `chemistry.sql`) | `lab` `BUN`; also `apacheapsvar.bun` | Direct |
| Impaired mental status | GCS (`first_day_gcs`); sedation inflates GCS < 15 | `nursecharting` GCS, `apacheapsvar` eyes/motor/verbal with a `meds` flag for unscorable GCS | **Proxy** (GCS < 15 for disorientation or somnolence; sedated patients are a problem) |
| SIRS ≥ 2 | mimic-code `score/sirs.sql` | Temperature, HR and RR from `vitalperiodic`; WBC and `-bands` from `lab`; PaCO2 from `lab` blood gas | Derived (bands often missing) |
| Age > 60 | `patients.anchor_age` | `patient.age` | Direct |
| Pleural effusion | ICD codes (proxy), or radiology reports in MIMIC-IV-Note (local text search) | No imaging reports; `diagnosisstring` "pleural effusion" only | **Proxy** in both; weakest item |

Two points follow from the table. **BISAP was designed for the first 24 hours of hospital admission**, not ICU admission (Wu et al., *Gut* 2008, [doi:10.1136/gut.2008.152702](https://doi.org/10.1136/gut.2008.152702)). Patients transferred to the ICU on day 3 or later will score differently. Also, the source reports that BISAP AUC was only 0.631 in MIMIC (range restriction).

## Compute and cost

A laptop is enough: 16 GB RAM and roughly 100 GB of free disk for both databases (`verify`). The SQL builds take hours. The authors' pipeline, with bootstraps and SHAP, takes minutes to under an hour on a CPU. No GPU and no API cost. Calendar time is set by credentialing (1–2 weeks) and SQL phenotyping (1–2 weeks, less if the cirrhosis study's pipeline is already built).

## Target numbers

| Quantity | Value | Where |
| --- | --- | --- |
| MIMIC-IV n, 28-day deaths | 1,362; 163 (12.0%) | Results; Table 1 |
| eICU n, in-hospital deaths | 742; 35 (4.7%) | Results; Table 1 |
| Median SOFA / BISAP / Charlson, MIMIC vs eICU | 10 vs 3 / 3 vs 1 / 5 vs 1 | Table 1 |
| Raw 5-fold CV AUC; bootstrap mean (95% CI) | 0.836; 0.844 (0.813–0.874) | Results; `RESULTS_SUMMARY.txt` |
| eICU AUC (95% CI) | 0.862 (0.747–0.918) | Results; Table 3 |
| SOFA / BISAP AUC (MIMIC only) | 0.764 / 0.631 | Table 2; Table 3 |
| Logistic regression on the same 14 features, 5-fold OOF AUC | **0.869** (higher than XGBoost) | Zenodo `Model_Comparison.csv` (not in the paper's Table 3 text) |
| LASSO AUC (apparent) | 0.881 | Table 3 |
| NRI / IDI vs BISAP | 0.256 / 0.151 | Table 3 |
| Raw XGBoost calibration slope, Brier | 0.618, 0.119 | Results, Calibration |
| eICU after MIMIC-fitted isotonic: "slope", Brier, HL p | 1.200 (0.913–1.606), 0.036, 0.012 | Results; Supplementary Table S4 |
| 15% threshold: sensitivity / specificity / NPV | 74.8% / 78.2% / 95.8% | Results; Supplementary Table S3 |
| AP-METRIC bedside score AUC, MIMIC / eICU | 0.845 / 0.877 | Figure 5 legend |
| Landmark AUC, day 1 → day 14 | 0.821 → 0.755 | Results |

## Known pitfalls

1. **Endpoint mismatch.** The model learns 28-day mortality (including deaths after discharge) but is scored on in-hospital death in eICU (Limitation 7). eICU's `hospitaldischargeoffset` allows **in-hospital death within 28 days of ICU admission** in both databases, which gives a harmonised endpoint (extension Gap 1).
2. **Feature selection outside cross-validation.** In the script, univariable screening, LASSO and the gain filter run on all MIMIC data, and only the final XGBoost is cross-validated. The CV AUC is therefore optimistic. The "bootstrap-validated" AUC only resamples the pooled out-of-fold predictions; it is not an optimism correction.
3. **The final model's early stopping watches the training set** (`evals=[(dfull,'train')]`), so it does not regularise.
4. **"Calibration slope" is non-standard.** The script fits an ordinary least-squares line of outcome on isotonic-calibrated probability (`np.polyfit`). A slope of 1.000 in MIMIC is guaranteed by construction, as the authors admit. The usual logistic calibration slope and intercept (on the logit scale) are not reported for either cohort.
5. **Preprocessing is not locked.** Winsorisation limits, chained-equation imputation and medians are re-estimated on eICU, so the externally validated "model" includes eICU-fitted steps. eICU had heavy missingness (MAP 71.6%, TyG 67.4%, lactate 58.9%; Limitation 5).
6. **Comparators were never validated externally.** SOFA and BISAP AUCs, NRI and IDI are reported in MIMIC only.
7. **Tiny external event count.** With 35 deaths, the eICU AUC CI is 0.75–0.92 and subgroup estimates are noise (one eICU stratum has a single event).
8. **Logistic regression beat XGBoost internally** (0.869 vs 0.836 OOF; `Model_Comparison.csv`). The paper chose XGBoost because its calibration looked better, but that calibration is isotonic on the same predictions.
9. **Case-mix shift in key features:** eICU's median Charlson 1 vs 5 and SOFA 3 vs 10 (Table 1). These may come from definitions (no billing codes in eICU) rather than from patients.
10. **Version drift in the authors' own data:** the eICU vasopressor flag was all zero until 20 July 2026, and the SQL patch "v7.6.3" changed BMI, SOFA-CNS and aetiology. Use the latest Zenodo version only.
11. **Small inconsistencies:** "577.x" (paper) vs "577.0" (README); "missing outcome" exclusions in MIMIC; the README's "fairness_n_flagged: 6" vs the paper's "no subgroup flagged" (the 6 is the descriptive |ΔAUC| > 0.05 count).
12. **DM classification** (72.9% DM-positive in MIMIC, Supplementary Note S1) is unusual. The 4-dimension definition needs "pre-admission glucose ≥ 126 mg/dL on ≥ 2 occasions" within 24 h of ICU admission, which is hard to reproduce exactly.

## Claude Code task list

1. Confirm that Atul's PhysioNet credentialing, CITI upload and DUAs (MIMIC-IV v3.1, eICU-CRD v2.0; optionally MIMIC-IV-Note v2.2) are complete. **Never ask for, or receive, row-level data in the session.**
2. Pull the latest Zenodo version (record 21465873) of the authors' script into `code/ap-icu-mortality/upstream/` with its MIT licence notice. Code only; no data exists there.
3. Write `sql/mimic/ap_00_cohort.sql`: ICD 577.0/K85.x, age ≥ 18, first AP episode and first ICU stay, an enzyme-confirmation flag (lipase or amylase ≥ 3× ULN within ±48 h), 28-day death from `dod`, and in-hospital death within 28 days. Output a counts-only flowchart.
4. Write `sql/mimic/ap_01_features.sql`: the 14 features, SOFA, the BISAP items (with GCS-proxy and pleural-effusion variants), and APS/SAPS II as extras.
5. Write `sql/eicu/ap_00_cohort.sql` and `ap_01_features.sql`: AP from `diagnosis` and `apacheadmissiondx` as separate flags; MAP from both vital tables; vasopressors from `infusiondrug` plus `medication`; Charlson from `pasthistory`; outcome from `hospitaldischargestatus` and `hospitaldischargeoffset`; APACHE IVa predicted mortality from `apachepatientresult`.
6. Run the upstream script unchanged on the rebuilt CSVs and compare with `RESULTS_SUMMARY.txt`. Report differences in n, events and AUC.
7. Atul runs everything locally and pastes back **only** `results/*.csv` aggregates.
8. Commit only code and aggregate results. `data/` stays gitignored.
