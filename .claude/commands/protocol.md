---
description: Write the full study protocol for an approved study (then gate 2 is Atul's sign-off)
argument-hint: <slug>
---
Write `studies/<slug>/protocol.md` for: $ARGUMENTS

**Preconditions.** The study's `status` must be `approved`; otherwise stop and say what is needed. If `replication.md` or `extension.md` has `enriched: false`, run the `ingest-study` skill in `enrich` mode first. Read `CLAUDE.md`, `study.yaml`, `replication.md` and `extension.md`. If `notes.md` exists, it is **binding design direction**: follow it, and say where the protocol departs from the extension because of it.

Front matter `enriched: true`. Sections (`##`):
1. **Background**, with verified references: fetch every DOI/URL; never invent a reference; write `verify` when you can't confirm one.
2. **Aims and hypotheses**: primary and secondary.
3. **Data**: access steps, licence and the required citation for each dataset; DUA limits (e.g. no external LLM APIs on MIMIC).
4. **Cohort and inclusion/exclusion criteria**, with the expected numbers taken from the dataset documentation.
5. **Preprocessing**.
6. **Models and baselines**: include the clinical scores and simple models that reviewers will expect.
7. **Metrics**: discrimination, calibration, clinical utility (decision curves) where relevant, and efficiency.
8. **Statistical analysis plan**: confidence intervals (bootstrap), comparisons, multiplicity, missing data, and sample-size reasoning (e.g. Riley et al. for prediction models, events per predictor, or precision of AUC).
9. **Validation**: internal (with splits that avoid leakage), external and temporal.
10. **Reporting checklist mapping**: a table mapping each item of the named guideline (TRIPOD+AI, CLAIM 2024, TRIPOD-LLM, STARD-AI, …) to a protocol section.
11. **Compute and cost**.
12. **Risks and mitigations**.
13. **Week-by-week timeline** to a preprint.
14. **Repository layout** for the analysis code. Data stays outside git.
15. **Claude Code analysis task list**: numbered, runnable steps.
16. **Three candidate journals**, from `journals/journals.yaml` (zero-APC routes), with one line each on fit, plus the preprint server.

Then:
- `python3 scripts/set_status.py <slug> protocol "Protocol drafted; awaiting Atul's sign-off"`;
- set `links.protocol` in `study.yaml` to `studies/<slug>/protocol.md`;
- validate, check links (`python3 scripts/check_links.py studies/<slug>`), build, then commit `study: protocol for <slug>` and push.

Tell Atul that gate 2 is his sign-off of the protocol.
