---
name: project-scaffolder
description: Automates the initialization of new software projects with a standardized "AI-First" foundation. Use when starting a new project to generate GEMINI.md mandates, setup standard configs, and create "bridge" files (CLAUDE.md, .cursorrules) that unify AI instructions across all IDEs.
---

# Project Scaffolder

## Overview
The Project Scaffolder ensures every new project starts with a canonical set of rules and architectural mandates. It centralizes all AI-specific instructions into a single `GEMINI.md` file and creates "Bridge Files" for other AI IDEs (Claude Dev, Cursor, Windsurf) that redirect them to this source of truth.

## Core Capabilities

### 1. AI Mandate Initialization
Generates a `GEMINI.md` file based on a project-specific template. This file acts as the project's constitution, defining:
- Architectural patterns and boundaries
- Coding standards and style requirements
- Security and data handling mandates
- Project-specific context and terminology

### 2. The AI Bridge System
Automatically generates lightweight "Bridge Files" for other AI-powered IDEs. These files contain a single directive: **"For all project rules, architectural mandates, and coding standards, refer to GEMINI.md."**

Generated bridge files include:
- `CLAUDE.md` (for Claude Dev / Cline)
- `.cursorrules` (for Cursor)
- `.windsurfrules` (for Windsurf)
- `CODEX.md` (for Codex-based tools)
- `ANTIGRAVITY.md` (for Antigravity environments)

### 3. Structural Scaffolding
Initializes the basic project structure based on the chosen stack (e.g., React, Node, Swift, Go):
- Runs environment-specific init commands (e.g., `npm init -y`, `go mod init`).
- Sets up `.gitignore`, `.env.example`, and a standardized `README.md`.
- Configures `.editorconfig` or IDE-specific settings for consistency.

## Usage

### Starting a New Project
When a user asks to "start a new project" or "scaffold a project":
1. Identify the project name and desired tech stack.
2. Run `node scripts/scaffold.cjs` with the project details.
3. Present the generated structure and the unified `GEMINI.md` for initial review.

## Resource Map

### scripts/
- `scaffold.cjs`: The primary orchestration script for creating directories and injecting templates.

### assets/
- `GEMINI.md.template`: The foundational mandate file.
- `bridge/`: Contains templates for `CLAUDE.md`, `.cursorrules`, etc., that point to `GEMINI.md`.
- `config/`: Standard `.gitignore`, `.editorconfig`, and `README.md` templates.
