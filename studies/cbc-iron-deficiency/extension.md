---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich cbc-iron-deficiency` to replace it with a full, verified guide.

## Proposed extension (from the register)

Predicting iron deficiency (low ferritin) from routine CBC: develop on NHANES, externally validate on an open Yemeni hospital dataset; logistic regression, XGBoost and TabPFN vs zero/few-shot LLMs

## Why it is new

Source used a private single-centre dataset with no code. Adds a fully open pipeline, external validation in an LMIC hospital population relevant to India's anaemia burden, LLM and TabPFN head-to-head, pathologist check against Mentzer/MCH logic, and decision-curve analysis.

## Design

- **Study type:** Diagnostic prediction model + external validation; LLM vs ML
- **Reporting guideline:** TRIPOD+AI (+TRIPOD-LLM); STARD-AI elements
- **Scores:** feasibility 5/5, novelty 3/5

The systematic gap analysis (novelty check per gap, open-data matches, design sketches) has not been done yet.
