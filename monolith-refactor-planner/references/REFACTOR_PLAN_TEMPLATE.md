# Refactor Plan: [Target File Name]

## 1. Executive Summary
- **Target File:** `path/to/file`
- **Current Size:** ~X lines
- **Goal:** [Briefly describe the goal, e.g., "Split a 1200-line React component into focused UI, state, and logic modules."]

## 2. Current Responsibilities
[List the distinct jobs the current file is doing. What makes it a monolith?]

## 3. Proposed Architecture
[Describe the new files that will be created and what they will do.]
- `new/path/FileA`: [Responsibility]
- `new/path/FileB`: [Responsibility]

## 4. Impact Analysis & Downstream Effects
[List the files, endpoints, or components that currently rely on the target file.]
- **Dependent Files:** [List from grep search]
- **API/Props Impact:** [Will the interface change? How will we handle it?]
- **Risk Mitigation:** [e.g., "We will update all imports in `src/app` in the same commit to avoid broken builds."]

## 5. Execution Steps
[Provide a step-by-step checklist for executing this refactor safely.]
- [ ] Step 1: Extract Types/Interfaces
- [ ] Step 2: Extract pure logic/utilities
- [ ] Step 3: Extract Sub-Component A
- [ ] Step 4: Extract Sub-Component B
- [ ] Step 5: Update Orchestrator / Main Component
- [ ] Step 6: Update downstream imports
