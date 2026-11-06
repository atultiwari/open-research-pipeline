---
description: Weekly scout — find 4–8 new study candidates across the four areas and open one PR
argument-hint: [optional focus or date window]
---
You are the weekly scout for the Open Research Pipeline. This file is the single source of truth for the scheduled cloud task. Optional focus from the caller: $ARGUMENTS

**Rules.** Follow `CLAUDE.md`, especially: open data only, verify every URL, licences recorded exactly, and defensive security only.

1. **Set up.** `git switch main && git pull`. Create branch `scout/<YYYY-MM-DD>` (today's date). Set run id `scout-<YYYY-MM-DD>`.
2. **Inbox first.** Run `/process-inbox` in scout mode, so links Atul filed from his phone are handled.
3. **Search** for 4–8 new candidates, aiming for 1–2 per area:
   - areas: computational pathology; gastro and hepatology AI; clinical data and medical LLMs; healthcare cybersecurity (defensive);
   - preprints first, ideally from the last ~14 days: arXiv (cs.CV, eess.IV, cs.CL, cs.CR, q-bio), medRxiv/bioRxiv (date-range API), then recent journal papers (OpenAlex search with a `from_publication_date` filter);
   - keep a candidate only if:
     - it runs on open data (open, free registration or credentialed);
     - its code exists or the method can be reimplemented;
     - it has a clear novelty delta Atul could add (external validation, newer models, subgroup or calibration analysis, LMIC/Indian relevance, a pathologist error taxonomy);
     - it is feasible on laptop, Colab, RunPod or API within about 10 weeks;
   - skip anything `python3 scripts/find_dupes.py` says already exists, unless the new paper materially changes an existing study; in that case, update that study.
4. **Ingest** each candidate with the `ingest-study` skill in `scout` mode (`--added-by scout --run-id scout-<date>`), with one commit per study on the scout branch.
5. **Check.** `python3 scripts/validate.py`, `python3 -m pytest -q`, `(cd site && npm run build)`; all must pass.
6. **Open one PR.** Push the branch, then open the PR with the REST API (cloud sessions block GitHub GraphQL, so do not use `gh pr create`): write the body to a file and run `gh api repos/atultiwari/open-research-pipeline/pulls -f base=main -f head=scout/<YYYY-MM-DD> -f title="scout: <date> — N candidates" -F body=@pr-body.md` (add `-F draft=true` if a check failed and could not be fixed). Do not commit `pr-body.md`. The body has a table (slug, area, score, compute, weeks, access actions), a line per rejected candidate with the reason, and a list of the searches run. End the body with "🤖 Generated with [Claude Code](https://claude.com/claude-code)".
7. **Never merge the PR.** Atul reviews it (gate 1 happens when he approves studies after merging).
