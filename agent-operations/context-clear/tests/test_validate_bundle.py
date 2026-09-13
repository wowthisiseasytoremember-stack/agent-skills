#!/usr/bin/env python3
"""Regression tests for Context Clear bundle validation."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_bundle.py"
SPEC = importlib.util.spec_from_file_location("context_clear_validator", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

GOOD_MD = """# Context Clear Checkpoint

## Resume in one sentence
Resume safely.

## Objective and definition of done
Finish the task.

## Canonical state
None known.

## Work completed
None known.

## Current execution state
None known.

## Decisions and constraints
None known.

## Evidence and validation
None known.

## Blockers and unresolved
None known.

## Next actions
1. Continue.

## Source-of-truth pointers
None known.

## Noncanonical / proposed
None known.

## Superseded
None known.

## Persistence receipt
Verified.
"""


class ContextClearValidatorTests(unittest.TestCase):
    def test_valid_bundle_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md_path = root / "CONTEXT_CLEAR.md"
            md_path.write_text(GOOD_MD, encoding="utf-8")
            digest = hashlib.sha256(GOOD_MD.encode("utf-8")).hexdigest()
            manifest_path = root / "context-clear.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "schema": "context-clear/v1",
                        "checkpoint_id": "20260913T051500Z-test-a1b2c3d4",
                        "created_at": "2026-09-13T05:15:00Z",
                        "project": "test",
                        "resume": "Resume safely.",
                        "status": "verified",
                        "content_sha256": digest,
                        "destinations": [
                            {
                                "type": "git",
                                "locator": "owner/repo:path@abc123",
                                "verified": True,
                                "verification": "read-back",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            md_ok, observed_digest = VALIDATOR.validate_markdown(md_path)
            self.assertTrue(md_ok)
            self.assertEqual(digest, observed_digest)
            self.assertTrue(VALIDATOR.validate_manifest(manifest_path, observed_digest))

    def test_missing_required_heading_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            md_path = Path(tmp) / "CONTEXT_CLEAR.md"
            md_path.write_text(
                GOOD_MD.replace("## Next actions", "## Missing next actions"),
                encoding="utf-8",
            )
            md_ok, _ = VALIDATOR.validate_markdown(md_path)
            self.assertFalse(md_ok)

    def test_verified_manifest_requires_verified_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md_path = root / "CONTEXT_CLEAR.md"
            md_path.write_text(GOOD_MD, encoding="utf-8")
            digest = hashlib.sha256(GOOD_MD.encode("utf-8")).hexdigest()
            manifest_path = root / "context-clear.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "schema": "context-clear/v1",
                        "checkpoint_id": "20260913T051500Z-test-a1b2c3d4",
                        "created_at": "2026-09-13T05:15:00Z",
                        "project": "test",
                        "resume": "Resume safely.",
                        "status": "verified",
                        "content_sha256": digest,
                        "destinations": [
                            {
                                "type": "server",
                                "locator": "/durable/path",
                                "verified": False,
                                "verification": "write only",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            self.assertFalse(VALIDATOR.validate_manifest(manifest_path, digest))

    def test_secret_pattern_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            md_path = Path(tmp) / "CONTEXT_CLEAR.md"
            md_path.write_text(
                GOOD_MD.replace("Verified.", "Verified. sk-" + "A" * 24),
                encoding="utf-8",
            )
            md_ok, _ = VALIDATOR.validate_markdown(md_path)
            self.assertFalse(md_ok)


if __name__ == "__main__":
    unittest.main()
