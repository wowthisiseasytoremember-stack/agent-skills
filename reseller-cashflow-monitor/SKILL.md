---
name: reseller-cashflow-monitor
description: Reseller-specific 3-statement financial monitoring (Cash Flow, P&L, Balance Sheet). Use to calculate the "Gas Tank" (available sourcing cash), the "Scoreboard" (actual net profit), and the "Stockpile Value" (total liquidated net worth).
---

# Reseller Cashflow Monitor

## Overview
This skill translates institutional 3-statement financial modeling (from the Financial Analysis Core plugin) into "Reseller-Speak". It provides a simplified but mathematically rigorous framework for monitoring business health, capital rotation, and re-investment capacity.

## Workflow: Financial Health Audit
1. **The Gas Tank (Cash Flow)**: Check `Cash on Hand` vs. `Pending Liabilities` (Shipping, Fees, Returns). Calculate re-investment capacity.
2. **The Scoreboard (P&L)**: Calculate `Gross Sales - COGS - Marketplace Fees - Shipping = Net Profit`. Audit monthly performance.
3. **The Stockpile Value (Balance Sheet)**: Calculate the current `Asset Value` (Cash + Inventory) minus `Liabilities`.

## Guidelines
- **Always Use Reseller Language**: Use "Gas Tank" for Cash Flow, "Scoreboard" for P&L, and "Stockpile Value" for Balance Sheet in user-facing interactions.
- **Identify Cash Crunches**: Alert the user if the "Gas Tank" is too low to support current sourcing habits.
- **Audit COGS Accuracy**: Ensure the "Scoreboard" uses the exact purchase price from `SourcingEvent` or `InventoryItem` records.

## Resources
- **[cashflow_logic.md](references/cashflow_logic.md)**: Detailed Reseller-Speak formulas and definitions.
