---
enriched: true
---
## What the original study did

Vaidya, Chen, Williamson and colleagues (Mahmood Lab; *Nature Medicine* 2024) trained attention-based multiple-instance learning (ABMIL and other MIL) models on whole-slide images and then measured performance separately for white, Black and Asian patients. There were three tasks:
- breast carcinoma subtyping (IDC vs ILC), trained on TCGA-BRCA (1,049 slides) and tested on a private Mass General Brigham cohort (MGB-breast, 1,265 slides);
- lung carcinoma subtyping (LUAD vs LUSC), trained on TCGA-LUAD/LUSC (1,043 slides) and tested on MGB-lung (1,960 slides);
- *IDH1* mutation prediction in gliomas, trained on the EBRAINS Digital Brain Tumour Atlas (873 slides) and tested on TCGA-GBMLGG (1,123 slides).

They compared patch encoders (ImageNet ResNet50, CTransPath, UNI), MIL architectures, Monte Carlo vs site-preserving splits, stain normalisation and bias-mitigation methods, and reported race-stratified AUC and true-positive-rate (TPR) disparity. The abstract reports white–Black AUC gaps of 3.0% (breast), 10.9% (lung) and 16.0% (*IDH1*) with common pipelines. The foundation model (UNI) narrowed these gaps but did not close them.

**Replicability verdict: partly replicable.**
- **Replicable on open data:** the *IDH1* arm (EBRAINS → TCGA-GBMLGG). Both cohorts are open, and the repository ships Monte Carlo splits for this task.
- **Not directly replicable:** the breast and lung arms, because the external test cohorts (MGB) are private. The closest open surrogate is CPTAC (CPTAC-BRCA, CPTAC-LUAD, CPTAC-LSCC). Its race mix differs, though: many Asian patients and almost no Black patients (see Data). So the surrogate can test white vs Asian gaps externally, but not white vs Black.
- **Full text:** the article is paywalled and not in PMC or Europe PMC (checked 2026-11-06). This guide uses the abstract, the figure and Extended Data legends on the publisher page, and the code repository. Anything taken from the Methods is marked **verify**.

## Data

| Dataset | Registry id | Access | How to get it | Size |
| --- | --- | --- | --- | --- |
| UNI2-h patch features, TCGA + CPTAC | `uni2h-features-tcga` | HF account; gated, auto-approved | `hf download sofieneb/uni2h_features --repo-type dataset --include "TCGA/TCGA-LUAD/*" "TCGA/TCGA-LUSC/*" "CPTAC/CPTAC_LUAD/*" "CPTAC/CPTAC_LSCC/*" --local-dir data/feats/uni2h` | 914 GB in all; lung subset ≈ 15% (1,683 slides) |
| CONCH v1.5 / Virchow2 / GigaPath features (same slides) | `conch-v15-features-tcga`, `virchow2-features-tcga`, `gigapath-features-tcga` | HF account; gated, auto-approved | same `--include` pattern | 121 GB / 1.97 TB / 914 GB in all |
| TCGA clinical data and (optional) WSIs | `tcga` | Open, no login | GDC API or portal for `demographic.race`, `diagnoses.age_at_diagnosis`, `tissue_source_site`, `primary_diagnosis`; GDC Data Transfer Tool only if you need raw slides | Slides: hundreds of GB per project |
| CPTAC clinical data and (optional) WSIs | `cptac` | Open, no login (TCIA, CC BY 4.0) | Clinical data from the GDC (project `CPTAC-3`) or PDC; slides via TCIA Aspera | LUAD 431.5 GB, LSCC 414 GB, BRCA 113.29 GB |
| EBRAINS Digital Brain Tumour Atlas (for the *IDH1* arm only) | `ebrains-brain-tumour-atlas` | Free EBRAINS account + data use agreement (non-commercial) | via [doi:10.25493/WQ48-ZGX](https://doi.org/10.25493/WQ48-ZGX) | 3,115 slides; download size verify |

**Demographics that shape the design** (GDC API, 2026-11-06):
- **TCGA lung:** 1,089 cases. 744 white, 84 Black, 17 Asian. The 84 Black patients come from 20 of 43 tissue source sites, and three sites hold 46% of them.
- **CPTAC-3 lung:** 339 cases. 192 white, 131 Asian (108 LUAD, 23 LUSC), 6 Black.
- **TCGA-BRCA:** 757 white, 183 Black, 61 Asian.

Storage tips:
- Download only the lung (and optionally breast) folders, onto a RunPod network volume. The UNI2-h lung subset is about 130 GB (an estimate from the share of slides).
- Keep everything under `data/` (gitignored). Never commit features, slide-level predictions joined to patient IDs, or demographic tables. Commit aggregate metrics only.

## Environment

The [CPATH_demographics repo](https://github.com/mahmoodlab/CPATH_demographics) lists Python 3.8.13, PyTorch 2.0.0 (CUDA 11.7), openslide-python 1.2.0, scikit-learn 1.2.1, pandas 1.5.3, slideflow 2.1.0 and smooth-topk. Its code is adapted from [CLAM](https://github.com/mahmoodlab/CLAM) (GPL-3.0).

For the feature-based workflow, a modern stack is enough:
- Python 3.10+, `torch`, `h5py`, `huggingface_hub[hf_transfer]`;
- `scikit-learn`, `pandas`, `scipy` and `statsmodels` (for mixed-effects and equivalence tests);
- `fairlearn` (optional, for metric helpers).

[TRIDENT](https://github.com/mahmoodlab/TRIDENT) is needed only if you extract features yourself, for example for the spot-check or the optional ResNet50 baseline.

**Code licences:** the CPATH_demographics LICENSE file is CC BY-NC-ND 4.0 (GitHub shows NOASSERTION). So is TRIDENT's. You can run them unmodified for non-commercial research. Write your own MIL and metric code rather than publishing modified copies.

## Step-by-step replication

**Arm A: the source study's open *IDH1* arm (replication anchor)**
1. Request EBRAINS access. Download the glioma slides that match the repo's `splits_MonteCarlo/Ebrains_IDH1Mutation` list, and the TCGA-GBM/LGG diagnostic slides listed in `splits_MonteCarlo/TCGA_GBMLGG/test.csv`.
2. Tile at 20× and extract UNI features with TRIDENT. The UNI2-h set has no EBRAINS features, so this step needs raw slides.
3. Run `commands/IDH1.sh` (ABMIL, 20 Monte Carlo folds), then `analysis/compute_TPR_disparity.py` on the TCGA-GBMLGG test set.
4. Compare race-stratified AUC and TPR disparity with Extended Data Fig. 3 (UNI panel).

**Arm B: open surrogate for lung (and breast) subtyping**
1. Download the lung UNI2-h features (TCGA-LUAD/LUSC, CPTAC_LUAD/LSCC). Build a slide table with `case_id = slide_id[:12]` for TCGA, and the CPTAC case ID from the file name (C3L-/C3N- prefix, verify the parsing).
2. Pull from the GDC API: race, ethnicity, age at diagnosis, sex, `tissue_source_site` (TCGA) and primary diagnosis. Label LUAD = 0, LUSC = 1. Drop CPTAC normal-tissue slides; the TCIA counts include them.
3. **Splits on TCGA:**
   - (i) 20-fold Monte Carlo patient-level splits;
   - (ii) 10-fold site-preserving splits, with no tissue source site in both train and test, as the paper did (Extended Data Figs 1–2).
4. Train ABMIL (gated attention, 1536 → 512 → 256 hidden, dropout 0.25) with class-balanced sampling. Train on TCGA, pick the epoch on a TCGA validation fold, then test on the whole CPTAC lung set without touching it.
5. Report overall AUC, race-stratified AUC, and TPR disparity (taken here as subgroup TPR minus overall TPR; confirm the paper's exact definition, verify; at the 0.5 threshold and at a threshold fixed on TCGA validation), with 95% bootstrap CIs over patients and the spread across folds.
6. Repeat on the TCGA internal test folds, so that internal and external disparity can be compared.
7. Optional breast arm: TCGA-BRCA IDC vs ILC → CPTAC_BRCA (112 slides). Count the ILC cases first (verify). ILC is probably too rare in CPTAC-BRCA for a race-stratified estimate.

## Compute and cost

| Task | Where | Time | Cost |
| --- | --- | --- | --- |
| Download lung features (~130 GB per encoder) | RunPod volume or a university server | a few hours | ~US$5/month storage |
| ABMIL, 30 runs (20 Monte Carlo + 10 site folds) × 1 encoder | 1 × RTX 4090 / L4 | ~3–5 GPU-h | ~US$2–4 |
| Same for 3 more encoders | same | ~10–15 GPU-h | ~US$8–12 |
| *IDH1* arm, including feature extraction for ~2,000 slides | RunPod A40/L40S | ~15–25 GPU-h, plus slide download | ~US$15–25 |
| Statistics | Laptop | | |

## Target numbers

- **Abstract:** white–Black AUC gaps of 3.0% (breast), 10.9% (lung) and 16.0% (*IDH1*) with common modelling approaches. The text also reports smaller gaps with UNI (values: verify; paywalled Results).
- ***IDH1* arm:** race-stratified ROC and TPR disparity for ABMIL + UNI, 20 folds (Extended Data Fig. 3 G–I). Read the values from the figure (verify).
- **Lung and breast:** the MGB results cannot be reproduced. Report the CPTAC results as a new open benchmark, not as a replication.
- **Cohort sizes to match:** TCGA-BRCA 1,049, TCGA-lung 1,043, EBRAINS 873, TCGA-GBMLGG 1,123 slides. The UNI2-h set has 1,053 TCGA lung and 1,133 TCGA-BRCA slides; the difference comes from the authors' slide filtering (verify).

## Known pitfalls

- **Race is confounded with site.** In TCGA, Black patients cluster in a few tissue source sites, and foundation-model features encode the site strongly (de Jong et al., arXiv 2501.18055; Zhang, ISBI 2026 / arXiv 2508.14779). A random split lets the model learn site, which can inflate or hide race gaps. Always report both split types.
- **Small subgroups.** CPTAC lung has 6 Black patients, so no white–Black external estimate is possible. TCGA lung has 17 Asian patients, so models are trained with almost no Asian examples. Report CIs and minimal detectable differences. Do not report point gaps alone.
- **TPR disparity depends on the threshold.** Fix the threshold on TCGA validation data. Also report AUC (threshold-free) and per-group calibration.
- **Frozen vs FFPE.** FAIR-Path describes its CPTAC-3 slides as frozen sections; TCGA diagnostic slides are FFPE. Check the preparation of each CPTAC slide you use (verify). A preparation shift would confound the external drop.
- **Third-party features.** Spot-check 5–10 slides by re-extracting UNI2-h features with TRIDENT and comparing cosine similarity. Patch sizes differ between sibling feature sets (224/256/512 px).
- **Licence layering.** The features and UNI2-h are CC BY-NC-ND, TCIA slides are CC BY 4.0, and the code is CC BY-NC-ND. Keep the work non-commercial, and never redistribute features.
- **Race labels** in the GDC are self-reported or registry-recorded, with many "not reported". Exclude those patients from the race analyses, but keep them in the overall metrics.

## Claude Code task list

1. Create `analysis/fairness-tcga-cptac/` with `pyproject.toml` (torch, h5py, huggingface_hub, scikit-learn, pandas, statsmodels). Confirm that `data/` is gitignored.
2. `fetch_clinical.py`: query the GDC API for TCGA-LUAD/LUSC/BRCA and CPTAC-3 lung cases. Write `data/clinical.parquet`, and commit only an aggregate demographics table.
3. `download_feats.py --encoder uni2h --cohorts lung`: run `hf download` with `--include` patterns, then check the slide counts against the card.
4. `spotcheck.py`: re-extract 5 slides with TRIDENT and report the cosine similarity to the HF features.
5. `splits.py`: 20 Monte Carlo and 10 site-preserving patient-level folds on TCGA. Save them under `data/splits/`.
6. `abmil.py`: train and evaluate with a fixed seed, writing per-fold, per-subgroup metrics to `results/metrics.csv`.
7. `fairness.py`: bootstrap CIs, TPR disparity at fixed thresholds, per-group ECE, a mixed-effects model (`correct ~ race + (1|site)`), and TOST equivalence tests.
8. Repeat steps 3–7 for CONCH v1.5, Virchow2 and GigaPath.
9. Optional: the *IDH1* anchor (Arm A).
10. `report.ipynb`: figures and tables. Commit code, figures and aggregate CSVs only.
