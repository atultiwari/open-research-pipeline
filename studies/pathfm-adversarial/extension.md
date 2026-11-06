---
enriched: true
---
**Defensive scope.** This study measures how much harm a few invisible patch changes can do to a foundation-model pipeline, and tests cheap ways to detect and blunt them. It never publishes attack code, attack settings, perturbed images or perturbations, and it never builds or releases a universal perturbation (CLAUDE.md rule 6). Attack families are named only in the abstract.

## Where the field stands (checked 2026-11-06)

- **Source, v1** (Liu et al., [arXiv 2505.24141](https://arxiv.org/abs/2505.24141), May 2025): three **slide-level** foundation models (CHIEF, TITAN, PRISM), each with its own frozen, pretrained aggregator, and MLP heads on top. Label-free white-box attacks on one random patch. Defence: uniform input noise.
- **Source, v2** (SSRN 2026, [doi:10.2139/ssrn.7383688](https://doi.org/10.2139/ssrn.7383688), not peer-reviewed): five slide-level models (the repo names CHIEF, PRISM, Prov-GigaPath, TITAN and FEATHER), eight tasks, and three input-transformation defences (bit-depth reduction, Gaussian blur, randomised smoothing). The repo also has a script that reuses noise across patches and slides within one model. Whether v2 reports **cross-model** transfer: **verify** (full text blocked, HTTP 403).
- **UTAP** (Wang, Yang, … Ozcan, UCLA; [Light Sci Appl 2026, doi:10.1038/s41377-026-02347-w](https://doi.org/10.1038/s41377-026-02347-w); preprint [arXiv 2510.16660](https://arxiv.org/abs/2510.16660)): a single fixed, universal perturbation optimised on UNI2-h that transfers to six other **patch-level** encoders, tested with **linear probes on patches** (NCT-CRC-HE-type and several out-of-distribution sets) and on the slide-level assistant SlideChat. Defences tested: a low-pass filter (bypassed once the attacker accounts for it), robustness tokens (little help, sometimes worse) and a separate CNN that detects perturbed patches (very high detection rates on its own perturbation). The authors name MIL-based slide models as future work. **This paper already covers patch-level transferability and a detector, so the stub's "cross-FM transferability" angle is no longer new on its own.**
- **Other pathology adversarial work:**
  - Ghaffari Laleh et al., *Nat Commun* 2022: patch-level CNNs and ViTs under labelled attacks, before foundation models.
  - [HSAT](https://arxiv.org/abs/2503.10629) (MICCAI 2025): adversarial training for histopathology patch models (OpenSRH).
  - [SAWR](https://arxiv.org/abs/2606.08745) (BMVC 2026): stain-aware wavelet purification of perturbed patches.
  - [Adversary-robust graph WSI learning](https://arxiv.org/abs/2403.14489) (2024): a denoiser for graph-based prostate grading, no foundation models.
  - Thota et al., ISBI 2024: an attack on a pathology vision-language model.
  - Ziaullah et al., ICECET 2026 ([doi:10.1109/icecet65726.2026.11632529](https://doi.org/10.1109/icecet65726.2026.11632529)): adversarial evaluation of multi-organ classification with CNNs and foundation models. Abstract not available; whether it uses MIL: **verify**.
- **Natural (non-adversarial) robustness with MIL heads:** PathoROB (Kömen et al., [Nat Commun 2026](https://doi.org/10.1038/s41467-026-73923-2), 20 encoders, robustness index); Moalin et al. (NeurIPS 2026, 12 encoders, plus six encoders with Attention-MIL on TCGA-BRCA under blur, stain and spatial corruption); Yajnik et al. ([arXiv 2607.04401](https://arxiv.org/abs/2607.04401)); Carretero et al. ([arXiv 2609.28231](https://arxiv.org/abs/2609.28231), centre bias through ABMIL/TransMIL). **None of these includes adversarial perturbations.**

**Searches run on 2026-11-06** (OpenAlex was out of its daily budget, so the skill's fallback order was used):
- **Semantic Scholar, citations of arXiv:2505.24141:** 1 result (a few-shot feature-augmentation paper in *Bioinformatics*, not about attacks). Semantic Scholar keyword search then returned HTTP 429 for all four queries: **rate-limited, not checked**.
- **Crossref** (from 2024-06-01, top 20–30 each): "Butterfly Effect in Pathology foundation models adversarial"; "adversarial attack multiple instance learning whole slide image"; "adversarial robustness pathology foundation model"; "transferable adversarial perturbation histopathology foundation model"; "adversarial example detection histopathology"; "adversarial defense histopathology stain normalization JPEG"; "universal adversarial perturbation whole slide image". Found the SSRN v2, UTAP (journal and Optica abstract), and ICECET 2026. No MIL adversarial study.
- **Europe PMC** (from 2024-01-01 or 2024-06-01): `"pathology foundation model" AND adversarial`; `adversarial AND (histopathology OR "whole slide" OR "computational pathology")`; `adversarial AND "multiple instance learning"`; `"adversarial attack" AND pathology AND (defense OR defence OR detection)`; `adversarial AND "foundation model(s)" AND (pathology OR histology OR microscopy)`; a title-restricted query; `ABSTRACT:"adversarial attack" AND ABSTRACT:"whole slide"` (0 hits). Only UTAP and PathoROB were relevant.
- **arXiv API** (3 searches, ≥6 s apart, sorted by date): `abs:adversarial AND (abs:pathology OR abs:histopathology) AND abs:foundation` (18 results); adversarial/perturbation AND ("multiple instance" OR "whole slide") AND (attack OR robustness) (33); adversarial AND histopathology AND (attack OR defense OR purification) (8). Relevant hits: UTAP, SAWR, HSAT, the source, and the 2024 graph-WSI paper.
- **Web search** (3 queries: adversarial attack + MIL + pathology foundation models + transferability + defence; pathology foundation models adversarial benchmark ABMIL/CLAM + detection; natural versus adversarial robustness correlation). Found the NeurIPS 2026 corruption study and a public review of UTAP noting that MIL aggregation was not tested.
- **GitHub:** the source repo (no licence; scripts for attacks, three defences, and within-model noise transfer).

**Bottom line:** no study has tested sparse, label-free perturbations against the pipeline most groups actually build, **a patch-level encoder plus a task-trained attention-MIL head**, across current encoders. None has measured the **clean-data cost** (accuracy and false alarms) of cheap defences at slide level, or used the MIL **attention map itself** as a detector. The novelty check is reasonably complete, with one hole: Semantic Scholar keyword search and OpenAlex citation search could not be run. **Rerun both before the protocol.**

**Overlap inside this repo:** `stain-robust-camelyon` (natural stain robustness of foundation-model MIL on CAMELYON16 → 17) and `plism-scanner` (scanner and smartphone drift) study **natural** shifts. This study is the **adversarial** counterpart. Reuse their feature extraction and ABMIL heads where the encoders match, so Gap 5 can link the three.

### Gap 1: Patch-level encoders with task-trained attention-MIL heads are untested

- **Evidence:** the source attacked slide-level models with frozen pretrained aggregators and MLP heads (v1 Section 5.1). v2 adds FEATHER, a pretrained ABMIL-type slide encoder, but still no task-trained MIL head. UTAP used linear probes on patches and SlideChat, and lists MIL as future work. Most published pipelines (CLAM, ABMIL, TransMIL on UNI2-h, Virchow2 or H-optimus features) train the aggregator for each task. Its attention can either dilute one bad patch or hand it the whole decision; nobody has measured which.
- **Novelty check:** all searches above. No study pairs adversarial perturbations with task-trained MIL on 2025–26 encoders. **Novel as of 2026-11-06** (Semantic Scholar keyword search not checked).
- **Open data:** `camelyon16`, `tcga` (NSCLC: LUAD vs LUSC), with `conch-v15-features-tcga`, `uni2h-features-tcga`, `virchow2-features-tcga` and `gigapath-features-tcga` to train the TCGA heads without downloading every slide.
- **Design sketch:**
  - *Hypothesis:* with a task-trained ABMIL head, changing one to four patches flips a clinically meaningful share of slide diagnoses, more for normal-to-tumour flips on CAMELYON16 (the MIL "one positive patch" logic), and vulnerability differs across encoders in a way not explained by clean accuracy or parameter count.
  - *Encoders (7):* UNI2-h, Virchow2, H-optimus-0, H-optimus-1 (if approved), Phikon-v2, Prov-GigaPath tile encoder, Midnight (kaiko, MIT), plus CONCH v1.5 for continuity with TITAN. ResNet-50 (ImageNet) as a baseline.
  - *Heads:* ABMIL (main) and CLAM-SB; TransMIL as a sensitivity check on one encoder.
  - *Threat model:* encoder weights known (they are public or obtainable by registration), task head and labels unknown, as in the source. Label-free objective on the slide embedding before the head.
  - *Efficiency:* cache clean features; only the few perturbed patches are re-encoded, so each attack is far cheaper than in the source, where the whole slide went through the slide encoder.
  - *Data:* CAMELYON16 official train (270) / test (129) split, plus TCGA-NSCLC 5-fold with an attacked subset of about 150 test slides.
  - *Metrics:* attack success rate (decision flips) and AUROC/accuracy drop with bootstrap CIs; flips split by direction (missed metastasis versus false metastasis); patch-count curve for 1, 2, 4 and 8 patches; vulnerability versus encoder size (tests the source's "butterfly" claim with 8 encoders instead of 3).
  - *Reporting guideline:* CLAIM 2024, with a pre-specified threat model and the standard adversarial-evaluation reporting items (budget, attacker knowledge, adaptive evaluation).
- **Rating:** feasibility 3 (gated models; WSI handling), novelty 4, RunPod, 4 weeks.

### Gap 2: Does the MIL attention map give the attack away? (attention-based detection)

- **Evidence:** the source found the attacked patch's tissue type matters (Section 5.4) and lists extractor-versus-aggregator disentanglement as limitation 3 (Section 6.2). In ABMIL, a perturbed patch that flips a slide probably has to win a large share of attention. That makes it visible in the heatmap a pathologist already looks at. UTAP's detector is a separate CNN trained on its own perturbation, which may not generalise to sparse, slide-specific changes.
- **Novelty check:** no study found using MIL attention concentration, embedding outlier scores or encoder disagreement to detect adversarial patches in WSIs (all searches above). **Novel as of 2026-11-06.**
- **Open data:** as Gap 1.
- **Design sketch:**
  - *Detectors, all label-free and cheap:* (a) attention concentration (top-1 attention share, attention entropy) relative to the clean distribution for that task; (b) Mahalanobis or k-NN outlier score of each patch embedding against the slide's own patches; (c) disagreement between two encoders' slide predictions (an attacker who knows one encoder may not move the other); (d) prediction change under small test-time augmentation of the top-attended patches.
  - *Outcomes:* slide-level detection AUROC; false-alarm rate on clean slides, expressed as flagged slides per 100 routine cases; detection rate at a fixed 1% false-alarm rate.
  - *Pathologist audit:* Atul reviews, blinded, the top-attended patches of flagged and unflagged slides and records whether he would have noticed anything (an expert-in-the-loop check, not a perceptibility claim).
  - *Defence-aware check:* repeat with an attacker who also tries to keep attention spread out, and report the cost to the attacker (lower success). Settings stay in the private repo.
- **Rating:** feasibility 4 (reuses Gap 1 runs), novelty 4–5, RunPod (small), 2 weeks on top of Gap 1.

### Gap 3: Cheap input defences, and what they cost on clean slides

- **Evidence:** v1 tested uniform noise on two tasks (Section 5.5); v2 tested bit-depth reduction, blur and randomised smoothing (repo README); UTAP tested a low-pass filter. None reported the clean-slide cost in terms a laboratory would use (missed metastases per 100 negative slides), and none tested the transforms that pipelines already apply: **JPEG re-encoding** at the quality WSI formats already use, and **stain normalisation** (Macenko/Reinhard), which many sites run anyway.
- **Novelty check:** Crossref "adversarial defense histopathology stain normalization JPEG" and arXiv query 3 found SAWR (wavelet purification, patch level) and general-domain JPEG defences, but no slide-level MIL evaluation of JPEG or stain normalisation as adversarial defences. **Partly novel.**
- **Open data:** as Gap 1.
- **Design sketch:**
  - *Defences:* uniform noise (the source's, as a reference), JPEG re-encoding, Macenko and Reinhard normalisation, randomised smoothing on the top-k attended patches only (cheap), and an encoder ensemble.
  - *Outcomes:* robust accuracy recovered; clean AUROC change; extra GPU time per slide; all with defence-aware evaluation as well as the naive case.
  - *Scope control:* run the full defence grid on three encoders (the most and least vulnerable from Gap 1, plus H-optimus-0 as the open Apache-2.0 model) on CAMELYON16 only, because each defence re-encodes every patch of the test slides.
- **Rating:** feasibility 3 (compute-heavy), novelty 3, RunPod, 2 weeks.

### Gap 4: Does keeping your encoder private help? (grey-box transfer between encoders)

- **Evidence:** in a hospital, the encoder in use may be a gated, non-commercial model, while an attacker can freely download an Apache-2.0 or MIT encoder (H-optimus-0, Prov-GigaPath, Midnight). UTAP shows universal patch perturbations transfer between encoders; nobody has measured whether **sparse, slide-specific** changes made on one encoder flip a **different** encoder's MIL head.
- **Novelty check:** UTAP covers transfer for universal patch perturbations with linear probes. Whether SSRN v2 covers cross-model transfer of sparse WSI perturbations: **verify**. **Partly novel.**
- **Open data:** as Gap 1.
- **Design sketch:** a source × target transfer matrix (8 × 8 encoders) of decision-flip rates on CAMELYON16, from the Gap 1 perturbations held in memory and evaluated on the other encoders' heads in the same run. Frame the result as a deployment question ("is an obscure encoder a defence?"). Report the matrix only; never store or share the perturbations.
- **Rating:** feasibility 4 (cheap once Gap 1 runs), novelty 3, RunPod, 1 week. A strong secondary analysis.

### Gap 5: Are encoders that resist scanner and stain shifts also harder to attack?

- **Evidence:** PathoROB, PLISM-based work, Moalin et al. and Yajnik et al. rank encoders on natural robustness, and the source and UTAP rank them on adversarial robustness, but nobody has correlated the two rankings for the same encoders. If they agree, labs can use one cheap natural-robustness test as a proxy; if not, they need both.
- **Novelty check:** web search for natural versus adversarial robustness correlation in pathology foundation models (2026-11-06) found the two literatures measured separately and no correlation study. **Novel as of 2026-11-06**, but small (n = 8 encoders).
- **Open data:** Gap 1 results, published PathoROB robustness indices, and `plism` (via `plism-scanner`) for a self-measured natural-robustness score.
- **Design sketch:** Spearman correlation, with bootstrap CIs over slides, between each encoder's adversarial flip rate (Gap 1) and its natural-robustness score (PLISM cross-scanner similarity, CAMELYON16 → 17 drop from `stain-robust-camelyon`). Treat it as descriptive, given eight points.
- **Rating:** feasibility 5, novelty 3, laptop, 1 week.

### Gap 6: Threat plausibility in a real laboratory, with an Indian framing

- **Evidence:** the source's threat model assumes an adversary who can change pixels between scanner and model (Section 3) but does not say where that could happen or what simpler controls would stop it. UTAP sketches injection points and a rescan protocol. Neither paper discusses non-ML controls (file hashing at the scanner, DICOM-WSI integrity, access logging) or LMIC deployment, where cloud-hosted inference on gated models is likely.
- **Novelty check:** no pathology adversarial paper found with an Indian or LMIC deployment framing (all searches above).
- **Design sketch:** a structured threat-plausibility table, written by Atul. Columns: pipeline step (scanner, local storage, PACS/LIS, transfer to cloud, inference), who can touch the file, what a pixel change requires, and the cheapest control (hash at acquisition, signed transfer, audit log). Map each control to the Digital Personal Data Protection Act 2023 and CERT-In reporting duties (verify current rules before writing). This is the discussion section, not a separate paper.
- **Rating:** feasibility 5, novelty 2 on its own, laptop, 1 week of expert time.

## Recommended extension

**Gaps 1 + 2 together, with 3 on a reduced grid, and 4–6 as secondary analyses:** "Can one or two invisible patch changes flip slide-level diagnoses in foundation-model MIL pipelines, and does the attention map give them away? A defensive benchmark of eight patch-level pathology encoders on CAMELYON16 and TCGA-NSCLC."

Why this one:
- **It is the remaining clear gap.** UTAP has taken "cross-encoder transferability", and v2 of the source covers slide-level models with input defences. Task-trained attention-MIL on current patch encoders, and attention-based detection with its false-alarm cost, are untested.
- **It is defensive by design.** The main outputs are vulnerability rates, detection AUROC at a fixed false-alarm rate, and the clean cost of cheap defences. Attack implementations come from a maintained library, run in a private repo, and nothing reusable is published.
- **It plays to a pathologist.** CAMELYON16 metastasis detection is a task Atul reads daily; the flip direction (missed metastasis versus false positive) has a clear clinical meaning; and the blinded attention-patch audit and the threat-plausibility table are expert contributions an ML group would not have.
- **It is affordable.** Caching clean features means only a handful of patches are re-encoded per attack. The expensive part is the defence grid, which is limited to three encoders on CAMELYON16. Estimate: about 80–150 GPU-h on RunPod (A100/L40S), roughly US$100–250 (verify current prices), plus streaming CAMELYON16 (762.5 GB in full) and about 150 TCGA-NSCLC test slides (about 120 GB).
- **Risks:** gated models (H-optimus-1 needs manual approval); attack strength depends on settings, so fix them in advance and report defence-aware results; small encoder count for the size and natural-robustness correlations; possible overlap if SSRN v2 or a UTAP follow-up adds MIL heads. Check both again before the protocol.

Expected time: about 8 weeks to an arXiv (cs.CV / eess.IV) preprint. Candidate zero-APC journals:
- Journal of Medical Systems (clinical AI and system security);
- Journal of Imaging Informatics in Medicine (WSI AI tools);
- Computerized Medical Imaging and Graphics.
