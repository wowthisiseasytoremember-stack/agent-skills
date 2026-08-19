---
name: design-token-compiler
description: Use when updating design system colors or typography to regenerate SwiftUI code from JSON automatically
---

# Design Token Compiler

Syncs `brand-colors.json` and `typography.json` with SwiftUI code. When designers update JSON, the skill regenerates Color extensions and Font definitions.

## One-Way Sync: JSON → Swift

**Truth Source:** `Docs/Product/Design/Assets/brand-colors.json`
**Generated Code:** `Modules/DesignSystem/Sources/DesignSystem/Tokens/Colors.swift`

Never edit the Swift file directly - edit JSON, regenerate.

## JSON Structure

### Colors

```json
{
  "tier1_casual": {
    "primary": "#4CAF50",
    "description": "Bright green for playful Tier 1 dashboard"
  },
  "tier2_hustler": {
    "primary": "#2E7D32",
    "description": "Standard green for Tier 2"
  },
  "neutral_background": "#F5F5F5",
  "neutral_card": "#FFFFFF"
}
```

### Typography

```json
{
  "hero": {
    "font": "SF Pro Rounded",
    "size": 48,
    "weight": "bold",
    "lineHeight": 1.2
  },
  "section": {
    "font": "SF Pro Rounded",
    "size": 20,
    "weight": "semibold"
  }
}
```

## Generated Swift Code

After compilation, `Colors.swift` looks like:

```swift
extension Color {
    static var tier1Casual: Color {
        Color(red: 0.298, green: 0.796, blue: 0.298)  // #4CAF50
    }

    static var tier2Hustler: Color {
        Color(red: 0.180, green: 0.494, blue: 0.196)  // #2E7D32
    }
}

extension ShapeStyle where Self == Color {
    static var primaryGreen: Color { .tier1Casual }
}
```

## Workflow

1. **Designer updates JSON** (e.g., tier colors, hero font size)
2. **Run compiler:** `swift Scripts/build/generate-tokens.swift`
3. **Verify Swift files updated**
4. **Commit both JSON + Swift files**

## Build Script Example

```swift
#!/usr/bin/env swift

import Foundation

func generateColors(from json: [String: Any]) {
    var swiftCode = """
    // AUTO-GENERATED: Do not edit directly. Update brand-colors.json instead.

    import SwiftUI

    extension Color {
    """

    for (name, config) in json {
        let hex = config["primary"] as? String ?? "#000000"
        let camelCase = toCamelCase(name)
        swiftCode += """

            static var \(camelCase): Color {
                Color(hex: "\(hex)")
            }
        """
    }

    swiftCode += "\n}\n"

    try? swiftCode.write(
        toFile: "Modules/DesignSystem/Sources/DesignSystem/Tokens/Colors.swift",
        atomically: true,
        encoding: .utf8
    )
}
```

## Usage in Code

```swift
import DesignSystem

struct DashboardView: View {
    var body: some View {
        VStack {
            Text("Net Profit")
                .foregroundColor(.tier1Casual)
        }
        .background(.neutralCard)
    }
}
```

## When to Use This Skill

- ✅ Color palette changed
- ✅ Typography scale updated
- ✅ New tier colors added
- ✅ Font weights adjusted
- ❌ Don't manually edit generated Swift files

## One-Way Sync Benefits

| Benefit | Impact |
|---------|--------|
| Single source of truth | Designers control colors, devs implement |
| Automated generation | No manual transcription errors |
| Type-safe in Swift | Compile-time color checking |
| Easy audits | All colors in one JSON file |
| Design consistency | Colors always match specs |

