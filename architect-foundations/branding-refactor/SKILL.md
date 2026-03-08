---
name: branding-refactor
description: Audits and refactors legacy project names (e.g., iFlip, FlipScale, Flippd) in the codebase. Helps maintain branding consistency by identifying outdated strings in UI, code, and configurations. Use when the project name has changed or after a merge of legacy work.
---

# Branding Refactor

## Overview

This skill provides a systematic workflow for identifying and replacing outdated branding, project names, and legacy ideas across your entire codebase. It helps ensure that user-facing text and internal identifiers align with your current vision.

## Workflow

### 1. Audit Branding
Use the `audit_branding.cjs` script to find all instances of legacy names across the codebase.

**Action:**
Run `node scripts/audit_branding.cjs` and review the locations of old branding.

### 2. Branding Mapping
Refer to the `branding_history.md` reference to understand what should be replaced and what the target name is.

**Action:**
Read `references/branding_history.md`.

### 3. Refactor Phase
Iterate through the identified files and apply targeted refactoring.

**Action:**
Use `grep_search` to find specific instances and `replace` to update them.

## Guidelines & Best Practices

For a full list of target names and refactor safety rules, see [references/branding_history.md](references/branding_history.md).

### Important Safety Rules:
- **Avoid Refactoring Target Names:** Identifiers like `SmartFlipInventoryAR` are tied to the Xcode project and bundle ID. Changing these may require significant re-configuration in Xcode.
- **Check UI Strings First:** Prioritize fixing "confusing" names in the UI.
- **Case Sensitivity Matters:** Search for uppercase, lowercase, and camel-case variants.

## Example Triggers

- "Help me find all instances of the old name 'Flippd' and replace it with 'iFlip'."
- "I want to audit the codebase for legacy branding like 'FlipScale'."
- "My project has gone through 4 name changes, can you help me clean up the old copy?"
- "Find and replace all the old ideas/names scattered throughout the code."
