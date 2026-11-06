---
enriched: true
---
## What the original study did

Xu, Yang, Peng and colleagues (Critical Care Medicine, Shenzhen People's Hospital) built a logistic regression model for **all-cause in-hospital mortality** in adults with cirrhosis who met Sepsis-3 on the first ICU day. Development data were MIMIC-IV v3.1. The MIMIC-IV cohort was split by calendar period: 2008–2016 for training (n = 1,328) and 2017–2022 for temporal validation (n = 724). External validation used eICU-CRD v2.0 (n = 657) and a private Shenzhen ICU cohort (SZPH-ICU, n = 131). LASSO picked **13 first-24-hour predictors** from 25 candidates. The model was drawn as a nomogram and put online as a Shiny calculator. Its AUROC was compared (DeLong, NRI) with eight existing scores: SOFA, ALBI, Child-Pugh, CLIF-OF, CLIF-C ACLF, CLIF-SOFA, MELD and MELD-Na.

**Source:** *Frontiers in Medicine* 13:1759988, published 9 February 2026 (accepted 20 January), [doi:10.3389/fmed.2026.1759988](https://doi.org/10.3389/fmed.2026.1759988); open full text in [PMC12926366](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12926366/), licensed CC BY 4.0. Read on 2026-11-06 via Europe PMC.

**Correction to the register.** The register said the paper lacked a comparison with CLIF scores. That is wrong: CLIF-OF, CLIF-C ACLF and CLIF-SOFA were all compared. What it did **not** compare: MELD 3.0, CLIF-C AD, APACHE IVa (which eICU ships ready-made), LIVERAID-ICU, and the other published cirrhosis–sepsis models (Lin 2024, Hu 2026, Xu X 2026).

**Code:** none released. The paper prints the full coefficient table (Table 2, including the intercept), so the model can be **reimplemented exactly**. The [web calculator](https://szph-icu.shinyapps.io/Cirrhosis-Sepsis-ICU/) can be used to spot-check your implementation with made-up inputs (never enter real patient values).

**Directly replicable?** Mostly yes. MIMIC-IV and eICU-CRD are credentialed open data. The SZPH-ICU arm is private and cannot be replicated; drop it.

## Data

| Dataset | Version | Role | Access |
| --- | --- | --- | --- |
| `mimic-iv` | v3.1 (the current version; released 11 Oct 2024) | Development (2008–2016) + temporal validation (2017–2022) | [PhysioNet](https://physionet.org/content/mimiciv/3.1/), credentialed |
| `eicu-crd` | v2.0 (current; released 15 Apr 2019) | External validation (208 US hospitals, 2014–2015) | [PhysioNet](https://physionet.org/content/eicu-crd/2.0/), credentialed |

**Access (both datasets, checked 2026-11-06).**
- Licence: PhysioNet Credentialed Health Data License 1.5.0.
- Data use agreement: [PhysioNet Credentialed Health Data Use Agreement 1.5.0](https://physionet.org/content/mimiciv/view-dua/3.1/).
- Training: CITI "Data or Specimens Only Research".
- Steps: create a PhysioNet account, apply for credentialing (needs a referee/supervisor), upload the CITI completion report, then sign the DUA on each dataset page. Allow **1–2 weeks** (`verify` the current turnaround). One credential covers both datasets.
- Total download size is not shown on the public pages (`verify` after login). Both datasets fit on a laptop SSD. Load them into a local PostgreSQL or DuckDB with the official [mimic-code](https://github.com/MIT-LCP/mimic-code) and [eicu-code](https://github.com/MIT-LCP/eicu-code) build scripts (both MIT licence). Keep everything under a gitignored `data/` folder outside this repo.

**DUA rules that shape this project.**
- **Never send MIMIC or eICU rows to an external LLM API**, including ChatGPT, the Claude API and this Claude Code session. PhysioNet's [notice on GPT-style services](https://physionet.org/news/post/gpt-responsible-use) says the DUA forbids sharing data through third-party APIs. Claude writes SQL and R/Python code. Atul runs it locally and shares only aggregate outputs (counts, AUROCs, plots without individual points) back into the session.
- Do not share access or redistribute derived row-level files. Commit code and aggregate tables only.
- Do not try to identify any individual **or institution**. eICU hospitals stay as anonymous `hospitalid` values.
- The DUA asks that code behind disseminated results be shared openly. Publish the SQL/R pipeline at preprint time.

## Environment

The paper used R 4.4.0 with `glmnet` (LASSO), `missForest` (imputation), `rms` (nomogram and calibration), `pROC` (DeLong), NRI and decision-curve packages (exact packages `verify`; not named for all steps).

Suggested stack:
- PostgreSQL 15+ or DuckDB, with the mimic-code `concepts_postgres` scripts (they include `sepsis/sepsis3.sql`, `sepsis/suspicion_of_infection.sql`, `score/sofa.sql`, `organfailure/meld.sql`, `organfailure/kdigo_*`).
- eicu-code `concepts/pivoted/pivoted-lab.sql`. It maps eICU lab names `total bilirubin`, `PT - INR`, `creatinine`, `sodium`, `albumin`, `lactate` and `WBC x 1000` with plausibility ranges.
- R 4.4: `glmnet`, `missForest` (or `mice`), `rms`, `pROC`, `dcurves`, `pmcalibration` or `CalibrationCurves`, `metafor` (per-hospital meta-analysis in the extension).

## Step-by-step replication

1. **Build the databases** locally (mimic-code and eicu-code build scripts), then run the mimic-code concept scripts.
2. **MIMIC-IV cohort.**
   - Cirrhosis: ICD-9/ICD-10 codes in `hosp.diagnoses_icd`. The authors' code list is in their Supplementary Table 1, which was **not read** for this guide (`verify` it before use). The usual set is ICD-9 571.2/571.5/571.6 and ICD-10 K70.3x, K74.3–K74.6. Decide in advance whether K74.6x alone counts.
   - Sepsis-3 on the first ICU day: the mimic-code `sepsis3` concept (suspected infection plus SOFA ≥ 2), restricted to the first ICU stay.
   - Exclude age < 18 and ICU stay < 24 h. Keep the first ICU admission per patient.
   - Calendar split: `patients.anchor_year_group` in {2008–2010, 2011–2013, 2014–2016} → training; {2017–2019, 2020–2022} → temporal validation. This is the only way to split MIMIC-IV by calendar time (dates are shifted). The group belongs to the patient's anchor year, so a few admissions can be misassigned; note this.
   - Target: 2,052 patients (1,328 + 724).
3. **Predictors (first 24 h after ICU admission).** Vital signs are **means** over 24 h. Labs are the **worst** value (maximum bilirubin, lactate, creatinine, WBC and INR). Urine output is coded as **< 400 mL per 24 h (yes/no)**. Vasopressor use is any vasopressor infusion (yes/no). GCS is the lowest value. **Units matter:** the coefficients assume bilirubin and creatinine in **µmol/L** (MIMIC stores mg/dL; multiply by 17.1 and 88.4).
4. **Preprocessing as in the paper.** Winsorise continuous variables at the 1st/99th percentiles. Impute with `missForest`. The paper does not say whether imputation was run separately per cohort or with the outcome included. Impute within each cohort, leave the outcome out, and report missingness per variable (the paper does not report it).
5. **Reimplement the model.** Use Table 2's intercept and 13 coefficients unchanged. Compute the linear predictor and predicted risk. Check it against the web calculator with 3–5 made-up input sets.
6. **Refit check.** Run LASSO (10-fold CV; the paper reports λ = 0.024, labelled "λ0.1se") on your training set. Check that the same 13 variables survive, and compare your refitted coefficients with Table 2.
7. **eICU cohort.**
   - Cirrhosis: eICU has no billing discharge diagnoses. Use `diagnosis.icd9code` and `diagnosisstring` (documented in the ICU, not billing codes) plus `pasthistory` ("Cirrhosis of the Liver") and `apachepredvar.cirrhosis`. Report how many patients each source adds. The paper does not say which it used.
   - Sepsis-3: eICU has no ready-made concept, and microbiology is sparse. Common choices are a sepsis diagnosis or APACHE admission diagnosis plus SOFA ≥ 2 on day 1, or antibiotics plus cultures where available. Pre-specify one and run the other as a sensitivity analysis.
   - Variables: vitals from `vitalperiodic`/`nursecharting`; labs from `lab`; urine from `intakeoutput` (or `apacheapsvar.urine`, a summed 24 h APACHE value); vasopressors from `infusiondrug.drugname`; GCS from `nursecharting` or the APACHE worst GCS. Outcome: `patient.hospitaldischargestatus` = Expired. Age "> 89" → 90.
   - Target: n = 657, 170 deaths (25.9%).
8. **Performance.** AUROC with 95% CI, Brier score, calibration plot. **Also** report calibration-in-the-large and calibration slope (the paper shows plots only), decision curves, and the Youden cut-off (0.238 in training).
9. **Comparators** in each cohort: SOFA, MELD, MELD-Na, ALBI, Child-Pugh, CLIF-OF, CLIF-C ACLF, CLIF-SOFA. Use DeLong tests and NRI against CLIF-SOFA.

## Compute and cost

Laptop (16 GB RAM, around 100 GB free disk for the two databases and their indexes, `verify`). SQL builds take a few hours. Modelling takes minutes. No GPU and no API cost. The calendar time is set by credentialing (1–2 weeks) and SQL phenotyping (2–3 weeks).

## Target numbers

| Quantity | Value | Where |
| --- | --- | --- |
| Training (2008–2016): n, deaths | 1,328; 319 (24.0%) | Results; Table 1 |
| Temporal validation (2017–2022): n, deaths | 724; 260 (35.9%) | Results; Table 1 |
| eICU-CRD: n, deaths | 657; 170 (25.9%) | Results |
| AUROC (95% CI), Brier: training | 0.822 (0.797–0.847), 0.135 | Table 3 |
| Temporal validation | 0.810 (0.777–0.843), 0.169 | Table 3 |
| eICU-CRD | 0.777 (0.734–0.821), 0.150 | Table 3 |
| Best comparator, training | CLIF-SOFA AUROC 0.759 | Results |
| eICU: nomogram vs CLIF-OF / CLIF-SOFA | p = 0.105 / 0.107 (not significant) | Results |
| NRI vs CLIF-SOFA (training / temporal / eICU) | 0.097 / 0.092 / 0.053 (p = 0.234) | Table 4 |
| Youden threshold (training) | 0.238 (sensitivity 73%, specificity 75%) | Results |
| Median MELD / CLIF-C ACLF (training) | 21 / 54 | Table 1 |

Comparator AUROCs for each cohort appear only in Figure 4 (values `verify` from the figure).

## Known pitfalls

1. **Units and transforms.** Bilirubin and creatinine coefficients are per µmol/L, and the intercept is large (23.858) because temperature enters untransformed in °C. A unit slip moves risk badly. Test against the calculator.
2. **"Most extreme" lab values plus averaged vitals** within 24 h is the paper's rule. The direction for each variable must be fixed in advance (e.g. lowest temperature or mean temperature? The paper says vitals were averaged).
3. **Lactate, creatinine and WBC were not significant** in the multivariable fit (p = 0.24, 0.26, 0.085; Table 2), yet they stayed in the model. This is relevant to a reduced score.
4. **Case mix shift.** Mortality rose from 24.0% to 35.9% between periods, and RRT use doubled (9.0% → 18.1%). AUROC stayed stable, but calibration-in-the-large must drift. Only plots are shown.
5. **Endpoint statement is out of date.** The paper says MIMIC-IV only has 28-day mortality. Since v3.0, MIMIC-IV includes out-of-hospital death up to one year after discharge (PhysioNet release notes). So 90-day mortality, the standard ACLF horizon, is available in MIMIC-IV (not in eICU).
6. **CLIF-C ACLF was computed for everyone.** Table 1 gives a CLIF-C ACLF median for the whole cohort, but the score is defined only for patients with ACLF. CLIF-C AD is the matching score for patients without ACLF. Report each score only in the population it was built for. Use the corrected CLIF-C AD formula (an erratum exists: [doi:10.1016/j.jhep.2015.04.002](https://doi.org/10.1016/j.jhep.2015.04.002)).
7. **Hepatic encephalopathy grade** (needed for CLIF-OF/ACLF and Child-Pugh) is not charted as West Haven grade in either database. GCS-based proxies are the norm. State the mapping.
8. **eICU phenotyping is the biggest source of difference.** Diagnoses there are documented in the ICU, not billing codes, and Sepsis-3 needs a proxy (step 7). The paper gives no eICU definitions.
9. **Imputation.** missForest on the pooled data, or with the outcome included, would leak information. Impute within each cohort.
10. **Small text errors in the paper:** "cirrhosis or sepsis" in the Results (it should be "and"), and BMI in "kg/m³" in Table 1. They do not change the numbers.
11. **Calendar split:** `anchor_year_group` is per patient (see step 2).

## Claude Code task list

1. Confirm that Atul's PhysioNet credentialing, CITI upload and both DUAs are complete. **Never ask for, or receive, row-level data in the session.**
2. Write `sql/mimic/00_cohort.sql`: cirrhosis codes (after reading Supplementary Table 1), the `sepsis3` join, first stay, ≥ 24 h, `anchor_year_group` split. Output: a counts-only flowchart.
3. Write `sql/mimic/01_features.sql`: the 24 h aggregates (means for vitals, worst values for labs), UO < 400 mL, vasopressor flag, lowest GCS, plus the comparator-score inputs.
4. Write `sql/eicu/00_cohort.sql` and `01_features.sql`, with each cirrhosis and sepsis definition as a separate flag.
5. Write `R/10_reimplement.R`: the Table 2 equation with unit conversion and unit tests against made-up calculator cases.
6. Write `R/20_validate.R`: AUROC, Brier, calibration intercept and slope, calibration plots, DCA, DeLong and NRI against the eight scores, for training, temporal and eICU cohorts.
7. Atul runs everything locally and pastes back **only** `results/*.csv` aggregates. Compare them with the target numbers.
8. Commit only code and aggregate results. `data/` stays gitignored.
