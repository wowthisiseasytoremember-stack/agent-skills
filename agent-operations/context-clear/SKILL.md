---
name: context-clear
description: >
  Preserve the execution-critical context of the current conversation before it is
  closed, reset, compacted, or handed to another agent. Trigger on /cc, "context
  clear", "checkpoint this chat", "back up this conversation", "make this safe to
  close", or equivalent requests. Distill anything that would be costly or unsafe
  to lose, classify canonical versus proposed state, persist it to a verified
  durable destination such as Git, a configured server path, or Google Drive, and
  prove a cold agent could resume without the original conversation.
compatibility: >
  Portable Agent Skill for local and hosted agents. Requires access to the current
  conversation plus at least one writable durable destination (Git/GitHub, local or
  server filesystem, or Google Drive). Python 3 is optional for bundled validation.
metadata:
  aliases: "/cc, cc, context clear"
  version: "1.0.0"
---

# Context Clear

## Mission

Make the current conversation disposable **without losing execution-critical state**.

`/cc` means: inspect the full conversation context available to you, identify information that exists only in the conversation and would materially matter later, distill it into a durable checkpoint, persist it to at least one verified destination, and test whether a zero-memory agent could safely resume from that checkpoint.

Do **not** equate "I wrote a summary" with success. Success requires:

1. the checkpoint contains the necessary state;
2. the checkpoint is persisted outside the conversation;
3. the persisted copy is read back or otherwise verified;
4. a cold-resume test passes; and
5. the user receives a persistence receipt.

If any of those fail, report **CC NOT CLEAR** rather than claiming the conversation is safe to close.

## Activation

Treat any of these as explicit activation:

- `/cc`
- `cc`
- `context clear`
- `checkpoint this chat`
- `back this conversation up`
- `make this safe to close`
- `save everything important before I start a new chat`
- equivalent wording with the same intent

Host note: the skill is canonical. `/cc` is an alias. If a host does not support custom slash commands, invocation by `cc`, `context clear`, or explicit skill selection must still activate this workflow.

## Non-goals

Do not:

- dump the entire raw conversation by default;
- preserve chatter merely because it appeared recently;
- copy facts that are already safely canonical unless a pointer to them is required for resumption;
- silently promote brainstorming, hypotheses, or proposed work into approved requirements;
- persist secrets, auth tokens, passwords, private keys, session cookies, or credential-bearing URLs;
- persist sensitive personal information unless it is essential to the requested work and the user explicitly wants it retained;
- write sensitive/private checkpoints to a public repository;
- claim a write succeeded without verification;
- overwrite a newer checkpoint blindly.

## What to recover from the conversation

Scan the available conversation from oldest relevant state through the current turn. Capture information that would create meaningful rediscovery, ambiguity, rework, or risk if the conversation vanished.

At minimum inspect for:

### 1. Objective and definition of done
- What is the user actually trying to accomplish?
- What does "finished" mean?
- What scope is explicitly in or out?

### 2. Decisions and operator approvals
- approved architecture or workflow choices;
- explicit "ship", "merge", "do not touch", "hold", or priority decisions;
- accepted defects or tradeoffs;
- policy, safety, privacy, or quality gates;
- decisions that superseded earlier decisions.

### 3. Exact execution state
- current repository/project;
- branch/worktree;
- commit SHA;
- issue/PR numbers;
- files created or changed;
- commands already run;
- tests/checks and their exact outcomes;
- artifacts already produced;
- the exact resume point.

### 4. Blockers, uncertainty, and unresolved work
- known failures;
- missing inputs;
- assumptions not yet validated;
- questions intentionally left open;
- least-confident areas.

### 5. Next actions
Record the smallest correct next steps in dependency order. Prefer executable next actions over vague plans.

### 6. Source-of-truth pointers
Record enough identifiers for a cold agent to locate durable evidence without the original chat:
- repository and path;
- commit/branch/tag;
- issue/PR;
- Drive file/folder;
- server path;
- relevant URL or durable ID when safe.

### 7. User-specific operating constraints
Only capture durable preferences or constraints that materially change execution for this task. Avoid unrelated biography or sensitive profile information.

### 8. Noncanonical material
Keep proposals, experiments, brainstorms, and alternatives if losing them would matter, but label them **PROPOSED / NONCANONICAL**.

### 9. Superseded material
If the conversation contains stale instructions likely to mislead a future agent, record them under **SUPERSEDED** with the replacement decision.

## Loss test

For every candidate fact, ask:

> If the original conversation disappeared right now, would a competent zero-memory agent be slower, more likely to make a wrong decision, repeat work, or violate a constraint without this fact?

If **yes**, preserve or point to it.
If **no**, omit it.

Prefer pointers over duplication when the durable canonical source already exists.

## Destination selection

At least one destination must be both **durable** and **verified**.

Use the first safe destination that fits the current project, then mirror only when configured or clearly useful.

### A. Existing project handoff/state convention
If the project already has a canonical handoff, state, resume, or agent-context location, use it rather than inventing another system.

Examples include `.handoff/`, `docs/handoffs/`, `STATE.md`, or a project-specific canonical state directory.

Do not alter canonical project files merely to satisfy this skill if the project explicitly forbids it.

### B. Dedicated Git context vault
If a configured context-vault Git repository exists, prefer it for cross-project checkpoints.

Recommended environment variable:

`CONTEXT_CLEAR_GIT_ROOT`

Recommended layout:

`<root>/<project>/<YYYY>/<YYYY-MM-DD>/<checkpoint-id>/`

Never commit credentials. If the target repository is public, persist only content that is safe to publish.

### C. Configured server storage
If a durable server/filesystem target is configured, use it.

Recommended environment variable:

`CONTEXT_CLEAR_SERVER_ROOT`

Use an atomic write where the host allows it: write to a temporary path, fsync/close if practical, rename into place, then read it back.

### D. Google Drive
If Google Drive is available, use a configured `Context Clear` folder or equivalent user-designated folder.

Recommended layout:

`Context Clear/<project>/<YYYY>/<YYYY-MM-DD>/<checkpoint-id>/`

Prefer a machine-readable manifest plus a human-readable checkpoint. Verify the uploaded object can be fetched/read after creation.

### E. No durable destination
Generate the checkpoint in the response if useful, but report **CC NOT CLEAR — no verified durable destination**.

A local temp file, uncommitted working-tree file, draft response, or memory-only summary does not count as durable persistence.

## Bundle format

A checkpoint should contain:

```text
<checkpoint-id>/
├── CONTEXT_CLEAR.md
└── context-clear.json
```

The Markdown is optimized for a human or agent resuming work. The JSON manifest is optimized for indexing and verification.

Use `references/SCHEMA.md` for the full format.

## Required Markdown sections

`CONTEXT_CLEAR.md` must contain:

1. `# Context Clear Checkpoint`
2. `## Resume in one sentence`
3. `## Objective and definition of done`
4. `## Canonical state`
5. `## Work completed`
6. `## Current execution state`
7. `## Decisions and constraints`
8. `## Evidence and validation`
9. `## Blockers and unresolved`
10. `## Next actions`
11. `## Source-of-truth pointers`
12. `## Noncanonical / proposed`
13. `## Superseded`
14. `## Persistence receipt`

Keep empty sections when they are semantically important; write `None known.` rather than deleting them.

## Classification rules

Every important statement should be unambiguous about its authority. Use these meanings:

- **CANONICAL** — durable source of truth or explicitly approved operator state.
- **APPROVED** — user/operator explicitly accepted it but it may not yet be encoded canonically.
- **OBSERVED** — directly verified from tools, files, tests, or system state.
- **PROPOSED** — suggested but not approved.
- **UNRESOLVED** — intentionally open or blocked.
- **SUPERSEDED** — once relevant but replaced by newer state.

Do not infer approval from repetition or from an assistant having proposed something earlier.

## Persistence protocol

1. Build the checkpoint in memory.
2. Redact credentials and unnecessary sensitive data.
3. Validate the structure.
4. Select a safe destination.
5. Write without clobbering newer state.
6. Verify by reading the persisted copy, checking a returned revision/object ID, or both.
7. Record the destination and verification evidence in `context-clear.json`.
8. Re-run validation on the persisted content when possible.
9. Perform the cold-resume test.
10. Only then return **CC CLEAR**.

For Git:
- prefer a dedicated checkpoint file rather than rewriting unrelated docs;
- preserve a dirty working tree;
- commit only the checkpoint material if making a commit;
- record repository, branch, commit SHA, and checkpoint path;
- never stage unrelated user changes.

For Google Drive:
- record stable file/folder IDs when available;
- verify by re-fetching the uploaded content or metadata.

For server/filesystem writes:
- record absolute durable path only when it is safe to expose;
- verify by reopening the final file after rename/write.

## Validation

If Python 3 is available, run:

```bash
python3 scripts/validate_bundle.py /path/to/CONTEXT_CLEAR.md --manifest /path/to/context-clear.json
```

The validator checks required sections, manifest structure, and common credential patterns. It does not prove semantic completeness; the cold-resume test does that.

## Cold-resume test

Before reporting success, pretend the original conversation no longer exists.

Using only the persisted checkpoint and its pointers, verify that a competent agent can answer:

1. What are we trying to accomplish?
2. What is canonical/approved versus merely proposed?
3. What has already been done and validated?
4. What is the exact current state and the biggest blocker/uncertainty?
5. What should happen next, in order?
6. Where is the durable evidence/source of truth?

Then ask:

> Is there any important decision, constraint, artifact location, test result, failure, or resume detail I am still relying on from the original conversation rather than from the checkpoint?

If yes, update the checkpoint and repeat the test.

## Final response contract

On success, respond compactly in this form:

```text
CC CLEAR

Persisted:
- <destination + durable identifier>

Resume:
<one-sentence resume point>

Verified:
- structure: PASS
- persistence/read-back: PASS
- cold-resume test: PASS
```

On failure:

```text
CC NOT CLEAR

Prepared:
- <what was captured>

Blocked:
- <why durable verified persistence did not complete>

Do not treat this conversation as disposable yet.
```

Never use `CC CLEAR` when only an in-chat summary exists.

## Privacy and safety

Before persistence, explicitly screen for:
- API keys and tokens;
- passwords and private keys;
- auth cookies;
- account numbers or secret identifiers;
- precise private addresses;
- health/relationship/financial or other sensitive personal details that are not essential to the work.

Store the minimum necessary context. A useful checkpoint is a recovery artifact, not a surveillance archive.

When the destination is public or its privacy is unknown, default to stricter redaction or choose a private destination.

## Idempotency

Repeated `/cc` invocations should be safe.

Prefer immutable timestamped checkpoint directories plus a stable optional `LATEST` pointer managed by the host. Never destroy an earlier good checkpoint merely because a newer run exists.

Suggested checkpoint ID:

`YYYYMMDDTHHMMSSZ-<project-slug>-<short-hash>`

## Completion standard

The conversation is context-cleared only when **nothing material needed to resume correctly exists solely in the conversation** and at least one durable copy has been verified outside the conversation.
