"""No-network contract tests for the shared PR risk classifier."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from risk import classify_files, classify_one, load_policy  # noqa: E402


EMPTY = {"additional_high": [], "additional_medium": []}


class RiskPolicyTests(unittest.TestCase):
    def test_docs_only_are_low(self):
        self.assertEqual(classify_files(["README.md", "docs/overview.md"], EMPTY)["tier"], "low")

    def test_python_change_is_medium(self):
        self.assertEqual(classify_one("src/service.py", EMPTY)[0], "medium")

    def test_releasing_and_workflow_paths_are_high(self):
        for filename in (
            ".github/workflows/ci.yml", ".github/pr-risk-policy.json",
            "AGENTS.md", "publish/youtube.py", "src/auth/token.py",
            "deploy/compose.yaml", ".env.production",
        ):
            with self.subTest(filename=filename):
                self.assertEqual(classify_one(filename, EMPTY)[0], "high")

    def test_repo_specific_patterns_escalate_only(self):
        policy = {"additional_high": ["ops/approval/**"], "additional_medium": ["assets/**"]}
        self.assertEqual(classify_one("ops/approval/gates.txt", policy)[0], "high")
        self.assertEqual(classify_one("assets/cat.jpg", policy)[0], "medium")
        self.assertEqual(classify_one("publish/upload.py", policy)[0], "high")

    def test_invalid_policy_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "policy.json"
            p.write_text('{"downgrade":["publish/**"]}')
            with self.assertRaises(ValueError):
                load_policy(p)

    def test_empty_or_traversal_fails_closed(self):
        with self.assertRaises(ValueError):
            classify_files([], EMPTY)
        with self.assertRaises(ValueError):
            classify_one("../unsafe.py", EMPTY)

    def test_ndjson_cli_produces_machine_readable_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            files = tmp / "files.ndjson"
            output = tmp / "report.json"
            summary = tmp / "summary.md"
            files.write_text('{"filename":"README.md"}\n{"filename":"src/thing.py"}\n')
            proc = subprocess.run(
                [sys.executable, str(Path(__file__).with_name("risk.py")),
                 "--files", str(files), "--output", str(output),
                 "--summary", str(summary)],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            self.assertEqual(json.loads(output.read_text())["tier"], "medium")
            self.assertIn("MEDIUM", summary.read_text())


if __name__ == "__main__":
    unittest.main()
