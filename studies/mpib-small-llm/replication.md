---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich mpib-small-llm` to replace it with a full, verified guide.

## What the original study did

*MPIB: A Benchmark for Medical Prompt Injection Attacks and Clinical Safety in LLMs* (arXiv (cs.CL/cs.CR), 2026-02-06). [Source](https://arxiv.org/abs/2602.06268).

## Data

- **Datasets:** MPIB v1.2 (9,697 instances; direct and RAG-indirect injection)
- **Access:** free registration (HF gated, auto-approval; CC-BY-NC-4.0)
- **Main link:** https://huggingface.co/datasets/jhlee0619/mpib

## Code

https://github.com/jhlee0619/mpib-eval

## Compute

RunPod (~20–40 GPU-h); about 4-6 weeks to a preprint (register estimate).

## Notes from the register

Released toolkit is minimal; the LLM-judge pipeline must be rebuilt. Keep the payload registry private and report aggregate metrics only. Possible EMNLP 2026 Findings version (verify).
