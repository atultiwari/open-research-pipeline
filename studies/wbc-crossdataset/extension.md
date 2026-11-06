---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich wbc-crossdataset` to replace it with a full, verified guide.

## Proposed extension (from the register)

Hematology vs histopathology vs general foundation models for white-cell classification: cross-dataset validation (WBCBench 2026 → PBC Barcelona → Raabin-WBC) and robustness to image degradation

## Why it is new

Challenge entries reported only in-distribution macro-F1. Trains frozen-encoder probes on single-institution WBCBench, tests zero-shot on Spanish and Iranian sets with pathologist-harmonised classes, compares DinoBloom with UNI2-h, H-optimus-0, Virchow2 and DINOv2, and reports degradation curves and calibration.

## Design

- **Study type:** Benchmark + external validation + robustness
- **Reporting guideline:** CLAIM 2024
- **Scores:** feasibility 5/5, novelty 3/5

The systematic gap analysis (novelty check per gap, open-data matches, design sketches) has not been done yet.
