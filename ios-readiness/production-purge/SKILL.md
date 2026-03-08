---
name: production-purge
description: Audits and cleans up an iOS project for production/App Store submission. Identifies and moves non-essential files (docs, history, scripts, etc.) into an archive folder to ensure a "squeaky clean" project structure. Use when preparing for a final build or submission.
---

# Production Purge

## Overview

This skill ensures your iOS project follows App Store submission best practices by removing "clutter" from the primary project directory. It identifies internal notes, development scripts, and AI tool history that should not be included in a final submission to Apple.

## Workflow

### 1. Audit Phase
Use the `audit_project.cjs` script to identify files that are typically excluded from production.

**Action:**
Run `node scripts/audit_project.cjs` and review the list of identified items.

### 2. Archive Phase
Review the audit results and move the non-essential items into a dedicated archive directory (e.g., `_SubmissionArchive/`).

**Action:**
Run `node scripts/archive_files.cjs [path1] [path2] ...` with the items you wish to move.

### 3. Cleanup Phase
Verify the final root directory structure. Essential files like `README.md`, `CLAUDE.md`, and the main project folder should remain, while all "noise" is consolidated.

## Guidelines & Best Practices

For a detailed list of what should be excluded and how to structure your project, see [references/exclusion_rules.md](references/exclusion_rules.md).

### Key Rules:
- **No Internal Docs**: Move roadmaps, todos, and internal audits to the archive.
- **No AI History**: Move `.aider` history and other agent logs.
- **No Local Scripts**: Move `.sh`, `.py`, and other development-only automation scripts.
- **No Large Archives**: Remove unused zip files or large temporary assets.

## Example Triggers

- "Help me clean up the project for Apple submission."
- "Prepare my app for a final production build."
- "Audit the project folders for any non-essential files."
- "Move all my internal notes and scripts into an archive folder."
