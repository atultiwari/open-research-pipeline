---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** Shah et al., IEEE IC-SIT 2026 ([doi:10.1109/IC-SIT69723.2026.11735904](https://doi.org/10.1109/IC-SIT69723.2026.11735904)). YOLOv3–v8 on TXL-PBC; YOLOv8 best (mAP@0.5 0.961). Paywalled; abstract read only.
- **Dataset paper:** Gan et al., Sci Data 2025 ([doi:10.1038/s41597-025-05980-z](https://doi.org/10.1038/s41597-025-05980-z)). Its own baselines already exceed the source (YOLOv5s mAP@0.5 0.980).
- **Same group as the source:** Elastic YOLO (Issac & Rajakumar, PLOS ONE 2026, [doi:10.1371/journal.pone.0347123](https://doi.org/10.1371/journal.pone.0347123)), mAP@0.5 0.947 on a clinician-annotated set.
- **Others on TXL-PBC:** BloodContourNet (2026, YOLO-based), plus several GitHub projects training YOLO11 and YOLO26 on TXL-PBC.
- **A larger open set for classification, not detection:** KU-Optofil PBC (Sci Data 2026, [doi:10.1038/s41597-026-06761-y](https://doi.org/10.1038/s41597-026-06761-y)), 31,489 single-cell images in 13 classes from a Sysmex DI-60.
- **Related study in this repo:** `wbc-crossdataset` (white-cell differential across analysers). This study is about whole-field detection and counting, not WBC classification.

**Searches run on 2026-11-06:**
- Europe PMC citations of the TXL-PBC paper (2 indexed).
- GitHub search "TXL-PBC" (4 repos).
- Crossref and Europe PMC (2024 onwards): "pre-annotation bias semi-automatic labeling object detection benchmark evaluation"; "blood cell detection cross-dataset generalization YOLO domain shift"; "platelet count smear image deep learning agreement analyzer".
- OpenAlex not used (daily budget used up).

**Verdict:** another YOLO leaderboard on TXL-PBC would add nothing. Two questions are open and testable:
- Are rankings on this dataset an artefact of how it was labelled?
- Do any of these detectors work on a source they have not seen?

### Gap 1: The labels were drawn by YOLOv8n

- **Evidence:** TXL-PBC labels were created by a YOLOv8n model trained on 250 hand-labelled images, then reviewed (Gan et al., Methods). The source then finds YOLOv8 best on these labels (abstract).
- **Novelty check:** found no blood-smear study, and no general detection study in the searches above, that tests whether model-assisted pre-annotation biases later detector rankings. A 2026 Neurocomputing paper refines benchmark labels with pseudo-labels ([doi:10.1016/j.neucom.2026.133046](https://doi.org/10.1016/j.neucom.2026.133046)), but it does not test ranking bias.
- **Open data:** `txl-pbc` test split (126 images).
- **Design sketch:**
  - *Hypothesis:* scored against labels drawn by a pathologist from scratch, YOLOv8-family detectors lose part of their lead, and rankings change, especially for platelets and overlapping RBCs.
  - *Re-annotation:* Atul re-annotates all 126 test images in a tool with no pre-labels (e.g. CVAT), following the TXL-PBC protocol for box rules. He double-annotates 20 images two weeks apart for intra-rater agreement.
  - *Detectors:* YOLOv3/5/7/8/11/26, RT-DETR and Faster R-CNN, trained on the original training labels.
  - *Metrics:* mAP@0.5 and mAP@0.5:0.95 against both label sets, Kendall's τ between the two rankings, and per-class differences with bootstrap CIs over images.
  - *Reporting guideline:* CLAIM 2024.
- **Rating:** feasibility 4, novelty 4, Colab, 3 weeks (including ~2–3 days of annotation).

### Gap 2: Random split across four sources

- **Evidence:** images were shuffled and split at random across BCCD, BCDD, PBC and Raabin-WBC (Gan et al., Data Integration).
- **Novelty check:** no leave-one-source-out detection result found on TXL-PBC.
- **Open data:** `txl-pbc` with `metadata_file.xlsx`; external sets `bccd` (the 204 BCCD images TXL-PBC excluded, with original labels corrected by Atul for a subset) and `bbbc041` (expert RBC/WBC boxes from malaria smears, a different lab and stain).
- **Design sketch:** train on three sources, test on the fourth, for each source. Train on all of TXL-PBC and test on BBBC041 (RBC and WBC only). Report the drop from the random split, per class.
- **Rating:** feasibility 5, novelty 3, Colab, 2 weeks.

### Gap 3: mAP is not a clinical endpoint

- **Evidence:** the source reports mAP, precision, recall and F1 only (abstract). Haematologists care about counts per field: platelet estimates, WBC per field, RBC crowding.
- **Design sketch:** per-image count error (MAE, Bland–Altman) for RBC, WBC and platelets against Atul's counts. A platelet-estimate rule (platelets per oil-immersion field × factor) as a clinically framed outcome. Error analysis of clumps, giant platelets and overlapping cells.
- **Rating:** feasibility 5, novelty 3, laptop, inside Gap 1.

### Gap 4: Low-resource deployment claim untested

- **Evidence:** the abstract recommends YOLOv5 for "limited resources", but speed was measured on unspecified hardware (verify).
- **Design sketch:** CPU and phone (ONNX, TFLite) latency for nano and small variants on a mid-range Android phone and a low-end laptop; accuracy after INT8 quantisation.
- **Rating:** feasibility 5, novelty 2, laptop, 1 week.

## Recommended extension

**Gaps 1 + 2 + 3 together:** pathologist re-annotation of the TXL-PBC test set to test whether model-assisted labels bias detector rankings, plus leave-one-source-out and BBBC041 external tests, reported as count agreement as well as mAP.

Why:
- It turns a crowded topic into a useful methods paper: a warning about benchmarks labelled with model help, which applies well beyond blood smears.
- Atul's annotation is the scarce input.
- Everything is open, small and cheap.
- The count-agreement framing speaks to haematologists, not just computer-vision readers.

Honest caveat: novelty is moderate (3/5). If the rankings do not change, the paper becomes a solid negative result plus a cross-source benchmark. About 5 weeks; JIIM, Indian J Pathol Microbiol or CMIG.
