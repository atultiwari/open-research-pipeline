---
enriched: true
---
## What the original study did

Negrini, Pighi, Mignolli, Salvagno and Lippi (Section of Clinical Biochemistry, University of Verona) asked whether a routine blood count can flag people whose iron studies will come back low. They took 32,437 outpatients aged 10–99 from their laboratory information system (January 2023 to January 2026) who had a CBC, serum iron, ferritin and transferrin from the same blood draw. Two targets were defined with sex-specific cut-offs: low ferritin (< 30 µg/L in women, < 50 µg/L in men; 44.2% positive) and low transferrin saturation (< 15% in women, < 20% in men; 24.0% positive). Nine inputs were used (age, sex, RBC, Hb, Hct, MCV, MCH, MCHC, RDW). They compared nine classifiers in R/caret on a 70/30 stratified split with repeated 10-fold cross-validation. XGBoost was best for both targets, and MCH (ferritin) and MCV (transferrin saturation) were the top random-forest features.

**Source status (checked 2026-11-06).**
- Preprint: Preprints.org, 2 April 2026, [doi:10.20944/preprints202604.0073.v1](https://doi.org/10.20944/preprints202604.0073.v1). Crossref links it to the journal version (`is-preprint-of`).
- **Peer-reviewed version:** *Journal of Clinical Medicine* 2026;15(12):4783, published 19 June 2026, [doi:10.3390/jcm15124783](https://doi.org/10.3390/jcm15124783), CC BY 4.0, PMID 42355951, open full text at [PMC13302493](https://pmc.ncbi.nlm.nih.gov/articles/PMC13302493/). This guide uses the journal version.
- The scripts were written in R 4.5.2 and are not shared. The data are "available on request" from the corresponding author.

**Not directly replicable.** The Verona data are private and there is no code. The closest open surrogate is **NHANES 2017–March 2020**, the only recent NHANES cycle that measured ferritin in men and older adults as well as women (see Data). It has the same nine inputs, ferritin on a Roche immunoassay, and transferrin saturation. The population is different: a national household sample rather than outpatients sent for iron studies. So the replication tests whether the *method* holds up, not whether the Verona numbers come out the same.

## Data

| Dataset | Role | Access | How to get it |
| --- | --- | --- | --- |
| NHANES 2017–March 2020 pre-pandemic (`P_` files) | Development (surrogate for the Verona cohort) | Open, no account; NCHS data use agreement | XPT files from `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/<FILE>.xpt`; doc pages are the same path with `.htm`, e.g. [P_FERTIN](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_FERTIN.htm) |
| NHANES 2017–2018 (`_J` files) | Alternative development set (one cycle, as in the register note) | Same | [FERTIN_J](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/FERTIN_J.htm), [FETIB_J](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/FETIB_J.htm), [CBC_J](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/CBC_J.htm), [HSCRP_J](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/HSCRP_J.htm) |
| NHANES August 2021–August 2023 (`_L` files) | Temporal validation (extension) | Same | [FERTIN_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/FERTIN_L.htm), CBC_L, HSCRP_L, DEMO_L |
| Kenya IFCC healthy adults (`kenya-ifcc-iron`) | External validation (extension) | Open, CC BY 4.0, no account | [Figshare doi:10.6084/m9.figshare.21107986](https://doi.org/10.6084/m9.figshare.21107986); one 50 KB Excel file |
| Yemeni hospital CBC (Mendeley Data) | **Excluded** (was the planned external set) | — | excluded: de-identification and data-quality concerns found on 2026-11-06, pending clarification with the depositors; see pitfall 9 |

**Who had ferritin measured in NHANES (CDC doc pages, fetched 2026-11-06).** This matters more than anything else in the design.

| Cycle | Ferritin file | Eligible | Values |
| --- | --- | --- | --- |
| 2015–2016 | FERTIN_I | Children 1–5 and **females 12–49 only** | 2,684 |
| 2017–2018 | FERTIN_J | Children 1–5 and **everyone aged 12+** | 6,589 of 7,332 records |
| 2017–March 2020 | P_FERTIN | Children 1–5 and everyone aged 12+ | 10,557 of 11,983 records |
| 2021–2023 | FERTIN_L | Children 1–5 and **females 12–49 only** | `WTPH2YR` carried in the file |

- Serum iron, TIBC and transferrin saturation (FETIB_J / P_FETIB, `LBDPCT`) cover ages 12+. There is no FETIB_L page for 2021–23 (HTTP 404), so transferrin saturation cannot be validated temporally.
- Soluble transferrin receptor (TFR_J, ages 1–5 and 12+) allows a body-iron sensitivity label in 2017–18.
- CBC (CBC_J, P_CBC, CBC_L; ages 1+) is measured on a **Beckman Coulter DxH 800** in the mobile examination centre. Variables: `LBXRBCSI`, `LBXHGB`, `LBXHCT`, `LBXMCVSI`, `LBXMCHSI`, `LBXMC` (MCHC, g/dL), `LBXRDW`, `LBXPLTSI`, `LBXWBCSI`.
- hs-CRP: `LBXHSCRP` (HSCRP_J, P_HSCRP, HSCRP_L).
- Demographics and design: `RIDAGEYR` (top-coded at 80), `RIAGENDR`, `RIDEXPRG` (pregnancy), `SDMVSTRA`, `SDMVPSU`.

**Weights** (same logic as `fib4-nhanes-extval`).
- 2017–2018 and 2017–March 2020 lab files have no phlebotomy weight. Use `WTMEC2YR` (J files) or `WTMECPRP` (P_ files). The P_ weights are valid only for the combined 2017–March 2020 file.
- 2021–2023: use `WTPH2YR` (phlebotomy weight, in FERTIN_L and CBC_L).
- Always pass `SDMVSTRA` and `SDMVPSU` to the variance estimator. Do not pool cycle weights without the NCHS pooling guidance.
- Model fitting can be unweighted. Report **prevalence, calibration and net benefit with weights**, because those are the population claims.

**Terms.** NHANES falls under the [NCHS data use agreement](https://www.cdc.gov/nchs/policy/data-user-agreement.html): statistical analysis only, no re-identification, no linkage. **Do not commit XPT or row-level derived files.** All needed XPT files are a few tens of MB (`verify`). Keep them under `data/raw/` (gitignored), or outside the repo.

## Environment

The source used R 4.5.2 with `caret`, `xgboost`, `e1071`, `pROC` (DeLong CIs) and caret's `rf`, `rpart`, `svmRadial` and `knn`. Two options:
- **Faithful replication:** R ≥ 4.4 with `caret`, `randomForest`, `rpart`, `kernlab`, `xgboost`, `e1071`, `pROC`, `haven` (reads XPT) and `survey`.
- **Python (recommended for the extension):** Python 3.11, `pandas`, `pyreadstat`, `scikit-learn`, `xgboost`, `tabpfn` (check the licence of the model weights before use, `verify`), `samplics` or R `survey` through `rpy2`, `dcurves` (decision curves), `matplotlib`.

## Step-by-step replication

1. **Download** P_DEMO, P_CBC, P_FERTIN, P_FETIB and P_HSCRP (and the J equivalents if you want 2017–18 alone). Use the URL pattern in the table, with a lower-case `.xpt`. Check that each file starts with `HEADER RECORD`: the fib4 study found NHANES URLs that return an HTML page with HTTP 200.
2. **Merge on `SEQN`.** Keep ages 12–80, drop pregnant participants (`RIDEXPRG == 1`), and keep complete cases for the nine inputs and the target. Report the flowchart with counts.
3. **Harmonise units to the source.** Hb g/dL → g/L (× 10); Hct % → L/L (÷ 100); MCHC g/dL → g/L (× 10); ferritin `LBDFERSI` (µg/L) unchanged.
4. **Labels exactly as in the source.**
   - Low ferritin: < 30 µg/L in women, < 50 µg/L in men.
   - Low TSAT: `LBDPCT` < 15% in women, < 20% in men.
   - NHANES computes TSAT from iron/TIBC; the source used iron/transferrin. Note this difference.
5. **Split and tune as the source did.** 70/30 split stratified on the label, with a fixed seed. Repeated 10-fold CV (3 repeats) on the training set, optimising AUC. Use the same nine model specifications and grids (journal Methods, section 2.3). For XGBoost: `nrounds` 50/100/150, `max_depth` 3/6, `eta` 0.1/0.3.
6. **Test-set metrics.** Accuracy, balanced accuracy, sensitivity, specificity, PPV, NPV and F1 at a 0.5 threshold; AUC with DeLong 95% CI; pairwise DeLong tests against the best model; Brier score. Also extract random-forest Gini importance.
7. **Repeat on 2017–18 alone** (J files) to answer the register's version of the question.
8. Write all tables to `results/replication/` as aggregates only.

## Compute and cost

- Laptop CPU. The RF/SVM grids on about 7,000–9,000 training rows take minutes to an hour. No GPU and no API cost for the replication.

## Target numbers

From the *J Clin Med* version (Tables 1 and 2; test set n = 9,730):

| Target | Model | AUC (95% CI) | Sens / Spec | Brier |
| --- | --- | --- | --- | --- |
| Low ferritin (44.2% positive) | XGBoost | 0.858 (0.851–0.866) | 0.749 / 0.843 | 0.147 |
| | Tuned random forest | 0.853 | 0.748 / 0.831 | 0.151 |
| | Logistic regression | **0.663** | 0.458 / 0.781 | 0.228 |
| Low TSAT (24.0% positive) | XGBoost | 0.801 (0.791–0.812) | 0.393 / 0.937 | 0.139 |
| | Logistic regression | 0.750 | 0.221 / 0.958 | 0.154 |

- Top random-forest features: MCH for ferritin, MCV for TSAT (Figures 5–6).
- **Mismatch to flag:** the abstract reports AUC ranges of 0.80–0.87 for ferritin and **0.85–0.96 for transferrin saturation**. But the transferrin-saturation table tops out at 0.801. Use the tables.
- Expect lower AUCs and a much lower prevalence of low ferritin in NHANES, because it is a household sample rather than patients already sent for iron studies. Success means the same *ranking* (boosting ≥ RF > LR) and similar feature importance, not the same AUC.

## Known pitfalls

1. **The logistic-regression baseline is probably mis-specified.** An LR AUC of 0.663 against 0.858 for XGBoost is a far bigger gap than other CBC-only ferritin models report (e.g. Efros et al. 2025: CBC-only AUC 0.741). The likely causes are linear terms only, with no age × sex interaction, while the label uses sex-specific cut-offs, in a cohort with a median age of 65. Fit LR with restricted cubic splines and an age × sex interaction before claiming that boosting is needed.
2. **Unusual label.** A ferritin cut-off of 50 µg/L in men, against 30 in women, is not a standard definition. It pushes prevalence to 44%. Report the conventional 15 and 30 µg/L cut-offs too, plus an inflammation-aware version (extension, Gap 4).
3. **No inflammation markers in the source.** Ferritin rises with inflammation; the authors list this as a limitation. NHANES has hs-CRP, so you can test it.
4. **The 0.5 threshold and the Brier score are the only calibration information.** There are no calibration plots, calibration slope or intercept, or decision curves.
5. **Analyser shift.** The source used a Sysmex XN; NHANES and Kenya used Beckman Coulter instruments. RDW and MCHC are the least transferable indices across analysers. Report models with and without them.
6. **Survey design.** Weighted prevalence and calibration need `WTMECPRP`/`WTMEC2YR` with strata and PSUs. Unweighted AUCs are acceptable for discrimination but say so.
7. **Ferritin eligibility differs by cycle** (table above). Code that assumes "ferritin = women 12–49" (true for 2015–16 and 2021–23) silently drops men and older adults in 2017–2020. The reverse mistake inflates temporal-validation claims.
8. **Label leakage in related work.** Papers that predict iron-deficiency *anaemia* (low ferritin **and** low Hb) from a CBC that includes Hb have half the label inside the inputs. Do not compare your AUCs with theirs unless the labels match.
9. **Yemeni dataset excluded.** The register's planned external set (Mendeley Data) was excluded: de-identification and data-quality concerns found on 2026-11-06, pending clarification with the depositors. It also showed undeclared duplicates and implausible values. Do not use or download it unless Atul clears it.
10. **Age top-coding** at 80 in NHANES, and the source's lower age limit of 10 (NHANES ferritin starts at 12). State the age range used.

## Claude Code task list

1. Create `data/raw/nhanes/` (gitignored). Download P_DEMO, P_CBC, P_FERTIN, P_FETIB and P_HSCRP (and the J files), then verify the `HEADER RECORD` of every file.
2. Write `src/build_cohort.py`: merge, exclusions, unit harmonisation, labels (source definition plus 15/30 µg/L), and a flowchart with counts.
3. Write `src/replicate_source.R` (caret, faithful) or `src/replicate_source.py` (sklearn/xgboost equivalents). Run both targets on P_ and on J.
4. Add `src/lr_splines.py`: LR with splines and an age × sex interaction, to test pitfall 1.
5. Produce weighted prevalence tables (`samplics` or R `survey`) and a test-set metrics table that matches the layout of the paper's Tables 1 and 2.
6. Save only aggregate CSVs and figures to `results/replication/`. Never commit XPT, parquet or row-level files.
