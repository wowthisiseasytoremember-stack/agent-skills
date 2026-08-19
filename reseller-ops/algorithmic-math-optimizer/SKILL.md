---
name: algorithmic-math-optimizer
description: Use when optimizing ROI calculations, pricing algorithms, inventory valuation, or complex profit formulas to maximize mathematical efficiency and accuracy
---

# Algorithmic Math Optimizer

Optimizes FlipScale's mathematical engines: ROI calculations, pricing strategies, inventory valuation algorithms, and profit projections. Focuses on efficiency and precision.

## Core Optimization Problems

### 1. ROI Calculation (Most Used)

**Standard Formula:**
```swift
func calculateROI(cost: Decimal, revenue: Decimal, fees: Decimal) -> Decimal {
    let netProfit = revenue - cost - fees
    let roi = (netProfit / cost) * 100
    return roi.rounded(toPlaces: 2)
}
```

**Optimized (handles edge cases):**
```swift
func calculateROI(cost: Decimal, revenue: Decimal, fees: Decimal) -> Decimal {
    guard cost > 0 else { return 0 }  // No division by zero

    let netProfit = revenue - cost - fees

    // If item is a loss, show negative ROI
    let roi = (netProfit / cost) * 100
    return roi.rounded(toPlaces: 2)
}

// Test cases
XCertAssertEqual(calculateROI(cost: 100, revenue: 150, fees: 10), Decimal(40))    // 40% ROI
XCertAssertEqual(calculateROI(cost: 100, revenue: 80, fees: 5), Decimal(-25))     // -25% loss
```

### 2. Break-Even Price Calculation

**Given cost + fees, what selling price breaks even?**

```swift
func breakEvenPrice(cost: Decimal, platformFeePercent: Decimal) -> Decimal {
    // sellingPrice - (sellingPrice * feePercent) = cost
    // sellingPrice * (1 - feePercent) = cost
    // sellingPrice = cost / (1 - feePercent)

    let oneMinusFee = 1 - (platformFeePercent / 100)
    guard oneMinusFee > 0 else { return cost }

    return (cost / oneMinusFee).rounded(toPlaces: 2)
}

// Example: Item costs $100, eBay fee is 12.9%
// Break-even: $100 / (1 - 0.129) = $114.82
let breakEven = breakEvenPrice(cost: 100, platformFeePercent: 12.9)
XCertAssertEqual(breakEven, Decimal(114.82))
```

### 3. Inventory Valuation (Aging Inventory)

**Revalue inventory based on how long it's been listed:**

```swift
func ageAdjustedValue(
    originalValue: Decimal,
    daysSinceListed: Int,
    depreciationRatePercent: Decimal = Decimal(2)  // 2% per month
) -> Decimal {
    let months = Decimal(daysSinceListed) / 30
    let monthlyDecay = depreciationRatePercent / 100

    // value = original * (1 - decay)^months
    let adjustedValue = originalValue * pow(1 - monthlyDecay, months)

    return max(adjustedValue, Decimal(0)).rounded(toPlaces: 2)
}

// Item valued at $100, listed for 90 days (3 months), 2% monthly decay
// Value: $100 * (0.98)^3 = $94.12
let adjusted = ageAdjustedValue(originalValue: 100, daysSinceListed: 90)
```

### 4. Optimal Pricing (Demand-Based)

**Price adjustment based on listing age and similar items:**

```swift
func optimalPrice(
    baseCost: Decimal,
    desiredROI: Decimal,
    similarListingCount: Int,
    daysSinceListed: Int
) -> Decimal {
    // Base: cost + (cost * desired ROI%)
    let targetPrice = baseCost * (1 + desiredROI / 100)

    // Demand adjustment: More competition = lower price
    let competitionFactor = Decimal(max(0.9, 1.0 - (Decimal(similarListingCount) * 0.01)))

    // Age adjustment: Older listing = lower price to move inventory
    let ageMonths = Decimal(daysSinceListed) / 30
    let ageFactor = Decimal(max(0.85, 1.0 - (ageMonths * 0.05)))

    let adjustedPrice = targetPrice * competitionFactor * ageFactor

    return max(baseCost * Decimal(1.1), adjustedPrice).rounded(toPlaces: 2)
}
```

### 5. Profit Projection (Time-Based)

**Estimate when inventory will sell out and profit materialize:**

```swift
struct ProfitProjection {
    let estimatedDaysToSellout: Int
    let projectedTotalProfit: Decimal
    let projectedCashOutDate: Date
    let sellThroughRate: Decimal  // % per week
}

func projectProfit(
    inventory: [InventoryItem],
    historicalSellThroughRate: Decimal = Decimal(0.25)  // 25% per week
) -> ProfitProjection {
    var remainingItems = inventory
    var totalProfit = Decimal(0)
    var daysToSellout = 0

    while !remainingItems.isEmpty && daysToSellout < 365 {
        let weekProfit = remainingItems.reduce(Decimal(0)) { sum, item in
            if item.isProbablySoldThisWeek(rate: historicalSellThroughRate) {
                return sum + item.estimatedProfit
            }
            return sum
        }

        totalProfit += weekProfit
        remainingItems.removeAll { $0.isProbablySoldThisWeek(rate: historicalSellThroughRate) }
        daysToSellout += 7
    }

    return ProfitProjection(
        estimatedDaysToSellout: daysToSellout,
        projectedTotalProfit: totalProfit,
        projectedCashOutDate: Date(timeIntervalSinceNow: TimeInterval(daysToSellout * 86400)),
        sellThroughRate: historicalSellThroughRate
    )
}
```

## Performance Optimization

### Batch Calculations (Don't Loop)

```swift
// ❌ SLOW: Loop 10k items
var totalProfit = Decimal(0)
for item in inventory {
    totalProfit += item.calculateProfit()
}

// ✅ FAST: Reduce
let totalProfit = inventory.reduce(Decimal(0)) { sum, item in
    sum + item.calculateProfit()
}

// ✅ FASTER: Use Foundation math (if applicable)
let totalProfit = inventory
    .map { $0.profit }
    .reduce(Decimal(0), +)
```

### Memoization (Cache Results)

```swift
class ProfitCalculator {
    private var profitCache: [Int: Decimal] = [:]

    func cachedProfit(for itemID: Int) -> Decimal {
        if let cached = profitCache[itemID] {
            return cached
        }

        let profit = calculateProfit(itemID: itemID)
        profitCache[itemID] = profit
        return profit
    }

    func clearCache() {
        profitCache.removeAll()
    }
}
```

## Algorithm Complexity (Big-O)

Target complexity for FlipScale:

| Operation | Complexity | Target | Achievable? |
|-----------|-----------|--------|------------|
| Calculate single item profit | O(1) | <1ms | ✅ Yes |
| ROI for 1000 items | O(n) | <50ms | ✅ Yes |
| Inventory reconciliation | O(n²) worst | <200ms | ⚠️ Use scoring |
| Valuation sweep (10k items) | O(n) | <100ms | ✅ Yes |
| Optimal pricing (comparison) | O(n log n) | <500ms | ✅ Yes |

## Testing Math Algorithms

```swift
func testProfitCalculation_StressTest() {
    let items = (0..<10_000).map { i in
        InventoryItem(
            cost: Decimal(Int.random(in: 5...500)),
            sellingPrice: Decimal(Int.random(in: 10...1000))
        )
    }

    let start = Date()
    let totalProfit = items.reduce(Decimal(0)) { $0 + $1.profit }
    let elapsed = Date().timeIntervalSince(start)

    XCertAssertLessThan(elapsed, 0.1)  // Must complete in <100ms
    XCertAssertEqual(totalProfit, expectedTotal, accuracy: 0.01)
}

func testROIAccuracy_PrecisionDrift() {
    // 100k random transactions, total should not drift
    var total = Decimal(0)
    for _ in 0..<100_000 {
        let roi = calculateROI(
            cost: Decimal.random(in: 5...500),
            revenue: Decimal.random(in: 10...1000),
            fees: Decimal.random(in: 0...100)
        )
        total += roi
    }

    // Allow max $0.01 drift across 100k calculations
    XCertAssertEqual(total, expectedTotal, accuracy: 0.01)
}
```

## Real-World Scenario

**User browsing thrift store with FlipScale:**

```swift
// Item is $50 cost
let cost = Decimal(50)

// What should I list it for?
let optimalPrice = optimalPrice(
    baseCost: cost,
    desiredROI: Decimal(50),  // Want 50% ROI
    similarListingCount: 47,  // 47 similar items active
    daysSinceListed: 0        // Just acquired
)
// Returns: $75 (would be $75 for 50% ROI, but competition reduces it)

// Will this be profitable?
let projection = projectProfit(inventory: [item])
// Returns: Est. 21 days to sell, $25 profit by April 15th

// Is it worth the shelf space?
if projection.projectedTotalProfit > Decimal(20) {
    "Yes, list it"
} else {
    "Maybe donate or batch sell"
}
```

## References

- Docs/Development/API_REFERENCE.md - MathEngine details
- Docs/Roadmap/Phases/PHASE_1_FINANCIAL.md - Financial roadmap
- Research: "Dynamic Pricing for Inventory" (academic papers)

