---
description: Approve a study (gate 1) and record it in status_history
argument-hint: <slug> [note]
---
Approve a study. Arguments: `$ARGUMENTS` (first word = slug, the rest = note).

1. `python3 scripts/set_status.py <slug> approved <note>`. If it errors (unknown slug, already approved), report the error and stop.
2. `python3 scripts/validate.py` and `(cd site && npm run build)`; both must pass.
3. `git add studies/<slug>/study.yaml && git commit -m "study: <slug> → approved" && git push`.
4. Reply in two lines: the study title, and the next step (`/protocol <slug>`). If the study's `replication.md` or `extension.md` still has `enriched: false`, suggest `/enrich <slug>` first.
