---
name: codebase-index-architect
description: Scans, indexes, and maps codebase architecture into LLM-optimized artifacts (Markdown/JSON). Use to provide a "source of truth" map that prevents redundant searching and token waste.
---

# Codebase Index Architect

The "Master Map" for the codebase. This skill performs deep architectural scanning, symbol indexing, and pattern auditing to provide a high-density source of truth (SoT).

## Core Capabilities
1.  **Symbol Indexing**: Maps all Structs, Classes, Actors, Enums, and Protocols to their files.
2.  **Pattern Auditing**: Identifies architectural violations (e.g., "SwiftUI in Services", "Double for Money").
3.  **Dependency Mapping**: Visualizes the flow from Model -> Service -> ViewModel -> View.
4.  **Stub Detection**: Finds all placeholder UI or logic marked as "stub" or "placeholder."

## Structured Outputs
- `CODEBASE_INDEX.json`: Machine-readable mapping of every symbol and its file path.
- `ARCHITECTURE_AUDIT.md`: LLM-optimized summary of state, patterns, and "Broken Windows."
- `DEPENDENCY_GRAPH.json`: Hierarchical view of the system's modular dependencies.

---

## Pattern: Double-for-Money Detection (Financial Precision)
**Violation**: `var amount: Double` or `func calculate(cost: Double)`
**Requirement**: Must use `Decimal`.
**Audit Logic**: Scan `Models/` and `Services/` for `Double` fields where name contains "Price", "Cost", "Amount", "Profit", "ROI", "Fee", or "Revenue".

## Pattern: Service Isolation (Clean Architecture)
**Violation**: `import SwiftUI` in any file under `Services/`.
**Requirement**: Services must be platform-agnostic business logic.
**Audit Logic**: Scan `Services/` for `import SwiftUI` or `import Combine` (unless specific to data flow).

## Pattern: UserTier Adherence (Adaptive UI)
**Violation**: Hard-coded strings like "Casual" instead of `UserTier.casual`.
**Requirement**: UI must check `UserTier` or `OperatorLevel` for adaptive copy/colors.
**Audit Logic**: Scan `Views/` for conditional logic based on tier.

---

## Commands & Workflows

### 1. Index Codebase
Scans the root directory and builds the `CODEBASE_INDEX.json`.

**Process**:
- List all files in `Sources/` and `App/`.
- Use regex to extract all `struct`, `class`, `actor`, `enum`, `protocol` declarations.
- Record line numbers and file paths.

### 2. Audit Architecture
Runs the pattern-matching logic to identify "Broken Windows."

**Output (ARCHITECTURE_AUDIT.md)**:
- **Precision Violations**: List of `Double` fields for money.
- **Isolation Violations**: List of `SwiftUI` imports in `Services/`.
- **Inconsistency Report**: Discrepancies between `OperatorLevel` and `UserTier`.

### 3. Map Dependencies
Tracks `import` statements and `@Relationship` declarations to build the `DEPENDENCY_GRAPH.json`.

---

## Iron Law of Indexing
**The index is the truth.** If a symbol is in the index, its path is guaranteed. If a pattern is audited, its status is documented. No future skill should use `grep` for information already present in the `CODEBASE_INDEX`.
