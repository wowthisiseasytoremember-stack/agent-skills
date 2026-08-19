---
title: Apple Design System (Tier-Adaptive)
name: apple-design-system
description: How to implement FlipScale's tier-adaptive design system with Apple HIG compliance
purpose: Guide developers to create consistent, tier-aware UI components using design tokens
keywords:
  - design tokens
  - tier system
  - design system
  - consistency
  - SwiftUI
  - components
  - Apple HIG
  - tier-adaptive
version: 1.0
---

# Apple Design System (Tier-Adaptive)

Implements Apple Human Interface Guidelines (HIG) 2026 with FlipScale's tier-adaptive visual system using design tokens. Enables building consistent UI components across tier 1 (premium), tier 2 (standard), and tier 3 (basic) users.

## Design Token Workflow Overview

Design tokens are reusable atomic design decisions (colors, typography, spacing, shadows, animations) stored in a centralized format and compiled for each user tier. This approach ensures consistency while allowing tier-specific variations.

**Core Workflow:**
1. Define tokens in centralized source (`tokens.json`)
2. Compile tokens for each tier (tier1, tier2, tier3)
3. Import generated token files into components
4. Use tokens exclusively (no magic numbers)
5. Recompile when design decisions change

### Key Principles

1. **Consistency**: Always use tokens; never use magic numbers
2. **Tier Awareness**: Explicitly handle tier differences in component logic
3. **Maintainability**: Centralize tier logic in helpers and reuse across components
4. **Documentation**: Document tier behavior and token usage
5. **Automation**: Use token compilation to stay in sync

## Design Token Categories

| Category | Purpose | Tier Variation | Example |
|----------|---------|-----------------|---------|
| **Color** | Brand colors, semantic colors (success, warning, error) | Tier 1: Full palette; Tier 2: Standard palette; Tier 3: Reduced palette | `colors.primary`, `colors.success` |
| **Typography** | Font families, sizes, weights, line heights | Tier 1: Full range (10-32pt); Tier 2: Core sizes (12-24pt); Tier 3: Essential sizes (14-20pt) | `typography.headline1`, `typography.body` |
| **Spacing** | Padding, margins, gaps (8pt base unit) | Tier 1: 8px increments; Tier 2: 8px increments; Tier 3: 16px increments (fewer options) | `spacing.xs`, `spacing.lg` |
| **Corner Radius** | Border radius values | Tier 1: Flexible (4-16px); Tier 2: Standard (8px); Tier 3: Minimal (4px) | `radius.small`, `radius.large` |
| **Shadow** | Elevation and depth effects | Tier 1: 4 levels; Tier 2: 2 levels; Tier 3: 1 level | `shadow.elevation1`, `shadow.elevation2` |
| **Animation** | Timing functions, durations, curves | Tier 1: Full animations (400ms+); Tier 2: Core animations (300ms); Tier 3: Minimal (100ms) | `animation.standard`, `animation.decelerate` |

## When to Use Design Tokens (vs. Magic Numbers)

| Scenario | CORRECT Token Usage | WRONG Magic Number | Why |
|----------|---------------------|-------------------|-----|
| Setting button background | `colors.primary` | `#007AFF` | Tokens maintain consistency across all tiers; magic numbers break tier treatment |
| Button padding on iPhone | `spacing.md` | `16` | Tokens scale appropriately; magic numbers ignore tier-specific spacing |
| Hero image corner radius | `radius.large` | `CGFloat(16)` | Tokens adapt per tier; hard-coded values prevent tier adaptation |
| Form input border | `colors.border` | `UIColor.gray` | Tokens ensure semantic consistency; magic numbers lack semantic meaning |
| View animation duration | `animation.standard` | `0.3` | Tokens scale; magic numbers bypass tier-specific animation rules |

## Apple HIG 2026 Principles

1. **Clarity** - Information hierarchy is obvious
2. **Deference** - Content takes center stage
3. **Depth** - Visual layers show importance
4. **Accessibility** - WCAG AAA minimum
5. **Performance** - Smooth 60 FPS animations

## Typography System (SF Pro Rounded)

All text uses **SF Pro Rounded** (Apple's friendly, readable font).

| Usage | Size | Weight | Line Height |
|-------|------|--------|------------|
| **Hero (Profit)** | 48pt | Bold | 1.2 |
| **Section Headers** | 20pt | Semibold | 1.3 |
| **Body Text** | 16pt | Regular | 1.5 |
| **Captions** | 12pt | Regular | 1.4 |
| **Buttons** | 16pt | Semibold | 1.0 |

### SwiftUI Implementation

```swift
extension Font {
    static let heroPrice = Font.system(
        size: 48,
        weight: .bold,
        design: .rounded
    )

    static let sectionHeader = Font.system(
        size: 20,
        weight: .semibold,
        design: .rounded
    )

    static let bodyText = Font.system(
        size: 16,
        weight: .regular,
        design: .rounded
    )
}

// Usage
Text("$1,234.00")
    .font(.heroPrice)
    .foregroundColor(.tier1Casual)
```

## Spacing Grid (8pt Base)

All spacing uses multiples of 8pt:

```swift
extension CGFloat {
    static let xs = 4.0      // Minimal (rarely used)
    static let sm = 8.0      // Padding within components
    static let md = 16.0     // Standard padding
    static let lg = 24.0     // Section spacing
    static let xl = 32.0     // Major sections
    static let xxl = 48.0    // Full-screen margins
}

// Usage
VStack(spacing: .md) {
    Text("Dashboard")
    MetricCard()
}
.padding(.lg)
```

## Color System (Tier-Adaptive)

### Tier 1: Casual (Bright)
```swift
extension Color {
    static let tier1Primary = Color(red: 0.298, green: 0.796, blue: 0.298)  // #4CAF50
    static let tier1Secondary = Color(red: 0.533, green: 0.835, blue: 0.533) // #87D887
}
```

### Tier 2: Hustler (Standard)
```swift
extension Color {
    static let tier2Primary = Color(red: 0.180, green: 0.494, blue: 0.196)  // #2E7D32
    static let tier2Secondary = Color(red: 0.302, green: 0.651, blue: 0.314) // #4DA64D
}
```

### Tier 3: Pro (Forest)
```swift
extension Color {
    static let tier3Primary = Color(red: 0.106, green: 0.369, blue: 0.125)   // #1B5E20
    static let tier3Secondary = Color(red: 0.259, green: 0.541, blue: 0.275) // #428F46
}
```

### Tier 4: Enterprise (Dark Teal)
```swift
extension Color {
    static let tier4Primary = Color(red: 0, green: 0.302, blue: 0.251)       // #004D40
    static let tier4Secondary = Color(red: 0.004, green: 0.447, blue: 0.369) // #01725E
}
```

## Tier-Aware Component Example: Card Component

### Understanding Tier Differences

The same component renders differently across tiers while maintaining visual hierarchy:

```swift
struct CardComponent: View {
    let title: String
    let description: String
    let tier: UserTier  // Enum: case tier1, tier2, tier3

    var body: some View {
        VStack(alignment: .leading, spacing: getSpacing()) {
            // Header
            Text(title)
                .font(.system(size: getTypography().headline.size,
                             weight: getTypography().headline.weight))
                .foregroundColor(DesignTokens.Colors.textPrimary)

            // Content
            Text(description)
                .font(.system(size: getTypography().body.size,
                             weight: getTypography().body.weight))
                .foregroundColor(DesignTokens.Colors.textSecondary)
                .lineLimit(getTierLineLimit())

            // Action Button (tier-specific treatment)
            if shouldShowButton() {
                Button("Learn More") {
                    // Action
                }
                .font(.system(size: getTypography().label.size))
                .foregroundColor(DesignTokens.Colors.primary)
            }
        }
        .padding(getPadding())
        .background(DesignTokens.Colors.cardBackground)
        .cornerRadius(DesignTokens.Radius.large)
        .shadow(color: getShadowColor(),
               radius: getShadowRadius(),
               x: getShadowOffsetX(),
               y: getShadowOffsetY())
    }

    // TIER ADAPTATION LOGIC
    private func getSpacing() -> CGFloat {
        switch tier {
        case .tier1: return DesignTokens.Spacing.lg    // 24px
        case .tier2: return DesignTokens.Spacing.md    // 16px
        case .tier3: return DesignTokens.Spacing.md    // 16px
        }
    }

    private func getPadding() -> EdgeInsets {
        switch tier {
        case .tier1:
            return EdgeInsets(top: DesignTokens.Spacing.lg,
                            leading: DesignTokens.Spacing.lg,
                            bottom: DesignTokens.Spacing.lg,
                            trailing: DesignTokens.Spacing.lg)
        case .tier2:
            return EdgeInsets(top: DesignTokens.Spacing.md,
                            leading: DesignTokens.Spacing.md,
                            bottom: DesignTokens.Spacing.md,
                            trailing: DesignTokens.Spacing.md)
        case .tier3:
            return EdgeInsets(top: DesignTokens.Spacing.sm,
                            leading: DesignTokens.Spacing.sm,
                            bottom: DesignTokens.Spacing.sm,
                            trailing: DesignTokens.Spacing.sm)
        }
    }

    private func getTypography() -> (headline: DesignTokens.Typography,
                                    body: DesignTokens.Typography,
                                    label: DesignTokens.Typography) {
        switch tier {
        case .tier1:
            return (headline: DesignTokens.Typography.headline1,
                   body: DesignTokens.Typography.body,
                   label: DesignTokens.Typography.label)
        case .tier2:
            return (headline: DesignTokens.Typography.headline2,
                   body: DesignTokens.Typography.body,
                   label: DesignTokens.Typography.caption)
        case .tier3:
            return (headline: DesignTokens.Typography.headline3,
                   body: DesignTokens.Typography.caption,
                   label: DesignTokens.Typography.caption)
        }
    }

    private func getTierLineLimit() -> Int? {
        switch tier {
        case .tier1: return nil        // Unlimited lines
        case .tier2: return 3          // Limited expansion
        case .tier3: return 2          // Further limited
        }
    }

    private func shouldShowButton() -> Bool {
        switch tier {
        case .tier1: return true       // Always show
        case .tier2: return true       // Always show
        case .tier3: return false      // Hide for basic tier
        }
    }

    private func getShadowColor() -> Color {
        switch tier {
        case .tier1, .tier2: return DesignTokens.Shadow.elevation2.color
        case .tier3: return DesignTokens.Shadow.elevation1.color
        }
    }

    private func getShadowRadius() -> CGFloat {
        switch tier {
        case .tier1: return 12
        case .tier2: return 8
        case .tier3: return 4
        }
    }

    private func getShadowOffsetX() -> CGFloat {
        return DesignTokens.Shadow.elevation1.offsetX
    }

    private func getShadowOffsetY() -> CGFloat {
        switch tier {
        case .tier1: return 8
        case .tier2: return 4
        case .tier3: return 2
        }
    }
}

// Usage
CardComponent(title: "Premium Feature",
             description: "This feature adapts based on your tier",
             tier: .tier2)
```

## Tier Differences Explained

**Tier 1 (Premium)**
- Full color palette (12+ colors)
- Maximum typography choices (8+ sizes/weights)
- Rich spacing (4px, 8px, 12px, 16px, 20px, 24px, 32px)
- All corner radius options (4-20px)
- 4 shadow levels for depth
- Smooth animations (300-500ms)
- All interactive elements visible
- Animations enabled by default

**Tier 2 (Standard)**
- Standard palette (8-10 colors)
- Core typography (5-6 sizes/weights)
- Balanced spacing (8px, 12px, 16px, 20px, 24px)
- Standard corner radius (8px, 12px)
- 2-3 shadow levels
- Moderate animations (200-300ms)
- Essential interactive elements
- Animations enabled with toggle option

**Tier 3 (Basic)**
- Limited palette (5-6 colors)
- Essential typography (3-4 sizes)
- Reduced spacing (16px, 20px, 24px)
- Minimal corner radius (4px, 8px)
- 1-2 shadow levels (minimal depth)
- Minimal animations (100-200ms)
- Core interactive elements only
- Animations optional/disable by default

## Component Library

### MetricCard (Core Component)

```swift
struct MetricCard: View {
    let label: String
    let value: String
    let color: Color
    let icon: String?

    var body: some View {
        VStack(alignment: .leading, spacing: .sm) {
            HStack {
                Text(label)
                    .font(.caption)
                    .foregroundColor(.secondary)

                Spacer()

                if let icon = icon {
                    Image(systemName: icon)
                        .foregroundColor(color)
                }
            }

            Text(value)
                .font(.heroPrice)
                .foregroundColor(color)
        }
        .padding(.md)
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(radius: 2)
    }
}
```

### TierBadge (Visual Indicator)

```swift
struct TierBadge: View {
    let tier: UserTier

    var body: some View {
        Label(tier.displayName, systemImage: tier.iconName)
            .font(.caption)
            .padding(.xs, .sm)
            .background(tier.color)
            .foregroundColor(.white)
            .cornerRadius(6)
    }
}
```

## Animation Patterns

### Spring Physics (Tier-Aware)

```swift
extension Animation {
    // Tier 1: Playful, fast
    static let tier1Bounce = Animation.spring(
        response: 0.4,
        dampingFraction: 0.7,
        blendDuration: 0.1
    )

    // Tier 4: Smooth, professional
    static let tier4Smooth = Animation.spring(
        response: 0.6,
        dampingFraction: 0.85,
        blendDuration: 0.2
    )
}

// Victory animation on profit logged
Text("$89.50")
    .font(.heroPrice)
    .scaleEffect(1.0)
    .animation(.tier1Bounce, value: profitJustLogged)
```

### Micro-Interactions

```swift
// Tap feedback
struct ProfitButton: View {
    @State var isPressed = false

    var body: some View {
        Button(action: {
            withAnimation(.easeInOut(duration: 0.2)) {
                isPressed = true
            }
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                isPressed = false
            }
        }) {
            Text("Log Sale")
                .scaleEffect(isPressed ? 0.95 : 1.0)
        }
    }
}
```

## Accessibility (WCAG AAA)

### Contrast Requirements

```swift
// ✅ CORRECT: 7:1 contrast ratio minimum
Text("$1,234")
    .foregroundColor(.tier1Primary)      // #4CAF50
    .background(.white)                  // Will have 7.2:1 ratio

// ❌ WRONG: Insufficient contrast
Text("Net Profit")
    .foregroundColor(.gray)              // Only 4.5:1 ratio
```

### Dynamic Type Support

```swift
Text("Net Profit")
    .font(.sectionHeader)               // Built-in scaling
    .lineLimit(1)
    .minimumScaleFactor(0.8)            // Never go below 80% size

// Test with:
// Settings → Accessibility → Display & Text Size → increase to Max
```

## Shadow & Depth

```swift
extension View {
    func cardStyle() -> some View {
        self
            .background(Color(.systemBackground))
            .cornerRadius(12)
            .shadow(color: Color.black.opacity(0.1), radius: 4, x: 0, y: 2)
    }
}
```

## Responsive Layout (iPhone + iPad Future)

```swift
struct DashboardView: View {
    @Environment(\.horizontalSizeClass) var sizeClass

    var body: some View {
        if sizeClass == .compact {
            // iPhone: Stack vertically
            VStack {
                MetricCard()
                MetricCard()
            }
        } else {
            // iPad: 2-column grid
            HStack {
                MetricCard()
                MetricCard()
            }
        }
    }
}
```

## Real-World Example: Complete Card

```swift
struct StorageLocationCard: View {
    let location: StorageLocation
    let tier: UserTier

    var body: some View {
        VStack(alignment: .leading, spacing: .md) {
            // Header
            HStack {
                VStack(alignment: .leading, spacing: .xs) {
                    Text(location.name)
                        .font(.sectionHeader)
                        .foregroundColor(.primary)

                    Text(location.dateAdded.formatted())
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                Spacer()
                TierBadge(tier: tier)
            }

            // Photo
            if let photo = location.photo {
                Image(uiImage: photo)
                    .resizable()
                    .scaledToFill()
                    .frame(height: 150)
                    .cornerRadius(8)
                    .clipped()
            }

            // Metrics
            HStack(spacing: .lg) {
                MetricCard(
                    label: "Investment",
                    value: location.totalCost.formatted(),
                    color: tier.color
                )

                MetricCard(
                    label: "Remaining Value",
                    value: location.remainingValue.formatted(),
                    color: tier.color
                )
            }

            // ROI
            Text("ROI: \(location.roi)%")
                .font(.bodyText)
                .foregroundColor(location.roi > 0 ? .green : .red)
        }
        .cardStyle()
    }
}
```

## Testing Visual Consistency

```swift
// Snapshot test each component
func testMetricCardAppearance_AllTiers() {
    let tiers: [UserTier] = [.casual, .hustler, .pro, .enterprise]

    for tier in tiers {
        let card = MetricCard(
            label: "Net Profit",
            value: "$1,234.00",
            color: tier.primaryColor
        )

        assertSnapshot(matching: card, named: "MetricCard_\(tier)")
    }
}
```

## Design System Recompilation Workflow

When design decisions change, follow this workflow:

1. **Update Source Tokens** (`tokens.json`)
   ```json
   {
     "color": {
       "primary": {
         "value": "#007AFF",
         "tier1": "#007AFF",
         "tier2": "#0051BA",
         "tier3": "#0040A0"
       }
     }
   }
   ```

2. **Run Token Compiler**
   ```bash
   npm run compile:tokens
   # Outputs:
   # - ios-tier1-tokens.swift
   # - ios-tier2-tokens.swift
   # - ios-tier3-tokens.swift
   ```

3. **Verify Compiled Output**
   ```swift
   // Auto-generated file: ios-tier2-tokens.swift
   struct DesignTokens {
       struct Colors {
           static let primary = Color(red: 0, green: 0.32, blue: 0.73)  // #0051BA
       }
   }
   ```

4. **Update Components** to use new tokens
5. **Run Tests** to verify consistency
6. **Deploy** updated components

## Common Mistakes & Anti-Patterns

### Mistake 1: Using Magic Numbers

**Problem**: Hard-coded values break tier adaptation and create maintenance burden.

```swift
// WRONG
VStack(spacing: 16) {  // Magic number - what tier is this?
    Text("Title")
        .font(.system(size: 18, weight: .bold))  // Magic number
        .padding(12)  // Magic number
}

// CORRECT
VStack(spacing: DesignTokens.Spacing.md) {
    Text("Title")
        .font(.system(size: DesignTokens.Typography.headline2.size,
                     weight: DesignTokens.Typography.headline2.weight))
        .padding(DesignTokens.Spacing.sm)
}
```

### Mistake 2: Ignoring Tier Differences in Styling

**Problem**: Same visual treatment across all tiers defeats tier-adaptive design purpose.

```swift
// WRONG
struct FeatureCard: View {
    var body: some View {
        VStack {
            Text("Feature")
                .font(.system(size: 20, weight: .bold))
                .padding(16)
        }
        .cornerRadius(12)
        .shadow(radius: 8)
    }
}

// CORRECT
struct FeatureCard: View {
    let tier: UserTier

    var body: some View {
        VStack {
            Text("Feature")
                .font(.system(size: getTitleSize(),
                             weight: getTitleWeight()))
                .padding(getTierPadding())
        }
        .cornerRadius(getTierCornerRadius())
        .shadow(radius: getTierShadowRadius())
    }

    private func getTitleSize() -> CGFloat {
        tier == .tier3 ? 16 : 20
    }

    private func getTitleWeight() -> Font.Weight {
        tier == .tier1 ? .bold : .semibold
    }

    private func getTierPadding() -> CGFloat {
        switch tier {
        case .tier1: return 20
        case .tier2: return 16
        case .tier3: return 12
        }
    }

    private func getTierCornerRadius() -> CGFloat {
        switch tier {
        case .tier1: return 16
        case .tier2: return 12
        case .tier3: return 8
        }
    }

    private func getTierShadowRadius() -> CGFloat {
        switch tier {
        case .tier1: return 12
        case .tier2: return 8
        case .tier3: return 4
        }
    }
}
```

### Mistake 3: Inconsistent Token Usage Across Components

**Problem**: Different components use different approaches, creating maintenance chaos.

```swift
// WRONG - Component A uses tokens
Button(action: {}) {
    Text("Save")
        .foregroundColor(DesignTokens.Colors.buttonText)
        .background(DesignTokens.Colors.primary)
}

// WRONG - Component B uses magic numbers
Button(action: {}) {
    Text("Save")
        .foregroundColor(.white)
        .background(Color(red: 0, green: 0.48, blue: 1))
}

// CORRECT - All components use tokens consistently
// Component A
Button(action: {}) {
    Text("Save")
        .foregroundColor(DesignTokens.Colors.buttonText)
        .background(DesignTokens.Colors.primary)
}

// Component B
Button(action: {}) {
    Text("Save")
        .foregroundColor(DesignTokens.Colors.buttonText)
        .background(DesignTokens.Colors.primary)
}
```

### Mistake 4: Forgetting to Recompile Tokens After Changes

**Problem**: Design changes not reflected in code; components use stale tokens.

```bash
# WRONG - Update tokens.json but forget to recompile
# Designers update colors but don't run:
npm run compile:tokens

# Result: Components still use old colors

# CORRECT - Always recompile after token changes
# 1. Update tokens.json
# 2. Run: npm run compile:tokens
# 3. Verify: ios-tier1/2/3-tokens.swift updated
# 4. Commit changes
# 5. Deploy
```

### Mistake 5: Hardcoding Tier Logic Instead of Using Helpers

**Problem**: Repeated tier logic in every component leads to bugs when tier behavior changes.

```swift
// WRONG - Duplicated tier logic everywhere
struct CardA: View {
    let tier: UserTier
    var body: some View {
        VStack {
            if tier == .tier1 {
                Text("Premium").font(.headline)
            } else if tier == .tier2 {
                Text("Standard").font(.body)
            } else {
                Text("Basic").font(.caption)
            }
        }
    }
}

struct CardB: View {
    let tier: UserTier
    var body: some View {
        VStack {
            if tier == .tier1 {
                Text("Feature").font(.headline)  // Same logic repeated
            } else if tier == .tier2 {
                Text("Feature").font(.body)
            } else {
                Text("Feature").font(.caption)
            }
        }
    }
}

// CORRECT - Centralized tier helpers
struct TierHelper {
    static func getTitleFont(for tier: UserTier) -> Font {
        switch tier {
        case .tier1: return .headline
        case .tier2: return .body
        case .tier3: return .caption
        }
    }
}

struct CardA: View {
    let tier: UserTier
    var body: some View {
        VStack {
            Text("Premium").font(TierHelper.getTitleFont(for: tier))
        }
    }
}

struct CardB: View {
    let tier: UserTier
    var body: some View {
        VStack {
            Text("Feature").font(TierHelper.getTitleFont(for: tier))
        }
    }
}
```

## Design System Consistency Checklist

Use this checklist to verify tier consistency before committing:

- [ ] All numeric values come from token files (no magic numbers)
- [ ] Component renders correctly for tier 1, 2, and 3 users
- [ ] Token recompilation completed after any design changes
- [ ] Spacing follows 8px base unit (or 16px for tier 3)
- [ ] Typography uses defined sizes only (not arbitrary pt values)
- [ ] Shadow levels map to tier capabilities
- [ ] Animation durations use token values
- [ ] Corner radius uses predefined values only
- [ ] Color usage is semantic (primary, success, error, etc.)
- [ ] Tier-specific logic is centralized in helpers
- [ ] Tests verify tier rendering differences
- [ ] No hard-coded platform-specific values

## Implementation Checklist for New Components

When creating a new component using design tokens:

1. [ ] Define tier behavior in requirements
2. [ ] Identify all design decisions (colors, spacing, typography, shadows, animations)
3. [ ] Map each decision to a token
4. [ ] Create tier-aware helper functions if needed
5. [ ] Implement component with tokens (no magic numbers)
6. [ ] Test rendering on tier 1, 2, and 3
7. [ ] Document tier differences in comments
8. [ ] Update design system documentation
9. [ ] Get design review
10. [ ] Commit with clear tier-adaptation details

## References

- [Apple HIG 2026](https://developer.apple.com/design/human-interface-guidelines/)
- [SF Pro Rounded Font](https://developer.apple.com/fonts/)
- [Color Accessibility](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- Docs/Product/Design/ - Full design specs
- Docs/Development/DESIGN_TOKEN_WORKFLOW.md
- Docs/Design/Core/VISUAL_SYSTEM.md

