from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills/travel-roadbook-builder/scripts/check_skill_update.py"
spec = importlib.util.spec_from_file_location("check_skill_update", MODULE_PATH)
checker = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(checker)


class CheckSkillUpdateTest(unittest.TestCase):
    def write_skill(self, version: str) -> Path:
        path = Path(tempfile.mkdtemp()) / "SKILL.md"
        path.write_text(f'---\nname: demo\nmetadata:\n  version: "{version}"\n---\n', encoding="utf-8")
        return path

    def test_reports_update_available(self) -> None:
        local = self.write_skill("0.1.0")
        remote = '---\nname: demo\nmetadata:\n  version: "0.2.0"\n---\n'
        with mock.patch.object(checker, "read_remote_text", return_value=remote):
            result = checker.check_update(local_path=local)
        self.assertEqual(result["status"], "update_available")
        self.assertEqual(result["current"], "0.1.0")
        self.assertEqual(result["latest"], "0.2.0")

    def test_reports_current(self) -> None:
        local = self.write_skill("0.2.0")
        remote = '---\nname: demo\nmetadata:\n  version: "0.2.0"\n---\n'
        with mock.patch.object(checker, "read_remote_text", return_value=remote):
            result = checker.check_update(local_path=local)
        self.assertEqual(result["status"], "current")


if __name__ == "__main__":
    unittest.main()
