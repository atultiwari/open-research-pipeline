---
enriched: true
---
## Gap analysis

Sources read:
- the arXiv full text (v1, HTML);
- the *Scientific Data* landing page;
- the Hugging Face card and file listing;
- the GitHub README of the segmentation code.

**Novelty searches** (2026-11-06, all public APIs):

| # | Search | Result |
| --- | --- | --- |
| 1 | OpenAlex works citing the article (`filter=cites:W7156926194`) and the HF dataset record (`cites:W7148553238`) | 0 results each |
| 2 | OpenAlex full-text search `HepatoBench` | 3 hits: the dataset, the article, and PathJev (arXiv:2610.32478) |
| 3 | Semantic Scholar citations for arXiv:2604.22858 | Rate-limited (HTTP 429), not checked |
| 4 | arXiv: `abs:liver AND abs:histopathology AND abs:"foundation model"`, newest first | Only OpenTME (arXiv:2604.12075) was relevant |
| 5 | OpenAlex: "hepatocellular carcinoma tissue composition whole slide deep learning survival TCGA-LIHC" (from 2021) | See Gap 3 |
| 6 | OpenAlex: "liver histopathology foundation model tissue classification benchmark" (from 2025) | No liver-specific foundation-model benchmark found |
| 7 | OpenAlex: "patch-level data leakage histopathology benchmark duplicate split inflation" (from 2023) | One related audit of multimodal WSI benchmarks (arXiv:2607.12278), not liver patches |

### Gap 1: No leakage-free split is possible; the published accuracy may be inflated

- **Evidence.**
  - The paper (Technical Validation; Data Records) says the split was done at slide level and that the partition was released.
  - The Hugging Face release has only class zips named `<class>_<index>.png` and a metadata file: no slide IDs and no split files (checked 2026-11-06).
  - PathJev (arXiv:2610.32478, Table 1 and footnote) found exact duplicates in the release, and noted that neighbouring indices appear to come from the same tissue.
- **Novelty check.** No work measures how much random patch splits inflate HepatoBench results (searches 1, 2, 6 and 7). PathJev used a 5,000-image draw only as a test set and treated images as independent; it did not quantify the inflation.
- **Open data:** `hepatobench`.
- **Design.**
  - *Hypothesis:* grouped, duplicate-aware splits lower macro-F1 noticeably compared with random splits, and change how the encoders rank.
  - *Methods:* MD5 and pHash audit; pseudo-groups from index runs and from embedding clusters; random versus grouped splits with five seeds; linear probes on frozen encoders.
  - *Metrics:* macro-F1, balanced accuracy, the inflation (random minus grouped), and how the ranking changes (Kendall τ).
  - *Reporting guideline:* CLAIM 2024.
- **Rating:** feasibility 5, novelty 4, Colab, 4–5 weeks.

### Gap 2: Outdated encoders, no confidence intervals and no calibration

- **Evidence.**
  - Only UNI, Virchow2 and GigaPath were tested, all as linear probes (Methods, "Liver Tissue Region Classification").
  - Results appear only in Figure 2, with no CIs, seeds or calibration.
  - The text says "four encoders" but lists three.
- **Novelty check.** No HepatoBench benchmark of UNI2-h, H-optimus-0/1, H0-mini, Phikon-v2, CONCH v1.5 or a general-domain DINOv2 baseline was found (searches 2, 4 and 6). PathJev used H-optimus-0 only as a supervised reference probe on 5,000 images.
- **Open data:** `hepatobench`.
- **Design.**
  - *Methods:* the eight to ten encoders listed in `replication.md`; linear and kNN probes; label-efficiency curves (1%, 5%, 10%, 100% of training groups); a laptop-CPU run of H0-mini for low-resource settings.
  - *Metrics:* macro-F1 with 95% bootstrap CIs over groups; expected calibration error; Brier score; images per second on CPU.
  - *Reporting guideline:* CLAIM 2024.
- **Rating:** feasibility 5, novelty 3 on its own; it becomes strong when combined with Gap 1. Colab, 3–4 weeks.

### Gap 3: Slide-level tissue composition has not been tested against outcome

- **Evidence.** HepatoQuant outputs composition reports, but the paper reports no survival or clinical-outcome analysis. It cites TCGA only as background.
- **Novelty check.** HCC histology–prognosis work on TCGA-LIHC is crowded, so the novelty here is limited to interpretable, pathologist-readable tissue fractions:
  - Shi et al., *Gut* 2020, doi:10.1136/gutjnl-2020-320930;
  - Wu et al., *Frontiers in Oncology* 2026, doi:10.3389/fonc.2026.1849274, a CONCH-based risk model on TCGA plus one hospital cohort.

  OpenTME (arXiv:2604.12075) already releases foundation-model tissue and cell readouts for TCGA liver slides. That is a ready comparator, but it also overlaps this gap.
- **Open data:** `tcga` (TCGA-LIHC diagnostic slides: 379 slides, 365 cases, 503.5 GB) with TCGA-CDR endpoints; `opentme` as the comparator.
- **Design.** Tile the slides and classify each tile with the best Gap 1/2 encoder. Compute necrosis, fibrosis, steatosis and inflammation fractions. Fit Cox models adjusted for stage and grade, and report C-index and time-dependent AUC. Check agreement with the OpenTME readouts. Reporting guidelines: REMARK and TRIPOD+AI.
- **Rating:** feasibility 3 (about 500 GB of slides), novelty 3, RunPod, 8–10 weeks.

### Gap 4: No external validation on another centre or scanner

- **Evidence.** All data come from one hospital. The Technical Validation section reports internal splits only.
- **Novelty check.** No external test of HepatoBench-trained classifiers was found (searches 1, 2 and 6).
- **Open data:** `paip2019`: 50 resection WSIs from three Korean hospitals, scanned on an Aperio AT2, with whole-tumour and viable-tumour masks. The data use agreement still needs checking.
- **Design.** Classify PAIP tiles. Measure tumour versus non-tumour agreement with the whole-tumour mask (Dice). Within the tumour, compare the predicted necrosis/fibrosis fraction with the non-viable area (whole tumour minus viable). Reporting guideline: CLAIM 2024.
- **Rating:** feasibility 4, novelty 4, RunPod ~5 GPU-h, 3 extra weeks.

### Gap 5: Label quality and a pathologist error taxonomy

- **Evidence.**
  - Class names are partly mistranslated: "Steroidal Degeneration" means steatosis, and "Biliary Reaction" means ductular reaction.
  - REA has only 1,540 patches.
  - The paper reports no inter-observer agreement.
- **Novelty check.** No label audit of HepatoBench was found (searches 1, 2 and 7).
- **Open data:** `hepatobench`.
- **Design.** Atul reviews a stratified sample of misclassified and cross-class-duplicate patches (e.g. 50 per confusion pair). He categorises each as a label error, an ambiguous patch (mixed tissue), an artefact, or a true model error, and reports the share of each. Reporting guideline: CLAIM 2024.
- **Rating:** feasibility 5, novelty 3, laptop, 1–2 weeks. This is a strong fit for a pathologist.

## Recommended extension

**Combine Gaps 1, 2 and 5, with Gap 4 as a secondary external arm.** The working title: *How much of liver tissue-classification accuracy is leakage?* The study:
1. measures the inflation from random patch splits on HepatoBench;
2. re-benchmarks current open encoders under duplicate-aware grouped splits, with CIs and calibration;
3. adds Atul's error taxonomy;
4. tests transfer to PAIP 2019.

**Why this one:**
- **Speed:** about 3.6 GB of data and under 12 GPU-hours, so the core is preprint-ready in about 6 weeks.
- **Novelty:** the leakage question has been raised (PathJev) but never measured, and the dataset has just been published in *Scientific Data*, so the finding is timely and useful to every later HepatoBench user.
- **Fit:** the error taxonomy and label audit draw on pathology expertise that ML groups lack.
- **Journals:** suits imaging-informatics journals with a zero-APC route, such as J Imaging Informatics in Medicine, Computerized Medical Imaging and Graphics, or Laboratory Investigation for the pathology framing.

**Gap 3 (survival on TCGA-LIHC)** is better kept as a follow-up study, because the area is crowded and the data are large.
