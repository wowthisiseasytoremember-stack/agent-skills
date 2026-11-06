# Free AI provider research — assessment (2026-11-05)

Status: **PROPOSED / UNVERIFIED**. This note is a derivative assessment of user-supplied research, **not a verbatim archival copy**. The original source remains in the ChatGPT conversation. Provider descriptions and quotas are subject to change.

## What is useful
- Maintain a registry of provider capabilities: modality, API availability, free allowance, rate limits, terms, credentials required, latency, success rate, and last verification.
- Run low-impact health checks and select providers through a capability router rather than hardcode a single free service.
- Keep human-in-the-loop for account creation, login consent, age verification, billing, and policies.
- Treat GPU notebooks as intermittent experiment capacity, not production infrastructure.

## Critical corrections
- Puter.js uses a **user-pays** model: signed-in users have a finite allowance and pay for overages. Not unlimited free inference for server workloads. https://developer.puter.com/pricing/
- Pollinations current published API docs show authentication required on gen.pollinations.ai; don't assume all endpoints remain anonymous or unlimited. https://gen.pollinations.ai/
- OpenRouter confirms 50 requests/day and 20 RPM for :free models on accounts below the credit threshold; availability varies. https://openrouter.ai/collections/free-models

## Proposed architecture
1. provider-registry.yaml — source-backed capability descriptions with verification date.
2. verify-providers — lightweight, permitted checks; outputs a structured JSON report.
3. capability-router — task-based ranked selection with timeout/fallback/circuit breaker.
4. provider-ledger — per-job provider, model, latency, retries, cost, errors, quality, license.
5. Production tier uses stable authorized APIs/local compute; opportunistic free capacity used for non-critical batch jobs only.

## Project opportunities
- 6925 RELAY: title candidates, transcripts, comment draft suggestions and metadata, never on-air or publish-critical paths.
- Tangle Trove media: draft thumbnails/storyboards and non-urgent image experiments, with explicit review of output rights.
- Agent skills: reusable provider-verification and resilience guidance.
- Ichabod: a single local service can expose verified capability choices to existing workflows.

## Safety
Do not publish credentials, browser profiles or sessions. Keep the Chrome debugging interface bound to loopback; do not automate around providers' anti-abuse controls or prohibited notebook tunneling. Preserve live-stream isolation. Never treat free-tier claims as service-level guarantees.

## Source preservation
A verbatim GitHub import was attempted but rejected by the connector safety checks. This derivative note must not be presented as the original source.
