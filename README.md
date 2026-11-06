# Open Research Pipeline

A public catalogue of research studies that can be replicated and extended using **openly available data**, in four areas:

1. computational pathology;
2. gastroenterology and hepatology AI;
3. clinical data and medical LLMs;
4. healthcare cybersecurity.

Each entry starts from a published paper, preprint, codebase or dataset, and has three parts: a summary, a **replication guide** and an **extension analysis** (the gaps in the work, and how to turn each into a new study on open data).

**Site:** https://atultiwari.github.io/open-research-pipeline/

Maintained by Dr. Atul Tiwari (Associate Professor of Pathology, Government Medical College, Chittorgarh), with Claude doing the legwork and Atul approving every study, protocol and manuscript.

## How it works

- `studies/<slug>/study.yaml` is the source of truth for each study (status, scores, datasets, source).
- `datasets/` is a registry of open datasets, reused to propose external-validation cohorts.
- `journals/` holds a shortlist of journals that can be published in without an article processing charge (APC), plus preprint servers.
- The site in `site/` is built with Astro and deployed to GitHub Pages on every push to `main`.

## Changing a study's status

- In Claude Code in this folder: `/approve <slug>`, `/park <slug>` or `/reject <slug> <reason>`.
- On a phone: open the study page, tap **Edit on GitHub**, change `status:` and add a line to `status_history`, then commit.

## Local development

```bash
pip install -r requirements.txt
python3 scripts/validate.py
cd site && npm install && npm run dev
```

## Rules

Open data only; no data files in the repo; every link and licence verified. See [CLAUDE.md](CLAUDE.md).

## Licence

Code: MIT ([LICENSE](LICENSE)). Written content: CC BY 4.0 ([LICENSE-content](LICENSE-content)).
