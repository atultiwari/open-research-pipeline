#!/usr/bin/env python3
"""Validate every study, dataset and journal file against its JSON Schema, plus cross-references.

Usage: python3 scripts/validate.py
Exit code 0 = valid, 1 = errors found. Warnings never fail the run.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN_SUFFIXES = {
    ".csv", ".tsv", ".parquet", ".feather", ".xlsx", ".xls", ".svs", ".ndpi", ".mrxs", ".scn",
    ".tif", ".tiff", ".h5", ".hdf5", ".npy", ".npz", ".pt", ".pth", ".ckpt", ".safetensors",
    ".pcap", ".pcapng",
}
SKIP_DIRS = {"node_modules", ".git", "dist", ".astro", ".venv", "venv", "__pycache__"}
REQUIRED_MD = ("replication.md", "extension.md")
FRONT_MATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def validator(name: str) -> Draft202012Validator:
    schema = json.loads((ROOT / "schema" / name).read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def schema_errors(v: Draft202012Validator, data, label: str) -> list[str]:
    out = []
    for err in sorted(v.iter_errors(data), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in err.path) or "(root)"
        out.append(f"{label}: {where}: {err.message}")
    return out


def check_front_matter(md: Path) -> list[str]:
    match = FRONT_MATTER.match(md.read_text(encoding="utf-8"))
    if not match:
        return [f"{md.relative_to(ROOT)}: missing front matter (--- enriched: true|false ---)"]
    fm = yaml.safe_load(match.group(1)) or {}
    if not isinstance(fm.get("enriched"), bool):
        return [f"{md.relative_to(ROOT)}: front matter needs 'enriched: true' or 'enriched: false'"]
    return []


def validate_datasets() -> tuple[set[str], list[str]]:
    v, errors, ids = validator("dataset.schema.json"), [], set()
    for path in sorted((ROOT / "datasets").glob("*.yaml")):
        data = load_yaml(path)
        label = str(path.relative_to(ROOT))
        errors += schema_errors(v, data, label)
        if isinstance(data, dict):
            if data.get("id") != path.stem:
                errors.append(f"{label}: id '{data.get('id')}' must match file name '{path.stem}'")
            ids.add(data.get("id"))
    return ids, errors


def validate_journals() -> tuple[set[str], list[str]]:
    jpath, ppath = ROOT / "journals" / "journals.yaml", ROOT / "journals" / "preprints.yaml"
    journals = load_yaml(jpath)
    errors = schema_errors(validator("journals.schema.json"), journals, "journals/journals.yaml")
    errors += schema_errors(validator("preprints.schema.json"), load_yaml(ppath), "journals/preprints.yaml")
    ids = [j.get("id") for j in journals.get("journals", [])]
    dupes = {i for i in ids if ids.count(i) > 1}
    errors += [f"journals/journals.yaml: duplicate id '{d}'" for d in sorted(dupes)]
    return set(ids), errors


def validate_study(folder: Path, v, dataset_ids, journal_ids) -> tuple[dict | None, list[str], list[str]]:
    label = str(folder.relative_to(ROOT))
    yml = folder / "study.yaml"
    if not yml.exists():
        return None, [f"{label}: missing study.yaml"], []
    data = load_yaml(yml)
    errors = schema_errors(v, data, f"{label}/study.yaml")
    warnings: list[str] = []
    if not isinstance(data, dict):
        return None, errors, warnings
    if data.get("id") != folder.name:
        errors.append(f"{label}: id '{data.get('id')}' must match folder name")
    for ds in data.get("datasets", []) or []:
        if ds.get("id") not in dataset_ids:
            errors.append(f"{label}: dataset '{ds.get('id')}' not found in datasets/")
    for j in data.get("candidate_journals", []) or []:
        if j not in journal_ids:
            errors.append(f"{label}: journal '{j}' not found in journals/journals.yaml")
    history = data.get("status_history") or []
    if history and history[-1].get("status") != data.get("status"):
        errors.append(f"{label}: status '{data.get('status')}' differs from last status_history entry")
    for name in REQUIRED_MD:
        md = folder / name
        errors += check_front_matter(md) if md.exists() else [f"{label}: missing {name}"]
    protocol = folder / "protocol.md"
    if protocol.exists():
        errors += check_front_matter(protocol)
        if data.get("status") in {"new", "parked", "rejected"}:
            warnings.append(f"{label}: has protocol.md but status is '{data.get('status')}'")
    return data, errors, warnings


def duplicate_sources(studies: list[dict]) -> list[str]:
    seen: dict[str, str] = {}
    warnings = []
    for s in studies:
        src = s.get("source", {})
        for key in ("doi", "arxiv_id", "url"):
            val = str(src.get(key) or "").lower().rstrip("/")
            if not val or val == "verify":
                continue
            val = re.sub(r"v\d+$", "", val) if key == "arxiv_id" else val
            tag = f"{key}:{val}"
            if tag in seen:
                warnings.append(f"possible duplicate: {s['id']} and {seen[tag]} share {key} {val}")
            else:
                seen[tag] = s["id"]
    return warnings


def forbidden_files() -> list[str]:
    errors = []
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"{path.relative_to(ROOT)}: data files must never be committed")
    return errors


def main() -> int:
    dataset_ids, errors = validate_datasets()
    journal_ids, jerr = validate_journals()
    errors += jerr
    v = validator("study.schema.json")
    studies, warnings = [], []
    for folder in sorted(p for p in (ROOT / "studies").iterdir() if p.is_dir()):
        data, serr, swarn = validate_study(folder, v, dataset_ids, journal_ids)
        errors += serr
        warnings += swarn
        if data:
            studies.append(data)
    warnings += duplicate_sources(studies)
    errors += forbidden_files()

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(studies)} studies, {len(dataset_ids)} datasets, {len(journal_ids)} journals: "
          f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
