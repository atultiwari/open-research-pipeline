---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** Monteiro et al., arXiv 2512.13376. v1 claimed frozen DINO keys beat specialised polyp networks on PolypGen. v2 (January 2026) withdrew the claims because of a freezing bug.
- **The authors have fixed the bug themselves.** Their renamed repo ([RepMatters](https://github.com/Trustworthy-AI-UU-NKI/RepMatters), August 2026, "accepted at MICCAI 2026 MLMI") now reports frozen and fine-tuned encoders side by side. Truly frozen encoders lose 7–10 Dice points, and only fine-tuned DINOv3 beats UM-Net (see `replication.md`). **A "correctly frozen re-evaluation" is therefore no longer new on its own.** The original stub's main idea has been overtaken.
- **Still missing from the corrected version:** any test outside PolypGen; any test on polyp-free frames; calibration; subgroup results; encoders larger than ViT-S.
- **Neighbouring work:**
  - PolypDINO (Ali et al., LNCS 2025, [doi:10.1007/978-3-031-98694-9_14](https://doi.org/10.1007/978-3-031-98694-9_14)): adapts DINOv2 for domain-generalised polyp segmentation. Abstract and datasets not retrieved (verify).
  - Polyp-DiFoM (Agnihotri et al., WACV 2026, arXiv 2512.09307): distils SAM and DINOv2 into small U-Nets, tested on Kvasir-SEG, CVC-ClinicDB, CVC-ColonDB, ETIS and CVC-300.
  - Taha and Lukmanov (Doklady Mathematics 2025, [doi:10.1134/s1064562425700541](https://doi.org/10.1134/s1064562425700541)): a layer-wise analysis of frozen encoders. They report that an intermediate layer works best, and a PolypGen Dice of 0.972 (the split is probably not centre-wise; verify).
  - SegDINO (arXiv 2509.00833): frozen DINOv3 with a light decoder, tested on Kvasir-SEG among other datasets.
  - Also: SD-SAM (SAM + DINOv3, LNCS 2026), DINOv2-UNet (IJCNN 2026), HAT-SAM3 (Visual Computer 2026), multi-encoder dataset pruning with DINOv2 (Bioengineering 2026), Mask-TS Net calibration (LNCS 2024).
- **New open data since the source:** FAR-POLYP-SEG (Tehran, Iran; JIIM, September 2026; Zenodo, CC BY 4.0). It has 432 masked polyp frames plus **7,749 normal-mucosa frames** with bowel-preparation scores. Its authors found that conventional models flag polyps on 25–60% of normal frames. No foundation-model encoder has been tested on it yet. PolypDB (2024) adds a Vietnamese centre and four image-enhanced modalities.

**Searches run on 2026-11-06.** OpenAlex returned HTTP 429 (daily budget used), so the skill's fallback order was used: Crossref, then Europe PMC, then web search.
- Crossref and Europe PMC (2023 onwards): "frozen DINOv2 polyp segmentation generalization"; "foundation model polyp segmentation PolypGen cross-center"; "(polyp segmentation) AND (DINOv2 OR DINOv3)"; "polyp segmentation calibration uncertainty out-of-distribution centre"; "polyp segmentation false positive normal mucosa frames foundation model"; "PolypDB polyp segmentation external validation"; "endoscopy foundation model polyp segmentation frozen benchmark EndoDINO GastroNet"; "FAR-POLYP-SEG".
- Crossref: "Representation Matters Rethinking Domain Generalization Polyp Segmentation", to find a published MLMI version (none found).
- Web search: the MLMI title; "DINOv3 frozen encoder polyp segmentation cross-dataset Kvasir CVC ETIS 2026"; PolypDINO; Polyp-DiFoM; the Taha and Lukmanov paper; PolypDB licence.
- **Not checked:** Semantic Scholar and the arXiv search API. arXiv was already rate-limited (HTTP 429) on the metadata call, and the four-call budget went on reading the source and PolypDB.

### Gap 1: No test outside PolypGen, and none in lower- or middle-income countries

- **Evidence:** v1 used PolypGen only (Datasets section), and the corrected README results are PolypGen-only too. PolypGen's one LMIC centre (C6, Alexandria, Egypt) has just 88 single frames.
- **Novelty check:** Crossref, Europe PMC and web searches (above) found frozen-DINO polyp models tested on Kvasir-SEG, CVC-ClinicDB, ETIS and ColonDB (Polyp-DiFoM, SegDINO). None was trained on PolypGen centres and tested on PolypDB-Vietnam or FAR-POLYP-SEG. No paper citing FAR-POLYP-SEG was found (two months old). **Partly filled** for the classic Western benchmarks; **open** for the Iran and Vietnam sets.
- **Open data:** `polypgen` (development), `kvasir-seg`, `cvc-clinicdb`, `polypdb` (Sweden and Vietnam folders), `far-polyp-seg`.
- **Design sketch:**
  - *Hypothesis:* frozen self-supervised features transfer better than fine-tuned ones to unseen countries and processors (Fujinon in Vietnam, Olympus CV-190 in Iran), even though fine-tuning wins inside PolypGen.
  - *Data:* train on all six PolypGen centres; test zero-shot on four external sets.
  - *Methods:* DINOv2, DINOv2-R and DINOv3 (ViT-S and ViT-B), frozen vs fine-tuned, plus nnU-Net and U-Net baselines; 3 seeds.
  - *Metrics:* per-image Dice and IoU, with bootstrap CIs and a paired comparison per external set.
  - *Reporting guideline:* CLAIM 2024.
- **Rating:** feasibility 4, novelty 3, RunPod (~15–25 GPU-h), 3 weeks.

### Gap 2: Nobody tests these models on polyp-free frames

- **Evidence:** v1 and the README report Dice, recall and pixel accuracy on polyp-positive frames only. A segmenter that paints polyps on normal mucosa would score well on these metrics. FAR-POLYP-SEG's authors showed that false-positive rates on normal frames reverse the Dice ranking of six conventional models (JIIM 2026, abstract).
- **Novelty check:** the "false positive normal mucosa frames foundation model" searches (Crossref, Europe PMC) found false-positive suppression methods and detection work. None measured frozen or fine-tuned foundation-model segmenters on curated normal frames. Open, as of 2026-11-06.
- **Open data:** `far-polyp-seg` (7,749 normal frames) and `polypgen` (4,275 negative sequence frames).
- **Design sketch:**
  - *Hypothesis:* fine-tuned encoders gain Dice but lose specificity on normal mucosa more than frozen encoders do.
  - *Metrics:* gated false-positive rate (any predicted polyp area above a size threshold), false-positive area per frame, and a frame-level ROC from the maximum predicted probability, reported against Dice for each model.
- **Rating:** feasibility 5, novelty 4, laptop once the models exist, 1 week.

### Gap 3: No calibration or failure flagging under centre shift

- **Evidence:** neither version reports calibration or any uncertainty output. Stable Dice can hide overconfident errors, as the PLISM study in this catalogue showed for pathology.
- **Novelty check:** Mask-TS Net (LNCS 2024) and several uncertainty-aware polyp networks exist (Crossref "polyp segmentation calibration uncertainty out-of-distribution"). None compares frozen and fine-tuned foundation encoders across external centres. Partly open.
- **Open data:** same as Gap 1.
- **Design sketch:** pixel-level ECE and Brier score on the polyp-boundary band. Image-level failure flag (mean predictive entropy, or a 5-pass TTA disagreement) scored by AUROC for "Dice < 0.5". Temperature scaling fitted on PolypGen validation only, then tested externally.
- **Rating:** feasibility 4, novelty 3, laptop/Colab, 1–2 weeks.

### Gap 4: No subgroup results by size, shape, modality, bowel preparation or chromoendoscopy

- **Evidence:** v1 has no subgroup analysis. PolypGen gives pixel-size categories and a chromoendoscopy flag (in the authors' split files). PolypDB separates WLI, NBI, BLI, LCI and FICE. FAR-POLYP-SEG has a Boston Bowel Preparation Scale (BBPS) score for every patient.
- **Novelty check:** no foundation-model polyp paper found that stratifies by BBPS or by image-enhanced modality on these sets (same searches). Open, but this is an analysis layer, not a stand-alone paper.
- **Design sketch:** Dice and false-positive rate by size tertile (mask area), by modality, by BBPS segment score (FAR) and by chromoendoscopy (PolypGen). Mixed-effects model with patient or sequence as a random effect.
- **Rating:** feasibility 4, novelty 3, laptop, 1 week.

### Gap 5: Only ViT-S was tested; no larger or endoscopy-specific encoders

- **Evidence:** the authors chose ViT-S on purpose (v1 Methods). Taha and Lukmanov found intermediate layers better than the last layer. Endoscopy-pretrained encoders (EndoDINO, arXiv 2501.05488; GastroNet-5M, Endoscopy 2025) exist, but whether their weights are openly downloadable was not checked (verify).
- **Novelty check:** layer choice is covered by Taha and Lukmanov. A size sweep with an endoscopy foundation model on PolypGen centre-wise folds was not found. Low novelty.
- **Design sketch:** ViT-S, B and L for DINOv2/v3; keys from layers {6, 9, last}; one endoscopy foundation model if its licence allows.
- **Rating:** feasibility 3 (DINOv3 gating, more GPU), novelty 2, RunPod 20+ GPU-h, 2 weeks.

### Gap 6: A reproducibility note on the freezing bug

- **Evidence:** the v1 numbers match the corrected fine-tuned row almost exactly (see `replication.md`). This is a clean real-world example of a one-character bug changing a paper's conclusion.
- **Novelty check:** the authors' own README now carries the corrected table, so the numbers are not new. A short "checks every frozen-encoder paper should report" note (trainable-parameter count, weight checksum) has value for teaching but little novelty.
- **Rating:** feasibility 5, novelty 2, laptop, 1 week. Best folded into the main paper's methods and supplement.

**Indian and LMIC angle:** two of the external sets come from LMICs (Vietnam, lower-middle income; Iran, upper-middle income), and PolypGen's Egypt centre can be reported separately. Bowel preparation is often poorer in low-resource settings, and FAR-POLYP-SEG's BBPS scores let us test that directly. **Low-cost or refurbished colonoscopes are not supported:** every open set found used standard Olympus or Fujinon processors, so the paper should not claim anything about low-cost devices.

**Pathologist angle:** none of these datasets has histology, so a pathologist cannot add a histology-linked error taxonomy. Atul's contribution would be a structured visual review of the worst false positives on normal mucosa (folds, bubbles, stool, light reflections, instruments). That is useful, but it is an endoscopic rather than a pathological skill.

## Recommended extension

**Gaps 1 + 2 together, with 3 and 4 as secondary analyses:** "Do frozen DINO encoders trained on PolypGen work in new countries and on polyp-free frames? Zero-shot external testing of frozen versus fine-tuned DINOv2/v3 polyp segmentation on Kvasir-SEG, CVC-ClinicDB, PolypDB (Sweden, Vietnam) and FAR-POLYP-SEG (Iran)."

Why this one:
- The original "correctly frozen" idea has been done by the authors themselves. The open questions now are external validity and specificity.
- FAR-POLYP-SEG (September 2026) is the newest open set, with thousands of normal frames. No foundation-model results on it have been published yet.
- All data are open, under 5 GB, with no credentialing. DINOv3 needs a gated (manual) Hugging Face request; DINOv2 is Apache-2.0.
- About 30–40 GPU-h in total. The frozen arm is cheap with cached features.
- It has a real clinical message: whether foundation-model segmenters over-call polyps on normal mucosa in an unseen hospital.

Expected time: about 6 weeks to an arXiv (eess.IV) or medRxiv preprint. Best-fit journals (zero-APC subscription routes): Journal of Imaging Informatics in Medicine (it published FAR-POLYP-SEG), Computerized Medical Imaging and Graphics, and Digestive Diseases and Sciences. Fit for Atul: moderate. It uses his ML skills and his GI area, but not histopathology.
