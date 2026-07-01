from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills/travel-roadbook-builder/scripts/render_roadbook.py"
spec = importlib.util.spec_from_file_location("render_roadbook", MODULE_PATH)
renderer = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(renderer)


class RendererTest(unittest.TestCase):
    def test_demo_renders_map_links(self) -> None:
        data = json.loads((ROOT / "skills/travel-roadbook-builder/examples/paris-roadbook.json").read_text())
        errors = renderer.validate(data)
        self.assertEqual(errors, [])

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "demo.html"
            html = renderer.render(data, "../assets/roadbook.css")
            output.write_text(html, encoding="utf-8")
            self.assertIn("Paris 3-Day Roadbook", html)
            self.assertIn("Google Maps", html)
            self.assertIn("Apple Maps", html)
            self.assertIn("uri.amap.com", html)

    def test_validation_requires_stop_name(self) -> None:
        data = {
            "trip": {"title": "Demo", "destination": "Paris"},
            "days": [{"date": "2026-05-20", "stops": [{}]}],
        }
        self.assertIn("days[1].stops[1] missing name", renderer.validate(data))


if __name__ == "__main__":
    unittest.main()
