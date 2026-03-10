---
title: "Micro-Interaction Polish"
name: subtle-polish-mechanics
purpose: "Delightful, purposeful micro-interactions and subtle animations"
superpowers: writing-skills
keywords:
  - polish
  - micro-interactions
  - motion
  - animation
  - delight
  - feedback
  - accessibility
  - SwiftUI
---

# Micro-Interaction Polish: Subtle-Polish-Mechanics

## Overview

Micro-interactions are the small, purposeful animations and feedback signals that make interfaces feel alive and responsive. This skill teaches the art of subtle motion design—the difference between a button that "works" and a button that *delights*.

### The Iron Law: Motion Should Earn Its Presence

Every animation must serve a purpose:
- **Feedback**: Signal that an action was received
- **Context**: Maintain spatial or logical relationships during transitions
- **Guidance**: Direct user attention intentionally, not accidentally
- **Delight**: Create a moment of joy without distracting from the task

The baseline failure is an unpolished interface: buttons with no hover states, screens that cut instead of flow, loading states with no indication of progress. The expected success transforms this into an experience where every interaction feels intentional, responsive, and refined.

---

## Micro-Interaction Principles

### 1. **Duration & Timing**
- **Instant feedback**: 100-200ms for immediate responses (hover states, toggles)
- **Transition flow**: 300-500ms for screen transitions and significant state changes
- **Loading indication**: Continuous loops with strategic pause points
- **Success celebration**: 400-600ms, subtle and gratifying

*Why?* Fast enough to feel responsive, slow enough to be perceived. Too quick = missed; too slow = frustrating.

### 2. **Easing Curves**
- **ease-in-out**: General UI transitions (smooth, familiar)
- **ease-out**: Entrances that should feel eager (spring-like)
- **ease-in**: Exits or dismissals (gravity pulling down)
- **spring**: Button presses, touches, delight moments (bouncy, natural)

### 3. **Layered Animation**
- Stagger child animations by 50-100ms
- Let elements move in sequence, not all at once
- Creates rhythm and hierarchy without complexity

### 4. **Subtle Scale & Opacity**
- Hover: 1.02x scale or 90% → 100% opacity (not 1.2x—that's overdone)
- Press: 0.98x scale (acknowledge the tap without breaking the grid)
- Loading: Gentle rotation or breathing opacity (8-10s loops)

### 5. **Feedback Over Flourish**
- Every animation answers: *What just happened?*
- Remove any animation that doesn't communicate state change
- Motion should support usability, not compete with it

---

## Motion Scenarios Table

| Scenario | Pattern | Duration | Easing | Implementation Note |
|----------|---------|----------|--------|---------------------|
| **Button Hover** | Scale 1.02x + opacity shift | 150ms | ease-in-out | Subtle, non-distracting |
| **Button Press** | Scale to 0.98x, then spring back | 100ms | spring | Physical, tactile feeling |
| **Screen Transition** | Fade + slide (enter from right/left) | 400ms | ease-in-out | Maintain direction context |
| **Loading Spinner** | Continuous rotation, slight pulse opacity | 8s loop | linear rotation + ease-in-out opacity | Breathing effect keeps it alive |
| **Success State** | Scale burst (1.0 → 1.1 → 1.0) + opacity | 500ms | spring | Celebrates without overdoing |
| **Error Toast** | Slide in from top, shake on focus, fade out | 300ms in / 150ms shake / 400ms out | ease-out / spring / ease-in | Draws attention, then retreats |
| **Dismiss/Collapse** | Scale down + fade, move off-screen | 300ms | ease-in | Gravity-like departure |
| **Form Input Focus** | Underline expands, label floats + color shift | 200ms | ease-out | Guides user attention |

---

## SwiftUI Code Examples

### Example 1: Subtle Button with Press Feedback

```swift
struct PolishedButton: View {
    @State private var isPressed = false

    var body: some View {
        Button(action: {
            triggerTap()
        }) {
            Text("Tap Me")
                .font(.headline)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 12)
                .background(Color.blue)
                .cornerRadius(8)
        }
        .scaleEffect(isPressed ? 0.98 : 1.0)
        .opacity(isPressed ? 0.8 : 1.0)
        .animation(.spring(response: 0.3, dampingFraction: 0.7), value: isPressed)
        .onTapGesture {
            isPressed = true
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                isPressed = false
            }
        }
    }

    private func triggerTap() {
        // Action logic
    }
}
```

**Why this works:**
- Spring easing creates a natural "bounce" feeling
- 0.98 scale is noticeable but doesn't break the layout
- 100ms press duration is perceived but quick
- Reset happens automatically, no jarring snap

---

### Example 2: Loading Spinner with Breathing Effect

```swift
struct BreathingSpinner: View {
    @State private var isRotating = false
    @State private var isBreathing = false

    var body: some View {
        ZStack {
            Circle()
                .stroke(Color.gray.opacity(0.2), lineWidth: 3)
                .frame(width: 40, height: 40)

            Circle()
                .trim(from: 0, to: 0.8)
                .stroke(Color.blue, style: StrokeStyle(lineWidth: 3, lineCap: .round))
                .frame(width: 40, height: 40)
                .rotationEffect(.degrees(isRotating ? 360 : 0))
                .animation(.linear(duration: 1).repeatForever(autoreverses: false), value: isRotating)
                .opacity(isBreathing ? 0.6 : 1.0)
                .animation(.easeInOut(duration: 1).repeatForever(autoreverses: true), value: isBreathing)
        }
        .onAppear {
            isRotating = true
            isBreathing = true
        }
    }
}
```

**Why this works:**
- Continuous rotation feels effortless
- Breathing opacity (0.6 → 1.0) adds visual rhythm without distraction
- Linear rotation is predictable; easing on opacity adds sophistication
- 1s loop feels natural, not rushed

---

### Example 3: Success State Celebration

```swift
struct SuccessCheckmark: View {
    @State private var isAnimating = false

    var body: some View {
        ZStack {
            Circle()
                .fill(Color.green.opacity(0.1))
                .frame(width: 60, height: 60)
                .scaleEffect(isAnimating ? 1.0 : 0.5)
                .opacity(isAnimating ? 1.0 : 0.0)

            Image(systemName: "checkmark")
                .font(.system(size: 24, weight: .bold))
                .foregroundColor(.green)
                .scaleEffect(isAnimating ? 1.0 : 0.3)
                .opacity(isAnimating ? 1.0 : 0.0)
        }
        .animation(.spring(response: 0.4, dampingFraction: 0.6), value: isAnimating)
        .onAppear {
            isAnimating = true
        }
    }
}
```

**Why this works:**
- Spring easing on the burst feels celebratory but controlled
- Staggered animation (circle appears first, then checkmark)
- Opacity + scale combined give weight to the moment
- 400-500ms total duration doesn't linger too long

---

### Example 4: Screen Transition with Context

```swift
struct ContextualTransition: View {
    @State private var showDetails = false

    var body: some View {
        ZStack {
            if !showDetails {
                listView
                    .transition(.asymmetric(
                        insertion: .opacity,
                        removal: .move(edge: .leading).combined(with: .opacity)
                    ))
            } else {
                detailView
                    .transition(.asymmetric(
                        insertion: .move(edge: .trailing).combined(with: .opacity),
                        removal: .opacity
                    ))
            }
        }
        .animation(.easeInOut(duration: 0.4), value: showDetails)
    }

    private var listView: some View {
        NavigationStack {
            List {
                ForEach(0..<5, id: \.self) { index in
                    Button(action: { showDetails = true }) {
                        Text("Item \(index)")
                    }
                }
            }
            .navigationTitle("Items")
        }
    }

    private var detailView: some View {
        VStack {
            Button(action: { showDetails = false }) {
                HStack {
                    Image(systemName: "chevron.left")
                    Text("Back")
                }
            }
            .padding()

            Text("Detail View")
                .font(.title)

            Spacer()
        }
    }
}
```

**Why this works:**
- Asymmetric transitions create directional context (forward/backward)
- 400ms feels natural for navigation
- Combined opacity + movement prevents jarring cuts
- Removal direction differs from insertion, reinforcing flow

---

## Polish Checklist

Before shipping any interactive element, verify:

- [ ] **Feedback Signal**: Does the element respond visually to user input?
  - Hover state exists (scale, opacity, or color)
  - Press/active state is distinct from hover
  - Disabled state is visually clear

- [ ] **Duration**: Is animation timing appropriate?
  - Instant feedback: 100-200ms
  - Transitions: 300-500ms
  - Loading: 8-10s loops
  - No animation exceeds 1s without purpose

- [ ] **Easing**: Does the curve match the motion?
  - Entrances: ease-out or spring
  - Exits: ease-in
  - Transitions: ease-in-out
  - No linear easing on scale/opacity (feels robotic)

- [ ] **Layering**: Are sequential elements staggered?
  - Child animations offset by 50-100ms
  - Visual hierarchy reinforced through timing
  - No simultaneous animations unless intentional

- [ ] **Scale Subtlety**: Is scaling restrained?
  - Hover: 1.02x maximum
  - Press: 0.98x maximum
  - No scale factor exceeds 1.1x unless celebrating

- [ ] **Purpose**: Can you answer "Why does this animate?"
  - Communicates state change
  - Guides user attention
  - Provides feedback or delight
  - Remove if answer is "just looks nice"

- [ ] **Accessibility**: Does motion support or hinder usability?
  - Respects `prefers-reduced-motion`
  - Feedback doesn't rely on motion alone
  - No strobing or rapid flashing
  - Animations don't prevent task completion

- [ ] **Performance**: Does the animation run smoothly?
  - No jank or stuttering on target devices
  - Frame rate maintained (60fps minimum)
  - Reduced motion versions ready

---

## Accessibility Guardrails

Motion must enhance usability, never hinder it.

### 1. **Respect Reduced Motion**
```swift
struct AccessibleButton: View {
    @Environment(\.accessibilityReduceMotion) var reduceMotion
    @State private var isPressed = false

    var body: some View {
        Button(action: {}) {
            Text("Accessible Tap")
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(8)
        }
        .scaleEffect(isPressed ? 0.98 : 1.0)
        .animation(
            reduceMotion ? .none : .spring(response: 0.3, dampingFraction: 0.7),
            value: isPressed
        )
    }
}
```

### 2. **Motion Conveys Information, Not Replaces It**
- Don't animate instead of labeling
- Use color + text + motion (not motion alone)
- Success toast should have text, not just animation

### 3. **No Strobing or Flashing**
- Avoid rapid opacity changes (>3 times per second)
- Prefer continuous, smooth motion
- Never exceed WCAG limits for photosensitivity

### 4. **Animations Don't Block Interaction**
- User can always tap through animations
- Don't disable buttons during transitions
- Loading spinners should have cancel options

### 5. **Test with Accessibility Inspector**
- Verify reduced motion behavior
- Check VoiceOver announcements don't conflict with motion timing
- Ensure keyboard navigation works smoothly

---

## Common Mistakes (Forbidden Patterns)

### ❌ **Over-Animation**
```swift
// WRONG: Too much, too long, distracting
.scaleEffect(isPressed ? 1.3 : 1.0)  // Scale is 30%—too much
.animation(.easeInOut(duration: 2.0))  // 2 seconds is forever
.rotationEffect(.degrees(isPressed ? 720 : 0))  // Multiple spins
```

**Fix**: Scale ≤1.02-1.1, duration ≤500ms, rotate ≤360° max once

---

### ❌ **Motion That Distracts**
```swift
// WRONG: Animation draws attention away from content
.blur(radius: isAnimating ? 10 : 0)
.animation(.easeInOut(duration: 3.0).repeatForever())
```

**Fix**: Micro-interactions fade into background; they don't dominate perception

---

### ❌ **Ignoring Accessibility**
```swift
// WRONG: No consideration for accessibility
@State private var isAnimating = false

var body: some View {
    ZStack {
        // Animation plays regardless of user preference
        Circle()
            .fill(Color.red)
            .scaleEffect(isAnimating ? 1.2 : 1.0)
            .animation(.linear(duration: 0.5).repeatForever())
    }
}
```

**Fix**: Always check `@Environment(\.accessibilityReduceMotion)`

---

### ❌ **Inconsistent Easing**
```swift
// WRONG: Mismatched easing creates dissonance
Button(action: {}) {
    Text("Go")
}
.scaleEffect(isPressed ? 0.95 : 1.0)
.animation(.linear(duration: 0.3))  // Linear on scale = stiff
```

**Fix**: Use spring or ease-in-out for scale/opacity, linear for rotation only

---

### ❌ **No Feedback for Important Actions**
```swift
// WRONG: Delete button with no feedback
Button(role: .destructive, action: { deleteItem() }) {
    Text("Delete")
}
// No animation, no haptic, no confirmation
```

**Fix**: Add press feedback, success state, or confirmation haptic

---

### ❌ **Animation Blocks Interaction**
```swift
// WRONG: User can't tap while animating
@State private var isAnimating = false

var body: some View {
    Button(action: {
        isAnimating = true
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            isAnimating = false
        }
    }) {
        Text("Processing...")
    }
    .disabled(isAnimating)  // Button locked during animation
}
```

**Fix**: Keep UI interactive; animations play in background

---

## Implementation Guidelines

### Step 1: Identify the Interaction
Ask: *What is the user trying to do?*
- Tapping a button → press feedback
- Switching tabs → context transition
- Uploading → loading indication
- Completing a form → success celebration

### Step 2: Choose the Motion Pattern
Refer to the Motion Scenarios table. Pick the pattern that matches.

### Step 3: Set Appropriate Timing
- Feedback: 100-200ms
- Transition: 300-500ms
- Celebration: 400-600ms

### Step 4: Select Easing Curve
- Entrance: ease-out or spring
- Exit: ease-in
- General: ease-in-out

### Step 5: Verify Subtlety
- Scale factors: 0.98–1.1 only
- Opacity ranges: 0.5–1.0 (nothing disappears during feedback)
- Rotation: 360° max, linear easing only

### Step 6: Add Accessibility Checks
- Does it respect `prefers-reduced-motion`?
- Does motion communicate or distract?
- Is feedback independent of motion?

### Step 7: Test & Iterate
- Run on target devices (iPad, iPhone)
- Check frame rate (60fps minimum)
- Verify with VoiceOver and Accessibility Inspector
- Get feedback from real users

---

## Reference: Apple HIG Motion Principles

- **Purposefulness**: Every animation communicates or guides
- **Responsiveness**: Immediate feedback to user actions
- **Continuity**: Transitions maintain spatial relationships
- **Subtlety**: Motion enhances without overwhelming
- **Respect**: Accessibility comes first, delight follows

Apple's design philosophy: *"Motion is a means to an end, not the end itself."*

---

## Keywords & Concepts

**Primary:**
- Micro-interactions
- Motion design
- Subtle animation
- Feedback signals
- Polish

**Secondary:**
- SwiftUI animation
- Easing curves
- Spring dynamics
- Accessibility-first design
- User delight

**Implementation:**
- Spring easing
- Scale effects
- Opacity transitions
- Staggered animations
- Asymmetric transitions

**Mindset:**
- Purposeful motion
- Restraint over excess
- Accessibility guardrails
- Feedback clarity
- Context preservation

---

## Final Iron Law

> **Every animation must earn its presence. If you can't explain in one sentence why it exists, remove it.**

The goal is not to make interfaces flashy—it's to make them feel *alive*, *responsive*, and *joyful*. Restraint, purpose, and clarity are the hallmarks of professional micro-interaction design.

Ship interfaces that feel refined. Your users will notice.
