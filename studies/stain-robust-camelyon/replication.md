---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich stain-robust-camelyon` to replace it with a full, verified guide.

## What the original study did

*A protocol for evaluating robustness to H&E staining variation in computational pathology models (CVPR 2026)* (arXiv, 2026-03-13). [Source](https://arxiv.org/html/2603.12886v1).

## Data

- **Datasets:** CAMELYON16/17
- **Access:** open (CC0 on AWS, no account)
- **Main link:** https://registry.opendata.aws/camelyon/

## Code

https://github.com/CTPLab/staining-robustness-evaluation

## Compute

RunPod (~60–120 GPU-h; reduce with fewer stain conditions/models); about 9 weeks to a preprint (register estimate).

## Notes from the register

Code Apache-2.0. CAMELYON is ~1 TB: use a RunPod volume near us-west-2. Source reports r=-0.22 in abstract vs -0.28 in results; quote carefully.
