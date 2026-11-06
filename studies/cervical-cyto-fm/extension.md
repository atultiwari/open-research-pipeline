---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** Dausort et al. (ISBI 2025). Five general or histology encoders, frozen and with LoRA, on four datasets, but only within each dataset. They used random splits, reported accuracy only, and never mapped label systems across datasets.
- **The original register idea is now partly taken.** The register proposed "updated encoders plus conventional Pap → LBC transfer". Since then:
  - **Three open cytology foundation models have appeared**, and their own papers compare them with histology encoders:
    - **CROWN** (Zheng et al., Nature Cancer 2026, [doi:10.1038/s43018-026-01240-0](https://doi.org/10.1038/s43018-026-01240-0)): DINOv2-style, more than 10 million cytology patches. Weights are on [Hugging Face](https://huggingface.co/LexieK/Crown) (Apache-2.0, automatic approval). The [code repository](https://github.com/LexieK7/CROWN) has no licence file.
    - **CervixFM** (Cheng et al., Research Square 2026, [doi:10.21203/rs.3.rs-8629620/v1](https://doi.org/10.21203/rs.3.rs-8629620/v1)): ViT-L pretrained on 18,375 cervical whole-slide images from four centres. It claims evaluation on "nearly all" public cervical datasets. Code at [yehua201826/CervixFM](https://github.com/yehua201826/CervixFM) (MIT); weights on Google Drive and Baidu.
    - **CytoFM** (Ivezić et al., CVPRW 2025, [doi:10.1109/CVPRW67362.2025.00461](https://doi.org/10.1109/CVPRW67362.2025.00461)): iBOT ViT-B. Weights via [ivezicV/CytoFM](https://github.com/ivezicV/CytoFM), which has no licence.
    - UniCAS (Cell Rep Med 2026, [doi:10.1016/j.xcrm.2025.102570](https://doi.org/10.1016/j.xcrm.2025.102570)) is slide-level, and no open weights were found.
  - **Jordán González, "Selective cell-level triage under domain shift in cervical cytology"** ([OSF preregistration, doi:10.17605/osf.io/kga5m](https://doi.org/10.17605/osf.io/kga5m), 27 June 2026). This is the closest planned work. It preregisters frozen foundation-model features, a leave-one-dataset-out protocol with APCData and RIVA as fixed external cohorts, group-aware splits, calibrated abstention and cost-aware deferral. No results were found on 2026-11-06. Its preregistration summary does not name the encoders, a liquid-based arm, few-shot adaptation or annotator disagreement.
  - **Cross-dataset work with CNNs:**
    - H-XAI-Cervix (Research Square 2026, [doi:10.21203/rs.3.rs-10930966/v1](https://doi.org/10.21203/rs.3.rs-10930966/v1); external APACC test in [Zenodo 10.5281/zenodo.22793515](https://doi.org/10.5281/zenodo.22793515)): EfficientNet, Herlev and SIPaKMeD tested on APACC.
    - A multi-source study (Bioengineering 2026, [doi:10.3390/bioengineering13030289](https://doi.org/10.3390/bioengineering13030289)): ResNet and EfficientNet, SIPaKMeD + Herlev + CRIC + proprietary slides, harmonised to four Bethesda classes.
    - The BMT authors' SurePath → ThinPrep CNN test (accuracy fell to about 60%; BMT paper, Usage Notes).
  - **Within-dataset foundation-model work:**
    - DINO LoRA on MLCC at 98.16% (ISIVC 2026, [doi:10.1109/ISIVC69944.2026.11574379](https://doi.org/10.1109/ISIVC69944.2026.11574379));
    - CERVEX on RIVA and SIPaKMeD (medRxiv 2026, [doi:10.64898/2026.09.03.26362210](https://doi.org/10.64898/2026.09.03.26362210));
    - an edge comparison on SIPaKMeD ([doi:10.33803/rjrpfr](https://doi.org/10.33803/rjrpfr)).
  - **Human-like errors:** two JASC 2026 meeting abstracts (["Does a foundation model misclassify cervical cytology cells like a human?"](https://doi.org/10.1016/j.jasc.2026.08.029) and ["A cervical cytology atlas derived from foundation model embedding space"](https://doi.org/10.1016/j.jasc.2026.08.006)) touch on this. Their text was not available, so the overlap is unknown.

**Searches run on 2026-11-06:**

| # | Search | Result |
| --- | --- | --- |
| 1 | OpenAlex works citing the ISBI paper (`cites:W4410296664`) | 4: CytoFM; SC-Net (2026); a plant-disease LoRA paper; CYTOLONE-v2 (Cytopathology 2026, urinary/cervical CLIP-LoRA). None cross-dataset. |
| 2 | OpenAlex search `HiCervix` | 25 hits, including CervixFM, LGPNet, active labelling, a VLM-explanation study and Kukuljan et al. (medRxiv 2025). None trains on one preparation and tests on another. |
| 3 | OpenAlex search "cytology foundation model benchmark" (from 2025-01-01) | Jordán preregistration, CervixFM, CROWN, CytoCrowd, a MedSigLIP thyroid benchmark. No independent cross-dataset cervical benchmark of the cytology encoders. |
| 4 | OpenAlex search "cervical cytology foundation model" (from 2025-01-01) | UniCAS, CervixFM, Cyto-SSL (AAAI 2026), CERVEX, the ISIVC DINO-LoRA paper, the two JASC abstracts, a histology-FM cervical chapter (2025). All within-dataset or slide-level. |
| 5 | Further OpenAlex searches | **Rate-limited (HTTP 429, daily budget used up)**; switched to Crossref and Europe PMC |
| 6 | Crossref "cross-dataset generalization cervical cell classification foundation model" (from 2024-06) | Nothing on cervical cytology |
| 7 | Crossref "SIPaKMeD Herlev cross-dataset external validation" | H-XAI-Cervix only |
| 8 | Crossref "Bethesda system mapping public cervical cytology datasets harmonization" | CytoSet (Neurocomputing 2027, detection); no paper harmonising the public sets for foundation models |
| 9 | Europe PMC: (cervical OR Pap OR LBC) AND cytology AND "foundation model", 2025–26 | 49 hits; none cross-preparation |
| 10 | Europe PMC: cervical cytology AND (cross-dataset OR external validation OR domain shift) AND (SIPaKMeD OR Herlev OR CRIC OR HiCervix OR APACC OR RIVA), 2024–26 | 64 hits; closest is the Bioengineering 2026 CNN study |
| 11 | Europe PMC: cervical cytology AND (interobserver OR multiple annotators OR label noise) AND (deep learning OR foundation model), 2025–26 | 178 hits; top 25 by date scanned; none evaluates encoders against RIVA's multi-annotator labels |
| 12 | DataCite "APCData", "APACC"; Hugging Face model search "cytology", "cyto"; GitHub repo search "cytology foundation model", "CervixFM", "CytoFM" | Open datasets and the three open cytology encoders listed above |
| 13 | Semantic Scholar citations of arXiv:2411.14975 | Rate-limited (HTTP 429), not checked |
| 14 | arXiv: `abs:cytology AND abs:"foundation model"` and a cervical variant | Rate-limited (HTTP 429, two attempts), not checked |

**Result:**
- An "updated encoders on SIPaKMeD/MLCC" benchmark is **no longer worth doing**: CervixFM and CROWN already run broad within-dataset evaluations.
- A frozen-feature leave-one-dataset-out benchmark is **planned** (Jordán), so it must not be the whole story.
- What is still open is the part a cytopathologist owns:
  - a defensible Bethesda mapping across seven open datasets;
  - preparation shift in both directions (conventional ↔ liquid-based);
  - an independent, leakage-audited test of the new cytology encoders against histology and general encoders;
  - few-shot LoRA used as site adaptation;
  - whether models fail where cytologists disagree.
- Novelty rests on that combination and on moving fast. Because three of the search sources were rate-limited, rerun searches 13–14 and an OpenAlex `cites:` search on CROWN and CervixFM before drafting.

### Gap 1: No cross-dataset, cross-preparation test under one Bethesda scheme

- **Evidence.**
  - The source evaluates each dataset separately (Section 4; Table 1) and names no external test.
  - The BMT authors report that preparation alone (SurePath vs ThinPrep) can drop a CNN to about 60% accuracy (BMT paper, Usage Notes).
  - Seven open cervical sets now cover three continents and both preparations. Each has a different label scheme.
- **Novelty check:** searches 3, 6, 7, 10. CNN-only multi-source work exists (Bioengineering 2026; H-XAI-Cervix). Jordán's planned benchmark uses conventional-smear cohorts (APCData, RIVA) and does not mention a liquid-based arm. **No foundation-model study trains on conventional smears and tests on liquid-based cytology, or the reverse.**
- **Open data:**
  - conventional: `cric-cervix` (Brazil), `riva-pap` (Argentina), `apcdata` (Uruguay), `apacc` (Hungary, binary only);
  - liquid-based: `hicervix` (China, cells; preparation to be confirmed), `mendeley-lbc-cervical` (India, fields), `bmt-thinprep` (USA, fields);
  - `sipakmed` (Greece, morphological classes) as a secondary set.
- **Design sketch.**
  - *Hypothesis:* encoder rankings measured within a dataset do not predict rankings across preparations. The drop is largest for the high-grade classes (ASC-H, HSIL) and smallest for the binary NILM-vs-abnormal task.
  - *Label levels* (mapping below, owned by Atul):
    - L1: NILM vs abnormal (≥ ASC-US), for all seven sets;
    - L2: NILM / low grade (ASC-US, LSIL) / high grade (ASC-H, HSIL, SCC);
    - L3: the six Bethesda categories, where the labels allow.
  - *Protocol:*
    - Train on CRIC (conventional) and test on RIVA, APCData, APACC, HiCervix, MLCC and BMT.
    - Train on HiCervix (liquid-based) and test on the conventional sets.
    - Run leave-one-dataset-out as the summary.
    - Split within each set by slide (RIVA, APACC, possibly APCData) or by field (CRIC).
    - The field-level sets (MLCC, BMT) are tiled. The field score is the maximum tile abnormality, plus top-k mean as a sensitivity analysis.
  - *Metrics:* balanced accuracy, macro-F1 and per-class recall (high-grade recall first), with 95% CIs by grouped bootstrap; the drop from within-dataset to cross-dataset; Spearman ρ between in-domain and external encoder rankings.
  - *Reporting guideline:* CLAIM 2024.
- **Rating:** feasibility 4 (HiCervix needs manual approval; three sets need nucleus-centred cropping), novelty 3, RunPod, 3–4 weeks.

### Gap 2: The new cytology foundation models have not been tested independently across datasets

- **Evidence.**
  - CROWN, CervixFM and CytoFM report their own benchmarks. CervixFM's README describes random-seed splits when a dataset has no official split, and none of the three is shown to be tested across preparations.
  - The source found that histology encoders were the best frozen features but adapted worse with LoRA, and concluded that cytology-specific models are needed (Section 5). Those models now exist.
  - Pretraining overlap is unknown. CROWN's 10 million patches may include public sets (verify from its supplement).
- **Novelty check:** searches 1–4, 9 and 12 found no independent head-to-head of CROWN, CervixFM or CytoFM with UNI2-h, Virchow2, H-optimus or CONCH v1.5 on a cross-dataset cervical task.
- **Open data:** as Gap 1.
- **Design sketch.**
  - *Encoders* (Hugging Face API, 2026-11-06):
    - cytology: CROWN (Apache-2.0, auto), CervixFM (MIT repository; Drive weights), CytoFM (no licence; benchmark only);
    - histology: UNI2-h, Virchow2, CONCH v1.5 (all CC-BY-NC-ND, auto), H-optimus-0 (Apache-2.0, auto), H-optimus-1 (CC-BY-NC-ND, manual), Phikon-v2, Midnight (MIT);
    - general: DINOv2-B (Apache-2.0), DINOv3-B (manual), CLIP ViT-B/16 and BiomedCLIP (the source's best few-shot models).
  - *Leakage audit:* for each cytology encoder, list its stated pretraining sources and flag any test set that overlaps.
  - *Metrics:* as Gap 1, plus parameters and CPU time per cell.
- **Rating:** feasibility 4 (CervixFM and CytoFM weights come from Drive links; H-optimus-1 and DINOv3 need manual approval), novelty 4, RunPod, adds about 1 week.

### Gap 3: Few-shot LoRA as site adaptation, not just low-data training

- **Evidence.** The source's main claim is that LoRA works with 1–16 images per class (Figure 1), but always on the same dataset it is tested on. A new laboratory faces a different question: how many locally labelled cells does it need to recover performance on its own slides?
- **Novelty check:** searches 1, 4 and 10 found no cross-site few-shot LoRA for cervical cytology. CYTOLONE-v2 used LoRA to move from cervical to urinary cytology, which is a different task.
- **Open data:** as Gap 1, with target-site shots drawn from training slides only.
- **Design sketch:** for each source → target pair, add k = 0, 1, 2, 4, 8, 16 and 50 target cells per class, then compare:
  - re-fitting the linear probe;
  - prototype (nearest-mean) adjustment;
  - LoRA rank 2 (source recipe) and rank 8.

  Report the shots needed to come within 2 points of in-domain balanced accuracy, with 3 seeds × 5 shot draws.
- **Rating:** feasibility 5, novelty 3, Colab/RunPod, 1–2 weeks.

### Gap 4: Do models fail where cytologists disagree?

- **Evidence.**
  - RIVA is the only open cervical set with four independent expert labels on a subset (386 patches, 7,507 cells; Zenodo record). Its paper quantifies inter-annotator divergence.
  - ASC-US and ASC-H exist precisely because cytologists cannot decide. Hard-label accuracy treats an ASC-US/LSIL confusion like a missed HSIL.
- **Novelty check:** search 11 found no study that scores foundation models against RIVA's multi-annotator labels. The JASC 2026 abstract "Does a foundation model misclassify cervical cytology cells like a human?" asks a related question; its methods and data could not be read (meeting abstract, no text). Cite it and check it before drafting.
- **Open data:** `riva-pap` (multi-annotator subset), with CRIC/HiCervix as the training sources.
- **Design sketch.**
  - Soft-label targets from the four annotators.
  - Metrics:
    - cross-entropy against the soft labels;
    - Spearman ρ between model predictive entropy and annotator entropy;
    - errors split into "annotators agreed" vs "annotators split";
    - model-vs-consensus agreement compared with each annotator-vs-consensus agreement (Cohen's κ), so the model is placed inside or outside the human range.
- **Rating:** feasibility 5, novelty 4, laptop once features exist, 1 week.

### Gap 5: The Bethesda mapping and an expert error taxonomy (the pathologist's question)

- **Evidence.**
  - The source pooled no labels and discussed none. The register note already flagged that SIPaKMeD and Bethesda labels differ.
  - The datasets use seven different schemes (see the mapping below). Every cross-dataset number depends on this mapping, yet published multi-source work states its mapping in a sentence (Bioengineering 2026).
- **Novelty check:** search 8 found no published, justified cross-walk of the open cervical sets.
- **Design sketch.**
  - Atul writes and signs the mapping table as a supplement. Every lossy or debatable mapping becomes a sensitivity analysis: dyskeratotic cells as low vs high grade; RIVA INF and ENDO excluded vs counted as NILM; HiCervix glandular and organism classes excluded.
  - Then add a severity-weighted cost matrix: a missed HSIL or SCC is critical, ASC-US ↔ NILM is minor.
  - Atul reviews the 200 most confident cross-dataset errors and codes the causes: preparation artefact, inflammation or blood obscuring, air-drying, overlap, atrophy or repair mimic, true ambiguity, probable label error, taxonomy mismatch.
- **Rating:** feasibility 5, novelty 3, about 1 week of expert time.

### Gap 6: India and low-resource relevance, and calibration

- **Evidence.**
  - MLCC is the only open Indian liquid-based set found in this search, and the source used it only within the dataset.
  - CERVEX and the edge paper show the interest in low-compute use.
  - No paper reports calibration under preparation shift.
- **Novelty check:** calibrated abstention and deferral are in Jordán's preregistration. The India-specific external test and small-encoder angle are not.
- **Design sketch:**
  - report MLCC (and BMT) field-level transfer separately;
  - add ECE, Brier score and reliability diagrams before and after temperature scaling fitted on the source;
  - include one small encoder (DINOv2-S or H0-mini, manual approval) with CPU latency.
- **Rating:** feasibility 5, novelty 2, inside Gap 1's budget.

## Draft Bethesda mapping (for Atul to own)

| Dataset | Native labels | L1 (NILM vs abnormal) | L2 (NILM / low / high) | L3 (six TBS classes) |
| --- | --- | --- | --- | --- |
| `cric-cervix` | NILM, ASC-US, LSIL, ASC-H, HSIL, SCC (cells) | yes | yes | yes |
| `apcdata` | same six (cells) | yes | yes | yes |
| `riva-pap` | NILM, INF, ENDO, ASC-US, LSIL, ASC-H, HSIL, SCC (cells, 1–4 annotators) | yes; INF and ENDO as NILM, or excluded (sensitivity) | yes | yes |
| `hicervix` | 29-class tree | yes | yes | squamous classes yes; glandular and organisms excluded (check the tree on download) |
| `apacc` | healthy, unhealthy, rubbish, both | healthy vs unhealthy only; rubbish and both excluded | no | no |
| `sipakmed` | superficial-intermediate, parabasal, metaplastic, koilocytotic, dyskeratotic | first three NILM; koilocytotic and dyskeratotic abnormal | koilocytotic → low grade; dyskeratotic indeterminate (both ways as sensitivity) | no |
| `mendeley-lbc-cervical` | NL, LSIL, HSIL, SCC (fields) | yes | yes | no ASC classes |
| `bmt-thinprep` | NILM, LSIL, HSIL (fields) | yes | yes | no |

L2 follows the two-tier squamous intraepithelial lesion terminology of The Bethesda System. ASC-H goes with high grade because it is worked up as possible HSIL. Atul to confirm this against current guidance and to decide how parabasal and atrophic cells are treated, since they are classic HSIL mimics.

## Recommended extension

**Gaps 1 + 2 + 4 as the core, with 3 and 5 as secondary analyses and 6 as a short section.** Working title: "Cytology, histopathology or general foundation models for cervical cells? A Bethesda-harmonised, slide-grouped benchmark from conventional Pap smears to liquid-based cytology, with few-shot LoRA site adaptation and cytologist-disagreement analysis."

Why this one:
- **New against current work:**
  - the first independent cross-dataset test of CROWN, CervixFM and CytoFM against current histology and general encoders;
  - preparation shift in both directions (conventional ↔ liquid-based), which Jordán's conventional-smear cohorts do not cover;
  - an Indian liquid-based external set;
  - errors judged against four-cytologist disagreement on RIVA.

  It reports the binary L1 level too, so it stays comparable with the CNN multi-source papers.
- **Feasibility:** all data are open or free to request. HiCervix needs an institutional email and manual approval; if it is refused, the liquid-based arm falls back to MLCC and BMT at field level. About 25–35 GPU-h.
- **Fit for a pathologist:** the mapping, the cost matrix, the mimic decisions (parabasal, atrophy, repair) and the error review are cytopathology judgements. This is Atul's edge over ML-only groups.
- **Time:** about 7 weeks to a medRxiv or arXiv (eess.IV) preprint.
- **Journals:** Journal of Imaging Informatics in Medicine, Computerized Medical Imaging and Graphics, Laboratory Investigation. All have subscription routes with no APC.

**Risks to manage:**
- Jordán's preregistered benchmark may report first. Cite it, and keep the liquid-based arm, the cytology encoders and the annotator analysis central.
- Pretraining overlap of the cytology encoders with the public test sets is unknown.
- HiCervix's preparation method and slide identifiers are still to be confirmed. MLCC has no patient key and disputed labels.
- Several encoders are CC-BY-NC-ND, and CytoFM has no licence. Use them for benchmarking only and redistribute nothing.
