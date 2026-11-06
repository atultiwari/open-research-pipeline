from find_dupes import find

STUDIES = [
    {"id": "plism-scanner", "title": "T1", "status": "new",
     "source": {"title": "Scanner-Induced Domain Shifts Undermine the Robustness of Pathology Foundation Models",
                "url": "https://arxiv.org/abs/2601.04163v1", "arxiv_id": "2601.04163v1"},
     "datasets": [{"id": "plism", "role": "benchmark"}]},
    {"id": "cirrhosis", "title": "T2", "status": "approved",
     "source": {"title": "Cirrhosis model", "url": "https://www.frontiersin.org/x", "doi": "10.3389/fmed.2026.1759988",
                "code_url": "https://github.com/a/b"},
     "datasets": []},
]
DATASETS = [{"id": "plism", "url": "https://huggingface.co/datasets/owkin/plism-dataset"}]


def test_matches_arxiv_across_versions():
    r = find(["https://arxiv.org/pdf/2601.04163v2"], [], [], STUDIES, DATASETS)
    assert [m["id"] for m in r["matches"]] == ["plism-scanner"]


def test_matches_doi_from_metadata_and_code_repo():
    assert find([], [], [{"doi": "10.3389/FMED.2026.1759988"}], STUDIES, DATASETS)["matches"][0]["id"] == "cirrhosis"
    assert find(["https://github.com/a/b"], [], [], STUDIES, DATASETS)["matches"][0]["id"] == "cirrhosis"


def test_fuzzy_title_match():
    r = find([], ["Scanner induced domain shifts undermine the robustness of pathology foundation models"], [], STUDIES, DATASETS)
    assert r["matches"][0]["id"] == "plism-scanner"


def test_dataset_link_gives_related_not_match():
    r = find(["https://huggingface.co/datasets/owkin/plism-dataset"], [], [], STUDIES, DATASETS)
    assert r["matches"] == []
    assert r["related"][0]["id"] == "plism-scanner"


def test_unrelated_link_finds_nothing():
    r = find(["https://arxiv.org/abs/2001.00001"], ["Something else entirely"], [], STUDIES, DATASETS)
    assert r["matches"] == [] and r["related"] == []
