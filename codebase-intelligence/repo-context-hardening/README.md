# repo-context-hardening

Repository discovery and agent-context hardening for GitHub repositories.

## Files

- `SKILL.md` — semantic discovery/hardening instructions used by the orchestrator.
- `scripts/context_lint.py` — deterministic CI checks for context discoverability and broken local references.
- `templates/repo-context-hardening.yml` — small caller workflow to copy into another repository.
- `../../.github/workflows/repo-context-hardening.yml` — reusable workflow hosted by `agent-skills`.

## Modes

| Mode | Runner | Behavior |
|---|---|---|
| `lint` | GitHub-hosted | Deterministic checks only. Never edits the repo. |
| `audit` | self-hosted | Hermes performs the full skill read-only; bounded YOLO-auto workers may do recon. |
| `apply` | self-hosted | Hermes hardens documentation/context, workflow validates changes, then opens a draft PR. |

`apply` never merges or deploys automatically.

## Self-hosted runner prerequisites

The runner used for `audit`/`apply` must have:

- `git`
- Hermes available as `hermes` or `~/.local/bin/hermes`
- configured MCP/delegation access used by Hermes, including YOLO-auto when available
- `gh` for `apply` with `open_pr=true`

Do not put provider API keys in workflow YAML or repository files. Use the runner's existing secure configuration.

## Add to another repository

Copy `templates/repo-context-hardening.yml` to:

```text
.github/workflows/repo-context-hardening.yml
```

The caller delegates to the canonical reusable workflow in this repository.

From GitHub Actions choose **Repo Context Hardening**, then select:

- `lint` for fast CI validation
- `audit` for semantic read-only discovery
- `apply` to produce a reviewable documentation-hardening draft PR

`target_path` may be `.` or a nested project/package. The semantic skill still inspects the applicable path ancestry and repository/workspace boundaries before editing.
