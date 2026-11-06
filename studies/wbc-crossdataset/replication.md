---
enriched: true
---
## What the original study did

Tian et al. (Universities of Oxford, Bristol and UCL with Chulalongkorn University; ISBI 2026, [doi:10.1109/ISBI61048.2026.11515899](https://doi.org/10.1109/ISBI61048.2026.11515899); preprint [arXiv 2604.10797](https://arxiv.org/abs/2604.10797)) describe the WBCBench 2026 challenge. The data are 13-class white-cell crops from one Thai hospital laboratory. The challenge had two phases. Phase 1 released clean training images. Phase 2 released copies degraded with blur, noise, crop, colour and illumination changes at three severities, with different severity mixes in train, validation and test (paper Tables 1–2). Teams were ranked by macro-F1 on the degraded test set. 101 of 241 registered teams submitted. The winner reached macro-F1 0.777 with an ensemble built on DinoBloom-B and DINOv3, against 0.635 for the organisers' ResNet-50 and 0.643 for Swin-Tiny (Table 3). Common classes were easy (mean F1 above 0.92). Band neutrophils, promyelocytes, plasma cells and prolymphocytes stayed hard (Table 4).

All evaluation was **in-distribution**: one site, one staining protocol, one analyser model, and synthetic degradation only. There was no external dataset, no calibration and no case-level (whole-differential) result. That is the gap the extension targets.

The study is replicable on open data. The dataset is gated but approved automatically.

## Data

| Dataset | What | Access | How to get it |
| --- | --- | --- | --- |
| `wbcbench-2026` | 55,002 pristine + 46,714 degraded crops; 493 cases (blood films); 13 classes; CellaVision DI-60, Wright-Giemsa, Thailand | Free registration; WBCBench Data Use Licence v1.0: **non-commercial, no redistribution** | [Hugging Face](https://huggingface.co/datasets/Xin-Tian/wbcbench2026): click "Request access", fill in the form, approval is automatic. Then run `hf auth login`. About 3.9 GB of parquet: pristine config 1.1 GB, degraded 2.8 GB. Allow twice that on disk, because `datasets` keeps a converted copy. |
| `pbc-barcelona` (extension) | 17,092 normal cells, 8 groups, CellaVision DM96, Spain | Open, CC BY 4.0 | [Mendeley Data](https://data.mendeley.com/datasets/snkd93bnjr/1) zip, no account |
| `raabin-wbc` (extension) | Double-labelled 5-class crops: Train 10,175, Test-A 4,339, Test-B 2,119; smartphone on microscope, Iran | Open download; **licence not stated** | "Free Data" on [raabindata.com](https://raabindata.com/), files on the [download server](https://dl.raabindata.com/Index%20of%20WBC%20Data/) (`Index of WBC Cropped_double_labeled/`: Train.rar 279 MB, TestA.rar 115 MB, TestB.zip 104 MB) |
| `cytologia` (extension) | 69,168 images, 75,437 labelled cell boxes, 23 normal and pathological classes, 19–20 European laboratories | Open, Etalab Open Licence 2.0 | [data.gouv.fr](https://www.data.gouv.fr/datasets/cytologia): labels CSV (2.6 MB) and images zip (1.4 GB), no account |

What the WBCBench card adds to the paper (checked 2026-11-06):
- **Pristine copies of every Phase 2 split** are included, linked to the degraded copies by `original_image_id`. Labels are released for all splits, including `phase2_test`.
- **Per-image degradation settings** are in `metadata/degradation_params.csv`, and the degradation code is in `scripts/` (MIT).
- `patient_hash` is a **case** (one film), not a person.
- **267 test images changed** after the challenge: 257 relabelled and 10 removed (`metadata/label_changes.csv`).

**Storage tips:**
- Keep everything under `data/` (gitignored), or on a Colab/RunPod volume.
- Write the WBCBench JPEG bytes to disk as published (the card shows how). Do not re-save them with `image.save()`, which re-encodes the JPEG.
- The WBCBench licence requires secure storage and deletion when access ends. Never put images, features or per-image predictions in a public repo.

## Environment

- The source paper has no code repository. The card lists participants' repositories (Nguyen et al., Le et al., Gitau et al., Srivastava et al.). The first checked, `trongduc-nguyen/WBCBench2026`, has **no licence file** on GitHub: read it, don't copy it.
- Python 3.10+, PyTorch 2.x, `timm` ≥ 1.0, `torchvision`, `datasets`, `huggingface_hub`, `pillow`, `pandas`, `numpy`, `scikit-learn`, `scipy`, `matplotlib`.
- **DinoBloom** ([marrlab/DinoBloom](https://github.com/marrlab/DinoBloom), Apache-2.0; weights on [Zenodo](https://zenodo.org/records/10908163), CC BY 4.0, 7 GB for all four sizes). The `timm` ports on Hugging Face (`1aurent/vit_base_patch14_224.dinobloom`, Apache-2.0, not gated) are the easiest way in.
- Encoders for the extension (Hugging Face API, 2026-11-06):

| Encoder | Family | Licence | Gating |
| --- | --- | --- | --- |
| DinoBloom-S/B/L | haematology | Apache-2.0 code, CC BY 4.0 weights | none |
| RedDino-base (`Snarcy/RedDino-base`) | haematology (red cells) | CC BY 4.0 | none |
| UNI2-h | histopathology | CC-BY-NC-ND-4.0 | auto |
| Virchow2 | histopathology | CC-BY-NC-ND-4.0 | auto |
| H-optimus-0 | histopathology | Apache-2.0 | auto |
| H0-mini | histopathology | CC-BY-NC-ND-4.0 | manual |
| Phikon-v2 | histopathology | "other" | none |
| DINOv2-B | general | Apache-2.0 | none |
| DINOv3 ViT-B/16 | general | "other" | manual |

## Step-by-step replication

The core replication reproduces the organisers' two baselines, then adds a frozen-encoder reference point.

1. **Load and audit.** Load both configs. Check the split sizes against the card (8,288 / 24,897 / 5,350 / 16,467 pristine) and check the class counts. Confirm that no `patient_hash` crosses splits.
2. **Rebuild the challenge-era test labels.** Take the challenge-era label from `label_changes.csv` for the 257 relabelled images. The 10 removed images are gone, so an exact match to the leaderboard is impossible. Report both label sets.
3. **Baseline A: ResNet-50.**
   - ImageNet weights, fine-tuned end to end with a 13-way head.
   - Cross-entropy weighted by inverse class frequency, AdamW, cosine schedule, label smoothing (paper Section 4A).
   - Train on `phase1_train` plus degraded `phase2_train`, and select on degraded `phase2_eval`.
   - The paper does not give input size, epochs, batch size or the smoothing value. Use 224 px, 30 epochs and smoothing 0.1, and record them as assumptions.
4. **Baseline B: Swin-Tiny.** The same recipe with `swin_tiny_patch4_window7_224`.
5. **Frozen reference: DinoBloom-B.** Train a logistic-regression probe on frozen features from the same training data. This anchors the extension and is close to what the top teams built on.
6. **Evaluate** on degraded `phase2_test`:
   - macro-F1 (primary), balanced accuracy, macro precision and macro specificity (the tie-breakers);
   - per-class F1 with the support counts (compare with Table 4);
   - results per severity, which the paper does not report.
7. **Sensitivity checks.**
   - Pristine vs degraded copies of the same test cells.
   - Current vs challenge-era labels.
   - With and without the cases from the 24 people who appear in more than one split. The card does not identify these people, so this is only possible if the organisers provide a person key. Otherwise report it as a limitation.

## Compute and cost

- Baselines: about 1–2 GPU-h each on a Colab T4 (about 33k training images at 224 px).
- Frozen DinoBloom-B features for all 101,716 WBCBench images: under 30 min on a T4.
- Extension (all four datasets, about 210k crops, 8–10 encoders): ViT-B encoders take minutes each; ViT-H/g encoders (UNI2-h, Virchow2, H-optimus-0) about 1 h each on an A40. Total about 8–12 GPU-h: Colab Pro, or RunPod A40 at about US$3–6.
- Probes, calibration and statistics run on a laptop.

## Target numbers

From the paper, on degraded `phase2_test` with challenge-era labels:

| Model | Macro-F1 | Balanced accuracy | Source |
| --- | --- | --- | --- |
| ResNet-50 baseline | 0.635 | 0.624 | Table 3 |
| Swin-Tiny baseline | 0.643 | 0.629 | Table 3 |
| Winner (FDVTS_WBC) | 0.777 | 0.753 | Table 3 |
| Median of 101 teams | verify (the value is missing from the arXiv HTML) | verify | Section 5 |

Per-class mean F1 across the top 10: SNE 0.984, LY 0.960, BL 0.871, BNE 0.423, PC 0.150 (Table 4). Expect your baselines within about ±0.02 macro-F1 of Table 3. Larger gaps point to a different recipe or label set. PC (12 test images) and PLY (2) make macro-F1 noisy, so give bootstrap 95% CIs resampled by case.

## Known pitfalls

- **Licence.** WBCBench is non-commercial with no redistribution. You may publish metrics, code, aggregate tables, up to 10 example images with citation, and non-commercial weights. Several encoders are CC-BY-NC-ND (UNI2-h, Virchow2, H0-mini).
- **Paper vs card.** The paper says 55,012 images split by patient with group-stratified sampling. The release has 55,002 images split at random by case, and 24 people span splits (about 14% of test images). Describe `patient_hash` as a case, and cite the card version (v1.0, October 2026).
- **Changed test labels.** Results with current labels are not comparable with the Kaggle leaderboard or the challenge papers. Say which label set you used.
- **Shortcut through image size.** 368 × 370 and 368 × 368 crops come from two different DI-60 analysers, and image size is partly tied to date. Resize or centre-crop to a common size before any model sees the images.
- **Pristine is not byte-identical.** Pristine images were re-saved as JPEG (mean difference about 1 grey level).
- **Rare classes.** `phase2_test` has only 2 PLY and 12 PC cells. Do not over-read their F1.
- **Pretraining exposure.** WBCBench and CytologIA are newer than DinoBloom, and DinoBloom held PBC out. Raabin's 10,175-cell training set was in DinoBloom pretraining.
- **External data used by teams.** Some teams trained on PBC and Raabin (paper Section 5.1). Never compare with their numbers in the cross-dataset arm.

## Claude Code task list

1. Create a separate analysis repo, `wbc-crossdataset-analysis/`, with `data/`, `features/` and `preds/` gitignored. Write a README saying that no images, features or per-image predictions are committed (WBCBench licence).
2. Write `download_wbcbench.py`: authenticate with `huggingface_hub`, download both configs and `metadata/*.csv` (read with `dtype=str`), write the JPEG bytes as published, and print split and class counts against the card.
3. Write `labels.py`: build `current` and `challenge_era` label columns from `label_changes.csv`. Add a unit test that 257 labels differ and 10 IDs are missing.
4. Write `preprocess.py`: a common square crop and resize, so the analyser cannot be read from image size. Add a test that the output sizes are identical across analysers.
5. Write `train_baseline.py --arch resnet50|swin_tiny`: the paper's recipe, with assumptions logged to `config.yaml` and seeds 0–2.
6. Write `embed.py --model dinobloom_b`: batched frozen features to `features/`, with resume support.
7. Write `probe.py`: logistic regression on the features, with class weights.
8. Write `evaluate.py`: macro-F1, balanced accuracy, macro precision and specificity, per-class F1, results per severity, and case-level bootstrap 95% CIs.
9. Write `results/replication.md`: aggregate tables only, compared with paper Tables 3–4, with every assumption listed.
