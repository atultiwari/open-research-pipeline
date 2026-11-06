# Open Research Pipeline: rules for Claude

This public repo is Dr. Atul Tiwari's catalogue of study opportunities that can be replicated and extended on **open data**. Atul supervises, revises and approves; Claude does the legwork. The repo builds a GitHub Pages site from `site/`.

## Hard rules

1. **Open data only.** Each dataset's `access` must be `open`, `free-registration` or `credentialed` (e.g. PhysioNet MIMIC/eICU: credentialing plus CITI training, flag the 1–2 week wait). Never paid data. Never UK Biobank. If a source paper used private data, its `replication.md` says "not directly replicable" and proposes the closest open surrogate, or recommends rejecting the study.
2. **Never commit data.** No dataset files, no patient-level or derived row-level data, nothing from credentialed sources (the PhysioNet DUA forbids redistribution). Commit only metadata, links, code and aggregate results. `.gitignore` blocks common data formats; do not override it.
3. **Verify, never invent.** Fetch every URL you write. Never invent a DOI, URL, dataset name, licence, number or author list. If you cannot confirm a value, write `verify` in that field (the site shows a badge).
4. **Licences.** Record dataset and code licences exactly as stated. Flag non-commercial (NC), no-derivatives (ND) and gated access (e.g. Hugging Face models that need an institutional email). Flag mismatches between a dataset card and its paper.
5. **Copyright.** Summarise in your own words. Quote at most one short sentence. No copied abstracts or figures.
6. **Defensive security only.** Cybersecurity studies are defensive. Never commit exploit payloads, attack strings or universal adversarial perturbations.
7. **Reporting guidelines.** Name the right one for each study: TRIPOD+AI, CLAIM 2024, STARD-AI, TRIPOD-LLM, MI-CLEAR-LLM, CONSORT-AI, RECORD or STROBE.
8. **Plain, specific English** throughout.
9. **Polite API use.** Public APIs only, with a User-Agent naming the project (`open-research-pipeline/1.0 (+https://github.com/atultiwari/open-research-pipeline)`). Never put Atul's email in requests.

## Layout

| Path | What it holds |
| --- | --- |
| `studies/<slug>/study.yaml` | Metadata and status (source of truth) |
| `studies/<slug>/replication.md` | How to replicate on open data |
| `studies/<slug>/extension.md` | Gaps and new publishable studies |
| `studies/<slug>/notes.md` | Atul's notes: **binding design direction**, never overwrite |
| `studies/<slug>/protocol.md` | Written only after Atul approves |
| `datasets/<slug>.yaml` | Open-dataset registry |
| `journals/journals.yaml`, `journals/preprints.yaml` | Zero-APC shortlist, excluded list, preprint servers |
| `schema/*.schema.json` | JSON Schemas (mirrored by zod in `site/src/content.config.ts`) |
| `scripts/` | Python tooling (`pip install -r requirements.txt`) |
| `site/` | Astro site |

Markdown files under `studies/` start with front matter: `enriched: true|false`. Stubs from the migration are `enriched: false` until `/enrich` rewrites them.

## Status flow and Atul's three gates

`new` → **gate 1: Atul approves** → `approved` → `/protocol` → `protocol` → **gate 2: Atul signs off the protocol** → `analysis` → `drafting` → **gate 3: Atul approves the manuscript** → `preprint` → `submitted` → `published`. Side exits: `parked`, `rejected`.

Every status change appends `{status, date, note}` to `status_history`.

## Before every push

```bash
python3 scripts/validate.py
cd site && npm run build
```

Both must pass. Commit messages: `study: add <slug> (<area>)`, `study: <slug> → <status>`, `feat:`, `fix:`, `docs:`, `chore:`.

Scout and other automated runs open a PR on branch `scout/<YYYY-MM-DD>` instead of pushing to `main`.
