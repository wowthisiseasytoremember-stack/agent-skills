#!/usr/bin/env python3
"""Validate a Context Clear checkpoint bundle using only the Python stdlib."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA = "context-clear/v1"

REQUIRED_HEADINGS = [
    "# Context Clear Checkpoint",
    "## Resume in one sentence",
    "## Objective and definition of done",
    "## Canonical state",
    "## Work completed",
    "## Current execution state",
    "## Decisions and constraints",
    "## Evidence and validation",
    "## Blockers and unresolved",
    "## Next actions",
    "## Source-of-truth pointers",
    "## Noncanonical / proposed",
    "## Superseded",
    "## Persistence receipt",
]

# Conservative high-signal patterns. This is a guardrail, not a full secret scanner.
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "bearer token": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}\b", re.IGNORECASE),
}

REQUIRED_MANIFEST_FIELDS = {
    "schema",
    "checkpoint_id",
    "created_at",
    "project",
    "resume",
    "status",
    "content_sha256",
    "destinations",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)


def validate_markdown(path: Path) -> tuple[bool, str]:
    text = path.read_text(encoding="utf-8")
    ok = True

    positions: list[int] = []
    for heading in REQUIRED_HEADINGS:
        pos = text.find(heading)
        if pos < 0:
            fail(f"missing required heading: {heading}")
            ok = False
        positions.append(pos)

    present_positions = [p for p in positions if p >= 0]
    if present_positions != sorted(present_positions):
        fail("required headings are not in canonical order")
        ok = False

    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            fail(f"possible credential detected ({label})")
            ok = False

    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return ok, digest


def validate_manifest(path: Path, expected_digest: str) -> bool:
    ok = True
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"manifest is not valid readable JSON: {exc}")
        return False

    missing = REQUIRED_MANIFEST_FIELDS - data.keys()
    if missing:
        fail(f"manifest missing required fields: {', '.join(sorted(missing))}")
        ok = False

    if data.get("schema") != SCHEMA:
        fail(f"manifest schema must be {SCHEMA!r}")
        ok = False

    if data.get("status") not in {"prepared", "persisted", "verified"}:
        fail("manifest status must be prepared, persisted, or verified")
        ok = False

    if data.get("content_sha256") != expected_digest:
        fail("manifest content_sha256 does not match CONTEXT_CLEAR.md")
        ok = False

    destinations = data.get("destinations")
    if not isinstance(destinations, list):
        fail("manifest destinations must be an array")
        ok = False
        destinations = []

    if data.get("status") == "verified":
        if not any(isinstance(d, dict) and d.get("verified") is True for d in destinations):
            fail("verified checkpoint requires at least one verified destination")
            ok = False

    serialized = json.dumps(data, sort_keys=True)
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(serialized):
            fail(f"possible credential detected in manifest ({label})")
            ok = False

    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path, help="Path to CONTEXT_CLEAR.md")
    parser.add_argument("--manifest", type=Path, help="Path to context-clear.json")
    args = parser.parse_args()

    if not args.markdown.is_file():
        fail(f"markdown file not found: {args.markdown}")
        return 2

    markdown_ok, digest = validate_markdown(args.markdown)
    manifest_ok = True

    if args.manifest is not None:
        if not args.manifest.is_file():
            fail(f"manifest file not found: {args.manifest}")
            return 2
        manifest_ok = validate_manifest(args.manifest, digest)

    if markdown_ok and manifest_ok:
        print(f"PASS: context-clear bundle structure valid; sha256={digest}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
