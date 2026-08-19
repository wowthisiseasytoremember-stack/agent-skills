---
name: project-xray
description: Use when analyzing an unfamiliar codebase, auditing project health, identifying technical debt or critical issues, determining next steps, or generating documentation for an existing project.
---

# Project X-Ray

## Overview

Systematic codebase analysis that produces a **health report**, **issue inventory**, **documentation**, and **prioritized next steps** — all saved as files inside the project being analyzed.

**Core principle:** Read structure before reading code. Map the skeleton, then examine organs. Write every output to disk — never just print to chat.

---

## Output Directory — Create First

**Before running any phase**, create the `.xray/` directory at the project root:

```bash
mkdir -p .xray
# Unhide folder for visibility in file explorer
# Windows:
attrib -h .xray
# macOS:
chflags nohidden .xray
```

**All outputs are written to `.xray/` inside the analyzed project (visible by default):**

| File | Contains |
|---|---|
| `.xray/structure-map.md` | Full directory tree with annotations |
| `.xray/health-report.json` | Health scores per dimension |
| `.xray/issues.json` | Issue inventory (P0–P3) |
| `.xray/next-steps.json` | Prioritized action list |
| `.xray/fixes.json` | Concrete fix commands per P0/P1 issue |
| `.xray/report.md` | Human-readable master summary |

If the project already has a `.xray/` folder, **overwrite all files** — this is a fresh scan.

---

## Phase 0 — Anchor (Always First)

Before anything else, resolve three questions:

| Question | Where to look |
|---|---|
| What type of project is this? | Root config files |
| What's the entry point? | package.json main/scripts, Makefile, Cargo.toml, build.gradle |
| What's the test/build story? | test/, spec/, CI config (.github/, .circleci/) |

```bash
ls -la
cat package.json 2>/dev/null || cat Cargo.toml || cat build.gradle || cat pyproject.toml
cat README.md 2>/dev/null | head -60
```

---

## Phase 1 — Structure Map → `.xray/structure-map.md`

Generate a full annotated directory tree. **Write it to `.xray/structure-map.md`.**

```bash
find . -not -path '*/node_modules/*' -not -path '*/.git/*' \
       -not -path '*/.xray/*' | sort | head -200
```

**Collect and annotate:**
- Every top-level folder with a one-line purpose description
- Language breakdown (count by file extension)
- Total file count, dependency count, test:src ratio

**Format:**
```markdown
# Structure Map
_Analyzed: 2026-02-25 · 142 files · TypeScript · Express_

## Directory Tree
```
project-root/
  src/              ← application code (controllers, services, models)
  src/controllers/  ← 8 files — route handlers
  src/services/     ← 12 files — business logic
  tests/            ← 6 files (test:src ratio: 0.21 ⚠️ low)
  docs/             ← empty
  .github/          ← CI workflows present
```

## Metrics
| Metric | Value |
|---|---|
| Total files | 142 |
| Source files | 58 |
| Test files | 12 |
| Test:src ratio | 0.21 |
| Dependencies | 34 direct, 8 dev |
| Languages | TypeScript (94%), JSON (4%), Shell (2%) |
```

---

## Phase 2 — Health Scoring → `.xray/health-report.json`

Score each dimension 0–10. Weight by impact. **Write to `.xray/health-report.json`.**

| Dimension | Weight | Signals |
|---|---|---|
| **Test Coverage Signal** | 25% | test:src ratio, presence of test config, CI badge |
| **Dependency Health** | 20% | outdated deps, known vulns, dep count vs size |
| **Code Organization** | 20% | folder structure clarity, naming consistency, separation of concerns |
| **Documentation** | 15% | README quality, inline comments, changelog |
| **Security Posture** | 10% | .env files committed, hardcoded secrets, CORS policy |
| **Build/CI Health** | 10% | CI config present, build scripts complete |

**Overall = Σ(score × weight)**

| Score | Label |
|---|---|
| 8–10 | Healthy |
| 6–7.9 | Stable |
| 4–5.9 | Needs Work |
| 0–3.9 | Critical |

**Schema:**
```json
{
  "overall_score": 6.2,
  "label": "Stable",
  "dimensions": {
    "test_coverage":    { "score": 4, "weight": 0.25, "evidence": "test:src ratio 0.21" },
    "dependency_health":{ "score": 7, "weight": 0.20, "evidence": "34 deps, lock file present" },
    "code_organization":{ "score": 7, "weight": 0.20, "evidence": "clear folder separation" },
    "documentation":    { "score": 5, "weight": 0.15, "evidence": "README exists, no API docs" },
    "security_posture": { "score": 8, "weight": 0.10, "evidence": "no committed secrets found" },
    "build_ci_health":  { "score": 6, "weight": 0.10, "evidence": "CI present, no coverage gate" }
  },
  "analyzed_at": "2026-02-25T10:00:00Z"
}
```

---

## Phase 3 — Issue Detection → `.xray/issues.json`

Scan in priority order. **Write to `.xray/issues.json`.**

### P0 — Blockers
- Committed secrets / credentials
- Missing entry point or broken imports
- No dependency lock file

### P1 — Critical Debt
- Zero test coverage
- God files (>500 lines, multiple responsibilities)
- Circular dependencies
- Hardcoded environment-specific values

### P2 — Quality Gaps
- No error handling at API boundaries
- Inconsistent naming conventions
- Dead code / unused exports
- TODO/FIXME density > 1 per 100 lines

### P3 — Hygiene
- No .gitignore or incomplete
- Inconsistent formatting
- Missing type annotations in typed projects
- Stale or missing CHANGELOG

**Schema:**
```json
[
  {
    "id": "ISSUE-001",
    "severity": "P1",
    "category": "test_coverage",
    "description": "No test files found in src/services/",
    "affected_paths": ["src/services/"],
    "line": null
  }
]
```

---

## Phase 4 — Fix Suggestions → `.xray/fixes.json`

For every P0 and P1 issue, generate one concrete fix. **Write to `.xray/fixes.json`.**

**Rules:**
- One fix per issue (reference `ISSUE-xxx` id)
- Include the exact runnable command when possible
- Include a prevention step, not just remediation
- Never suggest deleting files without explaining impact

**Schema:**
```json
[
  {
    "issue_id": "ISSUE-001",
    "severity": "P1",
    "immediate": "Install vitest and add a test for the highest-traffic service",
    "command": "npm install --save-dev vitest && npx vitest init",
    "prevention": "Add coverage threshold to CI: vitest run --coverage --threshold=60"
  }
]
```

---

## Phase 5 — Documentation Generation

Generate only what is missing. Write to the standard locations in the project (not inside `.xray/`).

| Missing | Write to |
|---|---|
| No README | `README.md` at project root |
| No API docs | `docs/api.md` |
| No CHANGELOG | `CHANGELOG.md` at project root |

**README template:**
```markdown
# Project Name

## What it does
[One paragraph]

## Setup
[Commands to install and run]

## Architecture
[Module/folder map — copy from .xray/structure-map.md]

## Testing
[How to run tests]
```

Record which docs were generated in `.xray/report.md` (see Phase 6).

---

## Phase 6 — Master Report → `.xray/report.md`

After all phases, write a human-readable summary to **`.xray/report.md`**.

```markdown
# Project X-Ray Report
_Project: [name] · Analyzed: [date] · Score: [X]/10 ([label])_

## Health Summary
[One paragraph with overall score and top 2 concerns]

## Critical Issues (P0–P1)
[Bulleted list from issues.json, P0 and P1 only]

## Next Steps (Top 5)
[Numbered list from next-steps.json]

## Files Written
- .xray/structure-map.md
- .xray/health-report.json
- .xray/issues.json
- .xray/fixes.json
- .xray/next-steps.json
- [any generated docs, e.g. README.md]
```

---

## Next Steps → `.xray/next-steps.json`

After scoring and issues are complete, produce a prioritized action list ranked by `impact/effort`.

```json
[
  { "priority": 1, "action": "Rotate exposed API key in .env", "effort": "low", "impact": "critical", "issue_ref": "ISSUE-001" },
  { "priority": 2, "action": "Add test coverage for billing service", "effort": "medium", "impact": "high", "issue_ref": "ISSUE-003" }
]
```

---

## Execution Checklist

Run in order. Do not skip. Write each file to disk before moving to the next phase.

- [ ] Create `.xray/` directory at project root
- [ ] Unhide folder: `attrib -h .xray` (Windows) or `chflags nohidden .xray` (macOS)
- [ ] Phase 0: Identify project type and entry point
- [ ] Phase 1: Write `.xray/structure-map.md`
- [ ] Phase 2: Write `.xray/health-report.json`
- [ ] Phase 3: Write `.xray/issues.json`
- [ ] Phase 4: Write `.xray/fixes.json`
- [ ] Phase 4: Write `.xray/next-steps.json`
- [ ] Phase 5: Write any missing docs to project root
- [ ] Phase 6: Write `.xray/report.md`
- [ ] Confirm all files written — list them to the user

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Printing findings to chat instead of writing files | Every output goes to `.xray/` — no exceptions |
| Reading all source files before mapping structure | Always Phase 0 + 1 first |
| Scoring without evidence | Every score needs a cited signal in the `evidence` field |
| Vague fixes ("improve error handling") | Fixes must include exact command or code snippet |
| Generating docs that duplicate existing content | Check what exists before generating |
| Treating all issues as equal | P0 before P1 before P2 before P3 — always |
| Forgetting `.xray/report.md` | This is the human entry point — always write it last |
