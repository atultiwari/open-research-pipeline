---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** Vaidya et al., *Nat Med* 2024 ([doi:10.1038/s41591-024-02885-z](https://doi.org/10.1038/s41591-024-02885-z)). Encoders: ResNet50-IN, CTransPath, UNI. The breast and lung external tests used private MGB data. Site-preserving splits and stain normalisation were tested only as preprocessing choices (Extended Data Figs 1–4).
- **FAIR-Path** (Lin et al., *Cell Rep Med* 2025, [doi:10.1016/j.xcrm.2025.102527](https://doi.org/10.1016/j.xcrm.2025.102527)):
  - pan-cancer fairness audit on TCGA, with 15 external cohorts including CPTAC;
  - found an age bias for LUAD vs LUSC in CPTAC, and says the race biases were not fully explained by procurement site, scanner or stage;
  - its foundation-model analysis (CHIEF, UNI, GigaPath) was on TCGA only, and its CPTAC slides were frozen sections.
- **García-de-la-Puente et al., ICIP 2026** ([doi:10.1109/ICIP61757.2026.11630439](https://doi.org/10.1109/ICIP61757.2026.11630439)): three pathology foundation models, four cancer tasks, balanced test sets, controlled training composition. Age was the most sensitive attribute, and a validation-tuned threshold reduced the gaps. The abstract mentions no external cohort or site analysis. The full text was not read (IEEE paywall).
- **Site and centre confounding without race:**
  - Zhang, *Hospital-Specific Bias in Patch-Based Pathology Models* ([arXiv 2508.14779](https://arxiv.org/abs/2508.14779); ISBI 2026): TCGA patch-level hospital bias, with an adversarial adaptor;
  - de Jong et al. ([arXiv 2501.18055](https://arxiv.org/abs/2501.18055)) and PathoROB (*Nat Commun* 2026): every foundation model they tested encodes the medical centre;
  - Kheiri et al. (*Sci Rep* 2025; *PLOS Digit Health* 2026): site shortcuts in TCGA models.
  - None of these links site to race-stratified performance.
- **Other:**
  - Rakaee et al., *JAMA Oncol* 2026: ancestry and EGFR prediction in private cohorts;
  - MeCaMIL (*IEEE TMI* 2026): a fairness-aware MIL method on TCGA-Lung;
  - Watson et al., *Cancers* 2026: equivalence testing and power for fairness claims.

**Searches run on 2026-11-06:**
- OpenAlex works citing the source (W4394976513): 123 results. Filtered titles for fair/bias/race/site/demograph/disparit/confound: 25 relevant, read the abstracts of the 8 closest.
- OpenAlex keyword searches (from 2024-01-01):
  - "pathology foundation model race fairness TCGA CPTAC";
  - "demographic disparity whole slide image foundation model external validation";
  - "race site confounding TCGA histopathology";
  - "tissue source site race TCGA deep learning bias";
  - "lung adenocarcinoma squamous subtyping Asian patients performance gap pathology AI";
  - "UNI2 fairness subgroup whole slide";
  - "equivalence test fairness pathology AI".
- arXiv (3 calls): `id_list=2508.14779`; `abs:fairness AND abs:pathology AND abs:foundation` (14 hits, only 2502.16889 relevant: a general ethics-risk audit of pathology foundation models); `abs:race AND abs:"whole slide"` (3 hits: MeCaMIL and two unrelated).
- Europe PMC full text of FAIR-Path (PMC12765949).
- Semantic Scholar: not used (to stay under rate limits).

**Result:** "foundation models still show demographic gaps on TCGA" is no longer new (FAIR-Path, ICIP 2026). Two things remain open:
- a fully open external test of current foundation models with race stratification, which nobody has run on CPTAC lung slides matched to the TCGA diagnostic-slide preparation;
- an explicit split of the apparent race gap into a site part and a residual part.

### Gap 1: Race gaps confounded with tissue source site

- **Evidence:**
  - The source used site-preserving splits only as a preprocessing option and did not estimate how much of the race gap site explains (Extended Data Figs 1–2).
  - In TCGA lung, three of 43 sites hold 46% of Black patients (GDC API, 2026-11-06).
  - Foundation-model embeddings encode the centre strongly (arXiv 2501.18055, 2508.14779).
  - FAIR-Path asserts that site does not fully explain the gaps, but only for its own (non-foundation) models and without a formal decomposition.
- **Novelty check:** none of the searches above found a study that models race-stratified error with site as a random effect, or compares random vs site-held-out splits for foundation-model MIL, together with external testing.
- **Open data:** `uni2h-features-tcga`, `conch-v15-features-tcga`, `virchow2-features-tcga`, `gigapath-features-tcga`, `tcga`, `cptac`.
- **Design sketch:**
  - *Hypothesis:* part of the TCGA white–Black gap in LUAD/LUSC subtyping is a site effect. It shrinks under site-held-out splits and after adjusting for site, and stronger encoders leave a smaller residual race effect.
  - *Methods:* ABMIL on 4 precomputed encoders; Monte Carlo vs site-preserving splits; a mixed-effects logistic model of per-slide correctness (`race + age + sex + stage + (1|site)`); a site-classification probe on slide embeddings as a measure of how much site each encoder carries.
  - *Metrics:* AUC and TPR gap by race with patient-level bootstrap CIs; the race odds ratio before and after site adjustment; site-probe balanced accuracy.
  - *Reporting guideline:* TRIPOD+AI (fairness items) with CLAIM 2024.
- **Rating:** feasibility 4, novelty 3 (FAIR-Path touches it qualitatively), RunPod, 3 weeks.

### Gap 2: Open external validation, and an adequately sized external white–Asian test

- **Evidence:**
  - The source's breast and lung external tests are private (Data availability statement).
  - TCGA lung has 17 Asian patients, whereas CPTAC-3 lung has 131, mostly LUAD (GDC API).
  - FAIR-Path's CPTAC slides were frozen sections, and its foundation-model analysis was internal only.
- **Novelty check:** no paper found that tests foundation-model MIL trained on TCGA against CPTAC lung slides (the Patho-Bench selection; preparation to be confirmed) with race-stratified metrics (searches above). FAIR-Path's limitations section says its Asian-subgroup analyses lacked power.
- **Open data:** as Gap 1. Use CPTAC-BRCA only as a secondary task after counting its ILC cases.
- **Design sketch:**
  - *Hypothesis:* models trained on almost no Asian patients still subtype Asian patients' tumours as well as white patients' tumours. Test this as an **equivalence** claim (TOST, margin pre-registered, e.g. ΔAUC ±0.03), not as "no significant difference".
  - *Methods:* train on TCGA, freeze, test on CPTAC; stratify by LUAD/LUSC, because the case mix differs by race; report per-group calibration (ECE, calibration slope).
  - *Reporting guideline:* TRIPOD+AI.
- **Rating:** feasibility 4, novelty 4, RunPod, 2 weeks on top of Gap 1.

### Gap 3: Power and equivalence instead of point gaps

- **Evidence:** the source reports p-values from permutation tests across folds, with no a priori margins. CPTAC lung has 6 Black patients, so white–Black external claims are impossible. Watson et al. (*Cancers* 2026) show that many fairness assessments are underpowered.
- **Novelty check:** no pathology WSI fairness study using equivalence margins was found (OpenAlex search "equivalence test fairness pathology AI").
- **Design sketch:** report the minimal detectable AUC and TPR difference for every subgroup comparison, with TOST equivalence results. State plainly which comparisons the open data cannot answer.
- **Rating:** feasibility 5, novelty 3, laptop, adds about 0.5 week.

### Gap 4: Pathologist error taxonomy by subgroup

- **Evidence:** the source and the follow-up papers report aggregate metrics only. None says *which* tumours are misclassified for each group.
- **Novelty check:** no subgroup-wise morphological error review was found in any of the papers above.
- **Design sketch:**
  - Atul reviews the CPTAC and TCGA slides that are misclassified (or have high uncertainty) for each race group, about 100–150 slides, at 5–20× on the TCIA/GDC viewers.
  - He codes the likely cause: poorly differentiated or solid pattern, mucinous or other variants, adenosquamous features, sparse tumour or crush artefact, frozen-section artefact, or a reference label that looks wrong.
  - Test whether the error mix differs by group. A difference would suggest case mix rather than "bias".
- **Rating:** feasibility 5, novelty 4, about 1 week of expert time.

### Gap 5: The *IDH1* arm with newer encoders (replication anchor)

- **Evidence:** the only fully open arm of the source study (EBRAINS → TCGA-GBMLGG) had the largest reported gap (16.0% AUC with common pipelines).
- **Novelty check:** no reproduction with UNI2-h or other 2025–26 encoders was found.
- **Design sketch:** re-run the repo's 20 folds with UNI features as a replication, then with UNI2-h (self-extracted on EBRAINS; the TCGA side can use the precomputed features).
- **Rating:** feasibility 3 (EBRAINS DUA and ~2,000 slides to tile), novelty 2 alone, RunPod, 2–3 weeks.
- **Use:** a replication anchor if time allows, not the headline.

### Gap 6: Low-compute and LMIC framing

- **Evidence:** all encoders tested are ViT-L/H scale. In Indian practice, cases are mostly read on low-cost scanners.
- **Design sketch:** add a distilled encoder (e.g. the OMNI models released by the same feature uploader; their Hugging Face licence tag is CC BY-NC 4.0, so check their fit for MIL first) and report gap versus compute. South Asian patients are absent from both TCGA and CPTAC, so state this as a limitation, not a result.
- **Rating:** feasibility 3, novelty 3. Secondary.

## Recommended extension

**Gaps 1 + 2, with Gaps 3 and 4 as built-in analyses:** "Is the race gap in pathology AI really a site gap? A fully open TCGA-to-CPTAC audit of four foundation-model MIL classifiers for lung cancer subtyping, with an external white-versus-Asian equivalence test and a pathologist error review."

Why this one:
- **Feasible:** all four encoders' features are precomputed for exactly the TCGA and CPTAC lung slides, labels and demographics come free from the GDC API, and there is no slide download. Compute is about 15–20 GPU-h.
- **New where it counts:** the site decomposition and the external Asian arm are not covered by FAIR-Path or ICIP 2026. The equivalence framing makes small-subgroup results honest.
- **Uses Atul's expertise:** histological subtyping, the error taxonomy, and judging whether "errors" are label problems.
- **Risks:** novelty relies on the ICIP 2026 full text not already doing this (unread). The CPTAC preparation (frozen vs FFPE) must be confirmed early, because it decides whether the external arm is clean.

Expected time: about 6 weeks to a medRxiv preprint. Best-fit journals: Journal of Imaging Informatics in Medicine, Laboratory Investigation, Computerized Medical Imaging and Graphics.
