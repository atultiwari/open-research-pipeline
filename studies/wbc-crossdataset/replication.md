---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich wbc-crossdataset` to replace it with a full, verified guide.

## What the original study did

*WBCBench 2026: A Challenge for Robust White Blood Cell Classification Under Class Imbalance* (arXiv, 2026-04-12). [Source](https://arxiv.org/html/2604.10797v1).

## Data

- **Datasets:** WBCBench 2026 (~100k images, 13 classes); PBC (17,092 images, CC BY 4.0); Raabin-WBC
- **Access:** free registration (HF gated, auto-approved, non-commercial, no redistribution); PBC and Raabin open
- **Main link:** https://huggingface.co/datasets/Xin-Tian/wbcbench2026

## Code

https://github.com/marrlab/DinoBloom

## Compute

Colab (~1–3 GPU-h per model); about 4 weeks to a preprint (register estimate).

## Notes from the register

Strong fit for a hematology-focused pathologist: class harmonisation needs expert judgement. PBC and Raabin were in DinoBloom pretraining: declare leakage. 267 WBCBench test labels changed after the challenge. PBC: https://data.mendeley.com/datasets/snkd93bnjr/1
