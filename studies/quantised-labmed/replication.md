---
enriched: true
---
## What the original study did

Warner et al. (MedARC, 35 authors) built **Medmarks**, an open-source suite of 30 medical LLM benchmarks: 19 verifiable ones (Medmarks-V: multiple-choice QA, MedCalc-Bench calculations, Med-HALT, MedHallu and others) and 11 open-ended ones graded by two LLM judges (Medmarks-OE: MEDEC, HealthBench, MedCaseReasoning and others). They evaluated 61 models in 71 configurations, from 3B open models to GPT-5.2 and Gemini 3 Pro, and ranked them by a dataset-weighted mean win rate. Open models ran on vLLM on up to eight H100s, each with its maker's recommended sampling settings. Main findings: frontier reasoning models lead; Qwen3 thinking models punch above their size; medical fine-tuning helps; open models use far more tokens than proprietary ones; and small models are the most sensitive to answer order.

**The paper already contains a small quantisation experiment (Section 3.10, Figure 8, Figure 25).** It covers one model family only: Qwen3-30B-A3B Instruct and Thinking (2507), at BF16, official FP8, and community AWQ 8-bit and 4-bit. 8-bit was essentially harmless. AWQ 4-bit cost a small but consistent amount on most datasets. A footnote says quantisation-aware-trained (QAT) checkpoints probably degrade less, but the authors could not test this. The old stub for this study said Medmarks ran "full precision only". That was wrong, and the extension has been redesigned around what is really missing.

- **Source:** [arXiv:2605.01417](https://arxiv.org/abs/2605.01417) (v1, 2 May 2026, cs.CL). No journal or conference version was found (arXiv metadata has no journal reference). The old "ICML 2026" label could not be confirmed, so treat the venue as **verify**.
- **Code:** [MedARC-AI/medmarks](https://github.com/MedARC-AI/Medmarks), MIT licence (GitHub API, 2026-11-06). Leaderboard: [medmarks.ai](https://medmarks.ai).

**Replicability verdict: fully replicable on open data.** Every subset this study uses is open and not gated. The harness talks to any OpenAI-compatible endpoint, so a local `llama-server` (llama.cpp) or vLLM server plugs straight in. The only closed part is the LLM judges used for open-ended tasks (GPT-5 mini plus Gemini 3 Flash or Grok 4.1 Fast). This study avoids them by scoring MEDEC on its verifiable subtasks.

## Data

All checked on 2026-11-06 (Hugging Face API, GitHub API, dataset cards). Item counts are for the splits Medmarks evaluates.

| Dataset (`datasets/` id) | What Medmarks evaluates | Licence as stated | Lab-medicine slice for this study | How to get it |
| --- | --- | --- | --- | --- |
| MedCalc-Bench Verified (`medcalc-bench`) | 1,100 test items, 55 calculators × 20 | CC-BY-SA-4.0 (HF card; NCBI repo README explains the share-alike origin from PMC-Patients) | **380 items** in the "lab test" category (19 calculators, e.g. anion gap, delta gap, albumin-corrected calcium, CKD-EPI, MDRD, LDL, FENa, serum osmolality, free water deficit, HOMA-IR, FIB-4, MELD Na) | `nsk7153/MedCalc-Bench-Verified` on HF, not gated |
| MedMCQA (`medmcqa`) | 4,183 validation items | Apache-2.0 on `openlifescienceai/medmcqa`. **The harness loads the `lighteval/med_mcqa` mirror, whose card states no licence** | **629 unique items**: Pathology 337, Biochemistry 171, Microbiology 122 (validation rows) | HF, not gated |
| Med-HALT (`med-halt`) | FCT and NOTA reasoning tests, validation subset (5,154 items each) | Apache-2.0 (HF card) | **577 items per test** (Pathology 311, Biochemistry 159, Microbiology 107) | `openlifescienceai/Med-HALT`, not gated |
| MedHallu (`medhallu`) | `pqa_labeled` 1,000 rows → 2,000 items (each question paired once with the true and once with the hallucinated answer) | HF card: **no licence stated**. Code repo MedHallu/MedHallu: MIT. Medmarks lists the dataset as MIT, which seems to come from the code repo | All 2,000 (PubMedQA-based, not lab-specific); optional tag of lab-topic items by Atul | `UTAustin-AIHealth/MedHallu`, not gated |
| MEDEC (`medec`) | MS test set, 597 notes | CC BY 4.0 (abachaa/MEDEC README; the HF mirror says the same) | All 597, scored on subtask A (error flag) and B (error sentence) | Harness uses the `sauravlmx/MEDEC-MS` mirror, which now redirects to `expx/MEDEC-MS`. Original: [abachaa/MEDEC](https://github.com/abachaa/MEDEC) |

**Important overlap (checked 2026-11-06):** all 577 Med-HALT lab-slice validation questions have exactly the same stem text as MedMCQA validation questions (3,810 of the 5,154 Med-HALT validation items match MedMCQA validation in total). Med-HALT FCT/NOTA are therefore **reformatted versions of the same MedMCQA stems**, not independent items. Analyse them as paired formats of one question (direct answer, none-of-the-above, judge a student's answer), never as extra independent evidence.

Benchmarks to **skip** because their licences are unclear: Medbullets, MTSamples, MedConceptsQA, MedDialog (Medmarks marks them "Not specified").

**Storage:** the whole slice is under 50 MB. Download it to `data/` (gitignored) or a scratch folder. Commit only code and aggregate scores, never item text or model outputs that quote items (MedCalc-Bench notes are share-alike patient vignettes; keep them out of the repo anyway).

## Environment

- **Harness:** Python 3.12 (`uv venv --python 3.12`; `pyproject.toml` asks for ≥3.11), `uv sync`. Main dependencies: `verifiers>=0.1.14,<0.2`, `prime`, `datasets`, `pyarrow`, `polars`, `pydantic`.
- **Inference engines:**
  - vLLM (current release) for BF16/FP8/AWQ replication runs on a GPU;
  - llama.cpp `llama-server` (OpenAI-compatible) for GGUF runs, on both a RunPod GPU and a real laptop CPU. Pin the llama.cpp build number. Quantisation kernels change between builds.
- **Analysis:** `pandas`, `numpy`, `scipy`, `statsmodels` (McNemar, mixed-effects logistic), `scikit-learn` (calibration), `matplotlib`.

## Step-by-step replication

The goal is to reproduce the Section 3.10 finding on the lab-medicine slice, plus BF16 anchors for small models that Medmarks also ran.

1. `git clone https://github.com/MedARC-AI/Medmarks && cd Medmarks && uv venv --python 3.12 && uv sync`.
2. Smoke test: `uv run medarc-eval bench --config configs/medmarks-smoke.toml ... --dry-run`, then a 25-item run against a local server.
3. Write a slice config (`configs/labmed-slice.toml`) that runs `medcalc-bench` (verified, test), `med_mcqa`, `med_halt` (`reasoning_fct` and `reasoning_nota`), `medhallu` (`pqa_labeled`) and `medec`. The harness has no subject filter. Either run the full sets and filter afterwards by item id (cheap: about 12,000 items in total), or add a small subject filter in your own fork. Run MEDEC with `--eval-method metrics`, which gives the error-flag accuracy and the other paper metrics without an API judge.
4. **Replicate Section 3.10 on the slice.** Serve each checkpoint with vLLM on one 80 GB GPU and run the slice with the sampling settings in `configs/medmarks-endpoints.toml`:
   - `Qwen/Qwen3-30B-A3B-Instruct-2507` (BF16);
   - `Qwen/Qwen3-30B-A3B-Instruct-2507-FP8`;
   - AWQ 8-bit and 4-bit. The endpoint file still names `cpatonn/...-AWQ-8bit` and `cpatonn/...-AWQ-4bit`; on Hugging Face these now redirect to `cyankiwi/Qwen3-30B-A3B-Instruct-2507-AWQ-8bit` and `-AWQ-4bit` (Apache-2.0, not gated).
5. **BF16 anchors for small models:** run `google/medgemma-1.5-4b-it`, `Qwen/Qwen3-4B-Thinking-2507` and `google/medgemma-4b-it` at BF16 on vLLM with Medmarks' sampling settings. These link your setup to the published heatmap (Figure 13).
6. `uv run medarc-eval process --runs-dir runs/evals`. Then compute per-dataset scores for the slice only, and MedHallu F1 with the environment's `postprocess.py` (unsure answers dropped).
7. Compare your full-dataset scores (not just the slice) with the Medmarks heatmap and leaderboard for the anchor models. Differences above about 3 points mean a setup problem: parser, chat template or sampling.

## Compute and cost

- Slice size: about 380 + 629 + 1,154 + 2,000 + 597 ≈ 4,760 items per model and precision. That roughly doubles to about 12,000 if you run the full sets and filter afterwards.
- Qwen3-30B-A3B in four precisions on one A100/H100 80 GB (vLLM, high concurrency, mostly short answers): about 4–8 GPU-h. Small BF16 anchors: about 1 GPU-h each.
- Total for the replication: **about 8–12 GPU-h on RunPod (roughly US$15–30)**. No paid API, because MEDEC is scored with paper metrics, not the judge.

## Target numbers

- **Qualitative (Section 3.10, Figure 8):** FP8 and AWQ 8-bit within noise of BF16 on most datasets; AWQ 4-bit slightly but consistently lower. Figure 25 has per-dataset bars, but the values are only in the image. Read approximate values off the figure, and report direction and size rather than exact matches.
- **Dataset difficulty (Section 3.3):** across all models, the mean score was 0.439 on MedCalc-Bench and 0.656 on MedMCQA. Your anchor models should fall around their positions in Figure 13.
- **Per-model scores:** use the [medmarks.ai](https://medmarks.ai) leaderboard and Figure 13 for MedGemma 1.5 4B, MedGemma 4B and Qwen3 4B Thinking.

## Known pitfalls

- **Sampling noise versus quantisation effects.** Medmarks used recommended sampling (temperature 0.6–1.0 for most models) and three rollouts for most multiple-choice sets, but **only one run for MedCalc-Bench and Med-HALT**. A 4-bit penalty of 1–2 points sits inside that noise. For the extension, use greedy decoding for the paired comparison, plus three sampled seeds as a sensitivity check.
- **Engine confound.** vLLM BF16 versus llama.cpp Q4 changes two things at once. Run every precision of a model on the same engine (llama.cpp BF16 GGUF as the reference for GGUF quants), and keep vLLM only for the Medmarks-comparable anchors.
- **Chat templates.** GGUF files carry their own chat template. A wrong template (especially for Gemma 4 and Qwen3.5 thinking toggles) looks like a quantisation loss. Check that the first 20 outputs per model parse cleanly before any full run.
- **Med-HALT reuses MedMCQA stems** (see Data). Do not count them as independent items. Also, the harness README for Med-HALT cites the wrong authors (Jeblick et al.); the correct citation is Pal, Umapathi and Sankarasubbu (CoNLL 2023).
- **Med-HALT count mismatch:** the Medmarks README lists 22,152 evaluated Med-HALT items, while the environment README gives 5,154 per test (10,308 for FCT + NOTA). Record which number your run produces (**verify**).
- **FCT validation items are deliberately imbalanced** (almost all proposed answers are wrong), so a model that always says "wrong" scores well. Report balanced accuracy or the per-class breakdown alongside accuracy.
- **MedMCQA answer keys are noisy.** Medmarks' own physician review (Appendix P, Tables 12–13) found unclear or wrong items. Atul's audit of the 337 pathology items can turn this into a finding.
- **MedHallu** has no dataset licence on its card (see Data). Report aggregates only and flag the mismatch.
- **MedCalc-Bench version:** the Verified set is updated over time (last modified 2026-09-08). Record the release tag you used.
- **Mirrors:** MedMCQA via `lighteval/med_mcqa` (no licence on the card) and MEDEC via a renamed mirror (MS subset only, no UW notes). Cite and license from the originals.
- **Pretraining contamination:** MedMCQA and PubMedQA (the basis of MedHallu) are old and public, so newer models may have seen them. This affects absolute scores more than BF16-versus-4-bit differences, which is another reason to use paired comparisons.

## Claude Code task list

1. In a separate analysis repo (not this catalogue), clone Medmarks and pin its commit hash. Add `data/`, `runs/` and `*.jsonl` to `.gitignore`.
2. Write `slice_ids.py`: download the five datasets, pick the lab-medicine item ids (MedCalc "lab test" category; MedMCQA and Med-HALT subjects Pathology, Biochemistry, Microbiology), check the counts against the table above, and save **only the ids** to `slice_ids.json`.
3. Write `configs/labmed-slice.toml`, plus a filter step that keeps only slice ids after `medarc-eval process`.
4. Write `serve_vllm.sh <model>` and `serve_llamacpp.sh <gguf>`, recording the engine version, GPU, context length and sampling in `runs/<model>/meta.json`.
5. Run step 4 (Qwen3-30B-A3B, four precisions) and step 5 (small BF16 anchors) of the replication.
6. Write `score.py`: per-dataset accuracy, MedCalc accuracy by calculator, MedHallu F1 and abstention rate, MEDEC flag accuracy and sentence-detection accuracy, Med-HALT balanced accuracy. Add bootstrap 95% CIs over items.
7. Write `compare_medmarks.py`: put your full-dataset anchor numbers next to the leaderboard values and flag differences over 3 points.
8. Save aggregate tables to `results/replication.md` and `results/*.csv` (scores only, no item text).
