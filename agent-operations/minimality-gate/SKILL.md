---
name: minimality-gate
description: >-
  Enforces the 7-step minimality decision ladder (YAGNI, codebase reuse, stdlib, native platform, approved dependencies, one-liners, minimal diffs) while strictly preserving security, input validation, error handling, and rollback observability.
---

# Minimality Gate

This skill enforces architectural minimality and YAGNI (You Aren't Gonna Need It) principles. The goal is to produce the smallest, cleanest, and most maintainable diff that completely satisfies the requirements.

## The 7-Step Decision Ladder

Stop at the first rung that completely solves the problem:

1. **Does this need to exist at all? (YAGNI)**
   - Reject speculative features, premature abstractions, and unused configuration hooks.
   - If a requirement is unnecessary or speculative, state why and omit it.

2. **Already in this codebase?**
   - Reuse existing utilities, helpers, types, and architectural patterns.
   - Search the repository before implementing duplicate logic.

3. **Standard library solves it?**
   - Prefer language/runtime standard library modules over third-party packages or hand-rolled helpers.

4. **Native platform feature covers it?**
   - Prefer built-in OS, database, browser, or framework capabilities (e.g., DB constraints, native CSS, platform CLI tools).

5. **Already-installed dependency covers it?**
   - Reuse dependencies already declared and verified in the project lockfile. Never add new dependencies when existing tools or minimal stdlib code suffice.

6. **Can it be a concise one-liner?**
   - Favor straightforward, idiomatic one-line expressions over multi-layer abstractions.

7. **Minimum working implementation**
   - Write the smallest, most direct implementation that works and includes verifiable tests.

## Bug Fix Principle: Root Cause Over Symptom Patching
- Trace callers and find where data originates before patching.
- Fix the issue at the common root rather than scattering defensive checks across downstream callers.

## Invariants That Must NEVER Be Simplified Away
- Input validation at trust boundaries (APIs, CLI arguments, file parsers).
- Error handling that prevents data corruption, state loss, or silent failures.
- Security controls, authorization checks, and secret handling.
- Basic accessibility and user safety requirements.
- Observability, rollback mechanisms, and test evidence.
