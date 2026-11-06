---
enriched: true
---
## Where the field stands (checked 2026-11-06)

ICU mortality prediction in acute pancreatitis on MIMIC and eICU is a **crowded** field. Europe PMC returns 171 papers with "pancreatitis" in the title, MIMIC or eICU in the abstract, and a mortality outcome. Most are single-biomarker association studies (lactate/albumin, BUN/albumin, RDW, TyG, glucose, ALBI, phosphate/albumin). The multivariable mortality models that matter here:

| Paper | Data | Model | External result | Comparators |
| --- | --- | --- | --- | --- |
| Li C et al., *BMJ Open* 2020 ([doi:10.1136/bmjopen-2020-041893](https://doi.org/10.1136/bmjopen-2020-041893)) | eICU only (n = 378; in-hospital mortality 4.4%) | **3-variable logistic "ABL"** (age, BUN, lactate); full equation printed | Bootstrap only (C-index 0.896) | APACHE IV (similar), DCA |
| Zou K et al., *Int J Gen Med* 2023 ([doi:10.2147/IJGM.S409812](https://doi.org/10.2147/IJGM.S409812)) | MIMIC-IV → eICU (n = 514) | Logistic dynamic nomogram | eICU AUC 0.847 | APACHE II (similar), BISAP (worse) |
| Ren W et al., *J Clin Gastroenterol* 2024 ([doi:10.1097/MCG.0000000000001910](https://doi.org/10.1097/MCG.0000000000001910)) | MIMIC-IV → eICU | Gaussian naive Bayes (best of 9) | eICU AUC 0.862 | none named in abstract |
| Jiang M et al., *BMC Gastroenterol* 2025 ([doi:10.1186/s12876-025-03723-3](https://doi.org/10.1186/s12876-025-03723-3)) | MIMIC-III+IV → eICU (n = 507) | XGBoost + SHAP | eICU AUC 0.89 | APACHE IV, SOFA, BISAP |
| Wei S et al., *BMC Med Inform Decis Mak* 2025 ([doi:10.1186/s12911-025-03033-4](https://doi.org/10.1186/s12911-025-03033-4)) | MIMIC-III+IV → Beijing (n = 199) | CatBoost, 13 features, web calculator | 0.782 | — |
| Gu K & Liu Y, *BMC Med Inform Decis Mak* 2025 ([doi:10.1186/s12911-025-03103-7](https://doi.org/10.1186/s12911-025-03103-7)) | MIMIC → eICU + Wenzhou (n = 2,559 in total) | Six ML models; LR, RF and XGB best | XGB best externally | clinical scores |
| Cheng C et al., *J Clin Gastroenterol* 2025 ([doi:10.1097/MCG.0000000000002311](https://doi.org/10.1097/MCG.0000000000002311)) | Xuzhou SAP → MIMIC-IV | GBM, 28-day mortality | MIMIC 0.811 | — |
| Qin et al., SSRN preprint 2026 ([doi:10.2139/ssrn.6617112](https://doi.org/10.2139/ssrn.6617112)) | Unnamed "publicly available" dataset (n = 477) | **Elastic-net logistic "transparent benchmark"**, leakage-aware | Internal only (optimism-corrected 0.826) | SOFA |
| **Source:** Hao Y et al., Research Square 2026 | MIMIC-IV (28-day) → eICU (in-hospital) | XGBoost, 14 features, isotonic | eICU 0.862 (35 events) | SOFA, BISAP (MIMIC only) |

**What none of these do:**
1. Validate on the **same endpoint** in both databases. Every MIMIC → eICU paper either uses in-hospital death throughout or, like the source, mixes endpoints.
2. Test any published AP model **independently** of its authors with locked coefficients. In particular, the eICU-derived ABL equation has never been tested in MIMIC-IV, and no MIMIC-derived model has been retested by anyone else in eICU.
3. Ask, with leakage-free selection and proper calibration statistics, whether boosting beats a 3–5-variable logistic model. The source's own released output shows logistic regression ahead (0.869 vs 0.836 out-of-fold).
4. Check whether the ICD-only AP case definition holds up against an **enzyme-confirmed (revised Atlanta) phenotype**.

**Novelty searches** (2026-11-06; hit lists in the scratchpad `ap/q1.txt`–`q14.txt` and `cr.txt`). OpenAlex single-work lookups worked (source W7204496872: 0 citations), but `search=` calls returned HTTP 429 (daily budget used up). The skill's fallback order was followed: Europe PMC, then Crossref, then web search. arXiv and Semantic Scholar were not used: the topic is clinical, and Europe PMC indexes Research Square, medRxiv and SSRN preprints.

| # | Source and query | Result |
| --- | --- | --- |
| 1 | OpenAlex `search=acute pancreatitis mortality MIMIC` | **Rate-limited (429), not checked** |
| 2 | OpenAlex work lookup and Europe PMC `CITES:PPR1307596_PPR` | 0 citing works. No independent validation of the source |
| 3 | Europe PMC: TITLE pancreatitis AND (MIMIC OR eICU) AND mortality terms | 171 hits. The models in the table above, plus about 120 biomarker-association papers |
| 4 | Europe PMC: pancreatitis AND BISAP AND (MIMIC OR eICU) | 159 hits. BISAP used as a covariate or comparator. No study of BISAP item ascertainment in MIMIC or eICU |
| 5 | Europe PMC: TITLE pancreatitis AND eICU AND "external validation" | 40 hits. All MIMIC → eICU designs validate in-hospital death or mix endpoints; none harmonises |
| 6 | Europe PMC: pancreatitis AND (MIMIC OR eICU) AND ("existing models" OR "head-to-head" OR "independent validation" OR replicat*) | 181 hits, none an independent validation of a published AP model |
| 7 | Europe PMC: pancreatitis AND (MIMIC OR eICU) AND "logistic regression" AND (XGBoost OR ML) AND calibration | 29 hits. Each develops its own model; none uses nested selection with logistic calibration slope and intercept |
| 8 | Europe PMC: pancreatitis AND (MIMIC OR eICU) AND (lipase OR amylase) AND (Atlanta OR "case definition" OR phenotyp*) | 197 hits, mostly noise. Li Y 2025 (lipase trajectories and mortality) is the nearest. **No study compares ICD-only vs enzyme-confirmed AP cohorts** |
| 9 | Europe PMC: pancreatitis AND eICU AND (hospital-level OR internal-external OR heterogeneity) | 112 hits, none with a hospital-level analysis of an AP model |
| 10 | Europe PMC: TITLE pancreatitis AND ("APACHE IV" OR "APACHE IVa") | 6 hits. Li 2020 and Jiang 2025 compared with APACHE IV in eICU (single model each) |
| 11 | Europe PMC: ABL nomogram / "age, BUN" + lactate in pancreatitis | Only the original Li 2020. **No external validation of ABL** |
| 12 | Europe PMC: (MIMIC OR eICU) AND ("outcome harmoni*" OR "endpoint definition") AND 28-day/in-hospital AND external validation | 127 hits, none on pancreatitis |
| 13 | Europe PMC: pancreatitis AND (MIMIC OR eICU) AND (simplified OR parsimonious OR "bedside score") | 87 hits. Biomarker ratios only; no compact multivariable score validated across both databases |
| 14 | Crossref × 4 (AP mortality ML MIMIC eICU external validation; AP BISAP SOFA APACHE eICU; AP logistic vs XGBoost calibration; AP model independent validation), from 2023 | Found Qin 2026 SSRN (elastic-net benchmark, internal only) and Ren 2026 *Int J Surg* (phosphate/albumin, multicentre). No independent or harmonised validation |
| 15 | Web search × 2 (harmonised 28-day vs in-hospital AP endpoint; head-to-head AP models with BISAP/APACHE IV in eICU) | Confirms the endpoint mismatch is unaddressed; no head-to-head found |

### Gap 1: Endpoint mismatch between development and validation

- **Evidence.** The model is trained on 28-day mortality and tested on in-hospital mortality (Methods; Limitation 7). eICU events are 4.7% against 12.0% in MIMIC. Part of that gap is the outcome definition, not the case mix. The source's isotonic calibrator is fitted to 28-day risk but scored against in-hospital death.
- **Novelty check.** Searches 2, 5, 12, 14 and 15. No AP paper harmonises the endpoint. The issue is acknowledged only as a limitation.
- **Open data:** `mimic-iv`, `eicu-crd`.
- **Design.**
  - *Primary endpoint in both databases:* in-hospital death within 28 days of ICU admission. In eICU this uses `hospitaldischargestatus` and `hospitaldischargeoffset`; in MIMIC, `deathtime` or `dod` before discharge, and ≤ 28 days.
  - *Secondary endpoints:* 28-day all-cause death (MIMIC only, as in the source) and in-hospital death at any time (both). Hospice discharge is a sensitivity analysis.
  - *Analysis:* retrain the source pipeline on each MIMIC endpoint. Validate on the matching eICU endpoint, and also on the mismatched one, to show how much the mismatch alone moves calibration and AUC.
  - *Reporting:* TRIPOD+AI and RECORD.
- **Rating:** feasibility 5, novelty 3, laptop, 1 week on top of replication.

### Gap 2: Leakage-free reimplementation and the parsimonious-logistic question

- **Evidence.**
  - Feature selection (univariable screen, LASSO, gain filter) runs on all MIMIC data before cross-validation. Early stopping of the final model watches the training set, and the "calibration slope" is an OLS slope on isotonic outputs (Zenodo script; replication.md pitfalls 2–4).
  - The authors' own `Model_Comparison.csv` shows plain logistic regression on the same 14 features with a higher out-of-fold AUC than XGBoost (0.869 vs 0.836). The paper presents XGBoost as best because of calibration.
- **Novelty check.** Searches 6, 7, 13 and 14. Qin 2026 (SSRN) proposed an elastic-net "transparent benchmark", but only internally validated and against SOFA alone. **No study tests ML against a compact logistic model with nested selection and external logistic calibration in AP.**
- **Open data:** `mimic-iv` (develop), `eicu-crd` (validate).
- **Design.**
  - *Hypothesis:* once selection is nested and preprocessing is locked, XGBoost does not beat a 5-variable penalised logistic model on discrimination (pre-specified ΔAUC margin 0.02) and is worse calibrated externally.
  - *Models:*
    - (a) The source XGBoost: selection inside each outer fold of nested cross-validation, with a locked MIMIC-fitted preprocessing pipeline and isotonic step applied unchanged to eICU.
    - (b) A pre-specified 5-variable logistic model: age, BUN, lactate, bilirubin and vasopressor use, with restricted cubic splines and ridge shrinkage.
    - (c) The full 14-feature logistic model.
    - (d) The published ABL equation (Li 2020: logit = −10.3074 + 0.0831·age + 0.4032·lactate + 0.0201·BUN; units `verify`, presumably mmol/L and mg/dL).
  - *Metrics:* AUC, logistic calibration intercept and slope, flexible calibration curves, Brier score, and net benefit at 5–30% thresholds. Riley minimum sample size for each model.
  - *Reporting:* TRIPOD+AI.
- **Rating:** feasibility 4, novelty 3, laptop, 2 weeks.

### Gap 3: Bidirectional, locked external validation of published AP equations and scores

- **Evidence.**
  - SOFA and BISAP were evaluated only in MIMIC (Tables 2–3).
  - The ABL equation was derived in eICU and never tested in MIMIC (searches 10–11).
  - eICU ships APACHE IVa predicted mortality (`apachepatientresult`), and the source did not use it.
- **Novelty check.** Searches 4, 10 and 11. Jiang 2025 and Zou 2023 compared single new models with APACHE IV/II and BISAP in eICU. **Nobody has run the reverse direction (eICU-derived → MIMIC), or tested locked published AP equations by an independent team.**
- **Open data:** `mimic-iv`, `eicu-crd`; optional `mimic-iv-note` for pleural effusion.
- **Design.** In both databases, on the harmonised endpoint, evaluate:
  - the ABL equation (eICU → MIMIC external; eICU apparent);
  - the source's AP-METRIC integer score, if Supplementary Table S6 gives the point thresholds (`verify`; not read);
  - BISAP (pleural-effusion variants: ICD proxy, MIMIC-IV-Note radiology regex, item dropped), SOFA, and APACHE IVa (eICU only);
  - the reimplemented models from Gap 2.

  Report BISAP at both its intended time point (first 24 h of hospital admission) and ICU admission, since a third of ICU AP patients may arrive after day 1 (`verify` in data). Raw scores are recalibrated with logistic regression before calibration is compared. Reporting guideline: TRIPOD+AI.
- **Rating:** feasibility 4 (pleural effusion is a proxy), novelty 3, laptop, 1–2 weeks.

### Gap 4: Does the AP case definition change the answer? (pathologist add-on)

- **Evidence.**
  - The source requires lipase or amylase ≥ 3× ULN only "where available" (Methods; 112 excluded for no enzyme rise; Figure 1).
  - eICU AP is identified from ICU-documented diagnoses, and aetiology could not be coded there (Results, Cohort characteristics).
  - Revised Atlanta needs 2 of 3 criteria (pain, enzymes ≥ 3× ULN, imaging; Banks et al., *Gut* 2013, [doi:10.1136/gutjnl-2012-302779](https://doi.org/10.1136/gutjnl-2012-302779)). ICD-coded cohorts mix in chronic pancreatitis flares, post-procedural hyperamylasaemia and secondary pancreatitis in shock.
- **Novelty check.** Search 8 found no AP paper on MIMIC or eICU comparing ICD-only with enzyme-confirmed phenotypes.
- **Open data:** `mimic-iv` (`labevents` lipase and amylase with reference ranges in `ref_range_upper`); `eicu-crd` (`lab`; whether lipase and amylase are charted as lab names is `verify`).
- **Design.**
  - Define three nested cohorts: ICD-only; ICD plus enzyme ≥ 3× ULN within ±48 h of hospital admission; and enzyme-confirmed excluding chronic pancreatitis codes (577.1/K86.0–K86.1) and post-ERCP codes.
  - Report how many patients each step removes. Then report model and score performance, and calibration-in-the-large, in each cohort.
  - This is a laboratory-medicine contribution Atul can lead: reference-range handling, assay-unit checks and enzyme timing.
  - Reporting guideline: RECORD for the phenotyping, TRIPOD+AI for performance.
- **Rating:** feasibility 4, novelty 3–4, laptop, 1 week extra.

### Gap 5: Hospital-level heterogeneity in eICU

- **Evidence.** The source reports one pooled eICU AUC, with 35 events spread over many hospitals.
- **Novelty check.** Search 9 found 0 AP papers with a hospital-level analysis.
- **Design.** Same approach as `cirrhosis-sepsis-icu` Gap 3: random-effects pooling by region or bed-size stratum. With so few AP deaths per hospital, this is **descriptive only**. Reuse that study's code.
- **Rating:** feasibility 2 (too few events), novelty 2, < 1 week. Secondary at most.

### Not pursued

- **DM-stratified glycaemic modelling and TyG.** The source already shows that these add almost nothing (SHAP ranks 12–14; ΔAUC +0.004). There is little to gain from repeating it.
- **Post-ERCP pancreatitis.** The register hoped this pipeline would feed a planned post-ERCP pancreatitis study. **No open dataset of post-ERCP pancreatitis exists** (as of 2026-11-06, none was found in PhysioNet, Kaggle, Zenodo, Figshare or this registry). MIMIC-IV has ERCP procedure codes, but they are too few and lack procedural detail for a credible model. The AP SQL and validation code built here can be reused later on a private, ethics-approved ERCP cohort, which would be outside this open catalogue.
- **Dynamic landmarking.** The source already did it, and it needs far more SQL.

## Recommended extension

**Gaps 1 + 2 + 3 as the core, with Gap 4 as the pathologist's secondary aim.** Working title: *Same endpoint, locked models: endpoint-harmonised, bidirectional external validation of ICU acute-pancreatitis mortality models (AP-METRIC XGBoost, the ABL equation, a 5-variable logistic score) against BISAP, SOFA and APACHE IVa in MIMIC-IV and eICU, with an enzyme-confirmed phenotype check.*

1. Replicate the source with the authors' released MIT-licensed script (replication.md).
2. Harmonise the endpoint: in-hospital death within 28 days of ICU admission in both databases (Gap 1).
3. Rebuild the source model leakage-free (nested selection, locked preprocessing). Compare it with a pre-specified 5-variable penalised logistic model and the published ABL equation, using logistic calibration slope and intercept and decision curves (Gap 2).
4. Validate everything locked in both directions: MIMIC → eICU and eICU → MIMIC. Add BISAP (with documented proxies), SOFA and APACHE IVa (Gap 3).
5. Repeat in an enzyme-confirmed AP cohort (Gap 4). Release all SQL and Python code, as the DUA expects.

**Why this one:**
- **Novelty (moderate):** a crowded field, but every paper so far develops its own model. This would be the first independent, endpoint-harmonised, two-way validation, and the first external test of the ABL equation. It answers a practical question: does a 3–5-number bedside formula do as well as boosting?
- **Feasibility:** the authors' code is released (MIT), so replication is quick. The data are credentialed open data, a laptop is enough, and the PhysioNet credential is shared with `cirrhosis-sepsis-icu`.
- **Fit (3/5):** lab-heavy predictors and the enzyme-phenotype aim suit a pathologist. The ICU SQL is the weak spot, and Claude can write it.
- **How it relates to `cirrhosis-sepsis-icu`:** both use MIMIC-IV v3.1 + eICU v2.0, one credential, the same local database build, and shared calibration, decision-curve and hospital-heterogeneity code. Build the cirrhosis pipeline first and reuse it here. The scientific questions differ. The cirrhosis study is a broad head-to-head of many published models against liver-specific scores (MELD 3.0, CLIF-C). This study goes deep on one model's design flaws (endpoint mismatch, selection leakage, unlocked preprocessing), on ML vs compact logistic models, and on case-definition validity. Run them back to back, not merged.
- **Journals:** Digestive Diseases and Sciences (pancreatitis), Indian Journal of Gastroenterology, or International Journal of Medical Informatics (the methods angle). All have zero-APC subscription routes. The BMC titles and JMIR, where the source was sent, are excluded (APC).

**Rating:** feasibility 4, novelty 3, fit 3, laptop, 6 weeks (including 1–2 weeks waiting for credentialing; about 4 weeks if the cirrhosis pipeline already exists).

**Novelty-check status:** two independent sources (Europe PMC, Crossref) plus web search were checked for Gaps 1–3. Gap 4 and Gap 5 rest on Europe PMC only, plus the general web searches, so they are **incomplete; rerun before the protocol**. OpenAlex `search=` and `cites:` (rate-limited today), arXiv and Semantic Scholar were not checked. Rerun OpenAlex before the protocol, because new MIMIC AP papers appear weekly.
