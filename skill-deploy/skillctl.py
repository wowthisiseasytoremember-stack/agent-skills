#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "skill-deploy" / "registry.json"
IGNORED_NAMES = {".git", "__pycache__", ".pytest_cache", ".DS_Store"}
SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


class SkillCtlError(RuntimeError):
    pass


def load_registry(path: Path | None = None) -> dict[str, Any]:
    path = path or REGISTRY_PATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SkillCtlError(f"registry not found: {path}") from exc
    if data.get("schema") != "agent-skills-registry/v1":
        raise SkillCtlError("unsupported registry schema")
    if not isinstance(data.get("skills"), dict):
        raise SkillCtlError("registry.skills must be an object")
    return data


def save_registry(data: dict[str, Any], path: Path | None = None) -> None:
    path = path or REGISTRY_PATH
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def get_entry(registry: dict[str, Any], name: str) -> dict[str, Any]:
    try:
        return registry["skills"][name]
    except KeyError as exc:
        raise SkillCtlError(f"unknown managed skill: {name}") from exc


def skill_path(entry: dict[str, Any]) -> Path:
    path = (ROOT / entry["path"]).resolve()
    if ROOT.resolve() not in path.parents:
        raise SkillCtlError("skill path escapes repository root")
    return path


def iter_files(root: Path):
    for p in sorted(root.rglob("*")):
        if p.is_dir():
            continue
        if any(part in IGNORED_NAMES for part in p.parts):
            continue
        yield p


def fingerprint(root: Path) -> str:
    h = hashlib.sha256()
    for p in iter_files(root):
        rel = p.relative_to(root).as_posix().encode()
        h.update(len(rel).to_bytes(4, "big"))
        h.update(rel)
        payload = p.read_bytes()
        h.update(len(payload).to_bytes(8, "big"))
        h.update(payload)
    return h.hexdigest()


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise SkillCtlError(f"{path}: missing YAML frontmatter")
    block = m.group(1)
    result: dict[str, str] = {}
    for key in ("name", "description"):
        mm = re.search(rf"(?m)^{key}:\s*(.*)$", block)
        if not mm:
            raise SkillCtlError(f"{path}: missing frontmatter field {key}")
        result[key] = mm.group(1).strip()
    return result


def secret_scan(root: Path) -> list[str]:
    findings: list[str] = []
    for p in iter_files(root):
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append(f"{p.relative_to(root)} matches {pattern.pattern}")
    return findings


def validate_skill(name: str, entry: dict[str, Any]) -> dict[str, Any]:
    path = skill_path(entry)
    if not path.is_dir():
        raise SkillCtlError(f"{name}: missing skill directory {path}")
    skill_md = path / "SKILL.md"
    if not skill_md.is_file():
        raise SkillCtlError(f"{name}: missing SKILL.md")
    fm = parse_frontmatter(skill_md)
    declared = fm["name"].strip("\"'")
    if declared != name:
        raise SkillCtlError(f"{name}: SKILL.md declares name {declared!r}")
    findings = secret_scan(path)
    if findings:
        raise SkillCtlError(f"{name}: possible secret material: " + "; ".join(findings))
    return {
        "name": name,
        "path": str(path.relative_to(ROOT)),
        "fingerprint": fingerprint(path),
        "targets": entry.get("targets", []),
    }


def default_target_dir(target: str) -> Path:
    home = Path.home()
    if target == "codex":
        override = os.environ.get("CODEX_SKILLS_DIR")
        if override:
            return Path(override).expanduser()
        codex_home = Path(os.environ.get("CODEX_HOME", home / ".codex")).expanduser()
        return codex_home / "skills"
    if target == "claude":
        return Path(os.environ.get("CLAUDE_SKILLS_DIR", home / ".claude" / "skills")).expanduser()
    raise SkillCtlError(f"unknown local target: {target}")


def atomic_copy_skill(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    temp = Path(tempfile.mkdtemp(prefix=f".{dest.name}.incoming-", dir=dest.parent))
    staged = temp / dest.name
    shutil.copytree(src, staged)
    backup = dest.with_name(dest.name + ".skillctl-backup")
    if backup.exists() or backup.is_symlink():
        if backup.is_dir() and not backup.is_symlink():
            shutil.rmtree(backup)
        else:
            backup.unlink()
    try:
        if dest.exists() or dest.is_symlink():
            os.replace(dest, backup)
        os.replace(staged, dest)
        if backup.exists() or backup.is_symlink():
            if backup.is_dir() and not backup.is_symlink():
                shutil.rmtree(backup)
            else:
                backup.unlink()
    except Exception:
        if (not dest.exists()) and backup.exists():
            os.replace(backup, dest)
        raise
    finally:
        shutil.rmtree(temp, ignore_errors=True)


def sync_local(
    name: str,
    entry: dict[str, Any],
    targets: list[str],
    dry_run: bool = False,
    dest_override: Path | None = None,
) -> list[dict[str, str]]:
    src = skill_path(entry)
    source_fp = fingerprint(src)
    receipts = []
    for target in targets:
        root = dest_override if dest_override is not None else default_target_dir(target)
        dest = root / name
        if dry_run:
            receipts.append(
                {
                    "target": target,
                    "destination": str(dest),
                    "status": "planned",
                    "fingerprint": source_fp,
                }
            )
            continue
        atomic_copy_skill(src, dest)
        copied_fp = fingerprint(dest)
        if copied_fp != source_fp:
            raise SkillCtlError(f"{target}: post-copy fingerprint mismatch")
        receipts.append(
            {
                "target": target,
                "destination": str(dest),
                "status": "synced",
                "fingerprint": copied_fp,
            }
        )
    return receipts


def build_zip(name: str, entry: dict[str, Any], output: Path) -> Path:
    src = skill_path(entry)
    output.parent.mkdir(parents=True, exist_ok=True)
    epoch = (1980, 1, 1, 0, 0, 0)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in iter_files(src):
            rel = p.relative_to(src).as_posix()
            info = zipfile.ZipInfo(rel, date_time=epoch)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, p.read_bytes())
    return output


def cloud_plan(name: str, entry: dict[str, Any]) -> dict[str, Any]:
    cloud = entry.get("cloud", {})
    return {
        "name": name,
        "action": "create-version" if cloud.get("skill_id") else "create-skill",
        "skill_id": cloud.get("skill_id"),
        "source": entry["path"],
        "fingerprint": fingerprint(skill_path(entry)),
    }


def cloud_publish(
    name: str,
    entry: dict[str, Any],
    registry: dict[str, Any],
    make_default: bool = True,
    write_registry: bool = True,
) -> dict[str, Any]:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SkillCtlError("OPENAI_API_KEY is required for cloud publish")
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise SkillCtlError(
            "OpenAI Python SDK is required: python -m pip install -U openai"
        ) from exc

    validate_skill(name, entry)
    with tempfile.TemporaryDirectory(prefix="skillctl-cloud-") as td:
        archive = build_zip(name, entry, Path(td) / f"{name}.zip")
        client = OpenAI()
        cloud = entry.setdefault("cloud", {})
        skill_id = cloud.get("skill_id")
        with archive.open("rb") as fh:
            if skill_id:
                version = client.skills.versions.create(
                    skill_id,
                    files=fh,
                    default=make_default,
                )
                receipt = {
                    "action": "create-version",
                    "skill_id": skill_id,
                    "version": version.version,
                    "default": make_default,
                }
            else:
                skill = client.skills.create(files=fh)
                skill_id = skill.id
                cloud["skill_id"] = skill_id
                receipt = {
                    "action": "create-skill",
                    "skill_id": skill.id,
                    "version": skill.default_version,
                    "default": True,
                }
                if write_registry:
                    save_registry(registry)
        receipt["fingerprint"] = fingerprint(skill_path(entry))
        return receipt


def command_validate(args):
    registry = load_registry()
    names = sorted(registry["skills"]) if args.all else [args.name]
    results = [validate_skill(n, get_entry(registry, n)) for n in names]
    print(json.dumps(results, indent=2))


def command_status(args):
    registry = load_registry()
    entry = get_entry(registry, args.name)
    base = validate_skill(args.name, entry)
    local = {}
    for target in ("codex", "claude"):
        dest = default_target_dir(target) / args.name
        if not dest.is_dir():
            local[target] = {"status": "missing", "destination": str(dest)}
        else:
            dest_fp = fingerprint(dest)
            local[target] = {
                "status": "current" if dest_fp == base["fingerprint"] else "drifted",
                "destination": str(dest),
                "fingerprint": dest_fp,
            }
    print(
        json.dumps(
            {"source": base, "local": local, "cloud": cloud_plan(args.name, entry)},
            indent=2,
        )
    )


def command_sync(args):
    registry = load_registry()
    entry = get_entry(registry, args.name)
    validate_skill(args.name, entry)
    targets = args.target or [
        t for t in entry.get("targets", []) if t in {"codex", "claude"}
    ]
    if not targets:
        raise SkillCtlError("no local targets configured")
    dest = Path(args.dest).expanduser() if args.dest else None
    print(
        json.dumps(
            sync_local(args.name, entry, targets, args.dry_run, dest), indent=2
        )
    )


def command_package(args):
    registry = load_registry()
    entry = get_entry(registry, args.name)
    validate_skill(args.name, entry)
    out = Path(args.output or (ROOT / "dist" / f"{args.name}.zip"))
    build_zip(args.name, entry, out)
    print(
        json.dumps(
            {"archive": str(out), "fingerprint": fingerprint(skill_path(entry))},
            indent=2,
        )
    )


def command_publish(args):
    registry = load_registry()
    entry = get_entry(registry, args.name)
    if args.dry_run:
        print(json.dumps(cloud_plan(args.name, entry), indent=2))
        return
    print(
        json.dumps(
            cloud_publish(
                args.name,
                entry,
                registry,
                not args.no_default,
                not args.no_write_registry,
            ),
            indent=2,
        )
    )


def command_deploy(args):
    registry = load_registry()
    entry = get_entry(registry, args.name)
    validation = validate_skill(args.name, entry)
    receipt: dict[str, Any] = {"validation": validation}

    if not args.cloud_only:
        targets = args.target or [
            t for t in entry.get("targets", []) if t in {"codex", "claude"}
        ]
        if targets:
            dest = Path(args.dest).expanduser() if args.dest else None
            receipt["local"] = sync_local(
                args.name, entry, targets, args.dry_run, dest
            )

    if not args.local_only:
        if args.dry_run:
            receipt["cloud"] = cloud_plan(args.name, entry)
        else:
            receipt["cloud"] = cloud_publish(
                args.name,
                entry,
                registry,
                make_default=not args.no_default,
                write_registry=not args.no_write_registry,
            )
    print(json.dumps(receipt, indent=2))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="skillctl",
        description="Validate, sync, package, and publish canonical Agent Skills.",
    )
    sub = p.add_subparsers(dest="command", required=True)

    v = sub.add_parser("validate")
    g = v.add_mutually_exclusive_group(required=True)
    g.add_argument("name", nargs="?")
    g.add_argument("--all", action="store_true")
    v.set_defaults(func=command_validate)

    s = sub.add_parser("status")
    s.add_argument("name")
    s.set_defaults(func=command_status)

    sy = sub.add_parser("sync")
    sy.add_argument("name")
    sy.add_argument("--target", action="append", choices=["codex", "claude"])
    sy.add_argument("--dest", help="override skills root; mainly for testing or custom agents")
    sy.add_argument("--dry-run", action="store_true")
    sy.set_defaults(func=command_sync)

    pk = sub.add_parser("package")
    pk.add_argument("name")
    pk.add_argument("--output")
    pk.set_defaults(func=command_package)

    pub = sub.add_parser("publish")
    pub.add_argument("name")
    pub.add_argument("--dry-run", action="store_true")
    pub.add_argument("--no-default", action="store_true")
    pub.add_argument("--no-write-registry", action="store_true")
    pub.set_defaults(func=command_publish)

    dep = sub.add_parser("deploy")
    dep.add_argument("name")
    dep.add_argument("--target", action="append", choices=["codex", "claude"])
    dep.add_argument("--dest", help="override skills root for local/server installs")
    dep.add_argument("--dry-run", action="store_true")
    mode = dep.add_mutually_exclusive_group()
    mode.add_argument("--local-only", action="store_true")
    mode.add_argument("--cloud-only", action="store_true")
    dep.add_argument("--no-default", action="store_true")
    dep.add_argument("--no-write-registry", action="store_true")
    dep.set_defaults(func=command_deploy)
    return p


def main(argv=None) -> int:
    try:
        args = parser().parse_args(argv)
        args.func(args)
        return 0
    except SkillCtlError as exc:
        print(f"skillctl: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
