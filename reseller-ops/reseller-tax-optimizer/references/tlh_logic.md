# Reseller Tax-Loss Harvesting (TLH) Logic

## Objective
To identify inventory items that are "stale" (aging beyond a threshold) and calculate the tax benefit of liquidating them at a loss to offset short-term capital gains from profitable flips.

## Formula: Net Tax Benefit
`Net Tax Benefit = (Cost Basis - Liquidation Price) * Effective Tax Rate`

## Strategic Liquidation Tiers
1. **Tier 1: Breakeven Flush**
   - Target: Items aging 60-90 days.
   - Action: Price at `(Cost + Shipping + Fees)` to recover capital without a tax loss.
2. **Tier 2: Tax-Advantaged Exit**
   - Target: Items aging 120-180 days.
   - Action: Price at `Cost * 0.5`. The resulting loss offsets high-margin wins elsewhere.
3. **Tier 3: The "Donation" Nuclear Option**
   - Target: Items aging 365+ days.
   - Action: Donate. Benefit is `Fair Market Value * Tax Rate`, plus 100% reclamation of storage space.

## Decision Tree
- **Is the item in a "Death Pile"?** (Unlisted > 30 days) -> Priority 1 for listing.
- **Has the item been listed > 180 days?** -> Trigger TLH audit.
- **Is current Market Value < Cost Basis?** -> Immediate TLH candidate.
