#!/usr/bin/env python3
"""Conservative, deterministic PR path risk classification.

This is a routing signal, NOT a bug finder, security scan, or merge approval.
Repository-specific policy may only escalate risk; it cannot downgrade the floor.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
from pathlib import Path
from typing import Any

LEVELS = {"low": 0, "medium": 1, "high": 2}
HIGH_PREFIXES = (
    ".github/workflows/", "deploy/", "deployment/", "infra/",
    "infrastructure/", "terraform/", "migrations/", "publish/",
    "publisher/", "auth/", "authentication/", "secrets/", "payments/",
    "billing/", "security/",
)
HIGH_BASENAMES = {
    "AGENTS.md", "CODEOWNERS", "Dockerfile", "docker-compose.yml",
    "docker-compose.yaml", ".env", ".env.production",
}
HIGH_COMPONENTS = {
    "auth", "authentication", "secrets", "credentials", "permissions",
    "payments", "billing", "publisher", "publish", "deploy", "migrations",
    "migration", "security", "terraform",
}
CODE_SUFFIXES = {
    ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".go",
    ".rs", ".sh", ".bash", ".sql", ".rb", ".java", ".php",
    ".yaml", ".yml", ".json", ".toml", ".ini", ".cfg",
}
DOC_SUFFIXES = {".md", ".mdx", ".rst", ".txt", ".adoc"}
POLICY_KEYS = {"additional_high", "additional_medium"}


def load_policy(path: Path | None) -> dict[str, list[str]]:
    if path is None or not path.is_file():
        return {"additional_high": [], "additional_medium": []}
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or set(raw) - POLICY_KEYS:
        raise ValueError("Policy must be an object with only additional_high/additional_medium")
    result: dict[str, list[str]] = {}
    for key in ("additional_high", "additional_medium"):
        patterns = raw.get(key, [])
        if not isinstance(patterns, list) or any(
            not isinstance(p, str) or not p.strip() for p in patterns
        ):
            raise ValueError(f"{key} must be an array of nonempty glob strings")
        result[key] = patterns
    return result


def classify_one(filename: str, policy: dict[str, list[str]]) -> tuple[str, str]:
    if not filename or filename.startswith("/") or "\\" in filename or ".." in filename.split("/"):
        raise ValueError(f"Invalid repository-relative path: {filename!r}")
    path = filename.lstrip("./")
    basename = path.rsplit("/", 1)[-1]
    parts = path.split("/")
    if path == ".github/pr-risk-policy.json":
        return "high", "review policy itself"
    if any(fnmatch.fnmatchcase(path, p) for p in policy["additional_high"]):
        return "high", "repository-specific protected path"
    if (
        basename in HIGH_BASENAMES
        or path.startswith(HIGH_PREFIXES)
        or (len(parts) > 1 and parts[0] == ".github" and basename == "CODEOWNERS")
    ):
        return "high", "protected release/control-plane path"
    if path.startswith(("docs/", "documentation/", "tests/", "test/")) and Path(path).suffix.lower() in DOC_SUFFIXES:
        return "low", "documentation or test prose"
    if any(part.lower() in HIGH_COMPONENTS for part in parts[:-1]):
        return "high", "sensitive execution surface"
    if any(fnmatch.fnmatchcase(path, p) for p in policy["additional_medium"]):
        return "medium", "repository-specific elevated path"
    if path.startswith(".github/"):
        return "medium", "repository automation/metadata"
    if Path(path).suffix.lower() in CODE_SUFFIXES:
        return "medium", "executable code or configuration"
    return "low", "non-executable content"


def classify_files(files: list[str], policy: dict[str, list[str]]) -> dict[str, Any]:
    if not files:
        raise ValueError("No changed files received; refusing to classify an incomplete diff")
    entries = []
    for filename in sorted(set(files)):
        tier, reason = classify_one(filename, policy)
        entries.append({"path": filename, "risk": tier, "reason": reason})
    highest = max(entries, key=lambda item: LEVELS[item["risk"]])["risk"]
    return {
        "schema_version": "pr-risk-v1",
        "tier": highest,
        "changed_files": len(entries),
        "operator_review_recommended": highest == "high",
        "note": "Path-based triage only. Not a code review, security scan, or authorization.",
        "files": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", type=Path, required=True, help="NDJSON from GitHub pull-files API")
    parser.add_argument("--policy", type=Path, default=None)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    try:
        policy = load_policy(args.policy)
        raw_lines = args.files.read_text(encoding="utf-8").splitlines()
        filenames: list[str] = []
        for line in raw_lines:
            if not line.strip():
                continue
            obj = json.loads(line)
            if not isinstance(obj, dict) or not isinstance(obj.get("filename"), str):
                raise ValueError("GitHub files API input must be NDJSON with filename")
            filenames.append(obj["filename"])
        report = classify_files(filenames, policy)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"::error::Risk classification unavailable: {exc}")
        return 2
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    rows = [
        "## Standard PR risk classification",
        f"**Risk: {report['tier'].upper()}** — {report['changed_files']} changed paths.",
        "",
        "**This is path triage, not AI review or merge authorization.**",
        "High-risk changes need explicit operator consideration; rely on branch protection or an independent check to enforce this.",
        "",
        "| Changed path | Tier | Reason |",
        "| --- | --- | --- |",
    ]
    for item in report["files"][:100]:
        safe = item["path"].replace("|", "\\|").replace("`", "\\`").replace("\n", " ")
        rows.append(f"| `{safe}` | {item['risk']} | {item['reason']} |")
    if len(report["files"]) > 100:
        rows.append(f"\nPlus {len(report['files']) - 100} paths in the JSON artifact.")
    args.summary.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"PR_RISK={report['tier'].upper()} FILES={report['changed_files']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
