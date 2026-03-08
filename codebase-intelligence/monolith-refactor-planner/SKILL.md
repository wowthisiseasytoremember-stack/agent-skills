---
name: monolith-refactor-planner
description: Scans for large monolithic files, generates a structured plan to refactor them into independent components, and analyzes downstream impacts. Use when asked to refactor large files, break down a monolith, or plan component deconstruction.
---

# Monolith Refactor Planner

You are an expert software architect specializing in breaking down large, complex "God files" into modular, independent components. Your goal is to systematically document a safe, step-by-step refactoring plan while identifying all potential downstream impacts.

## Workflow

### 1. Identify Target Monoliths
If the user hasn't specified a file, look for unusually large files in the codebase (e.g., files over 500-1000 lines). You can use shell commands (like `find . -name "*.ts*" -type f -exec wc -l {} + | sort -rn | head -n 10`) or codebase intuition to find candidates.

### 2. Analyze Current Responsibilities
Read the target file completely. Map out its current responsibilities:
- State management
- Data fetching / API calls
- UI rendering (for frontend)
- Business logic / utility functions
- Types and interfaces

### 3. Plan the Deconstruction
Propose a new architecture where the monolith is split into independent, focused components. 
- Group related functions, state, and UI together.
- Identify the "glue" or orchestrator component if necessary.

### 4. Impact Analysis
Before finalizing the plan, you MUST determine how this refactor will affect the rest of the system:
- **Dependency Search:** Use `grep_search` to find all files that import from the target monolith.
- **Endpoint/Props Impact:** Identify if breaking the file will change public interfaces, API endpoints, or component props.
- Document these risks and how to mitigate them (e.g., leaving a facade in place during transition).

### 5. Document the Plan
Generate a markdown file documenting the refactoring strategy. 
Use the template provided in `references/REFACTOR_PLAN_TEMPLATE.md` to ensure your output is structured and actionable. Do not start coding the refactor unless the user explicitly tells you to execute the plan.
