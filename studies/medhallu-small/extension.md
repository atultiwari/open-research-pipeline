---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich medhallu-small` to replace it with a full, verified guide.

## Proposed extension (from the register)

Can small open-weight models detect medical hallucinations? MedHallu on Gemma 3, MedGemma, Qwen3, Llama, with and without retrieved knowledge, plus a pathologist-annotated lab-medicine subset

## Why it is new

Original used GPT-4o, Llama-3.1, UltraMedical; best hard-item F1 was 0.625. Adds newer small open models, a small-model safety-checker design, a pathology/lab-topic subset with expert error taxonomy, and cost/latency trade-offs.

## Design

- **Study type:** LLM safety / hallucination detection
- **Reporting guideline:** TRIPOD-LLM; MI-CLEAR-LLM
- **Scores:** feasibility 5/5, novelty 3/5

The systematic gap analysis (novelty check per gap, open-data matches, design sketches) has not been done yet.
