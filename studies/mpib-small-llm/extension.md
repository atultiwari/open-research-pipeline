---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich mpib-small-llm` to replace it with a full, verified guide.

## Proposed extension (from the register)

Prompt-injection robustness of small, on-prem-deployable medical LLMs (<10B, quantised) on MPIB, with lightweight defences and their false-refusal cost

## Why it is new

Original tested 12 models (4B–72B) without newer small models or quantised variants. Adds Gemma-3/Qwen3/Phi-4-mini/Llama-3.2 in GGUF/AWQ, effect of quantisation on clinical-harm rate, one cheap defence stack, and optional Indian-guideline RAG poisoning set.

## Design

- **Study type:** Benchmark / red-team evaluation
- **Reporting guideline:** TRIPOD-LLM (adapted)
- **Scores:** feasibility 4/5, novelty 4/5

The systematic gap analysis (novelty check per gap, open-data matches, design sketches) has not been done yet.
