---
name: iflip-hustle-design
description: Implements the 'Serious Side Hustle' tier UI/UX logic for iFlip. Use when the user wants to scaffold or refine the high-fidelity 'Hustle HUD', 'Profit Calc' swiper, or 'Potential Return' slider, ensuring they are correctly wired to the ProfitCalculatorService.
---

# iFlip Hustle Design Skill

This skill governs the implementation of the "Serious Side Hustle" (Tier 2) visual identity. It bridges the gap between high-fidelity image mockups and functional SwiftUI code.

## 🏗️ Core Components

### 1. The Dopamine HUD (Home Screen Hero)
**Logic:**
- **Current Trip ROI:** High-impact metric box showing `%` ROI + `$ Potential Profit` (projected gains from active items).
- **Weekend Sourcing Trip Recovery:** Visual ring graph (e.g., 80%) answering "Did I pay for this trip yet?". Shows `$ Recovered` vs `$ Spent`.
- **Scan-Ready Performance Cards:** Color-coded for quick interpretation:
  - **Neutral (Blue):** Total Sourced items.
  - **Warning (Red):** Fees Paid (Total deductions).
  - **Success (Green):** **Pure Profit** (Total Net).
- **Profit Momentum:** 7-day bar chart (M-S) showing performance trajectory.

### 2. The Win Ritual & Momentum Engine (Retention & Celebration)
**Logic:**
- **Audio/Haptic Rituals:** Triggering `coin_drop.wav` (Common) or `legendary_win.wav` (Unicorn) and Taptic Engine feedback during "Sold" status changes.
- **Victory Pop-ups:** High-impact overlays for "Unicorn Flips" (>1000% ROI) using `DesignSystem.Colors.forRarity` for glowing halo effects.
- **Momentum Nudges:** Dynamic, probability-weighted strings (from `DynamicCopy.json`) that appear when users are "this close" to paying off a trip or hitting a goal.
- **Psychological Goal:** Create a "locked-in" loop where logging a sale provides a sensory reward (sound, light, haptics) that motivates the next sourcing trip.

### 3. Marketplace Swipe Calculator
**Logic:**
- Data Source: `ResalePlatform.allCases`
- Math: `ProfitCalculatorService.netProfit` (recalculated per platform)
- Gesture: `DragGesture` with spring animations for the Tinder-style stack.

### 4. Potential Return Slider
**Logic:**
- Value: Normalized `Double` (0.0 to 1.0).
- Visual: LinearGradient (Cyan -> Blue -> Purple) with a glowing shadow.
- Math: Used as a multiplier or "Confidence Score" for expected sale price.

## 🎨 Visual Invariants
- **Background:** Solid `#0A0A0A`.
- **Material:** `.ultraThinMaterial` with a `1px` white opacity border.
- **Typography:**
  - Headers: `DesignSystem.Typography.header` (Clash Display).
  - Data: `DesignSystem.Typography.number` (Satoshi).

## 🛠️ Implementation Workflow

1. **Scaffold View:** Use the normalized `#0A0A0A` template.
2. **Wire Math:** Connect `ProfitCalculatorService` to the inputs.
3. **Loop Platforms:** Iterate through `ResalePlatform` to generate the swipable `MarketplaceCard` stack.
4. **Apply Glows:** Use `.shadow(color: .emerald.opacity(0.4), radius: 12)` for profit numbers.

## 🖼️ Reference Assets
See `Docs/Design/Inspiration/` for the baseline images:
- `Gemini_AlmostPerfect_V1.png`
- `Workflow_AI_Scanner_SideBySide.png`
