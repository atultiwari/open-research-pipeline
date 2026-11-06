---
enriched: true
---
## Where the field stands (checked 2026-11-06)

Sources read:
- the full HTML text of the source (arXiv:2604.03205 v1) and the companion (arXiv:2604.06254 v1);
- the source's GitHub code and notebook outputs;
- the CICIoMT2024, CICIoT2023 and WUSTL-EHMS-2020 pages, and the CIC datasets FAQ;
- the header rows of the WUSTL CSV;
- the full text of Jodayree et al. 2026 (PMC13402581), Tarish et al. 2026 (PMC13655100) and Alruwaili et al. 2026 (PMC13667514);
- the README of a third-party generalisation benchmark (VedantGupta-DTU/IoT-NIDS-Generalization-Benchmark).

**The register's plan is now largely pre-empted.** It bundled five ideas: cross-dataset transfer, attack-held-out splits, deduplication, int8 edge models and SHAP stability. Each of these now has at least one 2025–2026 paper on CICIoMT2024 or a close relative:

- **CICIoMT2024 → WUSTL-EHMS-2020 transfer and leave-one-attack-type-out.** Jodayree et al., *Sci Rep* 2026 ([doi:10.1038/s41598-026-50813-7](https://doi.org/10.1038/s41598-026-50813-7)) trained a protocol-aware transformer with session-wise splits, used leave-one-attack-type-out for zero-day testing, and reported about 99.6% accuracy on WUSTL-EHMS-2020. The text read did not explain how WUSTL's Argus features were mapped to CICIoMT2024's window features. FedMedSecure (Tawfik et al., *Sci Rep* 2025, [doi:10.1038/s41598-025-25107-z](https://doi.org/10.1038/s41598-025-25107-z)) reported 91.44% across the same pair (from a search snippet; verify).
- **CICIoT2023 → CICIoMT2024 transfer.** DEA-IDS (Günay et al., *Sensors* 2026, [doi:10.3390/s26196200](https://doi.org/10.3390/s26196200)) combines SHAP, drift statistics and stable-feature selection under a stated leakage-free protocol. Maqsood et al. (Research Square 2026, [doi:10.21203/rs.3.rs-10517817/v1](https://doi.org/10.21203/rs.3.rs-10517817/v1)) also cover it, and the DTU benchmark repo adds INT8 quantisation and pruning.
- **Cross-dataset drops in IoMT generally.** Doménech et al., *Internet of Things* 2025 ([doi:10.1016/j.iot.2025.101631](https://doi.org/10.1016/j.iot.2025.101631)) reported F1 drops of up to about 67% between datasets (from a search snippet; the full text was paywalled).
- **On-device Tsetlin Machine.** The source authors have a follow-up, "On-Device Interpretable Tsetlin Machine-Based Intrusion Detection for Secure IoMT" (IEEE ISI 2026, [doi:10.1109/ISI69914.2026.11685835](https://doi.org/10.1109/ISI69914.2026.11685835); paywalled, contents verify), which probably closes the source's own "resource-constrained device" future-work item.
- **SHAP stability.** Abdullah et al. (CPS-IoTSec 2026, [doi:10.1145/3847353.3847506](https://doi.org/10.1145/3847353.3847506)) compare SHAP and LIME stability across retrained IoT detectors.

**What is still open.** No paper found measures, shortcut by shortcut, how much each common evaluation habit inflates CICIoMT2024 scores. The habits are: pooling the official train and test files and re-splitting rows at random; oversampling before the split; leaving cross-split duplicates in; reporting accuracy on a set that is mostly attacks; and testing only on attack types seen in training. Nor has anyone re-scored the published claims under one clean protocol. Two leads touch this and need checking before the protocol:
- one unidentified paper (indexed under the CICIoMT2024 title on ResearchGate and quoted by a web-search summary) reportedly found a 24.68% near-duplicate rate and only 0.16% cross-split duplication after deduplication;
- an aggregator page mentions a study listing windowing, validation-split and temporal-correlation problems in CICIoMT2024.

If either turns out to be a full audit, Gap 1 narrows to the re-scoring of published claims.

**Pilot evidence from the source's own outputs.** In the BLE training files, 34,291 of 99,840 DoS rows (34%) are exact duplicates, and 1,192 of 31,704 test rows (3.8%) are duplicates within the test set. The code removes duplicates within each split but never checks across train and test.

**Novelty searches** (2026-11-06). The OpenAlex daily budget was used up and the arXiv export API returned HTTP 429 and then timed out, so the skill's fallback order was followed: Crossref (from 2024-01-01), Europe PMC (2024-01-01 to 2026-11-06, which includes preprints), then web search. Semantic Scholar was not tried.

| # | Source | Query | Result |
| --- | --- | --- | --- |
| 1 | Crossref | "CICIoMT2024 cross-dataset generalization intrusion detection" | Generic cross-dataset NIDS papers (IEEE Access 2024 and 2026); none audit CICIoMT2024 |
| 2 | Crossref | "CICIoMT2024 WUSTL-EHMS transfer learning intrusion detection" | Single-dataset benchmarks; no leakage audit |
| 3 | Crossref | "CICIoMT2024 duplicate records data leakage" | Duplicate-leakage audits in other domains (heart disease, sleep, brain MRI, pathology); none on CICIoMT2024 |
| 4 | Crossref | "CICIoMT2024 unseen attack zero-day detection" | Generic zero-day IDS papers |
| 5 | Crossref | "CICIoMT2024 CICIoT2023 cross-dataset evaluation" | CICIoT2023-only benchmarks |
| 6 | Crossref | domain adaptation IoMT; int8 Raspberry Pi IoMT; SHAP stability IDS | DEA-IDS; Maqsood 2026; Mahbub 2026 (ACIIoT2023 → CICIoMT2024); Raspberry Pi 5/Hailo-8 edge-IoT IDS (2026); Abdullah 2026 SHAP/LIME stability |
| 7 | Crossref | source title | SVCC 2026 version of the source; ISI 2026 on-device follow-up |
| 8 | Europe PMC | `CICIoMT2024` | 51 hits, mostly single-dataset model papers; cross-dataset: DEA-IDS, Jodayree 2026, FedMedSecure, Maqsood 2026 |
| 9 | Europe PMC | `CICIoMT2024 AND (cross-dataset OR cross-domain OR generalization OR leakage OR duplicate OR "unseen attack" OR zero-day)` | 43 hits; none quantify leakage inflation |
| 10 | Europe PMC | `"WUSTL-EHMS" AND (cross-dataset OR transfer OR generalization)` | 34 hits; Tarish 2026 ("leakage-free" Nyström sampling: fit-on-train-only pipeline, no deduplication, no CICIoMT2024) |
| 11 | Web search | CICIoMT2024 + WUSTL cross-dataset; duplicates/leakage; leave-one-attack-out; "near-duplicate 24.68%"; benchmark pitfalls | Jodayree 2026; FedMedSecure; Doménech 2025; the federated graph unknown-attack preprint (rs-10527748); an unseen-DoS paper (Springer s44196-026-01268-1); the DTU benchmark repo; the unidentified 24.68% claim |
| 12 | arXiv API | `all:CICIoMT2024` | Not checked (HTTP 429, then timeout) |

### Gap 1: Nobody has measured how much each evaluation shortcut inflates CICIoMT2024 scores

- **Evidence.**
  - The source deduplicates within splits only (notebook cells), and its pooled five-fold cross-validation uses row-level shuffling.
  - The companion uses an 80/20 split with no test set, and its validation table suggests oversampling before the split (Table II).
  - Most CICIoMT2024 papers in searches 8–9 report 96–99.7% accuracy on a set that is mostly attacks.
  - The 2026 IoMT systematic review (Adohinzin et al., *Digital Threats*, [doi:10.1145/3816026](https://doi.org/10.1145/3816026)) names generalisation and evaluation practice as unaddressed dimensions.
- **Novelty check.** Searches 3, 9, 10 and 11 found no shortcut-by-shortcut inflation study on CICIoMT2024. Jodayree 2026 and DEA-IDS use clean protocols but do not report how much the leaky versions would inflate the numbers. The unidentified 24.68%/0.16% paper may cover the deduplication part. **Search status:** three independent sources (Crossref, Europe PMC, web), so complete by the skill's rule. Rerun OpenAlex `cites:` for the dataset paper and an arXiv search before the protocol.
- **Open data:** `ciciomt2024`.
- **Design sketch.**
  - *Hypothesis:* the official file-level split with cross-split duplicates removed gives clearly lower macro-F1 and MCC than the common pooled random-row split. Most of the gap comes from duplicates and window overlap, not from model choice. Model rankings change.
  - *Protocols (a ladder):*
    - P0: pooled train+test, oversample, then random 80/20 split (the companion's habit);
    - P1: pooled random split, oversampling inside training only;
    - P2: the official train/test files as released;
    - P3: P2 with cross-split exact duplicates removed from the test set;
    - P4: P3 with captures grouped where an attack has several numbered capture files (for example ICMP1/ICMP2), holding out whole captures;
    - P5: leave-one-attack-type-out within each family.
  - *Models:* the source's Tsetlin Machine, DT, RF, XGBoost, LightGBM, LR and a small MLP; optionally a reimplemented SE-ViT-BiLSTM.
  - *Metrics:* macro-F1, MCC, benign false-positive rate, and per-family recall, each with bootstrap 95% CIs over capture files; inflation = P0 score minus P3/P4 score; ranking change (Kendall τ).
  - *Reporting guideline:* TRIPOD+AI items on data sources, splits and leakage (adapted). There is no IDS-specific guideline; say so.
- **Rating:** feasibility 5, novelty 3–4 (3 if the unidentified audit is a full study), laptop, 4 weeks.

### Gap 2: Cross-dataset transfer claims are not reproducible because feature alignment is undisclosed

- **Evidence.** WUSTL-EHMS-2020 has Argus flow metrics, CICIoMT2024 has CIC window features, and WUSTL releases no pcaps (dataset pages). Only a handful of fields map by meaning: duration, rate, total bytes and packets, minimum and maximum packet size, and protocol. Jodayree 2026 reports about 99.6% transfer without describing the mapping in the text read. WUSTL labels were set from the attacker's source MAC, so identifier columns leak the label.
- **Novelty check.** CICIoT2023 → CICIoMT2024 transfer is done (DEA-IDS, Maqsood 2026, DTU repo), and so is CICIoMT2024 → WUSTL (Jodayree 2026, FedMedSecure). No paper found publishes a feature-by-feature harmonisation table or reports transfer with the leaking identifiers removed.
- **Open data:** `ciciomt2024`, `ciciot2023`, `wustl-ehms-2020`.
- **Design sketch.** Two arms.
  - *CICIoMT2024 ↔ CICIoT2023:* same extractor, about 44 shared features. Map the labels to shared families (benign, DoS, DDoS, Recon, Spoofing).
  - *CICIoMT2024 → WUSTL:* a published harmonisation table of 5–8 semantically matched features; binary only, because WUSTL attacks are man-in-the-middle; WUSTL identifier columns dropped.
  - *Metrics:* MCC, benign FPR, AUROC, calibration (ECE) before and after target-side threshold recalibration on 1% of target rows.
  - Report honest floor numbers alongside the published claims.
- **Rating:** feasibility 4, novelty 2–3, laptop, +1–2 weeks on top of Gap 1.

### Gap 3: Attack-held-out (zero-day) generalisation of lightweight, explainable models

- **Evidence.** The source tests only attack types seen in training (Section VI) and lists diverse realistic attacks as future work (Section VII).
- **Novelty check.** Jodayree 2026 already runs leave-one-attack-type-out on CICIoMT2024 with a transformer. The federated graph preprint and an unseen-DoS paper (search 11) also test unseen attacks. Lightweight or rule-based models (Tsetlin Machine, shallow trees) under this protocol were not found.
- **Open data:** `ciciomt2024`.
- **Design sketch.** Fold P5 of Gap 1 into the main paper. Report detection rate for the held-out type at a fixed benign FPR (1%), using binary benign-versus-attack heads.
- **Rating:** feasibility 5, novelty 2, laptop, part of Gap 1.

### Gap 4: Measured int8 edge cost, and whether explanations survive quantisation and leakage removal

- **Evidence.** The source measured time on a laptop only and lists resource-constrained devices as future work (Section VII). The companion lists compression and XAI as future work.
- **Novelty check.** The source authors' ISI 2026 follow-up appears to cover on-device Tsetlin Machines (paywalled, verify). The DTU repo reports INT8 dynamic quantisation for CICIoT2023 models. Abdullah 2026 covers SHAP/LIME stability across retrains. Untested: whether the top features change between the leaky (P0) and clean (P3/P4) protocols, and after int8 quantisation.
- **Open data:** `ciciomt2024`.
- **Design sketch.** Use ONNX Runtime int8 for the MLP and trees, and report model size and p50/p95 latency on a laptop CPU and, if available, a Raspberry Pi (optional; mark as not done if no device). SHAP top-10 overlap (Jaccard) and Kendall τ across seeds, protocols and fp32 versus int8.
- **Rating:** feasibility 4 (hardware optional), novelty 2, laptop, +1 week.

### Gap 5: Indian hospital framing (DPDP Act 2023, CERT-In)

- **Evidence.** None of the papers read discusses Indian hospital networks. Indian hospitals run many of the same Wi-Fi/MQTT/BLE devices, and the DPDP Act and CERT-In reporting duties make false-positive rates and explainability operational issues.
- **Novelty check.** Not searched as a standalone study; it is a discussion section.
- **Design sketch.** In the discussion, translate the benign FPR from Gap 1 into alerts per day for a typical Indian hospital ward network, and map detector outputs to incident-reporting duties (check current CERT-In and DPDP rules before writing; verify).
- **Rating:** feasibility 5, novelty 1 standalone; adds value inside Gap 1.

## Recommended extension

**Gap 1 as the core, with Gap 3 as its last protocol step and a slimmed Gap 2 (CICIoMT2024 ↔ CICIoT2023, plus the WUSTL harmonisation table) as the external check:** "How much of CICIoMT2024 intrusion-detection accuracy is an evaluation artefact? A shortcut-by-shortcut leakage audit of lightweight, explainable detectors, with transfer to CICIoT2023 and WUSTL-EHMS-2020."

Why this one:
- It is the part of the register's plan that the searches did not find done. Transfer, zero-day, int8 and SHAP-stability papers already exist, but none measures how much each shortcut inflates the scores.
- It has the same logic as the HepatoBench leakage audit in this catalogue (duplicates, grouped splits, ranking changes), which Atul already knows from pathology.
- All data are free (two CIC registration forms and one direct CSV), a laptop is enough, and the source code is public (GPL-3.0).
- A clear negative or corrective result is publishable in this crowded field. The register's own note said it is only publishable with a clear "published accuracies are inflated" finding.

Main risks:
- an unidentified paper may already report duplicate rates on CICIoMT2024;
- fit for a pathologist is modest, because there is no clinical-judgement component;
- WUSTL transfer can use only a few harmonised features.

Expected time: about 6 weeks to a preprint. Best-fit zero-APC journals: *Journal of Information Security and Applications*, *Computers & Security*, *Journal of Medical Systems*.
