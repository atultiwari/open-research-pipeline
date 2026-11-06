---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich fairness-tcga-cptac` to replace it with a full, verified guide.

## What the original study did

*Demographic bias in misdiagnosis by computational pathology models (Nature Medicine 2024)* (Nature Medicine, 2024-04). [Source](https://pubmed.ncbi.nlm.nih.gov/38641744/).

## Data

- **Datasets:** TCGA (BRCA, LUAD/LUSC, GBM/LGG) + CPTAC via precomputed UNI2-h features
- **Access:** open WSIs and clinical data; feature set CC-BY-NC-ND (gating unclear, verify)
- **Main link:** https://huggingface.co/datasets/sofieneb/uni2h_features

## Code

https://github.com/mahmoodlab/CPATH_demographics

## Compute

Laptop/Colab (~5–10 GPU-h on precomputed features); about 5 weeks to a preprint (register estimate).

## Notes from the register

Repo academic use only. Few Black/Asian patients: report CIs and power. Race is confounded with site (cf. arXiv 2508.14779). Check third-party feature counts against a small self-extracted sample.
