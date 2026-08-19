---
schema: agents-md/v1
project: agent-skills
initiative: agent-infra
family: swarm-research
what: >-
  Justin's own library of Claude Code skill packages — two dozen skill
  directories grouped into squads covering Apple/iOS design and review, reseller
  operations, gamification and behavioral loops, codebase intelligence, product
  strategy, plus imported vendored squads (seo-geo, content-factory,
  interactive-tools, web-quality, marketing). Each skill is a directory with a
  SKILL.md and supporting files, consumed through ~/.claude/skills.
status: active
updated: 2026-08-19 08:50 UTC
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
- `agent-skills` — Justin's own skills (this repo) + imported vendored squads
- `alireza-claude-skills` — upstream OSS fork (alirezarezvani/claude-skills, 5,200+ stars). Imported into `marketing/` (44) and `product-team/` (13) 2026-08-19. Engineering/finance squads were NOT imported (k8s/terraform/SaaS-metrics — not his stack).
- Source clones (`~/01_Infrastructure/claude-skills`, `~/Projects/skill-research/`, `~/06_Research_Swarm/alireza-claude-skills`) are vendored references, re-clonable from upstream. agent-skills is the working library.

## Imported squads (2026-08-19)
- `seo-geo/` — 15 skills from rampstackco/claude-skills (AEO/GEO/llms.txt, keyword, onpage, technical, programmatic, audits)
- `content-factory/` — 11 skills (content strategy/repurposing/distribution, landing-page copy, ads creative, email)
- `interactive-tools/` — 3 skills (comparison-tool, calculator, quiz/assessment design)
- `web-quality/` — 8 skills (code-review-web, qa-testing, performance-optimization, security-baseline, backup/DR, after-action-report, incident-response, monitoring)
- `marketing/` — 44 skills from alirezarezvani marketing squad (SEO, CRO, content, paid-ads, social, app-store, email, pricing)
- `product-team/` — 13 skills from alirezarezvani product-team squad (product-strategist, experiment-designer, competitive-teardown, product-discovery, ux-researcher-designer, roadmap-communicator, product-analytics, product-manager-toolkit, spec-to-repo, saas-scaffolder, landing-page-generator, ui-design-system, product-skills)
- `ios-readiness/apple-hig-expert/` — Apple HIG design/accessibility compliance skill (references/, scripts/hig_checker.py, templates/)

## Thin-skill consolidation (2026-08-19)
- 24 thin (~450-byte) prompt-template skills removed from `product-strategy/` and `ios-readiness/`:
  - 10 replaced by OSS equivalents in `product-team/` (A/B design, OKR/KPI, roadmap comms, competitor teardown, user research, HIG design/accessibility)
  - 14 retired unused (meeting-to-task-converter, post-mortem-skeleton, qa-test-generator, risk-register-builder, security-compliance-scanner, cost-effort-estimator, pricing-packaging-strategy-advisor, timeline-critical-path-planner, feature-launch-plan-generator, launch-readiness-checklist, demo-script-generator, user-journey-validator, data-privacy-impact-assessment, sprint-story-planner)
- Kept: 4 thin ios-readiness auditors (`ios-code-quality-auditor`, `ios-privacy-auditor`, `ios-shipping-checklist`, `ios-shipping-orchestrator`) — encode distinct Apple-specific knowledge (privacy manifests, Info.plist, code quality, shipping) not covered by apple-hig-expert. `ios-shipping-orchestrator` now routes design/accessibility to `apple-hig-expert`.
- `product-strategy/product-strategy-master` rewritten to route to `product-team/` skills.

## Usage
Skills are consumed by Claude Code via `~/.claude/skills/` or agent-board skill routing.
Check agent-board AGENTS.md for how skills are dispatched.

## Maintenance
- Add new skills as squad subdirectories
- Sync with local Claude Code skills periodically
- Do not conflate with alireza-claude-skills (OSS) without verifying intent
- Imported squads carry upstream provenance; upstream updates are manual re-imports
