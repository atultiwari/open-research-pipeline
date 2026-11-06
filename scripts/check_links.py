#!/usr/bin/env python3
"""Fetch every external URL in studies/, datasets/ and journals/ and report the HTTP status.

Usage: python3 scripts/check_links.py [path ...]
Some publishers block automated clients (403/429); those are reported as 'blocked', not failures,
and should be checked by hand once. Timeouts are reported but do not fail the run.
Exit code 1 only for 404/410 or connection failures.
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "open-research-pipeline/1.0 (+https://github.com/atultiwari/open-research-pipeline)"
URL_RE = re.compile(r"https?://[^\s)'\"<>\]]+")
BLOCKED = {401, 403, 405, 406, 429, 451, 503}
DEAD = {404, 410}


def collect(paths: list[Path]) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for base in paths:
        files = [base] if base.is_file() else [*base.rglob("*.yaml"), *base.rglob("*.md")]
        for f in files:
            for url in URL_RE.findall(f.read_text(encoding="utf-8")):
                found.setdefault(url.rstrip(".,;:"), set()).add(str(f.relative_to(ROOT)))
    return found


def fetch(url: str) -> tuple[str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return url, str(resp.status)
    except urllib.error.HTTPError as err:
        return url, str(err.code)
    except urllib.error.URLError as err:
        reason = type(getattr(err, "reason", err)).__name__
        return url, "timeout" if "Timeout" in reason else f"error: {reason}"
    except TimeoutError:
        return url, "timeout"
    except Exception as err:  # noqa: BLE001 - report any network failure
        return url, f"error: {type(err).__name__}"


def main() -> int:
    args = [Path(a).resolve() for a in sys.argv[1:]] or [ROOT / d for d in ("studies", "datasets", "journals")]
    urls = collect(args)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = sorted(pool.map(fetch, urls))
    bad = 0
    for url, status in results:
        code = int(status) if status.isdigit() else None
        if status == "timeout":
            label = "TIMEOUT"
        elif code in DEAD or code is None:
            label, bad = "DEAD   ", bad + 1
        elif code in BLOCKED:
            label = "BLOCKED"
        else:
            label = "OK     "
        if label != "OK     ":
            print(f"{label} {status:>5} {url}  ({', '.join(sorted(urls[url]))})")
    print(f"\n{len(results)} URLs checked, {bad} dead or unreachable")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
