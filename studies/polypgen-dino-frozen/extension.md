---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich polypgen-dino-frozen` to replace it with a full, verified guide.

## Proposed extension (from the register)

Cross-centre generalisation of polyp segmentation: correctly frozen re-evaluation of DINOv2/v3 key features on PolypGen with zero-shot external testing on Kvasir-SEG and CVC-ClinicDB

## Why it is new

Authors' own v2 note says the encoder was not properly frozen, so the claims are not fully valid. A transparent, correctly frozen reproduction with zero-shot external sets, newer encoders and failure analysis by polyp size and morphology fills a real gap.

## Design

- **Study type:** Segmentation domain-generalisation benchmark
- **Reporting guideline:** CLAIM 2024
- **Scores:** feasibility 4/5, novelty 3/5

The systematic gap analysis (novelty check per gap, open-data matches, design sketches) has not been done yet.
