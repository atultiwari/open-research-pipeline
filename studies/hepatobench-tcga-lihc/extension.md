---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich hepatobench-tcga-lihc` to replace it with a full, verified guide.

## Proposed extension (from the register)

Liver histology tissue classification: benchmark open pathology foundation models on HepatoBench, then test slide-level tissue composition (fibrosis, necrosis, steatosis) against TCGA-LIHC survival

## Why it is new

Paper benchmarked only UNI-v1, Virchow-2 and GigaPath. Adds lighter open encoders (H0-mini, Phikon-v2, UNI2, CONCH v1.5), label-efficiency curves, pathologist per-class error review, and a TCGA-LIHC survival test of tissue fractions.

## Design

- **Study type:** Benchmark + prognostic feature study
- **Reporting guideline:** CLAIM 2024; REMARK / TRIPOD+AI for survival
- **Scores:** feasibility 4/5, novelty 4/5

The systematic gap analysis (novelty check per gap, open-data matches, design sketches) has not been done yet.
