---
name: ingest-study
description: Add or update a study opportunity in the Open Research Pipeline from any research link (arXiv, medRxiv, bioRxiv, DOI, PubMed/PMC, journal page, GitHub repo, Hugging Face dataset or model, Zenodo, Figshare, Kaggle, PhysioNet). Use whenever Atul pastes a research link in this repo, says "add this study", or when /add-study, /process-inbox, /scout or /enrich run. Produces study.yaml, replication.md and extension.md on open data only, verified, then validates, builds and commits.
---

# Ingest a study

You turn one or more links into a complete, verified study entry, or improve an existing one. Read `CLAUDE.md` first; its hard rules override anything here. Work from the repo root.

**Inputs:** one or more links, an optional note from Atul (binding design direction), and a mode:
- `atul` (default): commit and push to `main`;
- `scout`: commit on branch `scout/<YYYY-MM-DD>` and open a PR, never push to `main`;
- `enrich`: the study already exists; rewrite its stubs to the full standard.

Track every URL you write. You must fetch it (step 1, WebFetch, or `scripts/check_links.py`) before it goes in a file. Anything unconfirmed is written as `verify`.

## 1. Identify and fetch metadata (deterministic first)

```bash
python3 scripts/fetch_meta.py --pretty <link> [<link> ...] > /tmp/meta.json
```

It classifies the link and queries the public API: arXiv export API, bioRxiv/medRxiv API, Crossref (OpenAlex fallback), NCBI E-utilities, GitHub (`gh api`), Hugging Face API, Zenodo, Figshare, and PhysioNet/Kaggle/web pages via citation meta tags. Check `warnings` (gated access, NC/ND licences, no code licence, credentialing). If a fetch fails, say so and fall back to WebFetch of the page. Never guess the missing fields.

Gated Hugging Face datasets return no card text through the API; WebFetch the dataset page instead. Use `--excerpt 20000` when a README or dataset card is long (licence sections often sit near the end).

Then read the full text you need: the paper (arXiv HTML/PDF, PMC, publisher page) or the README/dataset card. If a publisher page redirects to a login (Nature, Elsevier), read the open copy instead: Europe PMC (`https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:<doi>&format=json&resultType=core`), PMC, or the arXiv HTML. `text_excerpt` is for your reading only. **Never paste it into a file;** summarise in your own words, with at most one short quoted sentence.

**Preprint later published?** `fetch_meta.py` does not detect this; search OpenAlex by title (`/works?search=<title>`) for a journal or conference version. Point `source` at the peer-reviewed version (`type: journal` or `conference`, its `doi`, `url`, `venue` and `date`), keep `arxiv_id`, and mention the preprint in `source.title` or `venue`. Read both versions: limitations and numbers can change.

## 2. Expand the graph

- **Paper →** its code (`links.code`, "Code availability" section, Papers with Code) and its datasets (methods section).
- **Code →** the paper (README citation, `links.papers`, `links.dois`) and the datasets it loads.
- **Dataset or model →** the main papers that use it (card citations, OpenAlex `cites:` search, Semantic Scholar). Pick the best *source study* to build on: recent, with code, on open data, with a clear gap. If two or three are equally good, list them for Atul (title, year, one line each) and stop for his choice. In `scout` mode, pick the best and note the others in `extension.md`.

Run `fetch_meta.py` on each new link you adopt.

## 3. Check for duplicates

```bash
python3 scripts/find_dupes.py --meta /tmp/meta.json [<extra links>] [--title "<source title>"]
```

- In `enrich` mode the study itself appears in `matches`; that is expected. Look only for *other* matching slugs.
- `matches` not empty → **update that study instead** (`new_study.py --update`), and tell Atul which slug you updated and why.
- `related` lists studies that use the same dataset. Mention them, and avoid proposing the same extension twice.

## 4. Check data feasibility (never skip)

Atul has no data of his own. For every dataset the study needs:
1. Find or add it in `datasets/<slug>.yaml` (schema: `schema/dataset.schema.json`). For a new dataset, fetch its page or API and record (`doi` = the dataset's own DOI; the paper goes in `citation`) `access` (`open` / `free-registration` / `credentialed`), the licence exactly as stated, size, gating, institution and country. Flag NC/ND terms, gated models needing an institutional email, and mismatches between the card and the paper in `licence_notes`.
2. When a dataset has mirrors (Hugging Face, Kaggle, Owkin/TCIA copies), check that the mirror holds the *whole* dataset and the same licence. Preprocessed copies are often subsets (e.g. PLISM's Hugging Face copy omits the smartphone images). Record this in `licence_notes` or `notes`.
3. Record access steps in `access_actions` (e.g. "PhysioNet credentialing + CITI training (~1–2 weeks)", "HF gated access for UNI2-h").

If a supposedly de-identified open dataset turns out to contain direct identifiers (names, phone numbers, record numbers linked to names): stop using it, delete any downloaded copy, do **not** add it to `datasets/`, and do **not** describe the identifiers in any committed file (the repo is public; say only "excluded: de-identification concerns, pending clarification with the depositors"). Tell Atul privately in your report so he can decide whether to notify the depositors.

If the source used private or paid data, or UK Biobank, write "Not directly replicable" in `replication.md`. Then either name the closest open surrogate and redesign around it, or set `status: rejected` with the reason (via `scripts/set_status.py`). Say this plainly to Atul.

## 5. Write `replication.md`

Front matter `enriched: true`. Sections (use `##` headings):
1. **What the original study did**: 2–4 sentences, your own words.
2. **Data**: each dataset, and exactly how to get it (account, credentialing, gated-access request, download size, storage tips such as a RunPod volume near the bucket, or downloading a subset).
3. **Environment**: Python version and key packages, taken from the repo's `requirements`/`environment.yml`/`pyproject` when there is one.
4. **Step-by-step replication**: repo commands, or a reimplementation outline when there is no code (or no code licence: reimplement, don't copy).
5. **Compute and cost**: laptop / Colab / RunPod GPU-hours / API USD.
6. **Target numbers**: the main metrics to reproduce, with table or figure references from the paper.
7. **Known pitfalls**: licence, label changes, split leakage, pretraining overlap, version mismatches.
8. **Claude Code task list**: a numbered checklist a future session can run. Data stays outside the repo (`data/` is gitignored); commit only code and aggregate results.

## 6. Write `extension.md`: the gap analysis

Front matter `enriched: true`. Look for gaps systematically, and cite where each comes from (section, table or line of the paper, or the source you checked):
- the authors' own limitations and future-work statements;
- no external validation, or only internal/random splits (leakage risk);
- outdated models (older foundation models or LLMs);
- no subgroup or fairness analysis (age, sex, race, site, scanner);
- no calibration or decision-curve analysis;
- no low-compute or edge variant;
- TRIPOD+AI / CLAIM 2024 / TRIPOD-LLM items the paper missed;
- no Indian or LMIC relevance (anaemia burden, lean MASLD, low-cost scanners or smartphones, DPDP Act framing for security work);
- room for a pathologist's expert error taxonomy.

For each worthwhile gap (usually 3–6), write a `### Gap N: <name>` block with:
- **Evidence**: where the gap comes from.
- **Novelty check**: what you searched (OpenAlex works citing the source, Semantic Scholar, arXiv and medRxiv search, with queries and dates) and what you found. Name any paper that already fills the gap.
- **Open data**: matching dataset ids from `datasets/` (add new ones if needed).
- **Design sketch**: hypothesis; data; methods and baselines; metrics; reporting guideline.
- **Rating**: feasibility 1–5, novelty 1–5, compute tier, weeks to a preprint.

End with `## Recommended extension`: the single best gap, and why (feasibility × novelty, fit for a pathologist, speed to a preprint, journal fit).

Useful searches (all public, with the project User-Agent). Prefer OpenAlex: Semantic Scholar and arXiv rate-limit without a key (HTTP 429). Pause at least 3 s between arXiv calls, never run arXiv searches in parallel, and if Semantic Scholar refuses, record "rate-limited, not checked" rather than skipping silently.
- `https://api.openalex.org/works?filter=cites:<openalex_id>&sort=publication_date:desc&per-page=50`
- `https://api.openalex.org/works?search=<terms>&filter=from_publication_date:<YYYY-MM-DD>`
- `https://api.semanticscholar.org/graph/v1/paper/arXiv:<id>/citations?fields=title,year,externalIds&limit=100`
- `https://export.arxiv.org/api/query?search_query=all:<terms>&sortBy=submittedDate&max_results=50`
- `https://api.biorxiv.org/details/medrxiv/<YYYY-MM-DD>/<YYYY-MM-DD>` (date-range listing)

**When a service refuses** (OpenAlex daily budget used up, arXiv or Semantic Scholar 429), fall back in this order and record which one you used:
1. Crossref: `https://api.crossref.org/works?query.bibliographic=<terms>&filter=from-pub-date:<YYYY-MM-DD>&rows=50`.
2. Europe PMC (includes medRxiv/bioRxiv preprints): `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=<terms>%20AND%20FIRST_PDATE:[<YYYY-MM-DD>%20TO%20<YYYY-MM-DD>]&format=json&pageSize=50`.
3. Web search.

If fewer than two independent sources could be searched for a gap, mark that gap's novelty check "incomplete, rerun before the protocol".

## 7. Write `study.yaml`

Copy the essence of the recommended extension into `study.yaml`:
- `title`: the proposed new study, in one line;
- `novelty_delta`: 1–3 sentences;
- `scores`: feasibility, novelty, and `fit` (how well it suits a pathologist with an ML background);
- `compute`, `est_weeks`, `risks`, `access_actions`;
- `candidate_journals`: 2–3 ids from `journals/journals.yaml`, zero-APC routes only, matched to the area.

Fill `source` from the fetched metadata (`authors` as "First A et al.", `doi`, `arxiv_id`, `code_url`, and `code_licence` exactly as GitHub reports it). Fill `datasets` with ids and roles.

- **New study:** write a JSON spec and run `python3 scripts/new_study.py spec.json --added-by <atul|scout|claude-code> [--run-id <id>]`. The slug is short and kebab-case (e.g. `wbc-crossdataset`).
- **Existing study:** run `python3 scripts/new_study.py spec.json --update`, which never changes status or history.

Then write the two markdown files in full (replacing any stubs). Leave `notes.md` untouched. If `notes.md` exists, follow it.

## 8. Check, commit, report

```bash
python3 scripts/validate.py
python3 scripts/check_links.py studies/<slug> datasets
python3 -m pytest -q
(cd site && npm run build)
```

Fix every error. Treat `DEAD` links as errors: correct them, or replace them with `verify`. `BLOCKED` (bot-blocked publisher) is acceptable if you confirmed the page another way.

- `atul` / `enrich` mode: `git add studies/<slug> datasets journals && git commit -m "study: add <slug> (<area>)"` (or `study: enrich <slug>` / `study: update <slug>`), then `git push`.
- `scout` mode: `git switch -c scout/<YYYY-MM-DD>` (or reuse it), commit each study, push, then `gh pr create --title "scout: <date> candidates" --body <summary>`.

Report to Atul in under 120 words:
- the title;
- the recommended extension;
- the score (feasibility × novelty, plus fit);
- the data access actions;
- the page URL `https://atultiwari.github.io/open-research-pipeline/studies/<slug>/` (live about 2 minutes after the push).
