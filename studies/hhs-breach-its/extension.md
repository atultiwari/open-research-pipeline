---
enriched: true
---
## Where the field stands (checked 2026-11-06)

Sources read: the full text and both supplements of Jiang, Ross and Bai 2025 (Europe PMC, PMC12079295); the live HHS OCR portal (both tabs, column list and row counts); the VCDB repository (licence, README, data notes); the DPDP Act 2023 and DPDP Rules 2025 in the Gazette of India; and the CERT-In directions of 28 April 2022.

**The HHS breach portal is one of the most analysed open datasets in health security.** The register's plan (extend to 2026, add changepoint models, split by entity type and business associate) is now partly done:
- **Business associates** are covered by Ignatovski, *JMIR Med Inform* 2026 ([doi:10.2196/93588](https://doi.org/10.2196/93588)): 6,612 breaches from 2009 to December 2025, with BA involvement compared across three regulatory periods. It is also covered by Jackman et al., Research Square preprint 2026 ([doi:10.21203/rs.3.rs-9151808/v1](https://doi.org/10.21203/rs.3.rs-9151808/v1)): 6,374 breaches to 2024, providers versus BAs, using OLS and gamma GLMs.
- **Trend models** already exist. Yankson et al., *J Cybersecur Priv* 2025 ([doi:10.3390/jcp5030070](https://doi.org/10.3390/jcp5030070)) fitted ARIMA to hacking breaches. Xu published two 2025 IEEE workshop papers, "Trends in US Healthcare Data Breaches" ([doi:10.1109/icad65464.2025.11114030](https://doi.org/10.1109/icad65464.2025.11114030)) and "Evolving Risks in US Healthcare Breaches" ([doi:10.1109/icdmw69685.2025.00031](https://doi.org/10.1109/icdmw69685.2025.00031)). No abstracts were available, so whether they fit changepoints is unchecked (verify).
- **Ransomware prediction** from portal fields (2019–2025) was done by Sun et al., *ITM Web Conf* 2026 ([doi:10.1051/itmconf/20268401018](https://doi.org/10.1051/itmconf/20268401018)), with logistic regression and random forest. Discrimination was low.
- **Linkage to hospitals** was done by Akumani et al., *Health and Technology* 2026 ([doi:10.1007/s12553-026-01098-3](https://doi.org/10.1007/s12553-026-01098-3)), who linked breaches to US hospitals with confidence scores.
- Older anchors: McCoy and Perlis, *JAMA* 2018 (2010–2017 trends; [PMC6233611](https://pmc.ncbi.nlm.nih.gov/articles/PMC6233611/)); Neprash et al., *JAMA Health Forum* 2022 (376 ransomware attacks on care-delivery organisations, 2016–2021; [PMC9856685](https://pmc.ncbi.nlm.nih.gov/articles/PMC9856685/)).

**What nobody has done:** (1) checked how accurate any ransomware label taken from portal text is; (2) tested whether the apparent fall in ransomware after 2021 is caused by recent cases that have no description yet; (3) translated the HHS evidence into the breach rules of India's DPDP Rules 2025, which were notified in November 2025. The extension moves to these three questions.

**Novelty searches** (all on 2026-11-06):

| # | Source and query | Result |
| --- | --- | --- |
| 1 | OpenAlex, works citing the source (`cites:W4410362603`) | 40 works. Relevant: Jackman 2026 (BA vs provider), Sun 2026 (ransomware prediction), Akumani 2026 (hospital linkage), Holmgren 2025 (EHR consolidation, commentary). None validates a ransomware label or tests the post-2021 decline |
| 2 | OpenAlex title/abstract searches | **Not run: the OpenAlex daily quota was used up** (HTTP 429, reset after about 18 h; the quota is shared with parallel sessions). Europe PMC and Crossref were used instead |
| 3 | Europe PMC: `"data breach*" AND (HHS OR "Office for Civil Rights") AND ("time series" OR interrupted OR changepoint OR "change point" OR joinpoint OR segmented)`, 2018+ | 29 hits. Only Ignatovski 2026 (period comparison by logistic regression) and "Healthcare Data Breaches: Insights and Implications" (*Healthcare* 2020) are relevant. **No interrupted time-series or changepoint study of the portal** |
| 4 | Europe PMC: `"data breach*" AND (health* OR hospital*) AND ransomware` | 231 hits. Reviews, a media-framing review (JMIR 2025), resource-based-view work (HCMR 2025). No classifier validation |
| 5 | Europe PMC: `"data breach*" AND health* AND ("natural language processing" OR "large language model*" OR LLM OR GPT) AND (classif* OR ransomware)` | 172 hits. None classifies breach descriptions |
| 6 | Europe PMC: `"data breach*" AND "business associate*"` | 47 hits. Ignatovski 2026; a 2022 COVID-era entity-type study (*Perspect Health Inf Manag*); for-profit vs non-profit (HIM J 2023) |
| 7 | Europe PMC: `"data breach*" AND health* AND (COVID* OR pandemic) AND (HHS OR OCR OR HIPAA)` | 201 hits. The 2022 COVID entity-type study only; no ITS around March 2020 |
| 8 | Europe PMC: `"data breach*" AND (India OR Indian) AND (health* OR hospital*)`; `"Digital Personal Data Protection" AND (health* OR hospital*)` | 333 and 116 hits. Commentaries on DPDP for psychiatry, radiology AI and dermatology. **No study links breach-notification evidence to the DPDP Rules 2025** |
| 9 | Crossref: "interrupted time series healthcare data breaches HHS"; "change point detection healthcare data breaches" | Xu 2025 ×2 (no abstract); "Predictive Insights Into Healthcare Data Breaches: A Time Series Forecasting Approach" (2024, no abstract); Yankson 2025 (ARIMA). No changepoint paper with an abstract confirming it |
| 10 | Crossref: "classifying ransomware in HIPAA breach reports text" | Nothing relevant |
| 11 | Crossref: "healthcare data breach reporting delay discovery to notification"; "HIPAA breach notification GDPR comparison India" | Notification-law economics papers and a 2024 comparative law review. No health-specific DPDP comparison |
| 12 | Semantic Scholar batch lookup (abstracts of the Xu and Akumani papers) | **Rate-limited (HTTP 429), not checked** |
| 13 | arXiv `all:breach AND all:healthcare` | **Rate-limited (HTTP 429), not checked** (2 calls made) |

### Gap 1: Update to 2026 with formal changepoint and interrupted time-series models

- **Evidence.** The source ends in October 2024 and is descriptive: yearly shares and one P value (Table; Methods). It flags 2024 as incomplete (Table footnote a).
- **Novelty check.** Searches 3, 7 and 9 found ARIMA trend fitting (Yankson 2025), period comparisons (Ignatovski 2026), and two Xu 2025 papers whose methods are unknown. No confirmed changepoint or ITS analysis. But the plain "update plus trend model" is a small step, and Xu may already have done it (verify).
- **Open data:** `hhs-ocr-breach-portal`.
- **Design sketch.** Monthly counts from 2010-01 to 2026-10, by breach category. Use `ruptures` (PELT, with a BIC penalty) and Bai–Perron tests to find breakpoints without fixing them in advance. Then fit segmented negative-binomial models at pre-named policy dates: the Omnibus Rule (September 2013), the WannaCry outbreak (May 2017), the COVID-19 emergency (March 2020), and the Change Healthcare attack (February 2024). Add Fourier terms for seasonality, and run sensitivity analyses that drop mega-breaches. Reporting guideline: RECORD.
- **Rating:** feasibility 5, novelty 2, laptop, 2 weeks. Keep it as the backbone, not the headline.

### Gap 2: Is the post-2021 fall in ransomware real, or an artefact of missing descriptions?

- **Evidence.** The source reports ransomware falling from 31% of breaches in 2021 to 11% in 2024 (Table), while ransomware's share of *records* rose to 69%. Its Methods say that open cases, mostly 2023–2024, had no OCR description and were classified from web searches. The eAppendix counts unclear cases as non-ransomware and calls the estimate a lower bound. So the most recent years are the ones most likely to be under-counted. On the live portal (2026-11-06), the *Under Investigation* tab holds 748 reports from the last 24 months; 87 of the first 100 archived rows have a web description, while open cases are the ones the source had to describe from web searches.
- **Novelty check.** Searches 1, 4, 5 and 10 found no study that validated a ransomware label from breach text, or tested how description availability affects the trend.
- **Open data:** `hhs-ocr-breach-portal` (two dated snapshots); `vcdb` for a label cross-check.
- **Design sketch.**
  - *Hypothesis:* the 2022–2024 fall in ransomware share is smaller, or absent, once 2024 cases have been resolved and described, and once the label is checked for accuracy.
  - *Snapshot comparison:* compare a 2026 export with the paper's published 2024 counts. Re-estimate ransomware share for 2021–2024 among rows that now have descriptions. Model the probability that a row has a description as a function of its age (time since submission).
  - *Reference standard:* a stratified random sample of about 600 Hacking/IT descriptions, oversampling 2020–2026 and borderline regex hits. Atul and a second coder label each one ransomware / not / uncertain from a written codebook, independently. Report Cohen's κ.
  - *Index classifiers:* (a) the source's regex rules, rebuilt from the eAppendix; (b) a keyword baseline; (c) a small open-weight LLM run locally with a fixed prompt, temperature 0, and a pinned model version. Optionally, (d) the VCDB `action.malware.variety` label where the incident is in VCDB.
  - *Metrics:* sensitivity, PPV and F1 with 95% CIs, by year group. Then a misclassification-corrected ransomware trend, using the Rogan–Gladen correction or multiple imputation from the validation sample.
  - *Reporting guideline:* RECORD for the trend analysis; TRIPOD-LLM items for the LLM classifier, with STARD-style accuracy tables.
- **Rating:** feasibility 5, novelty 4, laptop, about 3 weeks (labelling takes most of the time).

### Gap 3: How concentrated are the harms? Mega-breaches and business-associate cascades

- **Evidence.** The source's Figure B shows that totals swing with single events (Anthem 2015; Change Healthcare 2024). It measures only records affected, and its Discussion says this misses operational disruption.
- **Novelty check.** BA involvement is covered by Ignatovski 2026 and Jackman 2026 (searches 1 and 6). Heavy-tail measures (top-1% share, Gini, power-law or log-normal fit) were not found in searches 3 and 9, but these are a minor addition.
- **Design sketch.** Lorenz curves and the top-10 share of records by year. Fit extreme-value or log-normal tails. Group rows that share a submission date, the same business associate, and the same description into one incident, and compare counts of reports with counts of incidents.
- **Rating:** feasibility 5, novelty 2, laptop, 1 week. Use it as a secondary analysis inside Gap 1.

### Gap 4: Clinical laboratories and diagnostic providers as a subgroup

- **Evidence.** The source groups all covered entities together. Laboratories and diagnostic services hold large volumes of results and are often reached through billing and collection vendors. That makes them a natural subgroup for a pathologist author.
- **Novelty check.** Searches 3–6 found no laboratory or diagnostic subgroup analysis of the portal.
- **Design sketch.** Flag entities by name and description (laboratory, pathology, diagnostic, imaging, radiology, genetic testing), hand-check every flagged row, and compare breach type, BA involvement, ransomware share and records affected with other providers. The subgroup may be small (verify the count after flagging).
- **Rating:** feasibility 4, novelty 3, laptop, 1 week on top of Gap 2.

### Gap 5: What would HHS-style evidence look like under India's DPDP Rules 2025?

- **Evidence.** The register asked for DPDP lessons. The legal texts, checked in the Gazette:
  - DPDP Act 2023, [Gazette of India, 11 August 2023](https://egazette.gov.in/WriteReadData/2023/248045.pdf). Section 2(u) defines a personal data breach to include loss of access, which covers ransomware. Section 8(5) requires reasonable security safeguards. Section 8(6) requires the Data Fiduciary to tell the Data Protection Board **and each affected Data Principal** about every breach. There is no size threshold. In the Schedule, failing to notify can draw a penalty of up to ₹200 crore, and failing to keep safeguards up to ₹250 crore.
  - DPDP Rules 2025, G.S.R. 846(E), [Gazette of India, 13 November 2025](https://egazette.gov.in/WriteReadData/2025/267650.pdf). Rule 7(1): tell each affected person without delay, giving the nature of the breach, likely consequences, mitigation, protective steps and a contact. Rule 7(2): tell the Board without delay, then send a detailed report within 72 hours (the Board can allow longer), covering causes, mitigation, any findings about who caused it, and the notices sent to individuals. Rule 6 sets minimum safeguards, including logs kept for one year. Under Rule 1(4), Rules 6 and 7 come into force 18 months after publication, so in mid-May 2027. Check the companion notice that brings section 8 of the Act into force (verify).
  - Alongside these, the CERT-In directions under section 70B of the IT Act (No. 20(3)/2022-CERT-In, [28 April 2022](https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf)) already require reporting listed cyber incidents to CERT-In within 6 hours, and keeping logs for 180 days.
  - Neither regime creates a **public** breach register like the HHS portal, so Indian researchers will have no equivalent dataset.
- **Novelty check.** Search 8 found commentaries on DPDP for clinical specialties, but no study using breach data to set DPDP priorities.
- **Design sketch.** A structured policy comparison set out as a table, against 45 CFR 164.400–414: threshold, clock, recipients, content, public listing, penalties, and the role of business associates versus Data Processors. Use the Gap 1–3 results to argue for specific points: (i) a public register of large breaches, because HHS data show that a register is what makes trends like these measurable; (ii) a mandatory ransomware or loss-of-availability field, which the source's authors also asked HHS for; (iii) processor-level reporting, given the BA cascades. Frame this for Indian hospitals and laboratories, including ABDM-linked systems (verify the current ABDM breach guidance before writing).
- **Rating:** feasibility 5, novelty 3 as a discussion section, laptop, 1 week. It adds most when built into Gap 2.

## Recommended extension

**Gap 2 as the headline, with Gap 1 as the modelling backbone, Gap 4 as a planned laboratory subgroup, and Gap 5 as the policy discussion:** "Is healthcare ransomware really declining? Validated ransomware classification of US HHS breach reports 2010–2026, changepoint analysis, and lessons for India's DPDP breach rules."

Why this one:
- It is the only question here that the searches show nobody has asked. BA trends (Ignatovski 2026, Jackman 2026), ARIMA trends (Yankson 2025) and ransomware prediction (Sun 2026) are taken. The accuracy of the ransomware label, and the artefact explanation for the post-2021 decline, are not.
- It turns the source's own caveats (open cases, unclear cases counted as negative, a lower-bound estimate) into a testable hypothesis, with a reference standard and corrected trend estimates.
- All data are open, with no registration. VCDB is CC BY-SA, so share only aggregates. A laptop is enough.
- The expert labelling and the laboratory subgroup use Atul's clinical judgement. It is a classifier-validation problem, much like diagnostic accuracy studies in pathology.
- The DPDP angle is timely: Rule 7 comes into force in May 2027, so Indian hospitals are setting up breach processes now.

Main risks: (1) one or both Xu 2025 papers may already contain changepoint models; this does not affect the Gap 2 headline. (2) The source's exact October 2024 labels cannot be obtained, so the artefact test relies on comparing published aggregates with a new snapshot. (3) Labelling about 600 descriptions needs a second coder.

Expected time: about 5 weeks to a preprint. Best-fit zero-APC journals: *Health Policy and Technology*, *Journal of Medical Systems*, *Health and Technology*.
