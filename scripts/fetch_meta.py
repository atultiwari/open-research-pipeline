#!/usr/bin/env python3
"""Fetch metadata for a research link deterministically, from public APIs only.

Usage:
    python3 scripts/fetch_meta.py <url-or-id> [more ...]      # prints a JSON list
    python3 scripts/fetch_meta.py --pretty https://arxiv.org/abs/2601.04163

Supports arXiv, bioRxiv/medRxiv, DOI (Crossref, OpenAlex fallback), PubMed/PMC (E-utilities),
GitHub, Hugging Face datasets and models, Zenodo, Figshare, PhysioNet, Kaggle, and any web page
with citation meta tags. The abstract/README excerpt is returned for Claude to read; it must be
summarised in Claude's own words and never committed verbatim.
"""
from __future__ import annotations

import base64
import html
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from linkkit import FetchError, Link, classify, find_links, http_get, http_json  # noqa: E402

ATOM = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
EXCERPT = 4000  # characters of abstract/README kept for reading


def record(link: Link, **fields) -> dict:
    base = {"input": link.url, "kind": link.kind, "title": None, "authors": [], "date": None, "venue": None,
            "doi": None, "arxiv_id": None, "url": link.url, "licence": None, "gated": None, "size": None,
            "text_excerpt": None, "links": {"code": [], "datasets": [], "papers": [], "dois": []},
            "extra": {}, "warnings": []}
    merged = {**base, **{k: v for k, v in fields.items() if v is not None}}
    if merged["text_excerpt"]:
        merged["links"] = find_links(merged["text_excerpt"])
        merged["text_excerpt"] = merged["text_excerpt"][:EXCERPT]
    return merged


def fetch_arxiv(link: Link) -> dict:
    raw = http_get(f"https://export.arxiv.org/api/query?id_list={link.key}")
    entry = ET.fromstring(raw).find("a:entry", ATOM)
    if entry is None or entry.find("a:title", ATOM) is None:
        raise FetchError(f"arXiv has no record for {link.key}")
    text = lambda tag: (entry.findtext(tag, default="", namespaces=ATOM) or "").strip()  # noqa: E731
    comment = text("arxiv:comment")
    return record(
        link, title=re.sub(r"\s+", " ", text("a:title")),
        authors=[a.findtext("a:name", namespaces=ATOM) for a in entry.findall("a:author", ATOM)],
        date=text("a:published")[:10], venue=f"arXiv ({entry.find('arxiv:primary_category', ATOM).get('term')})",
        doi=text("arxiv:doi") or None, arxiv_id=text("a:id").rsplit("/", 1)[-1], url=f"https://arxiv.org/abs/{link.key}",
        text_excerpt=f"{text('a:summary')}\n\nComment: {comment}",
        extra={"updated": text("a:updated")[:10], "comment": comment, "journal_ref": text("arxiv:journal_ref") or None},
    )


def fetch_biorxiv(link: Link) -> dict:
    data = http_json(f"https://api.biorxiv.org/details/{link.kind}/{link.key}")
    versions = data.get("collection") or []
    if not versions:
        raise FetchError(f"{link.kind} has no record for {link.key}")
    v = versions[-1]
    return record(
        link, title=v.get("title"), authors=[a.strip() for a in (v.get("authors") or "").split(";") if a.strip()],
        date=v.get("date"), venue=f"{link.kind} ({v.get('category')})", doi=v.get("doi"),
        licence=v.get("license"), url=f"https://www.{link.kind}.org/content/{v.get('doi')}v{v.get('version')}",
        text_excerpt=v.get("abstract"),
        extra={"version": v.get("version"), "published_doi": v.get("published") if v.get("published") != "NA" else None},
    )


def _openalex(doi: str, link: Link) -> dict:
    w = http_json(f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}")
    inv = w.get("abstract_inverted_index") or {}
    words = sorted((pos, word) for word, poss in inv.items() for pos in poss)
    return record(
        link, title=w.get("title"), authors=[a["author"]["display_name"] for a in w.get("authorships", [])],
        date=w.get("publication_date"), venue=((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
        doi=doi, licence=(w.get("primary_location") or {}).get("license"), url=f"https://doi.org/{doi}",
        text_excerpt=" ".join(word for _, word in words) or None,
        extra={"source": "openalex", "cited_by_count": w.get("cited_by_count"), "openalex_id": w.get("id")},
    )


def fetch_doi(link: Link) -> dict:
    doi = link.key
    try:
        m = http_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")["message"]
    except FetchError as err:
        rec = _openalex(doi, link)
        rec["warnings"].append(f"Crossref failed ({err}); used OpenAlex")
        return rec
    parts = (m.get("issued") or {}).get("date-parts", [[None]])[0]
    abstract = re.sub(r"<[^>]+>", " ", m.get("abstract") or "")
    return record(
        link, title=(m.get("title") or [None])[0],
        authors=[" ".join(filter(None, [a.get("given"), a.get("family")])) for a in m.get("author", [])],
        date="-".join(f"{p:02d}" if i else str(p) for i, p in enumerate(parts) if p) or None,
        venue=(m.get("container-title") or [None])[0] or m.get("publisher"), doi=doi,
        licence=((m.get("license") or [{}])[0]).get("URL"), url=m.get("URL") or f"https://doi.org/{doi}",
        text_excerpt=html.unescape(abstract).strip() or None,
        extra={"source": "crossref", "type": m.get("type"), "publisher": m.get("publisher"),
               "is_referenced_by_count": m.get("is-referenced-by-count")},
    )


EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def fetch_pubmed(link: Link) -> dict:
    db, uid = ("pmc", link.key.removeprefix("PMC")) if link.kind == "pmc" else ("pubmed", link.key)
    s = http_json(f"{EUTILS}/esummary.fcgi?db={db}&id={uid}&retmode=json")["result"][uid]
    ids = {i.get("idtype"): i.get("value") for i in s.get("articleids", [])}
    doi = ids.get("doi")
    abstract = None
    if db == "pubmed":
        xml = http_get(f"{EUTILS}/efetch.fcgi?db=pubmed&id={uid}&retmode=xml")
        abstract = " ".join("".join(t.itertext()) for t in ET.fromstring(xml).iter("AbstractText")) or None
    return record(
        link, title=s.get("title"), authors=[a.get("name") for a in s.get("authors", [])],
        date=s.get("sortpubdate", "")[:10].replace("/", "-") or s.get("pubdate"), venue=s.get("fulljournalname") or s.get("source"),
        doi=doi, text_excerpt=abstract, extra={"pmid": ids.get("pubmed") or uid, "pmcid": ids.get("pmc") or ids.get("pmcid")},
    )


def _github_api(path: str) -> dict:
    if shutil.which("gh"):
        out = subprocess.run(["gh", "api", path], capture_output=True, text=True, timeout=60)
        if out.returncode == 0:
            return json.loads(out.stdout)
    return http_json(f"https://api.github.com/{path}")


def fetch_github(link: Link) -> dict:
    repo = _github_api(f"repos/{link.key}")
    readme = ""
    try:
        readme = base64.b64decode(_github_api(f"repos/{link.key}/readme").get("content", "")).decode("utf-8", "replace")
    except (FetchError, json.JSONDecodeError, ValueError):
        pass
    commits = _github_api(f"repos/{link.key}/commits?per_page=1")
    last = commits[0]["commit"]["committer"]["date"][:10] if isinstance(commits, list) and commits else None
    lic = repo.get("license") or {}
    rec = record(
        link, title=repo.get("full_name"), authors=[repo.get("owner", {}).get("login")], date=(repo.get("created_at") or "")[:10],
        venue="GitHub", licence=lic.get("spdx_id") or "None (no licence file)", url=repo.get("html_url"),
        text_excerpt=f"{repo.get('description') or ''}\n\n{readme}",
        extra={"description": repo.get("description"), "stars": repo.get("stargazers_count"), "last_commit": last,
               "archived": repo.get("archived"), "default_branch": repo.get("default_branch"), "homepage": repo.get("homepage")},
    )
    if lic.get("spdx_id") in (None, "NOASSERTION"):
        rec["warnings"].append("No standard licence: reimplement rather than copy code")
    return rec


def fetch_hf(link: Link) -> dict:
    kind = "datasets" if link.kind == "hf-dataset" else "models"
    d = http_json(f"https://huggingface.co/api/{kind}/{link.key}")
    card = d.get("cardData") or {}
    tags = d.get("tags") or []
    arxiv = [t.split(":", 1)[1] for t in tags if t.startswith("arxiv:")]
    readme = ""
    try:
        readme = http_get(f"https://huggingface.co/{'datasets/' if kind == 'datasets' else ''}{link.key}/raw/main/README.md").decode("utf-8", "replace")
    except FetchError:
        pass
    lic = card.get("license")
    rec = record(
        link, title=card.get("pretty_name") or d.get("id"), authors=[d.get("author")], date=(d.get("createdAt") or "")[:10],
        venue="Hugging Face", licence=", ".join(lic) if isinstance(lic, list) else lic, gated=d.get("gated"),
        size=next((t.split(":", 1)[1] for t in tags if t.startswith("size_categories:")), None),
        url=f"https://huggingface.co/{'datasets/' if kind == 'datasets' else ''}{link.key}",
        text_excerpt=readme or None,
        extra={"downloads": d.get("downloads"), "likes": d.get("likes"), "last_modified": (d.get("lastModified") or "")[:10],
               "arxiv_ids": arxiv, "tags": tags[:30]},
    )
    rec["links"]["papers"] = list(dict.fromkeys(rec["links"]["papers"] + [f"https://arxiv.org/abs/{a}" for a in arxiv]))
    if d.get("gated"):
        rec["warnings"].append(f"Gated on Hugging Face ({d.get('gated')}): access request needed")
    if lic and re.search(r"nc|nd", str(lic), re.I):
        rec["warnings"].append(f"Licence {lic} has non-commercial and/or no-derivatives terms")
    return rec


def fetch_zenodo(link: Link) -> dict:
    d = http_json(f"https://zenodo.org/api/records/{link.key}")
    m = d.get("metadata", {})
    return record(
        link, title=m.get("title"), authors=[c.get("name") for c in m.get("creators", [])], date=m.get("publication_date"),
        venue="Zenodo", doi=d.get("doi") or m.get("doi"), licence=(m.get("license") or {}).get("id"),
        size=f"{sum(f.get('size', 0) for f in d.get('files', [])) / 1e9:.2f} GB", url=d.get("links", {}).get("html", link.url),
        text_excerpt=re.sub(r"<[^>]+>", " ", m.get("description") or ""),
        extra={"access_right": m.get("access_right"), "version": m.get("version")},
    )


def fetch_figshare(link: Link) -> dict:
    d = http_json(f"https://api.figshare.com/v2/articles/{link.key}")
    return record(
        link, title=d.get("title"), authors=[a.get("full_name") for a in d.get("authors", [])],
        date=(d.get("published_date") or "")[:10], venue="Figshare", doi=d.get("doi"),
        licence=(d.get("license") or {}).get("name"), size=f"{d.get('size', 0) / 1e9:.2f} GB",
        url=d.get("url_public_html", link.url), text_excerpt=re.sub(r"<[^>]+>", " ", d.get("description") or ""),
    )


def _meta_tags(page: str) -> dict[str, list[str]]:
    tags: dict[str, list[str]] = {}
    for m in re.finditer(r"<meta\s+[^>]*?(?:name|property)=[\"']([^\"']+)[\"'][^>]*?content=[\"']([^\"']*)[\"']", page, re.I):
        tags.setdefault(m.group(1).lower(), []).append(html.unescape(m.group(2)))
    return tags


def fetch_web(link: Link) -> dict:
    page = http_get(link.url).decode("utf-8", "replace")
    t = _meta_tags(page)
    first = lambda *keys: next((t[k][0] for k in keys if t.get(k)), None)  # noqa: E731
    title_tag = re.search(r"<title[^>]*>(.*?)</title>", page, re.S | re.I)
    body = re.sub(r"<script.*?</script>|<style.*?</style>", " ", page, flags=re.S | re.I)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body))
    rec = record(
        link, title=first("citation_title", "dc.title", "og:title") or (html.unescape(title_tag.group(1).strip()) if title_tag else None),
        authors=t.get("citation_author", []) or t.get("dc.creator", []),
        date=first("citation_publication_date", "citation_date", "dc.date"), venue=first("citation_journal_title", "og:site_name"),
        doi=first("citation_doi", "dc.identifier"), text_excerpt=first("citation_abstract", "description", "og:description") or text[:EXCERPT],
    )
    if link.kind == "physionet":
        lic = re.search(r"<dt>License</dt>\s*<dd>\s*<a[^>]*>(.*?)</a>", page, re.S) or re.search(
            r"License \(for files\):.*?<a[^>]*>(.*?)</a>", page, re.S)
        access = re.search(r"(Credentialed|Restricted|Open|Contributor Review) Access", page)
        rec.update(licence=html.unescape(lic.group(1)).strip() if lic else "verify", venue="PhysioNet",
                   extra={"access_policy": access.group(0) if access else "verify"})
        if access and access.group(1) in {"Credentialed", "Restricted", "Contributor Review"}:
            rec["warnings"].append("PhysioNet credentialing + CITI training needed (~1–2 weeks); DUA forbids redistribution")
    if link.kind == "kaggle":
        rec["warnings"].append("Kaggle needs an account; licence shown only when signed in (verify)")
        rec["licence"] = rec["licence"] or "verify"
    return rec


FETCHERS = {
    "arxiv": fetch_arxiv, "biorxiv": fetch_biorxiv, "medrxiv": fetch_biorxiv, "doi": fetch_doi,
    "pubmed": fetch_pubmed, "pmc": fetch_pubmed, "github": fetch_github, "hf-dataset": fetch_hf, "hf-model": fetch_hf,
    "zenodo": fetch_zenodo, "figshare": fetch_figshare, "physionet": fetch_web, "kaggle": fetch_web, "web": fetch_web,
}


def fetch(raw: str) -> dict:
    link = classify(raw)
    try:
        return FETCHERS[link.kind](link)
    except (FetchError, KeyError, IndexError, TypeError, ValueError, ET.ParseError) as err:
        return {"input": raw, "kind": link.kind, "url": link.url, "error": f"{type(err).__name__}: {err}"}


def main(argv: list[str]) -> int:
    pretty = "--pretty" in argv
    items = [a for a in argv if not a.startswith("--")]
    if not items:
        print(__doc__)
        return 2
    results = [fetch(a) for a in items]
    print(json.dumps(results, indent=2 if pretty else None, ensure_ascii=False))
    return 1 if all("error" in r for r in results) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
