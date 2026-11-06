---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich clinicalbench-labs` to replace it with a full, verified guide.

## Proposed extension (from the register)

Do routine laboratory values change LLM vs ML performance? Extend ClinicalBench (MIMIC-IV mortality, readmission, length of stay) with admission CBC/biochemistry panels

## Why it is new

ClinicalBench inputs had no lab values. Adding structured routine labs tests whether LLMs use numeric lab data as well as gradient boosting, with a lab-only ablation, calibration and an optional small LoRA fine-tune.

## Design

- **Study type:** EHR prediction / LLM vs ML (retrospective cohort)
- **Reporting guideline:** TRIPOD+AI; TRIPOD-LLM
- **Scores:** feasibility 3/5, novelty 4/5

The systematic gap analysis (novelty check per gap, open-data matches, design sketches) has not been done yet.
