---
name: ledger-logic-auditor
description: Use when building or updating financial math, inventory state machines, or profit calculations to ensure mathematical soundness and audit-readiness
---

# Ledger Logic Auditor

Ensures financial models are mathematically sound, meet regulatory requirements, and pass audit scenarios. Covers profit calculations, tax implications, state transitions, and reconciliation logic.

## Core Financial Rules

### Decimal Precision Always

```swift
// ❌ WRONG: Double loses precision
let profit = Double(cost) - Double(selling)

// ✅ CORRECT: Decimal + explicit rounding
let profit = (Decimal(selling) - Decimal(cost)).rounded(toPlaces: 2)
```

### Marketplace Fees (2026 Standards)

| Platform | Fee | Formula |
|----------|-----|---------|
| eBay | 12.9% | `(sellingPrice * 0.129).rounded(toPlaces: 2)` |
| Poshmark | 20% | `(sellingPrice * 0.20)` |
| Mercari | 10% | `(sellingPrice * 0.10)` |
| Facebook | 0% | No fee |
| Local Cash | 0% | No fee |

**Rule:** Fees deducted BEFORE profit calculation

```swift
let ebayFee = (sellingPrice * Decimal(0.129)).rounded(toPlaces: 2)
let netRevenue = sellingPrice - ebayFee
let profit = netRevenue - cost
```

### Inventory State Machine

```swift
enum InventoryStatus: String, Codable {
    case draft        // Item not yet listed
    case listed       // Active listing
    case sold         // Sold, awaiting removal
    case archived     // Moved to archive, not for sale
    case returned     // Customer return
}

// Valid state transitions
func canTransition(from: InventoryStatus, to: InventoryStatus) -> Bool {
    switch (from, to) {
    case (.draft, .listed), (.draft, .archived):
        return true
    case (.listed, .sold), (.listed, .archived):
        return true
    case (.sold, .archived):
        return true
    case (.archived, _):
        return false  // Terminal state
    default:
        return false
    }
}
```

### Profit Calculation Waterfall

```swift
// Order matters for accuracy and auditability
let profit = netProfit(
    cost: itemCost,
    sellingPrice: listingPrice,
    marketplace: .ebay,
    shipping: shippingCost,
    taxes: taxesPaid
)

func netProfit(
    cost: Decimal,
    sellingPrice: Decimal,
    marketplace: Marketplace,
    shipping: Decimal,
    taxes: Decimal
) -> Decimal {
    let fee = marketplace.fee * sellingPrice
    let revenue = sellingPrice - fee - shipping
    let profit = revenue - cost - taxes

    return profit.rounded(toPlaces: 2)
}
```

## Audit Checklist

Before submitting financial code:

- [ ] All currency is `Decimal`, never `Double`
- [ ] Rounding happens LAST, to 2 decimal places
- [ ] Fees calculated correctly per platform
- [ ] State machine transitions documented
- [ ] No division without zero checks
- [ ] Tax calculations comply with local law
- [ ] Reconciliation logic tested with 1000+ item scenarios
- [ ] Edge cases handled (free items, returns, adjustments)

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Using `Double` for money | ±$0.01 errors | Use `Decimal` |
| Rounding intermediate steps | Compounding errors | Round only at end |
| Fee calc order wrong | Wrong profit | Deduct fees BEFORE cost |
| No zero checks | Crashes on division | Guard against zero |
| State transitions unguarded | Data corruption | Use state machine |

## Reconciliation Logic

When syncing inventory to sales:

```swift
struct ReconciliationResult {
    let matchedItems: [InventoryItem]
    let unmatchedInventory: [InventoryItem]
    let unmatchedSales: [Sale]
    let discrepancies: [Discrepancy]
}

func reconcile(inventory: [InventoryItem], sales: [Sale]) -> ReconciliationResult {
    // Score-based matching, not first-match
    let matches = inventory.map { item in
        let candidates = sales.filter { sale in
            sale.price.distance(to: item.listingPrice) < 0.50
            && sale.date.timeIntervalSince(item.listedDate) < 7 * 86400
        }

        // Take best match by score
        return candidates.max { $0.matchScore > $1.matchScore }
    }

    // Rest is audit trail
    return ReconciliationResult(...)
}
```

## Testing Financial Logic

Every financial function needs these tests:

```swift
func testProfitCalculation_100k_Transactions() {
    // Generate 100k realistic transactions
    let items = generateTestInventory(count: 100_000)

    let total = items.reduce(Decimal(0)) { sum, item in
        sum + calculateProfit(item)
    }

    // Total should not drift by more than $0.01
    XCTAssertEqual(total, expectedTotal, accuracy: 0.01)
}

func testStateTransitions_AllPaths() {
    for from in InventoryStatus.allCases {
        for to in InventoryStatus.allCases {
            let result = canTransition(from: from, to: to)
            XCTAssertEqual(result, expectedTransitions[from, to])
        }
    }
}
```

## Real Audit Scenario

Imagine Apple's review team audits your financial handling:

- "Show us profit for $100 item, $30 cost, eBay sale"
  - Expected: $100 - ($100 × 0.129) - $30 = **$40.71**
  - Your code should match exactly

- "Reconcile 5 items sold and 3 still in inventory"
  - Your reconciliation should show zero discrepancies

- "What happens if an item costs $50 but sells for $49?"
  - Should show -$1.00 loss (no hiding)

## References

- IRS Regulations: Hobby loss rules (Schedule C)
- State Sales Tax: Varies by location
- Platform Fees: Official marketplace docs (eBay, Poshmark, etc.)
- Docs/Roadmap/Phases/PHASE_1_FINANCIAL.md - Full financial phase

