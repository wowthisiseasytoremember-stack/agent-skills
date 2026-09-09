---
name: repo-context-hardening
description: >
  Discover how a repository actually works, identify context future coding agents
  would otherwise rediscover mid-task, and harden the repository's instruction
  files, AGENTS.md, READMEs, architecture docs, runbooks, comments, invariants,
  protected-change boundaries, and source-of-truth maps. Use for repository
  onboarding, documentation repair, stale-context cleanup, or when agents keep
  misunderstanding a codebase.
---

# Repository Context Hardening

## Mission

Make the repository teach a zero-memory coding agent how to work in it safely.

Success means a cold agent can enter from the workspace root, repository root, or a nested directory and quickly determine:

- where it is;
- which instructions apply;
- where implementation truth lives;
- what state is canonical versus derived;
- what it may modify;
- what it must not modify without explicit operator approval;
- which commands and tests are correct;
- which documents are current;
- and where to start for the requested task.

Optimize for **minimum rediscovery cost**, not documentation volume.

Treat ambiguous ownership, hidden approval gates, unmarked generated files, misleading historical docs, and predictable agent traps as repository defects.

---

# BEFORE ANYTHING ELSE — Scope Gate

Do not inspect or edit implementation until all of these are answered:

1. What is the current working directory?
2. What is the target path?
3. What is the nearest Git repository root?
4. Is there a workspace/monorepo root above or below it?
5. Are there nested `.git` boundaries?
6. Which instruction/orientation files exist from the highest relevant workspace level down to the target?
7. Which of those files actually apply to the target path?
8. Which instruction mechanism does the expected coding tool actually load?

Inspect applicable context files such as:

```text
AGENTS.md
AGENT.md
CLAUDE.md
README*
CONTRIBUTING*
DEVELOPING*
.github/copilot-instructions.md
.cursor/rules/
.clinerules
docs/
.handoff/
```

Do not assume the current directory is the repository root.

Do not assume the nearest README is authoritative.

Do not assume `AGENTS.md` is the only instruction channel. If the expected agent tool loads another file natively, either make that file canonical or make it point clearly to the canonical instructions.

If multiple independent repositories exist under the invocation path, model them separately.

---

# Sizing Gate

Right-size the pass before deep reconnaissance.

## SMALL

One package or subsystem; roughly fewer than 30 meaningful source files.

- Do the reconnaissance yourself.
- Usually one root instruction file is enough.
- Do not create architecture/runbook/decision files unless the repo genuinely needs them.
- Avoid worker dispatch unless one area is unusually dense.

## MEDIUM

Several subsystems; roughly 30–200 meaningful source files.

- Read entry points and high-risk paths yourself.
- Delegate bounded reconnaissance for the rest.
- Create nested instructions only where local rules materially differ.

## LARGE

Many subsystems; roughly 200+ meaningful source files or a monorepo.

- Use parallel bounded reconnaissance heavily.
- Keep cross-subsystem synthesis in the orchestrator.
- Do not try to read the entire repository serially before forming the model.

These numbers are guidance, not law. Repository complexity matters more than raw file count.

---

# Doctrine

## Evidence before prose

Do not begin by rewriting documentation.

Establish present behavior from evidence first.

Default authority order:

1. executable tests and observed behavior;
2. active implementation;
3. schemas, contracts, and configuration;
4. CI/CD and operational scripts;
5. persisted/runtime evidence;
6. maintained current documentation;
7. comments;
8. historical plans and handoffs;
9. filenames and assumptions.

Contradictions must be investigated, not silently normalized.

## Current truth must be distinguishable from history

Plans, milestone notes, handoffs, old architecture documents, experiment reports, and archived branches are evidence of past intent or behavior. They are not automatically current instructions.

Clearly distinguish:

- CURRENT
- PLANNED
- DEPRECATED
- EXPERIMENTAL
- HISTORICAL
- UNKNOWN

## Assume the next agent is dumb

Do not rely on the next agent to infer a safety rule.

If an uninformed agent could reasonably edit the wrong file, bypass an approval gate, mutate derived state, deploy from the wrong path, confuse a plan with implementation, or overwrite evidence, make the rule explicit before the point of danger.

## Workers gather evidence; the orchestrator decides truth

Delegated workers do not get to declare repository-wide authority.

The orchestrator owns:

- canonical-source decisions;
- ownership boundaries;
- conflict resolution;
- architecture synthesis;
- protection classification;
- documentation placement;
- final validation.

## UNKNOWN is better than invented certainty

Use `UNKNOWN` whenever evidence is incomplete.

Never write documentation that sounds more certain than the repository evidence supports.

---

# 1. Recon

Build topology before reading deeply.

Identify:

- entry points;
- major packages/subsystems;
- manifests and workspace boundaries;
- tests;
- configuration;
- schemas/models/contracts;
- persistence/state stores;
- scripts/tools;
- CI/deployment;
- generated outputs;
- adapters/integrations;
- operator/control-plane surfaces;
- documentation and historical material.

Trace the paths that matter, not every file.

For important workflows, follow:

```text
entry
→ validation
→ transformation
→ canonical/persisted state
→ generated/derived state
→ downstream consumer
→ completion evidence
```

---

# Bounded Worker Reconnaissance

Use cheap limited-context workers aggressively when available, including YOLO-auto workers via MCP.

The rule is:

> Dispatch bounded read-only workers with exact paths and an evidence-only contract. The orchestrator synthesizes.

Worker rules:

- Give each worker one coherent subsystem, execution path, or roughly 10–30 meaningful files.
- Prefer semantic boundaries over arbitrary alphabetical chunks.
- Workers are read-only unless the operator explicitly asks otherwise.
- Workers report `CONFIRMED`, `LIKELY`, `UNKNOWN`, or `CONFLICTING`.
- Workers never declare repository-global truth.
- If a directory is large, split it across several workers rather than sending one worker the whole folder.

Good:

```text
Worker A: src/cli/ + src/config/
Question: How does execution enter the system and how is runtime config resolved?

Worker B: src/state/ + src/models/
Question: What state is persisted, canonical, projected, or generated?

Worker C: src/rendering/ + src/assets/
Question: Trace input assets to generated outputs and identify do-not-edit boundaries.

Worker D: src/publishing/ + src/adapters/
Question: Identify external side effects, evidence, retries, and operator gates.
```

Bad:

```text
Read src/ and tell me how the repository works.
```

Use this worker contract:

```text
You are a bounded repository reconnaissance worker.

SCOPE:
<exact paths>

DO NOT edit files.
DO NOT inspect unrelated areas unless needed to resolve a direct reference.
Your job is evidence collection, not global architecture.

Report:
1. Files inspected.
2. What this scope owns.
3. Entry points.
4. Inputs and outputs.
5. Important dependencies.
6. Canonical/persisted state encountered.
7. Generated/derived state encountered.
8. Invariants enforced by implementation or tests.
9. Operator/manual approval gates.
10. Dangerous-to-modify surfaces.
11. Relevant commands/tests.
12. Documentation conflicts.
13. Facts future agents would otherwise rediscover.
14. Unresolved questions.
15. Evidence paths for important claims.

Classify findings as CONFIRMED / LIKELY / UNKNOWN / CONFLICTING.
Use UNKNOWN instead of guessing.
```

If no workers are available, apply the same slicing to yourself. Work slice by slice and stop tracing once the questions for that slice are answered.

---

# 2. Model

Before editing docs, build the factual repository model.

## Repository map

Explain responsibilities, not just directory names.

## Ownership

For important components identify:

```text
OWNS
READS
WRITES
DERIVES
MUST NOT OWN
```

Explicitly document negative ownership where agents are likely to blur boundaries.

Example:

```text
Rendering owns media generation.

It does NOT own:
- editorial approval;
- canonical story identity;
- publication success.

Do not add those responsibilities here.
```

## Sources of truth

Use one consistent table:

| Concern | Canonical (owner) | Derived | Mutation rule | Never infer from |
|---|---|---|---|---|

If two artifacts represent the same state, determine which wins.

## Lifecycles

Document state transitions only when they matter.

For each important transition identify:

- trigger;
- owner;
- preconditions;
- persisted evidence;
- failure state;
- operator approval requirement.

Explicitly record non-equivalences where applicable:

```text
SHIP ≠ rendered
rendered ≠ publishable
scheduled ≠ published
file exists ≠ canonical
draft exists ≠ approved
```

## Invariants

Find non-obvious rules future agents could violate.

Prefer rules supported by tests, schemas, runtime validation, or CI.

Critical invariants that exist only as prose should be candidates for enforcement.

---

# 3. Protect

Build a protected-surface inventory.

Use these classifications:

```text
SAFE TO MODIFY
CAUTION
GENERATED — DO NOT EDIT DIRECTLY
OPERATOR APPROVAL REQUIRED
SECURITY / SECRET BOUNDARY
PRODUCTION-CRITICAL
HISTORICAL / READ-ONLY
EXTERNAL-SYSTEM OWNED
UNKNOWN — INVESTIGATE BEFORE MODIFYING
```

Do not use vague wording such as “be careful.”

Use explicit rules.

Example:

```text
OPERATOR APPROVAL REQUIRED

Do not change editorial SHIP/SKIP decisions, publication destinations,
campaign routing, canonical creative IDs, or other operator-owned product
decisions unless the operator explicitly requests that change.
```

For generated surfaces record:

```text
path
canonical upstream source
generator
regeneration command
whether manual edits are overwritten
```

For dangerous commands identify commands that can:

- publish externally;
- deploy;
- mutate production data;
- delete persistent state;
- rewrite migrations;
- send messages;
- change external integrations;
- rotate credentials;
- overwrite canonical evidence.

Critical safety rules may be repeated briefly in both root and local instruction files when missing them could cause external or destructive side effects.

---

# Operator Decisions Are Not Cleanup

Never “fix” an operator-owned decision because it looks inconsistent.

Typical approval-gated concerns include:

```text
SHIP / SKIP
publication destinations
creative identity
content approval
campaign routing
production rollout
destructive data cleanup
canonical taxonomy changes
security policy
external-account changes
```

Report inconsistencies. Do not normalize them away.

---

# Behavioral Bugs Found During Discovery

If discovery uncovers a product or behavioral defect:

- `audit` mode: report it; do not fix it.
- `apply` mode: report it separately; do not fix it unless implementation repair was explicitly requested.

Fixing behavior while reconstructing documentation changes the system being documented and can invalidate the evidence model.

Small tests or checks that encode an already-confirmed invariant are acceptable when they do not change product behavior.

---

# 4. Harden

Repair only the context defects supported by the model.

Classify findings as:

```text
MISSING
STALE
MISPLACED
DUPLICATED
AMBIGUOUS
UNSCOPED
UNPROTECTED
UNVERIFIED
HISTORICAL-AS-CURRENT
OVERDOCUMENTED
UNENFORCED
```

For each important fact ask:

> Where must the next agent encounter this before making the relevant mistake?

Use proximity:

```text
global operating rule        → root instruction file
subsystem-specific rule      → nested instruction file
architecture concept         → architecture/context doc
operational procedure        → runbook
API/interface contract       → docstring/interface docs
counterintuitive local why   → code comment
automatable invariant        → test/schema/CI/preflight
```

Do not solve every problem with another Markdown file.

---

# Root Instruction File

Keep the primary root agent instruction file compact; target roughly ≤150 lines when practical.

Include only applicable sections:

- Mission — always.
- Before You Edit Anything — always.
- Repository Map — always.
- Start Here — always.
- Canonical Sources — when multiple representations/state stores exist.
- Protected Surfaces — whenever any exist.
- Non-obvious Invariants — when applicable.
- Commands — always; verified or explicitly labeled unverified.
- Validation Matrix — when multiple test/check paths exist.
- Known Agent Traps — whenever any exist.
- Documentation Map — when deeper docs exist.
- Keeping This Current — normally include.

Recommended refresh note:

```text
## Keeping This Current

After significant refactors, new subsystems, ownership changes, deployment
changes, or workflow changes, re-run repo-context-hardening in refresh mode.
```

---

# Nested Instructions

Create nested instruction files only when a subtree has real local rules.

Target roughly ≤60 lines when practical.

A nested file should contain only what agents working in that subtree need:

- scope;
- responsibility;
- what it does NOT own;
- start-here files;
- canonical state;
- protected surfaces;
- generated outputs;
- operator gates;
- local tests/commands;
- upstream/downstream contracts;
- local traps.

Do not copy the root file into every directory.

---

# Deeper Documentation

Create `docs/REPOSITORY_CONTEXT.md` only when the root instruction file would otherwise become overloaded or the repo has enough architecture/state complexity to justify it.

Possible deeper docs, only when applicable:

```text
docs/REPOSITORY_CONTEXT.md
docs/architecture.md
docs/runbooks/
docs/decisions/
```

Do not create empty ceremonial sections.

Historical files that remain useful should be labeled clearly and point to current guidance.

---

# Known Agent Traps

This format is mandatory when a predictable wrong inference exists:

```text
TRAP:
`output/status.json` looks canonical.

REALITY:
It is regenerated from `state/events.sqlite`.

RULE:
Never modify `output/status.json` directly.

START HERE:
`src/state/projector.py`
```

This is one of the highest-value outputs of the entire pass.

---

# Reviewability

Before `apply`-mode edits:

- inspect Git status;
- preserve unrelated existing changes;
- do not reset, overwrite, or clean operator work;
- keep hardening changes reviewable as one coherent changeset where practical;
- never mix unrelated product-code changes into the documentation-hardening pass.

---

# Command and Path Verification

Check every new or modified path reference.

Verify safe commands where practical:

```text
--help
build
test
lint
format
preflight
development startup
documentation checks
```

Do not execute destructive or externally side-effecting commands merely to prove they exist.

Label those:

```text
NOT EXECUTED — external/destructive side effects
```

Never copy a command from old documentation and present it as verified without checking it.

---

# Prefer Enforcement Over Warnings

When a critical rule can be enforced cheaply, prefer:

```text
schema
unit test
integration test
lint rule
CI assertion
preflight
type system
repository consistency check
```

Documentation should explain the rule; automation should protect it.

Do not turn the hardening pass into an unrelated engineering project. If enforcement is substantial, recommend it rather than implementing it.

---

# 5. Verify

Validate from the perspective of a cold agent.

Test from 2–3 realistic entry points when applicable:

```text
workspace root
repository root
major subsystem
deep package directory
```

Give the simulated agent 2–3 representative real tasks.

It must be able to answer:

1. Where am I?
2. Which instructions apply?
3. Where do I start?
4. What is canonical?
5. What is generated or derived?
6. What must not be changed without approval?
7. Which tests/checks apply?
8. Which docs are current?
9. What does this subsystem own and not own?
10. Can I begin without reconstructing half the repository?

If a reasonable cold agent would fail one of the safety-critical questions, keep hardening.

---

# Quality Gate

## Hard gate — all applicable items must pass

- Cold agent can identify the correct repository/workspace root.
- Applicable instruction files and scope are clear.
- Canonical state is identified where state ambiguity exists.
- Protected surfaces are explicitly marked.
- Commands are verified or labeled unverified.
- No stale/historical document presents itself as current truth.
- Operator-approval surfaces are named.
- Generated files are labeled when they exist.

## Soft gate — pass when applicable

- Ownership boundaries are explicit.
- State lifecycles are documented.
- Validation matrix exists.
- Known traps are documented.
- Historical material is classified.
- Important invariants are automatically enforced or enforcement is recommended.

`N/A` is valid.

---

# Stop Condition

If the repository already satisfies the quality gate:

- do not manufacture documentation work;
- make only genuine path/link/minor clarity fixes if needed;
- report what was verified;
- return `STRONG` or `ADEQUATE`;
- creating no new files is a valid successful result.

---

# Minimum Viable Pass

If context or time becomes constrained, preserve this floor in order:

1. Root instruction file is accurate: mission, map, start-here paths, protected surfaces, verified commands, known traps.
2. Generated files are clearly labeled.
3. Operator-approval surfaces are named.
4. Canonical state is identified where ambiguity exists.
5. Remaining uncertainty is recorded as `UNKNOWN`.

The floor prevents most mid-task agent disasters. Everything beyond it is incremental.

---

# Output

Keep the final report compact. Do not force empty sections.

Produce:

## 1. Scope

```text
invocation path
target path
workspace root
repository root
nested repository boundaries
applicable instruction ancestry
```

## 2. Repository Model

Include only useful pieces:

- repository map;
- source-of-truth table;
- protected surfaces;
- important ownership/lifecycles/invariants.

## 3. Changes

For each changed document:

```text
CREATED
UPDATED
SUPERSEDED
ARCHIVED
REMOVED
UNCHANGED BUT VERIFIED
```

State why.

## 4. Rediscovery Risks Fixed

Use:

```text
BEFORE:
<what a future agent had to rediscover>

AFTER:
<where the truth is now documented and/or enforced>
```

## 5. Unknowns + Verdict

Record unresolved uncertainty.

Verdict:

- `STRONG` — cold agents should orient quickly with low rediscovery risk.
- `ADEQUATE` — workable; minor non-critical context remains implicit.
- `WEAK` — important architecture or ownership still requires code archaeology.
- `UNSAFE` — documentation misrepresents behavior or dangerous boundaries remain ambiguous.

Also report validation performed and any commands intentionally not executed because of side effects.

---

# Final Standard

The pass is complete only when this is defensible:

> A future agent can enter the relevant part of this repository with no conversation history, determine what context applies, understand local architecture and ownership, identify authoritative state, know what it must not change without explicit operator approval, find the correct commands and tests, and begin useful work without reconstructing the same repository knowledge from scratch.
