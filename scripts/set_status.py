#!/usr/bin/env python3
"""Change a study's status and append to its status_history.

Usage: python3 scripts/set_status.py <slug> <status> [note ...]
Used by /approve, /park, /reject and /protocol. Refuses unknown slugs or statuses, and a
'protocol' status unless protocol.md exists.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from studylib import STATUSES, STUDIES, load_yaml, study_path, today, write_study  # noqa: E402

PROTOCOL_OR_LATER = {"protocol", "analysis", "drafting", "preprint", "submitted", "published"}


class StatusError(ValueError):
    """A status change that is not allowed; the message is shown to the user."""


def updated(study: dict, status: str, note: str, date: str) -> dict:
    """Return a new study dict with the status changed; the input is not modified."""
    if status not in STATUSES:
        raise StatusError(f"Unknown status '{status}'. Use one of: {', '.join(STATUSES)}")
    if status == study.get("status"):
        raise StatusError(f"{study['id']} is already '{status}'")
    entry = {"status": status, "date": date, **({"note": note} if note else {})}
    return {**study, "status": status, "status_history": [*study.get("status_history", []), entry],
            "last_reviewed": date}


def main(argv: list[str], root: Path = STUDIES) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    slug, status, note = argv[0], argv[1].lower(), " ".join(argv[2:]).strip()
    path = study_path(slug, root)
    if not path.exists():
        print(f"ERROR: no study '{slug}' (looked for {path})")
        return 1
    if status in PROTOCOL_OR_LATER and not (path.parent / "protocol.md").exists():
        print(f"ERROR: '{status}' needs studies/{slug}/protocol.md first (run /protocol {slug})")
        return 1
    try:
        study = updated(load_yaml(path), status, note, today())
    except StatusError as err:
        print(f"ERROR: {err}")
        return 1
    write_study(study, root)
    print(f"{slug}: {status}" + (f" ({note})" if note else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
