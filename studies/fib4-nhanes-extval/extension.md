---
enriched: true
---
## Where the field stands (checked 2026-11-06)

FIB-4 versus elastography in NHANES is a **crowded** topic. The extension planned in the register (validate FIB-4 Plus on 2021–23, plus Asian and lean subgroups) has largely been done by others in 2026:
- **Jiang et al., *Gut and Liver* 2026** ([doi:10.5009/gnl260210](https://doi.org/10.5009/gnl260210); diamond open access, CC BY-NC). They developed a regularised second-stage model in MASLD adults with FIB-4 ≤ 2.67 on NHANES 2017–March 2020 (n = 3,004) and validated it temporally on August 2021–August 2023 (n = 1,959; 20.8% with LSM ≥ 8 kPa).
  - Methods: serology-based viral exclusion, weekly alcohol grams, fixed comparator pathways (standard, age-adjusted, high-risk-only FIB-4), and decision curves.
  - Result: validation AUROC 0.742.
  - Limitations they name: LSM is not histology and is affected by obesity, probe and exam quality; exclusions may be misclassified; SAFE and Agile were not compared; weights were used only for descriptive estimates.
- **Lasington et al., IDDF 2026 abstracts in *Gut*** ([ABS-0275](https://doi.org/10.1136/gutjnl-2026-iddf.193), [ABS-0276](https://doi.org/10.1136/gutjnl-2026-iddf.194)) stratified FIB-4 and XGBoost by race/ethnicity and by lean versus non-lean status across NHANES 2017–2023 (LSM ≥ 7 kPa, cross-validation, no survey design).
- Diabetes and obesity reducing FIB-4 accuracy has been shown in Canadian cohorts (Shaheen et al., *JHEP Reports* 2026, [doi:10.1016/j.jhepr.2026.101735](https://doi.org/10.1016/j.jhepr.2026.101735)). Low FIB-4 sensitivity in young adults has been shown in NHANES 2017–20 (van Kleef et al., *CGH* 2025, [doi:10.1016/j.cgh.2025.06.036](https://doi.org/10.1016/j.cgh.2025.06.036)).
- Head-to-head comparisons of non-invasive tests (MAF-5, SAFE, LiverRisk and others) exist for pre-2021 NHANES data (exact cycles `verify`) (van Kleef et al., *Hepatology* 2025, [doi:10.1097/hep.0000000000001356](https://doi.org/10.1097/hep.0000000000001356); *JCEH* 2025, [doi:10.1016/j.jceh.2025.102512](https://doi.org/10.1016/j.jceh.2025.102512)).

So the novelty has to come from what these papers leave open: **how much of the "missed fibrosis" is real**, given that both the reference standard (LSM) and the index test (AST, ALT, platelets) carry measurement error. That question suits a pathologist.

**Novelty searches** (2026-11-06; OpenAlex `search=` unless stated; queries and hit lists saved in the scratchpad):

| # | Query (from-date) | Result |
| --- | --- | --- |
| 1 | `FIB-4 NHANES 2021-2023` (any date) | 1,007 hits. Relevant: Jiang 2026 (*Gut Liver*); Liang 2026 Zenodo code "FIB-4 and elevated liver stiffness in restrictive operational MASLD" (2017–20 and 2021–23, no paper found); Kariyama 2026 OSF plan (FIB-3 vs FIB-4, 2017–2023); Ozer 2026 Zenodo (MetALD threshold, 2021–23) |
| 2 | `FIB-4 false negative MASLD NHANES elastography` (2023-01-01) | 63 hits. Chang 2024 *CGH* (FIB-4–elastography discordance in a general-population cohort); no false-negative phenotyping paper other than the source |
| 3 | `lean MASLD NHANES transient elastography FIB-4` (2022-01-01) | Lasington IDDF 2026 ×2; Chua 2025 *AJG* abstract (lean MASLD, 2017–18); Jain 2025 *AJG* abstract (clustering, 2017–18) |
| 4 | `Asian American MASLD NHANES fibrosis` (2021-01-01) | No paper uses Asian-specific MASLD criteria (BMI ≥ 23 and Asian waist cut-offs) to test FIB-4 |
| 5 | `machine learning significant fibrosis MASLD NHANES 2021-2023 external validation` (2025-01-01) | Huang 2025 *BMC Gastroenterol* (ML on 2021–23); Yue 2026 (explainable ML for F2+); several internal-only ML papers |
| 6 | `steatosis-associated fibrosis estimator SAFE score NHANES validation` (2023-01-01) | SAFE validated in the general US population (van Kleef 2023) and compared with FIB-4 (Li 2024; Aydin 2025 abstract, NHANES); none restricted to the FIB-4 < 1.3 stratum in 2021–23 |
| 7 | `FIB-4 age-adjusted cutoff obesity diabetes liver stiffness NHANES` (2024-01-01) | van Kleef 2025 *CGH*; Jiang 2026; Xie 2026 (adiposity vs FIB-4, 2011–18) |
| 8 | `liver stiffness overestimation controlled attenuation parameter obesity false positive elastography` (2017-01-01) | Karlas 2018 *APT* (CAP changes LSM interpretation; individual-patient-data meta-analysis, not NHANES). No NHANES study re-scores FIB-4 "false negatives" for LSM artefacts |
| 9 | `latent class analysis imperfect reference standard liver fibrosis FIB-4 elastography` (2015-01-01) | 6 hits, none in MASLD or NHANES |
| 10 | `multiverse specification curve analysis MASLD NHANES` (2020-01-01) | 0 hits |
| 11 | `FIB-4 analytical variability biological variation measurement uncertainty reclassification` (2015-01-01); `FIB-4 AST assay ... platelet analyser variability misclassification` | No relevant hits |
| 12 | Source paper: `Mohammad Ahmadullah Khan FIB-4 MASLD` (2026); `APASL single topic conference 2026 Kumamoto abstracts`; `FIB-4 false negatives phenotypes NHANES` (2025-06-01) | No indexed version of the source |
| 13 | arXiv `all:FIB-4 AND all:NHANES` (1 call) | 0 results |
| 14 | Europe PMC preprints: `"FIB-4" AND NHANES AND (elastography OR "liver stiffness") AND SRC:PPR` | 3 hits, none relevant |
| 15 | Semantic Scholar | Not checked: the source has no DOI or arXiv ID to look up citations for |

### Gap 1: No temporal or external validation of FIB-4 Plus

- **Evidence.**
  - The model was trained and tested on one 80/20 split of 2017–2020.
  - Its features were picked from SHAP on the same data (`src/exp09_fib4plus.py`).
  - The abstract asks for validation.
- **Novelty check.** Searches 1, 5 and 7. **Largely filled by Jiang 2026.** That study used the same cycles, the same LSM ≥ 8 kPa endpoint and a second-stage design after FIB-4, with temporal validation. Validating FIB-4 Plus on its own would be a small incremental step.
- **Open data:** `nhanes`.
- **Design.**
  - Lock the FIB-4 Plus coefficients on 2017–20, with features chosen inside cross-validation.
  - Apply them unchanged to 2021–23. Measure design-based AUROC, calibration slope and intercept, and net benefit.
  - Compare with Jiang's pathway, if the authors share their locked coefficients (their scripts are "on request").
  - Reporting guideline: TRIPOD+AI.
- **Rating:** feasibility 5, novelty 1, laptop, 2 weeks. Useful only as a component of a bigger study.

### Gap 2: Asian-specific MASLD criteria and lean MASLD

- **Evidence.**
  - The source applied BMI ≥ 23 only to the eligibility step (`exp08`, 39 extra Asian adults).
  - It found just 3 lean false negatives (`exp12`).
  - The abstract asks for lean-MASLD validation.
- **Novelty check.** Searches 3 and 4. Lasington (IDDF 2026) covered race × lean strata across 2017–2023, but as abstracts only, with LSM ≥ 7 kPa, no survey design, and Western BMI cut-offs. No study was found that uses Asian waist cut-offs (90/80 cm) together with BMI ≥ 23 to define both MASLD and "lean".
- **Open data:** `nhanes`. Pool both cycles: P_DEMO has 1,638 non-Hispanic Asian participants and DEMO_L has 681.
- **Design.** Survey-weighted false-negative rate and sensitivity of FIB-4 (standard and age-adjusted cut-offs), by:
  - Asian versus non-Asian;
  - lean (BMI < 23 in Asian adults, < 25 in others) versus non-lean;
  - each using both Western and Asian criteria.

  Report design-based CIs and the NCHS reliability flags for small cells. Reporting guideline: STARD 2015 plus RECORD.
- **Rating:** feasibility 4 (small cells; expect wide CIs), novelty 2, laptop, 2–3 weeks. Relevant to India (lean MASLD among South Asians), but US Asian adults are a mixed group, and NHANES does not report South Asian origin separately in the public files (`verify`).

### Gap 3: Is the "miss" real? Reference-standard robustness of FIB-4 false negatives

- **Evidence.**
  - The false-negative rate climbs to 37.7% at BMI ≥ 40 (`results/exp12`), exactly where LSM is least reliable.
  - The source applies no IQR/median filter, ignores the probe type and uses no CAP-aware threshold (`define_cohort.py`; replication.md pitfalls 3 and 11).
  - Jiang 2026 lists obesity, probe choice and exam quality as limitations, but does not quantify them.
  - Karlas et al. 2018 showed that steatosis (CAP) changes how LSM should be read.
- **Novelty check.** Searches 8, 9 and 10. No NHANES study re-estimates FIB-4 false negatives under defensible variations of the reference standard and the MASLD definition.
- **Open data:** `nhanes`. LUX files carry `LUXSIQRM`, `LUAPNME` (M or XL probe) and `LUXCAPM` in both cycles.
- **Design.**
  - *Hypothesis:* a meaningful share of obese "false negatives" disappears under stricter LSM reliability rules and CAP-aware thresholds, while diabetic false negatives persist.
  - *Methods:* a pre-registered multiverse (specification-curve) analysis. Vary:
    - LSM threshold: 8, 10 or 12 kPa;
    - reliability: IQR/median ≤ 30%, or not applied;
    - probe stratum: M or XL;
    - CAP-stratified LSM cut-offs, taken from published literature (`verify` the source before use);
    - alcohol rule: wrong per-day coding versus correct weekly grams;
    - viral exclusion: self-report versus serology;
    - MASLD definition: CAP 248 versus 274; Western versus Asian criteria;
    - FIB-4 cut-off: standard versus age-adjusted.

    For each specification, report the survey-weighted false-negative rate (`WTMECPRP` / `WTPH2YR`, strata and PSU) overall and by BMI class and diabetes status. As a sensitivity analysis, add a Bayesian latent-class model treating FIB-4, NFS and LSM as imperfect tests.
  - *Metrics:* false-negative rate and sensitivity, with design-based 95% CIs; the spread across specifications; and the share of the BMI ≥ 40 excess that each choice explains.
  - *Reporting guideline:* STARD 2015 (imperfect reference standard) and RECORD.
- **Rating:** feasibility 5, novelty 4, laptop, 3–4 weeks.

### Gap 4: The index test also has measurement error (AST, ALT, platelets near the 1.30 cut-off)

- **Evidence.** FIB-4 combines three lab values with sizeable analytical and within-person biological variation. No source analysis treats the 1.30 cut-off as uncertain. Every participant just under 1.30 counts as a certain "low risk".
- **Novelty check.** Search 11 found nothing on the probability of FIB-4 reclassification from biological or analytical variation. This is a laboratory-medicine angle that ML groups miss.
- **Open data:**
  - `nhanes` for the measured values;
  - published within-subject biological variation (CVI) and analytical CVs for AST, ALT and platelet count from the EFLM Biological Variation Database ([biologicalvariation.eu](https://biologicalvariation.eu/); record the exact CVs and their sources, `verify`).
- **Design.**
  - Use Monte Carlo resampling of each participant's AST, ALT and platelets within their combined CV.
  - Estimate each person's probability of being on the other side of 1.30 (and 2.67) on a repeat test.
  - Report the survey-weighted share of the "low risk" group in a measurement grey zone, and how many LSM-positive "false negatives" sit in that zone.
  - Propose an uncertainty band (e.g. 1.1–1.5) that triggers repeat testing, and compare its referral burden and yield with the age-adjusted and Jiang pathways.
  - Reporting guideline: STARD 2015.
- **Rating:** feasibility 5, novelty 4, laptop, 2 weeks. Strong fit for a pathologist, and it bears directly on Indian primary-care labs, where FIB-4 is often computed from a single LFT and CBC.

### Gap 5: Locked open-formula second-stage scores in the FIB-4 < 1.3 stratum, 2021–23

- **Evidence.**
  - The source compares FIB-4 Plus only with NFS and BMI.
  - Jiang 2026 states that SAFE could not be computed. But BIOPRO carries globulin (`LBXSGB`) in both cycles, so SAFE is computable. MAF-5 (waist, BMI, diabetes, AST, platelets) and LiverRisk (age, sex, glucose, cholesterol, AST, ALT, GGT, platelets) are also computable.
- **Novelty check.** Searches 6 and 7. The van Kleef head-to-head comparisons used pre-2021 NHANES data (cycles `verify`) and the whole metabolic-dysfunction population. No study was found that compares locked scores **within FIB-4 < 1.3** on 2021–23, with survey design and subgroups.
- **Open data:** `nhanes`.
- **Design.**
  - Compute FIB-4 Plus (locked on 2017–20), NFS, SAFE, MAF-5, LiverRisk and age-adjusted FIB-4 on the 2021–23 FIB-4 < 1.3 stratum, with no refitting.
  - Measure design-based AUROC, sensitivity at published cut-offs, calibration (where the score gives a probability), referrals per extra case found, and decision curves.
  - Break results down by BMI class, diabetes, sex and Asian ethnicity.
  - Take each formula from its original paper and record the citation; do not reuse code from papers without a licence.
  - Reporting guideline: TRIPOD+AI (validation) and STARD.
- **Rating:** feasibility 5, novelty 3, laptop, 3 weeks.

### Gap 6 (dropped): LLM phenotype descriptions

The Qwen2.5-32B phenotype text and its "LLM–SHAP concordance" (`exp06`, `exp07`, `exp15`) add little clinical value and need a 24 GB GPU. Using LLMs to predict MASLD fibrosis already has a proof of concept (Njei 2026, *Cureus*). Not pursued.

## Recommended extension

**Gaps 3 + 4 as the core, with Gap 5 as the clinical payoff.** Working title: *Missed or mismeasured? How much of FIB-4's "missed fibrosis" in MASLD survives correction for elastography artefacts and laboratory variation: a survey-weighted multiverse analysis of NHANES 2017–2023, with locked second-stage scores.*

1. Rebuild the source cohort with corrected alcohol, serology and LSM-quality rules (replication.md pitfalls 1–7), in both cycles with the correct weights.
2. Use a multiverse analysis to show how the false-negative rate, especially at BMI ≥ 40 and in diabetes, moves with reference-standard choices (Gap 3).
3. Estimate the measurement grey zone around FIB-4 1.30 from biological and analytical variation (Gap 4).
4. Among the false negatives that survive, compare locked SAFE, MAF-5, LiverRisk, NFS and FIB-4 Plus on 2021–23 (Gap 5). Report Asian and lean strata (Gap 2) as secondary, with honest CIs.

**Why this one:**
- **Novelty:** Jiang 2026 and Lasington 2026 have already done "validate a better model on 2021–23" and "stratify by race/lean". Nobody has asked whether the misses are real. The question rests on reference-standard and laboratory reasoning, which is a pathologist's home ground.
- **Feasibility:** open data with no registration, a laptop, and roughly 300 MB of files. The source code is MIT and ready to reuse.
- **Speed:** about 5 weeks to a preprint.
- **Journals:** the Indian or Asian-Pacific framing (lean MASLD, single-sample lab tests in primary care) suits Hepatology International (APASL, where the source was presented), Journal of Clinical and Experimental Hepatology (INASL), and the Indian Journal of Gastroenterology. All three have zero-APC subscription routes.

**Rating:** feasibility 5, novelty 3 (4 for Gaps 3–4 alone; the field is crowded, so be conservative), fit 4, laptop, 5 weeks.
