---
enriched: true
---
## What the original study did

Sáez-Maldonado et al. (Universidad de Granada, CMPB 2027, open access) graded 512 × 512 prostate biopsy patches into four ordered classes (non-cancerous, Gleason 3, 4, 5) from frozen features of seven pathology foundation models. They compared an ordinal Gaussian process (OGP: one latent function plus learned ordered thresholds, sparse variational GP with 500 inducing points) with a multi-class GP and 13 other classifiers, including six recent ordinal-learning methods. They also measured "rankability": the Spearman correlation between test labels and a linear projection of the embeddings fitted on the training set. SICAPv2 (expert-consensus labels) was highly rankable; CrowdGleason (labels from pathologists-in-training) was not. The OGP matched the best methods on SICAPv2 and won on every encoder on CrowdGleason, with the lowest calibration error in most settings.

**Directly replicable.** Both datasets are open (CC BY 4.0) and the code is public.

## Data

| Dataset | What | Access | How to get it |
| --- | --- | --- | --- |
| SICAPv2 | 155 WSIs from Valencia; patch labels from expert-consensus pixel masks. 9,959 patches (2,122 test) in the paper's Table 1 | Open, CC BY 4.0 | [Mendeley Data 9xxm58dvs3](https://data.mendeley.com/datasets/9xxm58dvs3), one zip of ~2.16 GB (`datasets/sicapv2`) |
| CrowdGleason | 19,077 patches from 1,045 WSIs (Granada). Crowd labels for train/val, expert-consensus labels for the 2,926-patch test set | Open, CC BY 4.0 | [Zenodo 14178894](https://zenodo.org/records/14178894): `Patches.zip` ~16.2 GB and `Annotations.zip` (`datasets/crowdgleason`) |

Use the official train/test splits. The paper reports 16,151 CrowdGleason patches in total (Table 1), which equals the 13,824 train plus 2,327 validation patches listed on Zenodo; check how the authors used the validation split before comparing numbers (verify).

**Model access** (Hugging Face API, 2026-11-06):

| Encoder | Licence | Gating |
| --- | --- | --- |
| UNI, UNI2-h, CONCHv1.5 | CC-BY-NC-ND-4.0 | auto |
| Virchow2 | CC-BY-NC-ND-4.0 | auto |
| Virchow | Apache-2.0 | auto |
| Prov-GigaPath | Apache-2.0 | auto |
| Phikon-v2 | "other" (see card) | not gated |

**Storage:** keep raw patches and feature arrays under `data/` (gitignored) or on a RunPod volume. Features are small (a few hundred MB per encoder per dataset).

## Environment

From the repo's `environment.yaml`: Python 3.10, TensorFlow 2.8.0, TensorFlow Probability 0.16.0, GPflow 2.1.3, scikit-learn ≥ 1.0, mord 0.7, netcal 1.3.6, Hydra ≥ 1.3, optional Weights & Biases. Feature extraction uses [TRIDENT](https://github.com/mahmoodlab/TRIDENT) (separate PyTorch environment).

TensorFlow 2.8 needs CUDA 11.2/cuDNN 8.1. On recent GPUs, run the GP stage on CPU or in an old CUDA container; at ~10–16k samples with 500 inducing points it is fast either way.

## Step-by-step replication

1. `conda env create -f environment.yaml && conda activate ordinalgp` in a clone of the repo (MIT text; GitHub shows NOASSERTION because the LICENSE file has unresolved merge-conflict markers, so cite the MIT terms and keep the notice).
2. Download both datasets into `data/`.
3. Extract patch features with TRIDENT for each encoder. Save `X_train.npy`, `y_train.npy`, `X_test.npy`, `y_test.npy`, `train_names.npy`, `test_names.npy` under `features_<ENCODER>/`, as the README describes.
4. Set the dataset roots in `src/data/SICAP_CLAM.py` and `src/data/CROWDGLEASON_CLAM.py`.
5. Sanity check on the toy data: `python src/experiments/main.py dataset=toy_non_rankable model=ordinal_svgp wandb.enabled=false training.epochs=500`.
6. Full run: Hydra multirun over `dataset=sicap,crowdgleason`, seven encoders, `model=ordinal_svgp,svgp_multiclass`, `seed=0..4`. Add baselines from `bash_scripts/`.
7. Compute rankability: fit linear regression of label on features (train), Spearman correlation on test.
8. Compute quadratic weighted kappa and ECE (15 bins) per run; paired t-tests with Holm correction over the 14 comparators.

## Compute and cost

- Feature extraction: ~30k patches × 7 encoders. Roughly 8–15 GPU-h on an L4 or A40 (RunPod ~US$5–10).
- GP and baselines: the authors used 4 × RTX 4090, but each run is small; a single GPU or a laptop CPU finishes the grid in hours.

## Target numbers

- **Rankability (Table 2):** SICAPv2 mean 0.822 (range 0.778 Virchow to 0.864 UNI2); CrowdGleason mean 0.661 (0.623 Virchow to 0.688 CONCHv1.5).
- **Rankability vs mean kappa across the 14 dataset–encoder pairs:** Spearman 0.93 (Section 4.1).
- **OGP, averaged over encoders (Tables 5–6, σ²δ sensitivity):** CrowdGleason kappa 0.771 and ECE 0.028 with σ²δ set to 0 at test (0.698 and 0.201 if retained); SICAPv2 kappa 0.857/0.856 and ECE 0.107/0.036 (zeroed/retained).
- **Per-encoder kappa and ECE:** Tables 3 and 4 are published as images; read them from the PDF and record the OGP and MGP values before starting.

## Known pitfalls

- **Test-time noise variance:** on CrowdGleason the authors set the ordinal likelihood noise σ²δ to 0 at prediction, because test labels are expert consensus. Report both settings; the choice changes ECE by almost an order of magnitude.
- **One split only:** all five seeds share one train/test split (Section 3.6), so the confidence intervals reflect initialisation, not data sampling.
- **Overlapping patches:** patches overlap by 50%. Keep all patches from one WSI in the same split; the official splits do this, so do not re-split at patch level.
- **Pretraining overlap:** some encoders may have seen public prostate slides (e.g. TCGA-PRAD) during pretraining. This matters less for these Spanish cohorts, but note it.
- **Licences:** most encoders are CC-BY-NC-ND; research use only, no redistribution of weights.
- **Old stack:** TF 2.8 + GPflow 2.1.3 pins; do not upgrade one without the others.

## Claude Code task list

1. Clone `fjsaezm/ordinal_gps_prostate` outside this repo; build the conda env; run the toy example.
2. Download SICAPv2 and CrowdGleason to `data/`; record checksums (Mendeley gives SHA-256).
3. Request Hugging Face access for the gated encoders; set up TRIDENT in a separate env.
4. Extract features for all seven encoders; save in the README layout.
5. Reproduce Table 2 rankability; compare within ±0.01.
6. Run OGP and MGP for five seeds on both datasets; then the 13 baselines.
7. Reproduce Tables 3–4 and the σ²δ sensitivity; flag any gap larger than 0.02 kappa.
8. Commit only scripts, configs and aggregate CSVs/plots to the study's results folder; never features, patches or masks.
