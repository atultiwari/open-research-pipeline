---
enriched: true
---
## What the original study did

Mohammad Ahmadullah Khan (BS Data Science, IIT Madras) looked for adults with metabolic dysfunction-associated steatotic liver disease (MASLD) whom FIB-4 calls "low risk" (FIB-4 < 1.30) but who have liver stiffness ≥ 8.0 kPa on FibroScan. The data were NHANES 2017–March 2020 (1,998 MASLD-eligible adults). He profiled these false negatives with XGBoost + SHAP and clustering, wrote phenotype descriptions with a local LLM (Qwen2.5-32B), and built a logistic "FIB-4 Plus" model (FIB-4 + HSI + waist + BMI) for the low-risk stratum. He compared it with the NAFLD Fibrosis Score (NFS). The work was an oral presentation at the APASL Single Topic Conference 2026 in Kumamoto (FP5-2, abstract 10340, 19 September 2026).

**Source status (checked 2026-11-06).** The source is a GitHub repository ([MAUK9086/masld-fib4](https://github.com/MAUK9086/masld-fib4), MIT licence, last commit 2026-11-03). The submitted abstract is in the repo at `results/APASL_STC2026_abstract.md`. No peer-reviewed paper or indexed abstract was found:
- OpenAlex author and title searches returned nothing;
- the APASL STC 2026 Kumamoto abstract book is not indexed in OpenAlex;
- Europe PMC preprint search found nothing.

The repo ships aggregate result CSVs, so most numbers can be checked against them.

**Directly replicable:** NHANES is open, and the code is MIT-licensed.

## Data

| Dataset | What | Access | How to get it |
| --- | --- | --- | --- |
| NHANES 2017–March 2020 pre-pandemic (`P_` files) | Development cycle. P_LUX: 10,409 elastography records (9,023 complete), ages 12+ | Open, no account | XPT files from `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/<FILE>.xpt` (doc page: same path with `.htm`, e.g. [P_LUX](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/P_LUX.htm)) |
| NHANES August 2021–August 2023 (`_L` files) | Temporal validation cycle. LUX_L: 7,199 records (6,280 complete); DEMO_L: 11,933 participants | Open, no account | `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/<FILE>.xpt` (e.g. [LUX_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/LUX_L.htm)); [cycle overview](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2021-2023) |

**Files and variables.** All doc pages were fetched on 2026-11-06.

| Purpose | 2017–2020 | 2021–2023 | Key variables (and naming changes) |
| --- | --- | --- | --- |
| Elastography | P_LUX | [LUX_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/LUX_L.htm) | `LUAXSTAT` (1 = complete), `LUXSMED` (LSM, kPa), `LUXSIQRM` (IQR/median), `LUXCAPM` (CAP), `LUAPNME` (probe/wand type) |
| Demographics and design | P_DEMO | [DEMO_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.htm) | `RIDAGEYR`, `RIAGENDR`, `RIDRETH3` (6 = non-Hispanic Asian), `SDMVSTRA`, `SDMVPSU`; weights `WTMECPRP` (2017–20) and `WTMEC2YR` (2021–23) |
| Chemistry | P_BIOPRO | [BIOPRO_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BIOPRO_L.htm) | `LBXSASSI` (AST), `LBXSATSI` (ALT), `LBXSGTSI` (GGT), `LBXSAL` (albumin), `LBXSGB` (globulin), `LBXSGL` (non-fasting glucose), `LBXSTR` (non-fasting triglycerides). **2021–23 carries `WTPH2YR`** |
| Blood count | P_CBC | [CBC_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/CBC_L.htm) | `LBXPLTSI` (platelets) |
| Body measures | P_BMX | [BMX_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BMX_L.htm) | `BMXBMI`, `BMXWAIST`, `BMXHT` |
| HbA1c | P_GHB | [GHB_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/GHB_L.htm) | `LBXGH` |
| Fasting triglycerides | P_TRIGLY (`LBXTR`, `WTSAFPRP`) | [TRIGLY_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/TRIGLY_L.htm) | **Renamed `LBXTLG`** in 2021–23; fasting subsample only (`WTSAF2YR`) |
| HDL | P_HDL | [HDL_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HDL_L.htm) | `LBDHDD` |
| Blood pressure | P_BPXO, P_BPQ | [BPXO_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BPXO_L.htm), [BPQ_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BPQ_L.htm) | `BPXOSY1-3`, `BPXODI1-3`. Medication: **`BPQ040A` (2017–20) became `BPQ150` (2021–23)** |
| Diabetes | P_DIQ | [DIQ_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DIQ_L.htm) | `DIQ010` |
| Alcohol | P_ALQ | [ALQ_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/ALQ_L.htm) | `ALQ121` (how often), `ALQ130` (drinks **on drinking days**) |
| Hepatitis B serology | P_HEPBD | [HEPBD_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HEPBD_L.htm), [HEPB_S_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HEPB_S_L.htm) | `LBDHBG` (HBsAg), `LBXHBC` (anti-HBc), `LBXHBS` (anti-HBs) |
| Hepatitis C serology | P_HEPC | [HEPC_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HEPC_L.htm) | `LBXHCR` (HCV RNA), `LBDHCI` (confirmed antibody) |
| Self-reported hepatitis | P_HEQ (`HEQ010` HBV, `HEQ030` HCV) | [HEQ_L](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/HEQ_L.htm) | **Only `HEQ010` in 2021–23**; there is no self-reported HCV item |

**Answer to the register note:** hepatitis B serology does exist for 2021–23 (HEPBD_L and HEPB_S_L, both with `WTPH2YR`). So HBV and HCV can be excluded on serology in both cycles.

**Weights.**
- The LUX_L documentation says to use examination (MEC) weights for elastography, unless the data are merged with a more restricted subsample.
- FIB-4 needs phlebotomy labs. The NHANES weighting tutorial says that phlebotomy weights (`WTPH2YR`) were introduced for the first time in 2021–23, to correct nonresponse to the blood draw. Use `WTPH2YR` for 2021–23 analyses.
- For 2017–2020, use `WTMECPRP`. The P_LUX documentation warns that these weights apply only to the combined 2017–March 2020 file, not to 2019–2020 on its own.
- Always use `SDMVSTRA` and `SDMVPSU` for variance estimates.
- Do not combine the two cycles' weights without following the NCHS guidance for pooling cycles.

**Terms.** Under the [NCHS data use agreement](https://www.cdc.gov/nchs/policy/data-user-agreement.html) the data may be used for statistical analysis only. Users must not attempt re-identification and must not link the data with identifiable records. The data are public-use with no account, but **do not commit XPT or derived row-level files**.

**Storage.** All the needed XPT files for both cycles total roughly 200–300 MB (`verify`; the README estimates ~200 MB for 2017–2020, and LUX_L.xpt is ~0.77 MB). Keep them under `data/raw/` (gitignored).

## Environment

From the repo's `requirements.txt` and README:
- Python 3.12, `numpy 1.26.4`, `pandas 2.2.3`, `scipy 1.13.1`, `pyreadstat 1.2.8`, `scikit-learn 1.5.2`, `xgboost 2.1.3`, `optuna 4.0.0`, `shap 0.46.0`, `umap-learn 0.5.7`, `hdbscan 0.8.40`, `statsmodels 0.14.4`, `matplotlib`, `seaborn`, `pyarrow`, `pyyaml`, `pytest`.
- The LLM steps (exp06, exp07, exp15) need `llama-cpp-python` built for CUDA, plus 24 GB VRAM for Qwen2.5-32B Q4. **Skip them.** They are not needed for the FIB-4 numbers or for the extension.
- For design-based statistics, add the R `survey` package (via `rpy2` or a separate R script) or the Python `samplics` package. The repo's `stats_utils.py` only does weighted proportions, with a plain bootstrap.

## Step-by-step replication

1. Clone the [source repo](https://github.com/MAUK9086/masld-fib4) into a work folder **outside** this repo. Create a fresh venv and `pip install -r requirements.txt`, but leave out the `llama-cpp-python` build in `setup.sh`.
2. **Fix the download URLs first.** `config.yaml` points to `https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/<FILE>.XPT`, and the script's alternative tries `.../nhanes/2019/DataFiles/`. On 2026-11-06 both returned an **HTML page with a success status, not an XPT file**. The script would save that HTML as `.XPT` and report success. Change the URL pattern to `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/<FILE>.xpt` (lower-case `.xpt`). Then check that every file starts with `HEADER RECORD`.
3. `python src/download_nhanes.py`, then `merge_nhanes.py` and `define_cohort.py`. Compare `results/exp01/cohort_flowchart.txt`: 10,409 → 8,965 adults → 7,768 complete scans → 2,143 MASLD → 1,998 with FIB-4.
4. Run `exp02` (misclassification), `exp04` (XGBoost/SHAP), `exp08` (ethnicity), `exp09` (FIB-4 Plus), `exp12` (BMI groups) and `exp17` (sensitivity). Skip exp05–07 if you are not doing the clustering or LLM arms.
5. Compare your numbers with the committed CSVs (target numbers below).
6. **Re-run with the corrections listed under pitfalls 1–6**, and record how much each changes the false-negative rate. This becomes the baseline for the extension.

## Compute and cost

- **Laptop** (CPU, 8–16 GB RAM) for everything except the LLM steps. The Optuna HPO in exp04 takes about 30–60 minutes, per the README.
- The LLM arm needs a 24 GB GPU overnight. It is optional and not recommended here.
- No API cost.

## Target numbers

From the abstract and the repo result files:

| Quantity | Value | Where |
| --- | --- | --- |
| MASLD-eligible adults | 1,998 | abstract; `results/exp01/cohort_flowchart.txt` |
| FIB-4 < 1.30 | 1,390 (70%) | abstract |
| LSM ≥ 8 kPa among FIB-4 low risk | 16.6% weighted (95% CI 13.5–20.0); 15.8% unweighted (220/1,390) | `results/exp02/population_extrapolation.txt`; `results/exp17/sensitivity_summary.csv` |
| False-negative rate by BMI (< 25 / 25–30 / 30–40 / ≥ 40) | 5.1 / 5.4 / 15.5 / 37.7% | `results/exp12/bmi_group_fn_rates.csv` |
| Diabetes vs no diabetes | 29.8% vs 11.8% | abstract |
| Weighted false-negative rate in non-Hispanic Asian adults | 11.4% (25/199) | `results/exp08/false_negative_rates_by_ethnicity.csv` |
| AUROC in low-risk stratum, 20% test split: FIB-4 Plus / NFS / BMI alone | 0.837 (0.773–0.898) / 0.749 / 0.793 | `results/exp09/fib4plus_vs_fib4_auroc.csv` |
| DeLong FIB-4 Plus vs NFS; NRI | p = 0.019; NRI 9.2% | `results/exp09/` |
| Lean MASLD false negatives | **n = 3** | `results/exp12/lean_masld_fn_profile.csv` |

## Known pitfalls

These come from reading the code (commit `f8889b1`) and the CDC documentation.

1. **Alcohol is mis-coded.** `define_cohort.py` treats `ALQ130` as drinks per day (> 2.14 for men, > 1.43 for women). The CDC codebook defines it as the average number of drinks *on the days the person drank*. This over-excludes people who drink rarely but have several drinks when they do. Compute weekly intake from `ALQ121` (frequency) × `ALQ130`, then apply the MASLD/MetALD thresholds (e.g. > 210 g/week for men and > 140 g/week for women, as in Jiang et al. 2026).
2. **Viral hepatitis is excluded on self-report only** (`HEQ010`/`HEQ030`). `HEQ030` does not exist in 2021–23. Use serology in both cycles: HBsAg (`LBDHBG`) and HCV RNA (`LBXHCR`).
3. **No LSM quality filter.** Only `LUAXSTAT == 1` is used. The `lux_iqr_ratio_max: 30` value in `config.yaml` is never applied. Add IQR/median ≤ 30% (`LUXSIQRM`) as a sensitivity rule, and record the probe type (`LUAPNME`).
4. **Weights and variance.**
   - Proportions use `WTMECPRP`, but the confidence intervals come from a plain bootstrap that ignores strata and PSUs.
   - The AUROCs, DeLong test and NRI are unweighted.
   - For 2021–23, use `WTPH2YR` (phlebotomy) rather than `WTMEC2YR`.
5. **FIB-4 Plus is optimistic.**
   - Its three features were chosen from SHAP on the whole low-risk stratum *before* the 80/20 split.
   - It was evaluated on one split (about 280 test participants and about 44 events, if no rows are dropped).
   - The Youden cut-off was chosen on the test set.
   - `class_weight="balanced"` distorts the predicted probabilities, so calibration is invalid unless refitted.
6. **The CAP ≥ 248 sensitivity analysis is broken.** `results/exp17/sensitivity_masld_definition.csv` gives the same n = 1,390 and the same rate for CAP ≥ 248 as for CAP ≥ 274, so the cohort was not re-derived.
7. **Fasting variables.**
   - The glucose criterion uses non-fasting serum glucose (`LBXSGL`) as if it were fasting glucose.
   - The triglyceride criterion uses the fasting-subsample `LBXTR`, which is missing for about half of participants. Missing values silently count as "criterion not met". Use `LBXSTR` (non-fasting, BIOPRO) or HbA1c and medication.
8. **No age-adjusted FIB-4 cut-off** (2.0 at age ≥ 65) is applied, although AASLD/EASL guidance uses it.
9. **Lean MASLD and Asian subgroups are tiny.**
   - Only 3 lean false negatives were found in 2017–2020.
   - DEMO_L has only 681 non-Hispanic Asian participants, against 1,638 in P_DEMO. Jiang et al. had 107 Asian adults in their 2021–23 MASLD cohort.
   - Pool the two cycles for subgroup work, and report imprecision honestly.
10. **Variable renames between cycles:** `LBXTR` → `LBXTLG`, `BPQ040A` → `BPQ150`, and `HEQ030` was dropped. Code that only looks up the old names silently fills `NaN`.
11. **Reference standard.** LSM ≥ 8 kPa is a screening phenotype, not histology. Stiffness can be raised by obesity, steatosis/CAP, inflammation and probe choice (Karlas et al., *Aliment Pharmacol Ther* 2018, [doi:10.1111/apt.14529](https://doi.org/10.1111/apt.14529)). Some of the "false negatives" at BMI ≥ 40 may be false positives on LSM.

## Claude Code task list

1. Clone the source repo outside this repo, patch the download URL (step 2), and add `data/` handling that writes only to a gitignored path.
2. Download the 2017–2020 files and confirm every XPT header; reproduce the exp01 flowchart.
3. Run exp02, exp04, exp08, exp09, exp12 and exp17; tabulate them against the target numbers.
4. Write `harmonise.py`, which maps 2017–20 and 2021–23 variables (renames above) to one schema and adds a `cycle` column.
5. Write `cohort_v2.py`, with serology-based viral exclusion, weekly alcohol grams, an IQR/median flag, a probe flag, non-fasting triglycerides and an age-adjusted FIB-4 flag.
6. Re-estimate the false-negative rate with design-based SEs (R `survey` or `samplics`), using `WTMECPRP` for 2017–20 and `WTPH2YR` for 2021–23.
7. Save only aggregate tables (counts, weighted rates, CIs) to `results/`. Commit code and aggregates only; never commit XPT or row-level parquet files.
