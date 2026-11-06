import pytest

from linkkit import classify, find_links, normalise_url


@pytest.mark.parametrize(
    "raw, kind, key",
    [
        ("https://arxiv.org/abs/2601.04163v1", "arxiv", "2601.04163v1"),
        ("https://arxiv.org/pdf/2411.14975", "arxiv", "2411.14975"),
        ("https://arxiv.org/html/2603.12886v1", "arxiv", "2603.12886v1"),
        ("2502.14302", "arxiv", "2502.14302"),
        ("https://www.medrxiv.org/content/10.1101/2024.01.08.24301018v1.full", "medrxiv", "10.1101/2024.01.08.24301018"),
        ("https://www.biorxiv.org/content/10.1101/2023.05.01.538999v2", "biorxiv", "10.1101/2023.05.01.538999"),
        ("10.3389/fmed.2026.1759988", "doi", "10.3389/fmed.2026.1759988"),
        ("doi:10.1038/s41591-024-02885-z", "doi", "10.1038/s41591-024-02885-z"),
        ("https://doi.org/10.17632/dmktk7t677.1", "doi", "10.17632/dmktk7t677.1"),
        ("https://www.frontiersin.org/journals/x/articles/10.3389/fdgth.2026.1701551/full", "doi", "10.3389/fdgth.2026.1701551"),
        ("https://pubmed.ncbi.nlm.nih.gov/38641744/", "pubmed", "38641744"),
        ("https://pmc.ncbi.nlm.nih.gov/articles/PMC1234567/", "pmc", "PMC1234567"),
        ("https://github.com/marrlab/DinoBloom.git", "github", "marrlab/DinoBloom"),
        ("https://github.com/mahmoodlab/TRIDENT/tree/main/docs", "github", "mahmoodlab/TRIDENT"),
        ("https://huggingface.co/datasets/owkin/plism-dataset", "hf-dataset", "owkin/plism-dataset"),
        ("https://huggingface.co/MahmoodLab/UNI2-h", "hf-model", "MahmoodLab/UNI2-h"),
        ("https://zenodo.org/records/10592256", "zenodo", "10592256"),
        ("https://physionet.org/content/mimiciv/3.1/", "physionet", "mimiciv/3.1"),
        ("https://www.kaggle.com/c/prostate-cancer-grade-assessment", "kaggle", "prostate-cancer-grade-assessment"),
        ("https://www.unb.ca/cic/datasets/iomt-dataset-2024.html", "web", "https://www.unb.ca/cic/datasets/iomt-dataset-2024.html"),
    ],
)
def test_classify(raw, kind, key):
    link = classify(raw)
    assert (link.kind, link.key) == (kind, key)


def test_normalise_url_ignores_version_scheme_and_format():
    assert normalise_url("https://arxiv.org/abs/2601.04163v1") == normalise_url("http://arxiv.org/pdf/2601.04163")
    assert normalise_url("https://doi.org/10.3389/FMED.2026.1759988") == "doi:10.3389/fmed.2026.1759988"
    assert normalise_url("https://www.example.org/a/b/?x=1#y") == normalise_url("http://example.org/a/b")
    assert normalise_url("https://github.com/MedHallu/MedHallu") == "github:medhallu/medhallu"


def test_find_links_sorts_code_data_papers():
    text = ("Code at https://github.com/a/b. Data: https://huggingface.co/datasets/c/d and "
            "https://zenodo.org/records/123. See arXiv:2501.00001 and doi 10.1000/xyz.")
    out = find_links(text)
    assert out["code"] == ["https://github.com/a/b"]
    assert out["datasets"] == ["https://huggingface.co/datasets/c/d", "https://zenodo.org/records/123"]
    assert out["papers"] == ["https://arxiv.org/abs/2501.00001"]
    assert out["dois"] == ["10.1000/xyz"]


def test_doi_cleaning_strips_markdown_but_keeps_balanced_parens():
    text = "See (doi 10.48550/arXiv.2411.14975)** and 10.1016/S0140-6736(20)30183-5."
    assert find_links(text)["dois"] == ["10.1016/S0140-6736(20)30183-5", "10.48550/arXiv.2411.14975"]
