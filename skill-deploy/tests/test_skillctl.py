import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SKILLCTL_PATH = Path(__file__).resolve().parents[1] / "skillctl.py"


class SkillCtlTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "repo"
        self.root.mkdir()
        (self.root / "skill-deploy").mkdir()
        skill = self.root / "agent-operations" / "context-clear"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: context-clear\ndescription: >\n  Preserve context.\n---\n# Context Clear\n",
            encoding="utf-8",
        )
        registry = {
            "schema": "agent-skills-registry/v1",
            "skills": {
                "context-clear": {
                    "path": "agent-operations/context-clear",
                    "aliases": ["/cc", "cc"],
                    "targets": ["codex", "claude", "openai-cloud"],
                    "cloud": {"skill_id": None},
                }
            },
        }
        (self.root / "skill-deploy" / "registry.json").write_text(
            json.dumps(registry), encoding="utf-8"
        )
        spec = importlib.util.spec_from_file_location("skillctl_tested", SKILLCTL_PATH)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self.m.ROOT = self.root
        self.m.REGISTRY_PATH = self.root / "skill-deploy" / "registry.json"

    def tearDown(self):
        self.tmp.cleanup()

    def entry(self):
        reg = self.m.load_registry()
        return reg, self.m.get_entry(reg, "context-clear")

    def test_validate_and_secret_rejection(self):
        _, entry = self.entry()
        result = self.m.validate_skill("context-clear", entry)
        self.assertEqual(result["name"], "context-clear")
        p = self.root / "agent-operations" / "context-clear" / "secret.txt"
        p.write_text("sk-" + "A" * 32, encoding="utf-8")
        with self.assertRaises(self.m.SkillCtlError):
            self.m.validate_skill("context-clear", entry)

    def test_atomic_sync_and_drift_repair(self):
        _, entry = self.entry()
        out = self.root / "installed"
        receipts = self.m.sync_local("context-clear", entry, ["codex"], False, out)
        self.assertEqual(receipts[0]["status"], "synced")
        installed = out / "context-clear"
        self.assertEqual(
            self.m.fingerprint(installed), self.m.fingerprint(self.m.skill_path(entry))
        )
        (installed / "SKILL.md").write_text("drift", encoding="utf-8")
        self.assertNotEqual(
            self.m.fingerprint(installed), self.m.fingerprint(self.m.skill_path(entry))
        )
        self.m.sync_local("context-clear", entry, ["codex"], False, out)
        self.assertEqual(
            self.m.fingerprint(installed), self.m.fingerprint(self.m.skill_path(entry))
        )

    def test_package_is_deterministic(self):
        _, entry = self.entry()
        a = self.root / "a.zip"
        b = self.root / "b.zip"
        self.m.build_zip("context-clear", entry, a)
        self.m.build_zip("context-clear", entry, b)
        self.assertEqual(a.read_bytes(), b.read_bytes())

    def test_cloud_plan_switches_after_id(self):
        _, entry = self.entry()
        self.assertEqual(
            self.m.cloud_plan("context-clear", entry)["action"], "create-skill"
        )
        entry["cloud"]["skill_id"] = "skill_123"
        self.assertEqual(
            self.m.cloud_plan("context-clear", entry)["action"], "create-version"
        )

    def test_deploy_dry_run_needs_no_network(self):
        rc = self.m.main(["deploy", "context-clear", "--dry-run"])
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
