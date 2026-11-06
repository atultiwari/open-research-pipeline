---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich clinicalbench-labs` to replace it with a full, verified guide.

## What the original study did

*ClinicalBench: Can LLMs Beat Traditional ML Models in Clinical Prediction?* (arXiv (v2; KDD'26 per repo), 2026-06-08). [Source](https://arxiv.org/abs/2411.06469).

## Data

- **Datasets:** MIMIC-IV v2.2 (hosp module incl. labevents)
- **Access:** credentialed/DUA (PhysioNet + CITI training, ~1–2 weeks)
- **Main link:** https://physionet.org/content/mimiciv/2.2/

## Code

https://github.com/canyuchen/ClinicalBench

## Compute

RunPod (~40–80 GPU-h); XGBoost on laptop; about 8 weeks to a preprint (register estimate).

## Notes from the register

Use MIMIC-IV v2.2 to match shipped split indices. MIMIC data cannot go to external APIs under the DUA: local open-weight models only. Start credentialing now. Cite ClinicRealm (arXiv 2407.18525).
