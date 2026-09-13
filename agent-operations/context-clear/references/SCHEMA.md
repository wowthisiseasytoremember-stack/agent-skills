# Context Clear bundle schema

Schema identifier: `context-clear/v1`

A Context Clear checkpoint is intentionally small. It preserves the minimum durable state needed to resume safely; it is not a raw chat transcript.

## Files

```text
<checkpoint-id>/
├── CONTEXT_CLEAR.md
└── context-clear.json
```

## `CONTEXT_CLEAR.md`

Required headings, in order:

```markdown
# Context Clear Checkpoint

## Resume in one sentence

## Objective and definition of done

## Canonical state

## Work completed

## Current execution state

## Decisions and constraints

## Evidence and validation

## Blockers and unresolved

## Next actions

## Source-of-truth pointers

## Noncanonical / proposed

## Superseded

## Persistence receipt
```

Use authority labels where they matter: `CANONICAL`, `APPROVED`, `OBSERVED`, `PROPOSED`, `UNRESOLVED`, `SUPERSEDED`.

## `context-clear.json`

Minimum shape:

```json
{
  "schema": "context-clear/v1",
  "checkpoint_id": "20260913T051500Z-example-a1b2c3d4",
  "created_at": "2026-09-13T05:15:00Z",
  "project": "example",
  "resume": "Continue from the verified resume point.",
  "status": "verified",
  "content_sha256": "<sha256 of CONTEXT_CLEAR.md>",
  "destinations": [
    {
      "type": "git",
      "locator": "owner/repo:path@commit",
      "verified": true,
      "verification": "read-back matched expected content hash"
    }
  ],
  "redactions": [],
  "source_refs": []
}
```

### Required fields

- `schema`: exactly `context-clear/v1`
- `checkpoint_id`: stable unique checkpoint identifier
- `created_at`: ISO-8601 timestamp
- `project`: human-readable project/workstream name
- `resume`: one-sentence resume point
- `status`: `prepared`, `persisted`, or `verified`
- `content_sha256`: SHA-256 of `CONTEXT_CLEAR.md`
- `destinations`: array of destination receipts

A checkpoint may claim `verified` only when at least one destination has `"verified": true`.

### Destination receipt

Recommended fields:

- `type`: `git`, `server`, `gdrive`, or another explicit durable backend
- `locator`: durable path/object/revision identifier
- `verified`: boolean
- `verification`: short description of read-back/revision evidence
- `revision`: optional commit SHA or object version
- `visibility`: optional `private`, `public`, or `unknown`

Do not put credentials into `locator`.

### Optional fields

- `redactions`: what classes of information were deliberately omitted
- `source_refs`: durable issue/PR/file/object references that support the checkpoint
- `supersedes`: previous checkpoint ID
- `conversation_label`: non-secret label for the source chat/session

## Recovery invariant

A valid bundle is necessary but not sufficient. Semantic success requires a cold agent to recover the objective, authority boundaries, completed work, current state, blockers, next steps, and durable evidence without the original conversation.
