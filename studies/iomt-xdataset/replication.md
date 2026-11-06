---
enriched: true
---
## What the original study did

Jaiswal, Andersen, Cenkeramaddi, Jiao and Granmo ([arXiv:2604.03205](https://arxiv.org/abs/2604.03205), April 2026; published at the 2026 Silicon Valley Cybersecurity Conference, [doi:10.1109/SVCC69905.2026.11642276](https://doi.org/10.1109/SVCC69905.2026.11642276)) built an intrusion detector for Internet of Medical Things (IoMT) networks from a Tsetlin Machine. This is a rule-based learner whose decisions are sums of votes from readable logical clauses. They trained it on CICIoMT2024 in three settings: Bluetooth Low Energy benign versus DoS (binary), Wi-Fi plus MQTT with six classes, and all protocols with seven classes, using the 11 features the two feature sets share. They compared it with eight standard classifiers and showed clause-vote heatmaps as explanations. The Tsetlin Machine was about as good as the trees on the binary task and better than them on the multi-class tasks, with inference times of a few microseconds per sample on a laptop.

**Companion paper.** Gueriani et al. ([arXiv:2604.06254](https://arxiv.org/abs/2604.06254); ISCTürkiye 2025, [doi:10.1109/ISCTrkiye68593.2025.11224819](https://doi.org/10.1109/ISCTrkiye68593.2025.11224819)) proposed a squeeze-and-excitation Vision Transformer plus BiLSTM detector and tested it on Edge-IIoTset and a six-class CICIoMT2024 subset. It used an 80/20 split with no separate test set. The near-equal class counts in its validation table suggest that oversampling happened before the split. It is useful here mainly as an example of the evaluation shortcuts the extension measures.

**Directly replicable.** CICIoMT2024 is free after a registration form. The source code is public under GPL-3.0 ([rkj08105/TM-driven-IDS](https://github.com/rkj08105/TM-driven-IDS)), but it holds only the Bluetooth notebooks (scenario 1). Scenarios 2 and 3 must be rebuilt from the paper's Tables III, V and VII. Because of the GPL, either keep any reused code under GPL-3.0 or write your own.

## Data

| Dataset | What | Access | How to get it |
| --- | --- | --- | --- |
| `ciciomt2024` | 40 IoMT devices (25 real, 15 simulated); Wi-Fi, MQTT and BLE captures; benign traffic plus 18 attack labels in five families for Wi-Fi/MQTT, and benign versus DoS for BLE. One feature CSV per capture, already in `train/` and `test/` folders | Free registration. No formal licence; the CIC datasets FAQ allows redistribution and mirroring with citation | Fill in the form at [cicresearch.ca/IOTDataset/CICIoMT2024](http://cicresearch.ca/IOTDataset/CICIoMT2024/) (linked from the [dataset page](https://www.unb.ca/cic/datasets/iomt-dataset-2024.html)). Download only `WiFi_and_MQTT/attacks/csv/` and `Bluetooth/attacks/` CSVs. Skip the pcaps (many GB) |
| `ciciot2023` (extension only) | 105 general IoT devices, 33 attack labels in 7 families, same window-feature extractor as CICIoMT2024 | Free registration, same CIC terms | [Dataset page](https://www.unb.ca/cic/datasets/iotdataset-2023.html). The CSVs are large; a stratified subsample is enough |
| `wustl-ehms-2020` (extension only) | 16,318 flows from a healthcare-monitoring testbed, with 35 Argus flow metrics and 8 biometrics; spoofing and data-alteration attacks | Open direct download; no licence stated | One 3.9 MB CSV from the [dataset page](https://research.engineering.wustl.edu/~jain/ehms/index.html) |

Keep all data under `data/` (gitignored) or outside the repo. The Wi-Fi/MQTT CSVs hold several million rows. Convert them once to parquet, and use `polars` or chunked `pandas` on a 16 GB laptop.

**Row counts to expect.** The Bluetooth files give 121,590 training and 31,704 test rows (code outputs). For Wi-Fi/MQTT, Table II of the source reports 6,987,390 training and 2,175,604 test rows, while Alruwaili et al. (*Sensors* 2026) report 7,160,831 and 1,614,182. Count your own and report which files you used.

## Environment

- The notebook metadata says Python 3.13.6. The paper names Keras on TensorFlow 2.2.0, which cannot run on Python 3.13, so treat the TensorFlow version as misreported. Use Python 3.11 for the widest package support.
- Packages: `pandas`, `numpy`, `scikit-learn` (`StandardScaler`, `KBinsDiscretizer`, `StratifiedKFold`), `imbalanced-learn` (SMOTE), `xgboost`, `lightgbm`, `tensorflow` or `torch` for the small neural network, `matplotlib`, and `seaborn`.
- Tsetlin Machine: the notebooks import both `pyTsetlinMachine` (`MultiClassTsetlinMachine`) and `tmu` (`TMClassifier`). Use `tmu` if `pyTsetlinMachine` will not build.
- Extension only: `shap`, `onnx`, `onnxruntime` (int8 quantisation), and `skl2onnx` or `hummingbird-ml` for tree models.
- A laptop CPU is enough.

## Step-by-step replication

1. **Load the CSVs by file name, not by `os.listdir` order.** The notebook reads `files[0..3]` from an unsorted directory listing, so labels can silently swap between machines. Map each file name to its label explicitly.
2. **Scenario 1 (BLE, binary).** Run `rkj_bt_TM_main.ipynb` and `rkj_bt_ML_main.ipynb` with the paths changed. Steps: drop missing values; drop duplicates within the training set and within the test set; SMOTE on the training data; `StandardScaler`; 5 quantile bins per feature, one-hot encoded; Tsetlin Machine with 100 clauses, T = 10, s = 2, 10 epochs. You should see 87,299 training rows after cleaning (34,291 duplicate DoS rows removed) and 30,512 test rows.
3. **Scenario 2 (Wi-Fi/MQTT, six classes).** Pool the 18 attack files into the five families plus benign. Same preprocessing as scenario 1. Tsetlin Machine with 100 clauses, T = 10, s = 5, 15 epochs (Table V). Use the 38 features the paper lists.
4. **Scenario 3 (all protocols, seven classes).** Keep only the features common to BLE and Wi-Fi/MQTT (11, as implied by the neural network's input layer in Table VII). Tsetlin Machine with 120 clauses, T = 15, s = 2, 15 epochs.
5. **Baselines.** DT, RF, XGBoost, LightGBM, KNN, NB, LR and a small neural network, with class weighting instead of SMOTE, as in the paper.
6. **Metrics.** Accuracy, macro precision, recall and F1, confusion matrices, and per-sample inference time. Also record MCC and the benign false-positive rate, which the paper omits.
7. **Explanations.** Rebuild the class-vote bar charts and clause-activation heatmaps for a few test samples per class.

## Compute and cost

A laptop: about 1–3 CPU-hours for all three scenarios, dominated by the Wi-Fi/MQTT Tsetlin Machine on several million rows (subsample the training set if needed, and report it). US$0. Downloading the CSVs needs a few GB of disk (verify the exact size after download).

## Target numbers

From the source paper (tables in arXiv:2604.03205 v1):
- **Scenario 1, BLE binary (Table IV):** Tsetlin Machine accuracy 0.995, precision 0.999, recall 0.991, F1 0.995. Several baselines score slightly higher (RF, XGBoost and LightGBM 0.998).
- **Scenario 2, six classes (Table VI):** Tsetlin Machine accuracy 0.907 and F1 0.906, against XGBoost 0.862, LightGBM 0.860, RF 0.816 and DT 0.803. The main error is confusion between DoS and DDoS.
- **Scenario 3, seven classes (Table VIII):** Tsetlin Machine accuracy 0.884 and F1 0.884, against XGBoost 0.851.
- **Inference time per sample:** Tsetlin Machine 0.74 µs (BLE), 4.06 µs (six classes) and 5.41 µs (seven classes) on an Apple M4 laptop.

From the companion (Table I): CICIoMT2024 six classes, 96.10% accuracy before balancing and 98.16% after. Do not try to match this number. It is the leakage-prone setup that the extension measures.

## Known pitfalls

- **Duplicates across the train/test boundary.** The code removes duplicates within each split but never checks rows that appear in both train and test. CIC features are averages over packet windows, so flood traffic produces many identical rows. Count the cross-split overlap before trusting any score.
- **Oversampling order.** The source applies SMOTE to the training set only, which is correct. The companion appears to oversample before splitting, which copies rows into the validation set.
- **Accuracy on a skewed class mix.** CICIoMT2024 Wi-Fi/MQTT is almost all attack traffic, so accuracy and weighted F1 flatter weak models. Report macro F1, MCC and the benign false-positive rate.
- **The "five-fold cross-validation"** in the notebook runs inside the training set with row-level shuffling. It is not a test of generalisation.
- **Features differ by protocol.** BLE has 27 HCI-based features; Wi-Fi/MQTT has about 38–45 window features. Scenario 3 discards most of them.
- **Version drift.** CIC has re-released feature files in the past. Record file names, row counts and download date.
- **Licence.** The code is GPL-3.0. CIC data have no formal licence, only the FAQ's permission to redistribute with citation; still, never commit the CSVs or derived row-level tables to this repo.
- **Defensive scope.** Use attack names only as class labels. Do not generate traffic, replay pcaps on a network, or publish anything that helps evade the detector.

## Claude Code task list

1. Create a separate analysis repo `iomt-xdataset-analysis/` with `data/`, `cache/` and `*.parquet` in `.gitignore`.
2. `fetch_notes.md`: record the CIC form date, file list, file sizes and SHA-256 checksums of the CSVs (data stay outside git).
3. `load_ciciomt.py`: build a file-name → label table (18 attack labels → 5 families + benign; BLE benign/DoS); convert to parquet; write `row_counts.csv`.
4. `audit_duplicates.py`: exact-duplicate counts within each file, within each split, and **across** train/test (hash of the feature vector without the label; also with the label, to find label conflicts). Aggregate counts only.
5. `replicate_tm.py`: scenarios 1–3 with the paper's hyperparameters; three seeds; save metrics as JSON.
6. `replicate_baselines.py`: the eight baselines with class weights; same metrics plus MCC and benign FPR.
7. `timing.py`: per-sample inference time on CPU, batch 1 and batch 1,024, with the hardware recorded.
8. `compare_targets.py`: table of reproduced versus reported numbers (Tables IV, VI, VIII), with differences.
9. Write `results/replication.md` with aggregate tables and figures only.
