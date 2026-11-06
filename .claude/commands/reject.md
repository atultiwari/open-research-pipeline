---
description: Reject a study and record the reason
argument-hint: <slug> <reason>
---
Reject a study. Arguments: `$ARGUMENTS` (first word = slug, the rest = reason).

If no reason is given, ask Atul for one in a single short question; a rejection always carries a reason.

1. `python3 scripts/set_status.py <slug> rejected <reason>`. Report any error and stop.
2. `python3 scripts/validate.py` and `(cd site && npm run build)`; both must pass.
3. `git add studies/<slug>/study.yaml && git commit -m "study: <slug> → rejected" && git push`.
4. Reply in one line with the title and the reason.
