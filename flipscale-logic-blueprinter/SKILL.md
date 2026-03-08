---
name: flipscale-logic-blueprinter
description: Storyboards and flowcharts complex logic (Math, Sourcing, Liquidation). Use to brainstorm and "whiteboard" the logic under the hood before committing to code.
---

# FlipScale Logic Blueprinter

The "Whiteboard" for FlipScale development. This skill transforms abstract requirements into visual Markdown flowcharts and logical maps so we can storyboard the "Brain" of the app.

## Core Workflows

### 1. The Math Waterfall Storyboard
Generates a step-by-step breakdown of how a single sale is processed.
**Output**: Flowchart showing Sale Price -> Platform Fee -> Shipping Gap -> Taxes -> Net Profit.

### 2. Sourcing HUD Storyboard
Maps the high-speed entry logic.
**Output**: Sequence diagram showing Photo Capture -> Category Guess -> Cost Entry -> ROI Projection.

### 3. Trip Recovery Blueprint
Defines exactly how we calculate when a sourcing trip "is paid for."
**Output**: Logical map showing Total Trip Cost vs. Cumulative Sales Profit.

---

## Storyboarding Template
When brainstorming a new feature, use this structure:
1.  **The User Goal**: What is the lady thirifting once a month trying to see?
2.  **The Logical Path**: A Mermaid-style flowchart of the decisions.
3.  **The Reward Trigger**: Where does the "Magic" happen in this logic?
4.  **The Decision Point**: What options do we need to provide to the user?

---

## Iron Law of Storyboarding
**See it before you build it.** If we can't flowchart the logic, we don't understand the brain. Use this skill to ask "What if...?" and "How does...?" before locking down decisions.
