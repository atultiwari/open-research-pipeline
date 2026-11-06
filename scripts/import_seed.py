#!/usr/bin/env python3
"""One-off migration: _seed/studies.json -> studies/<slug>/{study.yaml, replication.md, extension.md}.

Usage: python3 scripts/import_seed.py [--force]

Historical: the migration ran on 2026-11-04/06 and _seed/ was then deleted. To re-run it, restore
the seed first:  git checkout c154992 -- _seed
Values come only from the seed file, plus code licences read from the GitHub API on 2026-11-06.
Anything not in the seed is written as 'verify' or left for /enrich.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "_seed" / "studies.json"
MIGRATED_ON = "2026-11-04"

AREA = {
    "Computational pathology": "computational-pathology",
    "Gastro & hepatology AI": "gastro-hepatology",
    "Clinical data / LLMs": "clinical-data-llm",
    "Healthcare cybersecurity": "healthcare-cybersecurity",
}
TIER_ORDER = ("laptop", "colab", "api", "runpod")  # cheapest to most expensive
PHYSIONET = "PhysioNet credentialing + CITI training (~1–2 weeks; start early)"
HF_GATED = "Hugging Face gated access (auto-approval)"

# Per-study facts the flat seed record does not hold in structured form. All taken from the seed text;
# code licences from the GitHub API (2026-11-06). Keyed by the new slug.
EXTRA: dict[str, dict] = {
    "cbc-iron-deficiency": dict(
        tags=["haematology", "anaemia", "tabular-ml", "llm"], type="preprint",
        datasets=[("nhanes", "development"), ("mendeley-yemen-cbc", "external-validation")]),
    "clinicalbench-labs": dict(
        tags=["ehr", "llm-vs-ml", "laboratory-values"], type="preprint", code_licence="MIT",
        datasets=[("mimic-iv", "development")], access=[PHYSIONET]),
    "medhallu-small": dict(
        tags=["llm-safety", "hallucination", "small-models"], type="preprint", code_licence="MIT",
        datasets=[("medhallu", "benchmark")]),
    "medmcqa-path": dict(
        tags=["llm-benchmark", "prompt-sensitivity", "pathology-education"], type="preprint", code_licence="MIT",
        datasets=[("medmcqa", "benchmark")]),
    "quantised-labmed": dict(
        tags=["llm-benchmark", "quantisation", "low-resource"], type="preprint", code_licence="MIT",
        datasets=[("medmarks", "benchmark"), ("medmcqa", "benchmark"), ("medhallu", "benchmark")]),
    "cervical-cyto-fm": dict(
        tags=["cytology", "cervix", "foundation-models"], type="preprint", code_licence="MIT",
        datasets=[("sipakmed", "development"), ("mendeley-lbc-cervical", "external-validation"),
                  ("body-cavity-fluid-cytology", "benchmark")],
        access=["Gated access to some foundation models (UNI2-h, Virchow2; institutional email may be needed)"]),
    "fairness-tcga-cptac": dict(
        tags=["fairness", "foundation-models", "wsi"], type="journal", venue="Nature Medicine",
        code_licence="Other (NOASSERTION on GitHub; seed notes say academic use only)",
        datasets=[("uni2h-features-tcga", "development"), ("tcga", "development"), ("cptac", "external-validation")],
        access=[HF_GATED + " for precomputed UNI2-h features"]),
    "plism-scanner": dict(
        tags=["robustness", "scanner-shift", "smartphone", "foundation-models"], type="preprint",
        code_licence="Feature extraction: TRIDENT, Other (NOASSERTION on GitHub)",
        datasets=[("plism", "benchmark")],
        access=["Gated access to several foundation models (CC-BY-NC-ND; institutional email)"]),
    "stain-robust-camelyon": dict(
        tags=["robustness", "stain-variation", "lymph-node", "wsi"], type="preprint", code_licence="Apache-2.0",
        datasets=[("camelyon16", "development"), ("camelyon17", "external-validation")]),
    "wbc-crossdataset": dict(
        tags=["haematology", "white-cells", "foundation-models"], type="preprint", code_licence="Apache-2.0",
        datasets=[("wbcbench-2026", "development"), ("pbc-barcelona", "external-validation"),
                  ("raabin-wbc", "external-validation")],
        access=[HF_GATED + " for WBCBench 2026"]),
    "hhs-breach-its": dict(
        tags=["breaches", "ransomware", "time-series", "dpdp"], type="journal", venue="JAMA Network Open",
        datasets=[("hhs-ocr-breach-portal", "development"), ("vcdb", "external-validation")]),
    "icsma-cve-landscape": dict(
        tags=["medical-devices", "vulnerabilities", "cvss"], type="journal", venue="Frontiers in Digital Health",
        doi="10.3389/fdgth.2026.1701551",
        datasets=[("cisa-csaf", "development"), ("nvd-cve", "development"), ("first-epss", "development"),
                  ("cisa-kev", "development")]),
    "iomt-xdataset": dict(
        tags=["iomt", "intrusion-detection", "leakage", "edge-ml"], type="preprint",
        datasets=[("ciciomt2024", "development"), ("wustl-ehms-2020", "external-validation"),
                  ("ciciot2023", "external-validation")],
        access=["CICIoMT2024 download form (free)"]),
    "mpib-small-llm": dict(
        tags=["prompt-injection", "llm-safety", "quantisation"], type="preprint",
        code_licence="None stated on GitHub (no licence file)",
        datasets=[("mpib", "benchmark")], access=[HF_GATED + " for MPIB"]),
    "pathfm-adversarial": dict(
        tags=["adversarial-robustness", "foundation-models", "wsi"], type="preprint",
        code_licence="None stated on GitHub (no licence file)",
        datasets=[("camelyon16", "development"), ("tcga", "development")],
        access=["Hugging Face gated access for some foundation-model weights (free registration)"]),
    "ap-icu-mortality": dict(
        tags=["pancreatitis", "icu", "prognosis", "xgboost"], type="preprint",
        datasets=[("mimic-iv", "development"), ("eicu-crd", "external-validation")], access=[PHYSIONET]),
    "cirrhosis-sepsis-icu": dict(
        tags=["cirrhosis", "sepsis", "icu", "prognosis"], type="journal", venue="Frontiers in Medicine",
        doi="10.3389/fmed.2026.1759988",
        datasets=[("mimic-iv", "development"), ("eicu-crd", "external-validation")], access=[PHYSIONET]),
    "fib4-nhanes-extval": dict(
        tags=["masld", "fib-4", "survey-weighted", "lean-masld"], type="code", code_licence="MIT",
        datasets=[("nhanes", "development")]),
    "hepatobench-tcga-lihc": dict(
        tags=["liver", "tissue-classification", "foundation-models", "survival"], type="preprint",
        code_licence="None stated on GitHub (no licence file)",
        datasets=[("hepatobench", "benchmark"), ("tcga", "external-validation")]),
    "polypgen-dino-frozen": dict(
        tags=["polyp-segmentation", "domain-generalisation", "endoscopy"], type="preprint",
        code_licence="None stated on GitHub (no licence file): reimplement, do not copy",
        datasets=[("polypgen", "development"), ("kvasir-seg", "external-validation"),
                  ("cvc-clinicdb", "external-validation")],
        access=["Synapse account for PolypGen (free)"]),
}


def slug_of(old_id: str) -> str:
    return re.sub(r"^[a-z]{2}-\d{4}w\d{2}-", "", old_id)


def compute_tier(text: str) -> str:
    low = text.lower()
    found = [t for t in TIER_ORDER if t in low]
    return found[-1] if found else "laptop"


def est_weeks(text: str) -> int:
    numbers = [int(n) for n in re.findall(r"\d+", str(text))]
    return max(numbers) if numbers else 8


def code_fields(code: str, licence: str | None) -> dict:
    url = re.match(r"^(https?://\S+)$", code.strip())
    out = {"code_url": url.group(1)} if url else {"code_note": code.strip()}
    if licence:
        out["code_licence"] = licence
    return out


def arxiv_id(url: str) -> str | None:
    m = re.search(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5}(?:v\d+)?)", url)
    return m.group(1) if m else None


def build_study(rec: dict) -> dict:
    slug = slug_of(rec["id"])
    extra = EXTRA[slug]
    source = {"type": extra["type"], "title": rec["source_title"], "authors": "verify",
              "venue": extra.get("venue", rec["source_server"]), "date": rec["source_date"], "url": rec["source_url"]}
    if extra.get("doi"):
        source["doi"] = extra["doi"]
    if arxiv_id(rec["source_url"]):
        source["arxiv_id"] = arxiv_id(rec["source_url"])
    source.update(code_fields(rec["code_url"], extra.get("code_licence")))
    return {
        "id": slug, "legacy_id": rec["id"], "title": rec["proposed_study"], "area": AREA[rec["area"]],
        "tags": extra["tags"], "status": "new",
        "status_history": [{"status": "new", "date": MIGRATED_ON,
                            "note": f"Migrated from the claude.ai register ({rec['run_id']})"}],
        "source": source,
        "datasets": [{"id": d, "role": r} for d, r in extra["datasets"]],
        "study_type": rec["study_type"], "reporting_guideline": rec["reporting_guideline"],
        "novelty_delta": rec["novelty_delta"],
        "compute": {"tier": compute_tier(rec["compute_tier"]), "estimate": rec["compute_tier"]},
        "est_weeks": est_weeks(rec["est_weeks"]),
        "scores": {"feasibility": rec["feasibility"], "novelty": rec["novelty"], "fit": None},
        "risks": [], "access_actions": extra.get("access", []), "candidate_journals": [],
        "added_at": rec["added_at"], "added_by": "scout", "run_id": rec["run_id"],
    }


STUB_NOTE = ("> **Needs enrichment.** This is a stub migrated from the old register. "
             "Run `/enrich {slug}` to replace it with a full, verified guide.\n")


def replication_md(rec: dict, slug: str) -> str:
    return f"""---
enriched: false
---
{STUB_NOTE.format(slug=slug)}
## What the original study did

*{rec['source_title']}* ({rec['source_server']}, {rec['source_date']}). [Source]({rec['source_url']}).

## Data

- **Datasets:** {rec['dataset_name']}
- **Access:** {rec['dataset_access']}
- **Main link:** {rec['dataset_url']}

## Code

{rec['code_url']}

## Compute

{rec['compute_tier']}; about {rec['est_weeks']} weeks to a preprint (register estimate).

## Notes from the register

{rec['notes']}
"""


def extension_md(rec: dict, slug: str) -> str:
    return f"""---
enriched: false
---
{STUB_NOTE.format(slug=slug)}
## Proposed extension (from the register)

{rec['proposed_study']}

## Why it is new

{rec['novelty_delta']}

## Design

- **Study type:** {rec['study_type']}
- **Reporting guideline:** {rec['reporting_guideline']}
- **Scores:** feasibility {rec['feasibility']}/5, novelty {rec['novelty']}/5

The systematic gap analysis (novelty check per gap, open-data matches, design sketches) has not been done yet.
"""


def write_study(rec: dict, force: bool) -> str:
    study = build_study(rec)
    folder = ROOT / "studies" / study["id"]
    if folder.exists() and not force:
        return f"skip  {study['id']} (exists; use --force)"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "study.yaml").write_text(
        yaml.safe_dump(study, sort_keys=False, allow_unicode=True, width=110), encoding="utf-8")
    (folder / "replication.md").write_text(replication_md(rec, study["id"]), encoding="utf-8")
    (folder / "extension.md").write_text(extension_md(rec, study["id"]), encoding="utf-8")
    return f"wrote {study['id']}"


def main() -> int:
    force = "--force" in sys.argv
    if not SEED.exists():
        print("ERROR: _seed/studies.json is gone (migration done). Restore it with: git checkout c154992 -- _seed")
        return 1
    records = json.loads(SEED.read_text(encoding="utf-8"))
    missing = [slug_of(r["id"]) for r in records if slug_of(r["id"]) not in EXTRA]
    if missing:
        print(f"ERROR: no EXTRA mapping for {missing}")
        return 1
    for rec in records:
        print(write_study(rec, force))
    return 0


if __name__ == "__main__":
    sys.exit(main())
