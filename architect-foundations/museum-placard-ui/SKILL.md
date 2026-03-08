# Skill: Museum Placard UI Component Generator

This skill is designed to generate and implement high-fidelity "Museum Placard" or "Botanical Triage" style detail windows. These are characterized by a clean, academic, yet premium aesthetic using a dual-font system, specific color palettes, and structured data grids.

## Core Design Principles
1. **Dual-Font System**: Use a Serif font (e.g., Playfair Display) for titles and scientific names (italicized), and a clean Sans-Serif (e.g., Source Sans 3 or Inter) for body text and labels.
2. **Museum Triage Palette**: 
   - Backgrounds: Warm Parchment, Ivory, or Light Grey.
   - Accents: Aged Gold (#B8860B), Botanical Green (#1B4332), or Deep Indigo.
   - Borders: Subtle 1px lines, often with a slight inner shadow.
3. **Placard Headers**: Always include a thin (1.5px - 3px) gradient accent bar at the very top.
4. **Structured Data Grid**: Use "Metric Cards" (small boxes) for at-a-glance data like "Rarity," "Liquidity," or "Era."
5. **Transparency & Confidence**: Always include a "Confidence Meter" (AI-synthesized status) and a "Sources" footer.

## Component Templates

### 1. StatCard / ParamCard (The "Little Squares")
- **Layout**: Icon (top-left) + Label (top-right, small uppercase) + Value (center, bold).
- **Style**: Subtle background tint (e.g., `muted/50`), rounded corners (8px - 12px), and clear typography.

### 2. Taxonomy Tree
- **Layout**: Tiered, indented list with a connecting "thread" or bullet points.
- **Purpose**: Showing hierarchical data (Kingdom -> Species) or (Collection -> Item).

### 3. Triage Badge
- **Style**: Small, high-contrast labels for status (e.g., "AI-Synthesized," "Auth-Verified").

## Integration Instructions
When asked to implement this style:
1. **React/Web**: Use Tailwind CSS with custom HSL variables for the palette.
2. **React Native**: Use `StyleSheet` with consistent `Colors` constants. Prioritize `expo-image` for high-quality item rendering.
3. **Icons**: Use `Lucide` (Web) or `lucide-react-native` (Mobile) with a consistent stroke width (1.5px or 2px).

## Example JSON Schema (Enrichment)
Expect a structured object with sections: `taxonomy`, `tradeInfo`, `careGuide` (or `itemSpecifics`), and `sources`.

---
*Museum Placard UI Skill v1.0*
