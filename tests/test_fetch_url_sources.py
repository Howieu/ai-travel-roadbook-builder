from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills/travel-roadbook-builder/scripts/fetch_url_sources.py"
spec = importlib.util.spec_from_file_location("fetch_url_sources", MODULE_PATH)
fetcher = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(fetcher)


class FakeResponse:
    def __init__(self, body: str) -> None:
        self.body = body

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.body.encode("utf-8")


class FetchUrlSourcesTest(unittest.TestCase):
    def test_build_source_from_jina_reader_response(self) -> None:
        body = """Title: Paris First-Time Guide
URL Source: https://example.com/paris

Markdown Content:
The Louvre needs an advance ticket. Le Marais works well for cafes and shopping.
"""
        with mock.patch.object(fetcher, "urlopen", return_value=FakeResponse(body)) as urlopen_mock:
            source = fetcher.build_source("https://example.com/paris", 1, "2026-07-01T00:00:00Z", timeout=1)

        self.assertEqual(source["id"], "web-001")
        self.assertEqual(source["platform"], "web")
        self.assertEqual(source["readerUrl"], "https://r.jina.ai/https://example.com/paris")
        self.assertEqual(source["title"], "Paris First-Time Guide")
        self.assertEqual(source["accessStatus"], "read")
        self.assertEqual(source["confidence"], "medium")
        self.assertIn("Louvre", source["excerpt"])
        self.assertNotIn("URL Source:", source["excerpt"])
        urlopen_mock.assert_called_once()

    def test_xhs_url_is_recorded_without_fake_read(self) -> None:
        source = fetcher.build_source("https://www.xiaohongshu.com/explore/demo", 2, "2026-07-01T00:00:00Z", timeout=1)

        self.assertEqual(source["id"], "xhs-002")
        self.assertEqual(source["platform"], "xhs")
        self.assertEqual(source["accessStatus"], "unreadable")
        self.assertEqual(source["confidence"], "low")
        self.assertIn("agent-reach install --channels opencli", source["excerpt"])


if __name__ == "__main__":
    unittest.main()
