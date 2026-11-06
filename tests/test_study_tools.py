import json

import pytest
import yaml

import new_study
import set_status
from set_status import StatusError, updated

SPEC = {
    "id": "demo-study", "title": "A demonstration study title", "area": "gastro-hepatology",
    "source": {"type": "preprint", "title": "Paper", "url": "https://arxiv.org/abs/2601.00001"},
    "study_type": "Benchmark", "reporting_guideline": "TRIPOD+AI", "novelty_delta": "Adds external validation on open data.",
    "compute": {"tier": "laptop", "estimate": "a few hours"}, "est_weeks": 4, "scores": {"feasibility": 4, "novelty": 3},
}


def write_spec(tmp_path, spec):
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(spec))
    return str(p)


def test_new_study_creates_defaults_and_stubs(tmp_path):
    root = tmp_path / "studies"
    assert new_study.main([write_spec(tmp_path, SPEC), "--added-by", "scout", "--run-id", "r1"], root) == 0
    study = yaml.safe_load((root / "demo-study" / "study.yaml").read_text())
    assert study["status"] == "new" and study["added_by"] == "scout" and study["run_id"] == "r1"
    assert study["scores"] == {"fit": None, "feasibility": 4, "novelty": 3}
    assert "enriched: false" in (root / "demo-study" / "replication.md").read_text()


def test_new_study_refuses_existing_without_update(tmp_path):
    root = tmp_path / "studies"
    new_study.main([write_spec(tmp_path, SPEC)], root)
    assert new_study.main([write_spec(tmp_path, SPEC)], root) == 1


def test_update_merges_nested_and_protects_status(tmp_path):
    root = tmp_path / "studies"
    new_study.main([write_spec(tmp_path, SPEC)], root)
    patch = {"id": "demo-study", "status": "published", "scores": {"fit": 5}, "source": {"authors": "Doe J et al."}}
    assert new_study.main([write_spec(tmp_path, patch), "--update"], root) == 0
    study = yaml.safe_load((root / "demo-study" / "study.yaml").read_text())
    assert study["status"] == "new"
    assert study["scores"] == {"fit": 5, "feasibility": 4, "novelty": 3}
    assert study["source"]["authors"] == "Doe J et al." and study["source"]["title"] == "Paper"


def test_updated_appends_history_without_mutating():
    s = {"id": "x", "status": "new", "status_history": [{"status": "new", "date": "2026-01-01"}]}
    out = updated(s, "approved", "go", "2026-02-02")
    assert out["status"] == "approved" and out["status_history"][-1] == {"status": "approved", "date": "2026-02-02", "note": "go"}
    assert s["status"] == "new" and len(s["status_history"]) == 1


@pytest.mark.parametrize("status", ["bogus", "new"])
def test_updated_rejects_bad_or_same_status(status):
    with pytest.raises(StatusError):
        updated({"id": "x", "status": "new", "status_history": []}, status, "", "2026-01-01")


def test_set_status_needs_protocol_file(tmp_path):
    root = tmp_path / "studies"
    new_study.main([write_spec(tmp_path, SPEC)], root)
    assert set_status.main(["demo-study", "protocol"], root) == 1
    assert set_status.main(["demo-study", "approved", "looks", "good"], root) == 0
    study = yaml.safe_load((root / "demo-study" / "study.yaml").read_text())
    assert study["status_history"][-1]["note"] == "looks good"
    assert set_status.main(["missing", "approved"], root) == 1
