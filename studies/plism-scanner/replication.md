---
enriched: true
---
## What the original study did

Thiringer et al. (Karolinska Institutet, arXiv 2601.04163, January 2026) tested whether 13 pathology foundation models, plus an ImageNet ResNet-50 baseline, give the same embedding for the same breast tumour slide scanned on five different scanners. They used unsupervised embedding metrics (cosine distance, 1-nearest-neighbour match, Mantel correlation, neighbourhood consistency) and attention-MIL models for ER, PR, HER2 and grade, trained on TCGA-BRCA. Most models carried strong scanner signals. AUC often stayed stable while the predicted probabilities shifted between scanners, so calibration, not accuracy, was the hidden failure. CONCH and CONCHv1.5 were the most stable; UNI and UNI2-h ranked lowest on the embedding metrics.

**Not directly replicable.** The multiscanner cohort (CHIME Multiscanner: 384 slides × 5 scanners, Södersjukhuset, Stockholm) cannot be shared, as the paper's data availability statement says. The authors' code is "based on CLAM", with details on request. This study therefore uses the closest open surrogate: **PLISM** (`datasets/plism`), a public, registered multi-device dataset with the same design idea (the same tissue imaged on many devices), plus smartphones.

## Data

| Dataset | What | Access | How to get it |
| --- | --- | --- | --- |
| PLISM-wsi | 46 tissue types (TMA, University of Tokyo), 13 H&E stain conditions × 7 slide scanners = 91 WSIs; 310,947 registered 512 × 512 patches | Open, CC BY 4.0 | figshare+ collection, DOI [10.25452/figshare.plus.c.6773925](https://doi.org/10.25452/figshare.plus.c.6773925). Preprocessed copy (WSI subset only) on Hugging Face: [owkin/plism-dataset](https://huggingface.co/datasets/owkin/plism-dataset) (225 GB as `.h5`) or [owkin/plism-dataset-tiles](https://huggingface.co/datasets/owkin/plism-dataset-tiles) |
| PLISM-sm | The same TMAs photographed through a microscope eyepiece on 6 smartphones (Galaxy S20 5G, moto g8, Redmi Note9 Pro, iPhone 6, iPhone 13 mini, iTel P33); 57,902 images registered to the WSI patches | Open, CC BY 4.0 | figshare+ collection only. **The Owkin Hugging Face copies do not include smartphones.** |
| TCGA-BRCA (optional) | Only if you also reproduce the MIL arm | Open (GDC) | `datasets/tcga` |

Each PLISM subset ships a CSV listing tissue type, stain, device, coordinates and file path (Ochi et al., Sci Data 2024, [PMC10991301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10991301/)).

**Storage tips:**
- Start with PLISM-sm plus the matching PLISM-wsi patches for one or two stains. That is enough for every analysis below and avoids the full 225 GB download.
- Keep the data on a RunPod network volume or an external disk under `data/` (gitignored).

**Model access:** most strong encoders are gated on Hugging Face, and several are CC-BY-NC-ND. As of 2026-11-06 (HF API):

| Model | Licence | Gating |
| --- | --- | --- |
| UNI2-h | CC-BY-NC-ND-4.0 | auto |
| Virchow2 | CC-BY-NC-ND-4.0 | auto |
| CONCHv1.5 | CC-BY-NC-ND-4.0 | auto |
| H-optimus-0 | Apache-2.0 | auto |
| H-optimus-1 | CC-BY-NC-ND-4.0 | manual |
| H0-mini | CC-BY-NC-ND-4.0 | manual |
| Phikon-v2 | "other" | not gated |

Request access early, with an institutional email. Academic, non-commercial use only.

## Environment

- Python 3.10+, PyTorch 2.x, `timm`, `huggingface_hub`, `h5py`, `numpy`, `pandas`, `scikit-learn`, `scipy`, `matplotlib`.
- Reference implementation of the PLISM metrics: [owkin/plism-benchmark](https://github.com/owkin/plism-benchmark) (`plismbench`, MICCAI 2025). GitHub reports **no licence file**: use it to check the numbers, and reimplement the metrics rather than copying code.
- MIL arm (optional): [mahmoodlab/CLAM](https://github.com/mahmoodlab/CLAM).

## Step-by-step replication

1. Download the PLISM-sm and PLISM-wsi CSVs, then the image folders for the stains you need.
2. Build aligned groups: one row per tissue location, with the image path for each device and stain (from the CSV coordinates).
3. Extract tile embeddings for each encoder (ImageNet ResNet-50 baseline, H-optimus-0, UNI2-h, Virchow2, CONCHv1.5, Phikon-v2, H0-mini, and H-optimus-1 if access is granted). Use each model's own preprocessing; resize the 512-pixel tiles to 224.
4. Reproduce the original paper's unsupervised metrics *across devices for the same location*:
   - mean pairwise cosine distance;
   - 1-NN match rate (is the nearest neighbour of a tile on device A the same location on device B?);
   - Mantel correlation of the distance matrices;
   - intersection-over-K neighbourhood consistency.
5. Cross-check against the plismbench leaderboard for the WSI subset (cosine similarity and top-10 cross-scanner accuracy, dated 2025-03-03). Your WSI-only numbers should land close to theirs; differences point to preprocessing bugs.
6. Optional: train CLAM-SB on TCGA-BRCA for ER status. This reproduces the original supervised arm on TCGA only, since no public multiscanner slide-level cohort with receptor labels exists.

## Compute and cost

- Embeddings: about 1.5 h per ViT-B model for the whole PLISM-wsi set on one T4 (plismbench README). ViT-H/G models take 3–5× longer.
- Total: about 10–20 GPU-h on a RunPod A40/L4 (~US$5–15). Smartphone-only runs fit on Colab. Analysis runs on a laptop.

## Target numbers

There are no public target numbers from the source paper, because its cohort is private. Reproduce *qualitative* findings instead:
1. Scanner identity is recoverable from embeddings.
2. CONCH-family models are among the most stable.
3. UNI/UNI2-h are among the least stable (Thiringer et al., Fig. 6).

For quantitative checks, use the plismbench WSI leaderboard: for example, H0-mini cosine similarity 0.800, UNI2-h 0.591.

## Known pitfalls

- **Licences:** model weights are mostly NC-ND. You may publish metrics, not redistributed weights or features.
- **Owkin's Hugging Face copies omit smartphones.** Download PLISM-sm from figshare+.
- **Registration quality:** median error is 43 µm between serial WSI sections and about 1 µm for WSI–smartphone landmarks. Exclude locations with focus or crop problems (the CSV is already quality-controlled), and report how many tiles remain.
- **Magnification mismatch:** smartphones were shot at 400× through an eyepiece, while scanners work at about 0.25 µm/px. Document the resizing.
- **Stain and device confounding:** always hold the stain fixed when measuring device effects, and vice versa.
- **Pretraining overlap:** H0-mini's authors also built plismbench; declare this when ranking models.

## Claude Code task list

1. Create `analysis/plism-scanner/` in a separate analysis repo (never commit images or features). Add `data/` and `features/` to `.gitignore`.
2. Write `download.py` to fetch the PLISM-sm CSV and images and the PLISM-wsi CSV, plus the images for stains A and B, from figshare+. Verify the checksums.
3. Write `align.py` to build the location × device × stain index and drop incomplete groups. Report the counts.
4. Write `embed.py --model <name>`: batched extraction to `features/<model>/<device>_<stain>.npy`, with resume support.
5. Write `metrics.py`: cosine, 1-NN, Mantel and IoK across device pairs. Add a bootstrap over locations for 95% CIs.
6. Write `check_plismbench.py`: compare WSI-only results with the plismbench leaderboard, and flag any difference over 0.03.
7. Write `figures.py`: device × device heatmaps per model, and a UMAP coloured by device and by tissue type.
8. Write up the replication results in `results/replication.md` (aggregate numbers only).
