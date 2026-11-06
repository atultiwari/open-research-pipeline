---
enriched: true
---
## What the original study did

Chen, Yu and colleagues (corresponding author Kai Shu) built **ClinicalBench**, which compares 22 open-weight LLMs (14 general-purpose, 8 medical) with 11 traditional models (XGBoost, SVM, random forest, RNN, Transformer and others) on three hospital-visit tasks in MIMIC-III v1.4 and MIMIC-IV v2.2:
- length of stay in three classes (up to 1 week, 1–2 weeks, over 2 weeks);
- death during the visit;
- readmission within two weeks (code: next visit less than 15 days later).

Each patient's **first adult visit** is turned into a short text listing age, sex, the visit's **ICD diagnosis titles, ICD procedure titles and drug classes** (NDC mapped to ATC level 3). The traditional models get the same information as bag-of-codes counts. LLMs were tested by direct prompting at several temperatures and sizes (0.5B–70B), with chain-of-thought, self-reflection, role-play and in-context examples, and after LoRA fine-tuning. Traditional models won almost everywhere. Fine-tuning narrowed the gap but did not close it.

**Source.** Published in the *Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2* (KDD '26), 8 August 2026, [doi:10.1145/3770855.3818831](https://doi.org/10.1145/3770855.3818831), CC BY 4.0 (Crossref, checked 2026-11-06). Preprint [arXiv:2411.06469](https://arxiv.org/abs/2411.06469): v1 November 2024, v2 8 June 2026. **Read: v2 HTML in full.** v1 was not read separately. v2 adds a limitations section and caveats about ICD codes.

**Code.** [canyuchen/ClinicalBench](https://github.com/canyuchen/ClinicalBench), MIT licence (GitHub API), v1.0 package (August 2026), last commit 2026-09-29. It vendors a reduced copy of PyHealth v1.1.4 (BSD-3-Clause; see the repo's `NOTICE`). The 108 cohort split-index files ship in `data/`. Model outputs live in a separate Hugging Face dataset, [canyuchen/clinicalbench-results](https://huggingface.co/datasets/canyuchen/clinicalbench-results) (tagged MIT, auto-gated). Those files are **patient-level outputs derived from MIMIC**: treat them as credentialed data, keep them outside this repo, and never commit them.

### What the inputs really contain (checked in code, 2026-11-06)

- **No laboratory values, vital signs or notes.** `clinicalbench/config.py` hands the PyHealth reader only `diagnoses_icd`, `procedures_icd` and `prescriptions` from the MIMIC-IV `hosp` module. `labevents` is never read. The register's claim that labs are absent is **confirmed**. The paper's limitations section asks for "structured flowsheet data" in future work.
- **The inputs come from the whole stay, so they look back from discharge.** Diagnosis codes are assigned after discharge, and procedures and prescriptions cover the entire stay. For death during the visit, this is the label-leakage pattern shown by [Ramadan et al., JAMA Netw Open 2025](https://doi.org/10.1001/jamanetworkopen.2025.50454): ICD codes alone gave AUROC about 0.97 for MIMIC-IV in-hospital mortality, driven by codes such as cardiac arrest, brain death, palliative-care encounter and DNR status. ClinicalBench's README reports XGBoost AUROC 95.97 on MIMIC-III mortality, which fits this pattern. **This is the main gap the extension targets.**
- **MIMIC-IV version: v2.2.** The docs say the shipped indices are positions in the sample list that v2.2 produces. Any other release selects different patients.
- **Exclusions:** first visit per patient, age ≥ 18, and at least one diagnosis, one procedure and one drug code. That last rule quietly drops visits without a procedure code, which changes the case mix.

## Data

| Dataset | Version | Role | Access |
| --- | --- | --- | --- |
| `mimic-iv` | **v2.2** (released 6 Jan 2023; `hosp` + `icu` modules; DOI 10.13026/6mm1-ek67) | All three tasks, using the published splits | [PhysioNet v2.2](https://physionet.org/content/mimiciv/2.2/), credentialed |

MIMIC-III v1.4 is not needed: the extension uses MIMIC-IV only.

**Access (checked 2026-11-06).**
- Licence and agreement: PhysioNet Credentialed Health Data License 1.5.0 and Data Use Agreement 1.5.0.
- Steps: CITI "Data or Specimens Only Research" training, then PhysioNet credentialing (needs a referee), then sign the DUA on the v2.2 page. Allow **1–2 weeks** (`verify` the current turnaround).
- v2.2 is not the latest release (v3.1 is), but the v2.2 page is still live and is covered by the same credential.
- Download size is not shown on the public page (`verify` after login). `hosp/labevents` is by far the largest table, but the whole of `hosp` fits on a laptop SSD.
- Keep the data in a gitignored `data/` folder **outside this repo**, or in a DuckDB/PostgreSQL database built with [mimic-code](https://github.com/MIT-LCP/mimic-code) (MIT licence).

**DUA rules that shape this project.**
- **No MIMIC rows may go to an external LLM API.** That includes ChatGPT/OpenAI, the Claude API and this Claude Code session. PhysioNet's [responsible-use notice](https://physionet.org/news/post/gpt-responsible-use) says the DUA forbids sharing data with third parties through online services. The ClinicalBench paper itself used only open-source models for this reason.
- **Use local open-weight models only**, run on Atul's machine or on a RunPod pod that Atul controls. If RunPod is used, use a private pod with encrypted storage and wipe it after the run. Check with PhysioNet or the IRB whether a rented cloud GPU counts as "local" (`verify`).
- Claude writes the code. Atul runs it, and only aggregate results (AUROCs, counts, calibration bins) come back into the session.
- Do not redistribute derived row-level files, including prompts, lab extracts and per-patient predictions.
- The DUA asks that code behind published results be shared.

**Model licences for local use (Hugging Face API, 2026-11-06).**

| Model | Licence | Gating | Note |
| --- | --- | --- | --- |
| meta-llama/Meta-Llama-3-8B-Instruct | Llama 3 Community License | manual | ClinicalBench anchor |
| google/gemma-2-9b-it | Gemma terms | manual | ClinicalBench anchor; the best fine-tuned model in the paper |
| epfl-llm/meditron-7b | Llama 2 licence | auto | ClinicalBench medical anchor |
| Qwen/Qwen3.5-9B, Qwen/Qwen3.5-4B | Apache-2.0 | not gated | 2026 general models |
| google/gemma-4-12B-it, google/gemma-4-E4B-it | Apache-2.0 | not gated | 2026 general models |
| openai/gpt-oss-20b | Apache-2.0 | not gated | Reasoning model; fits one 24–48 GB GPU |
| microsoft/Phi-4-mini-instruct | MIT | not gated | Small baseline |
| google/medgemma-1.5-4b-it | Health AI Developer Foundations terms (`license:other`) | auto | Medical 2026 model |

All of these weights can be downloaded and run locally. None of them requires sending data to the model provider. The Llama and Gemma 2 gates need an HF account and acceptance of the terms; manual gates can take days.

## Environment

From the repo's `pyproject.toml`:
- Python 3.10 (conda);
- `pip install -e ".[llm]"` installs `transformers>=4.40`, `accelerate`, `peft`, `sentencepiece`, `xgboost>=1.5`, `scikit-learn`, `torch>=1.8` and `pandas>=1.3.2,<2`;
- `pytest tests/ -q` runs 104 tests without a GPU or MIMIC.

LoRA training uses LLaMA-Factory, which is not vendored (`docs/fine_tuning.md`). For the extension, add DuckDB and the mimic-code `concepts/measurement` SQL: `complete_blood_count.sql`, `chemistry.sql`, `blood_differential.sql`, `coagulation.sql`, `enzyme.sql` and `bg.sql` (lactate).

## Step-by-step replication

1. Check credentialing, the v2.2 DUA and the HF gates. Never place row-level data in this repo.
2. `git clone https://github.com/canyuchen/ClinicalBench && pip install -e ".[llm]" && pytest tests/ -q`.
3. Download MIMIC-IV v2.2 `hosp` and gunzip it. Then run `scripts/prepare_data.sh --mimic4 /path/to/mimiciv/2.2/hosp`. Check that the regenerated split files are byte-identical to the shipped ones. Run `pytest tests/test_config.py`, which checks the split sizes.
4. **Score without a GPU first.** Run `clinicalbench-fetch-results`, which accepts the HF gate and downloads 295 MB of patient-level outputs (keep them outside the repo). Then run `clinicalbench-table configs/paper/table_2.yaml --task mortality_pred --dataset mimic4`, which rebuilds the MIMIC-IV numbers from the released files.
5. Traditional baselines on CPU: `clinicalbench-baselines --task mortality_pred --dataset mimic4 --random_index 0`, repeated for indices 0–4 and all three tasks.
6. One LLM run end to end: `clinicalbench-llm --base_model google/gemma-2-9b-it --task mortality_pred --dataset mimic4 --mode ORI --scoring logits --random_index 0`, then `clinicalbench-score ... --auroc`. Keep the default `--token_id_mode legacy` to reproduce the paper. Use `auto` for new models (see pitfalls).
7. Compare your values with the targets below. Report the invalid-answer percentage next to every F1.

## Compute and cost

- **Data preparation and traditional baselines:** laptop, CPU, minutes per cohort.
- **Re-scoring the released results:** laptop, no GPU.
- **New LLM inference:** the MIMIC-IV test sets hold 5,768 visits (mortality), 5,020 (length of stay) and 4,664 (readmission) per split index. One logits pass per prompt, for one 7–9B model × 3 tasks × 5 splits (about 77k prompts of roughly 300–600 tokens), takes about 3–6 GPU-h on an A100 or L40S with HF transformers (estimate, `verify`).
- **The paper's own hardware:** 8 × RTX A6000 (Appendix A).
- **No API cost.** API use is not allowed.

## Target numbers

The paper's colour-coded Tables 1 and 4 render as images in the arXiv HTML, so their MIMIC-IV AUROCs were not readable. Get them with `clinicalbench-table configs/paper/table_2.yaml` (`verify`). Plain-text targets:

| Quantity | MIMIC-IV value | Where |
| --- | --- | --- |
| Mortality F1: XGBoost / SVM / RNN | 48.15 / 46.27 / 48.9 | Table 2 |
| Mortality F1: Llama3-8B / Meditron-70B / Qwen2-7B | 15.12 / 47.93 / 43.53 | Table 2 |
| Length-of-stay macro-F1: XGBoost / SVM | 64.19 / 66.43 | Table 2 |
| Length-of-stay macro-F1: Llama3-8B / Meditron-70B | 17.73 / 35.67 | Table 2 |
| Readmission F1: XGBoost / SVM / Llama3-8B | 27.73 / 28.27 / 25.05 | Table 2 |
| Mortality test prevalence | 200 / 5,768 (3.5%) | `SPLIT_SPECS`, config.py |
| MIMIC-III mortality AUROC: XGBoost / Gemma2-9B | 95.97 / 86.46 | README (from released files) |

## Known pitfalls

- **Version lock.** The shipped indices are valid only on MIMIC-IV v2.2. Do not use v3.1 for the replication. If labs are added, take them from v2.2 too. The lab `itemid`s changed between v2.2 and v3.0 and were fixed in v3.1, so check mimic-code's itemid lists against v2.2 `d_labitems` before use.
- **Hindsight inputs (label leakage).** Diagnosis codes, all-stay procedures and all-stay drugs are not available at admission. ClinicalBench's mortality task is therefore not a real-time prediction task (Ramadan et al. 2025). Say this plainly whenever you quote its numbers.
- **Unequal tuning.** Baselines are refit under 20 seeds and picked on validation F1. LLMs get one zero-shot pass (`docs/methodology.md`). Keep this asymmetry, or remove it on both sides.
- **Invalid answers are scored wrong, not dropped.** Always report `inv%`.
- **Answer-token lookup bug.** On SentencePiece tokenisers, the legacy `convert_tokens_to_ids` can return `<unk>` for bare digits, which makes AUROC meaningless for those models (`docs/methodology.md`). Use `--token_id_mode auto` for new work and say so.
- **Length-of-stay AUROC** binarises the task as "more than two weeks".
- **Balanced training data, natural-prevalence test data.** Thresholded F1 from models trained on balanced data is miscalibrated. Calibration needs recalibration on the validation set.
- **Temperature sweep (Figure 3)** samples, so it is not bit-reproducible. **Figure 4 adapters were not released.**
- **The released result files are derived patient-level data.** Never commit them.

## Claude Code task list

1. Confirm that Atul's PhysioNet credentialing, the MIMIC-IV v2.2 DUA and the HF gates (Llama 3, Gemma 2) are complete. Never request or accept row-level data in the session.
2. Clone ClinicalBench outside this repo. Install it and run the tests.
3. Write a `run_prepare.sh` wrapper for Atul that points `prepare_data.sh` at his local v2.2 `hosp` folder and checks the split files' hashes.
4. Re-score Table 2 from the released results. Save only the aggregate table to `studies/clinicalbench-labs/results/` (aggregate CSV).
5. Re-run the traditional baselines (indices 0–4) and one LLM (Gemma2-9B, logits) on all three tasks. Compare with the targets.
6. Log the package versions, GPU, `token_id_mode` and invalid rate for each run.
7. Start the extension pipeline in `extension.md`, beginning with the admission-time lab extraction SQL.
