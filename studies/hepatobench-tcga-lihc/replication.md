---
enriched: true
---
## What the original study did

Pathologists at Beijing Tsinghua Changgung Hospital cut small (150 × 150 px, 20×) patches from liver cancer resection slides and labelled each as one of seven tissue types: tumour, fibrosis, inflammation, necrosis, normal liver, bile duct (ductular) reaction and steatosis. After removing blurred, badly stained and duplicate patches, they released 87,301 patches as **HepatoBench**. They compared three pathology foundation models (UNI, Virchow2 and Prov-GigaPath) using a frozen encoder with a single linear layer on top. Separately, they trained a LoRA-adapted tumour/non-tumour segmentation model on 111 annotated slides, and combined the two into **HepatoQuant**, which reports the tissue composition inside and outside the tumour on a whole slide. The peer-reviewed version is in *Scientific Data* (2026); the preprint is arXiv:2604.22858.

**Replicability verdict: partly replicable.**
- **Can be replicated:** the patch-level benchmark. The patches are public.
- **Cannot be replicated as published:**
  - the claimed slide-level 7:2:1 split, because the release contains no slide IDs and no split files;
  - the segmentation model and HepatoQuant, because the 111 annotated slides are private and no classifier weights or code link was found. The GitHub repository covers segmentation code only, and has no licence.

## Data

| Dataset | Access | How to get it | Size |
| --- | --- | --- | --- |
| [HepatoBench](https://huggingface.co/datasets/xtxx/HepatoBench) (DOI 10.57967/hf/8231) | Open, not gated | `huggingface-cli download xtxx/HepatoBench --repo-type dataset --local-dir data/hepatobench` | 7 zips, ~3.6 GB; 87,301 PNGs |
| [PAIP 2019](https://paip2019.grand-challenge.org/) (optional external arm) | Free registration + data use agreement | Grand Challenge account, then accept the PAIP agreement and download the 50 training WSIs with masks | WSIs: verify size |
| [TCGA-LIHC](https://portal.gdc.cancer.gov/) (optional) | Open | GDC Data Transfer Tool with a manifest of diagnostic slides | 379 slides, 365 cases, 503.5 GB (GDC API, 2026-11-06) |

Storage tips:
- Keep everything under `data/` (gitignored). Never commit patches or embeddings, because of the licence terms below.
- HepatoBench fits on a laptop or in Colab.
- For TCGA-LIHC, download only the subset you need, onto a RunPod volume.

**Licence: read before use.**
- The dataset card says CC BY 4.0, but the paper's Usage Notes say CC BY-NC 4.0, and the article itself is CC BY-NC-ND 4.0. Treat the data as **non-commercial**.
- The authors ask that it is not used to build diagnosis-focused algorithms. Frame the work as benchmark quality and tissue quantification, not diagnosis.

## Environment

The patch benchmark has no released code, so reimplement it. Suggested stack:
- Python 3.10+;
- `torch` and `timm`, plus `huggingface_hub` for the encoders;
- `scikit-learn` for the linear and logistic probes;
- `imagehash` and `Pillow` for duplicate detection;
- `numpy`, `pandas` and `scipy` for analysis.

For the optional WSI arm, add `openslide-python` and a tiler such as TRIDENT or CLAM.

Encoders checked on Hugging Face (2026-11-06):

| Encoder | Licence | Gated |
| --- | --- | --- |
| [UNI](https://huggingface.co/MahmoodLab/UNI) | CC-BY-NC-ND-4.0 | auto |
| [UNI2-h](https://huggingface.co/MahmoodLab/UNI2-h) | CC-BY-NC-ND-4.0 | auto |
| [Virchow2](https://huggingface.co/paige-ai/Virchow2) | CC-BY-NC-ND-4.0 | auto |
| [Prov-GigaPath](https://huggingface.co/prov-gigapath/prov-gigapath) | Apache-2.0 | auto |
| [H-optimus-0](https://huggingface.co/bioptimus/H-optimus-0) | Apache-2.0 | auto |
| [H-optimus-1](https://huggingface.co/bioptimus/H-optimus-1) | CC-BY-NC-ND-4.0 | manual |
| [H0-mini](https://huggingface.co/bioptimus/H0-mini) | CC-BY-NC-ND-4.0 | manual |
| [Phikon-v2](https://huggingface.co/owkin/phikon-v2) | other | no |
| [CONCH v1.5](https://huggingface.co/MahmoodLab/conchv1_5) | CC-BY-NC-ND-4.0 | auto |
| [DINOv2-L](https://huggingface.co/facebook/dinov2-large) (general-domain baseline) | Apache-2.0 | no |

## Step-by-step replication

1. Download HepatoBench and unzip each class zip into `data/hepatobench/<class>/`. Check the counts against `dataset_meta.json`: 13,200 / 26,364 / 4,776 / 22,023 / 13,200 / 1,540 / 6,198.
2. **Duplicate audit.** Compute MD5 hashes (exact duplicates) and perceptual hashes (pHash, Hamming distance ≤ 4) for every patch. Record the duplicate clusters within each class and across classes. Cross-class duplicates are label conflicts.
3. **Pseudo-groups.** File names are `<class>_<index>.png`. Test whether consecutive indices come from the same tissue: compare the embedding similarity of neighbouring indices with random pairs. Build groups from runs of consecutive indices, then build a second set from embedding clusters (e.g. agglomerative clustering at a cosine threshold). Keep both definitions, for a sensitivity analysis.
4. **Splits.**
   - (a) A random stratified 7:2:1 patch split, like the paper's stated ratio.
   - (b) A grouped 7:2:1 split on the pseudo-groups, with duplicate clusters kept in one partition.
   - Use five seeds for each.
5. **Embeddings.** Resize patches from 150 to 224 px with bicubic interpolation (note this as a deviation, since the paper does not say how it resized). Extract frozen CLS embeddings with each encoder's own preprocessing. Cache them as `.npy` under `data/`.
6. **Probes.** Train a linear probe (logistic regression, L2, C tuned on validation) for each encoder. Report accuracy, macro precision, recall and F1, and balanced accuracy.
7. **Reproduce.** Compare the UNI, Virchow2 and GigaPath results on split (a) with the paper's Figure 2.
8. Optional: tile the PAIP 2019 slides at 20×, classify the tiles, and compare tumour versus non-tumour against the whole-tumour masks.

## Compute and cost

| Task | Where | Time | Cost |
| --- | --- | --- | --- |
| Embeddings: 87,301 patches × one ViT-L/H encoder | Colab T4/L4 or RunPod | ~0.5–1.5 GPU-h each; 6–12 GPU-h for 6–8 encoders | |
| Probes and statistics | Laptop CPU | | |
| PAIP arm (50 WSIs) | RunPod | ~5 GPU-h | |
| Whole project | | | Under US$20 on RunPod |

## Target numbers

- **From the paper:** the paper gives patch-level results for UNI, Virchow2 and GigaPath only in **Figure 2** (accuracy, precision, recall and F1). No numbers are given in the text, so read the bar values from the figure (verify) and treat them as approximate.
- **Class counts to reproduce exactly:** as in step 1 (sum 87,301).

## Known pitfalls

- **Inconsistent counts in the paper.** The text says "140,000 annotated patches in total (example numbers)", but the class counts sum to 87,301, which matches the released metadata. It also mentions "four encoders" but lists three. Use the released counts.
- **No slide IDs or split files.** The paper says the data were split at slide level and that the official partition is released, but the Hugging Face release (checked 2026-11-06) contains only class zips and a metadata file. Random patch splits will very likely leak tissue between train and test. PathJev (arXiv:2610.32478) independently reports exact duplicates in the release and that neighbouring indices seem to come from the same tissue.
- **Class names.** "Steroidal Degeneration" on the card means steatosis. "Biliary Reaction" means bile duct (ductular) reaction. REA has only 1,540 patches, so report per-class results and balanced accuracy.
- **Patch size.** 150 px at 20× is smaller than most encoders' 224 px input. Resizing changes the apparent magnification. Report results at both 224 px resized and 150 px padded.
- **Pretraining overlap.** None of these encoders is known to include HepatoBench, but check each model card.
- **Licences.** The data are non-commercial and most encoders are CC-BY-NC-ND. Do not publish fine-tuned weights of ND models, and do not redistribute patches.
- **Segmentation code.** It has no licence, so reimplement rather than copy it.

## Claude Code task list

1. Create `analysis/hepatobench/` with `pyproject.toml` (torch, timm, huggingface_hub, scikit-learn, imagehash, pandas). Add `data/` to `.gitignore` if it is not already there.
2. `download.py`: fetch and unzip HepatoBench into `data/hepatobench/`, then assert the class counts.
3. `dedup.py`: MD5 and pHash audit, writing `results/duplicates_summary.csv` (counts only, no images).
4. `groups.py`: build the index-run and embedding-cluster pseudo-groups, and plot neighbour similarity against random pairs.
5. `splits.py`: random and grouped 7:2:1 splits, five seeds each. Save the split index files under `data/`.
6. `embed.py --model <hf_id>`: cache embeddings for each encoder in the table above.
7. `probe.py`: train the logistic probes and write the metrics with 95% bootstrap CIs to `results/metrics.csv`.
8. `report.ipynb`: compare with Figure 2, show the inflation (random minus grouped), and draw confusion matrices.
9. Commit only code, figures and aggregate CSVs.
