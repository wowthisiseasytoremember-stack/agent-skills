---
name: flipscale-doc-sync
description: Use when maintaining Docs/ folder to keep documentation in sync with code changes, update ARCHITECTURE.md when adding services, or verify DocC catalogs match public APIs
---

# FlipScale Doc Sync

Manages FlipScale's extensive documentation, ensuring it stays synchronized with code. Handles architecture updates, feature documentation, roadmap maintenance, and DocC catalog generation.

## Documentation Truth Sources

Each doc category has a single source of truth:

| Category | Source File | Update Frequency |
|----------|-------------|------------------|
| **Architecture** | `Docs/Development/ARCHITECTURE.md` | When adding/removing modules or services |
| **Features** | `Docs/Product/Features/*.md` | When feature status changes |
| **Roadmap** | `Docs/Roadmap/FEATURE_ROADMAP.md` | Weekly during development |
| **Design Tokens** | `Docs/Product/Design/Assets/` | When design system changes |
| **API** | `Docs/Development/API_REFERENCE.md` | When public APIs change |

## Keeping Docs in Sync with Code

### 1. After Adding a New Service

When you create `Sources/FlipScale/Services/NewService/NewService.swift`:

```swift
// 1. Add to ARCHITECTURE.md
// Under "Services/" section, document:
// - Purpose
// - Key functions
// - Example usage

// 2. Add to API_REFERENCE.md
// Public APIs documentation

// 3. Create new feature doc if applicable
// Docs/Product/Features/NEWFEATURE.md

// 4. Update FEATURE_ROADMAP.md
// Mark feature status as "In Progress" or "Completed"

// Test: Run docC verification
// swift docs build --check-documentation
```

### 2. When Design Tokens Change

If you update `brand-colors.json`:

```swift
// 1. Update design-token-compiler skill output
//    (automatically generates Colors.swift)

// 2. Update DESIGN_TOKENS.md
// - Document new color name
// - Show hex value
// - Explain usage (which tier)

// 3. Update color accessibility test
// XCertAssertEqual(wcagContrast(color), >=7.0)

// 4. Mark in release notes
// Docs/CHANGELOG.md → "## Unreleased"
```

### 3. Updating Roadmap Status

Every Friday, update roadmap to reflect current week's progress:

```swift
struct RoadmapUpdate {
    let phase: String           // "Phase 1", "Phase 2", etc
    let task: String            // Task name
    let status: RoadmapStatus   // .notStarted, .inProgress, .completed
    let percentComplete: Int    // 0-100
    let notes: String           // Any blockers or changes
}

// Example
let update = RoadmapUpdate(
    phase: "Phase 1",
    task: "Financial Precision Audit",
    status: .inProgress,
    percentComplete: 65,
    notes: "Decimal migration 90% done, testing in progress"
)
```

### 4. DocC Catalog Generation

Keep DocC in sync with public APIs:

```bash
# Generate documentation from code comments
swift package generate-documentation

# Verify all public APIs are documented
swift docs validate --check-documentation

# Update DocC catalog
# Docs/Development/DocC/Documentation.docc/
```

## Documentation Structure Maintenance

### Checking What's Broken

```swift
// Quarterly, run this check:
func auditDocumentation() {
    // 1. Find all *.md files
    let docs = findAllDocs()

    // 2. Check for broken links
    for doc in docs {
        let links = extractLinks(doc)
        for link in links {
            if !fileExists(link) {
                print("BROKEN: \(doc) → \(link)")
            }
        }
    }

    // 3. Check for outdated info
    for doc in docs {
        if doc.lastUpdated < Date().addingTimeInterval(-30 * 86400) {
            print("STALE: \(doc) (30+ days old)")
        }
    }
}
```

### Adding New Documentation

Before shipping a feature:

```
✅ Code complete
✅ Tests pass
✅ Feature doc created: Docs/Product/Features/FEATURE.md
✅ Architecture doc updated: Docs/Development/ARCHITECTURE.md
✅ Roadmap updated: Docs/Roadmap/FEATURE_ROADMAP.md
✅ API reference updated: Docs/Development/API_REFERENCE.md
✅ DocC comments added to public APIs
✅ Changelog entry added: Docs/CHANGELOG.md

Only then: Ready to commit
```

## Automated Doc Sync Checklist

Before each commit, verify:

```swift
struct DocSyncChecklist {
    var archDocsCurrent: Bool = false
    var apiRefCurrent: Bool = false
    var changelogUpdated: Bool = false
    var docCCommentsAdded: Bool = false
    var linksValid: Bool = false
    var noStaleInfo: Bool = false

    var isComplete: Bool {
        return archDocsCurrent && apiRefCurrent &&
               changelogUpdated && docCCommentsAdded &&
               linksValid && noStaleInfo
    }
}
```

## Common Documentation Updates

### New Feature in Development
```markdown
## Vision Hub (STUB - In Progress)

**Status:** Phase 2 Research
**Last Updated:** 2026-02-17
**Owner:** Vision Team

### Purpose
AI-powered product recognition for camera scanning.

### Current Status
- [ ] Model training
- [ ] Camera integration
- [x] App architecture design
- [ ] Testing framework
```

### Completed Feature
```markdown
## Tier System ✅

**Status:** Shipped (v1.0)
**Released:** 2026-02-17

### Implementation
See: Sources/FlipScale/Models/UserTier.swift
Tests: Tests/FlipScaleTests/ModelTests/UserTierTests.swift

### Tier Definitions
- Tier 1: Casual
- Tier 2: Hustler
- Tier 3: Pro
- Tier 4: Enterprise

### Migration Notes
Users auto-assigned tier based on item count.
```

## Documentation Review Checklist

Before pushing to main:

- [ ] All public APIs documented (DocC)
- [ ] All new files referenced in ARCHITECTURE.md
- [ ] Feature status accurate in FEATURE_ROADMAP.md
- [ ] No broken links to other docs
- [ ] CHANGELOG.md updated
- [ ] Design token docs current
- [ ] No outdated (>30 day old) docs without update plan

## DocC Standards

Every public function needs documentation:

```swift
/// Calculates profit for a single inventory item.
///
/// Takes into account marketplace fees, shipping costs, and taxes.
/// Returns a negative value if the item is a loss.
///
/// - Parameters:
///   - cost: The acquisition cost of the item
///   - sellingPrice: The selling price on the marketplace
///   - platform: Which marketplace (eBay, Poshmark, etc)
///
/// - Returns: Net profit after all deductions, rounded to 2 decimal places
///
/// - Important: Always use Decimal type, never Double
///
/// - Example:
///   ```swift
///   let profit = calculateProfit(
///       cost: Decimal(50),
///       sellingPrice: Decimal(100),
///       platform: .ebay
///   )
///   // profit = Decimal(34.71)
///   ```
public func calculateProfit(
    cost: Decimal,
    sellingPrice: Decimal,
    platform: Marketplace
) -> Decimal {
    // implementation
}
```

## Quarterly Doc Audit

Every 3 months, run full audit:

```swift
func quarterlyDocAudit() {
    print("Running Q1 2026 Doc Audit...")

    // 1. Check for broken links
    let brokenLinks = findBrokenLinks()
    if !brokenLinks.isEmpty {
        print("⚠️ Found \(brokenLinks.count) broken links")
        // Fix or remove
    }

    // 2. Find outdated docs
    let staleDocs = findDocOlderThan(30)
    if !staleDocs.isEmpty {
        print("⚠️ Found \(staleDocs.count) stale docs")
        // Update or archive
    }

    // 3. Check feature alignment
    let completedFeatures = getCompletedFeatures()
    let docsFeatures = getDocumentedFeatures()

    let missing = completedFeatures.filter { !docsFeatures.contains($0) }
    if !missing.isEmpty {
        print("⚠️ Missing docs for: \(missing)")
    }

    print("✅ Audit complete")
}
```

## References

- Docs/Development/ARCHITECTURE.md - Technical architecture
- Docs/Roadmap/FEATURE_ROADMAP.md - Feature tracking
- Docs/Development/API_REFERENCE.md - Public API docs
- Docs/CHANGELOG.md - Version history
- Docs/Development/DocC/ - Documentation catalog

