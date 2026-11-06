---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich ap-icu-mortality` to replace it with a full, verified guide.

## Proposed extension (from the register)

Acute pancreatitis ICU mortality: reimplement a MIMIC-IV → eICU XGBoost model with a harmonised endpoint, benchmarked against BISAP, SOFA and a parsimonious logistic score

## Why it is new

Preprint develops on 28-day mortality but validates on in-hospital mortality. A harmonised-endpoint validation with ML vs BISAP/SOFA, decision curves and open code is a credible rapid paper, and builds a pancreatitis pipeline reusable for the planned post-ERCP pancreatitis study.

## Design

- **Study type:** Prognostic model replication + external validation
- **Reporting guideline:** TRIPOD+AI
- **Scores:** feasibility 4/5, novelty 3/5

The systematic gap analysis (novelty check per gap, open-data matches, design sketches) has not been done yet.
