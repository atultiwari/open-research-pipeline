---
enriched: true
---
## What the original study did

Liu, Shang et al. (Xi'an Jiaotong University and Westlake University, [arXiv 2505.24141](https://arxiv.org/abs/2505.24141), v1, 30 May 2025) asked whether **slide-level pathology foundation models** (WSI-FMs) can be pushed into wrong answers by tiny, invisible changes to a few patches. They tested three WSI-FMs: CHIEF (CTransPath patch encoder), TITAN (CONCH v1.5 patch encoder) and PRISM (Virchow patch encoder). The attacker is assumed to have the foundation model's weights but no labels and no access to the downstream classifier. The attack is therefore **label-free**: it pushes the slide embedding away from its clean value, which degrades whatever task sits on top. Four classic white-box gradient attack families were adapted to this setting, and only a single random patch per slide (about 0.1% of the patches) was changed, within a budget usually considered imperceptible. Downstream MLP classifiers on six tasks (TCGA-BRCA ER status, TCGA-RCC subtype, TCGA-NSCLC subtype, CAMELYON16 metastasis, EBRAINS IDH status and 12-class brain tumour subtype) lost accuracy. CHIEF was the most robust and PRISM the least, a ranking that tracked parameter count (the "butterfly effect"). A cheap defence, adding small uniform noise to every patch before encoding, recovered most of the lost accuracy on CAMELYON16 and TCGA-RCC.

**Two numbers in the stub needed correcting.** The v1 abstract says accuracy fell by "up to 20%". Table 1 shows much larger single-patch drops: for example TITAN on CAMELYON16 fell from 98.3% to 41.8% under the single-step attack (a 56.5-point drop), and PRISM on EBRAINS subtyping fell by 61.7 points. The stub's "98% to 42%" figure is that TITAN row, not a typical result.

**Later version (not peer-reviewed).** An expanded version, retitled *The Butterfly Effect in Pathology: Exploring Adversarial Attack in Pathology Foundation Models*, was posted on SSRN in 2026 ([doi:10.2139/ssrn.7383688](https://doi.org/10.2139/ssrn.7383688)), with M. Crispin-Ortuzar and Z. Deng added as authors. Its abstract reports five WSI-FMs, five datasets and eight tasks, drops of more than 60% in the worst cases, and lightweight input-transformation defences. The repo README lists the five models as CHIEF, PRISM, Prov-GigaPath, TITAN and FEATHER, and the defences as bit-depth reduction, Gaussian blur and randomised smoothing. The SSRN full text was not readable here (HTTP 403), so check its tables before quoting any v2 number. No journal version was found (Crossref and Europe PMC, 2026-11-06).

**Replicability verdict: replicable on open data, with gated models and a code-licence caveat.** All datasets are open or free-registration. The model weights are gated, and most are non-commercial and no-derivatives. The authors' code has **no licence**, so run it locally to check numbers but reimplement anything you keep.

**Safety rule for this study (CLAUDE.md rule 6).** This is defensive measurement. Never commit attack code, attack settings that would let someone reproduce a specific attack, perturbed images or perturbation tensors to this repo, and never release universal perturbations. Describe attack families in the abstract ("single-step and iterative gradient attacks on a few patches, bounded so they stay invisible"), and report only aggregate metrics.

## Data

| Dataset | Used for | Access | How to get it |
| --- | --- | --- | --- |
| CAMELYON16 (`datasets/camelyon16`) | Metastasis detection (binary). 399 slides in the paper's appendix (239 normal, 160 tumour) | Open, CC0 | AWS Open Data bucket `s3://camelyon-dataset/CAMELYON16/` (us-west-2, no account: `aws s3 cp --no-sign-request`). Listing on 2026-11-06: 399 slide images, 752.3 GB, plus 160 XML annotations and the official evaluation files; 762.5 GB in total with masks |
| TCGA via GDC (`datasets/tcga`) | ER status (BRCA), RCC subtype (KIRC/KIRP/KICH), NSCLC subtype (LUAD/LUSC) | Open (no login) | GDC portal or `gdc-client` with a manifest. Open diagnostic slides per the GDC API (2026-11-06): LUAD 541 (415.1 GB), LUSC 512 (408.6 GB), BRCA 1,133 (1,158.8 GB), KIRC+KIRP+KICH 939 (937.4 GB) |
| EBRAINS Digital Brain Tumour Atlas (`datasets/ebrains-brain-tumour-atlas`) | IDH status and 12-class subtype | Free registration; non-commercial data use agreement | EBRAINS account, then accept the DUA. Optional for this study: skip it unless you reproduce the brain tasks |

The paper's task counts (Appendix A) are: BRCA ER 779 slides, RCC 918, NSCLC 1,018, CAMELYON16 399, EBRAINS IDH 873, EBRAINS subtype 2,318. Ready-made labels and splits ship in the repo's `dataset_csv/` and `splits/` folders. Use them for reference only (no licence), and rebuild the labels from GDC clinical data and the CAMELYON16 reference files.

**Storage tips:**
- Do not download everything. For replication, pick **CAMELYON16 plus one TCGA task** (NSCLC is the cheapest). The paper attacked only 300 slides per task.
- Stream slides to a RunPod network volume (preferably in a US region, since the bucket is in `us-west-2`), extract features, keep the `.h5` feature files, and delete the WSI unless it is in the attacked subset.
- For TCGA training sets you can skip slide downloads altogether by using the precomputed CONCH v1.5 features (`datasets/conch-v15-features-tcga`, 121 GB, gated auto). Only the slides you attack need pixels.

**Model access (Hugging Face API, 2026-11-06):**

| Model (role in the source) | Licence | Gating |
| --- | --- | --- |
| [TITAN](https://huggingface.co/MahmoodLab/TITAN) (slide encoder) + [CONCH v1.5](https://huggingface.co/MahmoodLab/conchv1_5) (patch encoder) | CC-BY-NC-ND-4.0 | auto |
| [PRISM](https://huggingface.co/paige-ai/Prism) (slide encoder) + [Virchow](https://huggingface.co/paige-ai/Virchow) (patch encoder) | PRISM CC-BY-NC-ND-4.0; Virchow Apache-2.0 | both auto |
| [CHIEF](https://github.com/hms-dbmi/CHIEF) (CTransPath + aggregator) | GitHub reports AGPL-3.0, but the README says GPLv3 for non-commercial academic use (mismatch, flag it) | weights by request (Google Drive link in the README) or the Docker Hub image the README names |
| [Prov-GigaPath](https://huggingface.co/prov-gigapath/prov-gigapath) (v2 only) | Apache-2.0 | auto |

Request access with an institutional email before you start. Academic, non-commercial use only.

## Environment

- The repo has no `requirements.txt` or `environment.yml` (checked 2026-11-06). Its code imports PyTorch, `timm` and CLAM-style utilities, and ships model wrappers for CHIEF, CTransPath, ABMIL and GigaPath.
- Suggested stack: Python 3.10, PyTorch 2.x with CUDA 12, `timm`, `huggingface_hub`, `openslide-python`, `h5py`, `numpy`, `pandas`, `scikit-learn`, `scipy`, `matplotlib`.
- Tissue segmentation and patching: [CLAM](https://github.com/mahmoodlab/CLAM) (GPL-3.0), as in the paper (512 × 512 px at 20×), or [TRIDENT](https://github.com/mahmoodlab/TRIDENT) (CC BY-NC-ND 4.0 in its LICENSE file; GitHub shows "NOASSERTION").
- Standard attack and robustness implementations: use a maintained, licensed library rather than writing your own, e.g. IBM [Adversarial Robustness Toolbox](https://github.com/Trusted-AI/adversarial-robustness-toolbox) (MIT). Keep all of this in a **separate private analysis repo**, never in this one.
- **Code licence:** [Jiashuai-Liu-hmos/Attack-WSI-pathology-foundation-models](https://github.com/Jiashuai-Liu-hmos/Attack-WSI-pathology-foundation-models) has **no licence file** (GitHub API, 2026-11-06; last commit 2025-12-08, "complete attack pipeline"). Run it to check numbers; reimplement rather than copy.

## Step-by-step replication

1. **Accounts and access:** Hugging Face gated access for TITAN, CONCH v1.5, PRISM and Virchow; request CHIEF weights. No account is needed for CAMELYON16 or TCGA.
2. **Patching:** segment tissue and cut 512 × 512 px patches at 20× with CLAM for CAMELYON16 and TCGA-NSCLC. Cap at 7,000 patches per slide, taking a contiguous block as the paper did (Appendix C), and apply the same cap to the clean baseline.
3. **Clean features and classifiers:** extract patch features and slide embeddings with each WSI-FM's own pipeline. Train MLP classifiers with 5-fold cross-validation. When evaluating an attacked slide, use the fold model that never saw that slide (the paper's leakage control). Check clean accuracy against Table 1 before going further.
4. **Attacked subset:** randomly select 300 slides per task (fixed seed, saved list). For each slide, choose one random patch and repeat four times, as in Section 5.2.
5. **Attacks:** run the four attack families from the paper's Section 4.2 using the library implementations, with the label-free objective (distance between clean and perturbed slide embeddings). Take the budget, iteration count and step size from Appendix C; record them in the private analysis repo only.
6. **Metrics:** accuracy drop (AD) and attack success rate (ASR) as defined in the paper's reference [36]; mean ± SD over the four repeats.
7. **Defence:** add small uniform noise to all patches before encoding (Section 5.5) and re-measure clean and attacked accuracy on CAMELYON16 and NSCLC.
8. **Optional:** the perturbation-scope sweep (1, 2, 4, 8 patches, sequential versus parallel) on CAMELYON16 only, and the patch-type analysis (tumour patch in tumour slide, normal patch in tumour slide, normal patch in normal slide) using the CAMELYON16 annotations.

## Compute and cost

- The paper used servers with 8× RTX 4090 and 8× A100, but states that everything runs on a single A100 (Appendix C).
- Attack cost per task (TCGA-RCC, MIM-type attack on 300 slides): about 0.5 h for CHIEF and 1.75 h for PRISM on a 4090, and 9.3 h for TITAN on an A100. The full attack-plus-defence run took about 10 h (CHIEF), 12 h (PRISM) and 60 h (TITAN) per task, because the defence re-extracts every patch.
- Feature extraction for CAMELYON16 plus TCGA-NSCLC with three encoders: roughly 20–40 GPU-h.
- **Total for a two-task replication (CAMELYON16 + NSCLC, three models, attacks plus the noise defence):** about 120–180 GPU-h on RunPod A100/L40S, roughly US$150–300 at community prices (verify current prices). Dropping TITAN's defence arm halves this.
- Storage: about 760 GB for all of CAMELYON16 and 820 GB for TCGA-NSCLC if downloaded in full; far less if you stream and delete.

## Target numbers

From Table 1 (single random patch, accuracy %, no attack → strongest attack):

| Model | CAMELYON16 | TCGA-NSCLC | TCGA-RCC |
| --- | --- | --- | --- |
| CHIEF | 84.3 → 51.3 | 93.1 → 91.6 | 96.4 → 92.8 |
| PRISM | 95.3 → 45.4 | 93.1 → 54.5 | 90.0 → 44.4 |
| TITAN | 98.3 → 41.8 | 96.2 → 80.9 | 94.5 → 79.1 |

Also reproduce, qualitatively:
1. The robustness ranking CHIEF > TITAN > PRISM (Section 6.1, Appendix Table 2).
2. More perturbed patches matter more than a larger per-pixel budget (Figure 3).
3. Attacks on normal slides succeed more often than on tumour slides (Figure 4).
4. The uniform-noise defence restores most of the clean accuracy (Figure 5; Appendix Table 9, whose values did not render in the arXiv HTML, so read them from the PDF).

## Known pitfalls

- **Inconsistent headline numbers:** the v1 abstract ("up to 20%") disagrees with Table 1. Compare against the tables, and against SSRN v2 once readable.
- **Appendix tables 3–9 did not render** in the arXiv HTML (only the headers). Use the PDF.
- **Licences:** TITAN, CONCH v1.5 and PRISM are CC-BY-NC-ND. Publish metrics only, never features or weights. The CHIEF licence is stated two different ways (AGPL-3.0 on GitHub, GPLv3 non-commercial in the README).
- **Pretraining overlap:** several encoders saw TCGA during pretraining (e.g. Phikon-v2's card lists TCGA, CPTAC and GTEx; check each model card). CAMELYON16 is a cleaner test set.
- **Patch cap:** truncating to 7,000 contiguous patches changes which tissue the model sees on big slides. Report how many slides were truncated.
- **Leakage:** keep the out-of-fold rule for every attacked slide. CAMELYON16 also has an official train/test split; report both.
- **Defence evaluation:** a defence tested only against an attacker who ignores it overstates protection. The UTAP authors showed a filter defence being bypassed once the attacker accounted for it (Wang et al., Light Sci Appl 2026). Report defence-aware results as well.
- **Version drift:** the repo was updated in December 2025, after v1. Its scripts may match v2 rather than v1.

## Claude Code task list

1. Create a **private** analysis repo `pathfm-adversarial-analysis` (never this repo). Add `data/`, `features/`, `perturbations/` and `logs/` to `.gitignore`, and configure the attack runs to keep perturbed patches in memory only.
2. Write `download_camelyon16.py` (AWS `--no-sign-request`, slide list, checksums) and `gdc_manifest.py` for TCGA-NSCLC diagnostic slides (open access only).
3. Write `patch.py` (CLAM-style segmentation, 512 px at 20×, 7,000-patch contiguous cap) and log the truncation counts.
4. Write `extract.py --model {chief,titan,prism}`: patch features plus slide embeddings to `features/<model>/<slide>.h5`, with resume support.
5. Write `train_probe.py`: 5-fold MLP per task and model; save fold assignments; check clean accuracy against Table 1 (flag gaps over 3 points).
6. Write `attack_eval.py`, which calls library attack implementations with the label-free objective and the Appendix C settings read from a private config file. It writes only per-slide outcome rows (slide id, repeat, clean prediction, attacked prediction) to `results/raw/` (gitignored).
7. Write `defence_eval.py` for the uniform-noise defence (clean and attacked accuracy).
8. Write `summarise.py` to compute AD and ASR (mean ± SD), and write aggregate tables to `results/replication.md`.
9. Before any commit anywhere, grep the diff for tensors, image files and attack settings; commit aggregate numbers only.
