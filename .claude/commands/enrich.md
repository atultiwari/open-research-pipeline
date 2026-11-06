---
description: Bring a migrated or thin study up to the full replication + extension standard
argument-hint: <slug|all>
---
Enrich: $ARGUMENTS

- **One slug:** run the `ingest-study` skill in `enrich` mode on that study. Start from its `source.url` (and `code_url`), re-fetch the metadata, and fill in what the migration left out: `source.authors`, `doi`, `scores.fit`, `candidate_journals`, `risks`, and any dataset licences marked `verify`. Rewrite `replication.md` and `extension.md` in full, with `enriched: true`. Keep the study's current status and history. If the analysis changes the recommended extension, update `title`, `novelty_delta`, `scores`, `compute` and `est_weeks`, and say what changed and why. Commit `study: enrich <slug>` and push.
- **`all`:** list the studies whose `replication.md` or `extension.md` has `enriched: false`, sorted by headline score (highest first). Process them in batches of 4–5, one commit per study. After each batch, show a progress table (slug, new score, recommended extension in one line) and wait for Atul to say "continue".
