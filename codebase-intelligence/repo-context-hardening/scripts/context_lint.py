#!/usr/bin/env python3
"""Deterministic CI checks for repository agent-context hygiene.

This is deliberately conservative: it validates discoverability and reference
integrity without pretending it can prove architectural truth. The semantic
repo-context-hardening skill does that part.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

ROOT_INSTRUCTION_CANDIDATES = (
    "AGENTS.md",
    "AGENT.md",
    "CLAUDE.md",
    ".github/copilot-instructions.md",
    ".clinerules",
)

IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "vendor",
    "dist",
    "build",
    ".next",
    ".cache",
    "coverage",
}

MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
BACKTICK_PATH_RE = re.compile(
    r"`((?:\.?\.?/)?(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+(?:\.[A-Za-z0-9_.-]+)?)`"
)


@dataclass
class Finding:
    level: str
    code: str
    message: str
    path: str | None = None
    line: int | None = None


def emit(finding: Finding) -> None:
    command = "error" if finding.level == "error" else "warning" if finding.level == "warning" else "notice"
    attrs = []
    if finding.path:
        attrs.append(f"file={finding.path}")
    if finding.line:
        attrs.append(f"line={finding.line}")
    attr_text = (" " + ",".join(attrs)) if attrs else ""
    print(f"::{command}{attr_text}::{finding.code}: {finding.message}")


def walk_files(root: Path, names: set[str] | None = None, suffix: str | None = None) -> Iterable[Path]:
    if not root.exists():
        return
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        base_path = Path(base)
        for name in files:
            if names is not None and name not in names:
                continue
            if suffix is not None and not name.endswith(suffix):
                continue
            yield base_path / name


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def root_instruction_files(root: Path) -> list[Path]:
    found = []
    for candidate in ROOT_INSTRUCTION_CANDIDATES:
        path = root / candidate
        if path.is_file():
            found.append(path)
    cursor_rules = root / ".cursor" / "rules"
    if cursor_rules.is_dir() and any(cursor_rules.iterdir()):
        found.append(cursor_rules)
    return found


def check_instruction_presence(root: Path, findings: list[Finding]) -> None:
    found = root_instruction_files(root)
    if not found:
        findings.append(
            Finding(
                "error",
                "NO_ROOT_AGENT_CONTEXT",
                "No root agent instruction channel found (AGENTS.md, CLAUDE.md, copilot instructions, .clinerules, or .cursor/rules).",
            )
        )
        return
    findings.append(
        Finding(
            "notice",
            "ROOT_CONTEXT",
            "Root instruction channel(s): " + ", ".join(rel(p, root) for p in found),
        )
    )


def check_instruction_sizes(root: Path, findings: list[Finding]) -> None:
    instruction_names = {"AGENTS.md", "AGENT.md", "CLAUDE.md"}
    for path in walk_files(root, names=instruction_names):
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as exc:
            findings.append(Finding("warning", "READ_FAILED", str(exc), rel(path, root)))
            continue
        is_root = path.parent == root
        advisory = 150 if is_root else 60
        if len(lines) > advisory:
            findings.append(
                Finding(
                    "warning",
                    "CONTEXT_SIZE",
                    f"{len(lines)} lines; advisory target is <= {advisory}. Split only if local scope would become clearer.",
                    rel(path, root),
                )
            )


def normalize_markdown_target(raw: str) -> str | None:
    target = raw.strip().strip("<>")
    if not target or target.startswith("#"):
        return None
    if target.startswith(("http://", "https://", "mailto:", "tel:", "data:")):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    return target or None


def likely_local_path(token: str) -> bool:
    if token.startswith(("http://", "https://", "~", "$", "/")):
        return False
    if any(ch in token for ch in ("*", "{", "}", "<", ">", "|")):
        return False
    first = token.split("/", 1)[0]
    if first in {"npm", "python", "python3", "git", "gh", "cd", "make", "swift", "cargo", "go"}:
        return False
    return "/" in token or "." in Path(token).name


def check_doc_references(root: Path, findings: list[Finding]) -> None:
    doc_names = {"AGENTS.md", "AGENT.md", "CLAUDE.md", "README.md"}
    docs = list(walk_files(root, names=doc_names))
    docs_dir = root / "docs"
    if docs_dir.is_dir():
        docs.extend(walk_files(docs_dir, suffix=".md"))

    seen: set[Path] = set()
    for doc in docs:
        if doc in seen or not doc.is_file():
            continue
        seen.add(doc)
        text = doc.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()

        candidates: list[tuple[str, int, str]] = []
        for lineno, line in enumerate(lines, 1):
            for match in MD_LINK_RE.finditer(line):
                target = normalize_markdown_target(match.group(1))
                if target:
                    candidates.append((target, lineno, "markdown-link"))
            for match in BACKTICK_PATH_RE.finditer(line):
                target = match.group(1)
                if likely_local_path(target):
                    candidates.append((target, lineno, "backtick-path"))

        for target, lineno, kind in candidates:
            p = Path(target)
            resolved = (doc.parent / p).resolve() if target.startswith(("./", "../")) else (root / p).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                continue
            if not resolved.exists():
                level = "error" if kind == "markdown-link" else "warning"
                findings.append(
                    Finding(
                        level,
                        "BROKEN_DOC_REFERENCE",
                        f"Referenced local path does not exist: {target}",
                        rel(doc, root),
                        lineno,
                    )
                )


def check_context_ancestry(root: Path, findings: list[Finding]) -> None:
    nested = []
    for path in walk_files(root, names={"AGENTS.md", "AGENT.md", "CLAUDE.md"}):
        if path.parent != root:
            nested.append(rel(path, root))
    if nested:
        findings.append(
            Finding(
                "notice",
                "NESTED_CONTEXT",
                f"Found {len(nested)} nested instruction file(s): " + ", ".join(sorted(nested)[:12]) + (" …" if len(nested) > 12 else ""),
            )
        )


def check_git_boundary(root: Path, findings: list[Finding]) -> None:
    if not (root / ".git").exists():
        findings.append(
            Finding(
                "warning",
                "ROOT_NOT_GIT",
                "Selected root does not contain .git; confirm CI target_path is the intended repository/workspace boundary.",
            )
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repository/workspace root to lint")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--json", dest="json_path", help="Write machine-readable report")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"::error::ROOT_MISSING: target root does not exist: {root}")
        return 2

    findings: list[Finding] = []
    check_git_boundary(root, findings)
    check_instruction_presence(root, findings)
    check_instruction_sizes(root, findings)
    check_context_ancestry(root, findings)
    check_doc_references(root, findings)

    for finding in findings:
        emit(finding)

    report = {
        "root": str(root),
        "strict": args.strict,
        "counts": {
            "error": sum(f.level == "error" for f in findings),
            "warning": sum(f.level == "warning" for f in findings),
            "notice": sum(f.level == "notice" for f in findings),
        },
        "findings": [asdict(f) for f in findings],
    }

    if args.json_path:
        out = Path(args.json_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    errors = report["counts"]["error"]
    warnings = report["counts"]["warning"]
    print(json.dumps(report["counts"]))
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
