# Branding History & Naming Map

Use this map to identify and replace legacy branding throughout the codebase.

## 🕰️ Legacy Names
- **iFlip** (Most common legacy name)
- **FlipScale** (Earlier company/project name)
- **Flippd** (Research/Initial prototype name)
- **SmartFlipInventoryAR** (Original technical name)

## 🎯 Current Target Branding
- **Project/Product Name:** **RORK-iFlip** (or **iFlip** for short-form UI)
- **Technical/Target Name:** **SmartFlipInventoryAR** (Internal Xcode target name - *DO NOT REFACTOR WITHOUT CARE*)
- **App Store/User Display Name:** **iFlip**

## 🚦 Refactor Guidelines
- **UI Strings:** All user-facing text should use "iFlip" consistently.
- **Internal Logic:** Variable names and folder structures like `SmartFlipInventoryAR` are deeply tied to the Xcode project and build settings. Use caution when refactoring these to avoid breaking the build.
- **Case Sensitivity:** Search for variants like `iflip`, `IFLIP`, `iflip.com`, etc.
