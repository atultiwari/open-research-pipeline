---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich medmcqa-path` to replace it with a full, verified guide.

## What the original study did

*When Chain-of-Thought Backfires: Evaluating Prompt Sensitivity in Medical Language Models* (arXiv, 2026-03-26). [Source](https://arxiv.org/abs/2603.25960).

## Data

- **Datasets:** MedMCQA validation split (4,183 Qs; subject field incl. Pathology, Microbiology, Biochemistry)
- **Access:** open (Apache-2.0)
- **Main link:** https://huggingface.co/datasets/openlifescienceai/medmcqa

## Code

https://github.com/UNHSAILLab/MedMCQA-Robustness-Study

## Compute

RunPod (~20–40 GPU-h) + API (~USD 30–80); about 5 weeks to a preprint (register estimate).

## Notes from the register

Repo is MIT with a Colab notebook. MedMCQA keys are noisy, so the answer-key audit is itself a contribution. Could add repeated-sampling consistency (arXiv 2604.10535).
