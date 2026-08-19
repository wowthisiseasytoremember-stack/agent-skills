---
name: architect-foundations-master
description: Master orchestrator for core infrastructure, design systems, and project scaffolding. Use when the user asks to start a new project, refactor core branding, or sync design tokens. This skill coordinates sub-skills for scaffolding, branding, and design-to-code syncing.
---

# Architect Foundations Master

## Overview
This is the master orchestrator for the Architect Foundations squad. It is specialized in building the "bones" of a project, including initial scaffolding, design system alignment, and cross-IDE rule synchronization.

## Core Capabilities
When triggered, this skill will analyze the request and activate the appropriate sub-skills:

1.  **Project Initialization:**
    *   `project-scaffolder`: Initializing new projects with "AI-First" foundation and bridge files.
    *   `architectural-planner`: Scoping new features and locking down constraints before coding.
    *   `granular-shipping-roadmap`: Auditing TODOs and MVP states to build a detailed roadmap.

2.  **Design System & Identity:**
    *   `design-token-compiler`: Syncing JSON tokens with SwiftUI/CSS extensions.
    *   `branding-refactor`: Auditing and refactoring legacy project names (e.g., iFlip to FlipScale).
    *   `museum-placard-ui`: Implementing clean, descriptive UI components.

## Inline Formats

These outputs are produced directly by this master (no separate skill needed):

### Design-to-Engineering Handoff Checklist
When given a design mockup or description, validate completeness before coding starts:
- States (empty, loading, error, success).
- Edge cases (long text, mobile responsiveness, dark mode).
- Interactions (click, hover, scroll).
- Accessibility hints (keyboard nav, screen readers).

Return: 'Ready to hand to eng' or 'Design needs 1 more pass'.

## Workflow
1.  **Understand Foundation:** Determine if the request is for a new project, a core refactor, or a design system update.
2.  **Select Sub-Skills:** Choose relevant sub-skills to run in parallel.
3.  **Ensure Consistency:** Verify that all changes align with the project's canonical mandates (GEMINI.md).
