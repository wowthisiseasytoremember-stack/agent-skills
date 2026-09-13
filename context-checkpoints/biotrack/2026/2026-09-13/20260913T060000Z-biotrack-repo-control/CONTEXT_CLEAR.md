# Context Clear Checkpoint

## Resume in one sentence

Resume by leaving the active BioTrack provenance/data-integrity audit alone, treating the existing draft PRs/jobs as live coordination state, and—when the operator returns to the process-improvement thread—continue from the lightweight universal `repoctl`/GitHub-native coordination design captured below rather than rebuilding a BioTrack-specific control plane.

## Objective and definition of done

**CANONICAL / operator intent:** Improve the product-development/process system across the user's repositories so multiple local and cloud agents can safely understand current state, avoid duplicate or conflicting work, validate exact commits, and hand work off cleanly.

**APPROVED constraint:** Do not overengineer this. The solution must be universal enough to use across the user's repos, but it must stay lightweight and useful for a single operator.

**APPROVED constraint:** The separate BioTrack provenance/data-integrity audit is already owned by another agent. Do not interfere with or duplicate that active audit unless the operator explicitly reassigns a slice.

**Definition of done for the process-improvement thread:** a small portable protocol/tooling layer can be piloted in `agent-skills`, observed working across local and cloud agents, and then rolled out selectively to other repos without requiring a central server, database, mandatory GitHub Actions, or per-repo bespoke orchestration.

## Canonical state

### BioTrack work ownership and milestone boundary

**CANONICAL operator directive:** Another agent owns the current BioTrack provenance/integrity audit. Preserve noninterference.

The audit contract currently requires a blocking **Phase 0 read-only quality spot-check** before remediation. It must scrutinize every field encountered across code/data stores, with extra attention to discovery/expedition/provenance/collection-event metadata. Phase 0 must not normalize, reclassify, or modify data. Remediation threads (Aqua A.1, A.2, A.4; source inventory; Flora provenance reconciliation; expansion) follow only after Phase 0 assignments are understood.

Do not:
- modify the active Aqua/Flora/BioTrack data-audit branches;
- create competing remediation PRs;
- re-dispatch or overwrite mailbox work owned by the audit agent;
- normalize/reclassify canonical biological data;
- merge BioTrackCore PR #16, PR #17, AquaTrack PR #1, or the stacked PR #18 without explicit operator approval;
- spend milestone effort on Swift/Xcode/UI/app packaging unless the operator changes scope.

### Last observed live GitHub state from this conversation

**OBSERVED:** `ichabod-agent-mailbox#83` (`[AQUA-A4-CANONICAL]`) had zero comments on the final poll. It remains the in-flight/pending owner of Aqua A.4 canonical artifact generation.

**OBSERVED:** `ichabod-agent-mailbox#79` still had only the earlier partial read-only measurement comment. That comment explicitly left A.1 violation counts, A.2 default/inference distributions, stale/current artifact diff, Flora runtime timestamp path, and Core reuse classification open.

**OBSERVED:** BioTrackCore PR #16 remained open, draft, unmerged, and the documented resume checkpoint.

**OBSERVED:** BioTrackCore PR #17 remained open, draft, unmerged at head:
`0206f0d5a800af5f025618f68d0486c48bf352a2`
Branch:
`feat/data-contract-v1-20260912`

**OBSERVED:** AquaTrack PR #1 remained open, draft, unmerged at head:
`25e5b2faca17eb4742ea751d801252a2656157f7`
Branch:
`fix/canonical-species-export-20260912`

**OBSERVED:** Hosted GitHub Actions were intentionally non-blocking in this BioTrack milestone because the account had no available Actions minutes; local exact-SHA validation on Ichabod was being treated as authoritative for the data milestone.

## Work completed

### Contract-lineage integrity fix

A non-overlapping Contract v1 validation defect was found without touching the active data audit.

The existing Contract v1 validator rejected a transformation that directly parented itself, but did not reject multi-node transformation cycles such as:

`A -> B -> A`

The same graph-integrity problem could occur in inferred assertion dependencies via `method.input_assertion_ids`.

**OBSERVED change:** Created isolated branch:
`fix/contract-v1-acyclic-lineage-20260912`

It started exactly from PR #17 head:
`0206f0d5a800af5f025618f68d0486c48bf352a2`

**OBSERVED commit:**
`645e0878dd3c697b36087d09213d5fca24873ea2`

Diff relative to PR #17:
- added `tools/validate_contract_v1_lineage.py`;
- added one invocation to `tools/validate_local.sh`;
- 2 files changed;
- +93 lines;
- one commit ahead of PR #17.

**OBSERVED draft PR:** BioTrackCore PR #18:
`fix: reject cyclic Contract v1 provenance lineage`

PR #18 is intentionally stacked on PR #17, not `master`.

Its scope is strictly validation/integrity:
- transformation parent references must resolve and form an acyclic graph;
- assertion inference dependencies must resolve and form an acyclic graph;
- duplicate transformation/assertion IDs in the lineage projection are rejected;
- existing data-only local validation invokes the lineage gate.

No Aqua/Flora scientific data, Phase 0 work, mailbox #79/#83, Swift/Xcode/UI, or app packaging was modified by that PR.

At creation GitHub reported the stacked draft PR as not mergeable. No rebase, retargeting, conflict resolution, or merge attempt was made because merging was out of scope.

### Process-improvement research/design work

The conversation explored a universal repo/process-control system after identifying that the larger recurring problem is not merely missing documentation, but **live coordination state**: who owns what, whether a task is blocked, whether another agent is already modifying the same surface, which exact commit was validated, and whether a PR is stacked/dependent.

An initial BioTrack-specific "control plane" idea was deliberately generalized and simplified into the proposed `repoctl` protocol described below.

The existing `agent-skills` repository was inspected. Relevant existing capabilities:
- `codebase-intelligence/repo-context-hardening/` already hardens static repository context for cold agents;
- `agent-operations/context-clear/` already preserves execution-critical conversation context before clearing;
- `agent-operations/` is therefore a natural home for a future repo coordination skill/protocol.

## Current execution state

### BioTrack

The active data/provenance audit remains externally owned. Treat its scientific/data paths as write-locked unless the operator explicitly reassigns a slice.

PR #18 is a separate stacked validation-only proposal and must not be merged without operator approval.

### Universal repo-control work

No `repoctl` implementation was created in this conversation.

**PROPOSED only:** The design below is a high-confidence plan, but the operator has not approved implementation beyond asking that the unique ideas be preserved before clearing the conversation.

Natural proposed home:
`wowthisiseasytoremember-stack/agent-skills/agent-operations/repo-control/`

The name `repoctl` is a placeholder, not a canonical product name.

## Decisions and constraints

### Core architecture decision

**PROPOSED:** Build a lightweight **GitHub-native protocol + small local CLI + cloud/local agent skill**, not a BioTrack-specific service.

Model:

- GitHub owns durable coordination state: issues, dependencies, sub-issues, PRs, branches, comments, commits.
- `AGENTS.md` remains the human/agent instruction surface.
- `repo-context-hardening` reconstructs and repairs relatively static repository knowledge.
- proposed `repoctl` handles live preflight/claim/collision/validation state.
- `context-clear` preserves chat-only execution state before a conversation is discarded.
- local agents can use `git`/`gh`/filesystem;
- hosted/cloud agents can follow the same protocol through the GitHub connector/API.

There should be **no central runtime server** for V1.

### Do not make live state a committed source of truth

**PROPOSED:** Do not universalize the older `PROJECT_STATE.json` approach as a committed live-state source of truth.

Reason:
- HEAD, active PRs, job state, dirty state, and validation state become stale almost immediately;
- agents then have to decide whether GitHub/Git or the snapshot is newer;
- that recreates the exact ambiguity the system is trying to remove.

Preferred split:

**committed/static**
- `.repoctl.toml`;
- `AGENTS.md`;
- schemas/protocol docs;
- repo-specific validation/protection configuration.

**queried/generated on demand**
- current HEAD;
- current branch;
- dirty state;
- open PRs;
- current issue dependencies;
- live claims;
- validation status.

An explicit state snapshot may still be emitted for an audit/release/checkpoint, but it is an artifact, not the universal live source of truth.

### Small per-repo configuration

**PROPOSED:** Normal repos should need one small optional file:

`.repoctl.toml`

Use TOML so Python 3.11+ can parse it with stdlib `tomllib`; avoid pulling in YAML/parsing dependencies.

Possible configuration categories:
- validation profiles/commands;
- protected paths;
- generated paths + regeneration command;
- named dangerous/shared resources.

Do not duplicate information GitHub/Git can already determine.

### GitHub-native dependencies and hierarchy

**PROPOSED:** Use native GitHub issue dependency/sub-issue relationships where available instead of inventing a second dependency DAG.

Do not create `dependencies.json`.

Suggested hierarchy discipline for a single operator:
- initiative;
- workstream;
- actionable issue.

Avoid deep issue trees even if GitHub supports them.

### Agent claims solve the "same GitHub user" problem

Because many agents may act through the same GitHub account, normal issue assignment is insufficient to express live agent ownership.

**PROPOSED:** Represent a claim as a small machine-readable block in a GitHub issue comment.

Conceptual claim shape:

```json
{
  "schema": "repoctl.claim.v1",
  "claim_id": "<stable id>",
  "agent": "ichabod-aqua-audit",
  "issue": 83,
  "branch": "fix/canonical-species-export-20260912",
  "mode": "write",
  "paths": [
    "data/",
    "scripts/species_export.py"
  ],
  "resources": [
    "aquatrack-canonical-db"
  ],
  "created_at": "<timestamp>",
  "expires_at": "<timestamp>"
}
```

The GitHub comment remains human-readable but is machine-parseable by local or cloud agents.

### Collision semantics deliberately simple

Do not build arbitrary glob/intersection logic.

V1 claim scopes should be only:
- exact repo-relative files;
- repo-relative directory prefixes;
- exact named resources.

Examples:

`data/` conflicts with `data/species.json`.

`docs/` does not conflict with `data/`.

`resource:production-db` conflicts only with the same named resource.

This simplicity is intentional.

### Lease claims

Claims need an expiry so crashed agents cannot permanently lock work.

**PROPOSED default:** 24-hour lease.

An active agent may renew.

Expired claims become stale/reclaimable; no destructive automatic cleanup is required.

### Minimal command surface

The larger brainstorm contained six commands:

- `repoctl init`
- `repoctl doctor`
- `repoctl status`
- `repoctl claim ISSUE`
- `repoctl release ISSUE`
- `repoctl validate`

Do not grow a large command framework before these prove useful.

For implementation sequencing, `doctor` + `status` should come first and be read-only.

### `repoctl doctor` as universal preflight

The most important proposed behavior is a read-only preflight that answers:

- repo/root identity;
- default branch;
- current branch;
- HEAD;
- dirty status;
- current PR;
- requested/current issue;
- native blockers/dependencies;
- active claims/collisions;
- protected/generated surfaces;
- configured validation;
- whether the requested write is currently safe.

Fail-closed principle:

If GitHub dependency/claim state cannot be obtained, report `UNKNOWN`.

For a write operation, `UNKNOWN` must not silently become `SAFE`.

### Work lifecycle

Proposed universal lifecycle:

`DISCOVER -> PREFLIGHT -> CLAIM -> ISOLATE -> WORK -> VALIDATE -> PR -> RELEASE CLAIM`

Expanded:

1. Read applicable `AGENTS.md`/repo instructions.
2. Run/read `repoctl doctor`.
3. Inspect requested issue.
4. Check native GitHub blockers.
5. Check active claims.
6. Claim exact write scope.
7. Create/reuse an isolated branch/worktree when local.
8. Work only inside scope.
9. Validate exact commit.
10. File/update PR with validation evidence and dependencies.
11. Release claim.

### Worktrees are implementation detail, not protocol dependency

**PROPOSED:** Local `repoctl claim ISSUE --worktree` may create/reuse a Git worktree.

But worktrees must stay optional because hosted agents may not have or need the same filesystem model.

Never make the protocol depend on worktrees.

Safety rules:
- never reset the canonical checkout;
- never reuse another active claim's worktree;
- never delete dirty worktrees;
- never force-move branches as cleanup.

### Cloud/local parity

The protocol is the contract, not the Python script.

**Local implementation:** CLI can use `git`, `gh`, and filesystem.

**Hosted/cloud implementation:** skill performs equivalent operations through GitHub APIs/connectors.

Both must produce/read the same claim and validation record semantics.

### Exact validation evidence

Replace vague "tests passed" language with exact evidence tied to a commit.

Conceptual record:

```json
{
  "schema": "repoctl.validation.v1",
  "repository": "owner/repo",
  "commit": "<exact sha>",
  "profile": "full",
  "result": "pass",
  "checks": [
    {
      "name": "contract",
      "command": "python tools/validate_contract_v1.py",
      "exit_code": 0
    }
  ]
}
```

Important invariant:

**tested commit identity matters.**

A PR head changing after validation means old validation evidence no longer proves the new head.

### Separate work status from product maturity

Do not conflate:

**issue/work state**
- OPEN;
- CLAIMED;
- IN PROGRESS;
- BLOCKED;
- READY FOR REVIEW;
- DONE.

with:

**artifact/product maturity**
- SPECIFIED;
- IMPLEMENTED;
- VALIDATED;
- RUNTIME VERIFIED;
- USER VALIDATED;
- RELEASED.

Closing an issue does not itself prove a feature is shipped/released.

### PR metadata should answer four operational questions

Every PR should make these obvious:

1. Issue: what work item does this implement?
2. Scope: what changed?
3. Validation: what exact commit was tested and how?
4. Dependencies: is it stacked on another PR or blocked by another issue?

If the PR base is not the default branch, surface `STACKED PR` automatically.

PR #18 is the motivating example: its base is PR #17's branch, not `master`.

### Account-level templates later

**PROPOSED later:** use a personal-account `.github` repository for default PR/issue templates after the protocol is proven.

Keep templates small:
- PR template;
- bug;
- task;
- investigation.

Do not start with a large template bureaucracy.

### Reusable workflows later

Reusable GitHub workflows may eventually provide optional hosted checks, but they are not the core protocol.

The system must continue to work if Actions are unavailable or intentionally disabled.

### Rulesets/branch protection later

Rulesets/status requirements may be useful after local validation/evidence reporting is mature.

Do not make hosted required checks foundational while hosted CI capacity is unreliable; that can deadlock merges.

### Explicit overengineering exclusions

Do **not** build V1 around:
- Backstage;
- Redis;
- a central SQL coordination DB;
- a custom GitHub App;
- a web dashboard;
- Kubernetes;
- an event bus;
- arbitrary lock-expression/glob languages;
- a custom task dependency format;
- committed live-state snapshots as default truth;
- a proprietary replacement for `AGENTS.md`;
- mandatory GitHub Actions;
- automatic merging;
- autonomous merge-conflict resolution;
- auto-expanding issue trees;
- an AI project manager deciding priorities;
- a long-running daemon/server.

These were explicitly rejected because the user is a single operator and wants universal usefulness without turning coordination tooling into a new platform project.

## Evidence and validation

### BioTrack / GitHub evidence pointers

- BioTrackCore PR #16 — data-contract decision/resume checkpoint.
- BioTrackCore PR #17 — Contract v1, head observed at `0206f0d5...`.
- BioTrackCore PR #18 — stacked cyclic-lineage validation PR created in this conversation.
- AquaTrack PR #1 — canonical one-row export repair, head observed at `25e5b2f...`.
- `ichabod-agent-mailbox#83` — Aqua A.4 canonical artifacts job; no comments at final poll.
- `ichabod-agent-mailbox#79` — partial corrective measurements; several requested measurements remained open.

### Existing agent-skills evidence

`codebase-intelligence/repo-context-hardening/SKILL.md` already defines:
- evidence before prose;
- current truth vs history;
- source-of-truth mapping;
- protected surfaces;
- generated outputs;
- explicit operator gates;
- prefer enforcement over warnings;
- cold-agent verification.

The proposed repo-control layer should complement this instead of duplicating it.

`agent-operations/context-clear/SKILL.md` defines the checkpoint protocol used to create this file.

### Research-derived design conclusions from this conversation

The process-design pass concluded that existing Git/GitHub primitives should be reused rather than rebuilt:
- issues/PRs/branches/comments/commits remain durable coordination evidence;
- issue dependencies/sub-issues should be preferred over a custom dependency graph where available;
- Git worktrees are appropriate for local isolation but are not a cross-environment protocol;
- account-level GitHub templates and reusable workflows are optional rollout features, not the core.

These are design conclusions to re-check against current GitHub documentation when implementation begins; do not assume API details remain unchanged indefinitely.

## Blockers and unresolved

### BioTrack audit

The provenance/data-quality audit is still in flight and must not be duplicated.

#83 and #79 had not produced new completion evidence by the final poll in this conversation.

### Universal repo-control

**UNRESOLVED:** No implementation has been started.

**UNRESOLVED:** `repoctl` is only a working name.

**UNRESOLVED:** Exact claim-comment marker/serialization format should be decided when implementing.

**UNRESOLVED:** Lease duration of 24 hours is proposed, not operator-approved policy.

**UNRESOLVED:** Decide whether `repoctl init` belongs in the first implementation or should wait until the read-only pilot demonstrates what config is actually necessary.

**UNRESOLVED:** Decide whether validation evidence should be posted as PR/issue comments by default or only emitted locally/attached on request.

**UNRESOLVED:** Choose an ordinary third pilot repo after `agent-skills` and `ichabod-agent-mailbox`.

## Next actions

When this process-improvement thread resumes:

1. Re-read this checkpoint, then re-check current GitHub state before acting.
2. Do **not** resume BioTrack audit/remediation work unless explicitly reassigned.
3. Inspect current `agent-skills` state and any newer repo-control/context-hardening work before creating files.
4. If the operator approves implementation, start with **Phase 1 only**:
   - create `agent-operations/repo-control/`;
   - write a compact `SKILL.md`/protocol;
   - implement read-only `doctor` + `status`;
   - optionally support `.repoctl.toml`, but work safely when absent.
5. Pilot Phase 1 against:
   - `agent-skills`;
   - `ichabod-agent-mailbox`;
   - one ordinary application/code repo.
6. Only if the read-only pilot is genuinely useful, add **Phase 2 claims**:
   - issue-comment claim record;
   - exact file/directory-prefix/resource locks;
   - leases/stale detection;
   - cloud/local round-trip proof.
7. Only after claims work, add **Phase 3 validation evidence** tied to exact SHA.
8. Add optional worktree integration after the protocol is stable.
9. Roll out selectively across repos; archived/simple repos should not receive unnecessary config.

### Pilot acceptance threshold before broad rollout

Require all of these:

- cold local agent can understand current repo state;
- cold cloud agent sees the same ownership picture;
- overlapping write claims are blocked;
- non-overlapping work can proceed concurrently;
- native blockers prevent dependent work;
- stale/expired claims can be recovered;
- exact tested commit is recorded;
- stacked PRs are recognized;
- dirty canonical checkout is never destroyed;
- tool works without GitHub Actions;
- missing config degrades safely;
- no server/database is required.

## Source-of-truth pointers

### BioTrack

- `wowthisiseasytoremember-stack/biotrack-core` PR #16
- `wowthisiseasytoremember-stack/biotrack-core` PR #17
- `wowthisiseasytoremember-stack/biotrack-core` PR #18
- `wowthisiseasytoremember-stack/aquatrack` PR #1
- `wowthisiseasytoremember-stack/ichabod-agent-mailbox` issue #79
- `wowthisiseasytoremember-stack/ichabod-agent-mailbox` issue #83

### Process/agent tooling

- `wowthisiseasytoremember-stack/agent-skills/codebase-intelligence/repo-context-hardening/SKILL.md`
- `wowthisiseasytoremember-stack/agent-skills/agent-operations/context-clear/SKILL.md`

Proposed future location:
- `wowthisiseasytoremember-stack/agent-skills/agent-operations/repo-control/`

## Noncanonical / proposed

The following ideas are intentionally preserved because they were unique and potentially valuable, but they are **not approved implementation requirements**:

- working name `repoctl`;
- `.repoctl.toml` as a tiny optional config;
- TOML over YAML to stay dependency-light in Python;
- six-command ceiling: `init`, `doctor`, `status`, `claim`, `release`, `validate`;
- claim comment schema `repoctl.claim.v1`;
- validation evidence schema `repoctl.validation.v1`;
- 24-hour lease default;
- exact file / directory prefix / named resource lock model;
- optional `--worktree`;
- conventional local branch name `issue/<number>-<slug>` when the repo has no stronger convention;
- an account-wide `.github` repo for default templates after pilots;
- reusable workflows after local operation proves out;
- future ruleset/branch-protection integration only after it cannot deadlock the single-operator workflow.

Potential relationship among tools:

`AGENTS.md`
-> tells an agent how the repo works

`repo-context-hardening`
-> repairs static/current repository knowledge and source-of-truth boundaries

`repoctl` (proposed)
-> checks live coordination state, blockers, claims, exact validation evidence

GitHub Issues/PRs
-> durable work history and native dependencies

`context-clear`
-> preserves conversation-only state before the chat is discarded

## Superseded

### SUPERSEDED: BioTrack-specific control plane as the universal solution

Earlier in this conversation, a BioTrack-specific control plane was proposed with generated ecosystem state, workstream ownership, PR dependency guard, status-evidence linting, and `biotrack doctor`.

**Replacement:** Generalize the useful ideas into a small GitHub-native repo protocol/tool that can work across all repositories. BioTrack may consume it later; it should not own the universal mechanism.

### SUPERSEDED: committed `PROJECT_STATE.json` as universal live truth

Older BioTrack plans proposed generated `PROJECT_STATE.json` in each repo.

**Replacement for universal coordination:** query live state from Git/GitHub on demand. Explicit snapshots can still exist for releases/audits/checkpoints.

### SUPERSEDED: custom dependency graph

**Replacement:** use native GitHub issue dependencies/sub-issues where practical; do not maintain an additional dependency DAG.

### SUPERSEDED: server/dashboard-first design

**Replacement:** no central service for V1. GitHub is the durable coordination substrate; CLI/skill are clients of the same protocol.

## Persistence receipt

This checkpoint is intended to be persisted in the public `wowthisiseasytoremember-stack/agent-skills` repository because it contains project/process state only and deliberately omits credentials and unrelated sensitive personal information.

Redacted/omitted:
- passwords, tokens, credentials;
- unrelated personal profile details;
- private health/relationship/financial context;
- raw conversation chatter that is not needed to resume correctly.

Persistence verification is recorded in the accompanying `context-clear.json`.
