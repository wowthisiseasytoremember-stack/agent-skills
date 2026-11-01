# Standard PR risk review (pilot)

This is the shared **path-based risk routing** layer. It complements existing CI; it does not approve or merge code, make AI findings, prove deployment, or claim runtime verification.

## Adoption

In a caller repository, add `.github/workflows/standard-pr-risk.yml`:

```yaml
name: Shared PR Review
on:
  pull_request:
permissions:
  contents: read
  pull-requests: read
jobs:
  classify:
    uses: wowthisiseasytoremember-stack/agent-skills/.github/workflows/standard-pr-risk.yml@<PINNED_FULL_SHA>
    with:
      policy_ref: <SAME_PINNED_FULL_SHA>
```

Replace both placeholders with the *same immutable commit SHA from agent-skills after the pilot PR is merged*. During pilot-only testing, `@master` and `policy_ref: master` are usable but unpinned. Caller PRs run on GitHub-hosted runners; no production host or secrets are needed. The workflow uses a read-only token, fetches all changed paths via the GitHub API, runs the classifier's contract tests, emits a GitHub step summary and attaches `risk-report.json`. Do not mistake this for a full code review.

Optional caller file `.github/pr-risk-policy.json` **may only add protected paths**:

```json
{
  "additional_high": ["ops/release/**", "config/prod/**"],
  "additional_medium": ["prompts/**"]
}
```

Editing the caller policy, GitHub workflows or AGENTS.md is itself high risk. Unknown/invalid input fails the check; a valid high-risk classification is advisory and does not fail by itself.

## Three layers, one consistent contract

1. **Existing repository CI remains canonical for tests/lint/security.** Do not replace its checks with this routing signal. Review generated artifacts, provenance and data safety in project-specific CI.
2. **Independent substantive review** is a separate, bounded agent/human step. Hunt -> verify -> rank -> disposition, with each finding keyed to an exact PR head SHA, file/line, evidence, and status. An AI vote never counts as human approval. An automated "no findings" result is not proof of safety. Existing `web-quality/code-review-web` provides a review method; no new AI reviewer credentials, bot, or self-hosted runner are added by this PR.
3. **Merge and release authority** belongs to repository-specific protections and operating policy. A high risk result recommends operator consideration; if the repo lacks enforceable required checks/branch protection, this workflow **does not prevent merging or direct pushes**. Actual approvals, deployment and production verification require distinct state/receipts.

### Risk tiers

| Tier | Default | Intended handling |
|---|---|---|
| LOW | Documentation and non-executable content | Existing CI; eligible for low-touch handling |
| MEDIUM | Application code, tests/code, most configuration | Existing CI plus independent reviewer when available |
| HIGH | GitHub workflows, AGENTS.md, publisher, auth, payments, migrations, deploy, secrets, explicitly protected caller paths | Operator attention and independent review before merge; verify deployment separately |

Risk depends on **changed paths**, not author or size. This is deliberately conservative but cannot detect a dangerous behavioral change hiding in an ordinary code path. Escalation is permitted; no automatic downgrade is supported.

## Rollout / stop conditions

- Pilot this PR in `agent-skills`, run the included seven contract tests and inspect the Actions risk receipt. Do not treat an unrun action as verified.
- Add the tiny caller workflow via **draft PRs**, starting with one representative production repo. Compare results to the project's current CI and inspect false positives, API permissions, and execution time.
- Expand only after one complete green PR and risk receipt per repo. Keep CI separate and preserve existing publisher/approval/release rules.
- To *enforce* high-risk human authorization, add supported GitHub branch protection/rulesets or an equivalent separately verified gate. Private repos currently return a GitHub 403 upgrade response to ruleset GET under this account; do not assume rulesets can be enforced there.
- For continuous improvement, attach incident IDs, reproduction steps, expected vs actual outcome, exact bad/fix SHAs and regression tests to versioned cases. An evaluator can later compare reviewer versions on those cases before promoting prompts/models. Do not introduce a daily LLM run before a measured corpus exists.

**Rollback:** remove the caller workflow in a PR. The shared source cannot merge, publish or change caller code. Pinned SHA releases avoid surprise behavior changes.
