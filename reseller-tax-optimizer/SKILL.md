---
name: reseller-tax-optimizer
description: Professional-grade tax-loss harvesting and liquidation strategy for resellers. Use when identifying "stale" inventory, calculating tax benefits of losses, or designing liquidation pricing models to offset capital gains.
---

# Reseller Tax Optimizer

## Overview
This skill implements high-fidelity tax-loss harvesting (TLH) logic derived from institutional wealth management patterns. It enables resellers to strategically liquidate aging inventory ("Death Piles") at a loss to optimize their net tax position and reclaim trapped capital.

## Workflow: Tax-Loss Harvest Audit
1. **Inventory Scan**: Scan the `InventoryItem` database for items with `itemStatus == .listed` and `purchaseDate` older than 180 days.
2. **Cost-Market Basis Check**: Compare the original `purchasePrice` (Cost Basis) with the current `estimatedMarketValue`.
3. **Loss Identification**: Calculate potential capital loss (`Cost Basis - Liquidation Price`).
4. **Tax Benefit Calculation**: Apply the user's effective tax rate to the loss to show the "Net Tax Shield" value.
5. **Liquidation Suggestion**: Recommend a "Burn Price" (Tier 2/3) to trigger the loss and exit the position.

## Guidelines
- **Prioritize "Unlisted" Items**: Items in the "Death Pile" (>30 days unlisted) are primary candidates for immediate listing or donation.
- **Strategic Loss**: A $10 loss on a stale item can offset a $10 gain on a high-velocity item, resulting in $0 net tax liability for that pair.
- **Donation vs. Sale**: If the tax benefit of a donation (`FMV * Tax Rate`) is > `Net Liquidation Proceeds (Price - Fees - Shipping)`, recommend a donation.

## Resources
- **[tlh_logic.md](references/tlh_logic.md)**: Detailed formulas for Net Tax Benefit and Strategic Liquidation Tiers.
