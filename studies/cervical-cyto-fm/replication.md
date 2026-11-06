---
enriched: true
---
## What the original study did

Dausort, Godelaine, Zanella, El Khoury, Salmon and Macq (UCLouvain, UMons and ULB, Belgium; ISBI 2025, [doi:10.1109/ISBI60581.2025.10981249](https://doi.org/10.1109/ISBI60581.2025.10981249); preprint [arXiv 2411.14975](https://arxiv.org/abs/2411.14975)) asked whether foundation models built for natural images, biomedical figures or histology can classify cytology images. They ran three experiments on four public datasets:

1. **Frozen encoder plus a linear head** for five models (CLIP ViT-B/16, Google ViT-B/16, BiomedCLIP, QuiltNet and UNI ViT-L/16).
2. **Few-shot LoRA** (rank 2 on the query and value matrices) with 1–50 labelled images per class.
3. **LoRA on CLIP ViT-L/14** (rank 16 on all attention matrices) trained on 5–100% of HiCervix, compared with the HierSwin benchmark.

UNI was the best frozen feature extractor on three of four datasets (Table 1). With LoRA, CLIP needed only one or two images per class to beat the frozen linear probe on the three small datasets (Figure 1). LoRA-CLIP passed HierSwin's HiCervix accuracy with 70% of the training data and reached 80.23% with all of it, training 3.1 million parameters (Figure 2).

**Every result is within one dataset.** There was no external or cross-dataset test, no slide-grouped split, and no calibration. Results are top-1 accuracy averaged over three seeds. The three small datasets reach 92–100% accuracy, which is near the ceiling. The two cervical datasets use different label systems (SIPaKMeD: morphological cell types; MLCC: Bethesda field labels), and the paper never mapped them to each other.

The study is **mostly replicable on open data**. The body-cavity-fluid arm is no longer replicable: its Kaggle page returned HTTP 404 on 2026-11-06, and no original record was found.

## Data

| Dataset | What | Access | How to get it |
| --- | --- | --- | --- |
| `sipakmed` | 4,049 isolated cells cropped from 966 conventional Pap field images, 5 morphological classes, Greece | Open; no licence stated (page asks for citation) | Five 7z archives from the [University of Ioannina page](https://www.cs.uoi.gr/~marina/sipakmed.html), about 5.2 GB in total |
| `mendeley-lbc-cervical` (MLCC) | 972 liquid-based Pap field images (NL 612, HSIL 173, LSIL 113, SCC 74), India | Open, CC BY 4.0 | [Mendeley Data v4](https://data.mendeley.com/datasets/zddtpgzv63/4), 2.25 GB, no account |
| `hicervix` | 40,229 cells from 4,496 whole-slide images, 29 classes in 3 levels, China | Free registration (manual approval), CC BY 4.0 | [Zenodo access request](https://zenodo.org/records/11087263). The primary email on your Zenodo account must be institutional; give your full name, affiliation and official email in the request message |
| Body Cavity Fluid Cytology (BCFC) | Benign vs malignant effusion cells (Sanyal, Kaggle) | **Unavailable** | The Kaggle URL in the paper and repository returns 404 (2026-11-06). Drop this arm. |

**Storage tips:**
- Keep everything under `data/` (gitignored) or on a Colab/RunPod volume. Never commit images, features or per-image predictions.
- Use the original records. The source repository points to Kaggle mirrors for SIPaKMeD and MLCC, which were not checked against the originals.
- Ask for HiCervix access on day 1, because approval is manual and can take time.

## Environment

From the [repository](https://github.com/mdausort/Cytology-fine-tuning) (MIT; built on CLIP-LoRA):
- Python 3.9.13, `torch==2.2.2`, `torchvision==0.17.2`, then `pip install -r requirements.txt`. The requirements file is a frozen dump of a cluster environment (it pins jupyter and easybuild packages). Expect to prune it, and record what you changed.
- `open_clip` / OpenAI CLIP, `timm` (for UNI), and Weights & Biases logging (optional; results are also written to JSON).
- Encoders used by the source (Hugging Face API, 2026-11-06):

| Encoder | Licence | Gating |
| --- | --- | --- |
| CLIP ViT-B/16 and ViT-L/14 (`openai/...`) | no licence field on the card (OpenAI's MIT code licence) | none |
| BiomedCLIP | MIT | none |
| QuiltNet-B-16 | MIT | none |
| UNI (`MahmoodLab/UNI`) | CC-BY-NC-ND-4.0 | auto |
| Google ViT-B/16 (ImageNet-21k) | not checked | none |

## Step-by-step replication

1. **Get the data.** Download SIPaKMeD and MLCC from the original records. Request HiCervix access.
2. **Make the splits.** The repository expects `train/`, `val/` and `test/` folders with files named `classname_number`, but the paper does not give split ratios for SIPaKMeD or MLCC, and the repository ships no split files. Use 70/15/15, stratified by class, with seed 0, and log the split as an assumption. Also build a **grouped** split as a sensitivity check:
   - SIPaKMeD: group by source cluster image;
   - MLCC: no patient key exists, so state the leakage risk.

   HiCervix comes with official splits; use them.
3. **Fill in the paths.** Search the repository for the placeholder `TO CHANGE` and replace it with your data root.
4. **Experiment 1 (linear probe).** Run `main.py --task classifier --shots -1` for each of the 5 models × 3 datasets × 3 seeds. Select the learning rate on validation accuracy, as the paper did.
5. **Experiment 2 (few-shot LoRA).** Run `--task lora --r 2 --params "q v"` with shots 1, 2, 4, 8, 16 and 50, using CLIP first (the paper's main finding), then the others.
   - The README shows 50 iterations, but `launch_run.sh` uses 100. Run 100 and note the discrepancy.
6. **Experiment 3 (HiCervix).** Run `run.py --task percentage_lora` with CLIP ViT-L/14, `--r 16 --params "q k v o"`, at 10%, 30%, 50%, 70% and 100% of the data, level 3.
7. **Report** top-1 accuracy (mean ± SD over 3 seeds) as in Table 1 and Figures 1–2. Add balanced accuracy and macro-F1, which the paper omits and which matter for the imbalanced sets (MLCC is 63% negative).

## Compute and cost

- Experiment 1: frozen features for about 45k images × 5 encoders, under 1 GPU-h on a Colab T4.
- Experiment 2: 6 shot levels × 5 models × 3 datasets × 3 seeds, each run minutes long on tiny training sets. About 3–5 GPU-h.
- Experiment 3: LoRA on CLIP ViT-L/14 over the HiCervix training split (most of its 40,229 cells; exact split size verify on download), 5 fractions × 3 seeds. About 6–10 GPU-h on an A40 (RunPod, about US$3–5).
- Total: about 10–15 GPU-h (Colab Pro or RunPod, under US$10).

## Target numbers

Table 1 (mean accuracy, frozen encoder plus linear head):

| Dataset | CLIP | QuiltNet | BiomedCLIP | UNI | ViT |
| --- | --- | --- | --- | --- | --- |
| MLCC | 93.95 | 97.95 | 95.10 | 99.20 | 96.80 |
| SIPaKMeD | 90.50 | 92.00 | 87.62 | 93.33 | 89.71 |
| HiCervix (level 3) | 55.20 | 54.64 | 46.39 | 64.07 | 57.64 |

- BCFC values (94.7–100) cannot be checked, because the data are gone.
- Figure 2: LoRA-CLIP ViT-L/14 on 100% of HiCervix reached **80.23%**. With 70% of the data it already passed HierSwin's accuracy (the HierSwin value is read off the figure; take it from the HiCervix paper).
- Figure 1 values are plotted only. Read them off the figure, and expect to match within about ±2 points.

Your MLCC and SIPaKMeD numbers will depend on your split. If grouped splits give much lower accuracy than random splits, that is a finding in itself.

## Known pitfalls

- **Split leakage.** SIPaKMeD cells from one cluster image share stain and focus. MLCC has 963 images from 460 patients with no patient key. Random splits on either set overstate accuracy. The source paper's 99% MLCC accuracy is very likely inflated by this.
- **Label systems differ.** SIPaKMeD's five classes are cell types, not Bethesda categories. Koilocytes approximate LSIL. Dyskeratotic cells span LSIL to HSIL/SCC. Metaplastic and parabasal cells are normal but can mimic HSIL. MLCC labels whole fields. Never pool them without a documented mapping.
- **Disputed MLCC labels.** An independent reclassification (Zenodo, [doi:10.5281/zenodo.17259913](https://doi.org/10.5281/zenodo.17259913), CC BY-NC-ND 4.0) excludes or relabels some images. Report results on both label sets if you use it.
- **MLCC image count.** Version 4 holds 972 images, but its description says 963.
- **Ceiling effects.** At 97–100% accuracy, differences between encoders are within noise. Give confidence intervals.
- **Licences.** UNI is CC-BY-NC-ND (non-commercial; do not redistribute the weights). The HiCervix code has no licence (reimplement it). SIPaKMeD has no stated licence (do not redistribute the images).
- **Iteration count** differs between the README (50) and `launch_run.sh` (100).

## Claude Code task list

1. Create a separate analysis repo `cervical-cyto-fm-analysis/` with `data/`, `features/` and `preds/` gitignored, and a README saying that no images, features or per-image predictions are committed.
2. Write `download.py`: fetch SIPaKMeD (5 archives) and MLCC v4 (Mendeley public API file list). Verify file counts (4,049 cells; 972 images) and log SHA-256 sums.
3. Write `make_splits.py`: random 70/15/15 stratified splits (seed 0) and grouped splits (SIPaKMeD by cluster image), saved as CSV manifests. Add a unit test that no cluster crosses splits in the grouped manifest.
4. Clone the source repository outside the analysis repo, replace `TO CHANGE`, and write a thin wrapper `run_source.sh` that reads the manifests.
5. Run Experiments 1–2 on SIPaKMeD and MLCC, then Experiment 3 on HiCervix once access is granted.
6. Write `evaluate.py`: accuracy, balanced accuracy and macro-F1 with bootstrap 95% CIs (resampled by group where possible).
7. Write `results/replication.md`: aggregate tables only, compared with Table 1 and Figures 1–2, with every assumption (split ratio, iteration count, pruned requirements) listed.
