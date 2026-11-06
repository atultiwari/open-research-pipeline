#!/usr/bin/env python3
"""Find existing studies that match a link, DOI, arXiv id or title.

Usage:
    python3 scripts/find_dupes.py <url|doi|arxiv-id> [...] [--title "Paper title"] [--meta meta.json]
    python3 scripts/fetch_meta.py <url> | python3 scripts/find_dupes.py --meta -

Prints JSON: {"matches": [...], "related": [...]}.
- matches: studies whose *source* is the same work (same DOI, arXiv id, normalised URL, code repo, or a
  fuzzy title match >= 0.88). Update these instead of creating a new study.
- related: studies that use a matching dataset (useful when the link is a dataset or model).
Exit code 0 always; the caller decides.
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from linkkit import classify, normalise_url  # noqa: E402
from studylib import iter_datasets, iter_studies  # noqa: E402

TITLE_THRESHOLD = 0.88


def norm_title(title: str | None) -> str:
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", (title or "").lower())).strip()


def study_keys(study: dict) -> set[str]:
    """Every identifier a study's source can be recognised by."""
    src = study.get("source", {})
    keys = set()
    for field in ("url", "code_url"):
        if str(src.get(field, "")).startswith("http"):
            keys.add(normalise_url(src[field]))
    if src.get("doi") and src["doi"] != "verify":
        keys.add(f"doi:{src['doi'].lower()}")
    if src.get("arxiv_id") and src["arxiv_id"] != "verify":
        keys.add("arxiv:" + re.sub(r"v\d+$", "", src["arxiv_id"]))
    return keys


def query_keys(inputs: list[str], metas: list[dict]) -> set[str]:
    keys = {normalise_url(i) for i in inputs}
    for m in metas:
        if m.get("url"):
            keys.add(normalise_url(m["url"]))
        if m.get("doi"):
            keys.add(f"doi:{m['doi'].lower()}")
        if m.get("arxiv_id"):
            keys.add("arxiv:" + re.sub(r"v\d+$", "", m["arxiv_id"]))
        for u in m.get("links", {}).get("code", []) + m.get("links", {}).get("papers", []):
            keys.add(normalise_url(u))
        for d in m.get("links", {}).get("dois", []):
            keys.add(f"doi:{d.lower()}")
    return keys


def find(inputs: list[str], titles: list[str], metas: list[dict], studies: list[dict], datasets: list[dict]) -> dict:
    qkeys = query_keys(inputs, metas)
    qtitles = [norm_title(t) for t in titles + [m.get("title") for m in metas] if t]
    matches = []
    for s in studies:
        shared = sorted(qkeys & study_keys(s))
        best = max((difflib.SequenceMatcher(None, t, norm_title(s["source"].get("title"))).ratio() for t in qtitles),
                   default=0.0)
        if shared or best >= TITLE_THRESHOLD:
            reasons = [f"same {k.split(':', 1)[0] if ':' in k else 'url'}: {k}" for k in shared]
            reasons += [f"title similarity {best:.2f}"] if best >= TITLE_THRESHOLD else []
            matches.append({"id": s["id"], "title": s["title"], "status": s["status"], "reasons": reasons})

    ds_hits = {d["id"] for d in datasets
               if qkeys & {normalise_url(u) for u in [d.get("url", "")] + d.get("alt_urls", []) if u}}
    related = [{"id": s["id"], "title": s["title"], "status": s["status"],
                "datasets": sorted(ds_hits & {x["id"] for x in s.get("datasets", [])})}
               for s in studies if ds_hits & {x["id"] for x in s.get("datasets", [])}]
    return {"query_keys": sorted(qkeys), "dataset_ids": sorted(ds_hits), "matches": matches,
            "related": [r for r in related if r["id"] not in {m["id"] for m in matches}]}


def parse_args(argv: list[str]) -> tuple[list[str], list[str], list[dict]]:
    inputs, titles, metas, i = [], [], [], 0
    while i < len(argv):
        arg = argv[i]
        if arg in {"--title", "--meta"} and i + 1 < len(argv):
            value = argv[i + 1]
            if arg == "--title":
                titles.append(value)
            else:
                raw = sys.stdin.read() if value == "-" else Path(value).read_text(encoding="utf-8")
                loaded = json.loads(raw)
                metas += [m for m in (loaded if isinstance(loaded, list) else [loaded]) if "error" not in m]
            i += 2
        else:
            inputs.append(arg)
            i += 1
    return inputs, titles, metas


def main(argv: list[str]) -> int:
    if not argv or argv[0] in {"-h", "--help"}:
        print(__doc__)
        return 0
    inputs, titles, metas = parse_args(argv)
    if not (inputs or titles or metas):
        print(__doc__)
        return 2
    _ = [classify(x) for x in inputs]  # fail early on nothing; classify never raises
    result = find(inputs, titles, metas, list(iter_studies()), list(iter_datasets()))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
