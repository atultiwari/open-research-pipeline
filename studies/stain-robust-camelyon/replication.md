---
enriched: true
---
## What the original study did

Schönpflug et al. (University of Basel and Leiden University Medical Center) propose a three-step protocol for stress-testing computational pathology models against H&E staining variation:
1. pick reference staining conditions from a library;
2. measure each test slide's own stain vectors and intensities (Macenko-style unmixing);
3. re-render every tile towards the reference stains and re-run the model.

They built the library from the WSI part of PLISM (13 stains × 7 scanners). They applied the protocol to 306 microsatellite-instability (MSI) classifiers on the public SurGen colorectal cohort (738 patients): 300 gated-ABMIL models trained on TCGA-COAD/READ (100 each on UNI2-h, H-Optimus-1 and Virchow2 features) and 6 published models. There were four simulated conditions: low and high H&E intensity, and low and high H&E colour similarity. Robustness was defined as the min–max AUC range across the reference and the four simulated conditions. Robustness varied widely and was only weakly related to AUC.

**Publication status (checked 2026-11-06).** The peer-reviewed version is in the *Journal of Pathology Informatics* 22, 100702 (August 2026, CC BY 4.0), [doi:10.1016/j.jpi.2026.100702](https://doi.org/10.1016/j.jpi.2026.100702), open copy [PMC13545398](https://pmc.ncbi.nlm.nih.gov/articles/PMC13545398/). The preprint is [arXiv 2603.12886v1](https://arxiv.org/abs/2603.12886). The register's label "CVPR 2026" could **not** be confirmed. Neither the paper nor the arXiv comment field mentions CVPR. The CVF open-access listings for CVPR 2026, CVPR 2026 Findings and 11 medical or robustness workshops (CVMI, CV4Clinic, FoundGen-Bio, MULA, DataCV, DG-EBF, SAIAD, PHAROS-AIF-MIH, Med-Reasoner, BIOM, SAFE) contain no paper by these authors with this title.

**The r = −0.22 / −0.28 discrepancy, resolved.** The quantity is the Pearson correlation between reference AUC and robustness, defined as the min–max AUC range.
- arXiv v1 abstract: r = −0.22, 95% CI [−0.34, −0.11].
- arXiv v1 Results §3.3 (Fig. 4a, n = 306): r = −0.28, 95% CI [−0.39, −0.17].
- The published JPI abstract and Results both give **r = −0.28, 95% CI [−0.39, −0.17]**.

So −0.22 was a preprint abstract error, corrected at publication. Cite −0.28 from the JPI version. Note the sign: a *negative* correlation with the AUC *range* means that higher-AUC models tended to have slightly *smaller* ranges, i.e. to be slightly more robust. The relationship is weak, which is what both versions emphasise. Per-extractor values are unchanged: UNI2-h r = −0.51, Virchow2 −0.36, H-Optimus-1 −0.14 (not significant).

**Other changes between versions (read both).**
- PLISM variance decomposition (§3.1): the arXiv text says hematoxylin intensity varied more across stains and stain-vector angle more across scanners. The JPI text reverses this: colour similarity varies more across *stains*, and intensities slightly more across *scanners*. The discussion's practical advice changed with it.
- The JPI limitations section is longer. It adds an explicit statement that the findings are specific to colorectal cancer and MSI, and a fourth limitation that AUC is rank-based and may hide calibration shifts.

## Data

| Dataset | Use | Access | Size and notes |
| --- | --- | --- | --- |
| TCGA-COAD/READ (`datasets/tcga`) | Original development set (600 WSIs) | Open, GDC | Only for a strict replication |
| SurGen ([BioImage Archive S-BIAD1285](https://www.ebi.ac.uk/biostudies/bioimages/studies/S-BIAD1285)) | Original test set | Open (per the paper) | Not in `datasets/`; licence **verify** before use |
| PLISM-wsi (`datasets/plism`) | Source of the stain reference library | Open, CC BY 4.0 | You do **not** need the images: the derived references are released |
| CTPLab stain library and results ([HF dataset](https://huggingface.co/datasets/CTPLab-DBE-UniBas/staining-robustness-evaluation)) | PLISM references, SurGen stain properties, 300 trained models, results | Open, Apache-2.0, not gated (HF API, 2026-11-06) | Small; download first |
| CAMELYON16 (`datasets/camelyon16`) | Development set for the extension | Open, CC0, no account | 399 WSIs, 752.5 GB |
| CAMELYON17 (`datasets/camelyon17`) | Real multi-centre external test | Open, CC0, no account | 500 labelled training WSIs, 1,461 GB; test-set labels are not public |

**Getting CAMELYON without filling a disk.** The data are on AWS Open Data: `aws s3 ls --no-sign-request s3://camelyon-dataset/` (bucket in us-west-2, no account). Do not mirror the whole 3.7 TB.
- Stream one slide at a time: download, detect tissue, read tiles at 1 µm/px (as in the source), cache the tile pixels locally, then delete the WSI.
- Measure the cache size on 10 slides before committing to a volume size.
- Precomputed open features exist for CAMELYON16 (e.g. `torchmil/Camelyon16_MIL`, Apache-2.0, which also provides tile coordinates; `owkin/camelyon16-features`, Owkin non-commercial). They cover the *unaltered* stain only, so they cannot replace re-extraction under simulated stains. They are useful as a reference-condition sanity check, and the torchmil coordinates can save the tissue-detection step (check the tile size and magnification match).
- Keep everything under `data/` (gitignored) or on a RunPod network volume.

**Model access (HF API, 2026-11-06).**

| Model | Licence | Gating | Role |
| --- | --- | --- | --- |
| UNI2-h | CC-BY-NC-ND-4.0 | auto | Source FM |
| Virchow2 | CC-BY-NC-ND-4.0 | auto | Source FM |
| H-optimus-1 | CC-BY-NC-ND-4.0 | **manual** | Source FM (request early) |
| H-optimus-0 | Apache-2.0 | auto | Open-licence FM |
| Hibou-L | Apache-2.0 | auto | Open-licence FM |
| Midnight (kaiko-ai) | MIT | not gated | Open-licence FM |
| Phikon-v2 | "other" | not gated | Optional |
| CTransPath (public MSI models) | GPL-3.0 | not gated | Only for the strict MSI replication |

Academic, non-commercial use only for the NC-ND models. Do not redistribute their features.

## Environment

The repo has no `requirements.txt`. Its README asks for Python ≥ 3.8 and PyTorch, plus `torchvision numpy scikit-image openslide-python opencv-python-headless timm huggingface-hub einops pillow scipy shapely pandas matplotlib seaborn scikit-learn`. Use Python 3.10 or 3.11 with a recent PyTorch, and pin the versions you use in your own `requirements.txt`. OpenSlide needs the system library (`apt-get install openslide-tools`). The Philips-derived CAMELYON17 TIFFs read with OpenSlide, according to the dataset paper.

## Step-by-step replication

**A. Strict replication on MSI (optional, heavy).** The source used 444 H200 GPU-hours.
1. Clone [CTPLab/staining-robustness-evaluation](https://github.com/CTPLab/staining-robustness-evaluation) (Apache-2.0). The HF card links to a personal fork (`lely475`); use the CTPLab repo.
2. Download the HF artefacts: `plism-wsi_stain_references`, `surgen_stain_properties`, `MSI_classification_models/*`, `exp_results`.
3. Cheapest check: rerun `controlled_staining_simulations/evaluate_results.ipynb` on the released `exp_results` and reproduce Fig. 4a and Table 1. This needs no GPU.
4. Full rerun: `extract_features.py` on SurGen under the five conditions, then `apply_simulated_models.py`. The released models make retraining (`train_abmil.py`) unnecessary.

**B. Port the protocol to CAMELYON (the basis of the extension).**
1. Step 1: reuse the four PLISM references from the HF library (low and high intensity, Harris and Gill vectors).
2. Step 2: run `stain_vector_concentration_extraction/unmix_wsi_v1.py` on every CAMELYON16 and CAMELYON17 slide. Lymph nodes have a lot of dense hematoxylin and sometimes anthracotic pigment, so check the unmixing logs and tune `config.py` thresholds on 20 slides first.
3. Tile at 1 µm/px, 224 px. Re-render each tile to the four references and run each FM (`extract_features.py`). Cache features as `.h5` per slide, model and condition.
4. Train gated-ABMIL models on CAMELYON16 training slides (`train_abmil.py`, adapted to binary metastasis labels), sampling seeds, weight decay and splits as in the source. Use about 50 models per FM.
5. Apply the models to the CAMELYON16 test set and the CAMELYON17 training set under all five conditions (`apply_simulated_models.py`).
6. Compute reference AUC, min–max AUC range and bootstrap CIs exactly as in source §2.5.

## Compute and cost

- Strict MSI rerun: hundreds of GPU-hours. Skip it, or limit it to the notebook check in A3.
- CAMELYON port, about 900 WSIs:
  - Feature extraction is 5 conditions × 3–4 FMs. Rough estimate 40–80 GPU-h on an A100/L40S class GPU (RunPod, about US$40–120), plus CPU time for WSI reading. Re-time it on 10 slides.
  - Download is about 2.2 TB from S3, streamed per slide.
  - ABMIL training and evaluation run on one GPU or a strong CPU in hours.

## Target numbers

From the JPI version, for strict replication:
- Reference AUC range 0.769–0.911.
- Robustness range 0.007–0.079.
- Pearson r = −0.28 [−0.39, −0.17], n = 306 (Fig. 4a).
- Per-FM median AUC: UNI2-h 0.881, H-Optimus-1 0.865, Virchow2 0.856 (Appendix D).
- Ten "high-performing, robust" models (AUC > 0.90, range < 0.03), mostly UNI2-h+ABMIL (Fig. 4b).
- Table 1: high intensity was most often the best condition (127/306 models). Worst-case drops: −7.78% for high colour similarity, about −4.5% for intensity changes.

For CAMELYON there are no published targets under this protocol. As a sanity check, unaltered FM+ABMIL slide-level AUC on the CAMELYON16 test set is typically in the mid to high 0.9s.

## Known pitfalls

- **Cite the JPI numbers.** Use r = −0.28. Note that the PLISM variance statements reversed between versions.
- **Ceiling effect.** CAMELYON16 slide AUC is near saturated for modern FMs, so min–max AUC ranges may be tiny. Add sensitivity at fixed specificity, ECE and Brier score, and analyse ITC and micro-metastasis slides separately.
- **Centre overlap.** CAMELYON16 came from RUMC and UMCU, which are also CAMELYON17 centres. Report CWZ, RST and LabPON as the true external centres.
- **Label granularity.** CAMELYON17 slide labels include ITC. Decide in advance whether ITC counts as positive (clinically pN0(i+)), and report both choices.
- **Unmixing failure.** The Macenko-style unmixing is unreliable on blood, necrosis and pigment (JPI limitation 5). Lymph-node capsules and sinus histiocytes with pigment need QC.
- **Licences.** The FM licences (NC-ND) forbid sharing weights or derived features. Commit only code and aggregate metrics.
- **Pretraining overlap.** Some FMs may have seen CAMELYON or TCGA slides during pretraining. Check each model card and report it.

## Claude Code task list

1. Request HF access: UNI2-h, Virchow2 (auto); H-optimus-1 (manual, institutional email); H-optimus-0 and Hibou-L (auto).
2. Clone the CTPLab repo outside this repo. Download the HF stain library and `exp_results`, and reproduce Fig. 4a and Table 1 from the notebook (no GPU).
3. Write `code/stream_camelyon.py`: list the S3 keys, download one slide, detect tissue, tile at 1 µm/px, cache, delete. Time it on 10 slides.
4. Run `unmix_wsi_v1.py` on all CAMELYON slides. QC 30 slides visually (Atul). Save slide-level stain properties (aggregate CSV, no pixels).
5. Extract features under 5 conditions × chosen FMs on RunPod. Write a manifest of what has been done.
6. Train the ABMIL model population on CAMELYON16 training slides. Evaluate on the CAMELYON16 test set and CAMELYON17 under all conditions.
7. Compute AUC, AUC range, ECE, Brier score and size-stratified sensitivity, with 1,000 bootstrap resamples. Commit only aggregate tables and figures.
8. Run `python3 scripts/validate.py` before any commit.
