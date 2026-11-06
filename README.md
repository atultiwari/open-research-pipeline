# Open Research Pipeline

A public catalogue of research studies that can be replicated and extended using **openly available data**, in four areas:

1. computational pathology;
2. gastroenterology and hepatology AI;
3. clinical data and medical LLMs;
4. healthcare cybersecurity.

Each entry starts from a published paper, preprint, codebase or dataset, and has three parts: a summary, a **replication guide** and an **extension analysis** (the gaps in the work, and how to turn each into a new study on open data).

**Site:** https://atultiwari.github.io/open-research-pipeline/

Maintained by Dr. Atul Tiwari (Associate Professor of Pathology, Government Medical College, Chittorgarh). Claude does the legwork; Atul approves every study, protocol and manuscript.

## Adding a study: three ways

1. **Claude Code, in this folder:**
   ```
   /add-study <url> [more urls] [note]
   ```
   Any paper, preprint, DOI, PubMed/PMC link, GitHub repo, Hugging Face dataset or model, Zenodo, Figshare, Kaggle or PhysioNet link works. Anything after the links is treated as your design note.
2. **Claude app, in a session with this repo attached:** paste the link and say "add this study".
3. **From a phone:** open a GitHub issue with the [**Add a link**](https://github.com/atultiwari/open-research-pipeline/issues/new/choose) form. The next weekly scout run, or `/process-inbox`, picks it up, adds the study, comments with the link and closes the issue. Only issues opened by the maintainer are processed automatically.

All three run the same procedure, the [ingest skill](.claude/skills/ingest-study/SKILL.md):
- fetch the metadata from public APIs;
- check for duplicates;
- check that the data are open;
- write the replication guide and the gap analysis, with a novelty check for each gap;
- validate, build, and commit.

## The three approval gates

`new` → **1. Atul approves the study** (`/approve`) → `approved` → `/protocol` → `protocol` → **2. Atul signs off the protocol** → `analysis` → `drafting` → **3. Atul approves the manuscript** → `preprint` → `submitted` → `published`. Side exits: `/park` and `/reject`.

## Commands (Claude Code)

| Command | What it does |
| --- | --- |
| `/add-study <url> [note]` | Add a study (or update an existing one) from links |
| `/approve <slug> [note]` | Gate 1: approve a study |
| `/park <slug> [note]` | Keep for later |
| `/reject <slug> <reason>` | Reject, with a reason |
| `/protocol <slug>` | Write the full protocol for an approved study |
| `/enrich <slug\|all>` | Bring a thin study up to the full standard |
| `/process-inbox` | Ingest links from GitHub issues labelled `inbox` |
| `/scout` | Weekly search for 4–8 new candidates; opens one pull request |

**Changing a status from a phone:** open the study page, tap **Edit on GitHub**, change `status:`, add a line to `status_history`, and commit. The site rebuilds in about two minutes.

## Weekly scout

[`.claude/commands/scout.md`](.claude/commands/scout.md) is the single source of truth for the weekly scout. The scheduled cloud task should run `/scout` in this repository. It works on a `scout/<date>` branch and opens one pull request for review. It never pushes to `main`.

## How the repo is organised

- `studies/<slug>/study.yaml` is the source of truth for each study (status, scores, datasets, source). Next to it sit `replication.md`, `extension.md`, `notes.md` (Atul's notes, which are binding design direction) and `protocol.md`.
- `datasets/` is a registry of open datasets, reused to propose external-validation cohorts.
- `journals/` holds journals that publish without an article processing charge (APC), the excluded list, and preprint servers.
- `schema/` holds the JSON Schemas; `scripts/` the Python tooling; `site/` the Astro site, deployed to GitHub Pages on every push to `main`.

## Local development

```bash
pip install -r requirements.txt -r requirements-dev.txt
python3 scripts/validate.py         # schemas + cross-references + no data files
python3 -m pytest -q                # unit tests
python3 scripts/check_links.py      # fetch every external link
cd site && npm install && npm run dev
```

## Rules

Open data only, and no data files in the repo. Every link and licence is verified; anything unconfirmed is marked `verify`. Cybersecurity work is defensive only. See [CLAUDE.md](CLAUDE.md).

## Licence

Code: MIT ([LICENSE](LICENSE)). Written content: CC BY 4.0 ([LICENSE-content](LICENSE-content)).
