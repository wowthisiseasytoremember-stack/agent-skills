# Context Clear (`/cc`)

`context-clear` is a portable Agent Skill for making a conversation safe to close.

It scans the current conversation for execution-critical state that would otherwise disappear, separates canonical/approved state from proposals and superseded material, persists a compact checkpoint to a verified durable destination, and performs a cold-resume test before declaring success.

## Invocation

Preferred human shorthand:

```text
/cc
```

Canonical skill name:

```text
context-clear
```

Fallback phrases:

```text
cc
context clear
make this conversation safe to close
```

`/cc` is an alias, not part of the Agent Skills file-format standard. Hosts that support custom command aliases can map `/cc` to activation of `context-clear`; other hosts should invoke the skill by name or trigger phrase.

## Durability

A successful run requires at least one verified external destination:

1. an existing project handoff/state convention;
2. a configured Git context vault (`CONTEXT_CLEAR_GIT_ROOT`);
3. a configured durable server path (`CONTEXT_CLEAR_SERVER_ROOT`);
4. Google Drive.

The skill never calls an in-chat summary a successful backup.

## Outputs

Each checkpoint contains:

- `CONTEXT_CLEAR.md` — human/agent resume document;
- `context-clear.json` — machine-readable receipt and validation metadata.

See `references/SCHEMA.md`.

## Local installation

Place or link this skill directory into the skill directory used by the local agent. Existing consumers of this repository currently sync skills into `~/.claude/skills/`.

For hosts implementing the open Agent Skills format, install the directory unchanged.

## Hosted/cloud installation

Upload this directory as one skill bundle. OpenAI's Skills API accepts a directory upload or ZIP and supports immutable skill versions. Keep this Git repository as the canonical source and publish versions from reviewed commits.

## Slash-command alias

Do not fork the skill just to obtain `/cc`.

Where the host supports user-defined aliases, make the alias expand to a request equivalent to:

```text
Use the context-clear skill now. Treat this as an explicit /cc invocation.
```

Where the host does not expose custom slash-command registration, use `cc`, `context clear`, or select/invoke `context-clear` directly.

## Validation

With Python 3:

```bash
python3 scripts/validate_bundle.py CONTEXT_CLEAR.md --manifest context-clear.json
```
