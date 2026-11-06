---
description: Add a study from one or more research links (paper, preprint, code, dataset, model)
argument-hint: <url> [more urls] [note]
---
Run the `ingest-study` skill (`.claude/skills/ingest-study/SKILL.md`) in `atul` mode on:

$ARGUMENTS

Treat anything that is not a URL, DOI or arXiv id as Atul's note: binding design direction for the extension. If the links point to an existing study, update it instead and say so.
