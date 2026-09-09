#!/usr/bin/env python3
"""Deterministic CI checks for repository agent-context hygiene.

This is deliberately conservative: it validates discoverability, instruction
ancestry, and reference integrity without pretending it can prove architectural
truth. The semantic repo-context-hardening skill does that part.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

INSTRUCTION_FILES = {"AGENTS.md", "AGENT.md", "CLAUDE.md"}
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


def rel(path: Path, repo_root: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def find_git_root(target: Path) -> Path | None:
    current = target.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def path_chain(repo_root: Path, target: Path) -> list[Path]:
    repo_root = repo_root.resolve()
    target = target.resolve()
    try:
        relative = target.relative_to(repo_root)
    except ValueError:
        return [target]

    chain = [repo_root]
    current = repo_root
    for part in relative.parts:
        current = current / part
        chain.append(current)
    return chain


def instruction_channels_at(directory: Path) -> list[Path]:
    found: list[Path] = []
    for name in ROOT_INSTRUCTION_CANDIDATES:
        path = directory / name
        if path.is_file():
            found.append(path)
    cursor_rules = directory / ".cursor" / "rules"
    if cursor_rules.is_dir() and any(cursor_rules.iterdir()):
        found.append(cursor_rules)
    return found


def applicable_instruction_channels(repo_root: Path, target: Path) -> list[Path]:
    found: list[Path] = []
    for directory in path_chain(repo_root, target):
        found.extend(instruction_channels_at(directory))
    return found


def check_scope(target: Path, repo_root: Path | None, findings: list[Finding]) -> Path:
    if repo_root is None:
        findings.append(
            Finding(
                "warning",
                "GIT_ROOT_UNKNOWN",
                "No .git boundary was found in the target or its ancestors; treating the target as the workspace root.",
            )
        )
        return target

    if target != repo_root:
        findings.append(
            Finding(
                "notice",
                "NESTED_TARGET",
                f"Target is nested inside repository root: {rel(target, repo_root)}",
            )
        )
    return repo_root


def check_instruction_presence(repo_root: Path, target: Path, findings: list[Finding]) -> list[Path]:
    found = applicable_instruction_channels(repo_root, target)
    if not found:
        findings.append(
            Finding(
                "error",
                "NO_APPLICABLE_AGENT_CONTEXT",
                "No applicable agent instruction channel found from repository/workspace root to target (AGENTS.md, CLAUDE.md, copilot instructions, .clinerules, or .cursor/rules).",
            )
        )
        return []

    findings.append(
        Finding(
            "notice",
            "CONTEXT_ANCESTRY",
            "Applicable instruction channel(s), outermost to innermost: "
            + " -> ".join(rel(p, repo_root) for p in found),
        )
    )
    return found


def instruction_files_to_check(repo_root: Path, target: Path, applicable: list[Path]) -> list[Path]:
    files: set[Path] = {p for p in applicable if p.is_file()}
    for path in walk_files(target, names=INSTRUCTION_FILES):
        files.add(path)
    return sorted(files)


def check_instruction_sizes(repo_root: Path, target: Path, applicable: list[Path], findings: list[Finding]) -> None:
    for path in instruction_files_to_check(repo_root, target, applicable):
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError as exc:
            findings.append(Finding("warning", "READ_FAILED", str(exc), rel(path, repo_root)))
            continue

        is_repo_root = path.parent == repo_root
        advisory = 150 if is_repo_root else 60
        if len(lines) > advisory:
            findings.append(
                Finding(
                    "warning",
                    "CONTEXT_SIZE",
                    f"{len(lines)} lines; advisory target is <= {advisory}. Split only if local scope would become clearer.",
                    rel(path, repo_root),
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


def resolves_local_reference(doc: Path, token: str, repo_root: Path) -> bool:
    p = Path(token)
    candidates: list[Path] = []

    if token.startswith(("./", "../")):
        candidates.append((doc.parent / p).resolve())
    else:
        # Agent docs commonly use either file-relative or repository-root-relative
        # paths. Accept either rather than inventing one universal convention.
        candidates.extend(((doc.parent / p).resolve(), (repo_root / p).resolve()))

    repo_root_resolved = repo_root.resolve()
    for candidate in candidates:
        try:
            candidate.relative_to(repo_root_resolved)
        except ValueError:
            continue
        if candidate.exists():
            return True
    return False


def docs_to_check(repo_root: Path, target: Path, applicable: list[Path]) -> list[Path]:
    docs: set[Path] = {p for p in applicable if p.is_file()}
    docs.update(walk_files(target, names=INSTRUCTION_FILES))

    root_readme = repo_root / "README.md"
    if root_readme.is_file():
        docs.add(root_readme)

    docs_dir = repo_root / "docs"
    if docs_dir.is_dir():
        docs.update(walk_files(docs_dir, suffix=".md"))

    return sorted(docs)


def check_doc_references(repo_root: Path, target: Path, applicable: list[Path], findings: list[Finding]) -> None:
    for doc in docs_to_check(repo_root, target, applicable):
        text = doc.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()

        candidates: list[tuple[str, int, str]] = []
        for lineno, line in enumerate(lines, 1):
            for match in MD_LINK_RE.finditer(line):
                local_target = normalize_markdown_target(match.group(1))
                if local_target:
                    candidates.append((local_target, lineno, "markdown-link"))
            for match in BACKTICK_PATH_RE.finditer(line):
                local_target = match.group(1)
                if likely_local_path(local_target):
                    candidates.append((local_target, lineno, "backtick-path"))

        for local_target, lineno, kind in candidates:
            if resolves_local_reference(doc, local_target, repo_root):
                continue
            level = "error" if kind == "markdown-link" else "warning"
            findings.append(
                Finding(
                    level,
                    "BROKEN_DOC_REFERENCE",
                    f"Referenced local path does not exist from document or repository root: {local_target}",
                    rel(doc, repo_root),
                    lineno,
                )
            )


def check_nested_context(repo_root: Path, target: Path, applicable: list[Path], findings: list[Finding]) -> None:
    applicable_files = {p for p in applicable if p.is_file()}
    nested = [
        path
        for path in walk_files(target, names=INSTRUCTION_FILES)
        if path not in applicable_files
    ]
    if nested:
        findings.append(
            Finding(
                "notice",
                "DESCENDANT_CONTEXT",
                f"Found {len(nested)} deeper instruction file(s) below target: "
                + ", ".join(rel(p, repo_root) for p in sorted(nested)[:12])
                + (" …" if len(nested) > 12 else ""),
            )
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Target repository/workspace path to lint")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--json", dest="json_path", help="Write machine-readable report")
    args = parser.parse_args()

    target = Path(args.root).expanduser().resolve()
    if not target.exists() or not target.is_dir():
        print(f"::error::ROOT_MISSING: target path does not exist: {target}")
        return 2

    findings: list[Finding] = []
    discovered_git_root = find_git_root(target)
    repo_root = check_scope(target, discovered_git_root, findings)
    applicable = check_instruction_presence(repo_root, target, findings)
    check_instruction_sizes(repo_root, target, applicable, findings)
    check_nested_context(repo_root, target, applicable, findings)
    check_doc_references(repo_root, target, applicable, findings)

    for finding in findings:
        emit(finding)

    report = {
        "target": str(target),
        "repository_root": str(repo_root),
        "strict": args.strict,
        "applicable_instruction_channels": [rel(p, repo_root) for p in applicable],
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
