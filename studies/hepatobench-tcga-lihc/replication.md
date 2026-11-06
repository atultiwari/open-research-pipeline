---
enriched: false
---
> **Needs enrichment.** This is a stub migrated from the old register. Run `/enrich hepatobench-tcga-lihc` to replace it with a full, verified guide.

## What the original study did

*A Digital Pathology Resource for Liver Cancer Quantification with Datasets, Benchmarks, and Tools (HepatoBench / HepatoQuant)* (arXiv (cs.CV), 2026-04-22). [Source](https://arxiv.org/abs/2604.22858).

## Data

- **Datasets:** HepatoBench (87,301 patches, 7 classes) + TCGA-LIHC WSIs
- **Access:** open (treat as CC BY-NC 4.0); TCGA-LIHC open via GDC
- **Main link:** https://huggingface.co/datasets/xtxx/HepatoBench

## Code

https://github.com/lingxitong/PFM_Segmentation

## Compute

Colab + RunPod (~15–30 GPU-h for ~370 WSIs); about 6 weeks to a preprint (register estimate).

## Notes from the register

Dataset licence mismatch (card CC BY vs paper CC BY-NC). Paper says not for diagnosis-focused algorithms: frame as quantification. Fits HistoForge FM benchmarking.
