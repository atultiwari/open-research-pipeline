"""Shared helpers: polite HTTP, link classification and URL normalisation.

Used by fetch_meta.py and find_dupes.py. Standard library only.
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

USER_AGENT = "open-research-pipeline/1.0 (+https://github.com/atultiwari/open-research-pipeline)"
TIMEOUT = 30

ARXIV_ID = r"(\d{4}\.\d{4,5})(v\d+)?"
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\"'<>?#]+)", re.I)


@dataclass(frozen=True)
class Link:
    """A classified link. `key` is the identifier the fetcher needs (arXiv id, DOI, owner/repo, …)."""
    kind: str
    key: str
    url: str


class FetchError(RuntimeError):
    """Raised when a remote request fails; the message is safe to show to the user."""


RETRY_STATUS = {429, 500, 502, 503, 504}


def http_get(url: str, accept: str = "*/*", retries: int = 2, backoff: float = 3.0) -> bytes:
    """GET with a polite User-Agent; retries rate limits and server errors with a growing pause."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return resp.read()
        except urllib.error.HTTPError as err:
            if err.code in RETRY_STATUS and attempt < retries:
                time.sleep(backoff * (attempt + 1))
                continue
            raise FetchError(f"HTTP {err.code} for {url}") from err
        except (urllib.error.URLError, TimeoutError) as err:
            if attempt < retries:
                time.sleep(backoff * (attempt + 1))
                continue
            raise FetchError(f"Could not reach {url}: {getattr(err, 'reason', err)}") from err
    raise FetchError(f"Gave up on {url}")


def http_json(url: str) -> dict | list:
    raw = http_get(url, accept="application/json")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as err:
        raise FetchError(f"Response from {url} was not JSON") from err


def _clean_doi(doi: str) -> str:
    doi = urllib.parse.unquote(doi).rstrip(".,;*_`]")
    while doi.endswith(")") and doi.count(")") > doi.count("("):  # markdown "(doi)" leftovers
        doi = doi[:-1].rstrip(".,;*_`]")
    doi = re.sub(r"/(full|abstract|pdf|epdf|html|meta)$", "", doi, flags=re.I)
    return re.sub(r"(v\d+)?(\.full(\.pdf)?|\.abstract|\.pdf)?$", "", doi) if doi.startswith("10.1101/") else doi


RULES: list[tuple[str, re.Pattern]] = [
    ("arxiv", re.compile(rf"arxiv\.org/(?:abs|pdf|html)/{ARXIV_ID}", re.I)),
    ("biorxiv", re.compile(r"(?P<server>biorxiv|medrxiv)\.org/content/(?P<doi>10\.1101/[\d.]+)", re.I)),
    ("pubmed", re.compile(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", re.I)),
    ("pmc", re.compile(r"(?:ncbi\.nlm\.nih\.gov/pmc/articles|pmc\.ncbi\.nlm\.nih\.gov/articles)/(PMC\d+)", re.I)),
    ("github", re.compile(r"github\.com/([\w.-]+/[\w.-]+)", re.I)),
    ("hf-dataset", re.compile(r"huggingface\.co/datasets/([\w.-]+/[\w.-]+)", re.I)),
    ("hf-model", re.compile(r"huggingface\.co/(?!datasets/|spaces/|papers/)([\w.-]+/[\w.-]+)", re.I)),
    ("zenodo", re.compile(r"zenodo\.org/(?:records?|doi/10\.5281/zenodo\.)/?(\d+)", re.I)),
    ("figshare", re.compile(r"figshare\.com/articles/(?:[^/]+/)*(\d{5,})", re.I)),
    ("physionet", re.compile(r"physionet\.org/content/([\w.-]+)(?:/([\d.]+))?", re.I)),
    ("kaggle", re.compile(r"kaggle\.com/(?:datasets|competitions|c)/([\w.-]+(?:/[\w.-]+)?)", re.I)),
]


def classify(raw: str) -> Link:
    """Work out what kind of link this is. Bare arXiv ids and DOIs are accepted too."""
    text = raw.strip()
    if re.fullmatch(ARXIV_ID, text):
        return Link("arxiv", text, f"https://arxiv.org/abs/{text}")
    if re.fullmatch(r"(?:doi:)?10\.\d{4,9}/\S+", text, re.I):
        doi = _clean_doi(re.sub(r"^doi:", "", text, flags=re.I))
        return Link("doi", doi, f"https://doi.org/{doi}")
    for kind, pattern in RULES:
        m = pattern.search(text)
        if not m:
            continue
        if kind == "arxiv":
            return Link(kind, m.group(1) + (m.group(2) or ""), text)
        if kind == "biorxiv":
            return Link(m.group("server").lower(), _clean_doi(m.group("doi")), text)
        if kind in {"github", "hf-dataset", "hf-model"}:
            return Link(kind, re.sub(r"\.git$", "", m.group(1)), text)
        if kind == "physionet":
            return Link(kind, m.group(1) + (f"/{m.group(2)}" if m.group(2) else ""), text)
        return Link(kind, m.group(1), text)
    doi = DOI_RE.search(text)
    if doi:
        return Link("doi", _clean_doi(doi.group(1)), text)
    return Link("web", text, text)


def normalise_url(url: str) -> str:
    """Canonical form for duplicate checks: no scheme, www, query, fragment, trailing slash or arXiv version."""
    link = classify(url)
    if link.kind == "arxiv":
        return "arxiv:" + re.sub(r"v\d+$", "", link.key)
    if link.kind in {"doi", "biorxiv", "medrxiv"}:
        return f"doi:{link.key.lower()}"
    if link.kind in {"github", "hf-dataset", "hf-model"}:
        return f"{link.kind}:{link.key.lower()}"
    parts = urllib.parse.urlsplit(url.strip())
    host = parts.netloc.lower().removeprefix("www.")
    path = re.sub(r"/(index\.html?)?$", "", parts.path)
    return f"{host}{path}".lower()


def find_links(text: str) -> dict[str, list[str]]:
    """Pull code, dataset, paper and DOI links out of free text (abstracts, READMEs, cards)."""
    urls = re.findall(r"https?://[^\s)\]>\"'`]+", text or "")
    out: dict[str, list[str]] = {"code": [], "datasets": [], "papers": [], "dois": []}
    for u in dict.fromkeys(x.rstrip(".,;:") for x in urls):
        kind = classify(u).kind
        if kind == "github":
            out["code"].append(u)
        elif kind in {"hf-dataset", "zenodo", "figshare", "physionet", "kaggle"}:
            out["datasets"].append(u)
        elif kind in {"arxiv", "biorxiv", "medrxiv", "pubmed", "pmc"}:
            out["papers"].append(u)
    out["dois"] = sorted({_clean_doi(d) for d in DOI_RE.findall(text or "")})
    arxiv_mentions = re.findall(rf"arXiv[:\s]+{ARXIV_ID}", text or "", re.I)
    out["papers"] += [f"https://arxiv.org/abs/{a}" for a, _ in arxiv_mentions]
    out["papers"] = list(dict.fromkeys(out["papers"]))
    return out
