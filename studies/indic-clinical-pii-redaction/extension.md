---
enriched: true
---
## Atul's direction

Find the scope for PII extraction and redaction in healthcare reports, with priority on models small enough to run locally. The goal: identifiers are removed on the clinic's own machine, and only then is the report sent to Claude or ChatGPT for the heavy AI work.

## Where the field stands (checked 2026-11-06)

**Small Indic PII models (source):**
- cbx-indic-pii-extractor 17M/36M/58M (Apache-2.0, CPU-fast), trained and tested on chats, emails, forms, transcripts and prompts.
- Chitragupta (`LatentAILabs/chitragupta-pii-indic`, XLM-R large, Apache-2.0).
- No Indian model has been tested on lab, pathology or discharge reports.

**Clinical de-identification, local and small:**
- MedDeID (Hellemans et al., arXiv [2609.10049](https://arxiv.org/abs/2609.10049)): an on-premises framework. A compact transformer detected 98.9% of identifying text in Dutch hospital notes, and a model trained only on synthetic notes reached 96.1%. Dutch and synthetic English only.
- OpenMed PII models, e.g. [OpenMed-PII-SuperClinical-Small-44M](https://huggingface.co/OpenMed/OpenMed-PII-SuperClinical-Small-44M-v1) (Apache-2.0, trained on nvidia/Nemotron-PII): English, 54 types, not Indian identifiers.
- obi/deid_roberta_i2b2 and StanfordAIMI/stanford-deidentifier-base (MIT): US clinical notes.

**Multilingual clinical:**
- Meddies-PII (arXiv [2609.12544](https://arxiv.org/abs/2609.12544)): 1 million synthetic clinical documents in 17 languages. The dataset and model will be released "upon acceptance", and the abstract does not say whether Indian languages are included (verify).
- BioNLP 2026 multilingual clinical de-identification refinement ([doi:10.18653/v1/2026.bionlp-1.11](https://doi.org/10.18653/v1/2026.bionlp-1.11)).

**Limits of PHI removal:**
- A 2026 scoping review shows that removing explicit PHI does not make notes non-identifiable: rare diagnoses, places and timelines remain ([doi:10.3390/j9030022](https://doi.org/10.3390/j9030022)).
- DIRI ([arXiv 2410.17035](https://arxiv.org/abs/2410.17035)) re-identifies patients from anonymised notes with LLMs.

**Indian benchmarks with any medical content:** IndicPIIDetX (~1,000 healthcare-domain chats and forms), IndiaPII-Bench (286 short medical notes) and Ylemis (`medical_id` type). None has report layouts.

**Searches run on 2026-11-06:**
- Crossref and Europe PMC (2024 onwards): "de-identification clinical notes small language model local deployment"; "PII redaction before large language model healthcare privacy-preserving pipeline"; "Indian clinical text de-identification"; "de-identification pathology reports deep learning"; "multilingual clinical de-identification Hindi".
- arXiv: `deidentification AND clinical AND LLM`.
- Web search for MDeID/multilingual medical de-identification.
- Hugging Face model and dataset search ("OpenMed-PII", "chitragupta", benchmark cards).
- OpenAlex not used (daily budget used up).

**Verdict: real scope.** No open benchmark of Indian clinical reports exists, and no small Indian model has been tested on them. Nobody has measured the full local-redaction-then-cloud workflow: how much leaks, and how much the cloud answer degrades.

### Gap 1: No Indian clinical-report test set

- **Evidence:** the model cards list five document types, none of them a lab, pathology or discharge report (IndicPIIDetX card). PATIENT_ID is a weak label (17M card, Limitations).
- **Novelty check:** searches above found no Indian clinical de-identification corpus.
- **Open data:** none real. Build **IndiClinPII-Syn**:
  - *Document types (~1,500 reports):* CBC/LFT/KFT printouts, histopathology and cytology reports, radiology reports, discharge summaries, prescriptions, referral letters and WhatsApp-style result messages.
  - *Formats:* English, Hindi and code-mixed text, plus OCR noise from scanned printouts.
  - *How it is built:* Atul writes the layouts and clinical content. Every identifier is filled in by code: names, UHID and lab IDs, sample barcodes, ABHA, Aadhaar, phone numbers, addresses, referring and reporting doctors, hospital names, dates. Span labels come out exactly.
  - *Release:* CC BY 4.0, fully synthetic.
- **Design sketch:** run the 17M/36M/58M models, Chitragupta, OpenMed-44M and a rule baseline (Presidio with Indian ID patterns). Report character-level recall per identifier type (leakage first), precision, PII-free flag rate, and CPU latency on a standard clinic laptop.
- **Rating:** feasibility 5, novelty 4, laptop, 3 weeks.

### Gap 2: Over-redaction destroys clinical content

- **Evidence:**
  - DATE and AMOUNT cover every date and amount (cards, Limitations), so sample, report and admission dates vanish, and with them the intervals that clinical questions need.
  - Eponyms and doctor-named entities (Hodgkin lymphoma, Wilson disease, Hashimoto thyroiditis, Gleason score) may be tagged as PERSON.
  - The cards do not separate patient names from clinician names. For a cloud LLM, the referring doctor is usually harmless context; the patient's name is not.
- **Novelty check:** found no measurement of eponym false positives or clinical-date loss in Indian PII models.
- **Design sketch:**
  - *Probe set:* about 300 sentences with eponyms, lab values, doses and scores.
  - *Measures:* the share of clinical tokens removed (clinical-content loss) and the eponym false-positive rate.
  - *Date-shift option:* replace dates with consistent per-patient offsets, so intervals survive.
  - *Fix:* a light post-filter (eponym list from an open terminology such as `nci-thesaurus`), compared against fine-tuning.
- **Rating:** feasibility 5, novelty 4, laptop, 2 weeks (inside Gap 1's corpus).

### Gap 3: The redact-locally, reason-in-the-cloud workflow is unmeasured

- **Evidence:** this is Atul's question, and no study found it measured end to end. MedDeID stops at de-identification.
- **Design sketch:**
  - *Questions:* for 200 synthetic reports, ask a cloud LLM the same clinical questions (summarise, flag critical values, suggest next tests, draft a patient explanation in Hindi) on (a) the original and (b) the locally redacted report.
  - *Scoring:* Atul scores answer equivalence on a sample; an LLM judge scores the rest.
  - *Leak audit:* a regex and model check of everything that would have left the laptop.
  - *Outcome:* the trade-off curve between leakage and utility for each model size, with and without date-shifting.
  - *Data handling:* synthetic data only, so sending reports to the API is safe.
  - *Reporting guideline:* TRIPOD-LLM items for the utility arm.
- **Rating:** feasibility 5, novelty 4, laptop + API (~US$10–40), 2 weeks.

### Gap 4: Fine-tune the 17M model on clinical layouts

- **Evidence:** the 17M model was distilled from general documents only; PATIENT_ID and names in native script are its weak points (card).
- **Design sketch:** fine-tune the 17M and 58M models on a training split of IndiClinPII-Syn, with a different generator and name lists from the test split. Test on a held-out layout family, the three Indian benchmarks (to check nothing is forgotten), and, if credentialed, the PhysioNet nursing notes (`physionet-deid-nursing`) for English transfer. Export to ONNX; time on a low-end Windows laptop and an Android phone.
- **Rating:** feasibility 4, novelty 3, Colab, 2 weeks.

### Gap 5: Quasi-identifiers survive token redaction

- **Evidence:** scoping review and DIRI (above).
- **Design sketch:** on redacted reports, ask an LLM to guess the patient's age band, town or hospital from what is left. Report the residual risk and which report sections carry it. A short add-on section, not a paper on its own.
- **Rating:** feasibility 4, novelty 3, API, 1 week.

## Recommended extension

**Gaps 1 + 2 + 3:** build IndiClinPII-Syn, a pathologist-designed synthetic corpus of Indian lab, pathology and discharge reports. On it, measure how much the 17M–58M models leak and over-redact on a CPU laptop, and how much a cloud LLM's answers change after local redaction.

Why:
- It answers Atul's question directly, with a model small enough for any clinic laptop.
- Everything is open: Apache-2.0 models and a synthetic CC BY 4.0 corpus that others can reuse.
- It needs no credentialing or GPU.
- The report layouts and the over-redaction probes (eponyms, dates, doses) draw on Atul's pathology expertise.
- Under India's DPDP Act 2023, a local-first redaction step is a practical safeguard for clinicians already pasting reports into chatbots.

Add Gap 4 (fine-tuning) if the zero-shot models leak PATIENT_ID or names in native script. Be explicit that synthetic results need confirming on real reports under ethics approval. About 6 weeks; JAMIA, IJMI or JBI.
