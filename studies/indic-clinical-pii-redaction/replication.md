---
enriched: true
---
## What the original study did

CobuildX-AI released three small token-classification models (16.7M, 36.5M and 57.6M parameters) on Hugging Face on 2026-11-05. They find personal information in Indian text and return each value's exact position with one of 27 labels. The labels include Aadhaar, PAN, ABHA (as NATIONAL_ID), PATIENT_ID (MRN/UHID), names, phones, addresses, dates of birth and other dates. The models read 12 Indian languages and Indian English, in native script, romanised and code-mixed.

The 58M model is mmBERT-small fine-tuned on about 74,000 synthetic documents with its vocabulary cut to 40,000 tokens. The 36M and 17M models are layer-pruned copies distilled from an unreleased 307M teacher.

On the IndicPIIDetX test split, typed F1 is 0.930 (58M), 0.888 (36M) and 0.869 (17M), with precision of about 0.94 for all three. CPU time is 5–16 ms per short text. The cards report fewer false alarms on PII-free documents than the Chitragupta model (13–20% vs 53%).

There is no paper. The cards themselves list the limitations:
- Names written in native script are missed more often by the small sizes.
- PATIENT_ID and NATIONAL_ID are found less reliably than names, phones and emails.
- Every date is labelled, even dates not tied to a person.
- Health attributes are not detected.
- Training data was synthetic only.

**Directly replicable.** The models (Apache-2.0) and all three benchmarks (CC BY 4.0, CC0) are open and not gated.

## Data

| Dataset | What | Access |
| --- | --- | --- |
| IndicPIIDetX v0.1 | 10,035 synthetic documents (8,028 test), 27 labels, 13 languages × 3 writing styles; ~1,000 healthcare-domain documents | Open, CC BY 4.0 (`datasets/indicpiidetx`) |
| Ylemis India-PII | 10,000 synthetic cases, 16 entity types including `medical_id` | Open, CC0 (`datasets/ylemis-india-pii`) |
| IndiaPII-Bench | 2,000 adversarial documents, 286 of them medical notes, with labelled look-alike codes | Open, CC BY 4.0 (`datasets/indiapii-bench`) |

All three are small (tens of MB); download them to `data/`.

## Environment

From each model repo's `requirements.txt`: `torch>=2.1`, `transformers>=5.0`, `safetensors>=0.4`; optionally `onnxruntime>=1.23` for the ONNX file. Load the models with the bundled `pii.py` (`PIIExtractor`), not plain `AutoModel`: the 17M model uses a compressed embedding table. The ONNX model uses a Microsoft-specific attention operator, so it needs ONNX Runtime.

## Step-by-step replication

1. `hf download CobuildX-AI/cbx-indic-pii-extractor-{17M,36M,58M}`; `pip install -r requirements.txt`; run `example.py`.
2. Download the three benchmarks.
3. Reproduce typed F1 the way the card describes it:
   - map labels to the 14 shared types;
   - count a prediction if it overlaps a gold span of the same type;
   - join adjacent same-type pieces.
   Also run each benchmark's own scorer.
4. Report precision, recall, F1, and the share of PII-free documents flagged, per language and writing style.
5. Time each model on CPU (8 threads) and through ONNX Runtime on the same laptop.
6. Add the baselines from the card that are public: the Chitragupta PII model (`LatentAILabs/chitragupta-pii-indic`, Apache-2.0) and GLiNER-PII.

## Compute and cost

A CPU laptop is enough. Inference on about 20,000 short documents takes minutes. No GPU is needed.

## Target numbers

- **IndicPIIDetX test, typed F1 (precision / recall):** 58M 0.930 (0.945 / 0.915); 36M 0.888 (0.943 / 0.839); 17M 0.869 (0.943 / 0.806).
- **PII-free documents flagged:** 19.9%, 13.4%, 16.2%.
- **Ylemis typed F1:** 0.986 / 0.981 / 0.982. **IndiaPII-Bench:** 0.946 / 0.958 / 0.944. The cards say these two benchmarks shaped the training data, so they are not blind tests.
- **CPU speed (17M):** ~11 ms per short message, 72 ms per 2,000-character document.

## Known pitfalls

- **Same-group benchmark:** IndicPIIDetX was made by the model authors, with a different generator but the same team.
- **Typed-overlap F1 is lenient.** A partial name match counts as found, but for redaction a half-redacted name is a leak. Also report exact-span and character-level recall.
- **Precision-oriented models:** recall (leakage) matters more for privacy than precision. Report recall first.
- **AMOUNT and DATE** label every amount and date, so benchmarks that label only personal ones count these as false alarms.

## Claude Code task list

1. Download the three models and three benchmarks into `data/`; run the examples.
2. Write `eval/score.py` with typed-overlap, exact-span and character-level recall, plus the PII-free flag rate.
3. Reproduce the card tables; flag any gap greater than 0.02 F1.
4. Add the Chitragupta and GLiNER-PII baselines; time all models on CPU.
5. Commit the scoring code and aggregate tables only.
