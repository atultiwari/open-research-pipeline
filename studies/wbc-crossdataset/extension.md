---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** WBCBench 2026 (Tian et al., ISBI 2026). One Thai laboratory, CellaVision DI-60, 13 classes, synthetic degradation, in-distribution macro-F1 only. Top teams built on DinoBloom; none was tested on another site.
- **Sharma & Tapadiya, "Can You Trust Frozen Hematology Foundation Models under Acquisition Shift?"** ([arXiv 2608.25148](https://arxiv.org/abs/2608.25148), August 2026; HemaRAI workshop at MICCAI 2026). This is the closest prior work. It covers most of the **register's original proposal**:
  - 15 frozen encoders (DinoBloom, RedDino, Phikon, Lunit-DINO, DINOv2, CLIP and others) with linear and 1-NN probes;
  - trained on PBC/Acevedo (through BloodMNIST at 224 px) and tested zero-shot on MLL23, Matek and Raabin;
  - calibration (ECE, NLL, Brier, temperature transfer), a pretraining-exposure audit and label-shift test-time adaptation.
  - Its stated limitations are exactly where this study can add something: only the **five-class intersection**; **no leakage-free DinoBloom target**; image-level splits; one stain family per dataset. It did not use WBCBench or CytologIA, and its only pathology encoders are first-generation (Phikon, Lunit-DINO).
- **Zamora et al.** (SPIE 2026, [doi:10.1117/12.3112843](https://doi.org/10.1117/12.3112843)): held-out-dataset leukaemia classification (leukaemia vs not, then ALL vs AML) with DinoBloom, BiomedCLIP and CLIP. These are leukaemia labels, not the white-cell differential, and no histopathology encoders.
- **Gitau et al.** (ISBI 2026, [arXiv 2603.20383](https://arxiv.org/abs/2603.20383)): fine-tuned DinoBloom on WBCBench, in-distribution only. Their expert review found that cells every model got wrong were enriched for label errors.
- **Older cross-domain work** uses CNNs, not foundation models, mostly on five classes:
  - few-shot domain adaptation across 8 datasets (Chossegros et al., J Pathol Inform 2024, [doi:10.1016/j.jpi.2024.100405](https://doi.org/10.1016/j.jpi.2024.100405));
  - test-time augmentation (Putzu et al., J Imaging 2025, [doi:10.3390/jimaging11090295](https://doi.org/10.3390/jimaging11090295));
  - PBC-to-external calibration with CNNs and ViTs (Wable 2026, [doi:10.17762/jidmis.v3.3213](https://doi.org/10.17762/jidmis.v3.3213)).
- **CytologIA** (Sourdeau et al., npj Precis Oncol 2026, [doi:10.1038/s41698-026-01484-0](https://doi.org/10.1038/s41698-026-01484-0)): a 23-class multicentre challenge whose data are now open on data.gouv.fr. OpenAlex lists **no works citing it**, so it has not yet been used as a foundation-model external test set.

**Searches run on 2026-11-06:**

| # | Search | Result |
| --- | --- | --- |
| 1 | OpenAlex works citing the ISBI paper (`cites:W7161752142`) | 7: five challenge entries, a MobileNet/DenseNet/DINOv2 fusion on 5 classes, a product-of-experts ensemble. None external. |
| 2 | OpenAlex search `WBCBench` | 11, including Sharma (2608.25148) and Zamora (SPIE 2026) |
| 3 | OpenAlex search `DinoBloom` (from 2024) | 65; relevant: Sharma, Zamora, Gitau |
| 4 | OpenAlex: "white blood cell foundation model cross-dataset generalization" (from 2024) | No study with WBCBench as source or CytologIA as target |
| 5 | OpenAlex: "histopathology foundation model UNI Virchow blood smear white blood cell" (from 2024-06) | 4 hits, none relevant: no UNI2-h, Virchow2 or H-optimus on blood cells |
| 6 | OpenAlex: "automated differential count deep learning case-level agreement blast flag peripheral blood" (from 2023) | Commercial-analyser validations only (e.g. a DI-60 deep-learning system in 3 Japanese hospitals, IJLH 2026); no open-model case-level study |
| 7 | OpenAlex: "white blood cell classification corruption robustness blur noise benchmark", "… calibration uncertainty out-of-distribution", "smartphone microscope … CellaVision transfer", "leukocyte classification domain shift external validation" | CNN-era and single-dataset calibration papers; nothing pairing synthetic and real shift for foundation models |
| 8 | OpenAlex works citing Sharma (`cites:W7204477680`) and CytologIA (`cites:W7161293737`) | 0 each |
| 9 | arXiv: `abs:"white blood cell" AND abs:"foundation model"` | 6 results; only Sharma is on point |
| 10 | Semantic Scholar citations of arXiv:2604.10797 | Rate-limited (HTTP 429), not checked |

**Result:** a five-class "train on one dataset, test on others" benchmark with calibration is **no longer new**: Sharma did it. What is still open is everything a haematologist actually needs from a differential:
- the immature granulocytes and blasts;
- a training set the haematology foundation model has never seen;
- the current histopathology encoders;
- whole-slide (case-level) consequences.

### Gap 1: No leakage-free, clinically complete cross-site test

- **Evidence.**
  - WBCBench is single-site and reports only in-distribution scores (paper Sections 3.1 and 5; Table 3).
  - Sharma lists its limitations: the five-class intersection, no leakage-free DinoBloom target, and a source (Acevedo) that is DinoBloom's only held-out set (Sections 4 and 6).
  - WBCBench (released 2026) and CytologIA (June 2025) both post-date DinoBloom (2024), and DinoBloom held PBC out of pretraining (DinoBloom paper, Section 3). So **WBCBench → PBC and WBCBench → CytologIA are leakage-free for every haematology encoder**, with Raabin as the in-pretraining control.
- **Novelty check:** searches 1–4, 8 and 9 found no work with WBCBench as source, or CytologIA as target, for any foundation model.
- **Open data:** `wbcbench-2026` (source), `pbc-barcelona`, `cytologia`, `raabin-wbc` (targets).
- **Design sketch.**
  - *Hypothesis:* encoder rankings on clean WBCBench do not predict rankings on the external sets. The loss is largest for the classes that matter clinically: blasts, the immature granulocytes (promyelocyte, myelocyte, metamyelocyte) and bands.
  - *Label harmonisation (Atul):* map every dataset to a shared maturation-aware set: SNE, BNE, LY, VLY/reactive, MO, EO, BA, IG (PMY/MY/MMY, and individually where available), BL. Document each mapping decision. CytologIA's LAM3 (APL promyelocyte) and its lymphoma cell classes go to an "out-of-taxonomy" bucket, reported separately. Then evaluate on three nested levels:
    - L1: the five mature classes (comparable with Sharma);
    - L2: L1 plus IG and BL;
    - L3: the full shared set per target.
  - *Methods:* frozen features plus logistic-regression and 1-NN probes. Train on WBCBench pristine `phase1_train` + `phase2_train`, tune on `phase2_eval` (case-grouped), and test on the WBCBench test set and zero-shot on each target.
  - *Metrics:* macro-F1, balanced accuracy and per-class recall, with 95% CIs (bootstrap by case on WBCBench, by image elsewhere); Spearman ρ between in-domain and target rankings; the relative drop.
  - *Reporting guideline:* CLAIM 2024.
- **Rating:** feasibility 5, novelty 4, Colab, 3–4 weeks.

### Gap 2: Current histopathology foundation models are untested on blood cells

- **Evidence.**
  - The register asked "haematology vs histopathology vs general" encoders.
  - Sharma's pathology arm is Phikon (v1) and Lunit-DINO only; it found the two diverged sharply (Table 1).
  - Gitau's "pathology foundation model" was DinoBloom.
  - No study tests UNI2-h, Virchow2, H-optimus-0, H0-mini or Phikon-v2 on peripheral-blood cells.
- **Novelty check:** search 5 (4 hits, none relevant) and search 9.
- **Open data:** as Gap 1.
- **Design sketch.**
  - *Hypothesis:* tissue-trained encoders give competitive results on mature cells but lose to haematology encoders on blasts and immature granulocytes. General encoders (DINOv2/v3) sit in between.
  - *Encoders* (three families, matched where possible on ViT-B):
    - haematology: DinoBloom-S/B/L, RedDino-base;
    - histopathology: UNI2-h, Virchow2, H-optimus-0, H0-mini, Phikon-v2;
    - general: DINOv2-B, DINOv3-B (if access is granted), ImageNet ResNet-50.
  - *Metrics:* as Gap 1, plus compute per image (GFLOPs, CPU time).
  - *Reporting guideline:* CLAIM 2024.
- **Rating:** feasibility 5 (gated encoders are auto-approved apart from H0-mini and DINOv3), novelty 4, Colab/RunPod, adds about 1 week to Gap 1.

### Gap 3: No case-level (whole-differential) or calibration endpoints

- **Evidence.**
  - WBCBench ranks single cells only (Section 4B).
  - Yet the card shows each case is the analyser's verified differential for one film (median 112 cells), and blasts appear in 215 of 493 cases.
  - Clinicians act on the differential and on flags ("blasts present", "left shift"), not on cell-level F1.
  - Sharma reports calibration for five classes on image-level splits, with no case structure.
- **Novelty check:** search 6 found only validations of commercial analysers (closed models, closed data). Search 7 found no foundation-model calibration on a 13-class case-grouped set.
- **Open data:** `wbcbench-2026` only, because no external set carries case identifiers.
- **Design sketch.**
  - *Endpoints per test case:*
    - absolute error of each cell-type percentage against the expert differential (Bland–Altman, as in analyser validation);
    - blast-positive case detection (any blast, and blasts ≥ 1–2% as sensitivity analyses): sensitivity at fixed specificity, AUROC;
    - immature-granulocyte flag (left shift);
    - cell-level calibration (ECE, Brier, reliability diagrams) and case-level flag calibration.
  - *Built-in device shift:* train on cases from one DI-60 analyser and test on the other. Image size identifies the analyser, so resize to a common size first.
  - *Reporting guideline:* CLAIM 2024 plus TRIPOD+AI items for calibration.
- **Rating:** feasibility 5, novelty 4, laptop once features exist, 1–2 weeks.

### Gap 4: Does synthetic degradation predict real shift?

- **Evidence.**
  - WBCBench's premise is that synthetic blur, noise and colour changes stand in for scanner and setting shift (Section 3.3). The paper never tests this against real external data.
  - Sharma found that synthetic *stain* corruptions did not reproduce DinoBloom's real failure (Section 5, "Mechanism").
  - The WBCBench card releases paired pristine and degraded copies with per-image settings, so robustness can be measured as a dose–response.
- **Novelty check:** search 7 found nothing pairing synthetic and real shift for blood-cell foundation models. Sharma's single mechanism probe is a partial overlap.
- **Open data:** `wbcbench-2026` (paired copies), plus the targets from Gap 1.
- **Design sketch:**
  - per encoder, the macro-F1 drop and prediction flips from pristine to degraded, by severity and by operation (degradation curves);
  - then the correlation between each encoder's synthetic-robustness score and its real cross-site drop (Spearman, across the 10–12 encoders).
- **Rating:** feasibility 5, novelty 3, laptop, 1 week.

### Gap 5: Maturation-aware error taxonomy

- **Evidence.**
  - The hardest classes lie on the granulocyte maturation continuum (BNE, PMY, MMY; paper Table 4).
  - Gitau showed that the shared failures are enriched for label noise.
  - Flat macro-F1 treats a band called segmented the same as a blast called a lymphocyte, although only the second is clinically dangerous.
- **Novelty check:** none of the papers above uses an ordinal or severity-weighted error metric for white-cell foundation models across sites.
- **Design sketch:**
  - a cost matrix agreed by Atul (adjacent maturation stage = minor; blast missed = critical) and a severity-weighted error rate;
  - Atul reviews the 200 cross-site errors with the highest confidence and codes the causes: stain, focus, cell overlap, true morphological ambiguity, probable label error, taxonomy mismatch.
- **Rating:** feasibility 5, novelty 3, about 1 week of expert time.

### Gap 6: Low-cost and smartphone relevance for India

- **Evidence.**
  - WBCBench is DI-60 data, an expensive analyser; the paper itself notes such systems are hard to deploy in low-resource settings (Section 1).
  - Raabin-WBC was captured with ordinary smartphones on microscopes, and its Test-B uses a different phone and microscope.
- **Novelty check:** Sharma includes Raabin, but only five classes and no small-encoder analysis.
- **Design sketch:**
  - report DI-60 → smartphone transfer (Raabin Test-A/Test-B) separately;
  - add small encoders (DinoBloom-S 22M, H0-mini, RedDino-small) with CPU latency, framed for district laboratories and phone-on-microscope practice.
- **Rating:** feasibility 5, novelty 3, inside Gap 2's budget.

## Recommended extension

**Gaps 1 + 2 + 3 as the core, with 4–6 as secondary analyses.** Working title: "Haematology vs histopathology vs general foundation models for the white-cell differential: a leakage-free cross-analyser benchmark from WBCBench 2026 to PBC, CytologIA and Raabin-WBC, with calibration and case-level blast flags."

Why this one:
- **New against Sharma (2026):**
  - a source no haematology encoder has seen;
  - blast and immature-granulocyte classes;
  - CytologIA's 19 laboratories as an unused multicentre target;
  - the current histopathology encoders;
  - case-level clinical endpoints.
  It still reports Sharma's five-class level, so the two papers can be compared directly.
- **Feasibility:** all data are open or auto-approved, and the whole study needs about 8–12 GPU-h.
- **Fit for a pathologist:** label harmonisation across four taxonomies, the cost matrix and the error review need a haematopathologist. This is Atul's edge over ML-only groups.
- **Time:** about 6 weeks to an arXiv (cs.CV / eess.IV) or medRxiv preprint.
- **Journals:** Journal of Imaging Informatics in Medicine, Computerized Medical Imaging and Graphics, Medical & Biological Engineering & Computing. All are subscription routes with no APC.

**Risks to manage:**
- Sharma's overlap: cite it prominently and position this study as the clinically complete, leakage-free follow-up.
- Raabin's licence is unstated: use it only for aggregate metrics, and email the authors.
- CytologIA has no centre IDs, and its dataset DOI did not resolve.
- WBCBench is non-commercial, with person overlap between splits and changed test labels: report both label sets.
