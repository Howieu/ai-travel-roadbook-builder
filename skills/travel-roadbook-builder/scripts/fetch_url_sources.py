#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def reader_url(url: str) -> str:
    return f"https://r.jina.ai/{url}"


def platform_from_url(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "xiaohongshu.com" in host or "xhslink.com" in host:
        return "xhs"
    if "notion.site" in host or "notion.so" in host:
        return "notion"
    if "feishu.cn" in host or "larksuite.com" in host:
        return "feishu"
    return "web"


def source_id(index: int, platform: str) -> str:
    prefix = "xhs" if platform == "xhs" else platform
    return f"{prefix}-{index:03d}"


def clean_lines(content: str) -> list[str]:
    return [line.strip() for line in content.splitlines() if line.strip()]


def extract_title(content: str, url: str) -> str:
    for line in clean_lines(content):
        if line.lower().startswith("title:"):
            title = line.split(":", 1)[1].strip()
            if title:
                return title
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            if title:
                return title
    host = urlparse(url).netloc
    return host or url


def excerpt(content: str, max_chars: int = 520) -> str:
    lines = []
    for line in clean_lines(content):
        lowered = line.lower()
        if lowered.startswith(("title:", "url:", "url source:", "markdown content:")):
            continue
        if line.startswith("!["):
            continue
        lines.append(line)
    text = re.sub(r"\s+", " ", " ".join(lines)).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "..."


def fetch_content(url: str, timeout: float) -> str:
    req = Request(reader_url(url), headers={"User-Agent": "travel-roadbook-builder/0.1"})
    with urlopen(req, timeout=timeout) as response:
        data = response.read()
    return data.decode("utf-8", errors="replace")


def build_source(url: str, index: int, captured_at: str, timeout: float = 20) -> dict:
    platform = platform_from_url(url)
    base = {
        "id": source_id(index, platform),
        "type": "guide",
        "platform": platform,
        "url": url,
        "readerUrl": reader_url(url),
        "title": None,
        "author": None,
        "capturedAt": captured_at,
        "excerpt": "",
        "accessStatus": "unreadable",
        "confidence": "low",
    }
    if platform == "xhs":
        base["excerpt"] = (
            "Xiaohongshu direct reading requires Agent Reach plus an active Xiaohongshu backend. "
            "Run `agent-reach install --channels opencli`, log into Xiaohongshu in Chrome, rerun doctor, "
            "or paste the note text/screenshots."
        )
        return base
    try:
        content = fetch_content(url, timeout)
    except Exception as exc:  # pragma: no cover - exact network errors vary by platform.
        base["error"] = str(exc)
        return base
    base.update(
        {
            "title": extract_title(content, url),
            "excerpt": excerpt(content),
            "accessStatus": "read",
            "confidence": "medium",
        }
    )
    return base


def urls_from_args(urls: list[str], file_path: str | None) -> list[str]:
    all_urls = list(urls)
    if file_path:
        all_urls.extend(Path(file_path).read_text(encoding="utf-8").splitlines())
    cleaned = []
    for url in all_urls:
        value = url.strip()
        if value and not value.startswith("#"):
            cleaned.append(value)
    return cleaned


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch public URL source records through Agent Reach's Jina Reader path.")
    parser.add_argument("urls", nargs="*", help="Public URLs to read.")
    parser.add_argument("--file", help="Newline-delimited URL list.")
    parser.add_argument("--out", help="Write JSON output to this path. Defaults to stdout.")
    parser.add_argument("--timeout", type=float, default=20, help="Per-URL timeout in seconds.")
    args = parser.parse_args()

    urls = urls_from_args(args.urls, args.file)
    if not urls:
        print("error: provide at least one URL or --file", file=sys.stderr)
        return 2

    captured_at = utc_now()
    payload = {"sources": [build_source(url, index, captured_at, args.timeout) for index, url in enumerate(urls, start=1)]}
    output = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
