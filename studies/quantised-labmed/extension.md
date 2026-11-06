---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich quantised-labmed` to replace it with a full, verified guide.

## Proposed extension (from the register)

Laptop-deployable medical LLMs: accuracy and hallucination cost of 4/8-bit quantisation on a lab-medicine slice of Medmarks (MedMCQA-pathology, MedCalc-Bench, MedHallu, MEDEC)

## Why it is new

Medmarks evaluated 61 models at full precision only. Adds quantisation levels on consumer GPU and CPU laptop for Indian low-resource deployment, with tokens/sec, RAM, cost per 1,000 questions and calibration, restricted to lab-medicine tasks (anion gap, eGFR, corrected calcium via MedCalc-Bench).

## Design

- **Study type:** LLM benchmarking / deployment evaluation
- **Reporting guideline:** TRIPOD-LLM; MI-CLEAR-LLM
- **Scores:** feasibility 5/5, novelty 3/5

The systematic gap analysis (novelty check per gap, open-data matches, design sketches) has not been done yet.
