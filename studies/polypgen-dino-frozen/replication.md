---
enriched: true
---
## What the original study did

Monteiro, Corbetta, Beets-Tan, Teixeira and Silva (University of Porto, INESC TEC, Netherlands Cancer Institute, Utrecht and Maastricht; arXiv 2512.13376) segmented colon polyps with a small vision transformer (ViT-S) pretrained by DINO. Instead of the usual output tokens, they took the attention **"key"** vectors of the last layer, projected them to 1,024 channels, and decoded them with a plain upsampling CNN with no skip connections. They tested cross-centre generalisation on the 1,537 single frames of PolypGen in two ways: leave-one-centre-out (DG: train on five centres, test on the sixth) and extreme single-domain generalisation (ESDG: train on one centre, test on the other five). They compared DINOv1, DINOv2, DINOv2 with registers and DINOv3 against U-Net, nnU-Net and UM-Net.

**What changed between versions (checked 2026-11-06):**

| Version | Date | Content |
| --- | --- | --- |
| v1 | 2025-12-15 | Full paper (29 pages, under review at MIDL 2026). Claims a *frozen* encoder; DINOv3 best (DG Dice 80.00, ESDG 73.64), beating UM-Net and nnU-Net. |
| v2 | 2026-01-21 | **Withdrawal notice only** (1 KB, no paper). The authors found a bug: the DINO encoder had not been properly frozen, so the results and claims are not fully valid. |
| Code repo, Aug 2026 | 2026-08-10 to 08-20 | Renamed to `RepMatters`, retitled "Representation Matters: Rethinking Domain Generalization in Polyp Segmentation", README says **accepted at MICCAI 2026 MLMI**. Now reports frozen (A) and fine-tuned (B) encoders separately. |

**The bug, located in the code history:** in `keyvitseg/main.py` the freeze line assigned a value to the method name (`requires_grad_ = False`) instead of calling it, so nothing was frozen. Commits on 2025-12-30 switched between the right and wrong forms. The August 2026 commits set `requires_grad = False` on every encoder parameter and pass only trainable parameters to the optimiser.

**What the corrected results show (README results table, August 2026):** the v1 "frozen" numbers match the new *fine-tuned* DINOv3 row almost exactly (DG Dice 79.88, ESDG 73.47), which confirms that v1 really reported fine-tuned models. With a truly frozen encoder, Dice drops by 7–10 points: the best frozen model is DINOv2 (DG 72.71, ESDG 66.00), and frozen DINOv3 (DG 70.42, ESDG 63.53) falls *below* UM-Net with its full loss (DG 73.26, ESDG 63.22). So the headline claim that "frozen DINO keys beat specialised polyp networks" no longer holds. Only fine-tuned DINOv3 beats them.

**Published version:** no MLMI 2026 (LNCS) record was found in Crossref or by web search on 2026-11-06 (OpenAlex was rate-limited). The `source` field points to arXiv v1, because that is the only full text. Re-check for the LNCS chapter before the protocol.

## Data

| Dataset | Role | Access | How to get it |
| --- | --- | --- | --- |
| PolypGen (`datasets/polypgen`) | Development (6 centres) | Free Synapse account | Download `PolypGen2021_MultiCenterData_v3.zip` from [Synapse syn45200214](https://www.synapse.org/#!Synapse:syn45200214). Use the 1,537 single frames with masks (`data_C1` to `data_C6`). The 4,275 negative sequence frames are useful for false-positive tests. |
| Kvasir-SEG (`datasets/kvasir-seg`) | External test (Norway) | Open, research/education only | 1,000 images, about 46 MB. Linked from the author's [GitHub README](https://github.com/DebeshJha/Kvasir-SEG); the Simula download page refused connections on 2026-11-06, so retry later. |
| CVC-ClinicDB (`datasets/cvc-clinicdb`) | External test (Spain) | Open, research/education only | 612 frames at 384 × 288. The [official page](https://polyp.grand-challenge.org/CVCClinicDB/) currently has an empty download link, so record which mirror you use and its checksum. |
| PolypDB (`datasets/polypdb`) | External test (Sweden, **Vietnam**; 5 modalities) | Open, no formal licence | One 1.39 GB zip on [OSF](https://osf.io/pr7ms/). Use the Sweden and Vietnam folders. The Norway folder overlaps HyperKvasir. |
| FAR-POLYP-SEG (`datasets/far-polyp-seg`) | External test (**Iran**, 2025, polyp-free frames) | Open, CC BY 4.0 | 344 MB zip on [Zenodo](https://doi.org/10.5281/zenodo.20284781): 432 masked polyp frames and 7,749 normal-mucosa frames from 455 patients. |

The original paper used **only PolypGen**. The last four rows are for the extension. All five downloads together are under 5 GB and fit on a laptop disk or a small RunPod volume. Keep them under `data/` (gitignored), outside this repo.

**Licence summary:** PolypGen's paper says CC BY 4.0, but its Synapse page forbids redistribution and new derived datasets. Kvasir-SEG and CVC-ClinicDB are research and education only (non-commercial). PolypDB has no stated licence. FAR-POLYP-SEG is CC BY 4.0. Publish only aggregate metrics and code, never images, masks or derived crops.

**Model weights:**

| Model | Licence | Access (HF API, 2026-11-06) |
| --- | --- | --- |
| DINOv1 ViT-S/16 (`facebookresearch/dino`) | Apache-2.0 | torch.hub, open |
| DINOv2 ViT-S/14, with registers (`facebook/dinov2-small`, `-with-registers-small`) | Apache-2.0 | open |
| DINOv3 ViT-S/16, ViT-B/16 (`facebook/dinov3-vits16-pretrain-lvd1689m` etc.) | DINOv3 License (custom, "other") | **gated, manual approval** |

Ask for DINOv3 access on Hugging Face early.

## Environment

The repo has no `requirements.txt`. From its imports you need: Python 3.10+, PyTorch 2.x with CUDA, `lightning`, `hydra-core`, `omegaconf`, `albumentations`, `wandb` (logging, optional), `timm`, and `torch.hub` access to `facebookresearch/dino`, `dinov2` and `dinov3`. Add `monai` or `segmentation-models-pytorch` for metrics and baselines, and `nnunetv2` if you rerun nnU-Net.

**Code licence:** [Trustworthy-AI-UU-NKI/RepMatters](https://github.com/Trustworthy-AI-UU-NKI/RepMatters) has **no licence file**, so read it, but reimplement rather than copy. Its feature extractor is adapted from [ShirAmir/dino-vit-features](https://github.com/ShirAmir/dino-vit-features) (MIT), which you may reuse with attribution.

## Step-by-step replication

1. **Splits.** The six DG and six ESDG fold files (`gener_folds/*.json`) were deleted from the repo on 2026-08-10. They are still in the commit history (commit `f1e4e5e`, 2025-12-04). Rebuild them from that commit, or write your own centre-wise splits. Each split entry lists image, mask, centre and a chromoendoscopy flag. Keep 10–20% of the training centres as a validation set for checkpoint selection.
2. **Preprocessing.** Resize to 224 × 224 and apply ImageNet normalisation. Augment with flips, rotation up to 45° (p = 0.5) and colour jitter (p = 0.3).
3. **Model.** Load the DINO ViT-S. Register a hook on the last block's qkv projection and keep the keys of all heads (6 heads × 64 = 384 dimensions). Drop the CLS and register tokens. Use stride 8 for v1/v3 (patch 16) and the matching 50% overlap for v2 (patch 14). Reshape to a grid, apply a 1 × 1 conv to 1,024 channels, then four (bilinear upsample + double conv) blocks and a 1 × 1 output conv with 2 classes.
4. **Freezing done right.** For the frozen arm, call `encoder.requires_grad_(False)` and `encoder.eval()`. Build the optimiser from trainable parameters only. **Assert** that the number of trainable parameters equals the decoder count, and that an encoder weight checksum is unchanged after one epoch. That check is the whole lesson of this paper.
5. **Training.** Dice loss, AdamW (the current code; the paper says Adam), lr 1e-5, batch 4, up to 300 epochs, mixed precision, best checkpoint by validation Dice.
6. **Evaluation.** Dice, recall and pixel accuracy per held-out centre, averaged across the 6 folds (as in the paper). Also report IoU, and per-image Dice with 95% bootstrap CIs.
7. **Baselines.** At least U-Net and nnU-Net (2D). UM-Net is optional: its decoder needs skip connections, and the authors used a modified version.

**Cost-saving tip for the frozen arm:** with the encoder frozen and no augmentation, you can cache key features once per image and train only the decoder on the cache. That is minutes per fold. Run the augmented version only for the final models.

## Compute and cost

- ViT-S at 224 px, about 1,300 training images: roughly 0.5–1.5 GPU-h per 300-epoch run on an A40/L4 (estimate; the authors used an RTX 8000).
- Full replication (4 DINO versions × frozen/fine-tuned × 12 folds) is about 96 runs, or 50–100 GPU-h. Do a reduced set first: DINOv2 and DINOv3, both arms, all 12 folds (48 runs, about 25–50 GPU-h, roughly US$10–25 on RunPod).
- The external-testing extension adds about 10–20 GPU-h. Analysis runs on a laptop.

## Target numbers

Use the **corrected** README table (August 2026), not v1 Table 1. Mean Dice × 100 across folds:

| Model | DG Dice | ESDG Dice |
| --- | --- | --- |
| nnU-Net | 65.09 | 52.36 |
| UM-Net (full loss) | 73.26 | 63.22 |
| DINOv2 frozen (A) | 72.71 | 66.00 |
| DINOv3 frozen (A) | 70.42 | 63.53 |
| DINOv2-R fine-tuned (B) | 76.34 | 70.92 |
| DINOv3 fine-tuned (B) | 79.88 | 73.47 |

The fold-to-fold standard deviation is large (12–14 Dice points in DG), mostly because C6 (88 frames) behaves differently. A replication is successful if (a) fine-tuned DINOv3 is best, (b) frozen encoders lose about 7–10 Dice points, and (c) your means fall within one fold-SD of these.

## Known pitfalls

- **The freezing bug itself.** Check trainable-parameter counts and encoder checksums in every run, and log them in the results.
- **v1 numbers are fine-tuned numbers.** Never cite v1 Table 1 as frozen results.
- **Fold files are gone from the current tree.** Use commit `f1e4e5e` or document your own splits.
- **`keyvitseg/main.py` does not run as published.** On 2026-11-06 it fails Python parsing: there is a stray top-level `else:` after the freeze block. The README also says `train.case: A/B`, but the code reads `extractor.freeze`. Expect to fix things, which is another reason to reimplement.
- **C6 is tiny.** With 88 frames, leave-C6-out folds have wide CIs. Report per-centre results, not only the mean.
- **Sequence-frame leakage.** If you add PolypGen sequence frames, keep each sequence inside one split.
- **Dataset overlap.** Kvasir-SEG is part of HyperKvasir, and PolypDB's Norway images come from HyperKvasir. Run a perceptual-hash check across all sets before testing.
- **Shortcut cues.** Kvasir images often show the green ScopeGuide thumbnail. Check whether masks or predictions react to it.
- **Licences.** NC terms on Kvasir-SEG and CVC-ClinicDB, and PolypGen's no-redistribution rule. Publish metrics and code only.

## Claude Code task list

1. Create a separate analysis repo `polypgen-dino-frozen-analysis`. Add `data/`, `features/` and `checkpoints/` to `.gitignore`. Never commit images, masks or features.
2. `get_data.md`: manual steps for Synapse (PolypGen), Zenodo (FAR-POLYP-SEG), OSF (PolypDB), Kvasir-SEG and the chosen CVC-ClinicDB mirror. Record SHA-256 checksums.
3. `splits.py`: rebuild the 6 DG and 6 ESDG folds from commit `f1e4e5e`, or create centre-wise splits with a fixed seed. Write JSON under `splits/` (filenames only).
4. `dedup.py`: perceptual hashes across PolypGen, Kvasir-SEG, CVC-ClinicDB, PolypDB and FAR-POLYP-SEG. Report and drop near-duplicates.
5. `model.py`: a DINO key extractor (v1/v2/v2R/v3) plus the decoder, with `--freeze`. Assert trainable-parameter counts and encoder checksums.
6. `train.py`: Lightning training with Dice loss and best-by-val-Dice selection, logging the parameter counts. Add `cache_features.py` for fast frozen runs.
7. `eval.py`: per-image Dice, IoU and recall, per-centre tables, and bootstrap CIs. Write `results/*.csv` (aggregates only).
8. Compare with the corrected targets above. Write `results/replication.md` with a table of your numbers against the README numbers.
