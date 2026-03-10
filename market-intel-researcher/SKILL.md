---
name: market-intel-researcher
description: Use when researching marketplace data, competitor pricing, platform fee updates, or verifying real-world marketplace information for FlipScale features
---

# Market Intel Researcher

Researches real-world marketplace data for FlipScale: current eBay/Poshmark/Mercari fees, pricing trends, competitor features, platform policy changes.

## Current Marketplace Data (2026)

### Platform Fees (Verified)

| Platform | Fee % | Shipping Cost | Final Price % | Notes |
|----------|-------|----------------|---------------|-------|
| **eBay** | 12.9% | Variable | ~13% off | Includes final value + payment fees |
| **Poshmark** | 20% | Flat $2.95 | ~22% off | Flat rate shipping deduction |
| **Mercari** | 10% | Variable | ~10-12% off | Varies by shipping method |
| **Facebook Marketplace** | 0% | Buyer pays | 0% | No fees, local pickup |
| **Cash/Local** | 0% | N/A | 0% | No fees or platform |

**Update cadence:** Check quarterly (platforms change fees seasonally)

### Competitor Analysis (2026)

**FlippD (Main Competitor)**
- MRR: ~$24K
- Users: ~800-1000
- Features:
  - Basic inventory tracking
  - Storage location management
  - Profit calculator
  - ❌ No tier system
  - ❌ No Apple Watch
  - ❌ No AI vision

**Differentiators:**
- ✅ Tier-adaptive UX
- ✅ AI product recognition
- ✅ Apple Watch companion
- ✅ Real-time pricing
- ✅ Predictive liquidation

### Platform Policy Tracking

Track these for changes:

```swift
struct MarketplacePolicy {
    let platform: String
    let policyName: String
    let currentValue: String
    let effectiveDate: Date
    let nextReview: Date
}

// Examples to monitor:
let policies: [MarketplacePolicy] = [
    MarketplacePolicy(
        platform: "eBay",
        policyName: "Final Value Fee",
        currentValue: "12.9% + $0.30",
        effectiveDate: Date(timeIntervalSince1970: 1704067200),  // Jan 2024
        nextReview: Date(timeIntervalSinceNow: 90 * 86400)
    ),

    MarketplacePolicy(
        platform: "Poshmark",
        policyName: "Commission",
        currentValue: "20% flat",
        effectiveDate: Date(timeIntervalSince1970: 1577836800),  // Jan 2020
        nextReview: Date(timeIntervalSinceNow: 90 * 86400)
    )
]
```

## Research Workflow

### 1. Quarterly Fee Audit

Every 3 months, verify current fees:

```swift
func auditMarketplaceFees() {
    let platforms = ["eBay", "Poshmark", "Mercari", "Facebook"]

    for platform in platforms {
        // Visit official platform fee page
        // Document current fees
        // Update AppConfiguration if changed
        // Notify users if significant change

        let oldFee = AppConfiguration.marketplaceFee(for: platform)
        let newFee = fetchCurrentFee(platform)

        if oldFee != newFee {
            // Update in-app
            AppConfiguration.updateMarketplaceFee(platform, newFee)

            // Notify affected users
            notifyUsersOfFeeChange(platform, from: oldFee, to: newFee)
        }
    }
}
```

### 2. Competitive Feature Tracking

Monitor what competitors release:

```swift
struct CompetitorFeature {
    let competitor: String
    let feature: String
    let releaseDate: Date
    let flipsScaleEquivalent: String?
    let urgency: Priority  // .low, .medium, .high, .critical
}

// Track as competitors add features
let features: [CompetitorFeature] = [
    CompetitorFeature(
        competitor: "FlippD",
        feature: "Apple Watch app",
        releaseDate: Date(timeIntervalSinceNow: -30 * 86400),  // 30 days ago
        flipsScaleEquivalent: "FlipScaleWatch (already done)",
        urgency: .low  // We shipped this first
    ),

    CompetitorFeature(
        competitor: "FlippD",
        feature: "AI item recognition",
        releaseDate: Date(timeIntervalSinceNow: 90 * 86400),  // Expected in 3 months
        flipsScaleEquivalent: "Vision Hub (in progress)",
        urgency: .high  // Need to ship before they do
    )
]
```

### 3. Marketplace Trends Research

Track what's selling, pricing trends:

```swift
struct MarketplaceTrend {
    let category: String
    let trend: String  // "increasing", "stable", "declining"
    let averagePrice: Decimal
    let velocity: String  // "fast", "moderate", "slow"
    let seasonality: String
}

// Research: What categories are hot on Poshmark right now?
let trends: [MarketplaceTrend] = [
    MarketplaceTrend(
        category: "Designer handbags",
        trend: "increasing",
        averagePrice: Decimal(200),
        velocity: "fast",
        seasonality: "Year-round"
    ),

    MarketplaceTrend(
        category: "Winter jackets",
        trend: "seasonal",
        averagePrice: Decimal(75),
        velocity: "fast",
        seasonality: "Oct-Feb peak"
    )
]
```

## Data Sources

### Official
- eBay Seller Center (fees, policies)
- Poshmark Community (announcements)
- Mercari Help Center (fees)
- Facebook Commerce docs

### Third-Party Aggregators
- Terapeak (eBay trends)
- Depop/Vinted (younger market trends)
- Reddit r/Flipping (community intelligence)
- TikTok Shop (emerging platform)

### Internal Tracking
- FlipScale user data (what's selling)
- User feedback (pain points)
- Usage metrics (feature adoption)

## Implementation: Fee Updates

When platform fees change:

```swift
enum AppConfigurationUpdate {
    case marketplaceFeesChanged(platform: String, oldFee: Decimal, newFee: Decimal)
    case competitorFeatureReleased(feature: String)
    case marketplacePolicyChanged(policy: String, description: String)
}

// Update AppConfiguration.swift
struct AppConfiguration {
    static let marketplaceFees: [String: Decimal] = [
        "eBay": Decimal(0.129) + Decimal(0.30),  // 12.9% + $0.30
        "Poshmark": Decimal(0.20),               // 20%
        "Mercari": Decimal(0.10),                // 10%
        "Facebook": Decimal(0),                  // Free
    ]
}

// Test that fees are current
func testMarketplaceFeesAreCurrent() {
    let ebayFeeFromWeb = fetchFromEBayOfficial()
    let ebayFeeInApp = AppConfiguration.marketplaceFees["eBay"]

    XCertAssertEqual(
        ebayFeeFromWeb,
        ebayFeeInApp,
        accuracy: 0.001
    )
}
```

## Red Flags to Watch

| Red Flag | Action |
|----------|--------|
| Platform raises fees >1% | Update calculator, notify users |
| Competitor ships major feature | Assess urgency for similar feature |
| New marketplace launches | Research fit for FlipScale users |
| Policy change (returns, fees) | Update help docs |
| Seasonal trend shift | Alert users to hot categories |

## Research Schedule

- **Weekly:** Monitor Reddit r/Flipping, TikTok Shop
- **Monthly:** Check competitor app updates
- **Quarterly:** Audit all marketplace fees & policies
- **Yearly:** Deep competitive analysis, market report

## Integrating Research into Product

```swift
// Example: Use market research to update recommendations

func getListingRecommendation(for item: InventoryItem) -> ListingRecommendation {
    let trend = marketTrend(for: item.category)
    let competition = similarListings(for: item)

    // Use trend velocity to recommend platform
    if trend.velocity == "fast" && competition.low {
        return ListingRecommendation(
            recommendedPlatform: .poshmark,  // Fast sales = 20% fee OK
            recommendedPrice: Decimal(100),
            daysToSellEst: 7,
            reason: "Designer bags selling fast on Poshmark right now"
        )
    } else {
        return ListingRecommendation(
            recommendedPlatform: .ebay,  // Higher competition = lower prices = lower fees
            recommendedPrice: Decimal(85),
            daysToSellEst: 21,
            reason: "High competition on Poshmark, better value on eBay"
        )
    }
}
```

## References

- eBay Seller Center: https://sellercentercommunity.ebay.com
- Poshmark Community: https://posh.mk/community
- Mercari Help: https://help.mercari.com
- Reddit r/Flipping: https://reddit.com/r/Flipping
- Docs/Product/Features/MARKETPLACE_DATA.md

