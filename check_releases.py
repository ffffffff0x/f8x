#!/usr/bin/env python3
"""Check GitHub releases against versions declared in the f8x script.

Usage:
  HTTP(S)_PROXY env vars are honored (e.g. http://127.0.0.1:7890).
  Optionally set GITHUB_TOKEN to raise rate limits.
  python3 check_releases.py --file f8x --output diff.txt
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import quote

import requests

# Regex for GitHub release comment and version assignment
REPO_COMMENT = re.compile(r"^#\s+https://github.com/([^/\s]+)/([^/\s]+)")
ASSIGNMENT = re.compile(r"^\s*([A-Za-z0-9_]+)\s*=\s*\"([^\"]+)\"")


@dataclass
class Entry:
    owner: str
    repo: str
    var: str
    current: str


class VersionComparer:
    def __init__(self) -> None:
        self._packaging = self._load_packaging()

    @staticmethod
    def _load_packaging():
        try:
            from packaging import version as pkg_version  # type: ignore

            return pkg_version
        except Exception:
            return None

    @staticmethod
    def _clean(ver: str) -> str:
        # Keep the first token, strip leading refs like v/"Version"
        ver = ver.strip()
        ver = ver.split()[0]
        ver = ver.lstrip("vV")
        return ver

    def is_newer(self, latest: str, current: str) -> bool:
        latest_clean = self._clean(latest)
        current_clean = self._clean(current)

        if self._packaging:
            try:
                return self._packaging.parse(latest_clean) > self._packaging.parse(current_clean)
            except Exception:
                pass

        # Fallback: simple inequality check
        return latest_clean != current_clean


def parse_entries(lines: Iterable[str]) -> List[Entry]:
    entries: List[Entry] = []
    pending_repo: Optional[Tuple[str, str]] = None

    for line in lines:
        comment_match = REPO_COMMENT.match(line)
        if comment_match:
            pending_repo = (comment_match.group(1), comment_match.group(2))
            continue

        if pending_repo is None:
            continue

        assign_match = ASSIGNMENT.match(line)
        if assign_match:
            var_name, value = assign_match.groups()
            if "Ver" in var_name or "Version" in var_name:
                entries.append(Entry(pending_repo[0], pending_repo[1], var_name, value))
                pending_repo = None  # Only grab the first version line after a repo comment

    return entries


def fetch_latest(owner: str, repo: str, session: requests.Session, verbose: bool = False) -> Optional[str]:
    api_base = f"https://api.github.com/repos/{owner}/{repo}"
    for endpoint in ("releases/latest", "tags"):
        url = f"{api_base}/{endpoint}"
        resp = session.get(url, timeout=15)
        if resp.status_code == 404:
            continue
        if not resp.ok:
            if verbose:
                print(f"{owner}/{repo} {endpoint} -> HTTP {resp.status_code}")
            return None
        data = resp.json()
        if endpoint == "releases/latest":
            tag = data.get("tag_name")
            if tag:
                return tag
        else:
            if isinstance(data, list) and data:
                tag = data[0].get("name")
                if tag:
                    return tag
    return None


def release_url(owner: str, repo: str, tag: str) -> str:
    # Encode tag to handle characters like + or spaces safely in URLs
    return f"https://github.com/{owner}/{repo}/releases/tag/{quote(tag, safe='')}"


def build_session(proxy: Optional[str]) -> requests.Session:
    session = requests.Session()
    proxies: Dict[str, str] = {}
    if proxy:
        proxies = {"http": proxy, "https": proxy}
    else:
        if os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy"):
            proxies["http"] = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
        if os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy"):
            proxies["https"] = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxies:
        session.proxies.update(proxies)

    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    session.headers.update(headers)
    return session


def load_file(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Compare f8x versions with GitHub releases")
    parser.add_argument("--file", default="f8x", help="Path to the f8x bash file")
    parser.add_argument("--output", default="diff.txt", help="Where to write differences")
    parser.add_argument("--proxy", default="http://127.0.0.1:7890", help="Proxy URL, overrides HTTP(S)_PROXY")
    parser.add_argument("--verbose", action="store_true", help="Print fetch errors and skips")
    args = parser.parse_args(argv)

    lines = load_file(args.file)
    entries = parse_entries(lines)

    session = build_session(args.proxy)
    comparer = VersionComparer()

    updates: List[str] = []
    for entry in entries:
        latest = fetch_latest(entry.owner, entry.repo, session, verbose=args.verbose)
        if not latest:
            continue
        if comparer.is_newer(latest, entry.current):
            updates.append(
                f"{entry.owner}/{entry.repo}: {entry.current} -> {latest} ({entry.var}) "
                f"{release_url(entry.owner, entry.repo, latest)}"
            )

    with open(args.output, "w", encoding="utf-8") as out:
        if updates:
            out.write("\n".join(updates))
        else:
            out.write("All tracked GitHub projects are up to date.\n")

    print(f"Checked {len(entries)} repositories; updates written to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
