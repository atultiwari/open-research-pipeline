---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** Rajapaksha et al., arXiv [2610.33691](https://arxiv.org/abs/2610.33691) (WACV 2027). Its claims: better scores than WSI-LLaVA, and a visible reasoning graph.
- **Benchmark origin:** WSI-Bench from WSI-LLaVA (Liang et al., ICCV 2025, arXiv [2412.02141](https://arxiv.org/abs/2412.02141)).
- **Nearby knowledge- or concept-guided report generators:** knowledge retrieval with regional feature selection (CMPB 2025, [doi:10.1016/j.cmpb.2025.108677](https://doi.org/10.1016/j.cmpb.2025.108677)); SCOUT, concept-grounded generation (arXiv [2605.01144](https://arxiv.org/abs/2605.01144)); RANGER, retrieval re-ranking (arXiv [2603.04348](https://arxiv.org/abs/2603.04348)); PathMem (arXiv [2603.09943](https://arxiv.org/abs/2603.09943)); general-purpose agents for report generation (arXiv [2601.11540](https://arxiv.org/abs/2601.11540)).

**Searches run on 2026-11-06:**
- Crossref and Europe PMC (2024 onwards): "knowledge graph pathology report generation whole slide"; "pathologist evaluation generated pathology reports whole slide image hallucination"; "WSI-Bench report generation"; "metadata shortcut primary site whole slide report generation"; "NCI Thesaurus knowledge graph histopathology".
- arXiv: `all:"report generation" AND all:pathology AND all:knowledge`, sorted by date (15 results).
- OpenAlex was not used (daily free budget used up earlier today).

No study found that has a pathologist grade, slide by slide, whether the morphology claims in a knowledge-guided WSI report are actually visible, or that tests these systems for metadata shortcuts or outside TCGA.

### Gap 1: The explanation is a class template, and nobody checked it against the slide

- **Evidence:** knowledge tokens are deterministic: all slides with the same predicted class get the same subgraph (Section 3.2). Green/red colouring of "present/absent" features is post-hoc text matching (Fig. 5 caption). Evaluation is BLEU/ROUGE/METEOR, BERTScore and an LLM judge only (Sections 4.1–4.2); no pathologist read the generated reports.
- **Novelty check:** searches above found no expert claim-level audit of a knowledge-guided WSI report generator.
- **Open data:** `wsi-bench` (208 test slides), `tcga` (slides viewable in the GDC portal).
- **Design sketch:**
  - *Hypothesis:* most morphology statements in PathKGen reports are copied from the class template; a sizeable share are not visible on that slide, and template-derived claims are wrong more often than claims the model adds itself.
  - *Data:* stratified sample of ~100 test slides across cohorts.
  - *Methods:* split each report into atomic claims; label each as template-derived or model-added; the pathologist rates each claim as visible, not visible, or contradicted, blinded to model arm (PathKGen vs vision-only).
  - *Metrics:* claim-level precision, template share, contradiction rate, diagnosis correctness; agreement with WSI-Precision.
  - *Reporting guideline:* TRIPOD-LLM.
- **Rating:** feasibility 4, novelty 4, RunPod plus ~3 weeks of review, 5 weeks.

### Gap 2: Primary-site metadata may carry the diagnosis

- **Evidence:** primary site alone gives 84% accuracy for the histology classifier (Table 1); the 31 "histology" classes are TCGA cohorts (Appendix A, Table 6). A wrong anchor drops WSI-Precision from 0.480 to 0.254 (Table 5), so the report follows the anchor.
- **Novelty check:** found shortcut work in radiology report generation (EMNLP Findings 2026, [doi:10.18653/2026.findings-emnlp.688](https://doi.org/10.18653/2026.findings-emnlp.688)), none for metadata in WSI report generation.
- **Open data:** `wsi-bench`, `tcga`.
- **Design sketch:** remove the site input, swap it to a plausible wrong site (e.g. lung ↔ head and neck for squamous carcinoma), and give site-ambiguous cases (squamous, adenocarcinoma at several sites). Measure diagnosis flips, claim changes and WSI-Precision. TRIPOD-LLM.
- **Rating:** feasibility 5, novelty 4, RunPod (inference), 2 weeks.

### Gap 3: TCGA only, 208 test reports

- **Evidence:** one benchmark, one split (Section 3.5); one training seed; the WSI-Precision 95% CI (0.451–0.499, Table 7) overlaps the vision-only and histology-only ablations (Table 3).
- **Novelty check:** no PathKGen-style model evaluated outside TCGA in the searches above.
- **Open data:** `cptac` slides with `conch-v15-features-tcga` (CPTAC features built with the same encoder and patch size), labelled with CPTAC histology from the PDC/TCIA.
- **Design sketch:** compute TITAN features for ~300 CPTAC slides across the cohorts shared with TCGA; generate reports; score diagnosis accuracy and claim correctness (from Gap 1's rubric on a subset). Repeat training with three seeds for all arms. TRIPOD-LLM.
- **Rating:** feasibility 4, novelty 3, RunPod, 3 weeks.

### Gap 4: The graph depends on UMLS and GPT-4o, and may have seen test reports

- **Evidence:** graph built from WSI-Bench ground-truth reports with GPT-4o and SapBERT/UMLS (Section 3.4); exclusion of test reports is not stated. UMLS needs a licence agreement; GPT-4o is a paid API.
- **Novelty check:** no pathology report generator found that uses an NCIt-based graph.
- **Open data:** `nci-thesaurus` (CC BY 4.0), training reports from `wsi-bench`.
- **Design sketch:** rebuild the graph from training reports only, with an open LLM (e.g. Qwen2.5-7B) and NCIt concepts; have the pathologist review edges (and record which ones were changed). Compare test scores and claim correctness with the original graph. TRIPOD-LLM.
- **Rating:** feasibility 4, novelty 3, laptop/RunPod, 3 weeks.

### Gap 5: Small models for low-resource settings

- **Evidence:** 1.5B and 3B variants come close to the 7B vision-only model (Table 4), but were not checked for correctness.
- **Design sketch:** include the 1.5B/3B variants in Gap 1's audit; report claim correctness per model size and GPU memory needed. Relevant to pathology labs in South Asia (authors in Sri Lanka, Atul in India).
- **Rating:** feasibility 5, novelty 2, RunPod, +1 week on top of Gap 1.

## Recommended extension

**Gaps 1 + 2 together, with the CPTAC arm of Gap 3 if time allows:** a pathologist audit of whether PathKGen's morphology claims are visible on the slide, and how much of the report changes when the primary-site input is removed or swapped.

Why: it tests the paper's central claim (explainability) with the one thing the authors did not have, a pathologist reading the generated claims against the slide. It needs no new data, only slides viewable in the GDC portal and inference (or a modest retrain). Data are all open or click-through. Expected outcome is publishable either way: if the claims hold, it is independent evidence; if not, it quantifies template copying and shortcut use, which matters for any knowledge-guided report generator. TRIPOD-LLM framing fits JIIM or Artificial Intelligence in Medicine. About 7 weeks to a preprint, mostly review time.
