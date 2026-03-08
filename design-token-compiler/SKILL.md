---
name: design-token-compiler
description: Translates JSON design tokens into SwiftUI code. Use when updating colors, typography, or spacing in the Design System, and when synchronizing brand-colors.json with Swift extensions.
---

# Design Token Compiler

You are a bridge between Design and Engineering.

## Core Mandates

### 1. Token Source of Truth
- The files `Resources/Data/brand-colors.json` and `typography.json` are the sources of truth.
- Do not define colors directly in SwiftUI Views.

### 2. Code Generation
- Generate SwiftUI extensions like `extension Color { static let brandPrimary = Color("...") }`.
- Ensure dark mode support is handled via Asset Catalogs or semantic token mapping.

### 3. Component Hierarchy
- Follow the "Tier System":
  - **Tier 1 (Tokens)**: Colors, Fonts, Spacing.
  - **Tier 2 (Atoms)**: Buttons, Labels.
  - **Tier 3 (Molecules)**: Item Cards, Input Rows.

## Workflow

1. **Update**: When the user changes `brand-colors.json`, offer to regenerate the `DesignSystem/Tokens.swift` file.
2. **Standardization**: When the user asks for a "Blue button," suggest using a Tier 2 component instead of raw styling.
