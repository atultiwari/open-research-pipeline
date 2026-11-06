#!/usr/bin/env python3
"""Scaffold a study folder, or update an existing study, from a JSON spec.

Usage:
    python3 scripts/new_study.py spec.json [--added-by atul|scout|claude-code] [--run-id ID]
    python3 scripts/new_study.py - < spec.json
    python3 scripts/new_study.py spec.json --update      # merge into an existing study

The spec holds study.yaml fields (see schema/study.schema.json); at minimum: id, title, area,
source {type, title, url}, study_type, reporting_guideline, novelty_delta, compute, est_weeks, scores.
Defaults are filled in (status 'new', status_history, empty lists, added_at today). On --update,
status and status_history are never changed (use set_status.py). Stub replication.md and
extension.md (enriched: false) are created only if missing. Run scripts/validate.py afterwards.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from studylib import STUDIES, load_yaml, study_path, today, write_study  # noqa: E402

PROTECTED_ON_UPDATE = {"id", "status", "status_history", "added_at", "added_by", "legacy_id"}
STUB = """---
enriched: false
---
> **Needs enrichment.** Run `/enrich {slug}` to write the full {what}.
"""


def with_defaults(spec: dict, added_by: str, run_id: str | None, date: str) -> dict:
    base = {
        "tags": [], "status": "new",
        "status_history": [{"status": "new", "date": date, "note": f"Added by {added_by}"}],
        "datasets": [], "risks": [], "access_actions": [], "candidate_journals": [],
        "added_at": date, "added_by": added_by,
    }
    study = {**base, **spec}
    study["scores"] = {"fit": None, **spec.get("scores", {})}
    if run_id and "run_id" not in spec:
        study["run_id"] = run_id
    return study


def merged(existing: dict, spec: dict, date: str) -> dict:
    """Return existing updated with spec; nested dicts (source, scores, compute, links) merge key by key."""
    out = dict(existing)
    for key, value in spec.items():
        if key in PROTECTED_ON_UPDATE:
            continue
        out[key] = {**existing.get(key, {}), **value} if isinstance(value, dict) and isinstance(existing.get(key), dict) else value
    out["last_reviewed"] = date
    return out


def ensure_stubs(folder: Path, slug: str) -> list[str]:
    created = []
    for name, what in (("replication.md", "replication guide"), ("extension.md", "extension analysis")):
        path = folder / name
        if not path.exists():
            path.write_text(STUB.format(slug=slug, what=what), encoding="utf-8")
            created.append(name)
    return created


def parse(argv: list[str]) -> tuple[dict, dict]:
    opts = {"added_by": "claude-code", "run_id": None, "update": "--update" in argv}
    args = [a for a in argv if a != "--update"]
    for flag, key in (("--added-by", "added_by"), ("--run-id", "run_id")):
        if flag in args:
            i = args.index(flag)
            opts[key] = args[i + 1]
            del args[i:i + 2]
    if len(args) != 1:
        raise SystemExit(__doc__)
    raw = sys.stdin.read() if args[0] == "-" else Path(args[0]).read_text(encoding="utf-8")
    return json.loads(raw), opts


def main(argv: list[str], root: Path = STUDIES) -> int:
    spec, opts = parse(argv)
    slug = spec.get("id")
    if not slug:
        print("ERROR: spec needs an 'id' (kebab-case slug)")
        return 1
    path = study_path(slug, root)
    if path.exists() and not opts["update"]:
        print(f"ERROR: studies/{slug} already exists. Re-run with --update to merge, or pick another id.")
        return 1
    if opts["update"] and not path.exists():
        print(f"ERROR: --update given but studies/{slug} does not exist")
        return 1
    date = today()
    study = merged(load_yaml(path), spec, date) if opts["update"] else with_defaults(spec, opts["added_by"], opts["run_id"], date)
    write_study(study, root)
    stubs = ensure_stubs(path.parent, slug)
    print(f"{'updated' if opts['update'] else 'created'} studies/{slug}/study.yaml" + (f"; stubs: {', '.join(stubs)}" if stubs else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
