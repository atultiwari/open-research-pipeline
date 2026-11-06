---
enriched: true
---
## What the original study did

Rajapaksha et al. (University of Moratuwa, Sri Lanka; arXiv 2610.33691, accepted to WACV 2027) generate a pathology report from a TCGA whole-slide image with a LLaVA-style model. A visual path turns CONCH v1.5 patch features into TITAN slide tokens (128 × 768), projected into Qwen2.5-7B-Instruct. A knowledge path first predicts the slide's histology (31 classes, which match TCGA cohorts) from the slide embedding plus the primary site, then pulls that class's one-hop neighbourhood from a 177-node, 317-edge graph and passes it to the LLM as structured text. The graph was built by having GPT-4o extract morphology terms from WSI-Bench reports, mapping them to UMLS with SapBERT, and having pathologists check it. On the 208 WSI-Bench test reports, PathKGen beat WSI-LLaVA on BLEU, ROUGE-L, METEOR and the LLM-judged WSI-Precision.

**Partly replicable now.** The slides (TCGA) are open, WSI-Bench is on Hugging Face behind a click-through, and the authors have uploaded their preprocessed JSONs and TITAN features. The code has no licence, and the trained weights are "coming soon". You can retrain from scratch for research.

## Data

| Dataset | What | Access | How to get it |
| --- | --- | --- | --- |
| WSI-Bench (report subset) | 9,749 train / 208 test slide–report pairs from TCGA; 9,452 slides kept after dropping slides with no microns-per-pixel value | Gated (auto), no licence stated | [Lucas-yuc/WSI-Bench](https://huggingface.co/datasets/Lucas-yuc/WSI-Bench) (`datasets/wsi-bench`) |
| PathKGen preprocessed copy | `WSI-Bench-{train,test}_Report_knowledge.json` with knowledge prompts already embedded, plus per-slide TITAN features (`.h5`) | Not gated, no licence stated | [deepshark43/wsi_bench_pathkgen](https://huggingface.co/datasets/deepshark43/wsi_bench_pathkgen) |
| TCGA slides | Only needed to rebuild features or for pathologist review | Open (GDC) | `datasets/tcga`; view slides in the GDC portal without downloading |
| CONCH v1.5 TCGA/CPTAC features | Same encoder and patch settings (512 px, 20×, TRIDENT) as PathKGen | Gated (auto), CC-BY-NC-ND | `datasets/conch-v15-features-tcga` (121 GB; download only the slides you need) |

## Environment

From the repo's `environment.yml` and `requirements.txt`: Python 3.10, PyTorch 2.5.1 (CUDA 12.1), transformers 4.57.3, bitsandbytes 0.45 (QLoRA), flash-attn 2.8.3, accelerate 1.12, bert-score 0.3.13, scispaCy `en_core_sci_sm`, and `neo4j` 6.1 for the graph store. Models: CONCH v1.5 and TITAN (MahmoodLab, CC-BY-NC-ND, gated auto) and Qwen2.5-7B-Instruct (Apache-2.0, not gated). Feature extraction uses [TRIDENT](https://github.com/mahmoodlab/TRIDENT); the README says TITAN must be modified to also save its 2D tokens.

## Step-by-step replication

1. Clone the repo outside this project; create the `vlm` conda env; edit `paths_config.sh` and `paths_config.py`.
2. Download the PathKGen Hugging Face copy into `data/` (dataset JSONs + `slide_features/`). Check the slide count against 9,452 + 208.
3. Download Qwen2.5-7B-Instruct into `checkpoints/`.
4. Stage 1: train the projection layer only (`pipeline/train_stage1.sh`; 8 epochs, effective batch 64).
5. Stage 2: QLoRA on the LLM plus projector (`pipeline/train_stage2.sh`; 1 epoch, effective batch 128; BLEU-4-weighted hard-example loss, Appendix B.1). Seed 42.
6. Inference on the 208 test slides (`pipeline/inference.sh`); score BLEU-1–4, ROUGE-L, METEOR, BERTScore, and WSI-Precision (LLM judge from WSI-LLaVA).
7. Re-run the ablations: vision only, histology only, site only, and the counterfactual anchors (oracle, random wrong).
8. Optional: rebuild the auxiliary classifier (`auxiliary_classifier/`) and the graph (`knowledge_path/graph_construct/`); this needs GPT-4o calls and a UMLS licence.

## Compute and cost

- Stage 1 + stage 2 at 7B: roughly 15–30 GPU-h on one A100 80 GB (RunPod ~US$25–50); 1.5B and 3B variants are cheaper. The paper does not report GPU hours (verify).
- WSI-Precision needs an LLM judge (API cost: a few US$ for 208 reports).
- Rebuilding features from raw slides is expensive (TB-scale TCGA download); avoid it by using the released features.

## Target numbers

- **Table 2 (PathKGen, 208 test reports):** BLEU-1 0.512, BLEU-4 0.261, ROUGE-L 0.519, METEOR 0.485, WSI-Precision 0.480. Baseline rows are copied from WSI-LLaVA and WSI-Agents, not re-run.
- **Table 3 ablation (7B):** vision-only WSI-Precision 0.4661; histology-only 0.4570; site-only 0.4480; full 0.4802.
- **Table 5 counterfactuals:** oracle anchor 0.4830; random wrong anchor 0.2540.
- **Table 1 auxiliary classifier:** accuracy 0.975, macro-F1 0.971 with embedding + site; site alone 0.842 / 0.694.
- **Section 4.2:** BERTScore F1 0.9081 (RoBERTa-large).

## Known pitfalls

- **WSI-Precision is noisy:** the paper's own 95% CI (Table 7) is 0.451–0.499, which contains the vision-only (0.466) and histology-only (0.457) scores. Re-run with several training seeds before claiming a knowledge-path gain.
- **CIs come from repeated evaluation, not repeated training:** training used one seed (42).
- **Metric gaming:** the loss up-weights samples with low BLEU-4, so BLEU gains partly reflect the objective.
- **Possible graph leakage:** the graph was mined from "ground truth reports of WSI-Bench" without saying test reports were excluded. Rebuild it from training reports only and compare.
- **Histology = TCGA cohort:** the 31 classes are TCGA project names, so "histology" is close to "which TCGA study", and primary site gives much of it away.
- **Licences:** code has no licence; WSI-Bench has none stated; CONCH v1.5 and TITAN are NC-ND. Do not redistribute features or weights.

## Claude Code task list

1. Request Hugging Face access (WSI-Bench, CONCH v1.5, TITAN); download the PathKGen preprocessed copy to `data/`.
2. Set up the env on RunPod (A100 80 GB); clone the repo outside this project.
3. Train stage 1 and stage 2 at 7B with seeds 42, 1, 2; run inference on the 208 test slides.
4. Score all metrics; report mean ± SD over training seeds next to Table 2.
5. Re-run Table 3 and Table 5 ablations with the same seeds.
6. Check graph leakage: rebuild the graph from training reports only (needs GPT-4o or an open LLM and UMLS) and compare test scores.
7. Commit only scripts, configs and aggregate metric tables; never reports, features or weights.
