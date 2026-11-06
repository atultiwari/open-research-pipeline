---
enriched: true
---
## What the original study did

Kazemi et al. (Technical University of Munich; npj Digital Medicine 2026, open access) benchmarked 19 pathology foundation models, plus a ResNet50 baseline, as frozen feature extractors for CLAM attention-MIL on 3,528 H&E biopsy slides from 790 patients in the German multicentre BarrettNet cohort. The slides were PAXgene-fixed rather than formalin-fixed. There were two tasks:
- **Morphological subtyping into four classes:** normal/non-Barrett 41%, Barrett's without dysplasia 48%, Barrett's with dysplasia 4%, adenocarcinoma 7%.
- **Adenocarcinoma detection.**

They ran 10-fold cross-validation at several magnifications. The five models that agreed best with the expert consensus ("expert-consistent", ExCo: Virchow2, UNI2-h, Hibou-L, Virchow, UNI) were then combined into a multi-magnification ensemble. The ensemble reached subtyping AUROC 0.907 and κ 0.651, and detection AUROC 0.909 and κ 0.673. Gains over single models were uneven, and dysplasia stayed poorly detected.

**Not directly replicable.** The data availability statement says the BarrettNet slides are not public and are available only on request with institutional approval. The custom evaluation and ensembling scripts are also available only on request. No open whole-slide cohort covers non-dysplastic Barrett's and dysplasia:
- Searches of Zenodo, Hugging Face and Europe PMC on 2026-11-06 found only single-cell and CODEX data (Zenodo 14976467) and model weights with annotations under embargo (Zenodo 17583572, CC-BY-NC-ND).
- GTEx oesophagus notes mention Barrett's or intestinal metaplasia in only 2 of 622 mucosa samples.

The only part that can be rebuilt on open data is adenocarcinoma detection and typing, using TCGA-ESCA tumours and GTEx normal oesophagus/GE-junction slides as a surrogate.

## Data

| Dataset | What | Access | How to get it |
| --- | --- | --- | --- |
| TCGA-ESCA | 158 open diagnostic slides: 65 adenocarcinoma NOS + 1 tubular adenocarcinoma, ~92 squamous (GDC API, 2026-11-06) | Open | `datasets/tcga`; GDC portal or IDC collection `tcga_esca` |
| GTEx oesophagus | Non-diseased postmortem oesophagus mucosa and gastroesophageal junction slides with pathology notes | Open (licence: verify) | `datasets/gtex-histology`; GTEx histology viewer or IDC collection `gtex` |

Download into `data/` (gitignored). IDC serves slides as DICOM from public cloud buckets (`idc-index` Python package); TCGA SVS files are ~0.5–1 GB each.

## Environment

The source used Python 3.11.7, OpenSlide 1.3.1, PyTorch 2.5.1 (CUDA 12.4), [TRIDENT](https://github.com/mahmoodlab/TRIDENT) for patching and features, and [CLAM](https://github.com/mahmoodlab/CLAM) for MIL. Encoders: Virchow, Virchow2, UNI, UNI2-h, Hibou-L, H-optimus-0, CONCH/CONCHv1.5, Prov-GigaPath, Kaiko ViT variants and others (most gated on Hugging Face, several CC-BY-NC-ND).

## Step-by-step replication (surrogate)

1. Pull the TCGA-ESCA diagnostic slide manifest and the GTEx oesophagus mucosa and GE-junction slide list. Record each slide's fixation and source.
2. Patch with TRIDENT at 10× and 20×; extract features with 6–10 encoders, including the five ExCo models.
3. **Task A, adenocarcinoma vs squamous (TCGA only):** removes the GTEx/TCGA source confound.
4. **Task B, normal vs adenocarcinoma:** GTEx vs TCGA. Report it with a source-classifier control (Gap 2 in `extension.md`).
5. Train CLAM per encoder and magnification with 10-fold patient-level Monte Carlo CV (80% train, 10% validation, 10% test), as the source did.
6. Rebuild the source's ExCo selection: rank single models by κ with the reference on the same folds, and ensemble the top five by averaging probabilities.
7. Rebuild the same ensemble with nested selection (choose members on inner folds only), and compare.

## Compute and cost

- Slide download is ~1 TB transient: 160 TCGA slides plus about 1,000 GTEx slides; subsample GTEx if storage is tight.
- Features: ~20–40 GPU-h on an L4 or A40 (RunPod ~US$10–25). CLAM training is minutes per fold.

## Target numbers (source, BarrettNet; not expected on the surrogate)

- **Subtyping:** best single AUROC 0.901 (Virchow); ensemble AUROC 0.907, F1 0.696, accuracy 0.795, κ 0.651 (Table 1).
- **Detection:** ensemble AUROC 0.909, F1 0.836, accuracy 0.959, κ 0.673; Kaiko ViT-S16 and ViT-L14 single-model AUROC 0.903.
- **Agreement:** best single κ with the reference 0.638 (Virchow2); Fleiss' κ 0.779 across models and the reference.
- **Heatmaps:** inter-rater ICC 0.651 for heatmap alignment.

## Known pitfalls

- **Source confound:** GTEx normal (postmortem, autolysis, research protocol) vs TCGA tumour (surgical, FFPE, many sites). A model can tell the source apart without seeing cancer. Always report a "which dataset?" classifier as a control.
- **Selection on the test folds:** choosing ensemble members by agreement with the reference across the same CV folds that report performance is optimistic. Use nested CV.
- **Small adenocarcinoma class:** only ~66 TCGA slides; report CIs per patient and avoid magnification sweeps that multiply comparisons.
- **Licences:** many encoders are NC-ND and gated; research only.

## Claude Code task list

1. Query the GDC and IDC for the TCGA-ESCA and GTEx oesophagus slide lists; save the manifests (IDs only) to the study folder.
2. Download slides to `data/` on a RunPod volume; patch with TRIDENT at 10× and 20×.
3. Extract features for the ExCo five plus CONCHv1.5, H-optimus-0 and ResNet50.
4. Train CLAM for Task A and Task B with 10-fold patient-level CV.
5. Build the ExCo ensemble two ways (same-fold vs nested selection); report the gap.
6. Train the source-classifier control for Task B.
7. Commit manifests, scripts and aggregate metric tables only.
