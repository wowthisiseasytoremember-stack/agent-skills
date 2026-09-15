# Project State Reconstruction — Regression Scenarios

These scenarios test whether the skill reconstructs current system state instead of merely summarizing retrieved documents.

Each scenario has a **failure mode**, **evidence**, and **expected behavior**.

---

## 1. Wrong Initial Repository

### Setup

The user names Project A. Historical context associates Project A with a feature. A current reconciliation document or code reference shows the feature actually lives in Project B.

### Expected

- Correct the target repository before deep analysis.
- Explain that Project A is adjacent/consumer/supplier rather than authoritative for the requested capability.
- Continue from Project B without requiring the user to restate the task.

### Fail

- Deeply inspect Project A and give a confident feature-state answer from the wrong repo.

---

## 2. Stale Default Branch

### Setup

`master` is several weeks old. Multiple recent branches and an open PR contain active integration work.

### Expected

- Treat default branch as stable baseline, not total current project state.
- Inspect recent branches/PRs relevant to the capability.
- Report both stable/default and active integration lines.

### Fail

- State that the feature is absent because it is absent from `master`.

---

## 3. “Canonical” File Is Stale

### Setup

`PROJECT_STATE_CANON.md` says evaluation is running. Two later commits on the same branch contain completed evaluation artifacts and updated PR status.

### Expected

Classify:

```text
artifact intent: canonical state record
actual status: stale
superseded by: later direct evidence
```

### Fail

- Give the canonical-named file automatic precedence.

---

## 4. Evaluated Candidate Is Not Implemented

### Setup

An evaluation script defines Candidate B and reports excellent metrics. The real production-candidate implementation still uses Baseline A.

### Expected

Report:

```text
Candidate B: evaluated / promising
Candidate B in production path: no
Baseline A: current implementation
```

### Fail

- Say Candidate B is the current detector/algorithm because its evaluation is newest.

---

## 5. PR Body Overstates Integration

### Setup

A PR description says a new path is wired. The changed code shows only analysis helpers; the production entrypoint is unchanged.

### Expected

- Treat PR body as status/intention evidence.
- Inspect the changed production code path.
- Report actual integration state.

### Fail

- Treat PR prose as implementation proof.

---

## 6. Branch-Only Feature

### Setup

A feature exists on `experiment/new-mode` and passes tests there. It is not merged into the integration branch or default branch.

### Expected

Classify:

```text
implemented: yes
validated on experiment branch: yes
integrated: no
operational: no evidence
```

### Fail

- Report “shipped” or “done.”

---

## 7. Stale Submodule Pin

### Setup

Parent Repo P pins submodule S at commit `111aaa`. Active work in S is at `999zzz`, and downstream discussions assume the newer behavior.

### Expected

- Detect the submodule edge.
- Report `PINNED_TO 111aaa` and `STALE_PIN` relative to active development.
- Explain reproducibility consequence: cloning P cannot reproduce active S state.

### Fail

- Treat current submodule repo head as what Parent P actually references.

---

## 8. Documentation Disagrees With Git Topology

### Setup

`AGENTS.md` says a nested repo is “not a submodule.” `.gitmodules` and the parent Git tree report it as a submodule.

### Expected

- Git topology wins for the topology question.
- Mark documentation stale.

### Fail

- Repeat the documentation claim without checking Git metadata.

---

## 9. Shared Credential Coupling

### Setup

Repo A imports Repo B's config by adding B to `sys.path` and reads B's OAuth file. Both repos can publish to the same external platform.

### Expected

Add architecture edges:

```text
A IMPORTS_FROM B
A SHARES_CREDENTIAL B
```

Evaluate whether shared external-account state creates collision or sequencing constraints.

### Fail

- Map A and B as independent because neither is a Git dependency of the other.

---

## 10. Mutual Exclusion Through External Runtime

### Setup

Two separate programs can both publish to the same live ingest key. Running both concurrently causes failure or undefined behavior.

### Expected

Represent:

```text
Program A MUTUALLY_EXCLUSIVE_WITH Program B
```

The external ingest key/runtime is part of the architecture.

### Fail

- Model both as harmless parallel output paths.

---

## 11. Filesystem Owner != Producer

### Setup

An artifact is written beneath `/data/project-a/...`, but the script that created it lives in Project B.

### Expected

Distinguish:

```text
filesystem namespace: Project A
producer: Project B
canonical code owner: Project B
consumer: possibly Project A
```

### Fail

- Debug Project A because the file path contains Project A's name.

---

## 12. Semantic Authority != Implementation Owner

### Setup

Repo Core defines a graph contract. Repo Engine contains the Python/SQLite implementation. Domain repos supply source data. A production repo consumes the graph read-only.

### Expected

Map separate roles:

```text
Core      GOVERNS / semantic authority
Engine    IMPLEMENTS
Domain A  PRODUCES_FOR Engine
Domain B  PRODUCES_FOR Engine
Prod      READS_FROM graph artifact
```

Do not collapse them into one “graph project.”

### Fail

- Assign implementation ownership to Core solely because it defines the contract.

---

## 13. Read-Only Consumer Is Upstream-Gated

### Setup

A downstream adapter passes fixture tests, but the upstream data artifact still has source-truth defects. The adapter is intentionally draft and read-only.

### Expected

Report:

```text
consumer implementation: implemented
consumer validation: fixture-passing
production promotion: blocked
blocker: upstream truth/release gate
```

### Fail

- Promote the consumer because its local tests are green.

---

## 14. Domain App Is Not Current Product Center

### Setup

A repository contains a rich client app and old app-first roadmap. A current operator directive says active priority is domain database/research data feeding a shared graph and production system; client UI is backburnered.

### Expected

- Current operator directive wins for priority.
- Model domain repo as upstream data supplier.
- Keep client as downstream/backburner.

### Fail

- Draw the client app as a peer production/control-plane system because it has more visible UI code.

---

## 15. Negative Claim Without Correct Search Lane

### Setup

Docs do not mention Feature X. The code repository has not been searched.

### Expected

- Do not conclude X is absent.
- Search the code/config lane first.
- If still incomplete, say `NOT FOUND IN SEARCHED SCOPE`.

### Fail

- “Feature X does not exist.”

---

## 16. Accepted Debt Reopened By Cleanup

### Setup

An operator explicitly accepted defect D for release v0.9. A newer agent sees D in code and calls it a blocker.

### Expected

- Preserve accepted debt state.
- Reopen only if conditions changed or D blocks the current objective.

### Fail

- Spend the next iteration fixing D merely because it is technically imperfect.

---

## 17. “Latest” Search Result Is Historical

### Setup

Search returns a recently indexed document describing an older event. An older-indexed PR has a newer event timestamp/current state.

### Expected

- Compare event/commit/PR timestamps and authority, not retrieval order.
- Report actual current state.

### Fail

- Treat first/latest search result as latest project state.

---

## 18. Ecosystem Architecture Request

### Setup

The user asks for an architecture map of several projects.

Evidence shows:
- domain repos feed a shared research implementation;
- one core repo defines semantics;
- one production repo consumes read-only;
- a utility repo provides shared media;
- a live runtime is a submodule of the production repo;
- distribution is one-way through a scheduler;
- client apps are backburnered.

### Expected

Before drawing:

1. reconstruct ownership;
2. classify edge types;
3. identify active/gated/planned/stale relationships;
4. distinguish semantic authority from implementation owner;
5. distinguish production center from research-truth center;
6. render architecture from that evidence model.

### Fail

- Produce a visually attractive peer-to-peer box diagram based on project names alone.

---

# Scoring

A strong run should satisfy all applicable criteria:

- Correct authoritative lane selected.
- Current state separated from history.
- State ladder preserved.
- Contradictions surfaced and resolved.
- Cross-repository/system edges discovered.
- Gated/planned paths are not drawn as active.
- Negative claims are scoped.
- One defensible next action follows from evidence.

Any run that confidently collapses **planned -> implemented -> operational** should fail the eval even if the final recommendation happens to be correct.
