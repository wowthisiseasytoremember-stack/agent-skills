---
name: ios-hig-2026
description: Use when choosing between UI patterns (modals, sheets, forms), designing interaction flows, or making design decisions for FlipScale to ensure Apple HIG 2026 compliance and eliminate ad-hoc design rationalization
---

# iOS HIG 2026 Reference Guide

Apple's Human Interface Guidelines 2026 provide the authoritative framework for iOS design decisions. This skill ensures FlipScale developers apply HIG principles systematically instead of guessing or following trends.

## HIG 2026 Hierarchy (Decision Priority)

Apple HIG 2026 establishes this modality hierarchy for user interaction:

1. **Inline editing** (best) - Modify content where it appears
2. **Sheets** (modal presentation) - Non-modal overlays, user can dismiss
3. **Bottom sheets** (persistent modals) - Full workflow, committed action
4. **Modals (full-screen)** (use sparingly) - Critical alerts, single-purpose workflows
5. **Popovers** (iPad only) - Contextual menus, small forms

**Key principle:** Use the least disruptive modality that accomplishes the task.

## FlipScale Pattern Decision Table

| Use Case | Pattern | HIG Reasoning | Example |
|----------|---------|---------------|---------|
| **Log single transaction** | Bottom sheet | User committing to action; non-dismissible until valid | "Log Sale" form |
| **Edit existing item** | Sheet (modal) | Non-committal; user can cancel without loss | "Edit inventory item" |
| **Quick confirmation** | Alert + sheet | Verify before committing | "Confirm $89.50 sale?" |
| **Multi-step workflow** | Bottom sheet progression | Sequential screens maintaining context | Multi-tier profit entry |
| **Browse categories** | Inline + filter | No modal needed; discovery mode | "View all categories" |
| **Delete/destructive** | Alert modal | Explicit confirmation, prevents accidents | "Delete this item?" |
| **Info disclosure** | Sheet | Contextual help, doesn't interrupt flow | "Why is this ROI 45%?" |

## Core HIG 2026 Principles for FlipScale

### 1. **Clarity**
- Every UI decision must eliminate ambiguity about user's next action
- Don't ask users to figure out the design

**Wrong for "Log Sale" dialog:**
```swift
// ❌ Modal with unclear exit path
Button("Done") { }  // Does this save? Cancel? What's the state?
```

**Correct (HIG 2026):**
```swift
// ✅ Bottom sheet with explicit outcomes
HStack {
    Button("Cancel", role: .cancel) { dismiss() }
    Button("Log Sale", role: .destructive) { saveAndDismiss() }
}
```

### 2. **Deference**
- UI should serve the content/task, not demand attention
- Don't use modals for browsing or exploration

**Wrong:**
```swift
// ❌ Modal for category selection (too heavyweight)
NavigationStack {
    CategoryListView()  // in modal = feels trapped
}
```

**Correct:**
```swift
// ✅ Sheet for category selection (easy to dismiss)
.sheet(isPresented: $showCategories) {
    CategoryListView()
}
```

### 3. **Accessibility (WCAG AAA)**
- Modals MUST have clear focus management
- Sheets MUST have dismiss gestures (swipe down, outside tap)
- Bottom sheets MUST require explicit action to dismiss

**Wrong:**
```swift
// ❌ No dismiss affordance
.sheet(isPresented: $showForm) {
    FormView()
        // Where does user click to go back?
}
```

**Correct:**
```swift
// ✅ Explicit dismiss button + swipe support
.sheet(isPresented: $showForm) {
    NavigationStack {
        FormView()
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { isOpen = false }
                }
            }
    }
}
```

### 4. **Depth & Layering**
- 2-3 layers maximum (prevent cognitive overload)
- Each layer should add context, not multiply options

**Wrong:**
```swift
// ❌ Modal containing sheet containing picker (too deep)
.sheet(isPresented: $s1) {
    VStack {
        .sheet(isPresented: $s2) {  // NESTED
            PickerView()
        }
    }
}
```

**Correct:**
```swift
// ✅ Flat: modal or sheet, single level
.sheet(isPresented: $showForm) {
    FormWithInlinePicker()
}
```

## Modal vs. Sheet: The Decision Framework

**Use MODAL (.fullScreenCover) ONLY when:**
- ✅ Workflow is single-purpose and linear
- ✅ No benefit to seeing context behind (e.g., onboarding)
- ✅ User will NEVER want to peek back at previous screen
- ✅ Dismissal is forced (must complete or force-quit)

**Use SHEET (.sheet) when:**
- ✅ User might want to cancel mid-action
- ✅ Context behind sheet is helpful for decision-making
- ✅ User can see partially through (on iPad)
- ✅ Swipe-down dismiss is expected

**Use BOTTOM SHEET when:**
- ✅ User is committing to an action (log sale, confirm price)
- ✅ Workflow is non-dismissible until validated
- ✅ Persistent UI (not floating) is needed
- ✅ iPad and iPhone have same experience (no popover)

## FlipScale: Transaction Entry Case Study

**Question:** "Should FlipScale use bottom sheet or modal for transaction input?"

**HIG 2026 Answer:**

**Context:**
- User is actively committing to a sale (intentional action)
- User wants confirmation visible before finalizing
- User should NOT be able to dismiss mid-entry without warning
- Dashboard context (profit so far) is NOT helpful during entry

**Decision → BOTTOM SHEET:**

```swift
struct LogSaleView: View {
    @State var isPresented = false
    @State var form = SaleForm()

    var body: some View {
        VStack {
            Button("Log Sale") {
                isPresented = true
            }
        }
        .sheet(isPresented: $isPresented) {
            ZStack {
                VStack(spacing: 16) {
                    // Header
                    HStack {
                        Text("Log Sale")
                            .font(.headline)
                        Spacer()
                        Button(action: { isPresented = false }) {
                            Image(systemName: "xmark.circle.fill")
                                .foregroundColor(.secondary)
                        }
                    }

                    // Form content
                    Form {
                        Section("Item") {
                            Picker("Category", selection: $form.category) {
                                ForEach(Category.allCases) { cat in
                                    Text(cat.name).tag(cat)
                                }
                            }
                            TextField("Item name", text: $form.itemName)
                        }

                        Section("Pricing") {
                            TextField("Cost", value: $form.cost, format: .currency(code: "USD"))
                            TextField("Selling Price", value: $form.sellingPrice, format: .currency(code: "USD"))

                            if let roiPercent = form.roiPercent {
                                Text("ROI: \(roiPercent)%")
                                    .foregroundColor(roiPercent > 0 ? .green : .red)
                            }
                        }
                    }

                    // Action buttons (COMMITMENT LAYER)
                    HStack(spacing: 12) {
                        Button(role: .cancel) {
                            isPresented = false
                        } label: {
                            Text("Cancel")
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.bordered)

                        Button(action: saveSale) {
                            Text("Log Sale")
                                .frame(maxWidth: .infinity)
                        }
                        .buttonStyle(.filled)
                        .disabled(!form.isValid)
                    }
                    .padding()
                }
                .padding()
            }
            .presentationDetents([.medium, .large])  // User can resize
            .presentationDragIndicator(.visible)      // Shows swipeable affordance
        }
    }

    func saveSale() {
        // Validate and save
        if form.isValid {
            // Haptic feedback
            HapticManager.shared.playSuccess()

            // Save to database
            SaleService.shared.log(form)

            // Dismiss
            isPresented = false

            // Show confirmation
            showSuccessNotification()
        }
    }
}
```

**Why this works per HIG 2026:**
1. ✅ **Clarity:** "Cancel" and "Log Sale" buttons are explicit
2. ✅ **Deference:** Form is lightweight, doesn't trap user
3. ✅ **Depth:** Single layer (sheet), form is inline
4. ✅ **Accessibility:** Swipe-down works, buttons are large, colors + text (not icon-only)
5. ✅ **Validation:** User can't submit invalid data (button disabled)
6. ✅ **Feedback:** Haptic + visual confirmation after save

## Anti-Rationalization: Explicit HIG Citations

These rationalizations and why they fail:

| Developer Says | HIG Reality | Reference |
|---|---|---|
| "I'll just use a modal, it's simpler" | Modals add cognitive load. Sheets are simpler. | HIG 2026 Modality: "Use the least disruptive presentation" |
| "Modals are more standard" | Sheets are the HIG 2026 default for non-critical tasks | HIG 2026 Sheets: "Preferred for most workflows" |
| "The designer will figure it out later" | Architectural debt. HIG decisions are code decisions. | Iron Law: Early principle application prevents rework |
| "Bottom sheets are just a trend" | Bottom sheets are HIG 2026 standard for committed actions | HIG 2026: Explicit guidance for transaction workflows |
| "Users will understand either way" | Accessibility and clarity vary significantly. Test with users. | WCAG AAA: Not optional |
| "Let me try both and pick one" | HIG provides the specification. Use it directly. | Iron Law: Test against principle, not trial-and-error |
| "This modal doesn't need a dismiss button" | Every presentation requires explicit dismiss (accessibility) | WCAG AAA: "Visible control for dismissal" |

## Common Mistakes Section

### Mistake 1: Modal for non-critical flows

**❌ Wrong:**
```swift
.fullScreenCover(isPresented: $editMode) {
    EditItemView()  // User can't go back easily
}
```

**✅ Correct:**
```swift
.sheet(isPresented: $editMode) {
    EditItemView()  // User can dismiss with swipe
}
```

**HIG Reason:** Full-screen modals should be reserved for critical flows (onboarding, payment). Editing existing items is a non-critical task per HIG 2026.

---

### Mistake 2: Nested sheets (exceeds depth limit)

**❌ Wrong:**
```swift
.sheet(isPresented: $showForm) {
    FormView()
        .sheet(isPresented: $showPicker) {  // NESTED
            PickerView()
        }
}
```

**✅ Correct:**
```swift
// Flatten: use single sheet with state machine
.sheet(isPresented: $showForm, content: formContent)

func formContent() -> some View {
    FormView(pickerState: $pickerState)  // Pass picker state as binding
}
```

**HIG Reason:** HIG 2026 explicitly recommends max 2-3 layers. Nested sheets violate hierarchy principle.

---

### Mistake 3: No dismiss affordance (accessibility violation)

**❌ Wrong:**
```swift
VStack {
    Text("Select category")
    List(categories) { cat in
        Button(cat.name) { select(cat) }
    }
    // No close button!
}
.sheet(isPresented: $isOpen) { /* ... */ }
```

**✅ Correct:**
```swift
NavigationStack {
    VStack {
        List(categories) { cat in
            Button(cat.name) {
                select(cat)
                isOpen = false  // Auto-dismiss on selection
            }
        }
    }
    .toolbar {
        ToolbarItem(placement: .cancellationAction) {
            Button("Cancel") { isOpen = false }
        }
    }
}
.sheet(isPresented: $isOpen) { /* ... */ }
```

**HIG Reason:** WCAG AAA requires visible dismiss path. Swipe-down alone isn't enough for users with motor difficulties.

---

### Mistake 4: Using sheet for confirmation (should be alert)

**❌ Wrong:**
```swift
.sheet(isPresented: $showConfirm) {
    VStack {
        Text("Delete this item?")
        HStack {
            Button("No") { }
            Button("Yes") { }
        }
    }
}
```

**✅ Correct:**
```swift
.alert("Delete this item?", isPresented: $showConfirm) {
    Button("Delete", role: .destructive) { deleteItem() }
    Button("Cancel", role: .cancel) { }
}
```

**HIG Reason:** HIG 2026 reserves alerts for quick confirmations. Sheets are for extended workflows.

---

### Mistake 5: Bottom sheet with optional dismissal

**❌ Wrong:**
```swift
.sheet(isPresented: $logSale) {
    SaleFormView()
    // User can cancel anytime = loss of data (frustrating)
}
```

**✅ Correct:**
```swift
.sheet(isPresented: $logSale) {
    SaleFormView()
        .interactiveDismissalDisabled(form.hasChanges)
        // Warn if they try to dismiss with unsaved data
}
```

**HIG Reason:** User commitment during transaction entry is explicit. Don't let them accidentally dismiss.

## SwiftUI Pattern: HIG-Compliant Form

```swift
struct HICCompliantFormPattern: View {
    @State var isPresented = false
    @State var formState = FormState()

    var body: some View {
        Button("Open Form") {
            isPresented = true
        }
        .sheet(isPresented: $isPresented) {
            FormContainerView(
                isPresented: $isPresented,
                formState: $formState
            )
        }
    }
}

struct FormContainerView: View {
    @Binding var isPresented: Bool
    @Binding var formState: FormState
    @FocusState var focusedField: FormField?

    var body: some View {
        NavigationStack {
            Form {
                Section("Details") {
                    TextField("Name", text: $formState.name)
                        .focused($focusedField, equals: .name)

                    Picker("Category", selection: $formState.category) {
                        ForEach(Category.allCases, id: \.self) { cat in
                            Text(cat.name).tag(cat)
                        }
                    }
                }

                Section("Pricing") {
                    TextField(
                        "Price",
                        value: $formState.price,
                        format: .currency(code: "USD")
                    )
                    .focused($focusedField, equals: .price)
                    .keyboardType(.decimalPad)
                }
            }
            .navigationTitle("New Item")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        if formState.hasChanges {
                            // Warn before dismissing
                            showDiscardAlert()
                        } else {
                            isPresented = false
                        }
                    }
                }

                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        if formState.isValid {
                            saveForm()
                            isPresented = false
                        }
                    }
                    .disabled(!formState.isValid)
                }
            }
        }
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
    }

    func saveForm() {
        HapticManager.shared.playSuccess()
        FormService.shared.save(formState)
    }

    func showDiscardAlert() {
        // Show confirmation before losing data
    }
}

struct FormState {
    var name: String = ""
    var category: Category = .electronics
    var price: Decimal = 0

    var hasChanges: Bool {
        !name.isEmpty || price > 0
    }

    var isValid: Bool {
        !name.isEmpty && price > 0
    }
}

enum FormField {
    case name
    case price
}
```

## Keywords for Search

- HIG (Human Interface Guidelines)
- design patterns
- iOS guidelines
- Apple 2026
- modality hierarchy
- sheet vs modal
- bottom sheet
- transaction entry
- form patterns
- interaction design
- accessibility (WCAG AAA)
- FlipScale patterns

## Design Decision Audit Checklist

Before implementing any modal, sheet, or form, verify:

- [ ] **HIG Hierarchy Applied:** Used least-disruptive modality (per HIG 2026 priority list)
- [ ] **Use Case Mapped:** Found pattern in FlipScale Decision Table; if not found, escalate to design lead
- [ ] **Accessibility Verified:** Dismiss button visible + swipe-down + WCAG AAA contrast (7:1+)
- [ ] **Depth Constraint:** No nested sheets; maximum 2-3 layers total
- [ ] **State Management:** Form state persists on dismissal? Data loss protected?
- [ ] **Button Clarity:** Action buttons explicit ("Save", "Delete", not "OK"); roles assigned (`.cancel`, `.destructive`)
- [ ] **Focus Management:** Keyboard focus starts in primary field; respects VoiceOver
- [ ] **Feedback:** Haptic + visual confirmation on action completion
- [ ] **iPad Compatibility:** Sheets behave consistently (no popovers unless intentional)

## Testing Behavioral Compliance

```swift
// Test 1: HIG Compliance - Is this sheet or modal?
func testUIModality_TransactionEntry() {
    // GIVEN: User opens transaction entry
    // WHEN: Form appears
    // THEN: Should be .sheet (dismissible), not .fullScreenCover (trapped)

    XCertAssertEqual(modalType, .sheet)
    XCertAssertTrue(canDismissWithSwipe)  // Swipe down works
    XCertAssertTrue(hasVisibleCancelButton)  // Explicit dismiss path
}

// Test 2: Clarity - Are buttons unambiguous?
func testButtonClarity_TransactionEntry() {
    let buttons = formView.buttons

    // Should NOT have: "OK", "Done", "Submit"
    XCertAssertFalse(buttons.contains(where: { $0.label.contains("OK") }))

    // SHOULD have: "Log Sale", "Cancel" with roles
    XCertAssertTrue(buttons.contains(where: { $0.label == "Log Sale" && $0.role == .none }))
    XCertAssertTrue(buttons.contains(where: { $0.label == "Cancel" && $0.role == .cancel }))
}

// Test 3: Accessibility - Can user with motor disability use it?
func testAccessibility_DismissalPaths() {
    // Multiple dismiss paths required
    let dismissPaths = [
        canSwipeDown,
        canTapCancelButton,
        canTapOutside  // Depends on design
    ]

    XCertAssertGreaterThanOrEqual(dismissPaths.filter({ $0 }).count, 2)
}
```

## Real-World Decision Example: FlipScale Tier Entry

**Scenario:** New feature - multi-tier profit entry (Tier 1-4 users enter different fields)

**Question:** Bottom sheet or modal?

**HIG 2026 Analysis:**
1. User is committing to save profit data? YES
2. Can user cancel mid-entry without warning? NO (data loss)
3. Is context behind screen helpful? NO (form is self-contained)
4. Single workflow or multi-step? Multi-step with progression

**Decision: Bottom sheet with progression**

```swift
struct TierAdaptiveEntry: View {
    @State var showForm = false
    @State var currentStep: FormStep = .basic

    var body: some View {
        Button("Enter Profit") {
            showForm = true
        }
        .sheet(isPresented: $showForm) {
            NavigationStack {
                Group {
                    switch currentStep {
                    case .basic:
                        BasicProfitForm(nextStep: $currentStep)
                    case .tierSpecific:
                        TierSpecificForm(tier: userTier, nextStep: $currentStep)
                    case .confirmation:
                        ConfirmationForm(nextStep: $currentStep)
                    }
                }
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) {
                        Button("Cancel") { showForm = false }
                    }
                }
            }
            .presentationDetents([.medium, .large])
            .interactiveDismissalDisabled(form.hasChanges)
        }
    }
}

enum FormStep {
    case basic
    case tierSpecific
    case confirmation
}
```

**Why this works:**
- ✅ Bottom sheet = committed workflow
- ✅ Single sheet with NavigationStack = no nesting (violates hierarchy)
- ✅ Cancel button available at all steps
- ✅ Data protected if dismissed (.interactiveDismissalDisabled)
- ✅ Tier-adaptive content without modal bloat

## References

- [Apple HIG 2026 - Presentations](https://developer.apple.com/design/human-interface-guidelines/presentations)
- [Apple HIG 2026 - Modality](https://developer.apple.com/design/human-interface-guidelines/modality)
- [SwiftUI Sheets & Modals](https://developer.apple.com/documentation/swiftui/presentations)
- [WCAG AAA Accessibility](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- Docs/Design/Core/VISUAL_SYSTEM.md - FlipScale design tokens
- Docs/Development/APPLE_2026_ARCHITECTURE.md - Technical architecture
