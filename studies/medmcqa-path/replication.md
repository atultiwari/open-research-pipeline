---
enriched: true
---
## What the original study did

Sadanandan and Behzadan (SAIL Lab, University of New Haven) tested how fragile Google's MedGemma is to the way a question is put to it. On the 4,183-item MedMCQA validation split they compared prompting styles (zero-shot direct, chain-of-thought, few-shot, a bare "answer-only" prompt), reordered the answer options (random shuffle, cyclic rotation by one or two places, swapping only the distractors), and tried three fixes: cloze scoring (pick the option letter with the highest next-token log-probability), permutation voting (majority vote over four orderings) and chain-of-thought self-consistency. A separate experiment truncated PubMedQA abstracts in different ways. The headline claims: chain-of-thought lowered MedGemma-4B accuracy by 5.7 points, few-shot prompts lowered it by 11.9 points and pushed the model towards option A, shuffling options changed the answer on 59% of items, and cloze scoring beat every prompt (51.8% for 4B, 64.5% for 27B).

- **Source:** [arXiv:2603.25960](https://arxiv.org/abs/2603.25960) (v1, 26 March 2026, cs.CL and cs.AI). An earlier version is on Research Square ([doi:10.21203/rs.3.rs-8759042/v1](https://doi.org/10.21203/rs.3.rs-8759042/v1), 3 February 2026). The code README calls the paper a camera-ready for "2AI 2025" (paper 183), but no proceedings record was found on Crossref or by web search on 2026-11-06, so the peer-reviewed venue is **verify**.
- **Code:** [UNHSAILLab/MedMCQA-Robustness-Study](https://github.com/UNHSAILLab/MedMCQA-Robustness-Study), MIT (GitHub API, 2026-11-06; last commit 17 June 2026). It holds the LaTeX source and PDF of the paper, a Colab notebook and the full pipeline (`main.py`, experiments 1–5).

**Replicability verdict: fully replicable on open data.** MedMCQA and PubMedQA are open and not gated. The only gate is MedGemma's Health AI Developer Foundations terms (accepted automatically on Hugging Face).

**This catalogue entry focuses on the MedMCQA part.** PubMedQA truncation is outside the pathology scope and close to the retrieval work in `medhallu-small`; replicate it only if the MedMCQA numbers do not match.

## Data

| Dataset (`datasets/` id) | What the paper used | Licence as stated (checked 2026-11-06) | Slice for this study | How to get it |
| --- | --- | --- | --- | --- |
| MedMCQA (`medmcqa`) | Validation split, 4,183 items, 21 subjects; train split for few-shot pools | HF card YAML: Apache-2.0, not gated. The card's own "Licensing Information" section says "Needs More Information"; the original GitHub repo ([medmcqa/medmcqa](https://github.com/medmcqa/medmcqa)) is MIT. Record both | **630 items**: Pathology 337, Biochemistry 171, Microbiology 122 (630 unique ids, no duplicate stems) | [openlifescienceai/medmcqa](https://huggingface.co/datasets/openlifescienceai/medmcqa), pin revision `91c6572c454088bf71b679ad90aa8dffcd0d5868`; the validation parquet is 1.5 MB |
| PubMedQA (`pubmedqa`) | `pqa_labeled`, 1,000 items | see `datasets/pubmedqa.yaml` | not used here | optional |

Aggregate facts about the slice, counted from the validation parquet on 2026-11-06 (nothing but counts leaves the scratch folder):
- **Key positions:** A 29.4%, B 27.6%, C 21.0%, D 22.1%. In the whole validation split they are A 32.2%, B 25.9%, C 22.1%, D 19.7%. A model that always answers "A" scores 32% on the full split, well above the 25% the paper uses as its chance line.
- **Item types:** 175 of 630 are `choice_type = multi`; 129 have a negative stem (not / except / false / least, by a simple regex); 43 have a position-anchored option ("all of the above", "none of the above", "both"), and in 11 of these that option is the key.
- **Explanations:** 338 items carry the dataset's explanation text, which helps the answer-key audit.
- **Exam tags:** 102 items are tagged AIIMS 2017–2020; the rest have no year.

**Storage:** download to `data/` (gitignored) in a separate analysis repo. Never commit item text, options, explanations or model outputs that quote them. The questions come from Indian entrance exams and coaching material, and their copyright is not addressed by either licence.

## Environment

From the repo's `requirements.txt`: Python ≥3.9 (use 3.11), `torch>=2.0`, `transformers>=4.40`, `datasets`, `bitsandbytes`, `accelerate`, `pydantic>=2.0`, `pyyaml`, `numpy`, `pandas`, `scikit-learn`, `matplotlib`, `seaborn`. Pin exact versions (`pip freeze > requirements.lock`) because the file gives only lower bounds, and Gemma-3-based MedGemma needs a recent `transformers`.

Models used: `google/medgemma-4b-it` and `google/medgemma-27b-text-it` (both "other" licence = Health AI Developer Foundations terms, auto-gated; checked on the HF API 2026-11-06). Run them at BF16. The README warns that 27B in 4-bit gives NaN outputs.

## Step-by-step replication

1. `git clone https://github.com/UNHSAILLab/MedMCQA-Robustness-Study && cd MedMCQA-Robustness-Study`, record the commit hash, `python -m venv venv && pip install -r requirements.txt`, `huggingface-cli login` after accepting the MedGemma terms.
2. `python main.py --verify` and `python main.py --test`, then `python main.py -e all -m 4b -l 100` as a smoke test.
3. Full MedGemma-4B runs: `-e prompt_ablation`, `-e option_order`, `-e cloze_score`, `-e permutation_vote`, `-e cot_self_consistency` (each `-m 4b`). Use `scripts/run_multi_seed.py` for seeds 42, 123 and 456 on the option-order experiment.
4. MedGemma-27B: `-e cloze_score -m 27b` on an 80 GB GPU (A100/H100). Run all 4,183 items, not only the 1,000 the paper used.
5. Re-score everything on the 630-item pathology slice by filtering on item id after the run (the repo has no subject filter).
6. Check the parser: save raw outputs (outside the repo) and re-score them with a strict parser (see Known pitfalls). Count unparseable outputs per condition, and how many chain-of-thought outputs hit the 256-token limit before giving a letter.

## Compute and cost

- MedGemma-4B on one 24 GB GPU (RunPod L4/A10/L40S): about 4,183 items × (10 prompt conditions + 5 orderings × 3 seeds + cloze + 4-way voting) ≈ 130,000 short generations plus about 8,400 chain-of-thought generations of up to 256 tokens. Roughly 6–10 GPU-h.
- MedGemma-27B cloze on all 4,183 items: one forward pass each, under 1 GPU-h on an 80 GB card.
- **Total: about 8–12 GPU-h on RunPod (roughly US$10–25). No paid API.** The Colab notebook runs 4B on a free T4 for spot checks.

## Target numbers

| Quantity | Paper value | Where |
| --- | --- | --- |
| Zero-shot direct, 4B | 47.6% [46.1, 49.1], position bias 0.137 | Table 4 |
| Zero-shot CoT, 4B | 41.9% (−5.7 points; 750 items lost, 512 gained) | Table 4, Appendix B table |
| Few-shot direct, 4B | 35.7%, position bias 0.472, predicts "A" on 76% of items | Table 4, Appendix C |
| Random shuffle / rotate-1 / rotate-2, 4B | 27.3% / 20.2% / 21.9%; flip rates 57.8% / 72.9% / 69.7% | Table 6 (seed 42) |
| Cloze scoring | 51.8% (4B, n = 4,183); 64.5% (27B, n = 1,000) | Table 8, Appendix F |
| Permutation vote K = 4, 4B | 49.0% vs mean single ordering 45.1%; agreement 70% | Appendix F (n = 1,000) |

Treat a difference of more than 2 points on the full split as a setup problem (chat template, parser, `max_new_tokens`). Report the same metrics on the 630-item slice as new numbers; the paper gives no per-subject results.

## Known pitfalls

- **Inconsistencies inside the paper.** Check these before trusting or citing the headline numbers:
  - The text says distractor swaps cost 8.9 points; the table says 0.0 points with a 36.1% flip rate.
  - The Methods promise 10 prompt conditions and three seeds with confidence intervals for option order; only five conditions and seed 42 are tabulated.
  - Cloze for 27B and permutation voting used 1,000-item subsets, so they cannot be compared directly with the 4,183-item 4B numbers.
  - The paper's ground-truth key distribution (A 32.2%, B 25.1%, C 21.4%, D 21.3%) matches the dataset only for A. The validation split gives B 25.9%, C 22.1%, D 19.7%.
  - CoT self-consistency appears in the Methods but has no results.
- **Rotations score below chance (20–22%).** That is what a model with a strong "A" habit does once the key moves away from A, combined with A-heavy keys. It is not evidence that the model has no knowledge. Report accuracy against an "always A" baseline (32.2%), not only 25%.
- **The answer parser is the biggest threat to the headline numbers (checked in the code, 2026-11-06).** `parse_mcq_answer` in `src/evaluation/metrics.py` is used by experiments 1 and 2. It upper-cases the output and, unless it finds the literal string "ANSWER:", returns the **first character anywhere in the text that is A, B, C or D**, including letters inside ordinary words. So "The answer is C" is scored as "A" (from "ANSWER"), and a chain-of-thought that opens "Based on the findings…" is scored as "B" whatever it concludes. This explains why fewer than 2.5% of outputs were unparseable. It probably inflates the "A" bias, and may make the CoT and few-shot penalties partly a parsing artefact. Do not replicate with this parser except as a reproduction check. Re-score with a strict parser (a bare letter, or a final "Answer: X" line) and report both.
- **The 256-token cap adds to this.** The paper's own worked example (Table 5) was cut off at 256 tokens before any conclusion, yet it was scored as "A". Re-run CoT with 1,024–2,048 tokens, take the *final* stated answer, and report truncation rates.
- **Naive shuffling breaks some items.** The shuffler (`src/perturbations/option_shuffle.py`) moves every option, including "all of the above"-type options, which then point at the wrong set. 43 slice items (335 in the full split) are affected. Keep anchored options in place, or analyse these items separately.
- **Noisy answer keys.** MedMCQA keys contain errors (Medmarks Appendix P found unclear or wrong items). An item with a wrong key counts a correct, order-stable model as wrong in every condition.
- **Contamination.** MedMCQA is old and public. Absolute accuracies of newer models are inflated; paired, within-item comparisons are less affected.
- **Licence mismatch.** The HF card says Apache-2.0 in its metadata but "Needs More Information" in its text, and the GitHub repo says MIT. Cite both. MedGemma outputs fall under the HAI-DEF terms.
- **Med-HALT overlap.** Med-HALT reasoning items reuse MedMCQA validation stems (see `datasets/medmcqa.yaml`). Do not add them as independent evidence.

## Claude Code task list

1. In a separate analysis repo, clone the source code and pin its commit. Add `data/`, `outputs/` and `*.jsonl` to `.gitignore`.
2. Write `slice_ids.py`: load the pinned MedMCQA validation parquet, check the subject counts (337 / 171 / 122 = 630) and save **only the ids** of the pathology slice to `slice_ids.json`.
3. Write `item_flags.py`: per item id, store flags only (anchored option and its position, negative stem, `choice_type`, explanation present). No text.
4. Run the five MedGemma-4B experiments and 27B cloze (steps 3–4 above), logging the commit, GPU, `transformers` version and the HF revisions of model and data to `outputs/meta.json`.
5. Write `rescore.py`: score every condition twice, with the original `parse_mcq_answer` and with a strict parser (bare letter or final "Answer: X"; otherwise unparseable). Report per-condition accuracy with Wilson CIs, position bias, flip rate and McNemar tests on (a) the full split and (b) the 630-item slice, with anchored items reported separately; add an "always A" baseline row.
6. Write `compare_paper.py`: put your numbers next to the target table above and flag gaps of more than 2 points.
7. Re-run zero-shot CoT with `max_new_tokens` 1,024 and report the truncation rate and the corrected CoT − direct difference.
8. Save aggregate tables only (`results/replication.md`, `results/*.csv`).
