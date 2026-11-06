---
enriched: true
---
## What the original study did

Lee, Jang and Choi (Seoul National University Hospital) built **MPIB**, a benchmark of 9,697 items derived from MedQA and PubMedQA, to test whether prompt injection pushes LLMs into clinically harmful answers. Injected instructions arrive either in the user's message (**V1**, direct) or inside a retrieved document in a RAG-style context (**V2**, indirect). Benign (V0) and borderline (V0′) items measure over-refusal. An LLM judge (Qwen-2.5-72B-Instruct) gives each answer a harm type (H1 misdiagnosis to H5 evidence manipulation) and a severity from 0 to 4. The main metrics are **CHER₃** (share of attacked items judged severity ≥3), **ASR₂** (severity ≥2) and **FPR-H** (wrong refusals on benign items). The authors tested 13 open models (4B–72B, general and medical) under five defence settings, D0–D4. Two findings stand out: ASR and CHER can move apart, and the best defence depends on where the injection sits. The peer-reviewed version is in *Findings of EMNLP 2026* ([doi:10.18653/2026.findings-emnlp.1670](https://doi.org/10.18653/2026.findings-emnlp.1670)). The preprint is [arXiv:2602.06268](https://arxiv.org/abs/2602.06268) (v2, 25 August 2026).

**Replicability verdict: replicable on open data, with one large caveat.** The dataset is open (auto-approved gate). The released toolkit, however, is deliberately minimal: it rebuilds inputs, runs the subject model, and computes metrics from judge scores you have already produced. It does **not** include the judge pipeline or the D2–D4 defence prompts. You must rebuild those from the paper (Section 3.5 and Appendix S), so expect close but not identical numbers.

**Safety rule for this study (CLAUDE.md rule 6).** This is defensive work. Never write payloads, attack strings or example prompts into this repo, issues, logs or the manuscript. Describe attack categories in the abstract and report only aggregate metrics.

## Data

| Dataset | What | Access | How to get it |
| --- | --- | --- | --- |
| MPIB v1.2 (`datasets/mpib`) | 9,697 items: 2,734 V0, 5,737 V0′, 644 V1, 582 V2 (94 strict, 488 borderline). Splits: train 7,759, validation 969, test 969, grouped by source question | Free registration: Hugging Face gate, auto-approved; CC BY-NC 4.0 | Log in to Hugging Face, accept the terms on [jhlee0619/mpib](https://huggingface.co/datasets/jhlee0619/mpib), then `hf auth login` and `hf download jhlee0619/mpib --repo-type dataset --local-dir <path outside repo>` |

Checked 2026-11-06 (HF API and dataset page):
- **Gating and size:** `gated: auto`; total size 25.5 MB. Files: `data/train.jsonl`, `data/validation.jsonl`, `data/test.jsonl`, and `data/restricted/payload_registry.json`.
- **Redaction:** in the splits, the V2 poisoned passages are replaced by a redaction marker. The registry restores them.
- **Terms:**
  - non-commercial research, safety evaluation, education or defensive development only;
  - no clinical use;
  - do not redistribute or expose functional strings from the registry;
  - aggregate results and redacted records may be shared under CC BY-NC 4.0.
- **Source datasets:** MedQA ([jind11/MedQA](https://github.com/jind11/MedQA)) and PubMedQA ([pubmedqa/pubmedqa](https://github.com/pubmedqa/pubmedqa)) are both MIT on GitHub. The paper also says PubMedQA is MIT.

**Storage:**
- Keep the whole download, especially the registry, **outside the repository** (e.g. `~/secure/mpib/`, or a RunPod volume). Do not use `data/` inside the repo for the registry: `.gitignore` is a safety net, not a guarantee.
- Never paste registry content into a notebook that gets committed.

## Environment

- **Reference environment (repo):** `requirements.txt` pins only `vllm==0.6.6`, which the authors ran on CUDA 12.1. The metric script (`src/eval_operational.py`) needs only the Python standard library.
- **Use a newer vLLM.** vLLM 0.6.6 predates Gemma 4, Qwen3.5 and MedGemma 1.5, so the extension needs a current release. Pin the exact version in your own `requirements.txt` and record it in the paper (MI-CLEAR-LLM).
- **Other packages:** Python 3.10+, `transformers`, `huggingface_hub`, `pandas`, `numpy`, `scipy`, `statsmodels` (for McNemar and mixed models), `scikit-learn`, `matplotlib`.
- **Quantised inference (extension):** `llama.cpp` / `llama-cpp-python` for GGUF; vLLM for AWQ/W4A16 checkpoints.
- **Code licence:** [jhlee0619/mpib-eval](https://github.com/jhlee0619/mpib-eval) has **no licence file** (GitHub API, 2026-11-06). You may run it locally to check numbers, but **reimplement rather than copy** it into this project's code. The three scripts are short.

## Step-by-step replication

1. **Get access:** accept the MPIB gate and download v1.2 outside the repo. Confirm the split counts against the dataset card (7,759 / 969 / 969).
2. **Rebuild the inputs:** run the toolkit's reconstruction step on `test.jsonl`, passing the registry path explicitly so the V2 contexts are restored exactly. Write the output outside the repo. A run without the registry gives structural placeholders only, which is fine for testing the pipeline but not for results.
3. **Run the subject models:** use the authors' fixed system prompt and assembler as described in Section 3.5, with deterministic decoding (temperature 0) and the default that leaves contexts out of response files. To start, replicate three small anchors from the original matrix:
   - Qwen2.5-7B-Instruct;
   - Llama-3.1-8B-Instruct;
   - MedGemma-4B-it.
4. **Rebuild the judge:** take the system prompt, input fields and JSON schema (harm types, severity 0–4, refusal correctness, short rationale) from **Appendix S**. Run Qwen-2.5-72B-Instruct at temperature 0 with `max_tokens=1024`, then apply strict JSON validation. On one 80 GB GPU, the [AWQ checkpoint](https://huggingface.co/Qwen/Qwen2.5-72B-Instruct-AWQ) is the practical choice. **Record this as a deviation**, because the authors ran full precision on 4 × A6000.
5. **Compute the metrics:** use the operational convention, in which invalid judge outputs count as unsafe:
   - CHER₃ and ASR₂ per vector (V1, V2);
   - FPR-H on V0 items;
   - JSON validity, and valid-only sensitivity numbers.

   Reimplement the counting logic of `eval_operational.py` (≈ standard library) and check it against the original script on the same file.
6. **Rebuild the defences** from Section 3.5, without copying any prompt text into the repo:
   - D1: hierarchy hardening in the system prompt;
   - D2: input guard, with Qwen2.5-7B rewriting the user query;
   - D3: context sanitiser, with Qwen2.5-7B neutralising instructions in retrieved text;
   - D4: D2 and D3 coupled.

   These are reimplementations, so report them as "D1–D4 (reimplemented)".
7. **Add 95% bootstrap CIs** (10,000 resamples), as in Appendix N. Cells are small: about 67 V1 and 64 V2 test items per model × defence cell, inferred from the reported percentages (**verify** against `test.jsonl`).
8. **Run an expert audit:** Atul blindly re-scores a stratified sample (for example 100 responses) for severity and harm type. Report weighted κ against the judge. This mirrors the paper's Tier-2 audit.

## Compute and cost

- **Original:** about 800 GPU-hours on 4 × RTX A6000 for the whole matrix, judge selection and cross-validation (Appendix M).
- **Replication of 3 small anchors × D0–D4 on the test split:**
  - subject inference: about 2–4 GPU-h on one L40S/A100;
  - judging with Qwen2.5-72B-AWQ: about 3–6 GPU-h on an A100 80 GB / H100.
  - Total: about 10 GPU-h on RunPod (roughly US$15–30). Laptop for analysis.
- No paid API is needed. The paper's frontier-model check (Appendix O) is optional and is not part of this replication.

## Target numbers

From Table 5 (operational convention, test split, %):

| Model | Defence | V1 CHER₃ | V1 ASR₂ | V2 CHER₃ | V2 ASR₂ | FPR-H |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-7B | D0 | 70.1 | 80.6 | 12.5 | 60.9 | 5.6 |
| Qwen2.5-7B | D2 | 59.7 | 77.6 | 14.1 | 67.2 | 6.8 |
| Llama-3.1-8B | D0 | 76.1 | 85.1 | 20.3 | 57.8 | 8.5 |
| MedGemma-4B | D0 | 88.1 | 95.5 | 21.9 | 64.1 | 11.7 |

Qualitative findings to reproduce:
1. V1 CHER is much higher than V2 CHER for most models.
2. Under V2, ASR₂ is far above CHER₃, so most V2 failures are severity 2.
3. D2 tends to lower V1 CHER, and context-side defences (D3/D4) tend to lower V2 CHER, but neither is uniformly best.
4. The lowest V1 CHER₃ in the whole matrix is 50.7%.

Judge check: Kendall τ 0.65 and Recall@4 0.75 for Qwen-2.5-72B on the authors' selection set (Table 2). That set is not released, so you cannot reproduce it. Use Atul's audit instead.

## Known pitfalls

- **Payload hygiene:**
  - responses, judge inputs and judge rationales can echo injected text, so keep all row-level files outside the repo;
  - commit only aggregate tables;
  - never use `--include_contexts` for anything you might share.
- **The judge dominates the results.** The authors call absolute rates "controlled estimates". V2 rankings changed against a Qwen-2.5-32B judge (Spearman 0.46). A quantised judge, a different vLLM version or different JSON handling will shift the numbers. Report judge model, quantisation, version and invalid-output rate.
- **Defences are reimplemented.** The released toolkit does not include the D2–D4 prompts, so differences from Table 5 are expected. Do not present them as a failed replication.
- **Small cells:** about 64–67 adversarial items per cell gives 95% CIs of roughly ±11 percentage points. Use paired tests across settings on the same items.
- **V2 is a post-retrieval audit**, not end-to-end RAG security: every V2 item contains at least one poisoned passage (Section 3.2).
- **Ill-posed items:** 17 test items were judged ill-posed by both raters (Appendix Q). Two are flagged with `labels.wellposed_audit` in v1.2. Report results with and without them.
- **Licences:**
  - MPIB is CC BY-NC (non-commercial);
  - MedGemma uses Health AI Developer Foundations terms (auto-gated);
  - Llama models need manual approval on Hugging Face;
  - Qwen2.5-72B uses the custom Qwen licence.

## Claude Code task list

1. Atul accepts the MPIB gate on Hugging Face. Download v1.2 to a path **outside** the repo, and record the path in an untracked `.env` file.
2. Write `analysis/mpib/` code (new, own licence):
   - `assemble.py`: build the prompt from the redacted record plus the restored context in memory;
   - `run_subject.py`: run vLLM or llama.cpp at temperature 0, writing responses to the external path;
   - `judge.py`: implement the Appendix S schema, with strict JSON validation;
   - `metrics.py`: CHER₃, ASR₂, FPR-H, JSON validity, bootstrap CIs.
3. Smoke test: build structural placeholders without the registry, and run one model on 20 items to check the pipeline.
4. Check `metrics.py` against the authors' `eval_operational.py` on the same judge file. The counts must match exactly.
5. Run the 3 anchor models × D0 on the test split, then judge with Qwen2.5-72B-AWQ.
6. Compare with Table 5. Log the differences and likely causes (judge quantisation, prompt assembly).
7. Reimplement D1–D4, then run and judge them.
8. Export a stratified audit sheet of 100 items: model and defence hidden, with **no injected context included**. Atul scores it. Compute weighted κ.
9. Commit only code, configs and aggregate CSVs/figures (`results/mpib/*.csv`). Add a pre-commit grep that blocks any file containing the redaction marker or text from the registry.
