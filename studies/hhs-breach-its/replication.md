---
enriched: true
---
## What the original study did

Jiang, Ross and Bai (Michigan State, Yale, Johns Hopkins) published a short research letter in *JAMA Network Open* on 14 May 2025 ([doi:10.1001/jamanetworkopen.2025.10180](https://doi.org/10.1001/jamanetworkopen.2025.10180), CC BY 4.0; open copy [PMC12079295](https://pmc.ncbi.nlm.nih.gov/articles/PMC12079295/)). It is a cross-sectional study (STROBE) of every breach of 500 or more records reported to the HHS Office for Civil Rights (OCR) from October 2009 to 31 October 2024. After removing duplicates and incomplete rows, 6,468 breaches remained, grouped by the year they were reported. The OCR portal has no ransomware field, so the authors flagged ransomware inside the "Hacking/IT Incident" category. They used a rule-based Python script (regular expressions) on the OCR case descriptions, and on web or news searches for open cases that had no OCR description, mostly from 2023–2024. The eAppendix lists the rules: words like "ransom", cryptocurrency, encryption or "locked" systems, extortion wording, and names of known ransomware groups, with negation filters. Unclear cases were counted as not ransomware. The analysis was descriptive: yearly counts, shares, and records affected, run in SAS 9.4. The paper reports no accuracy check of the ransomware classifier, and no trend or changepoint model beyond a single P value for the rise in hacking.

**Directly replicable on open data, with one caveat.** The breach list is public and needs no registration. But the authors did not share their script or their ransomware labels; their data-sharing statement says no. The web-search descriptions they added for open cases are not in any public file either. A replication therefore rebuilds the classifier from the eAppendix rules and will not match exactly for 2023–2024.

## Data

| Dataset | What | Access | How to get it |
| --- | --- | --- | --- |
| `hhs-ocr-breach-portal` | HIPAA breaches affecting 500+ individuals. On 2026-11-06: 748 under investigation plus 7,329 archived = 8,077 rows. Columns: entity, state, entity type, individuals affected, submission date, breach type, location, business associate present, web description | Open; US federal government work; no registration | Open the [portal](https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf) and choose "View HIPAA Breach Reports". Use **Export as CSV** on the *Under Investigation* tab, then switch to the *Archive* tab and export again. The export is a JSF post-back, so do it by hand in a browser. Save both files with the download date in the file name, outside the repo |
| `vcdb` (optional cross-check) | VERIS-coded public incidents, with healthcare incidents chosen on purpose (`plus.sub_source = "phidbr"`) | Open, CC BY-SA 4.0 | `git clone --depth 1 https://github.com/vz-risk/VCDB` and use `data/joined/vcdb.json.zip` (about 4.6 MB). Record the commit hash |

**Legal anchors for the reporting rules:** the HIPAA Breach Notification Rule is in 45 CFR 164.400–414 ([eCFR, part 164 subpart D](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-D)). Breaches of 500 or more must reach HHS within 60 days of discovery. Smaller ones are logged each year and are not listed publicly.

**Storage:** both CSV exports together are a few MB. Keep them in `data/raw/<YYYY-MM-DD>/` (gitignored). The portal is updated continuously, so each export is a different dataset; never overwrite an old snapshot.

## Environment

- Python 3.10+ with `pandas`, `numpy`, `statsmodels` (segmented Poisson or negative-binomial regression), `ruptures` (changepoint detection), `scipy`, `matplotlib`, `regex`. R users: `segmented`, `strucchange`, `MASS::glm.nb`.
- No GPU. A laptop is enough. The optional LLM step in the extension runs a small open-weight model locally (for example through Ollama) or calls a hosted API for a few US dollars.
- There is no source code to copy, so write everything from the eAppendix description.

## Step-by-step replication

1. **Download** both portal tabs as CSV on the same day. Write `provenance.json` with the date, row counts per tab, and file hashes.
2. **Combine and clean.** Stack the two tabs and parse dates. Remove exact duplicates (same entity, state, date and count) and rows missing key fields. Log every rule you apply. Limit to submission dates from 2009-10-01 to 2024-10-31 to match the paper.
3. **Year and category.** Year = year of the *breach submission date*, as in the paper. Map OCR breach types to the paper's five groups: ransomware hacking/IT, non-ransomware hacking/IT, theft, unauthorised access/disclosure, and improper disposal/loss/other/unknown. Rows listing several types need a written rule; for example, any row that includes Hacking/IT goes to hacking.
4. **Rebuild the ransomware rules** from the eAppendix. Two tiers: (a) "ransom"/"ransomware" without negation; (b) cryptocurrency, encryption or "locked" wording, extortion wording that excludes regulatory terms, and named groups (LockBit, BlackCat/ALPHV, Conti, Ryuk, REvil, DarkSide, Hive, Clop, RansomHub). Apply them only to Hacking/IT rows. Count "uncertain" as not ransomware. Keep the rules in one versioned file.
5. **Descriptions for open cases.** The paper added news descriptions for open cases. For a faithful replication, record for each row whether it has an OCR web description. Report results with and without the open cases. Do not scrape news sites at scale; if you add any by hand, log the source URL.
6. **Tabulate** breaches and records affected per year and category, as in the paper's Table and Figure panels A and B. Add a trend test for the share of hacking (for example a Cochran–Armitage test or a binomial GLM on year).
7. **Compare** each cell with the targets below and explain any difference over 5%. Expect larger differences for 2023–2024, because rows have been revised and moved to the archive since October 2024.

## Compute and cost

A laptop, under an hour of processing, US$0. Manual work: about half a day to download, clean and check the rules.

## Target numbers

From the paper's Table (2024 covers January–October only):
- 6,468 unique breaches, 2010–2024. Hacking/IT rose from 8 of 216 breaches (4%) in 2010 to 457 of 566 (81%) in 2024.
- Ransomware: 0 in 2010; a peak of 222 of 715 breaches (31%) in 2021; 61 of 566 (11%) in 2024. Total 1,090 ransomware breaches.
- Records affected: about 732 million in total, of which hacking/IT accounted for about 643 million (88%) and ransomware about 285 million (39%). Ransomware's share of records was above half every year from 2020 (51%, 44% in 2021, 51%, 51%) and 69% in 2024.
- The 2015 spike in records comes from the Anthem breach (about 79 million records).

## Known pitfalls

- **Moving target.** Rows move from *Under Investigation* to *Archive*, individuals-affected counts are revised (for example Change Healthcare, which the paper cites at 100 million), and some rows disappear. The paper's October 2024 snapshot cannot be rebuilt exactly. Report your snapshot date in every table.
- **Missing descriptions bias recent years.** Open cases often have no OCR description, so a text classifier will miss ransomware in the most recent 24 months. This may explain part of the paper's 2024 "decline" (see the extension, Gap 2).
- **Reporting year is not breach year.** HIPAA allows 60 days, and many entities report late. Mega-breaches are sometimes split into many rows, one per covered entity, when a business associate is hit. Decide whether to count incidents or reports, and say which.
- **Records are not people.** The same person can appear in several breaches. The paper adds up records, and so should you when replicating, but label it as records.
- **No small breaches.** Breaches under 500 records are never listed, so all counts are lower bounds.
- **Regex brittleness.** Words like "locked" or "encrypt" also appear in defensive phrases ("the laptop was encrypted"). The eAppendix negation rules are only described, not given, so your false-positive rate will differ.
- **VCDB is not independent.** Its healthcare stream is selected from, and largely coded from, the same HHS reports. Do not call it external validation.
- **Licences.** The portal data are a US government work. VCDB is CC BY-SA 4.0, so any adapted VCDB file you share must keep that licence. Commit only aggregate tables.
- **Defensive scope.** Report categories, counts and dates only. Do not compile ransomware gang tooling, ransom notes or leak-site content.

## Claude Code task list

1. Create `analysis/hhs-breach-its/` in a separate analysis repo, with `data/` gitignored.
2. Ask Atul to export both portal tabs (Under Investigation and Archive) as CSV and save them under `data/raw/<date>/`. Write `provenance.json`.
3. `clean.py`: stack, deduplicate, parse dates, and map breach types to the five groups. Write `data/clean/breaches.parquet` and a cleaning log.
4. `ransomware_rules.py`: the eAppendix two-tier regex classifier, with unit tests on about 30 hand-written example descriptions (no real ransom notes).
5. `replicate.py`: yearly Table and Figure A/B. Write `results/replication_table.csv` (aggregate only) and figures.
6. `compare_targets.py`: cell-by-cell comparison with the paper; flag differences over 5%.
7. Write `results/replication.md` summarising the match, the snapshot date, and the share of rows without an OCR description by year.
