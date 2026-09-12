#!/usr/bin/env python3
"""Reject post-apply context-lint findings that were not present pre-apply.

Finding identity intentionally ignores line numbers so harmless documentation
line shifts do not turn an unchanged issue into a regression. All other finding
fields are compared, preserving severity/code/message/path distinctions.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


IGNORED_FINDING_KEYS = {"line", "lineno", "line_number"}


def load_report(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"::error::unable to read lint report {path}: {exc}") from exc

    findings = data.get("findings")
    if not isinstance(findings, list):
        raise SystemExit(f"::error::lint report has no findings list: {path}")
    if any(not isinstance(item, dict) for item in findings):
        raise SystemExit(f"::error::lint report findings must be objects: {path}")
    return data


def freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return tuple(sorted((key, freeze(item)) for key, item in value.items()))
    if isinstance(value, list):
        return tuple(freeze(item) for item in value)
    return value


def finding_identity(finding: dict[str, Any]) -> tuple[tuple[str, Any], ...]:
    return tuple(
        sorted(
            (key, freeze(value))
            for key, value in finding.items()
            if key not in IGNORED_FINDING_KEYS
        )
    )


def format_finding(finding: dict[str, Any]) -> str:
    level = finding.get("level", "unknown")
    code = finding.get("code", "UNKNOWN")
    path = finding.get("path") or finding.get("file") or "<repo>"
    message = finding.get("message", "")
    return f"{level}:{code}:{path}: {message}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reject new context-lint findings after a canary apply, ignoring line-number-only movement."
    )
    parser.add_argument("pre_report", type=Path)
    parser.add_argument("post_report", type=Path)
    args = parser.parse_args()

    pre = load_report(args.pre_report)
    post = load_report(args.post_report)

    pre_findings = pre["findings"]
    post_findings = post["findings"]
    pre_counts = Counter(finding_identity(item) for item in pre_findings)
    post_counts = Counter(finding_identity(item) for item in post_findings)

    regressions = post_counts - pre_counts
    if not regressions:
        print("lint finding-set gate: no new findings")
        return 0

    by_identity = {finding_identity(item): item for item in post_findings}
    print(f"::error::lint finding-set regressed with {sum(regressions.values())} new finding(s)")
    for identity, count in sorted(regressions.items(), key=lambda item: repr(item[0])):
        finding = by_identity[identity]
        for _ in range(count):
            print(f"::error::{format_finding(finding)}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
