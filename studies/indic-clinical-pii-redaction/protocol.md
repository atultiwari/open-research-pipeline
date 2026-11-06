---
enriched: true
---
> **Status:** draft for gate 2 (Atul's sign-off). No analysis has been run. Drafted 2026-11-06.

## 1. Background

Clinicians in India increasingly paste lab, pathology and discharge reports into cloud chatbots such as Claude and ChatGPT. These reports carry direct identifiers:
- patient name and age/sex line;
- UHID or lab number, and sample barcode;
- phone number and address;
- referring doctor and hospital;
- increasingly the ABHA number from the Ayushman Bharat Digital Mission (https://abdm.gov.in/).

India's Digital Personal Data Protection Act 2023 and its Rules (notified November 2025; official text URL: verify) make these identifiers personal data. A practical safeguard is to remove identifiers on the clinician's own machine before anything is sent to a cloud model. That needs a de-identification model small and fast enough for an ordinary clinic laptop, and evidence that it works on Indian report formats.

**What exists:**
- **US clinical de-identification:** well studied on US notes, e.g. the 2014 i2b2/UTHealth shared task (Stubbs et al., J Biomed Inform 2015, doi:10.1016/j.jbi.2015.06.007) and the PhysioNet deid software and gold-standard nursing notes (Neamatullah et al., BMC Med Inform Decis Mak 2008, doi:10.1186/1472-6947-8-32). The US HIPAA Safe Harbor method lists the identifiers to remove, including all date elements except the year (HHS guidance, https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html).
- **Local, compact de-identification models:** recent work shows they work in other languages. MedDeID detected 98.9% of identifying text in Dutch hospital notes, and 96.1% with synthetic-only training (Hellemans et al., arXiv:2609.10049). Meddies-PII built 1 million synthetic clinical documents in 17 languages, not yet released (arXiv:2609.12544).
- **Small Indian PII models (the source):** CobuildX-AI released cbx-indic-pii-extractor in 17M, 36M and 58M sizes (Apache-2.0, Hugging Face, 2026-11-05). They are fine-tuned or distilled from mmBERT-small (Marone et al., arXiv:2509.06888) and cover 27 labels, including Aadhaar, ABHA and PATIENT_ID, in 12 Indian languages and Indian English. They run in milliseconds on a CPU.
  - They were trained and tested only on synthetic chats, emails, forms, transcripts and prompts.
  - Their cards say PATIENT_ID and names in native script are weak points.
  - Every date and amount is removed.
  - Health attributes are not detected.
- **Indian benchmarks:** none contains Indian report layouts. IndicPIIDetX, IndiaPII-Bench and Ylemis India-PII have only short medical chats or notes.
- **Limits of identifier removal:** removing explicit identifiers does not remove re-identification risk. A 2026 scoping review (doi:10.3390/j9030022) and the DIRI attack (Morris et al., arXiv:2410.17035) show this.

**Gap:** nobody has tested small, local Indian PII models on Indian clinical reports, measured what they wrongly remove, or measured the full workflow of redacting locally and then reasoning in the cloud.

## 2. Aims and hypotheses

**Primary aim.** Measure identifier leakage (1 − recall) of the 17M, 36M and 58M models on a new synthetic corpus of Indian clinical reports, against open baselines, on a CPU laptop.

- **H1.** Zero-shot, all three models leak patient identifiers specific to clinical reports (PATIENT_ID: UHID, lab number, sample barcode; names in native script) more than general identifiers (phone, email, Aadhaar). Character-level recall for PATIENT_ID is below 0.90 for every size.

**Secondary aims.**
- **H2, over-redaction.** The models remove clinically needed content: eponymous disease names tagged as PERSON in at least 5% of occurrences, and all report and sample dates removed under default settings.
- **H3, downstream utility.** With date-shifting and an eponym post-filter, a cloud LLM's answers on locally redacted reports match its answers on the originals in at least 90% of report–question pairs (non-inferiority margin 5 percentage points, compared with original vs original re-runs).
- **H4, fine-tuning (conditional).** If H1 holds, fine-tuning the 17M model on a separate synthetic clinical training set raises PATIENT_ID recall to at least 0.95 on held-out layout families, without losing more than 0.02 typed F1 on IndicPIIDetX.
- **Exploratory.** Residual re-identification risk: how often an LLM can infer age band, town or hospital from redacted reports.

## 3. Data

| Dataset | Use | Access | Licence and citation |
| --- | --- | --- | --- |
| **IndiClinPII-Syn** (built here) | Primary test set; training set for H4 | Created in this study | Will be released as CC BY 4.0; fully synthetic |
| IndicPIIDetX v0.1 (`datasets/indicpiidetx`) | Reproduction; forgetting check for H4 | Open, Hugging Face | CC BY 4.0; cite CobuildX, doi:10.57967/hf/11457 |
| IndiaPII-Bench (`datasets/indiapii-bench`) | Reproduction; medical-note slice (286) | Open | CC BY 4.0; cite the dataset card |
| Ylemis India-PII (`datasets/ylemis-india-pii`) | Reproduction | Open | CC0 1.0 |
| PhysioNet deidentified nursing notes (`datasets/physionet-deid-nursing`) | Optional English transfer check | Credentialed (CITI + DUA, ~1–2 weeks) | PhysioNet Credentialed Health Data License 1.5.0; cite Neamatullah et al. 2008 and PhysioNet. **The DUA forbids sending these notes to external LLM APIs**, so they are used only with local models. |
| NCI Thesaurus (`datasets/nci-thesaurus`) | Eponym list for the post-filter and probe set | Open | CC BY 4.0 |

**Models:**
- cbx-indic-pii-extractor 17M, 36M and 58M (Apache-2.0).
- `LatentAILabs/chitragupta-pii-indic` (Apache-2.0).
- `OpenMed/OpenMed-PII-SuperClinical-Small-44M-v1` (Apache-2.0).
- A GLiNER PII model, e.g. `knowledgator/gliner-pii-base-v1.0` (licence: verify on the card).
- Microsoft Presidio (MIT) with added Indian recognisers.

**Cloud LLM (utility arm):** one Anthropic model (e.g. Claude Sonnet 5.5) and one OpenAI model, used **only on synthetic reports**.

No real patient data is used anywhere in this study.

## 4. Cohort and inclusion/exclusion criteria

There is no patient cohort. The "cohort" is the synthetic corpus.

**IndiClinPII-Syn target composition (test split):** 1,500 reports.

| Document family | n | Notes |
| --- | ---: | --- |
| Haematology/biochemistry printouts (CBC, LFT, KFT, lipid, HbA1c, thyroid) | 400 | Table layouts, reference ranges, flags |
| Histopathology and cytology reports | 300 | Gross, microscopy, diagnosis; eponyms; specimen IDs |
| Radiology reports | 150 | |
| Discharge summaries | 250 | Long narrative, many dates |
| Prescriptions and OPD slips | 200 | Doses, durations, doctor registration numbers |
| Referral letters and WhatsApp-style result messages | 200 | Code-mixed, romanised Hindi |

**Language mix:** 60% English, 20% Hindi (Devanagari) or bilingual headers, 20% code-mixed or romanised. About 25% of documents get OCR-style noise (character swaps, broken table alignment).

**Identifier inventory (all generated by code):**
- patient name, age/sex, date of birth;
- UHID/MRN, lab or accession number, sample barcode;
- ABHA number and address, Aadhaar (full or masked);
- phone, email, postal address with PIN code;
- referring and reporting doctor names and medical council registration numbers;
- hospital or lab name;
- dates (sample, report, admission, discharge).

Doctor and hospital names get their own labels, so they can be scored apart from patient identifiers.

**Expected spans:** about 10–15 identifier spans per report, so ~15,000–22,000 spans, with at least 300 per identifier type.

**Exclusions:** reports that fail generator checks (label offsets wrong, identifier outside a span, an LLM-written stray name not filled in by code) are regenerated, not kept.

**Probe set (H2):** 300 short clinical sentences containing eponyms (e.g. Hodgkin, Wilson, Hashimoto, Paget, Gleason, Crohn, Cushing), lab values, drug doses and scores, with no patient identifiers.

**Separate training set (H4 only):** 3,000 reports from a different generator seed, different name and place lists, and two layout families held out from the test set.

## 5. Preprocessing

1. **Templates.** Atul writes 40–60 layout templates across the six families: section headings, table structure, typical wording. An LLM (a local model, or an API model on templates with no patient data) writes varied clinical narratives into the slots; **identifier slots are left as placeholders**.
2. **Identifier filling.** Python fills each placeholder. It uses Faker (MIT; has `en_IN`, `hi_IN`, `mr_IN`, `gu_IN`, `ta_IN`, `or_IN` locales) plus custom generators for UHID, lab number and barcode formats, ABHA (14-digit number and ABHA address), and Aadhaar with a valid Verhoeff checksum (as IndicPIIDetX does). Character offsets are recorded as the text is built.
3. **Native-script names.** Names are transliterated to Devanagari for Hindi documents.
4. **Noise.** OCR-style perturbations are applied after labelling, and offsets are re-mapped.
5. **Audit.** Atul checks 100 random reports for realism and missed identifiers. A regex sweep looks for unlabelled digit runs, email-like strings and capitalised name-like tokens. Any error found triggers a generator fix and a full rebuild.
6. **Label mapping.** Each model's labels are mapped to the study's types (patient name, clinician name, PATIENT_ID, ABHA, Aadhaar, phone, email, address, date, organisation). Unmappable types are reported separately.

## 6. Models and baselines

| Arm | Model | Why |
| --- | --- | --- |
| Source | cbx-indic-pii-extractor 17M / 36M / 58M (PyTorch and ONNX) | Main question |
| Indic baseline | Chitragupta (XLM-R large) | Highest-recall Indian model on the cards |
| Clinical baseline | OpenMed-PII-SuperClinical-Small-44M | Small English clinical PII model |
| Zero-shot baseline | GLiNER PII (base) | Commonly used open option |
| Rule baseline | Presidio with Indian regexes (Aadhaar with Verhoeff, PAN, ABHA, Indian phone, PIN code) plus a header-line rule ("Name:", "UHID:", "Lab No:") | What a careful engineer would build without ML; reviewers will expect it |
| Ensemble | Union of the best ML model and the rule baseline | Recall-first deployment option |
| Fine-tuned (H4) | 17M and 58M fine-tuned on the IndiClinPII-Syn training set | Tests whether small models can learn report layouts |

**Post-processing options (H2/H3):**
- **(a) Date-shifting:** replace each date with a date shifted by a per-document random offset, so intervals are preserved.
- **(b) Eponym allow-list:** drop PERSON spans matching NCIt disease and eponym terms when they occur in a clinical-term context.
- **(c) Clinician-name policy:** remove patient names always; replace clinician names with a role token.

## 7. Metrics

**Leakage (primary):**
- character-level recall per identifier type (the share of identifier characters redacted);
- entity-level "any-character-leaked" rate, where a partial redaction counts as a leak;
- document-level leak rate (at least one patient identifier left).

**Precision / over-redaction:**
- character-level precision;
- clinical-content loss (the share of non-identifier tokens redacted);
- eponym false-positive rate on the probe set;
- PII-free flag rate on the benchmarks' no-PII documents.

**Reproduction:** typed-overlap F1 as on the model cards, plus exact-span F1.

**Utility (H3):**
- for 200 test reports × 4 questions (summary, critical-value flags, suggested next tests, a patient explanation in Hindi), whether the answer on the redacted report is equivalent to the answer on the original;
- a baseline of original vs original re-runs, to separate model noise from redaction effects.

**Efficiency:**
- median and 95th-percentile latency per report;
- peak RAM;
- model file size;
- all on a standard laptop (Intel i5/i7 or Apple M-series, 8–16 GB RAM, CPU only) and through ONNX Runtime.

**Residual risk (exploratory):** LLM accuracy at guessing age band, town and hospital from redacted text, compared with chance.

## 8. Statistical analysis plan

- **Confidence intervals:** 95% CIs by document-level cluster bootstrap (2,000 resamples), since spans within a document are correlated.
- **Primary comparison:** character-level recall for PATIENT_ID and patient name, per model, against the 58M model as reference. Paired cluster bootstrap of differences, with Holm correction across the six comparator models within each identifier type.
- **H2:** eponym false-positive rate with a Wilson 95% CI per model; one-sided test against 5%.
- **H3, non-inferiority:** the equivalence rate (redacted vs original) minus the equivalence rate (original vs original). The margin is −5 percentage points, judged by the lower bound of the paired bootstrap CI.
- **Judge validation:** Atul scores 20% of pairs blind to arm; report Cohen's κ between Atul and the LLM judge. If κ < 0.6, Atul scores all pairs.
- **H4:** recall on held-out layout families before vs after fine-tuning (paired bootstrap); typed F1 on IndicPIIDetX before vs after (non-inferiority margin −0.02).
- **Sample size:**
  - *Recall:* with ≥300 spans per identifier type and true recall ≈0.95, the 95% CI half-width is about ±2.5 percentage points before clustering, and about ±3.5 with a design effect of 2.
  - *Overall patient identifiers:* with ~5,000 spans, about ±0.6 points (±0.9 with clustering), enough to separate models 3 points apart.
  - *Utility:* 800 report–question pairs at an expected equivalence of 0.92 give a half-width of about ±1.9 points (±2.7 with clustering by report), well inside the 5-point margin.
- **Missing data:** none expected. Model failures (crashes, timeouts) are counted as full leaks for that document.
- **Subgroups:** language (English, Hindi, code-mixed), OCR noise yes/no, and document family. These are descriptive, with no multiplicity adjustment.

## 9. Validation

- **Internal:** splits are kept separate by generator seed, name list, place list and layout family. Post-filters are tuned on a 300-report dev split; the 1,500-report test split is touched once.
- **Held-out layouts (H4):** two layout families appear only in the test set.
- **External, Indian:** the three public benchmarks (IndicPIIDetX test split; IndiaPII-Bench medical-note slice; Ylemis).
- **External, clinical English (optional):** PhysioNet deidentified nursing notes, local models only, if credentialing is completed in time.
- **Temporal:** not applicable to synthetic data.
- **Real-world check:** out of scope here. The limitations section will call for an ethics-approved check on real Indian reports, run entirely on-premises.

## 10. Reporting checklist mapping

TRIPOD+AI (Collins et al., BMJ 2024, doi:10.1136/bmj-2023-078378) is written for prediction models, so this is an adapted mapping for a de-identification classifier. The TRIPOD-LLM items (Gallifant et al., Nat Med 2025, doi:10.1038/s41591-024-03425-5) cover the cloud-LLM utility arm.

| Item (TRIPOD+AI / TRIPOD-LLM) | Where addressed |
| --- | --- |
| Title and abstract: identify the model, task, data and evaluation | §2, §16 |
| Background and objectives | §1, §2 |
| Data source and dates | §3, §4 |
| Participants / units of analysis, eligibility | §4 (synthetic reports; exclusions) |
| Data preparation, quality checks | §5 |
| Outcome (reference standard) definition | §4–§5 (labels generated by code; audit) |
| Predictors / inputs | §5 (text only) |
| Sample size | §8 |
| Missing data | §8 |
| Analytical methods, model specification | §6 |
| Performance measures | §7 |
| Model updating / fine-tuning | §6 (H4), §9 |
| Fairness / subgroups | §8 (language, script, OCR, family) |
| Open science: code, data and model availability | §14, §16 (CC BY 4.0 corpus, Apache-2.0 models) |
| Patient and public involvement | Not applicable (synthetic); state in the paper |
| LLM: model name, version, access date, settings, prompts | §6, §15 (prompts versioned in the repo) |
| LLM: evaluation design and human evaluation | §7, §8 (Atul's blinded scoring, κ) |
| LLM: data leakage / training contamination | §1, §5 (synthetic corpus created after model training) |
| Limitations and interpretation | §12 |

## 11. Compute and cost

| Step | Hardware | Time | Cost |
| --- | --- | --- | --- |
| Corpus generation (narratives) | API LLM or local model | ~1 day | US$5–20 |
| Zero-shot evaluation, all models | CPU laptop | hours | 0 |
| Chitragupta (XLM-R large) on CPU | laptop | ~1 day | 0 |
| Fine-tuning 17M / 58M (H4) | Colab T4 or RunPod L4 | 1–3 GPU-h | US$0–5 |
| Utility arm, 2 cloud LLMs × 200 reports × 4 questions × 2 conditions + re-runs | API | ~1 day | US$15–40 |
| LLM judge | API | | US$5–10 |

**Total:** under US$80.

## 12. Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Synthetic reports are easier or more regular than real ones | Atul's realism audit, OCR noise, held-out layouts; state the limitation plainly; plan a real-report check later |
| An LLM-written narrative contains an unlabelled real-looking name or number | Placeholders only in LLM text; regex sweep; manual audit of 100 reports |
| The same group made the models and IndicPIIDetX | IndiClinPII-Syn is independent; report the public benchmarks only as secondary |
| Meddies-PII or MedDeID release multilingual clinical models mid-study | Add them as baselines if released; the corpus and the leakage-plus-utility framing stay new |
| Date-shifting changes clinical meaning (e.g. seasonal disease, pregnancy dating) | Report utility with and without shifting; keep the year when safe |
| LLM judge bias in the utility arm | Atul's blinded 20% scoring with κ; switch to full human scoring if κ < 0.6 |
| Credentialed nursing notes sent to an API by mistake | Code guard: the API client refuses any input flagged as coming from PhysioNet; local models only |
| Over-claiming privacy | Report residual-risk findings; frame the tool as a safeguard, not anonymisation |

## 13. Week-by-week timeline

| Week | Work |
| --- | --- |
| 1 | Reproduce the model cards on the three public benchmarks; build the scorer; Atul drafts templates for the six families |
| 2 | Identifier generators (UHID, barcode, ABHA, Aadhaar Verhoeff, Faker Indian locales); narrative generation; first 300-report dev split |
| 3 | Atul's realism audit; generator fixes; full test and training splits; probe set |
| 4 | Zero-shot evaluation of all models; latency and RAM on the laptop; post-filters tuned on dev |
| 5 | Utility arm (cloud LLMs) and judge validation; residual-risk probe; H4 fine-tuning if triggered |
| 6 | Analysis, figures, write-up; release the corpus and code; preprint |

## 14. Repository layout

The analysis code lives in a separate public repo (e.g. `indiclinpii`); this study folder keeps only aggregate results and links.

```
indiclinpii/
├── generator/            # templates (Atul), identifier generators, noise, offsets
│   ├── templates/
│   ├── ids.py            # UHID, barcode, ABHA, Aadhaar (Verhoeff), phone, PIN
│   └── build_corpus.py   # seeds per split; writes JSONL with spans
├── models/               # wrappers: cbx (pii.py), chitragupta, openmed, gliner, presidio
├── eval/
│   ├── score.py          # character / entity / document leakage; precision; content loss
│   ├── bootstrap.py      # cluster bootstrap, Holm
│   └── latency.py
├── utility/              # cloud-LLM questions, prompts, judge, guards
├── finetune/             # H4
├── results/              # aggregate CSVs and figures only
└── data/                 # gitignored: corpus builds, benchmark downloads
```

The synthetic corpus is published as a Hugging Face dataset under CC BY 4.0, not committed to git. PhysioNet notes are never stored in either repo.

## 15. Claude Code analysis task list

1. Create the `indiclinpii` repo; pin Python 3.11 and `torch`, `transformers>=5.0`, `onnxruntime>=1.23`, `presidio-analyzer`, `faker`, `gliner`.
2. Download the 17M/36M/58M models, Chitragupta, OpenMed-44M and the GLiNER PII model; write one `predict(text) -> spans` wrapper each.
3. Download IndicPIIDetX, IndiaPII-Bench and Ylemis to `data/`; write `eval/score.py`; reproduce the card tables (flag gaps > 0.02 F1).
4. Implement identifier generators with unit tests (Verhoeff checksum, ABHA format, offsets survive noise).
5. Load Atul's templates; generate narratives with placeholders; fill identifiers; write dev (300), test (1,500) and training (3,000) splits with separate seeds and name lists.
6. Run the regex sweep and export 100 random reports for Atul's audit; fix and rebuild until the audit passes.
7. Build the 300-sentence eponym/probe set from Atul's list and NCIt terms.
8. Run zero-shot evaluation for all arms on dev; tune post-filters (date-shift, eponym allow-list, clinician-name policy) on dev only.
9. Run the final test-split evaluation once; compute cluster-bootstrap CIs and Holm-adjusted comparisons.
10. Measure latency, RAM and file size on the reference laptop (PyTorch and ONNX).
11. Utility arm: select 200 test reports; run 4 questions × {original, redacted, original re-run} on two cloud LLMs; log model versions and dates; LLM judge; export a 20% blinded sample for Atul.
12. If PATIENT_ID recall is below 0.95, fine-tune 17M and 58M on the training split; evaluate on held-out layouts and IndicPIIDetX.
13. Residual-risk probe on 100 redacted reports.
14. Write aggregate tables and figures to `results/`; copy summaries into this study folder; draft the manuscript.

## 16. Candidate journals and preprint

- **JAMIA** (`jamia`): core informatics venue for de-identification and privacy-preserving LLM use; values open corpora.
- **International Journal of Medical Informatics** (`ijmi`): practical health-IT deployment papers, including LMIC settings.
- **Journal of Biomedical Informatics** (`jbi`): methods-focused; the natural home of the i2b2 de-identification lineage.

Check each journal's current zero-APC subscription route in `journals/journals.yaml` before submission.

**Preprint:** medRxiv (health informatics), or arXiv cs.CL if the venue prefers.
