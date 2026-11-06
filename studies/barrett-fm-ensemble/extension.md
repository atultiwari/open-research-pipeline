---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** Kazemi et al., npj Digit Med 2026 ([doi:10.1038/s41746-026-03329-3](https://doi.org/10.1038/s41746-026-03329-3)). Private PAXgene cohort, one scanner, 10-fold CV, no external test. The authors call for routine-FFPE, multi-scanner, dysplasia-enriched external validation and for triage studies (Discussion).
- **Dysplastic Barrett's deep learning with multisite external validation** already exists on private data: Codipilly et al., Am J Gastroenterol 2025 ([doi:10.14309/ajg.0000000000003495](https://doi.org/10.14309/ajg.0000000000003495)).
- **Ensembling pathology foundation models** on public cohorts is published: Luo et al., Cancer Cell 2026 ([doi:10.1016/j.ccell.2026.08.008](https://doi.org/10.1016/j.ccell.2026.08.008)).

**Searches run on 2026-11-06:**
- Zenodo, "Barrett esophagus histology": no whole-slide image datasets.
- Hugging Face, "barrett" and "esophag": nothing relevant.
- Europe PMC and Crossref (2020 or 2023 onwards): "Barrett esophagus whole slide images public dataset deep learning dysplasia"; "Barrett oesophagus histopathology dataset publicly available"; "Barrett esophagus dysplasia deep learning whole slide external validation"; "esophageal adenocarcinoma whole slide foundation model TCGA-ESCA"; "foundation model ensemble selection bias nested cross-validation computational pathology".
- GTEx API: notes for 622 oesophagus mucosa and 401 GE-junction samples.
- OpenAlex not used (daily budget used up earlier today).

**Bottom line:** the source's main contribution (full-spectrum Barrett's subtyping, dysplasia) cannot be studied on open data today. What remains testable is narrow.

### Gap 1: Ensemble members were chosen using the reported folds

- **Evidence:** the Methods (Ensembling) average the top five single-scale models "identified by Cohen's kappa" against the reference, computed fold-wise on the same 10 Monte Carlo splits (80/10/10) that report the ensemble. They then test the ensemble's improvement with one-sided Wilcoxon tests on those same runs. Training length was also swept (1–50 epochs) "to determine the upper bound of performance". No nested or held-out selection is described.
- **Novelty check:** found no pathology study measuring how much same-fold model selection inflates FM ensemble gains (searches above).
- **Open data:** `tcga` (TCGA-ESCA), `gtex-histology`.
- **Design sketch:** rebuild the selection procedure on adenocarcinoma vs squamous (TCGA-ESCA) and on normal vs adenocarcinoma; compare same-fold vs nested selection over many encoder pools; repeat on one larger open task already in this repo (e.g. `panda` or `camelyon16`) to show it generalises. Metric: the optimism gap in AUROC and κ, with patient-level bootstrap. CLAIM 2024.
- **Rating:** feasibility 4, novelty 3, RunPod, 4 weeks.

### Gap 2: Normal-vs-cancer on open data is confounded by source

- **Evidence:** any open "normal" oesophagus comes from GTEx (postmortem) and any cancer from TCGA (surgical), unlike the source's single-pipeline cohort.
- **Design sketch:** train a classifier on the source of the slides alone (GTEx vs TCGA) using non-tumour regions; report how much of normal-vs-cancer performance it explains. Mostly a caution for the surrogate, not a paper on its own.
- **Rating:** feasibility 5, novelty 1, laptop, 1 week.

### Gap 3: Dysplasia (the clinically important class) has no open data

- **Evidence:** dysplasia was 4% of slides and stayed poorly detected (Abstract; class-wise analysis). No open cohort found.
- **Open data:** none. A future collaboration or a new public release (e.g. if the BEACON annotations in Zenodo 17583572 come with slides) would be needed.
- **Rating:** feasibility 1 on open data.

### Gap 4: Pathologist review of attention on GE-junction mucosa

- **Evidence:** the authors report attention drifting to necrosis, inflammation, fibrin and stroma, with only moderate reviewer agreement on heatmaps (ICC 0.651).
- **Design sketch:** Atul codes attention failures on TCGA-ESCA adenocarcinoma and GTEx GE-junction slides (cardiac/oxyntic mucosa, squamous mucosa, reflux change) for the ExCo models. Small, descriptive.
- **Rating:** feasibility 4, novelty 2, laptop, 2 weeks.

## Recommended extension

**Recommendation: park this study.** The surrogate cannot touch what makes the source useful (Barrett's subtyping and dysplasia), FM ensembling on TCGA is already published, and the open normal-vs-cancer task is confounded by source. If Atul still wants something from it, the only defensible paper is **Gap 1**, a short methods note on selection bias in FM ensembling. Its value comes from the method, not from Barrett's, and it should be built on larger open tasks than TCGA-ESCA. Revisit this study if an open Barrett's slide cohort with dysplasia labels is released.
