---
name: apple-design-2026
description: Expert guidance on Apple Front-End Design and Best Practices for 2026, focusing on the "Liquid Glass" aesthetic, SwiftUI 6+ features, and Agentic UX.
---

# Apple Front-End Design & Best Practices (2026)

This skill provides procedural knowledge for designing and implementing state-of-the-art iOS/iPadOS/visionOS applications in 2026, adhering to the "Liquid Glass" design language introduced at WWDC 2025.

## 🎨 The "Liquid Glass" Aesthetic

Liquid Glass represents a shift from static glassmorphism to dynamic, physically-informed materials that react to the environment and user interaction.

### Core Principles
- **Dynamic Materiality:** UI elements should feature real-time refraction, specular highlights, and varying levels of "fluidity" based on the background.
- **3D Depth & Layering:** Use 3D shadows and refractive offsets to communicate hierarchy. Content should appear to "float" with tangible depth.
- **Hyper-Rounding:** Adopt the more aggressive corner radii inspired by visionOS. Buttons and cards should feel organic and soft.
- **Specular Highlights:** Edge lighting on buttons and cards that shifts as the user tilts the device (simulated via gyroscopic data in SwiftUI).

## 🛠️ SwiftUI 2026 Best Practices

### Component Usage
- **Native WebView:** Use the native `WebView` component (SwiftUI 6+) for embedding web content with high-performance observability.
- **Dynamic TabView:** Implement the shrinking/glassy tab bar behavior that adapts to scroll position.
- **Toolbar Groups:** Use `ToolbarItemGroup` with the new `.glassy` placement for floating toolbars.

### Layout & Animation
- **Spatial Consistency:** Use `SpatialStack` (if available) or standard layout primitives with `.zOffset()` to ensure apps are ready for "Spatial Mode" on iPadOS and visionOS.
- **Matched Geometry:** Use `matchedGeometryEffect` for transitions between list views and detail views, especially when expanding cards.
- **Micro-Animations:** Every state change should have a corresponding high-fidelity animation and haptic feedback ("The Pop").

## 🤖 Agentic & Adaptive UX

### Designing for AI
- **App Intents:** Every major action must be exposed via App Intents to allow Siri and system agents to navigate the UI.
- **Predictive Surface:** Use `.predictiveVisibility()` to show/hide UI elements based on the user's likely next action.
- **Contextual Bubbles:** AI-driven status updates (like "Categorizing...") should use pulsing, semi-transparent "Liquid" containers.

## ♿ Accessibility & Inclusivity
- **Contrast Ratios:** Maintain a minimum 4.5:1 ratio for all text.
- **Declarative Labels:** Ensure every interactive element has a clear, concise `accessibilityLabel`.
- **Dynamic Type:** All custom fonts (like Satoshi or Clash Display) must scale correctly with system settings.

## 📐 Implementation Checklist
- [ ] Is the background a solid ultra-dark (#0A0A0A) or adaptive mesh gradient?
- [ ] Do cards have a 1px refractive border?
- [ ] Are animations "bouncy" but purposeful?
- [ ] Is the hierarchy clearly communicated via depth/refraction rather than just color?
- [ ] Are App Intents implemented for all core workflows?
