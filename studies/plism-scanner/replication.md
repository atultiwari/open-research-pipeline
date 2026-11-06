---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich plism-scanner` to replace it with a full, verified guide.

## What the original study did

*Scanner-Induced Domain Shifts Undermine the Robustness of Pathology Foundation Models* (arXiv, 2026-01-07). [Source](https://arxiv.org/abs/2601.04163v1).

## Data

- **Datasets:** PLISM (registered multi-scanner, smartphone and multi-stain tiles; Ochi et al., Sci Data 2024)
- **Access:** open (CC BY 4.0; free HF login for bulk download)
- **Main link:** https://huggingface.co/datasets/owkin/plism-dataset

## Code

None from source; reimplementable. Feature extraction: https://github.com/mahmoodlab/TRIDENT

## Compute

RunPod (~10–20 GPU-h); analysis on laptop; about 5 weeks to a preprint (register estimate).

## Notes from the register

Full set ~225 GB: download a subset. Tiles already registered, so no WSI handling. Many FMs are CC-BY-NC-ND and gated (institutional email). Cite prior Owkin/Kaiko PLISM numbers; position on scanner/smartphone and calibration.
