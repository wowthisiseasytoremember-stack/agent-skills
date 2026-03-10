---
name: codebase-review-matrix
description: Generates and maintains a high-density `codebase_review_matrix.md`. Maps every file's I/O, Tech/Design/Shipping notes, and evaluates alignment with the app's Vibe, Ethos, and Aesthetic.
---

# Codebase Review Matrix (The "Living Map")

This skill transforms a raw codebase into a structured, human-readable matrix. It is the definitive audit log for technical integrity, design polish, and "Vibe" alignment.

## Core Mandates
1.  **Input/Output Rigor**: Document every file's data contracts (Types, Formats, Protocols) given and accepted.
2.  **Multidimensional Notes**:
    - **Tech Notes**: Logic, performance, and "Broken Windows" (bugs/debt).
    - **Design Notes**: UI/UX polish, animation timing, and layout consistency.
    - **Shipping Notes**: Deployment readiness, env-var dependencies, and production constraints.
3.  **Ethos & Vibe Audit**: Every file must be evaluated against the app's **Aesthetic, Goals, Workflows, and Vibe**. If a file is "soul-less" or clunky, it's a violation.
4.  **UTC Synchronization**: All timestamps MUST be in UTC (ISO 8601).

## Mandatory Artifact: `codebase_review_matrix.md`
This file is the "Master Registry" of the project state.

### Table Schema:
| File | Purpose (Plain English) | Inputs (Format/Type) | Outputs (Format/Type) | Tech Notes | Design Notes | Shipping Notes | Ethos/Vibe Match | Last Updated (UTC) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `path/to/file` | What it does for the user. | What it takes in. | What it spits out. | Logic/Bugs. | Aesthetic/UX. | Readiness/Env. | Alignment check. | `YYYY-MM-DD HH:mm:ss` | `[ ]`, `[/]`, `[x]` |

---

## Commands & Workflows

### 1. Initialize Matrix (`init-matrix`)
The "Big Bang" scan. Use this at the start of a project or when taking over a new one.
**Process**:
- Deep scan all source files.
- Infer Purpose, I/O, and Notes using LLM reasoning.
- Perform the first "Vibe Check" against the `GEMINI.md` or `SYSTEM_DOCTRINE.md`.
- Generate the `codebase_review_matrix.md` in the root.

### 2. Update File (`update-matrix <file_path>`)
Run this after any edit to a file.
**Process**:
- Re-analyze the file's I/O and Logic.
- Update Tech/Design/Shipping notes based on the latest changes.
- Re-evaluate the Vibe Match (did the change break the aesthetic?).
- Refresh the UTC timestamp.

### 3. Vibe Audit (`audit-vibe`)
A specialized scan that ignores code logic and focuses strictly on **Ethos, Aesthetic, and UX Flow**.
**Process**:
- Review all files marked `[x]` (Reviewed).
- Ensure consistency in naming, typography, and "feel."
- Identify "Vibe Debt" (functional but ugly/clunky code).

---

## Iron Law of the Matrix
**If it isn't documented, it's debt.** The matrix is the only source of truth for "How this app works" and "Why it feels this way." All UTC timestamps are final.
