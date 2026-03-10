---
name: reseller-ops-master
description: Master orchestrator for FlipScale financial engine and platform-specific tools. Use when the user asks for profit analysis, tax-loss harvesting, or eBay listing strategies. This skill coordinates sub-skills for cash flow, unit economics, and platform-specific logic.
---

# Reseller Ops Master

## Overview
This is the master orchestrator for the Reseller Ops squad. It is specialized in the business logic of reselling, including financial monitoring, platform fee analysis, and inventory valuation.

## Core Capabilities
When triggered, this skill will analyze the request and activate the appropriate sub-skills:

1.  **Financial Monitoring & Strategy:**
    *   `reseller-cashflow-monitor`: 3-statement financial monitoring for reseller inventory.
    *   `reseller-tax-optimizer`: Tax-loss harvesting and liquidation strategies.
    *   `reseller-unit-economics`: Calculating Sell-Through Rate (STR) and margins.
    *   `ledger-logic-auditor`: Auditing financial logic and P&L calculations.

2.  **Platform & Listing Tools:**
    *   `ebay-csv-formatter`: Generating and processing eBay File Exchange CSVs.
    *   `ebay-family-friendly-replier`: Crafting friendly, problem-solving customer replies.
    *   `flipscale-platform-intelligence`: Analyzing marketplace fee structures and comparison logic.
    *   `market-intel-researcher`: Verifying trends and platform fee updates.

3.  **Behavioral & Logic Design:**
    *   `flipscale-behavioral-planner`: Planning "Magic" engagement moments and triggers.
    *   `behavioral-loop-architect`: Gamification and the psychology of engagement.
    *   `flipscale-logic-blueprinter`: Storyboarding complex math and sourcing flows.
    *   `flipscale-precision-guard`: Enforcing architectural invariants (Decimal for money).

## Workflow
1.  **Identify Domain:** Determine if the request is Financial, Platform-specific, or Behavioral.
2.  **Select Sub-Skills:** Choose relevant sub-skills to run in parallel.
3.  **Synthesize Logic:** Ensure all financial calculations and platform interactions are aligned.
