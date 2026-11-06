---
enriched: true
---
## What the original study did

Shah et al. (VIT Vellore; IEEE IC-SIT 2026, paywalled) trained five YOLO versions (v3, v4, v5, v7, v8) with the same preprocessing and augmentation on TXL-PBC, a public dataset of peripheral blood smear fields with boxes for red cells, white cells and platelets. They compared precision, recall, F1, mAP and inference speed.

According to the abstract, YOLOv8 was the most accurate (mAP@0.5 = 96.11%) and YOLOv5 the best trade-off between speed and accuracy. The authors recommend YOLOv5 for low-resource real-time use and YOLOv8 for precision-critical diagnosis.

**Only the abstract and IEEE metadata could be read;** the full text is paywalled. Details below that are not in the abstract come from the dataset paper (Gan et al., Sci Data 2025) or are marked `verify`. No code was released.

**Replicable.** TXL-PBC is open, and every model is a public YOLO release.

## Data

| Dataset | What | Access |
| --- | --- | --- |
| TXL-PBC | 1,260 field images (882 train / 252 val / 126 test), 18,143 boxes; 160 BCCD + 100 BCDD + 500 PBC + 500 Raabin-WBC images | Open: [GitHub](https://github.com/lugan113/TXL-PBC_Dataset) (MIT) and Figshare (doi:10.6084/m9.figshare.27073186.v8); `datasets/txl-pbc` |

TXL-PBC was built by hand-labelling 250 images, training YOLOv8n on them, using that model to pre-label the remaining images, and then reviewing everything by hand. Images from the four sources were shuffled and split at random. `metadata_file.xlsx` maps each image to its source. The whole dataset is about 100 MB.

**Licence caution:** the repo says MIT, but it includes PBC images (CC BY 4.0) and Raabin-WBC images (no licence stated). Use it for research, and cite all four sources plus Gan et al.

## Environment

Ultralytics for YOLOv5 and v8 (and newer versions: YOLO11, YOLO26), the official YOLOv7 repo, and Darknet or ports for v3 and v4. Python 3.10+, PyTorch 2.x. The dataset paper trained at 320 × 320, batch 16, AdamW, learning rate 0.001. The source's input size and epochs are not stated in its abstract (verify).

## Step-by-step replication

1. Download TXL-PBC and check the split counts (882/252/126) and class totals.
2. Train YOLOv3, v4, v5 (s), v7 and v8 (s) with one shared recipe: same image size, augmentation, epochs and early stopping, with 3–5 seeds each.
3. Evaluate on the test split: precision, recall, F1, mAP@0.5 and mAP@0.5:0.95, per class and overall; inference time on GPU and CPU.
4. Compare with the source abstract (YOLOv8 mAP@0.5 0.961) and with Gan et al. Table 3, where YOLOv5s already reaches mAP@0.5 0.980 on the same split.

## Compute and cost

Small: each model trains in well under 1 GPU-hour on a Colab T4. A full seed sweep is about 5–10 GPU-hours.

## Target numbers

- **Source abstract:** YOLOv8 mAP@0.5 = 0.9611 (best); YOLOv5 the fastest high-accuracy option. Per-class values are not available.
- **Dataset paper, Gan et al. Table 3 (TXL-PBC test):** YOLOv5s overall mAP@0.5 0.980, mAP@0.5:0.95 0.857; WBC 0.994; RBC 0.989; platelets 0.956. YOLOv8s and YOLO11s are also reported there.

## Known pitfalls

- **Labels drawn by a YOLOv8n model.** Even after review, boxes follow YOLOv8's habits: box tightness, which overlapping cells get split, which faint platelets get kept. That can favour YOLOv8-family detectors when they are scored against these labels.
- **Random split across mixed sources.** Each source has its own magnification, stain and camera. Test images come from the same four sources as training, so this tests in-distribution performance only.
- **PBC and Raabin images are single-cell crops** centred on one WBC, unlike whole fields. Mixing them inflates WBC scores.
- **mAP@0.5 hides counting errors** in crowded RBC fields and platelet clumps.

## Claude Code task list

1. Download TXL-PBC and source metadata to `data/`; verify counts.
2. Set up Ultralytics (v5, v8, 11) plus YOLOv7, YOLOv3 and YOLOv4 ports; one config per model with the shared recipe.
3. Train 5 seeds each; evaluate on test; record per-class metrics and timing.
4. Tabulate against the source abstract and Gan et al. Table 3.
5. Commit configs, scripts and aggregate tables only.
