---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** Sáez-Maldonado et al., CMPB 2027 ([doi:10.1016/j.cmpb.2026.109700](https://doi.org/10.1016/j.cmpb.2026.109700)). Patch-level, frozen encoders, two Spanish cohorts, one official split each. Rankability idea taken from Sonthalia et al., "On the rankability of visual embeddings" (NeurIPS 2025, [doi:10.52202/085713-2222](https://doi.org/10.52202/085713-2222)).
- The source has no citing works yet (Crossref `is-referenced-by-count` 0, 2026-11-06).

**Searches run on 2026-11-06** (OpenAlex refused: daily budget used up; fell back to Crossref and Europe PMC, both from 2023 onwards):
- "ordinal Gleason pattern foundation model external validation"
- "conformal prediction Gleason grading"
- "Gleason pattern SICAPv2 Arvaniti external validation foundation model"
- "rankability foundation model embeddings ordinal"
- "ordinal regression Gleason calibration cross-dataset"

**Nearest work found:**
- Ordinal conformal prediction for diabetic retinopathy grading (Diagnostics 2026, [doi:10.3390/diagnostics16162645](https://doi.org/10.3390/diagnostics16162645)): same idea, different organ, not pathology.
- EfficientNet with ordinal focal loss for prostate grades (Bioengineering 2026, [doi:10.3390/bioengineering13050503](https://doi.org/10.3390/bioengineering13050503)): ordinal loss, no foundation models, no rankability.
- A conference abstract on Gleason pattern segmentation from foundation-model features (J Urol 2026, [doi:10.1097/01.ju.0001191428.57520.39.04](https://doi.org/10.1097/01.ju.0001191428.57520.39.04)): segmentation, not ordinal or calibration.
- Ebbert et al., medRxiv July 2026 ([doi:10.64898/2026.07.28.26359127](https://doi.org/10.64898/2026.07.28.26359127)): slide-level triage by cancer-tissue fraction across scanners; not patch-level ordinal grading.

None tests ordinal GPs, or foundation-model rankability, on an external Gleason cohort.

### Gap 1: No external validation

- **Evidence:** each dataset is evaluated only on its own official split, and all five seeds share that split; the authors say their tests capture initialisation variance, not data variance (Section 3.6). Both cohorts are Spanish and from the same research network.
- **Novelty check:** the five searches above found no external test of OGP or of rankability-guided encoder choice for Gleason grading.
- **Open data:** `arvaniti-tma` (Zurich, CC0, pixel masks benign/G3/G4/G5), `panda` (Radboud gland-level G3/G4/G5 masks, Kaggle rules). Training on `sicapv2` and `crowdgleason`.
- **Design sketch:**
  - *Hypothesis:* the OGP's advantage over multi-class GP and SVM grows under site shift, because external embeddings are less rankable; in-domain rankability ranks encoders the same way external kappa does.
  - *Data:* train on SICAPv2, on CrowdGleason, and on both pooled. Test on Arvaniti TMA cores and on patches cut from PANDA-Radboud masks (majority-label patches, mapped to the four classes; stroma excluded).
  - *Methods:* OGP, MGP, SVM, ordinal logistic regression, CORF; 4–7 encoders. Measure external rankability using the training-set projection.
  - *Metrics:* quadratic weighted kappa, ECE, Brier score, non-adjacent error rate, all with patient/core-level bootstrap CIs; Spearman between in-domain and external rankability.
  - *Reporting guideline:* CLAIM 2024 with TRIPOD+AI external-validation items.
- **Rating:** feasibility 4, novelty 4, RunPod, 4 weeks.

### Gap 2: Calibrated probabilities are not turned into decisions

- **Evidence:** the paper argues calibration matters for clinical use (Sections 4.3, 5) but stops at ECE and reliability diagrams. It cites conformal prediction for ordered classes as related work (Section 1.1) without applying it.
- **Novelty check:** found ordinal conformal prediction only for diabetic retinopathy (above); nothing for Gleason patterns on foundation-model features.
- **Open data:** same as Gap 1.
- **Design sketch:**
  - *Hypothesis:* ordinal (contiguous) conformal sets built on OGP probabilities are smaller at the same coverage than sets from MGP or SVM, and keep coverage better under site shift.
  - *Methods:* split-conformal and ordinal-contiguous sets (e.g. G3–G4) at 90% and 95% coverage; calibrate in domain, test in and out of domain; a referral rule: send to the pathologist when the set spans more than one grade, or includes G4/G5 with benign.
  - *Metrics:* empirical coverage, mean set size, referral rate, kappa on retained patches.
  - *Reporting guideline:* CLAIM 2024.
- **Rating:** feasibility 5, novelty 4, laptop once features exist, 2 weeks on top of Gap 1.

### Gap 3: Label noise is modelled with one global variance

- **Evidence:** the authors restricted the ordinal noise to a single σ²δ (Section 2.2.1), and found its test-time treatment changes ECE several-fold (Tables 5–6). They blame CrowdGleason's low rankability on label noise (Section 4.1) without measuring it per patch.
- **Novelty check:** no Gleason study found that compares a learned per-patch noise term with measured annotator disagreement.
- **Open data:** `crowdgleason` (crowd vs expert labels; whether `Annotations.zip` holds per-annotator labels needs checking), `arvaniti-tma` (second-pathologist annotations on the test TMA, verify).
- **Design sketch:** heteroscedastic OGP (σδ as a function of x); test whether high predicted noise flags patches where annotators disagreed. Metrics: AUROC of noise for disagreement, kappa and ECE versus the homoscedastic model. CLAIM 2024.
- **Rating:** feasibility 3, novelty 4, RunPod, 4 weeks.

### Gap 4: Patch level only

- **Evidence:** the authors name slide-level prediction and slide encoders (TITAN, PRISM) as future work (Section 5).
- **Novelty check:** slide-level ISUP grading on PANDA is well covered (the PANDA challenge itself); the new part would only be ordinal-GP aggregation.
- **Open data:** `panda`.
- **Design sketch:** aggregate patch OGP outputs into primary + secondary pattern and ISUP grade; compare with an ordinal head on TITAN slide embeddings. Kappa vs ISUP.
- **Rating:** feasibility 2 (412 GB, heavy compute), novelty 2, RunPod, 8+ weeks. Not recommended now.

### Gap 5: No pathologist review of severe errors

- **Evidence:** the t-SNE figures separate adjacent from non-adjacent errors (Figs 7–8) but nobody looks at what those patches show.
- **Novelty check:** no foundation-model Gleason paper found with a morphology-based error taxonomy.
- **Open data:** any of the above; images are openly licensed, so example tiles can be shown in a paper under CC BY / CC0 (check each dataset's attribution terms).
- **Design sketch:** Atul reviews a stratified sample of non-adjacent errors and high-uncertainty referrals (e.g. 200 patches) and codes them: benign mimics (atrophy, adenosis, HGPIN, inflammation), cribriform vs fused G4, tangential cuts, crush or edge artefact, stain issues, label error. Report frequencies by encoder and classifier.
- **Rating:** feasibility 5, novelty 3, laptop, 1–2 weeks of review.

## Recommended extension

**Gaps 1 + 2 + 5 together:** external validation of the OGP on the Zurich TMAs and PANDA-Radboud, conformal referral sets, and Atul's taxonomy of the severe errors.

Why: every dataset is open and downloadable today (no credentialing); the authors' code is public, and only the external test adds work. It answers the obvious reviewer question the source leaves open (does it travel?), turns calibration into a referral rule a pathologist can judge, and the error taxonomy is work only a pathologist can do. Estimate six weeks to a preprint; CLAIM 2024 framing fits JIIM or CMPB (same journal as the source, as a direct follow-up). Gap 3 is a good second paper if per-annotator labels exist.
