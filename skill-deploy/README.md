# Portable Skill Deployment

`agent-skills` is the canonical source. `skill-deploy/skillctl.py` validates a managed skill, copies the exact bundle into local agent skill directories, packages it deterministically, and publishes immutable versions to the OpenAI Skills API.

Only skills explicitly listed in `registry.json` are deployable. This is deliberate: the repository contains imported/vendored skills that must never be bulk-published accidentally.

## Managed targets

- **Codex local:** `${CODEX_SKILLS_DIR}` when set, otherwise `${CODEX_HOME:-~/.codex}/skills`.
- **Claude Code local:** `${CLAUDE_SKILLS_DIR}` when set, otherwise `~/.claude/skills`.
- **Server/custom agent:** use `--dest /path/to/skills-root` with either local target selector.
- **OpenAI cloud:** the Skills API. First publish creates the skill; later publishes create immutable versions. The returned non-secret `skill_id` is written back to `registry.json` unless `--no-write-registry` is used.

Local deployment uses a staged copy, atomic replace, and SHA-256 tree fingerprint verification. It does not silently merge files into an installed skill.

## Normal workflow

From the repository root:

```bash
python skill-deploy/skillctl.py validate context-clear
python skill-deploy/skillctl.py deploy context-clear --dry-run
python skill-deploy/skillctl.py deploy context-clear --local-only
```

After `OPENAI_API_KEY` is available and the current OpenAI Python SDK is installed:

```bash
python -m pip install -U openai
python skill-deploy/skillctl.py publish context-clear --dry-run
python skill-deploy/skillctl.py publish context-clear
```

One-command local + cloud deployment:

```bash
python skill-deploy/skillctl.py deploy context-clear
```

The default cloud behavior promotes the new immutable version to the skill's default. Use `--no-default` when creating a cloud version that should not become active yet.

## Useful commands

```bash
# Validate every explicitly managed skill.
python skill-deploy/skillctl.py validate --all

# Compare the canonical source fingerprint with local installs.
python skill-deploy/skillctl.py status context-clear

# Sync only Codex.
python skill-deploy/skillctl.py sync context-clear --target codex

# Sync to a server/custom skills root.
python skill-deploy/skillctl.py sync context-clear --target codex --dest /srv/agent-skills

# Build a deterministic transport archive without publishing it.
python skill-deploy/skillctl.py package context-clear
```

## Adding another skill

1. Keep the skill itself in its normal canonical directory.
2. Ensure `SKILL.md` has top-level `name` and `description` frontmatter.
3. Add one explicit entry to `registry.json` with its path and targets.
4. Run `validate`, then `deploy --dry-run`.
5. Deploy locally and/or publish to cloud.

A registry entry intentionally starts with `"skill_id": null`. The first successful cloud publish records the returned ID. Later publishes use that ID to create immutable versions instead of creating duplicate cloud skills.

## Safety contract

Deployment stops before writing when validation fails. The validator checks the canonical path, required skill metadata, name consistency, and common credential patterns. Local writes are staged and verified. Cloud publishing requires `OPENAI_API_KEY` and imports the OpenAI SDK only when the cloud path is actually used, so local-only operation has no third-party Python dependency.

`--dry-run` performs validation and computes the exact local/cloud plan without making writes or network calls.
