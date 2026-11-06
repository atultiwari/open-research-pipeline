---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich pathfm-adversarial` to replace it with a full, verified guide.

## What the original study did

*The Butterfly Effect in Pathology: Exploring Security in Pathology Foundation Models* (arXiv (cs.CV/cs.CR), 2025-05-30). [Source](https://arxiv.org/abs/2505.24141).

## Data

- **Datasets:** Camelyon16; TCGA-BRCA/RCC/LUNG
- **Access:** open (Camelyon16 CC0; TCGA open on GDC; some FM weights HF-gated, free registration)
- **Main link:** https://camelyon16.grand-challenge.org/

## Code

https://github.com/Jiashuai-Liu-hmos/Attack-WSI-pathology-foundation-models

## Compute

RunPod (~30–60 GPU-h); about 6-8 weeks to a preprint (register estimate).

## Notes from the register

Best fit with HistoForge work but storage-heavy (Camelyon16 ~700 GB); start with a subset or one TCGA project. Do not release universal perturbations.
