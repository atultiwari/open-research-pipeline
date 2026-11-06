---
enriched: true
---
## What the original study did

Pandit and colleagues (UT Austin, UNC Chapel Hill, Drexel) built **MedHallu**, 10,000 PubMedQA research questions, each paired with its correct answer (the abstract's conclusion) and one hallucinated answer. Qwen2.5-14B wrote the hallucinated answers in one of four styles: question misinterpretation, incomplete information, mechanism misattribution, or evidence fabrication. Three filter LLMs (GPT-4o-mini, Gemma-2-9B, Qwen2.5-7B) then screened them, and an NLI model checked that each one really differed from the truth. How many filter models an answer fooled set its difficulty: easy, medium or hard. The authors then asked 14 LLMs (2B–14B open models, four medical fine-tunes, GPT-4o and GPT-4o-mini) to label single answers as hallucinated or not. They ran this with and without the abstract ("knowledge"), and with and without a "not sure" option. Main findings: hard items are hard (best hard F1 0.625, GPT-4o); the abstract helps a lot; general models beat medical fine-tunes; "not sure" raises precision.

The peer-reviewed version is in the *Proceedings of EMNLP 2025*, pp. 2858–2873 ([doi:10.18653/v1/2025.emnlp-main.143](https://doi.org/10.18653/v1/2025.emnlp-main.143), [ACL Anthology](https://aclanthology.org/2025.emnlp-main.143/)). The preprint is [arXiv:2502.14302](https://arxiv.org/abs/2502.14302) (v1 only, 20 February 2025). This guide uses the EMNLP text.

**Replicability verdict: fully replicable on open data, but expect only approximate numbers.** The dataset and code are open (MIT). However, the released detection script does not exactly match the paper's binary setting, and it samples answers at random without a seed (see pitfalls). Treat the paper's tables as targets to approach, not to match exactly.

## Data

| Dataset | What | Access | How to get it |
| --- | --- | --- | --- |
| MedHallu (`datasets/medhallu`) | 1,000 `pqa_labeled` + 9,000 `pqa_artificial` items; about 21 MB parquet | Open, not gated; MIT (card text) | `load_dataset("UTAustin-AIHealth/MedHallu", "pqa_labeled", revision="515060458a945c633debc6fd5baac7764416b724")` |
| PubMedQA (`datasets/pubmedqa`) | Source of MedHallu; gives PMIDs and MeSH terms | Open; MIT | `load_dataset("qiaojin/PubMedQA", "pqa_labeled")` (1 MB). Join to MedHallu on the exact question text |

Checked 2026-11-06 (HF API, datasets-server statistics, dataset card, GitHub API):
- **Licence:** the card metadata has no `license` field, but the card text states MIT, and the code repo is MIT. Record it as "MIT (card text)" and pin the revision above. Stanford's HELM scenario pins the same revision.
- **Join:** all 1,000 `pqa_labeled` questions match PubMedQA exactly, and every MedHallu "Ground Truth" is identical to PubMedQA's `long_answer`. "Knowledge" is the rest of the same abstract. The join gives you the PMID (needed to exclude the source during retrieval) and the MeSH terms (needed to define a lab-medicine subset).
- **Storage:** small enough for a laptop. Keep it outside the repo anyway (for example `~/data/medhallu/`). Never commit row-level files or model outputs that quote answers or abstracts.

## Environment

- **Paper (Appendix I):** PyTorch 2.4.0, CUDA 12.2, vLLM 0.6.3.post1 (tensor parallel 4, 4 × RTX A6000). The repo has no `requirements.txt`. Its README lists Python 3.8+, PyTorch, Transformers, vLLM and Sentence-Transformers.
- **Use for replication:** Python 3.11, a current `vllm` (needed for Gemma 4 / Qwen3.5 in the extension), `transformers`, `datasets`, `pandas`, `scikit-learn`, `scipy`, `statsmodels`, `matplotlib`. Pin exact versions in your own `requirements.txt` (MI-CLEAR-LLM).
- **Code licence:** [MedHallu/MedHallu](https://github.com/MedHallu/MedHallu) is MIT (GitHub API, 2026-11-06). Its `Detection/detection_vllm_notsurecase.py` can be reused with attribution. Rewriting the evaluator is still advised, because of the parsing and sampling issues below.

## Step-by-step replication

1. **Load and freeze the data:** load `pqa_labeled` at the pinned revision and join it to PubMedQA. Save the item IDs and a SHA-256 of the parquet in `results/medhallu/manifest.json`.
2. **Build the evaluation set, in two versions:**
   - *Paper-style:* for each item, pick the ground-truth or the hallucinated answer with a fair coin. The paper does this (released code, `run_evaluation`), but you must use a **fixed seed** and save the draw.
   - *Paired (recommended, as in MedHELM):* score **both** answers for every item, giving 2,000 judgements with balanced labels. Report both versions. The paired one is the reference for the extension.
3. **Prompts:** reimplement the binary detection prompt (paper Figure 7) with and without the "World Knowledge" block, which holds the PubMedQA context list. For the "not sure" arm, use the three-way prompt from the released script. The script puts the system text inside the user turn, so do the same.
4. **Decoding:** the paper used temperature about 0.2–0.3 (the script uses 0.3, top-p 0.95, max 512 tokens). Run once at the paper's settings to replicate. Then rerun greedily (temperature 0) as the clean reference. For a stability estimate, rerun three times at 0.3.
5. **Parse strictly:** accept only `0`, `1` or `2` as the first non-space token. Count anything else as invalid and report the invalid rate. Do **not** reuse the released parser (see pitfalls).
6. **Models (anchors from Table 2):** Qwen2.5-3B-Instruct, Qwen2.5-7B-Instruct, Llama-3.2-3B-Instruct, Gemma-2-2b-it and Llama-3.1-8B-Instruct, plus one medical fine-tune (BioMistral-7B). This covers the small-model end of the table, which the extension builds on.
7. **Metrics:** use the hallucinated answer as the positive class. Report overall precision, recall and F1; F1 by difficulty; and, for the "not sure" arm, the response rate. Add accuracy and balanced accuracy for comparison with MedHELM, with 95% bootstrap CIs (10,000 resamples, clustered by item in the paired version).
8. **Full set (optional):** repeat steps 2–7 on all 10,000 items to compare with Table 2 directly. It is cheap with small models.

## Compute and cost

- **Original:** generating the dataset took about 26.5 h on 4 × A6000 (Table 6). Detection compute is not reported.
- **This replication:** 6 models × 2 knowledge settings × 2,000 judgements (paired), plus the paper-style draw, comes to about 50k short generations. That is roughly 2–4 GPU-h on one 24–48 GB GPU (RunPod L4/L40S/A6000), about US$2–8. The full 10k set is about 5× that. An API is not needed. GPT-4o is optional and is left out.

## Target numbers

From Table 2 (10,000 items, single random answer per item):

| Model | F1 no knowledge | Hard F1 no knowledge | F1 with knowledge | Hard F1 with knowledge |
| --- | --- | --- | --- | --- |
| Qwen2.5-3B-Instruct | 0.606 | 0.556 | 0.676 | 0.661 |
| Qwen2.5-7B-Instruct | 0.553 | 0.402 | 0.839 | 0.770 |
| Llama-3.2-3B-Instruct | 0.499 | 0.384 | 0.734 | 0.664 |
| Gemma-2-2b-it | 0.553 | 0.457 | 0.715 | 0.631 |
| Llama-3.1-8B-Instruct | 0.522 | 0.372 | 0.797 | 0.722 |
| BioMistral-7B | 0.570 | 0.525 | 0.648 | 0.634 |
| GPT-4o (reference only) | 0.737 | 0.625 | 0.877 | 0.811 |

For `pqa_labeled` alone, use Table 9: data generated by Qwen2.5-14B, mean ± SD over three generation runs. Example: Qwen2.5-3B 0.606 → 0.676, Llama-3.1-8B 0.501 → 0.763. The released split is one of those runs.

Qualitative findings to reproduce:
1. Knowledge raises F1 for every general model, by an average of +0.25.
2. Hard F1 is lower than easy F1 for every model.
3. Medical fine-tunes gain less from knowledge than general models.
4. With "not sure" (Table 4), larger models abstain much more often: Qwen2.5-14B answers only 27.9% of items.

**External anchors:**
- Stanford [MedHELM](https://doi.org/10.1038/s41591-025-04151-2) scores both answers on `pqa_labeled` with knowledge (via the [HELM](https://github.com/stanford-crfm/helm) MedHallu scenario).
- A third-party harness reports that frontier and fast models reach about 87–95% accuracy there, and 66–83% with the abstract removed ([jev-medhallu-benchmark](https://github.com/stperic/jev-medhallu-benchmark), MIT; not peer-reviewed).

Use these to sanity-check the paired version.

## Known pitfalls

- **The released evaluator differs from the paper:**
  - Only the "not sure" script is released. The binary script behind Table 2 is not.
  - The script draws one answer per item with an **unseeded** `random.randint`, so every run and every model sees a different label mix.
  - Its parser labels any output containing "not" or "non" as *hallucinated*, before it checks for "not sure". So "not sure" and "non-hallucinated" both count as positives. This can inflate recall and distort the Table 4 response rates.
  - It reads column names (`least_similar_answer`, `final_difficulty_level`, a `knowledge` dict) that do not exist in the Hugging Face release. You must remap them.
- **Internal inconsistencies in the paper:**
  - Section 3 says a sample is kept when a *majority* of filter models are fooled; Section 4 says *at least one*.
  - The text gives Qwen2.5-7B's baseline F1 as 0.533; Table 2 says 0.553.
  - The Figure 4 caption names Qwen2-7B; the text and Figure 5 say Qwen2.5-7B.

  Note these in your write-up rather than "fixing" the targets.
- **Length artefact:** the paper limits hallucinated answers to ±10% of the ground-truth length. In the released `pqa_labeled`, only 14% meet that, and 75% are shorter (median 171 vs 251 characters; computed 2026-11-06 from the datasets-server rows). A length-only rule will beat chance. Report a length baseline next to every model.
- **The "knowledge" is an oracle:** it is the same abstract that the correct answer summarises. The with-knowledge setting is closer to a reading-comprehension (faithfulness) check than to real-world fact-checking.
- **Circular difficulty labels:** "hard" means all three filter models (GPT-4o-mini, Gemma-2-9B, Qwen2.5-7B) were fooled. Low hard-item scores for those same models, or their close relatives, are partly built in.
- **Machine-generated negatives:** no human checked whether each hallucinated answer is actually wrong, or whether each PubMedQA conclusion is a fair "truth". The `pqa_labeled` name refers to PubMedQA's yes/no/maybe labels, not to MedHallu's answers.
- **Licences of anchors:**
  - Llama 3.x needs manual Hugging Face approval;
  - Qwen2.5-3B uses the Qwen research licence (non-commercial);
  - Gemma 2 uses the Gemma terms.

## Claude Code task list

1. Create `analysis/medhallu/` (new code, MIT): `data.py` (load at the pinned revision, join to PubMedQA, write the manifest), `prompts.py` (Figure 7 binary prompt and the three-way prompt, with and without knowledge), `run.py` (vLLM, seeded, greedy and T=0.3 modes, outputs written to `~/data/medhallu/outputs/`), `parse.py` (strict parser and invalid counter), `metrics.py` (P/R/F1 by difficulty, balanced accuracy, response rate, clustered bootstrap CIs).
2. Unit-test `parse.py`: the released parser's failure cases ("not sure", "non-hallucinated", "0 - factual") must map correctly.
3. Smoke test: Qwen2.5-3B on 50 items, both versions, both knowledge settings.
4. Run the 6 anchor models on `pqa_labeled` (paper-style seeded draw and paired version). Write `results/medhallu/replication.csv` with aggregates only.
5. Compare with Tables 2 and 9. Log differences and their likely causes (draw, parser, decoding, vLLM version).
6. Compute the length-only and TF-IDF-overlap baselines (scikit-learn, 5-fold CV by item) and add them to the table.
7. Optionally run the full 10,000 items for the two Qwen2.5 anchors.
8. Commit only code, configs and aggregate CSVs and figures. Add `outputs/` and any `*.jsonl` that holds answers to `.gitignore` if they are not already covered.
