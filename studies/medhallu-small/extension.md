---
enriched: true
---
## Where the field stands (checked 2026-11-06)

- **Source:** Pandit et al., MedHallu, *EMNLP 2025* (arXiv 2502.14302).
  - It tested 14 detectors. The open ones are all 2024 models of 2B–14B (Gemma-2, Llama-3.1/3.2, Qwen2.5, DeepSeek-R1-Distill-Llama-8B) plus four Llama/Mistral-era medical fine-tunes.
  - It used two evidence conditions: none, or the **source abstract** itself.
  - There was no specialist verifier (NLI/MiniCheck/HHEM-type), no calibration, no human check of the hallucinated answers, and no artefact baseline.
- **Large-model leaderboards on MedHallu:**
  - Stanford [MedHELM (Nature Medicine 2026)](https://doi.org/10.1038/s41591-025-04151-2) scores both answers of the 1,000 `pqa_labeled` items, with the abstract, for 13 mostly large or proprietary models.
  - A third-party harness, [jev-medhallu-benchmark](https://github.com/stperic/jev-medhallu-benchmark) (MIT, September 2026, not peer-reviewed), adds fast frontier models. It reports about 87–95% accuracy with the abstract and 66–83% without it. In other words, the oracle-abstract setting is close to saturated for big models.
- **Artefacts:**
  - [PARALLAX (Hussain & Kantarcioglu, arXiv 2605.17028)](https://doi.org/10.48550/arxiv.2605.17028) evaluates 22 internal-state and output detectors on six corpora, including a 500-item MedHallu sample. A TF-IDF text-similarity control reached AUROC 0.71 on MedHallu, so part of the apparent detection signal is surface text.
  - PARALLAX cites the dataset as "MedHallBench Authors, 2024" and says GPT-4 generated the pairs, which does not match this dataset. **Verify** which release it used.
  - It tests no prompted small LLMs, no length baseline and no retrieval.
- **Other work that uses MedHallu:**
  - [Eryılmaz et al., JMIR Preprints 2026](https://doi.org/10.2196/preprints.109219): self-consistency disagreement as an error signal across 7 open models and 5 datasets, MedHallu among them. This is a different task (answering, not judging a given answer).
  - [Krishnaprasad, Research Square 2026](https://doi.org/10.21203/rs.3.rs-9749892/v1): a TF-IDF retrieval-plus-threshold detector tested on MedHallu and TruthfulQA. It is not small-LLM based and has no expert audit.
  - [MedHal-Loc (arXiv 2606.21517)](https://doi.org/10.48550/arxiv.2606.21517): span localisation on 300 PubMedQA-derived statements with injected errors.
- **Lightweight detectors outside medicine:** [Faujdar & Kadvani, GroundLM 2026](https://aclanthology.org/2026.groundlm-1.29/) benchmark CPU-only detectors (ROUGE, BERTScore, a DeBERTa NLI) on HaluEval. They found NLI plus similarity is best for QA. MedHallu was not included.
- **Expert adjudication:** [Cecil & Freedman, Findings of EMNLP 2026](https://aclanthology.org/2026.findings-emnlp.1935/) show that single-pass medical hallucination labels miss errors, and that adjudicators disagree. Which existing benchmark they re-adjudicated: **verify**.

**Searches run on 2026-11-06:**
- **OpenAlex:**
  - title search for the published version: found EMNLP 2025, W4416037066;
  - works citing W4416037066: 43 results, all read by title, with abstracts for the 8 closest;
  - keyword searches: **rate-limited, not checked** (the free daily budget ran out mid-session).
- **Crossref keyword searches** (from 2025-03-01, top 12 each), used in place of OpenAlex:
  - "MedHallu medical hallucination detection";
  - "small language models medical hallucination detection";
  - "lightweight hallucination detector biomedical question answering";
  - "hallucination detection benchmark artifacts shortcut length bias";
  - "retrieval augmented hallucination detection PubMed evidence";
  - "pathologist expert annotation LLM hallucination laboratory medicine";
  - "MedGemma Gemma 3 Qwen3 hallucination";
  - "abstention selective prediction hallucination detection medical language model".
- **Semantic Scholar citations of arXiv:2502.14302:** rate-limited (HTTP 429), not checked.
- **arXiv API:** four calls (`abs:MedHallu`, small/lightweight medical hallucination detection, PubMedQA hallucination detection), all refused with "Rate exceeded". Not checked.
- **GitHub code search for "UTAustin-AIHealth/MedHallu":** about 30 repos. Users include HELM/MedHELM, Medmarks, MIRIAD, CoEval, opik, the jev benchmark and "When Rubrics Fail" (Farrow et al., arXiv 2609.12718, rubric grading). None evaluates 2026 sub-10B models with realistic retrieval, or audits labels.

**Bottom line:**
- Nobody has published MedHallu results for **2026 sub-10B open models**, or for **cheap specialist verifiers**.
- No one has tested detection under **realistic retrieval** (source abstract excluded) instead of the oracle abstract.
- No one has controlled for the **length artefact**.
- No one has checked how many "hallucinated" answers a **domain expert** agrees are wrong.
- arXiv and Semantic Scholar could not be checked, so **rerun those two before the protocol**.

**Overlap inside this repo:**
- `quantised-labmed` uses MedHallu as one outcome of **quantisation**. Do not add quantisation here, and run everything at BF16.
- `mpib-small-llm` uses an overlapping 2026 small-model panel for **prompt-injection** safety. Keep the panels aligned so the studies can cite each other.

### Gap 1: 2026 small open models and cheap verifiers are untested

- **Evidence:** Table 2 and Table 7 list only 2024-era open models. The Limitations section says advanced models and prompting strategies were out of reach. The best open small model with the abstract was Qwen2.5-7B (F1 0.839).
- **Novelty check:** the citing works (OpenAlex), the Crossref queries and the GitHub search found no MedHallu results for Gemma 4, Qwen3.5, Phi-4-mini or MedGemma 1.5, and none for HHEM/MiniCheck/LettuceDetect. MedHELM and the jev harness cover large and hosted models. **Novel as of 2026-11-06** (arXiv not checked).
- **Open data:** `medhallu`, `pubmedqa`.
- **Design sketch:**
  - *Generative judges,* with licences and gating per the HF API (2026-11-06):

    | Model | Licence | Gating |
    | --- | --- | --- |
    | [Gemma 4 E2B-it](https://huggingface.co/google/gemma-4-E2B-it) | Apache-2.0 | not gated |
    | [Gemma 4 E4B-it](https://huggingface.co/google/gemma-4-E4B-it) | Apache-2.0 | not gated |
    | [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) | Apache-2.0 | not gated |
    | [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | Apache-2.0 | not gated |
    | [Phi-4-mini-instruct](https://huggingface.co/microsoft/Phi-4-mini-instruct) | MIT | not gated |
    | [MedGemma 1.5 4B-it](https://huggingface.co/google/medgemma-1.5-4b-it) | Health AI Developer Foundations terms | auto |
    | [Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) (anchor to Table 2) | Apache-2.0 | not gated |
    | [Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) (anchor) | Llama 3.2 licence | manual approval |

  - *Specialist verifiers* (these need evidence, so they run in the knowledge conditions only):

    | Model | Licence | Note |
    | --- | --- | --- |
    | [HHEM-2.1-Open](https://huggingface.co/vectara/hallucination_evaluation_model) | Apache-2.0 | CPU-feasible |
    | [MiniCheck-Flan-T5-Large](https://huggingface.co/lytang/MiniCheck-Flan-T5-Large) | MIT | CPU-feasible |
    | [Bespoke-MiniCheck-7B](https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B) | CC BY-NC 4.0 (card) | research use only |
    | [LettuceDetect base](https://huggingface.co/KRLabsOrg/lettucedect-base-modernbert-en-v1) | MIT | token-level |
    | [DeBERTa-v3-large NLI](https://huggingface.co/MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli) | MIT | the "classic" baseline |

  - *Protocol:*
    - paired scoring of both answers per item (2,000 judgements on `pqa_labeled`);
    - greedy decoding and a strict parser;
    - Qwen3.5 run with thinking on and off as a secondary contrast.
  - *Metrics:*
    - AUROC (from the token probability of "1", or the verifier score);
    - F1 and balanced accuracy at a threshold fixed on `pqa_artificial`;
    - hard-item F1;
    - latency per check on CPU and GPU.
  - *Reporting guideline:* TRIPOD-LLM, with MI-CLEAR-LLM items (model revision hash, decoding, prompt).
- **Rating:** feasibility 5, novelty 3 on its own (a refresh), RunPod (verifiers on a laptop), 2 weeks.

### Gap 2: The "knowledge" is the answer key. Test realistic retrieval instead

- **Evidence:**
  - "Knowledge" is the PubMedQA context of the same abstract whose conclusion is the ground truth (paper Appendix J and Figure 7; confirmed by the exact join on 2026-11-06).
  - Gains of +0.25 F1 (Section 5.2) therefore measure reading the answer key.
  - The Limitations section asks for other corpora.
  - The jev harness shows this setting is near ceiling for large models.
  - A deployed checker never gets the source abstract.
- **Novelty check:**
  - Crossref "retrieval augmented hallucination detection PubMed evidence" found general RAG-detector robustness work ([Kulanthaivelu, Research Square 2026](https://doi.org/10.21203/rs.3.rs-11400108/v1): DeBERTa AUROC falls under evidence shift on RAGTruth and HaluBench) and HA-MedRAG (internal states plus retrieval for *mitigation*).
  - Krishnaprasad's TF-IDF detector retrieves evidence, but without excluding the source, and with no LLM judges.
  - None replaces MedHallu's oracle abstract with retrieved literature that excludes the source.
  - **Novel as of 2026-11-06.**
- **Open data:** `medhallu`, `pubmedqa` (PMIDs and MeSH). PubMed itself via [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25497/), which is free and needs no account. An API key is optional. Do not put Atul's email in requests (CLAUDE.md rule 9).
- **Design sketch:**
  - *Evidence conditions:*
    - E0 none;
    - E1 oracle abstract (the paper's setting);
    - E2 top-5 PubMed abstracts retrieved by question, **source PMID excluded**;
    - E3 as E2, restricted to papers published before the source paper. This is the strictest and most realistic condition.
  - *Retrieval:* E-utilities `esearch` plus `efetch`, re-ranked with [MedCPT](https://huggingface.co/ncbi/MedCPT-Query-Encoder) (public domain).
  - *Retrieval quality:* log recall of near-duplicate abstracts with a similarity cut-off, and record how often the source's conclusion is restated by a citing paper (leakage).
  - *Hypotheses:*
    - the E1 → E2/E3 drop is large for small LLMs and larger still for NLI verifiers, which assume the evidence entails or contradicts the answer;
    - with retrieval, the ranking of models changes.
  - *Analysis:* paired, mixed-effects logistic regression (correct ~ condition × model + difficulty, with item as a random effect); McNemar for the key contrasts.
- **Rating:** feasibility 4 (the retrieval pipeline is the main build), novelty 4, laptop for retrieval plus RunPod for judging, 2 weeks.

### Gap 3: Construction artefacts and circular difficulty labels

- **Evidence:**
  - Section 4 says hallucinated answers were held within ±10% of the ground-truth length. In the released `pqa_labeled`, only 14% are, and 75% are shorter (computed 2026-11-06).
  - Difficulty was defined by whether GPT-4o-mini, Gemma-2-9B and Qwen2.5-7B were fooled (Section 3). Low hard-item scores for those models and their relatives are therefore partly built in.
  - Sections 3 and 4 disagree on the filter rule (majority vs at least one).
  - PARALLAX found TF-IDF AUROC 0.71 on a MedHallu sample.
- **Novelty check:**
  - Crossref "…artifacts shortcut length bias" found artefact audits in other domains (URL detection, IoMT IDS) and PARALLAX.
  - PARALLAX is the only medical-hallucination artefact study. It addresses internal-state detectors and teacher-forced text similarity, not length, not difficulty circularity, and not prompted LLM judges.
  - **Partly novel.**
- **Open data:** `medhallu`.
- **Design sketch:**
  - *Text-only baselines,* run without any model: answer length, length ratio, TF-IDF overlap with the question, and a logistic regression on these features with 5-fold CV grouped by item.
  - *Length-matched subset:* items whose two answers differ by ≤10% in length, plus a length-stratified analysis. Rerun Gap 1/2 rankings on it.
  - *Circularity:* compare hard-item performance of the filter models' families (Gemma, Qwen2.5) with families that played no part in construction (Phi, Llama-3.2).
  - Report every model's margin over the best text-only baseline. Treat that margin as the honest headline.
- **Rating:** feasibility 5, novelty 3–4, laptop, under 1 week. It strengthens every other gap.

### Gap 4: Are the "hallucinations" really wrong? A pathologist audit of a lab-medicine subset

- **Evidence:**
  - No human checked the generated answers. The pipeline relies on LLM filters and an NLI threshold (Section 3).
  - The paper's examples include a hedged ground truth (Table 10, the NASH/ASH laboratory-marker item).
  - "Misinterpretation of question" makes up 75% of `pqa_labeled`, and some such answers may be off-topic rather than false.
  - The paper itself warns the data is machine-generated (ethics statement).
  - Cecil & Freedman show single-pass medical labels are incomplete.
- **Novelty check:** no Crossref, citing-work or GitHub result reports an expert audit of MedHallu labels. The closest work is rubric-based grading ("When Rubrics Fail") and generic adjudication (Cecil & Freedman). **Novel as of 2026-11-06.**
- **Open data:** `medhallu`, `pubmedqa` (MeSH). Of the 1,000 `pqa_labeled` items, 169 carry laboratory, biopsy, biomarker, pathology or diagnostic-accuracy MeSH terms (checked 2026-11-06). Atul curates these to about 120–150 genuine lab-medicine and pathology items.
- **Design sketch:**
  - *Blinded review:* Atul reviews each item's two answers in random order, with the question and abstract. For each answer he records:
    - is it correct, incorrect, or partly correct / unverifiable;
    - if incorrect, the error type, using a pathologist taxonomy (wrong analyte or test, wrong direction of change, wrong diagnostic-accuracy claim, wrong grade or stage, overgeneralisation from a study population, off-topic);
    - the potential clinical harm (none / minor / major).
  - *Reliability:* a second rater (a colleague in pathology or lab medicine) re-rates 30% for Cohen's κ, or Atul re-rates after a 2-week washout for intra-rater κ.
  - *Outputs:*
    - label-validity rate;
    - detector metrics recomputed on the expert-confirmed labels;
    - which error types the small models miss.
  - Publish aggregate counts only. Do not republish the items.
- **Rating:** feasibility 5, novelty 4, laptop, about 1–1.5 weeks of expert time. This is Atul's distinctive contribution.

### Gap 5: Calibration and abstention done properly

- **Evidence:**
  - The "not sure" option is prompted only (Section 5.4, Tables 4–5), and the released parser counts "not sure" as *hallucinated* (see `replication.md`).
  - There is no AUROC, calibration or risk–coverage analysis, although precision under abstention is the paper's safety argument.
- **Novelty check:** the Crossref abstention query found general selective-prediction work (conformal risk control for RAG detection) and Eryılmaz et al. (self-consistency for answering, not judging). No calibration study on MedHallu turned up. **Partly novel.**
- **Open data:** `medhallu`.
- **Design sketch:**
  - Score with token probabilities and verifier scores.
  - Report the expected calibration error (ECE) after temperature scaling, fitted on `pqa_artificial` and tested on `pqa_labeled`, plus risk–coverage curves (error rate at 50/80/90% coverage).
  - Compare with the prompted "not sure" option, using a strict parser.
- **Rating:** feasibility 5, novelty 3, a secondary analysis inside Gaps 1–2 (no extra compute).

### Gap 6: Cost and on-prem framing for Indian hospitals

- **Evidence:** the paper reports no cost or latency figures. A hospital in India that checks LLM answers locally (DPDP Act) would use a CPU server or a single small GPU.
- **Novelty check:** Faujdar & Kadvani benchmark CPU detectors outside medicine. No medical or Indian-context study turned up.
- **Design sketch:** report checks per second, and the cost per 1,000 checks, on a CPU-only server and on a single 16–24 GB GPU for each detector. Add a "verifier first, small LLM for the uncertain rest" cascade, evaluated under E2/E3. **No quantisation** (that belongs to `quantised-labmed`).
- **Rating:** feasibility 5, novelty 2 on its own, laptop. Adds deployment value.

## Recommended extension

**Gaps 1 + 2 + 3 + 4 together, with 5 and 6 as secondary analyses:** "Can small open-weight models catch medical hallucinations without the answer key? MedHallu with 2026 sub-10B models and cheap verifiers under realistic PubMed retrieval, with artefact controls and a pathologist-audited lab-medicine subset."

Why this one:
- **It fixes what makes current MedHallu numbers hard to trust.**
  - The oracle abstract (Gap 2) puts large models near ceiling and turns the task into reading comprehension.
  - The length artefact and circular difficulty labels (Gap 3) inflate or bias scores.
  - Unchecked machine-generated labels (Gap 4) leave the ground truth itself uncertain.
  - A study that controls all three and then ranks small models is more useful than another leaderboard row.
- **It is new on each axis checked:**
  - no sub-10B 2026 models or specialist verifiers on MedHallu;
  - no source-excluded retrieval;
  - no length control;
  - no expert label audit.
  - PARALLAX is the nearest work and covers a different detector family.
- **It suits Atul (fit 4/5).** The label audit and lab-medicine error taxonomy need a pathologist, and they shape the paper's clinical message. The engineering is light: short generations from small models, PubMed retrieval, and scikit-learn baselines.
- **It is fully open and cheap:**
  - MedHallu and PubMedQA are MIT and not gated;
  - most models are Apache-2.0 or MIT and not gated;
  - roughly 15–25 GPU-h on RunPod (about US$10–30), no paid API.
- **Main risks:**
  - **Searches incomplete:** arXiv and Semantic Scholar could not be checked today, so rerun them before the protocol.
  - **Retrieval leakage:** handle with the source-PMID exclusion and the date-restricted E3.
  - **Single rater:** add a second rater or a washout re-rate.

Expected time: about 6 weeks to a medRxiv/arXiv (cs.CL) preprint. Candidate zero-APC journals:
- Journal of Biomedical Informatics (`jbi`; methods-heavy NLP; it already publishes medical hallucination detection work);
- International Journal of Medical Informatics (`ijmi`);
- Journal of Medical Systems (`jms`).
