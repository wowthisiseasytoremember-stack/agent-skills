# Local-agent implementation brief — AI provider verification and bounded fallback pilot

Date: 2026-11-06
Status: PROPOSED / NOT CLAIMED / NOT APPROVED FOR PRODUCTION
Canonical discussion: https://github.com/wowthisiseasytoremember-stack/agent-skills/pull/17
Related assessment (same branch): research/free-ai-provider-assessment-2026-11-05.md
Related previous handoff: https://github.com/wowthisiseasytoremember-stack/agent-skills/pull/17#issuecomment-6673283108

## Instructions to an agent with no chat history

You are implementing a **small, reversible pilot**, not a new platform. The operator wants the existing workflows to discover and use permitted low-cost AI inference and image-generation capacity, while remaining resilient to shifting free tiers and provider failures. Another agent may be working on the same topic. **Before editing, read this brief and PR #17, inspect repository instructions, open claims, issues, open PRs, locks, and existing gateway/registry/ledger code. Publish a claim in the current canonical implementation thread. If someone owns it already, coordinate with them and do not create a parallel branch.**

## Objective and boundaries

1. Identify existing model gateway / provider catalog / capability router / event ledger; **prefer reuse**. A public project `sass-maker/free-ai` has a provider registry and policy checks, but its role in this operator's system is **unverified**. Assess fitness, maintenance, license, ownership, and integration before adopting.
2. Verify **three eligible providers** using dated official source links and bounded, authorized smoke calls. OpenRouter, Pollinations, and Puter are research candidates, NOT automatically compatible/equivalent. Puter is reportedly user-pays; don't treat it as unlimited backend inference. Pollinations authentication requirements must be checked. Record any exclusions.
3. Implement only what the existing architecture lacks: a minimal machine-readable registry, permitted health probes, hard ceilings, and fallback selection for **offline, noncritical** work. Initially no production service or cron required.
4. Pilot on at least ten representative offline Content Factory tasks (e.g., headline/title or storyboard proposals) and compare against current baseline. Record per-task quality and cost, failures, latency, and selection outcomes.
5. Make a small isolated PR with current-head test evidence. Do not merge, activate, deploy, bill, create accounts, or change publication settings without separate authority.

**Never touch:** live 6925 capture/streaming/publishing paths, existing comment auto-replier, provider credentials, Google SSO sessions, browser profile stores, CI/review policy (#13/#14), other agents' active branches or locks, any production scheduler. Treat user-provided NSFW and CDP material as historical research only, not automation authorization. No anti-bot evasion, unsupported scraping, or tunneling around provider restrictions.

## Where files belong

Do not assume the suggested names below exist. After inspecting the selected canonical implementation repository, use **its established conventions** for configuration, tests, scripts, documentation, and reporting. If equivalent code already exists, extend it instead of adding duplicates. The only known canonical research location is `agent-skills` PR #17, file `research/free-ai-provider-assessment-2026-11-05.md`. Keep the implementation link and verification receipts discoverable in that PR.

Expected *logical* artifacts, not mandatory new directories:
- Provider metadata, in the current configuration registry (YAML/JSON/database as already used). Fields: provider ID, capability/modality, API-vs-UI-vs-client-SDK, enabled/disabled, models, verified limits, source URLs/date, authentication requirement (not credentials), rights/terms, cost status, uncertainty.
- A bounded verification command in existing scripts/tests infrastructure, with status, method, timestamp, latency, quota/cost observation, errors, and zero secrets.
- A test or configuration for selection/fallback in the existing router, with no retry storm and no unbounded requests.
- A dated pilot receipt in the project's normal report/test artifact location, linked back to PR #17.
- Existing owner issue/PR updated with claims, blockers, and final disposition.

## Verification criteria

- Primary sources documented for **at least three provider candidates**; mark unknown, not free, if missing current proof. Verify account requirements, quotas, permissible automation, commercial image rights, and client/browser-only restrictions.
- Provider probe has explicit timeout; rate-limit handling (429 with bounded exponential backoff); hard max retries and per-run budget; does not retry forbidden or payment-required operations.
- Test response is actual model inference, not merely 200 from a /models or heartbeat endpoint. A failed check must not mark a provider healthy.
- Logging excludes API keys, auth cookies, secret URLs, raw private prompts, SSO identifiers, and response text when sensitive.
- Fallback order deterministic and explainable. Unknown/unavailable providers skipped; fail closed without a usable candidate. No surprise billing.
- At least ten real representative offline tasks scored against current baseline with stated rubric (semantic correctness, brand/editorial fit, useful output, cost, latency, reliability).
- Nothing writes to content publication, social comments, livestream, or other production queues.

## Test suite to add/run using existing framework

1. **Schema/source test**: every enabled candidate has dated primary docs, modalities, auth description, bounded limits, and machine-valid config; secrets absent.
2. **Healthy route test**: permitted provider returns valid minimal generation; verify model and output schema.
3. **429 / timeout / 5xx tests**: bounded backoff and fallback, circuit breaker (if the existing router has one), no tight loop.
4. **Exhausted budget / no provider test**: explicit non-success outcome, zero requests or spend beyond ceiling.
5. **Secret redaction test**: synthetic token/cookie/private prompt never appears in logs, exceptions, JSON receipt.
6. **Isolation test**: mock external publish/comment/live endpoints; assert zero calls during all probes/pilot.
7. **Task pilot**: >=10 tasks with measured results and comparison. No unverified blanket quality claims.
8. **Existing regression suite** for any files modified; capture exact command, commit SHA, exit code and outputs in PR. Do not invent command names before inspecting the chosen repository.

## Stop conditions

Stop and report blockers if a claimed owner exists, terms prohibit intended use, auth would require unsafe automation, the provider has no eligible allowance and no authorized payment ceiling, or the proposed change could affect production. Do not work around the restriction.

## Completion receipt (add to canonical implementation issue/PR and link from PR #17)

Owner/claim URL; repository and exact head SHA; changed paths; provider evidence links and verification times; tests/commands and exit status; 10-task quality/cost/latency table; dry-run fallback evidence; known gaps; production state (should be OFF); next explicitly authorized action.

## Context / rationale

Original conversation supplied a 19-provider research matrix (text/API, web image tools, GPU compute), a Chrome CDP/Google SSO checklist, and a JSON example report. Those descriptions were user-supplied hypotheses, not independently qualified guarantees. The verbatim user text was not preserved in GitHub due a previous connector rejection; a separate preservation issue must remain open until an authoritative copy is uploaded. The research assessment identified 6925 offline editorial drafts, Content Factory images, and Ichabod shared capability discovery as potential future consumers. Prefer a small single-workload pilot over standing infrastructure.
