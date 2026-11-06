---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** Thiringer et al., arXiv 2601.04163. Private breast cohort, 14 encoders, embedding metrics plus MIL. Calibration shifts were shown only as LOWESS plots, with no ECE or Brier score.
- **plismbench** (Filiot et al., arXiv 2501.16239, MICCAI 2025; [repo](https://github.com/owkin/plism-benchmark)): already ranks about 20 encoders on PLISM embedding stability (cosine similarity, top-10 retrieval across scanners and stains). A public MICCAI review noted that it used **only the PLISM-wsi subset** ([review page](https://papers.miccai.org/miccai-2025/0247-Paper4289.html)).
- **Lee et al., bioRxiv October 2026** ([doi:10.64898/2026.10.07.757122](https://doi.org/10.64898/2026.10.07.757122)): six scanners on normal tissue ("PanNormal"), with PLISM as external validation. Decomposes scanner effects into colour and frequency, and tests image-level corrections on 8 encoders. Embedding-level only, scanners only.

**Searches run on 2026-11-06:**
- OpenAlex works citing the source (W7119544620): 9 results.
- OpenAlex title/abstract search for "PLISM".
- arXiv search `all:PLISM`: 3 results (DistillPath 2608.17872, the CTPLab stain protocol 2603.12886, plismbench 2501.16239).
- Web search for PLISM + smartphone + foundation model + calibration.
- OpenAlex search for smartphone microscope pathology foundation model robustness, 2025 onwards.

**Result:** the original study's design is no longer new on its own. Re-running embedding stability on PLISM-wsi would duplicate plismbench. The extension therefore moves to what nobody has done on public data: smartphones, and the step from embedding drift to calibrated predictions.

### Gap 1: Smartphone capture is untested for foundation models

- **Evidence:** the source used scanners only (Section 3). plismbench and Lee et al. used PLISM-wsi only, even though PLISM-sm has 57,902 smartphone images registered to the same locations (Ochi et al. 2024).
- **Novelty check:** none of the above searches found a foundation-model evaluation on PLISM-sm (2026-11-06).
- **Open data:** `plism` (PLISM-sm + PLISM-wsi).
- **Design sketch:**
  - *Hypothesis:* smartphone capture moves embeddings further than any scanner change does, and the order of models differs from the scanner-only rankings.
  - *Data:* matched locations across 7 scanners and 6 phones, with the stain held fixed.
  - *Methods:* the source paper's metrics, reported per device pair.
  - *Metrics:* cosine distance, 1-NN, IoK, with bootstrap CIs.
  - *Reporting guideline:* CLAIM 2024.
- **Rating:** feasibility 5, novelty 4, Colab/RunPod, 3 weeks.

### Gap 2: Embedding drift is not linked to calibration of real predictions

- **Evidence:** the source shows probabilities drifting between scanners (Figs 9–10) but reports no calibration metric. It names calibration stability as a priority for future work (Section 6). plismbench and Lee et al. are embedding-only.
- **Novelty check:** web and OpenAlex searches found no PLISM study reporting ECE, Brier score or prediction flips across devices (2026-11-06).
- **Open data:** `plism`. Its per-tile tissue-type labels (46 types) give a supervised task with no extra annotation.
- **Design sketch:**
  - *Hypothesis:* devices with larger embedding drift cause larger calibration error and more prediction flips, even when balanced accuracy barely moves. Embedding-stability metrics predict this.
  - *Task:* linear probes (logistic regression) per encoder, trained on one reference scanner and stain for tissue type (46 classes, and a pathologist-grouped tumour-vs-non-tumour task). Tested on every other scanner and phone.
  - *Metrics:* balanced accuracy, ECE, Brier score, flip rate for the same tile across devices, and the Spearman correlation between embedding metrics and calibration loss.
  - *Reporting guideline:* CLAIM 2024 (with TRIPOD+AI calibration items).
- **Rating:** feasibility 5, novelty 4, laptop once features exist, 2 weeks on top of Gap 1.

### Gap 3: Cheap mitigations were not tested

- **Evidence:** the source lists normalisation and augmentation as untested (Section 6.3). Lee et al. test image corrections but not their effect on calibration.
- **Novelty check:** the CTPLab protocol (arXiv 2603.12886) covers stain variation for MSI, not device shift or smartphones.
- **Open data:** `plism`.
- **Design sketch:**
  - *Methods:* compare Macenko and Reinhard normalisation, colour augmentation during probe training, and per-device temperature scaling fitted on 100 tiles.
  - *Metrics:* recovery of ECE and flip rate as a share of the gap.
- **Rating:** feasibility 4, novelty 3, laptop/Colab, 2 weeks.

### Gap 4: Small and distilled encoders for low-cost settings

- **Evidence:** the source found that robustness does not track model size or recency. H0-mini (a ViT-B distillate) tops plismbench. DistillPath (arXiv 2608.17872, 22M parameters) appeared in August 2026.
- **Novelty check:** neither has been tested on smartphone images (as of the searches above).
- **Design sketch:** add small encoders and report robustness per GFLOP, plus CPU inference time, for district-hospital and smartphone deployment in India.
- **Rating:** feasibility 4, novelty 3, 1 extra week. Check DistillPath's licence and weights before use (**verify**).

### Gap 5: Pathologist error taxonomy on device failures

- **Evidence:** none of the three papers looks at *which* tissues fail on which devices.
- **Design sketch:** Atul reviews the 200 tiles with the largest cross-device flips and codes the causes (blur, glare, colour cast, cropping, ambiguous tissue). An error table per tissue type tells smartphone users which tissues they can trust.
- **Rating:** feasibility 5, novelty 4, about 1 week of expert time.

## Recommended extension

**Gaps 1 + 2 together, with 3–5 as secondary analyses:** "From scanner to smartphone: do pathology foundation-model embeddings that drift across imaging devices also break calibration? A registered public benchmark on PLISM."

Why this one:
- It is the only design that is both clearly new (no smartphone or calibration results exist for foundation models) and fully open (CC BY 4.0, no credentialing).
- It needs about 15 GPU-h.
- It makes direct use of Atul's expertise (tissue grouping, error taxonomy).
- It speaks to Indian and LMIC practice, where phone-on-microscope teleconsultation is common.

Expected time: about 5 weeks to a medRxiv/arXiv (eess.IV) preprint. Best-fit journals: J Imaging Informatics in Medicine, Computerized Medical Imaging and Graphics, Medical & Biological Engineering & Computing.
