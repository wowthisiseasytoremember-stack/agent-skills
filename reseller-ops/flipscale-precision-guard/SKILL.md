---
name: flipscale-precision-guard
description: Enforces "No-Matter-What" architectural invariants: Decimal-only for money, zero SwiftUI in Services, and unified UserTier terminology. Use to fix precision drift and architectural leaks.
---

# FlipScale Precision Guard

The "Enforcer" for FlipScale's technical integrity. This skill ensures that once an architectural decision is made (like using Decimal for all money), it is strictly maintained across the project.

## Invariant 1: Financial Precision (Decimal-Only)
**Requirement**: Every field, variable, or parameter representing money or miles must use `Decimal`.
**Violation**: Use of `Double` or `Float` for currency.
**Impact**: Prevents ±$0.01 drift across thousands of transactions.

## Invariant 2: Service Isolation (Platform Agnostic)
**Requirement**: Files in `Sources/FlipScale/Services/` must not `import SwiftUI`.
**Violation**: UI-framework leak into business logic.
**Impact**: Ensures logic is reusable for WatchOS and Widgets without bloat.

## Invariant 3: Unified Identity (UserTier)
**Requirement**: Use `UserTier` exclusively for adaptive UI logic.
**Violation**: Use of legacy `OperatorLevel` or hard-coded strings.
**Impact**: Maintains a single source of truth for the 4-tier adaptive UX.

---

## Commands & Workflows

### 1. Fix Precision Drift
Auto-migrates `Double` fields to `Decimal` in Models and Services.
- Input: `ARCHITECTURE_AUDIT.md` (Precision section).
- Process: Replace `Double` with `Decimal` and update initializers.

### 2. Purge UI Leaks
Identifies and proposes refactors for Services importing SwiftUI.
- Input: `ARCHITECTURE_AUDIT.md` (Isolation section).
- Process: Moves UI-specific logic (like Toasts or Alerts) to ViewModels.

### 3. Terminology Audit
Ensures all adaptive logic uses the unified `UserTier` enum.

---

## Iron Law of Precision
**Math is absolute.** Never settle for "close enough" in financial software. If it touches a dollar sign, it's a `Decimal`.
