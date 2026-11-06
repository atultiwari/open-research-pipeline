"""Read and write study folders. Shared by find_dupes.py, new_study.py and set_status.py."""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
STUDIES = ROOT / "studies"
DATASETS = ROOT / "datasets"
STATUSES = ("new", "approved", "protocol", "analysis", "drafting", "preprint", "submitted", "published",
            "parked", "rejected")


def today() -> str:
    return dt.date.today().isoformat()


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def dump_yaml(data: dict) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=110)


def iter_studies(root: Path = STUDIES):
    for path in sorted(root.glob("*/study.yaml")):
        yield load_yaml(path)


def iter_datasets(root: Path = DATASETS):
    for path in sorted(root.glob("*.yaml")):
        yield load_yaml(path)


def study_path(slug: str, root: Path = STUDIES) -> Path:
    return root / slug / "study.yaml"


def write_study(study: dict, root: Path = STUDIES) -> Path:
    path = study_path(study["id"], root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_yaml(study), encoding="utf-8")
    return path
