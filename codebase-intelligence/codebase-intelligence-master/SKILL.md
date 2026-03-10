---
name: codebase-intelligence-master
description: Master orchestrator for codebase analysis, architectural mapping, and deep refactoring. Use when the user asks to understand a complex system, find a root cause, or plan a major refactor. This skill coordinates sub-skills for architecture exploration, tech debt ROI, and automated x-rays.
---

# Codebase Intelligence Master

## Overview
This is the master orchestrator for the Codebase Intelligence squad. It is specialized in mapping, analyzing, and optimizing entire codebases. It uses `project-xray` as its primary diagnostic tool and then delegates specific fixes or refactors to sub-skills.

## Core Capabilities
When triggered, this skill will analyze the codebase or request and activate the appropriate sub-skills:

1.  **Architecture & Mapping:**
    *   `project-xray`: The primary diagnostic for mapping application flow and identifying health issues.
    *   `architecture-explainer`: Visual, no-jargon diagrams and executive summaries.
    *   `codebase-index-architect`: Indexing and mapping the codebase for LLM-optimized search.
    *   `codebase-review-matrix`: Evaluating file-level I/O and architectural alignment.

2.  **Refactoring & Optimization:**
    *   `monolith-refactor-planner`: Scans for large monolithic files and plans their deconstruction.
    *   `tech-debt-inventory-roi`: Ranks debt by impact and payoff ROI.
    *   `xray-performance-optimizer`: Detects and resolves performance bottlenecks.

3.  **Specialized Validation:**
    *   `xray-logic-validator`: Audits business logic and state transition gaps.
    *   `xray-ux-refiner`: Audits UI edge cases, loading states, and layout shifts.
    *   `xray-silent-error-sleuth`: Identifies and fixes silent errors and unhandled rejections.

## Workflow
1.  **Diagnostic Phase:** Always run `project-xray` first to understand the current state.
2.  **Selection Phase:** Choose the specialized sub-skills needed for the specific refactor or fix.
3.  **Execution Phase:** Run selected skills and synthesize a master plan or fix.
