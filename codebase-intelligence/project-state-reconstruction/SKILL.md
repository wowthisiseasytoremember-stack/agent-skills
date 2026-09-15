---
name: project-state-reconstruction
description: >
  Reconstruct the current evidence-backed state of a project or multi-repository
  system before deciding, auditing, executing, or handing work to another agent.
  Use when context may be stale or fragmented; when the user says check it,
  audit it, continue this, what next, search everything, hand this off, or do it;
  when multiple repos/files/connectors may disagree; or when repository
  boundaries do not match real system boundaries. Distinguishes intended,
  implemented, integrated, validated, operational, canonical, experimental,
  stale, and unknown state; maps cross-system dependencies; and limits retrieval
  to the minimum evidence needed for a defensible answer or action.
---

# Project State Reconstruction

## Mission

Reconstruct **what is actually true now** before making consequential project decisions.

This skill is not a generic search routine and not a documentation summarizer. It is an evidence-routing, contradiction-resolution, system-boundary, and execution-readiness discipline.

Use it to answer questions such as:

- What is the current state of this project?
- Did that change actually ship?
- Which branch/worktree/PR is current?
- Is this plan implemented, merged, tested, deployed, or merely proposed?
- What does this repository depend on outside itself?
- Which other projects feed, govern, consume, import, mount, index, or share state with this one?
- What should happen next?
- Can another agent safely continue from here?

Success means the answer survives inspection by a skeptical operator without relying on stale memory, filenames, or unverified summaries.

---

# Core Principle

> **Repository boundary != system boundary. Document name != authority. Plan != implementation. Implementation != integration. Integration != validation. Validation != operation.**

Do not collapse these states.

---

# When To Invoke

Invoke this skill when one or more of these are true:

- the user asks to **check**, **audit**, **reconstruct**, **continue**, **resume**, **red team**, **search everything**, **hand off**, **do it**, or decide **what next**;
- prior conversation context may be stale relative to repositories or runtime state;
- multiple branches/worktrees/PRs exist;
- a project spans multiple repositories or connected systems;
- a canonical/current/source-of-truth document may be stale;
- a candidate or experiment may be confused with the production implementation;
- one repository imports, mounts, shells into, or hardcodes paths from another;
- shared credentials, databases, storage, runtime ports, queues, stream keys, or services create coupling;
- the answer could cause destructive, external, production, merge, deployment, or handoff actions.

Do **not** invoke the full workflow for a trivial lookup where one authoritative source is already known and current.

---

# Operating Modes

Infer a mode from the request. Do not make the user choose terminology.

| User intent | Mode | Required result |
|---|---|---|
| “check it” | `VERIFY` | current state + verdict + evidence |
| “what’s the state?” | `RECONSTRUCT` | state snapshot + unresolved gaps |
| “audit it” | `AUDIT` | state + ranked gaps + safe fixes where allowed |
| “red team it” | `RED_TEAM` | weakest assumptions + defensible floor |
| “what next?” | `DECIDE` | highest-ROE next action from reconstructed state |
| “continue/resume this” | `RESUME` | recover active line + continuation point |
| “search everything” | `EXHAUSTIVE` | coverage of all materially relevant available lanes |
| “handoff to another agent” | `HANDOFF` | execution-grade state packet |
| “do it” | `EXECUTE` | minimum sufficient reconstruction, then act and validate |

Mode changes retrieval depth, not evidence standards.

---

# Evidence Depth

Right-size the pass.

## Level 1 — Lightweight

Use for navigation or low-stakes lookup.

Example: “Where did we put the current renderer?”

Requirements:
- search the likely authoritative lane;
- verify the target exists;
- answer without ecosystem-wide reconstruction.

## Level 2 — Decision Grade

Use for prioritization, architecture, merge decisions, or “what next?”

Requirements:
- reconstruct relevant intended/actual state;
- inspect active branches/PRs/issues when materially relevant;
- identify contradictions and blockers;
- map external dependencies that could change the decision.

## Level 3 — Execution Grade

Use before destructive, production, deployment, merge, deletion, credential, external-side-effect, or lower-powered-agent handoff work.

Verify as applicable:
- repository and project identity;
- active branch/worktree/PR;
- canonical implementation path;
- dependencies and shared state;
- approval/operator decisions;
- validation gates;
- rollback or reversibility;
- required evidence the executor must leave behind.

Do not hand an execution agent a summary that has not reached execution-grade confidence.

---

# State Model

For each important capability or change, keep these states distinct:

```text
INTENDED      — plan/spec/approved direction says it should exist
IMPLEMENTED   — code/config/data artifact exists
INTEGRATED    — connected to the real active path / merged / wired in
VALIDATED     — tests/probes/evidence demonstrate required behavior
OPERATIONAL   — running/serving/used in the real environment now
```

A useful report may therefore say:

```text
Intended:     yes
Implemented:  yes
Integrated:   yes
Validated:    partial
Operational:  unknown
```

Never translate this into “done.”

---

# Artifact Classification

Classify encountered artifacts when relevant:

```text
CANONICAL
APPROVED BUT NOT IMPLEMENTED
IMPLEMENTED / UNVERIFIED
PRODUCTION
EXPERIMENTAL
DRAFT
STALE
SUPERSEDED
DEPRECATED
HISTORICAL
GENERATED / DERIVED
UNKNOWN
```

A filename containing `CANONICAL`, `CURRENT`, `STATE`, `SOURCE_OF_TRUTH`, `MASTER`, or similar wording gives **zero automatic authority**.

A state document can become stale within the same branch if later commits supersede it.

---

# Authority Is Question-Specific

There is no single universal source hierarchy. Choose the authoritative lane for the claim.

Default guidance:

| Question | Strong evidence |
|---|---|
| Does code exist? | current code / repository tree |
| What code is integrated? | active branch/PR/merge graph/config |
| What is running? | runtime/deployment/service evidence |
| Did it pass? | current test/build/probe output |
| What was intended? | approved plan/spec/operator directive |
| What is assigned? | canonical issue/project tracker |
| What recently changed? | commits/PRs + recent operational notes |
| What decision was made? | operator directive / accepted decision record |
| What is scheduled? | scheduler/calendar/cron/runtime config |
| What was attempted historically? | git history / handoffs / logs |

Rules:

> More recent does not automatically mean more authoritative.

> More authoritative does not automatically mean more current.

> Runtime reality beats a README for runtime-state questions.

> Code beats a plan for implementation-state questions.

> An operator-approved product decision is not invalidated by aesthetically cleaner code or documentation.

---

# Mandatory Ecosystem Discovery Pass

This is the major extension beyond ordinary repository inspection.

Before assuming the target project is self-contained, ask:

> **What other systems supply, consume, govern, import, mount, index, publish, validate, share credentials with, share storage with, or execute this project?**

Run the ecosystem pass whenever any evidence suggests the repository boundary may not equal the system boundary.

Search for:

- Git submodules and nested Git repositories;
- sibling repositories referenced by absolute or relative filesystem path;
- imports or `sys.path` manipulation into another repo;
- copied/reused scripts or shared libraries;
- API clients and local service URLs;
- shared SQLite/Postgres/Redis databases;
- shared mounted storage, media roots, or object stores;
- shared OAuth, API tokens, stream keys, service accounts, or config files;
- common queues, cron jobs, schedulers, or supervisors;
- one project producing artifacts consumed by another;
- one project writing into another project’s filesystem namespace;
- a control-plane repo configuring or governing another runtime;
- duplicated implementations of the same capability;
- mutual-exclusion relationships such as two publishers owning one ingest key;
- parent repo pins that lag active submodule development;
- downstream analytics/reporting systems;
- system-of-record catalogs/indexers that span projects.

Do not assume these relationships are symmetrical.

---

# Ecosystem Edge Types

When mapping a multi-project system, classify important edges using precise relationship types rather than generic “depends on.”

Recommended vocabulary:

```text
OWNS
CONTAINS
SUBMODULE_OF
PINNED_TO
STALE_PIN
IMPORTS_FROM
READS_FROM
WRITES_TO
PRODUCES_FOR
CONSUMES
CONFIGURES
GOVERNS
VALIDATES
MONITORS
INDEXES
PUBLISHES_TO
SHARES_CREDENTIAL
SHARES_STORAGE
SHARES_DATABASE
SHARES_RUNTIME
DUPLICATES_CAPABILITY
MUTUALLY_EXCLUSIVE_WITH
SUPERSEDES
BACKBURNER_CLIENT_OF
```

Also distinguish four identities where necessary:

```text
filesystem owner
producer
consumer
canonical code owner
```

They may be different systems.

---

# Wave 1 — Broad but Bounded Reconstruction

Use one logical first wave across every materially relevant authoritative lane.

Do not search every available source blindly. Search enough to fill the required answer slots.

Typical lanes:

- active repository code/config;
- branches/worktrees/PRs;
- issues/project tracking;
- canonical plans/contracts/operator directives;
- runtime/deployment evidence;
- connected files/docs;
- external systems only when they materially govern the project;
- ecosystem neighbors discovered by references.

For large systems, parallelize bounded read-only reconnaissance when possible.

Each worker or slice should report evidence, not global truth.

---

# Merge the Evidence

After Wave 1, build an internal state table:

```text
VERIFIED
INFERRED
REPORTED BUT NOT VERIFIED
CONTRADICTED
STALE
UNKNOWN
```

Do not paper over contradictions.

For important claims, track:

```text
claim
source
source authority for this claim type
recency
conflict status
state classification
```

---

# Contradiction Resolution

When sources conflict, resolve deliberately.

Use, in order appropriate to the claim:

1. direct runtime or executable evidence;
2. active implementation/configuration;
3. accepted operator decision;
4. current integration/merge state;
5. maintained contracts/specifications;
6. current documentation;
7. historical plans/handoffs.

Example:

```text
README: detector enabled
runtime config: detector disabled
later operator decision: detector intentionally disabled for v0.9
```

Resolution:

```text
CURRENT: detector disabled
README: stale
operator debt acceptance: still active
```

Never silently choose the source that makes the story cleaner.

---

# Wave 2 — Consequential Gap Resolution Only

After merging Wave 1, identify only gaps that could change:

- the verdict;
- the next action;
- the handoff;
- a destructive/external action;
- production safety;
- system-boundary interpretation.

Search again only for those gaps.

Then stop.

Default maximum: **two logical retrieval waves**.

Do not keep collecting corroborating evidence once the answer is already decision-safe.

---

# Negative Evidence

> **Absence of retrieval is not evidence of absence.**

Allowed:

> “I did not find `X` after searching the current repository paths, symbols, and relevant history.”

Not allowed without adequate scope:

> “`X` does not exist.”

To make a negative claim, search the authoritative lane that could establish absence.

If the scope cannot establish it, report `UNKNOWN` or `NOT FOUND IN SEARCHED SCOPE`.

---

# Latest / Current Protection

Do not equate:

```text
latest retrieved item
latest timestamp in one document
latest default-branch commit
latest search result
```

with:

```text
actual current project state
```

For “latest/current/now” questions inspect the integration surface appropriate to the system:

- active branches/PRs;
- deployment/runtime state;
- currently pinned submodules;
- current operator priority docs;
- newest accepted decision;
- latest validated artifact.

Default branch alone is often insufficient.

---

# Candidate / Experiment Protection

A candidate may be:

- proposed;
- benchmarked;
- counterfactually evaluated;
- implemented only in analysis code;
- implemented on a branch;
- integrated into the production-candidate path;
- production deployed.

These are different states.

Mandatory rule:

> **Evaluation of a candidate does not make the candidate implemented. Inspect the real production code path.**

Similarly:

> **A PR body is status evidence, not implementation evidence.**

Inspect changed code/config when the distinction matters.

---

# Canonicality Rules

An artifact is canonical only when evidence establishes its authority.

Possible signals:

- explicitly approved by the operator;
- referenced from current instruction/entrypoint files;
- current active branch/deployment points to it;
- accepted PR/merge promoted it;
- current runtime reads it;
- downstream systems depend on it;
- current tests/contracts treat it as authoritative.

Never promote experimental material to canonical because it is newer.

Never demote an accepted operator decision because a newer plan disagrees.

---

# Staleness

Evidence has different volatility.

High-staleness examples:

- branch/worktree state;
- open PR status;
- production deployment;
- service health;
- current assignments;
- test results after code changes;
- submodule pins relative to active development.

Low-staleness examples:

- historical rationale;
- stable architecture principles;
- accepted long-lived product constraints.

Refresh volatile state before consequential decisions.

Do not hardcode universal TTLs unless the project has explicit ones.

---

# Accepted Debt / Operator Overrides

Track accepted imperfections explicitly.

Example:

```yaml
accepted_debt:
  - defect: fullscreen_duplicate
    accepted_for: v0.9
    operator_decision: true
```

Do not repeatedly reopen accepted debt unless:

- conditions changed;
- it blocks a new objective;
- the operator asks to revisit it.

Operator decisions are state, not cleanup opportunities.

---

# Required Answer Slots

Before finalizing a consequential answer, identify the slots the answer must support.

Typical slots:

```text
project/system identity
canonical/active branch or integration line
intended state
implemented state
integrated state
validated state
operational state
known blockers
accepted debt
cross-project dependencies
contradictions
unknowns
highest-ROE next action
```

Do not answer until every material slot is either supported or explicitly `UNKNOWN`.

---

# DECIDE — Highest-ROE Next Action

When asked “what next?”, do not return an unranked backlog.

Prefer actions that:

- unblock many downstream tasks;
- resolve a consequential unknown;
- validate a risky assumption;
- promote a proven candidate to the real path;
- create revenue or production value;
- eliminate recurring rediscovery;
- reduce fragile cross-system coupling;
- create observable, reviewable progress.

Conceptual ranking:

```text
expected value
× unblock factor
× confidence
× reversibility
-----------------
effort × risk
```

Use judgment; do not manufacture fake numeric precision.

---

# AUDIT Mode

Default flow:

```text
inspect
→ establish state
→ identify gaps
→ rank by consequence
→ fix reversible/high-confidence gaps when requested/allowed
→ validate
→ report remaining blockers
```

Do not stop at a defect list when the user asked you to audit and you can safely repair the issue.

Do not modify behavior merely because reconstruction discovered a bug unless the user asked for implementation repair.

---

# EXECUTE Mode

Reconstruct the **minimum sufficient execution-grade state**, then act.

Before externally consequential or destructive work verify:

- target identity;
- active line/version;
- dependencies;
- approval gates;
- rollback path;
- validation criteria.

After acting, validate the result from the authoritative lane.

Do not report success based only on the write/action returning without error when a stronger validation is available.

---

# HANDOFF Mode

A handoff must prevent the next agent from rediscovering resolved state.

Required structure:

```markdown
# Objective

# Verified starting state

# Canonical artifacts / repos

# Branch / worktree / runtime context

# Ecosystem dependencies and shared state

# Decisions already made

# Accepted debt / explicit non-goals

# Exact work to perform

# Validation gates

# Evidence the executor must leave behind

# Stop conditions

# Return packet
```

Rules:

- make the executor’s outputs observable to the supervising agent;
- distinguish verified facts from reported/unverified claims;
- include exact paths/branches/SHAs when relevant;
- do not ask the executor to re-decide architecture already settled;
- define stop conditions before destructive or ambiguous branches;
- lower-powered executors need less ambiguity, not more prose.

---

# State Snapshot Artifacts

Do not create state files automatically for every task.

For large or long-running systems, a snapshot may reduce rediscovery.

Preferred shape:

```yaml
project: example
as_of: 2026-09-14T20:00:00-07:00
status: snapshot
authoritative: false

integration:
  branch: feature/x
  commit: abc123

state:
  intended: true
  implemented: true
  integrated: partial
  validated: partial
  operational: unknown

blockers: []
accepted_debt: []
next_action: ...
evidence: []
```

Critical rule:

> A snapshot accelerates reconstruction. It never replaces source evidence.

If used, mark it explicitly non-authoritative and refresh volatile fields before consequential actions.

---

# Output Contract

For substantial reconstruction, default to a compact answer-first structure:

```markdown
## Verdict

[1–3 sentences]

## Current state

- Intended:
- Implemented:
- Integrated:
- Validated:
- Operational:
- Blocked by:

## Ecosystem dependencies

[only material cross-system edges]

## Material discrepancies

[stale docs, contradictions, stale pins, overlapping ownership]

## Highest-ROE next action

[one recommended action]

## Evidence

[only important citations/paths]
```

For simple questions, collapse the structure.

Do not expose retrieval mechanics unless they help explain a surprising verdict.

---

# Architecture Map Requirements

When the task asks for architecture, do not draw first.

First reconstruct the system, then render the diagram from the evidence model.

The map must distinguish at least:

- source/acquisition systems;
- semantic/contract authority;
- implementation/runtime owner;
- canonical state stores;
- production/control-plane owner;
- downstream consumers;
- distribution/external systems;
- backburner/deprecated clients;
- active vs gated vs planned vs stale relationships.

A useful architecture diagram should show **ownership and edge type**, not merely boxes connected by arrows.

Do not draw conceptual adjacency as if it were an implemented dependency.

---

# Relationship to Other Skills

## repo-context-hardening

`repo-context-hardening` makes a repository legible to future cold agents.

`project-state-reconstruction` determines what is actually true **across repositories, branches, files, runtime surfaces, and neighboring systems now**.

Use both when a project is both hard to understand and actively evolving.

## Specialized repository/domain skills

This skill orchestrates evidence routing. It should call or defer to specialized skills for deep local inspection, implementation, data analysis, or domain-specific work.

It decides **where truth should come from**; it does not duplicate every specialist capability.

---

# Anti-Patterns / Never Do This

Never:

- treat a plan as implementation evidence;
- treat implementation as deployment evidence;
- treat a test claim as validation without seeing current evidence when it matters;
- treat `master`/`main` as the whole project when active branches/PRs exist;
- treat a document named `CANONICAL` as automatically current;
- treat evaluation results as proof the evaluated candidate is wired into production;
- declare something absent without searching its authoritative lane;
- silently promote experimental material to canonical;
- silently normalize contradictions;
- restart accepted/rejected work without changed conditions;
- fix accepted technical debt merely because it looks ugly;
- assume filesystem ownership equals code ownership or producer ownership;
- assume two repos are independent because Git does not link them;
- ignore shared credentials/storage/ports/stream keys as architecture;
- create a custom search/vector/MCP infrastructure layer before native repositories/files/connectors prove insufficient;
- ask the operator for information that can be retrieved from available authoritative sources;
- keep researching after the answer is decision-safe.

---

# Quality Gate

Before finalizing a consequential reconstruction, verify all applicable items:

- [ ] Correct project/system identity established.
- [ ] Authoritative lane chosen for each material claim.
- [ ] Intended/implemented/integrated/validated/operational state separated.
- [ ] Active branches/PRs/worktrees checked when relevant.
- [ ] “Latest/current” claims are not based on retrieval order alone.
- [ ] Canonical/stale/experimental status is evidence-backed.
- [ ] Candidate evaluation is not confused with production implementation.
- [ ] Contradictions are resolved or explicitly left unresolved.
- [ ] Negative claims have adequate search scope.
- [ ] Ecosystem discovery pass was run when repo boundary may differ from system boundary.
- [ ] Shared credentials/storage/databases/runtime resources were considered.
- [ ] Submodules/nested repos/pins were checked when present.
- [ ] Required answer slots are filled or marked `UNKNOWN`.
- [ ] Retrieval stopped after consequential gaps were resolved.
- [ ] Recommended next action follows from the reconstructed state.
- [ ] Execution/handoff guidance is reproducible and observable.

---

# Validation / Evals

Use `evals/scenarios.md` for regression scenarios.

The skill should reliably catch at least:

- wrong initial repository;
- stale default branch;
- stale “canonical” state document;
- evaluated-but-not-implemented candidate;
- branch-only feature incorrectly described as production;
- stale parent submodule pin;
- shared credential/runtime coupling across repos;
- duplicate capability with mutual exclusion;
- domain-data system incorrectly modeled as peer production system;
- semantic authority living in one repo while implementation lives in another;
- downstream consumer that is read-only and gated on upstream truth;
- absence claim made without searching the correct lane.

---

# Final Doctrine

The goal is not to know everything.

The goal is to know **enough of the right things, from the right sources, at the right freshness level, to make the next decision or action defensible**.

When the system is messy, preserve the mess in the model until the evidence justifies simplifying it.
