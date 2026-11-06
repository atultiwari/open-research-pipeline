---
description: Park a study (keep it for later) and record why
argument-hint: <slug> [note]
---
Park a study. Arguments: `$ARGUMENTS` (first word = slug, the rest = note).

1. `python3 scripts/set_status.py <slug> parked <note>`. Report any error and stop.
2. `python3 scripts/validate.py` and `(cd site && npm run build)`; both must pass.
3. `git add studies/<slug>/study.yaml && git commit -m "study: <slug> → parked" && git push`.
4. Reply in one line with the title and the note.
