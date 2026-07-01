#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen


DEFAULT_REMOTE = "https://raw.githubusercontent.com/Howieu/ai-travel-roadbook-builder/main/skills/travel-roadbook-builder/SKILL.md"


def skill_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def frontmatter(text: str) -> str:
    match = re.match(r"---\n(.*?)\n---", text, flags=re.S)
    return match.group(1) if match else ""


def metadata_value(text: str, key: str) -> str | None:
    match = re.search(rf"^\s*{re.escape(key)}:\s*[\"']?([^\"'\n]+)", frontmatter(text), flags=re.M)
    return match.group(1).strip() if match else None


def read_local_version(path: Path | None = None) -> str | None:
    skill_path = path or skill_dir() / "SKILL.md"
    return metadata_value(skill_path.read_text(encoding="utf-8"), "version")


def read_remote_text(url: str, timeout: float) -> str:
    request = Request(url, headers={"User-Agent": "travel-roadbook-builder-update-check"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def check_update(remote_url: str | None = None, timeout: float = 8, local_path: Path | None = None) -> dict:
    skill_path = local_path or skill_dir() / "SKILL.md"
    local_text = skill_path.read_text(encoding="utf-8")
    current = read_local_version(local_path)
    remote_url = remote_url or metadata_value(local_text, "update_url") or DEFAULT_REMOTE
    try:
        latest = metadata_value(read_remote_text(remote_url, timeout), "version")
    except Exception as exc:
        return {"status": "unknown", "current": current, "latest": None, "error": str(exc)}
    if not current or not latest:
        return {"status": "unknown", "current": current, "latest": latest, "error": "missing version metadata"}
    status = "current" if current == latest else "update_available"
    return {"status": status, "current": current, "latest": latest, "remote": remote_url}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check whether the installed Travel Roadbook Builder skill is stale.")
    parser.add_argument("--remote", help="Remote SKILL.md URL to compare against. Defaults to metadata.update_url.")
    parser.add_argument("--timeout", type=float, default=8, help="Network timeout in seconds.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    result = check_update(args.remote, args.timeout)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["status"] == "update_available":
        print(f"update_available: local {result['current']} -> remote {result['latest']}")
    elif result["status"] == "current":
        print(f"current: {result['current']}")
    else:
        print(f"unknown: {result.get('error', 'could not check update')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
