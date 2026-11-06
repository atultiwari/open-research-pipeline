---
enriched: true
---
## Where the field stands (checked 2026-11-06)

Predicting low ferritin from a blood count is a **crowded** topic. Several 2024–2026 papers already cover parts of the register's plan:
- **Multi-site and deployed models.** Chang et al., *Clin Chem* 2025 ([doi:10.1093/clinchem/hvaf074](https://doi.org/10.1093/clinchem/hvaf074)): CBC plus cell-population data from 3 Taiwanese hospitals, AUROC > 0.94, deployed in the lab system. Kurstjens et al., *CCLM* 2022 ([doi:10.1515/cclm-2021-1194](https://doi.org/10.1515/cclm-2021-1194)): CBC + CRP in anaemic primary-care patients, AUC 0.90–0.92; the algorithm beat 12 laboratory specialists.
- **CBC-only models in large EHR cohorts.** Efros et al., *BMJ Open* 2025 ([doi:10.1136/bmjopen-2024-097016](https://doi.org/10.1136/bmjopen-2024-097016)): iron deficiency without anaemia, 211,486 patients; CBC-only AUC 0.741. Us et al., *BMC Med Inform Decis Mak* 2026 ([doi:10.1186/s12911-026-03601-2](https://doi.org/10.1186/s12911-026-03601-2)): an ANN with AUC 0.837, after excluding inflamed cases.
- **NHANES development with LMIC validation already exists, but for iron-deficiency *anaemia*.**
  - Pullakhandam and McRoy, *BioMedInformatics* 2024 ([doi:10.3390/biomedinformatics4010036](https://doi.org/10.3390/biomedinformatics4010036)): NHANES (> 19,000 instances), validated on Kenyan data from the same Omuse et al. study registered here as `kenya-ifcc-iron`.
  - Palika et al., *Indian J Med Res* 2026 ([doi:10.25259/ijmr_1500_2025](https://doi.org/10.25259/ijmr_1500_2025)): NHANES 2017–2023 women aged 15–50 (n = 3,604), inflammation-adjusted IDA, random forest, validated on 381 Indian women. Reports ~95% sensitivity and specificity.
  - Both labels need low Hb, and Hb is also an input, so part of the answer is in the features.
- **Indian CBC-only model.** Sarma et al., *Sci Rep* 2026 ([doi:10.1038/s41598-026-64184-6](https://doi.org/10.1038/s41598-026-64184-6); preprint [doi:10.21203/rs.3.rs-10075784/v1](https://doi.org/10.21203/rs.3.rs-10075784/v1)): north-east India, 1,122 adults, penalised LR with AUC 0.82 (ferritin < 30) and 0.90 (< 15); internal validation only.
- **NHANES used to validate a child CBC model.** Guo et al., *Br J Nutr* 2026 ([doi:10.1017/s0007114526107168](https://doi.org/10.1017/s0007114526107168)): MCH + RDW in Chinese children, externally validated on NHANES 2021–23 children (n = 232).
- **LLMs on lab data.** Yesil et al., *Lab Med* 2026 ([doi:10.1093/labmed/lmag074](https://doi.org/10.1093/labmed/lmag074)): XGBoost beat three API LLMs (holdout AUC 0.880 vs 0.73–0.74) at classifying ICD-10 groups from routine panels, in only 80 holdout patients. Ye et al., *JMIR* 2026 ([doi:10.2196/87802](https://doi.org/10.2196/87802)): GPT-5, Grok 4 and DeepSeek R1 interpreting 100 CBC reports, rated by experts. **No paper was found that compares zero/few-shot LLMs with ML and TabPFN for predicting low ferritin from a CBC.**
- **Ferritin thresholds are being re-examined in NHANES.** Mei et al., *Blood Red Cells & Iron* 2026 ([doi:10.1016/j.brci.2025.100029](https://doi.org/10.1016/j.brci.2025.100029)): physiologically based thresholds in US adolescents and adults. Dugan et al., same journal, 2026 ([doi:10.1016/j.brci.2026.100152](https://doi.org/10.1016/j.brci.2026.100152)): alternative thresholds in US adults. The threshold values were not read (no abstract available, `verify`).

So "CBC → low ferritin with ML" and "NHANES → LMIC validation" are not new. What is still open:
- LLMs and TabPFN head-to-head with honest baselines;
- a ferritin-only label without Hb leakage, across men, women and older adults (only 2017–2020 NHANES allows this);
- inflammation-aware and physiological ferritin labels;
- survey-weighted calibration and net benefit in two external populations.

**Novelty searches** (2026-11-06). Hit lists are saved in the scratchpad (`novelty_epmc.txt`).

| # | Source and query | Result |
| --- | --- | --- |
| 1 | OpenAlex `cites:W7165182315` (works citing the JCM paper) | 1 hit: Iftikhar et al., *Systems and Soft Computing* 2026 ([doi:10.1016/j.sasc.2026.200680](https://doi.org/10.1016/j.sasc.2026.200680)), explainable ML for IDA from CBC. No abstract available, so its dataset is `verify` |
| 2 | OpenAlex `search=` (7 queries: iron deficiency ML CBC; NHANES ferritin ML; LLM iron deficiency; LLM CBC; TabPFN laboratory; external validation; Yemen) | **Rate-limited, not checked**: the shared daily OpenAlex budget was used up (HTTP 429). Replaced by Europe PMC and Crossref (rows 4–9) |
| 3 | Semantic Scholar citations of `DOI:10.3390/jcm15124783` | 1 citing paper (the same Iftikhar 2026) |
| 4 | Europe PMC, title search: (iron deficiency OR ferritin OR iron status) AND (machine learning OR AI OR XGBoost OR prediction), 2021–2026 | Us 2026; Palika 2026; Chang 2025; Efros 2025; Adabor 2025 (BamClassifier, Ghana); Tepakhan 2025 and others on IDA vs thalassaemia |
| 5 | Europe PMC abstract search: NHANES AND (ferritin OR iron deficiency) AND (ML terms), 2018–2026 | 9 hits; only Palika 2026 predicts iron status from CBC |
| 6 | Europe PMC abstract search: (large language model OR GPT-4 OR ChatGPT OR LLM) AND (ferritin OR iron deficiency), 2023–2026 | 5 hits, none predicting ferritin (one LLM protocol tool for anaemia in haemodialysis) |
| 7 | Europe PMC title search: LLM terms AND (laboratory OR blood count OR haematology OR anaemia OR iron), 2023–2026 | Yesil 2026 (*Lab Med*), Ye 2026 (*JMIR*); exam-style benchmarks; nothing on ferritin |
| 8 | Europe PMC abstract search: (TabPFN OR tabular foundation model) AND (anaemia OR ferritin OR iron deficiency OR blood count OR haematology) | 4 hits: TabPFN for mortality using ferritin as an input, ITP, COVID, colorectal-cancer CBC screening. **None predicts iron status** |
| 9 | Europe PMC abstract search: ferritin/ID AND ML AND (decision curve OR calibration) AND CBC | 0 hits |
| 10 | Europe PMC abstract search: ferritin/ID AND ML AND (Sysmex OR Beckman OR analyser) AND (transportability OR external validation) | 1 hit (Guo 2026, children); no analyser-transfer study |
| 11 | Europe PMC abstract search: ferritin/ID AND ML AND CBC AND (India OR LMIC OR Africa OR Yemen) | Palika 2026; Sarma 2026 preprint; a 2022 *PLoS One* anaemia classifier |
| 12 | Europe PMC preprints (`SRC:PPR`): ferritin/ID AND (ML OR language model OR XGBoost), 2023–2026 | 22 hits; the source preprint itself; no LLM or TabPFN ferritin preprint |
| 13 | Crossref bibliographic query `large language model iron deficiency ferritin complete blood count` (2023+) | Sarma 2026 (*Sci Rep*), Pullakhandam 2024, Mei 2026, Dugan 2026; no LLM ferritin paper |
| 14 | arXiv `all:"iron deficiency" AND (all:"language model" OR all:TabPFN OR all:"blood count")` (2 attempts, ≥ 5 s apart) | **Rate-limited ("Rate exceeded"), not checked** |
| 15 | DataCite dataset search: ferritin AND haemoglobin AND (MCV OR blood count) | Yemeni Mendeley set; a Mendeley hepcidin/ACD set (not checked); the Kenya Figshare set was found through Pullakhandam's references |

### Gap 1: No external validation, and a private single-centre cohort

- **Evidence.** The Discussion says all data came from one institution, that external cohorts on different analysers are needed, and that the cohort was selected (only patients who had iron studies ordered). Data are on request, and there is no code.
- **Novelty check.** Rows 4, 5, 11 and 13. Multi-site and external validation exist (Chang 2025, Kurstjens 2022, Pullakhandam 2024, Palika 2026). Simply "validating a CBC model externally" is **not new**.
- **Open data:**
  - `nhanes`: 2017–March 2020 for development; 2021–23 for temporal validation (women 12–49 only);
  - `kenya-ifcc-iron`: healthy adults, Beckman analyser, altitude 1,700–2,100 m;
  - the Yemeni Mendeley set is excluded (de-identification concerns; see Gap 6).
- **Design.** Develop on NHANES with the source's nine inputs. Lock the models. Validate on NHANES 2021–23 (temporal) and Kenya (geographic, LMIC) without refitting. Report discrimination, calibration slope and intercept, and calibration plots. Then apply recalibration-in-the-large and report it separately. Reporting guideline: TRIPOD+AI.
- **Rating:** feasibility 5, novelty 2, laptop, 2–3 weeks. Necessary as a base, not enough on its own.

### Gap 2: LLMs and a tabular foundation model have not been compared with classical ML for this task

- **Evidence.** The source compares only classical classifiers. Its authors used an LLM (Claude via GitHub Copilot) only for code review. LLMs are increasingly asked to "read" CBC reports (Ye 2026). TabPFN (Hollmann et al., *Nature* 2025, [doi:10.1038/s41586-024-08328-6](https://doi.org/10.1038/s41586-024-08328-6)) claims strong small-data tabular performance, which matters for the 528-person Kenyan set.
- **Novelty check.** Rows 6, 7, 8, 12, 13 and 14 (arXiv not checked). Yesil 2026 compared LLMs with XGBoost on lab panels, but for ICD codes in 80 patients. **No study compares zero/few-shot LLMs, TabPFN and ML for low ferritin from a CBC.**
- **Open data:** `nhanes`, `kenya-ifcc-iron`.
- **Design.**
  - *Hypothesis:* zero-shot LLMs rank low-ferritin risk worse than a spline LR. Few-shot prompts and haematology-rule prompts narrow the gap. TabPFN matches XGBoost on NHANES and transfers better to Kenya.
  - *Arms:*
    - pathologist rules: MCH < 27 pg, MCV < 80 fL, Mentzer index, RDW;
    - spline LR;
    - XGBoost;
    - TabPFN (≤ 10,000 training rows, `verify` the current limit);
    - two LLMs: one small open-weight model run locally, and one API model;
    - each LLM zero-shot, few-shot (k = 8 or 16 labelled examples) and with a rule-guided prompt.
  - LLMs output a probability (0–100) and a label at temperature 0. Repeat 3 times to measure stability.
  - Use the same locked test sets for every arm. Send no NHANES or Kenyan rows to an API whose terms allow training on inputs; the NCHS agreement forbids linkage, not analysis, but check the API terms (`verify`).
  - *Metrics:* AUC with DeLong CIs, calibration, Brier score, net benefit, invalid-output rate, cost per 1,000 predictions.
  - *Reporting guideline:* TRIPOD-LLM, plus TRIPOD+AI for the ML arms.
- **Rating:** feasibility 4 (API cost and prompt engineering), novelty 4, API (~USD 20–60, `verify` current prices), 3–4 weeks.

### Gap 3: Is boosting really needed? An honest baseline check

- **Evidence.** The source's LR AUC of 0.663 against XGBoost's 0.858 (Table 1) is much wider than gaps reported elsewhere (Efros 2025: CBC-only 0.741; Sarma 2026: penalised LR 0.82). The LR had linear terms only, while the label uses sex-specific cut-offs (replication pitfall 1). There was no comparison with simple haematology rules that pathologists already use.
- **Novelty check.** Rows 4 and 9. CBC-index rules (Mentzer and similar) are compared with ML mainly for **IDA vs thalassaemia trait**, not for low ferritin in general. No calibration or decision-curve comparison was found (row 9: 0 hits).
- **Open data:** `nhanes`, `kenya-ifcc-iron`.
- **Design.** On the same locked splits, compare:
  - single indices (MCH, MCV, RDW, Mentzer);
  - LR with linear terms (as in the source);
  - LR with restricted cubic splines and an age × sex interaction;
  - XGBoost.

  Report ΔAUC with CIs, calibration, and **decision curves framed as test utilisation**: ferritin tests ordered per extra iron-deficient person found, at threshold probabilities of 10–40%.
  Reporting guideline: TRIPOD+AI.
- **Rating:** feasibility 5, novelty 3, laptop, 1–2 weeks. Strong fit for a pathologist.

### Gap 4: The label itself (ferritin cut-off, inflammation, and Hb leakage in related work)

- **Evidence.**
  - The source uses < 30 µg/L in women and < 50 µg/L in men and has no CRP (limitations paragraph).
  - Palika 2026 and Pullakhandam 2024 predict IDA, which includes low Hb, from inputs that include Hb (replication pitfall 8).
  - NHANES papers are now proposing new ferritin thresholds (Mei 2026; Dugan 2026).
- **Novelty check.** Rows 5, 11 and 13. Palika adjusted for inflammation, but for IDA in women only. No paper was found that measures how CBC-model performance changes across ferritin definitions in men, women and older adults, or that quantifies the inflation caused by Hb leakage.
- **Open data:**
  - `nhanes`: hs-CRP; sTfR in TFR_J (2017–18) for a body-iron sensitivity label;
  - `kenya-ifcc-iron`: hs-CRP, TSAT, transferrin.
- **Design.** Re-fit and re-validate under each of these labels:
  - (a) source sex-specific 30/50;
  - (b) < 15 µg/L;
  - (c) < 30 µg/L;
  - (d) inflammation-aware: a higher cut-off when hs-CRP > 5 mg/L, using a published rule (WHO 2020 ferritin guideline or BRINDA regression correction; cite the exact rule, `verify`);
  - (e) the physiological threshold from Mei 2026 (`verify` the value);
  - (f) IDA (low ferritin and low Hb), with and without Hb among the inputs, to show the leakage.

  Report a "specification curve" of AUC and calibration across labels and subgroups (sex, age ≥ 65, CRP > 5). Reporting guideline: TRIPOD+AI (and STARD for the reference-standard discussion).
- **Rating:** feasibility 5, novelty 3, laptop, 1–2 weeks. Pathologist home ground: it is about what "iron deficient" means in the lab.

### Gap 5: Analyser transportability (Sysmex vs Beckman)

- **Evidence.** The source names analyser heterogeneity as a reason for external validation. NHANES (DxH 800) and Kenya (ACT 5 DIFF) both use Beckman instruments; Verona used a Sysmex XN.
- **Novelty check.** Row 10: nothing found on transferring ferritin-prediction models between analysers.
- **Open data.** No open dataset has paired Sysmex and Beckman counts with ferritin. Only an indirect test is possible: refit without RDW and MCHC (the least harmonised indices) and see how much accuracy is lost, and whether external calibration improves.
- **Rating:** feasibility 3, novelty 3, laptop, 1 week as a sensitivity analysis inside the main study. A full analyser study would need private paired data.

### Gap 6 (on hold): Yemeni hospital validation

- **Evidence.** This was the register's planned external set: an LMIC hospital population with heavy anaemia.
- **Problem.** The dataset was excluded: de-identification and data-quality concerns found on 2026-11-06, pending clarification with the depositors. It also has undeclared duplicates, implausible values and an extreme case mix (heavy anaemia, many very high ferritin values), with no RDW or MCHC. **Do not use it unless Atul clears it**, and even then only as a stress test.

## Recommended extension

**Gaps 2 + 3 + 4, built on Gap 1.** Working title: *Can a routine blood count tell who needs a ferritin test? Zero/few-shot LLMs, TabPFN and classical models against haematology rules: survey-weighted development on NHANES 2017–March 2020 with temporal (NHANES 2021–23) and Kenyan external validation.*

1. Replicate the source method on NHANES 2017–March 2020 (replication.md). This is the only recent cycle with ferritin in men and older adults.
2. Compare pathologist rules, linear and spline LR, XGBoost, TabPFN and two LLMs (zero-shot, few-shot, rule-guided) on the same locked splits (Gaps 2 and 3).
3. Repeat across ferritin definitions, including inflammation-aware and physiological cut-offs, and show how IDA labels with Hb inputs inflate accuracy (Gap 4).
4. Validate without refitting on NHANES 2021–23 (women 12–49, `WTPH2YR`) and on Kenyan healthy adults. Report calibration and decision curves as ferritin tests saved per missed deficient person (Gap 1). Include an RDW/MCHC-free sensitivity model (Gap 5).

**Why this one:**
- **Novelty.** NHANES-based CBC models and NHANES → Kenya/India validation already exist, so the novelty is the LLM/TabPFN head-to-head with honest rule baselines and the label analysis. No paper fills that combination.
- **Fit for a pathologist.** The rule baselines, the definition of iron deficiency, inflammation, analyser effects and the "test utilisation" framing are laboratory-medicine questions that ML-only groups usually skip.
- **Feasibility.** All data are open with no registration: NHANES (a few tens of MB) and a 50 KB Kenyan file. It runs on a laptop, plus a small API budget.
- **Speed and journals.** About 5–6 weeks to a preprint. Good fits on the zero-APC list: *Computer Methods and Programs in Biomedicine* (`cmpb`), *International Journal of Medical Informatics* (`ijmi`) and *Journal of Medical Systems* (`jms`). A haematology or laboratory-medicine journal (e.g. *Clinical Chemistry and Laboratory Medicine*) would also fit, but none is on the shortlist yet (`verify` its APC route before adding it).

**Rating:** feasibility 5 (4 for the LLM arm), novelty 3 (the field is crowded; 4 for the LLM/TabPFN arm alone), fit 5, API tier, 6 weeks.
