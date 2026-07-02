#!/usr/bin/env python3
"""Shared GitHub helpers for skill install scripts."""

from __future__ import annotations

import os
import urllib.error
import urllib.request


def github_request(url: str, user_agent: str) -> bytes:
    headers = {"User-Agent": user_agent}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def github_api_contents_url(repo: str, path: str, ref: str) -> str:
    return f"https://api.github.com/repos/{repo}/contents/{path}?ref={ref}"


def raw_skill_md_exists(slug: str, ref: str, path: str) -> "bool | None":
    """Cheap check: does ``<path>/SKILL.md`` exist, via raw.githubusercontent.com?

    Returns ``True`` (exists), ``False`` (404 → absent), or ``None`` (inconclusive:
    rate limit / network error / possibly-private repo). raw.githubusercontent.com
    is a CDN — it is NOT subject to the api.github.com 60-req/hr unauth limit, it
    follows repo renames, and it costs ~0.3s instead of a full repo download. Lets a
    `--dry-run` reject a wrong ``--path`` in ~0.3s instead of ~20s.
    """
    bare = path.strip("/")
    sub = "" if bare in ("", ".", "..") else bare + "/"
    url = f"https://raw.githubusercontent.com/{slug}/{ref}/{sub}SKILL.md"
    headers = {"User-Agent": "phoenix-skill-install", "Range": "bytes=0-0"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return 200 <= resp.status < 400
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            # Public repo: 404 = absent. With a token the repo may be private and
            # raw may not honor it → stay safe and report inconclusive.
            return None if token else False
        return None
    except (urllib.error.URLError, TimeoutError, OSError):
        return None
