---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich medmcqa-path` to replace it with a full, verified guide.

## Proposed extension (from the register)

Pathology and lab-medicine slice of MedMCQA (AIIMS/NEET-PG style): prompt sensitivity, answer-order bias and permutation voting across open-weight and frontier models, with a pathologist-built error taxonomy

## Why it is new

Source tested only MedGemma 4B/27B with aggregate accuracy. Adds per-subject pathology/microbiology/biochemistry results, newer open models plus 1–2 frontier APIs, a pathologist error taxonomy, an audit of wrong answer keys in pathology items, and cost per correct answer.

## Design

- **Study type:** LLM benchmarking / robustness evaluation
- **Reporting guideline:** TRIPOD-LLM; MI-CLEAR-LLM
- **Scores:** feasibility 5/5, novelty 3/5

The systematic gap analysis (novelty check per gap, open-data matches, design sketches) has not been done yet.
