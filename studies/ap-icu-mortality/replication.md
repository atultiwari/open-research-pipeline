---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich ap-icu-mortality` to replace it with a full, verified guide.

## What the original study did

*Development and external validation of a metabolic-clinical XGBoost model for mortality prediction in acute pancreatitis* (Research Square, 2026-08-28). [Source](https://www.researchsquare.com/article/rs-10464724).

## Data

- **Datasets:** MIMIC-IV (AP ICU) + eICU-CRD
- **Access:** credentialed/DUA (PhysioNet + CITI)
- **Main link:** https://physionet.org/content/eicu-crd/2.0/

## Code

None; reimplementable (LASSO → 14-feature XGBoost, isotonic calibration, SHAP)

## Compute

Laptop; about 5 weeks to a preprint (register estimate).

## Notes from the register

Shares PhysioNet credential with the cirrhosis study. No open post-ERCP pancreatitis dataset exists. Frame as independent validation.
