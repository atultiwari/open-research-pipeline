---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich cbc-iron-deficiency` to replace it with a full, verified guide.

## What the original study did

*Predicting Iron Deficiencies Using Routine Complete Blood Cell Count Parameters: A Machine Learning Approach and Evaluation* (Preprints.org, 2026-04-02). [Source](https://www.preprints.org/manuscript/202604.0073).

## Data

- **Datasets:** NHANES 2017–18 CBC_J, FERTIN_J, FETIB_J; external: Mendeley Yemeni hospital set (n=1,998, CC BY 4.0, DOI 10.17632/dmktk7t677.1)
- **Access:** open
- **Main link:** https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/FERTIN_J.htm

## Code

None; reimplementable (sklearn/xgboost)

## Compute

Laptop; API (~USD 10–30) for the LLM arm; about 4 weeks to a preprint (register estimate).

## Notes from the register

Restrict external model to shared features (Hb, RBC, Hct, MCV, MCH, WBC, platelets, age, sex); RDW missing in Yemeni set. Adjust for inflammation with NHANES CRP (HSCRP_J). External dataset: https://data.mendeley.com/datasets/dmktk7t677/1
