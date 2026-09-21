---
name: verification-gate
description: >-
  Strict verification protocol before completion claims: execute fresh verification commands, inspect exit codes and outputs, forbid unverified assertions, and emit structured evidence receipts.
---

# Verification Gate

**The Iron Law:** `NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE`

Never claim a task, fix, test, or build is complete, passing, or working without executing the concrete verification command in the current turn and inspecting its raw output.

## The 5-Step Verification Process

Before asserting status or declaring a task complete:

1. **IDENTIFY:** Determine the exact command(s) that prove the implementation or fix works (e.g., `pytest`, `npm test`, `cargo test`, linter, compiler).
2. **RUN:** Execute the complete verification command freshly in the target environment.
3. **READ:** Read the full stdout/stderr, inspect the process exit code, and verify 0 failures and 0 unhandled errors.
4. **VERIFY:** Confirm the output matches expected behavior. If failures exist, report the actual failure output immediately.
5. **CLAIM WITH EVIDENCE:** State completion only alongside the exact command executed, exit code, and quantitative test summary.

## Common Anti-Patterns to Reject

| Unacceptable Claim | Required Evidence |
|---|---|
| "Tests should pass now" | Fresh test run output showing 0 failures |
| "Linter passed so code is correct" | Compiler / test suite execution with 0 errors |
| "Code looks clean / complete" | Explicit execution proof and status check |
| "Agent reported success" | Independent verification of diff and test results |
| "Regression fixed" | Red-to-green verification cycle (test fails before, passes after) |

## Receipt Requirement
When closing an issue or reporting task completion, include a structured verification receipt containing:
- Base commit SHA and active HEAD commit SHA.
- Commands executed and their exit codes.
- Number of tests passed, failed, and skipped.
- Explicit list of files modified and verification status.
