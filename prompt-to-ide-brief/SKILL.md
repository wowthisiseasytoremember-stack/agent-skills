---
name: prompt-to-ide-brief
description: Convert messy, contradictory, or overly detailed user prompts into a concise, IDE-ready brief with intent, scope, deliverables, guardrails, assumptions, questions, success checks, and a short work plan. Use when a user asks to clean, restructure, or make actionable prompts for coding agents/IDEs (Cursor, Claude, Antigravity, etc.), or when prompts are scattered, contain error logs, or mix multiple requests.
---

# Prompt To Ide Brief

## Overview

Turn raw prompts into a short, executable brief that a coding agent can follow safely, with clear deliverables and guardrails.

## Workflow

1. Extract the core intent in 1-2 sentences.
2. Normalize scope:
- Split combined requests into discrete tasks.
- Mark out-of-scope items explicitly if the prompt mixes unrelated work.
3. Convert into concrete deliverables:
- Files, changes, or outputs that must exist when done.
4. Add guardrails:
- Safety constraints, approvals needed, or do/don't rules.
5. Resolve ambiguity:
- State assumptions.
- Ask at most 3 blocker questions.
6. Define success checks:
- Tests, build, lint, or manual verification.
7. Provide a short, ordered work plan (3-7 steps).

## Output Template

Use this exact section order. Keep each section concise.

Intent:
Scope:
Deliverables:
Guardrails:
Assumptions:
Questions:
Success checks:
Work plan:

## Guardrail Rules

Follow these rules to keep the brief safe and useful:

- Do not invent requirements. If something is missing, ask a question or mark an assumption.
- Preserve user priorities and wording when possible; only rewrite to remove ambiguity.
- If the prompt contains conflicts, surface them explicitly under Questions.
- If a request implies data loss (e.g., wipe DB), put it in Guardrails and ask for confirmation if not explicit.
- Keep it IDE-agnostic (works for Cursor, Claude, Antigravity, etc.).

## Examples

Example A (conflicting model request):
Input: "honestly if chatgpt is working and sonnet keeps giving issues then get rid of it"
Output:
Intent: Remove the failing model integration if ChatGPT is stable.
Scope: In: Sonnet integration removal and related cleanup. Out: new model integrations.
Deliverables: Remove Sonnet provider and references; update config and docs if needed.
Guardrails: Confirm removal does not break core flows; keep ChatGPT intact.
Assumptions: "Sonnet keeps giving issues" refers to runtime errors in current build.
Questions: Which files define model providers and which environment(s) are affected?
Success checks: Build passes; no Sonnet references remain.
Work plan: Identify Sonnet entry points; remove and refactor; update docs; run build.

Example B (build errors + git sync):
Input: "MAKE SURE WE ARE FULLY SYNCED WITH GIT... ALSO GIT HAS ANOTHER BRANCH..."
Output:
Intent: Ensure repo is clean, synced, and using a single active branch.
Scope: In: git status, branch cleanup, docs update location. Out: feature work.
Deliverables: Clean working tree; one active branch; docs published or placed in shared location.
Guardrails: Do not delete branches without confirmation.
Assumptions: "Public" means accessible to all IDEs via the shared repo.
Questions: Which branch is intended to be the primary? Where should docs live?
Success checks: git status clean; single active branch; docs accessible.
Work plan: Check status/branches; resolve extra branch; sync; update docs.
