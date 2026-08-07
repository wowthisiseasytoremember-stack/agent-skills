---
schema: agents-md/v1
project: agent-skills
initiative: agent-infra
family: swarm-research
what: >-
  Justin's own library of Claude Code skill packages — roughly two dozen skill
  directories grouped into squads covering Apple/iOS design and review, reseller
  operations, gamification and behavioral loops, codebase intelligence, and product
  strategy. Each skill is a directory with a SKILL.md and supporting files, consumed
  through ~/.claude/skills. Distinct from the alireza-claude-skills OSS fork.
status: active
updated: 2026-08-07 05:44 UTC
---

# agent-skills — Claude Code Skill Library

**Initiative:** agent-infra
**Status:** Active — synced from local Claude Code skills
**Last sync:** 2026-06-10

## What this is
Repository of Claude Code skills organized by squads (40+ skill packages). These are Justin's own skills, distinct from the alireza-claude-skills OSS fork.

## Structure
Skills are organized into squad directories. Each skill is a directory with a SKILL.md and supporting files.

## Relationship to alireza-claude-skills
- `agent-skills` — Justin's own skills (this repo)
- `alireza-claude-skills` — upstream OSS fork (alirezarezvani/claude-skills, 5,200+ stars)
- Relationship unclear — verify which is source-of-truth before modifying either

## Usage
Skills are consumed by Claude Code via `~/.claude/skills/` or agent-board skill routing.
Check agent-board AGENTS.md for how skills are dispatched.

## Maintenance
- Add new skills as squad subdirectories
- Sync with local Claude Code skills periodically
- Do not conflate with alireza-claude-skills (OSS) without verifying intent
