---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich fairness-tcga-cptac` to replace it with a full, verified guide.

## Proposed extension (from the register)

Do newer foundation models reduce demographic performance gaps? Race-, age- and site-stratified audit of UNI2-h MIL on TCGA with CPTAC external validation

## Why it is new

Original used older encoders and private MGB data for breast and lung tasks. Rebuilds the tasks fully on open TCGA (train) and CPTAC (external) with UNI2-h, reports disparity by race, age and submitting site, and tests whether site-stratified splits shrink apparent bias.

## Design

- **Study type:** Fairness / subgroup analysis + external validation
- **Reporting guideline:** TRIPOD+AI / CLAIM 2024
- **Scores:** feasibility 4/5, novelty 4/5

The systematic gap analysis (novelty check per gap, open-data matches, design sketches) has not been done yet.
