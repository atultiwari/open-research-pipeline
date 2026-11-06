---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source.** Schönpflug et al., *J Pathol Inform* 2026 ([doi:10.1016/j.jpi.2026.100702](https://doi.org/10.1016/j.jpi.2026.100702)). Stain-simulation protocol, shown only for colorectal MSI on one external cohort (SurGen) with three FMs.
- **PathoROB.** Kömen et al., *Nat Commun* 2026, [doi:10.1038/s41467-026-73923-2](https://doi.org/10.1038/s41467-026-73923-2). Robustness of 20 FMs to non-biological medical-centre features. Its tile-level CAMELYON subset ([HF, CC0](https://huggingface.co/datasets/bifold-pathomics/PathoROB-camelyon), 22,402 patches) already measures how strongly *centre* dominates FM embeddings on CAMELYON. It also shows that Reinhard normalisation and domain-adversarial training improve downstream generalisation. It works at tile and embedding level with real centres, not controlled stain simulation, and has no slide-level MIL calibration.
- **Robustifying FMs.** Filiot et al., arXiv 2607.22861 (July 2026; cites the source): a fine-tuning recipe raises the PathoROB robustness index and releases robustified Phikon-v2 ("Phaet") and Midnight-12k ("Mascaret") on Hugging Face (`wearewaiv`, licence "other", **verify** terms). Whether these models are also more robust at slide level under controlled stain shifts is untested.
- **Stain normalisation and retrieval on PLISM.** Meng et al., bioRxiv October 2026 ([doi:10.64898/2026.10.13.758918](https://doi.org/10.64898/2026.10.13.758918)): normalisation does not consistently help matched-location retrieval, and Macenko can hurt it. Embedding-level, PLISM only.
- **Sarcoma stain/scanner study.** bioRxiv 2025 ([10.1101/2025.08.18.670932](https://www.biorxiv.org/content/10.1101/2025.08.18.670932v2)): FMs were fairly robust to real re-staining and re-scanning in sarcoma subtyping. Different organ and task, no CAMELYON.
- **Slide-level CAMELYON16 → 17 with FMs.**
  - nnMIL (arXiv 2511.14907) and an uncertainty study (arXiv 2606.30020: MC dropout and deep mutual learning, calibration as NLL) use CAMELYON16/17 with FM features.
  - Neither simulates stain shifts or relates calibration to stain properties.
  - Both descriptions come from search-result abstracts only. Semantic Scholar was rate-limited and the arXiv call budget was used up, so their full texts were **not read**. Read them before the protocol.
- **Patch-level Camelyon17-WILDS** is a saturated domain-generalisation benchmark (UNI, Virchow report > 97% accuracy). It is not slide-level and has no stain attribution.

**Relation to other studies in this catalogue.**
- `plism-scanner` asks whether tile embeddings drift across scanners and *smartphones* on PLISM's registered tissue, and whether that breaks calibration of tissue-type probes. There is no clinical slide-level task and no stain simulation.
- This study is different. It takes a real clinical slide-level task (nodal metastasis), applies *controlled stain simulation* (the CTPLab protocol), and tests the protocol itself: does simulated stain robustness predict what happens at real new centres (CAMELYON17)? The two share only the PLISM origin of the stain references (this study uses the released stain vectors, not the PLISM images). A secondary analysis could reuse `plism-scanner`'s embedding-drift metrics as one more predictor.
- `pathfm-adversarial` also uses CAMELYON16, but for adversarial attacks. No overlap in question. Shared feature caches could save compute if both proceed (the licences allow local reuse only).

**Searches run on 2026-11-06.** OpenAlex was out of its daily budget, so the skill's fallback order was used.
- Semantic Scholar citations of arXiv:2603.12886: 4 citing works (arXiv 2607.22861; CSNet, JIIM 2026; an MSI meta-analysis, Cureus 2026; a spatial-transcriptomics uncertainty preprint). None applies the protocol to another task.
- Europe PMC citations of PMID 42701405: 0.
- Crossref:
  - `stain variation robustness pathology foundation models lymph node metastasis CAMELYON` (from 2024)
  - `simulated staining variation multiple instance learning robustness external validation multicentre`
  - `calibration under stain shift whole slide image classifier`
  - Nothing relevant beyond Meng et al. 2026.
- Europe PMC:
  - `(camelyon OR "lymph node metastasis") AND (stain OR staining) AND "foundation model" AND robust*` (2024–2026, 92 hits; only PathoROB is directly relevant)
  - `"multiple instance learning" AND (stain OR staining) AND (calibration OR "expected calibration error") AND (camelyon OR "lymph node")` (86 hits, none relevant)
  - `"PathoROB" OR "robustness index" ...` (9 hits)
- arXiv API:
  - `abs:camelyon AND abs:stain AND abs:foundation` returned 0.
  - `all:camelyon AND all:stain` returned 3 older papers. The API returned unusually few results, so treat this as weak evidence.
- Web search (3 extended queries):
  - simulated stain variation with CAMELYON17 and UNI/Virchow at slide level;
  - whether simulated stain robustness predicts real multi-centre drops and calibration;
  - ABMIL calibration (ECE) for CAMELYON16 → 17 with FMs.
  - None found a study that does this.

**Novelty check status:** at least two independent sources (Crossref, Europe PMC, web search, plus Semantic Scholar citations) were searched for each gap below. OpenAlex citation and keyword searches were **not** run (budget exhausted). Rerun OpenAlex `cites:` and a keyword search before the protocol.

### Gap 1: Does simulated stain robustness predict real multi-centre failure?

- **Evidence:** the source tested on one external cohort and never compared simulated robustness with performance at real new laboratories. JPI limitations (first and third) say the findings are task-specific and that simulation isolates only part of real variability. The conclusion recommends simulated stains as a stand-in for local validation, which is the claim that needs testing.
- **Novelty check:** none of the searches above found a study that correlates protocol-style simulated robustness with observed cross-centre performance. PathoROB uses real centres but no controlled simulation. Its robustness index could serve as a comparator predictor.
- **Open data:** `camelyon16` (development; RUMC and UMCU), `camelyon17` (500 labelled WSIs, 100 per centre; CWZ, RST and LabPON are truly external).
- **Design sketch:**
  - *Hypothesis:* a model's simulated AUC range on the CAMELYON16 test set predicts its real AUC drop and AUC spread across the CAMELYON17 centres. Slides whose measured stain lies far from the training stain distribution are more often misclassified.
  - *Data:* 50 ABMIL models per FM on CAMELYON16, with 3–4 FMs.
  - *Methods:* protocol Steps 1–3 with the four PLISM references. Add "real-centre references" (median stain vectors and intensities of each CAMELYON17 centre) as a fifth and sixth condition.
  - *Metrics:* Spearman correlation between simulated range and real centre drop, at model and FM level, with bootstrap CIs. Per-slide logistic model of error against stain distance (Mahalanobis distance in stain-vector and intensity space).
  - *Reporting guideline:* CLAIM 2024 (TRIPOD+AI for the external validation items).
- **Rating:** feasibility 3, novelty 5, RunPod, about 6 weeks.

### Gap 2: Calibration and score stability under stain shift

- **Evidence:** the JPI version lists rank-based AUC as limitation 4 and names calibration shifts and absolute score stability as future work (Conclusion).
- **Novelty check:** arXiv 2606.30020 reports NLL for FM-based MIL on CAMELYON16/17 but does not vary stain (abstract only, **verify**). No stain-simulation calibration study was found (Crossref, Europe PMC, web; 2026-11-06).
- **Open data:** `camelyon16`, `camelyon17`.
- **Design sketch:** same model population. Report ECE, Brier score, calibration slope and intercept, and the rate of slides that flip at the 0.5 threshold and at a high-sensitivity threshold, per condition. Test per-condition temperature scaling fitted on 20 CAMELYON17 slides per centre.
- **Rating:** feasibility 4 (no extra GPU once Gap 1 features exist), novelty 4, laptop, +1 week.

### Gap 3: Which metastases does stain variation hide? (a pathologist's stratification)

- **Evidence:** the source task (MSI) is a slide-level molecular label with no size dimension. In nodal staging, isolated tumour cells and micro-metastases are the clinically hard cases and depend on subtle nuclear detail, so they may be the most stain-sensitive.
- **Novelty check:** no study found that stratifies FM stain robustness by metastasis size category (searches above).
- **Open data:** `camelyon17` (slide labels: 36 ITC, 59 micro, 87 macro, 318 negative), `camelyon16` (lesion contours give metastasis area).
- **Design sketch:**
  - Sensitivity per size category under each condition.
  - Attention-map review of slides that flip under simulation: Atul codes the cause, e.g. pale hematoxylin hiding ITC, eosin-heavy sinus histiocytes mimicking tumour, capsule or pigment artefact.
  - A short error taxonomy table.
- **Rating:** feasibility 4, novelty 4, laptop, +1–2 weeks of expert time.

### Gap 4: Open-licence and robustified FMs

- **Evidence:** the source used three NC-ND foundation models (one with manual gating). PathoROB and Filiot et al. 2026 show that robustness can be improved at embedding level, but do not test slide-level stain-simulation robustness.
- **Novelty check:** no slide-level stain-simulation results found for H-optimus-0, Hibou-L, Midnight or the robustified Phaet and Mascaret (searches above).
- **Open data:** same.
- **Design sketch:** add H-optimus-0 (Apache-2.0), Midnight (MIT) and, if their licence allows research use, Phaet and Mascaret. Test whether the PathoROB robustness index of each FM predicts its slide-level stain range.
- **Rating:** feasibility 3 (more GPU), novelty 3, RunPod, +1–2 weeks.

### Gap 5: Indian and LMIC staining ranges (deferred)

- **Evidence:** the PLISM library is Japanese and SurGen and CAMELYON are European. The JPI limitations note that real slides exceed the PLISM range. Hand-stained, variable H&E is common in Indian district laboratories.
- **Open data:** no open Indian WSI cohort with nodal labels was found. Simulated "extreme" references beyond the PLISM range (e.g. the 1st and 99th percentiles of observed CAMELYON17 stain properties, or wider) can stand in.
- **Rating:** feasibility 3, novelty 3. Keep as a discussion point and sensitivity analysis.

## Recommended extension

**Gap 1 + Gap 2 as the core, with Gap 3 as the pathologist's contribution:** "Does simulated stain robustness predict real multi-centre failure? The CTPLab H&E protocol applied to lymph-node metastasis (CAMELYON16 → CAMELYON17), with calibration and metastasis-size analysis."

Why this one:
- It turns the source's open question (does the protocol generalise beyond MSI, and does simulation stand in for real laboratories?) into a direct, falsifiable test. CAMELYON17 is the only open, CC0, slide-level cohort with five labelled centres and three scanners.
- It is clearly different from `plism-scanner` (tile-level device drift, no clinical slide task) and from PathoROB (real-centre embedding robustness, no controlled simulation).
- Calibration and size stratification need no extra GPU, and the size analysis uses Atul's expertise directly.
- The main risk is a ceiling effect on CAMELYON16 AUC. The ITC and micro-metastasis strata and the calibration metrics are built in to keep the analysis informative.

Expected time: about 8 weeks to an arXiv (eess.IV) or medRxiv preprint. Data access is immediate (no account) and compute is 40–80 GPU-h. Best-fit zero-APC journals: J Imaging Informatics in Medicine, Computerized Medical Imaging and Graphics, Laboratory Investigation. The source's own journal (JPI) is on the excluded list (APC).
