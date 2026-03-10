---
name: dopamine-loop-architect
description: Framework for behavioral engagement without predatory dark patterns. Use when designing milestone celebrations, achievement mechanics, or dopamine loops that sustainably motivate users.
---

# Dopamine Loop Architect

Design sustainable dopamine loops that drive user engagement while explicitly rejecting predatory dark patterns. This skill provides a psychological framework for achievement systems that feel earned, not manipulative.

## RED Phase: The Failure State

### Problem Definition: Generic Celebration is Empty

**Baseline Approach (❌ FAILS):**
```
"Show a popup when user hits $500 milestone"
→ User sees: Generic popup, quick dismiss
→ Psychological impact: None (feels hollow)
→ Long-term effect: Disengagement
```

**Why it fails:**
- No anticipation (dopamine precedes reward)
- No connection to user identity/values
- No investment mechanism (no next challenge)
- Feels automaton-like, not personally earned
- User asks: "Why should I care?"

**Expected Outcome of Failure:**
- ✗ Hollow achievement feeling
- ✗ No psychological resonance
- ✗ Feels manipulative or patronizing
- ✗ User dismisses and ignores future achievements
- ✗ Engagement plateau or decline

### RED Phase Capture: What We're Fixing

**Generic Implementation:**
```
"Show a popup"
```

**Skilled Implementation:**
```
Design loop:
  Anticipation (goal visibility)
  → Progress signals (incremental dopamine)
  → Achievement (climactic reward)
  → Celebration (emotional resonance)
  → Investment (next challenge)
```

---

## GREEN Phase: The Dopamine Loop Framework

### Core Psychology: How Dopamine Actually Works

**Key Insight (from behavioral neuroscience):**
Dopamine is NOT released at reward—it's released in **anticipation** of reward. The loop is:
1. **Anticipation** (dopamine spike when goal is visible)
2. **Progress** (continued dopamine for incremental wins)
3. **Achievement** (climax moment)
4. **Celebration** (emotional peak & reflection)
5. **Next Loop** (dopamine from new visible goal)

The **danger zone**: If celebration feels empty or achievement feels unearned, the loop breaks and users feel manipulated.

### The Four-Stage Dopamine Loop Flowchart

```
┌─────────────────────────────────────────────────────────────┐
│                    DOPAMINE LOOP CYCLE                      │
└─────────────────────────────────────────────────────────────┘

STAGE 1: GOAL VISIBILITY (Anticipation)
├─ User sees clear milestone: "$500 profit unlocks Tier 2"
├─ Dopamine release begins
├─ Visual anchor: Progress bar, countdown, or streak indicator
└─ Psychology: Motivation emerges from clarity

              ↓ User takes consistent action ↓

STAGE 2: PROGRESS SIGNALS (Incremental Dopamine)
├─ Each micro-achievement triggers small dopamine hit
├─ "$450/$500 to milestone!" shown in dashboard
├─ Notification: "You're 90% there!"
├─ Visual feedback: Progress bar fills slightly
└─ Psychology: Reinforcement without reward (yet)

              ↓ User hits milestone ↓

STAGE 3: ACHIEVEMENT (Climactic Moment)
├─ $501 reached—milestone triggered
├─ Visual celebration: Confetti, pulse, animation
├─ Emotional resonance tied to identity
├─ "🎉 You've reached $500! You're now a Tier 2 Pro"
└─ Psychology: Peak emotional moment

              ↓ Celebration ensues ↓

STAGE 4: CELEBRATION + INVESTMENT (Motivation for Next Loop)
├─ Celebration includes identity affirmation
├─ "Tier 2 Pros unlock exclusive insights"
├─ Show next milestone immediately
├─ "$500 reached! Next: $2,000 for Tier 3"
├─ New streak/goal becomes visible
└─ Psychology: Transition to next dopamine loop

              ↓ Cycle repeats ↓

SUSTAINABILITY CHECK:
├─ Is anticipation earned? (Did user work for this?)
├─ Is celebration proportional? (Not manipulative exaggeration)
├─ Is next goal challenging but achievable?
└─ Can user opt-out without shame? (Is it truly optional?)
```

### Complete Code Example: Milestone Event Structure

**From CoreFinancial Design Patterns:**

```swift
// DOPAMINE LOOP: Milestone System
struct MilestoneSystem {

    // STAGE 1: GOAL VISIBILITY
    // User sees clear milestone with progress
    func initializeMilestoneView(user: User) -> MilestoneProgress {
        let nextMilestone = user.calculateNextMilestone()

        return MilestoneProgress(
            currentAmount: user.totalProfit,
            targetAmount: nextMilestone.target,
            progressPercent: user.profitTowardMilestone(),
            tier: nextMilestone.tier,
            description: "Unlock \(nextMilestone.tier) status"
        )
    }

    // STAGE 2: PROGRESS SIGNALS
    // Incremental dopamine hits as user progresses
    func onTransactionLogged(_ transaction: Transaction, user: inout User) {
        user.totalProfit += transaction.profit

        let newProgress = user.profitTowardMilestone()

        // Show incremental progress
        if newProgress >= 25 && previousProgress < 25 {
            showProgressNotification("25% to milestone! Keep going")
        }
        if newProgress >= 50 && previousProgress < 50 {
            showProgressNotification("Halfway there! 🔥")
        }
        if newProgress >= 75 && previousProgress < 75 {
            showProgressNotification("Almost there! Last 25%")
        }
    }

    // STAGE 3 & 4: ACHIEVEMENT + CELEBRATION
    // Climactic moment with identity affirmation + next goal
    func onMilestoneReached(_ milestone: Milestone, user: User) {
        // Phase 3a: Climactic moment
        showCelebrationAnimation()
        playVictorySound()
        HapticManager.shared.playSuccess()

        // Phase 3b: Identity affirmation
        let celebrationMessage = CelebrationMessage(
            title: "🎉 \(milestone.tier) Achieved!",
            subtitle: "You've earned \(milestone.tier) status",
            emoji: milestone.emoji,
            identityMessage: "You're now a \(milestone.tier) seller"
        )
        showCelebrationCard(celebrationMessage)

        // Phase 4: Investment in next loop
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            let nextMilestone = user.calculateNextMilestone()

            showNextMilestoneTeaser(
                title: "Next milestone: \(nextMilestone.tier)",
                amount: nextMilestone.target,
                encouragement: "You're on your way!"
            )

            // Reset progress bar for next loop
            self.initializeMilestoneView(user: user)
        }
    }

    // SUSTAINABILITY GUARD: Is this predatory or genuine?
    func validateMilestoneIsEthical(_ milestone: Milestone) -> Bool {
        // Check: Is achievement actually earned?
        let isEarned = milestone.requirementType == .actualUserBehavior

        // Check: Is celebration proportional?
        let isCelebrationProportional = !milestone.usesExaggeratedLanguage()

        // Check: Can user opt out?
        let canOptOut = milestone.isOptionalToDisplay

        // Check: Is next goal challenging but achievable?
        let nextMilestone = calculateNext(for: milestone)
        let isNextChallenging = nextMilestone.target > milestone.target * 1.5
        let isNextAchievable = nextMilestone.target < milestone.target * 10

        return isEarned && isCelebrationProportional && canOptOut &&
               isNextChallenging && isNextAchievable
    }
}

// INTEGRATION: Track dopamine loop health
struct DopamineLoopMetrics {
    var milestoneReachedPerWeek: Int
    var averageMilestoneEngagementTime: TimeInterval
    var userOptOutRate: Double
    var sustainmentScore: Double  // 0.0-1.0

    // Health check: If opt-out rate > 30%, loop feels predatory
    var isHealthy: Bool {
        userOptOutRate < 0.30 && sustainmentScore > 0.7
    }
}
```

---

## Sustainable vs Predatory: The Critical Table

| Dimension | ✅ SUSTAINABLE | ❌ PREDATORY |
|-----------|----------------|------------|
| **Anticipation Source** | User works toward visible goal | Artificial scarcity ("Sale ends in 2h!") |
| **Progress Signals** | Real incremental progress shown | Fake intermediate rewards |
| **Achievement Feeling** | Earned through genuine effort | Given freely, feels hollow |
| **Celebration Language** | Proportional affirmation | Exaggerated hype-speak |
| **Next Challenge** | Challenging + achievable | Impossible or trivial |
| **Opt-Out Friction** | Zero friction, no shame | Hard to disable, shaming messages |
| **Consistency of Rules** | Rules don't change mid-loop | Goalposts move constantly |
| **Psychological Residue** | User feels proud, competent | User feels manipulated, tired |
| **Long-term Behavior** | Sustained engagement | Boom-bust burnout cycle |
| **User Autonomy** | User controls the loop | App controls the user |

---

## Psychology Principles Deep Dive

### 1. Anticipation (The Pre-Reward Dopamine)

**Principle:** Dopamine peaks when goal is **visible and achievable**, not when reward is given.

✅ **Good Implementation:**
```swift
// User can SEE the milestone
VStack {
    Text("$500 Profit Milestone")
        .font(.headline)

    ProgressView(value: 0.75)
    Text("$375 / $500 — You're at 75%")
        .font(.caption)
}
// Dopamine effect: User feels motivated, not yet rewarded
```

❌ **Bad Implementation:**
```
// Hidden milestone, sudden surprise
// User has no anticipation to look forward to
// Dopamine spike comes only at end (manipulative)
// When celebration comes, it feels unearned
```

**Psychology rule:** No anticipation = No sustainable dopamine loop.

### 2. Progress Signals (Incremental Rewards)

**Principle:** Multiple small dopamine hits > One large hit (desensitization prevention).

✅ **Good Implementation:**
```
25%: "Great start! 🚀"
50%: "Halfway there! 🔥"
75%: "Almost there! Last push!"
100%: "🎉 Milestone reached!"
```
Each checkpoint gives small dopamine release, building momentum.

❌ **Bad Implementation:**
```
Silent progress until 100%, then massive celebration
→ User feels manipulated ("Why the sudden hype?")
→ Next loop feels less exciting (desensitization)
```

### 3. Achievement Calibration (Proportionality)

**Principle:** Celebration intensity should match effort required.

✅ **Calibrated:**
- Small goal ($50) → Small celebration ("Nice flip!")
- Medium goal ($500) → Medium celebration ("You're crushing it! 🎉")
- Large goal ($5,000) → Large celebration + identity affirmation ("You're now Elite")

❌ **Miscalibrated:**
- Easy goal ($50) → Massive celebration ("🎊🎊🎊 LEGENDARY ACHIEVEMENT!!!")
  → User feels patronized
- Hard goal ($5,000) → Tiny celebration ("OK 👍")
  → User feels cheated

**Sustainability rule:** Celebration must match effort. Misalignment = Feels predatory.

### 4. Investment Mechanism (Next Loop Clarity)

**Principle:** Dopamine is sustained when next challenge is **immediately visible**.

✅ **Good Implementation:**
```
Achievement moment:
"🎉 $500 milestone reached! You're Tier 2!"

Immediately followed by:
"Next milestone: $2,000 for Tier 3
You're already $500 in. $1,500 to go!"
```
→ Dopamine loop immediately cycles

❌ **Bad Implementation:**
```
"Congratulations! Enjoy your achievement!"
(No next milestone shown)
→ Dopamine dissipates
→ User asks: "Now what?"
→ Engagement drops
```

**Sustainability rule:** Every celebration must immediately transition to next loop or feel complete.

### 5. Novelty & Variety (Desensitization Prevention)

**Principle:** Dopamine response decreases with repetition. Combat via novelty.

✅ **Good Implementation:**
```swift
// Vary celebration formats
enum CelebrationStyle {
    case animation      // First-time milestones
    case sound         // Occasional (not every time)
    case badge         // Mastery recognition
    case tier          // Status change
    case streak        // Consistency reward
}

// Don't repeat same celebration every time
func selectCelebrationStyle(for milestone: Milestone) -> CelebrationStyle {
    if milestone.isFirstMilestone { return .animation }
    if milestone.isBadgeEarned { return .badge }
    if milestone.isStatusChange { return .tier }
    return .streak
}
```

❌ **Bad Implementation:**
```
Same confetti animation every single milestone
→ Dopamine habituates quickly
→ User stops noticing after 5 milestones
```

### 6. Identity Affirmation (Psychological Stickiness)

**Principle:** Dopamine is sustainable when tied to **self-identity**, not just rewards.

✅ **Sustainable:**
```
"🎉 You've reached $500. You're now a Pro Seller.
Pro Sellers know the market inside and out."
```
→ Dopamine tied to identity = Long-term stickiness

❌ **Predatory:**
```
"🎉 You've reached $500. Here's a free badge!
(Generic reward, no identity connection)"
```
→ Dopamine tied to novelty only = Short-term only

---

## Common Mistakes: Predatory Patterns to Forbid Explicitly

### ❌ FORBIDDEN Pattern 1: Artificial Scarcity

```swift
// PREDATORY: False scarcity
"Only 3 of your items left before tier expires!"
"This bonus ends in 2 hours!"

// Why it fails: Goalpost was user's real behavior,
// not some external deadline. Feels manipulative.

// SUSTAINABLE: Real constraints
"Next tier available when you reach $1,000 total profit"
"You're 40% there based on this month's pace"
```

**Guard:** If the deadline is artificial (not real-world constrained), forbid it.

---

### ❌ FORBIDDEN Pattern 2: Shame-Based Motivation

```swift
// PREDATORY: Shame messaging
"You haven't logged an item in 3 days. Don't break your streak!"
"Other sellers are logging 5 items/week. You're at 2."

// Why it fails: Dopamine from shame is unhealthy.
// Creates anxiety, not joy. Unsustainable.

// SUSTAINABLE: Positive framing
"You're on a 7-day streak! Nice consistency."
"Similar sellers usually see first sale within 5 days."
```

**Guard:** If motivation comes from shame/fear, forbid it.

---

### ❌ FORBIDDEN Pattern 3: Unearned Rewards

```swift
// PREDATORY: Gift rewards that feel hollow
User has done nothing, yet:
"Congratulations! You got a free achievement today!"

// Why it fails: Dopamine from free rewards habituates instantly.
// User learns that achievements are meaningless.
// No anticipation = no sustainable dopamine.

// SUSTAINABLE: Earned achievements
"You've now logged 100 items.
100-Item Master achievement unlocked!"
```

**Guard:** If reward isn't connected to real user behavior, forbid it.

---

### ❌ FORBIDDEN Pattern 4: Streaks That Punish

```swift
// PREDATORY: Streak reset creates anxiety
"Your 15-day streak is at risk!
Log an item TODAY or lose it all."

// Why it fails: Dopamine from anxiety relief
// (not achievement) = predatory.

// SUSTAINABLE: Streaks as celebration, not whip
"You've got a 15-day streak! 🔥
Keep it up if you like, no pressure."
```

**Guard:** If streak mechanics create fear/shame, forbid them.

---

### ❌ FORBIDDEN Pattern 5: FOMO Notifications

```swift
// PREDATORY: Fear of missing out
"Other sellers are logging now! Don't fall behind!"
"Limited-time offer on Tier 2 upgrade ends in 1 hour!"

// Why it fails: FOMO dopamine is addictive but unhealthy.
// Creates compulsive behavior, not engagement.

// SUSTAINABLE: Valuable notifications only
"Your item sold! You made $89 profit."
"You've reached $500 milestone. Check it out."
```

**Guard:** If notification creates FOMO urgency, forbid it.

---

### ❌ FORBIDDEN Pattern 6: Hidden Unsubscribe

```swift
// PREDATORY: Hard to disable
UserDefaults.standard.set(true, forKey: "enableStreaks")
// No UI toggle, buried in settings

// Why it fails: User feels trapped.
// Psychological friction = bad faith design.

// SUSTAINABLE: Easy opt-out
Settings {
    Toggle("Show Streaks", isOn: $showStreaks)
    Toggle("Show Milestones", isOn: $showMilestones)
    Toggle("Show Notifications", isOn: $showNotifications)
}
// Users can disable anything instantly, no guilt
```

**Guard:** If opt-out requires >3 taps, forbid it.

---

## Implementation Checklist: "Is This Sustainable or Predatory?"

Before shipping any dopamine loop, answer these questions:

```swift
struct SustainabilityCheck {

    // Q1: Anticipation
    var isGoalVisibleBeforeCompletion: Bool
    var userWorkedForAchievement: Bool

    // Q2: Progress
    var showsIncrementalProgress: Bool
    var providesRegularSmallRewards: Bool

    // Q3: Achievement
    var celebrationProportionalToEffort: Bool
    var celebrationTiedToIdentity: Bool
    var neverUsingShame: Bool

    // Q4: Investment
    var nextChallengeImmediatelyVisible: Bool
    var nextChallengeIsAchievable: Bool
    var nextChallengeIsChallenging: Bool

    // Q5: Autonomy
    var userCanOptOutEasily: Bool
    var noPenaltyForOptingOut: Bool
    var streaksNeverCreateAnxiety: Bool

    // Q6: Transparency
    var rulesAreConsistent: Bool
    var goalpostsNeverMove: Bool
    var noArtificialScarcity: Bool

    var isSustainable: Bool {
        isGoalVisibleBeforeCompletion &&
        userWorkedForAchievement &&
        showsIncrementalProgress &&
        celebrationProportionalToEffort &&
        nextChallengeImmediatelyVisible &&
        nextChallengeIsAchievable &&
        userCanOptOutEasily &&
        !neverUsingShame
    }
}
```

**If ANY item is false, redesign before shipping.**

---

## Real-World Sustainable Example: Weekly Seller Loop

```
MONDAY 9 AM:
User opens app. Dashboard shows:
├─ "$450 profit this month"
├─ "Next milestone: $500 for Tier 2"
├─ Progress bar: 90% filled
├─ 🔥 7-day streak (if user logs consistently)

MONDAY-FRIDAY:
Each sale triggers:
├─ Notification: "Sold! +$45 profit"
├─ Dashboard updates live
├─ Progress bar visible: "$451 → $452 → $498 → $501"

FRIDAY 2 PM:
User hits $500 (milestone reached)

→ CELEBRATION SEQUENCE
├─ Visual: Confetti animation (proportional)
├─ Sound: Chime (not jarring)
├─ Haptic: Victory buzz (1 sec)
├─ Card: "🎉 You've reached $500!
          You're now Tier 2 Pro"
├─ Identity: "Tier 2 Pros unlock market insights"

2.5 SECONDS LATER:
→ NEXT LOOP BEGINS
├─ Next milestone teaser shown
├─ "$500 reached! Next: $2,000 for Tier 3"
├─ Progress bar resets: "$500/$2,000 — Start fresh"
├─ New goal is now visible again
└─ Dopamine loop cycles

RESULT:
✅ User feels proud (identity affirmed)
✅ User feels motivated (next goal visible)
✅ User feels in control (can opt out anytime)
✅ Loop is sustainable long-term
```

---

## Keywords & Taxonomy

**Primary:** dopamine, engagement, gamification, behavioral design, psychology

**Secondary:** sustainable, dark patterns, ethical design, habit formation, motivation

**Related Concepts:**
- Anticipatory dopamine vs reactive dopamine
- Identity-driven motivation vs reward-driven motivation
- Proportional celebration vs exaggerated hype
- Earned achievement vs hollow recognition
- Progressive challenge vs impossible goals
- User autonomy vs compulsion mechanics

---

## References & Research

**Behavioral Psychology:**
- Cialdini, R. (2021). *Influence: The Psychology of Persuasion* (6th ed.)
- BJ Fogg. Behavioral Model: Trigger → Motivation → Ability
- Nir Eyal. *Hooked: How to Build Habit-Forming Products* (ethical interpretation only)

**Dopamine Science:**
- Berridge, K. C., & Kringelbach, M. L. (2015). *Affective Neuroscience of Pleasure*
  Key finding: Dopamine peaks in **anticipation**, not consumption
- Schultz, W. (2013). *Updating Dopamine Reward Signals*
  Key finding: Dopamine encodes predictive value, not hedonic value

**Ethical Design:**
- Center for Humane Technology: darkpatterns.org
- Calvo, R. A., & Peters, D. (2014). *Positive Computing*
- Dark Patterns by Harry Brignull: deceptive UX patterns to avoid

---

## When to Use This Skill

✅ **Use dopamine-loop-architect when:**
- Designing achievement systems (milestones, badges, tiers)
- Building notification strategies for engagement
- Creating gamification mechanics
- Planning celebration moments (victories, streaks, status)
- Auditing existing engagement loops for predatory patterns
- Training teams on ethical behavioral design

❌ **Don't use when:**
- Designing purely functional features (no motivation layer)
- Building security/authentication systems (wrong domain)
- Creating transactional flows (not habit-formation)

---

## Validation Tests

```swift
// Test 1: Goal visibility
func testGoalIsVisibleBeforeCompletion() {
    let user = User(profitTowardMilestone: 0.0)
    let milestone = MilestoneCalculator.next(for: user)

    // Milestone should be shown immediately
    XCTAssertNotNil(user.displayedMilestone)
    XCTAssertEqual(user.displayedMilestone?.target, milestone.target)
}

// Test 2: Celebration is proportional
func testCelebrationProportionalToEffort() {
    let easyMilestone = Milestone(target: 50, difficulty: .low)
    let hardMilestone = Milestone(target: 5000, difficulty: .high)

    let easyCelebration = CelebrationSystem.select(for: easyMilestone)
    let hardCelebration = CelebrationSystem.select(for: hardMilestone)

    // Hard milestone should have more elements
    XCTAssertGreater(hardCelebration.animationDuration,
                     easyCelebration.animationDuration)
}

// Test 3: No shame-based messaging
func testNoShamingMessages() {
    let inactiveUser = User(daysSinceLastAction: 5)
    let message = EngagementMessage.generate(for: inactiveUser)

    XCTAssertFalse(message.contains("other"),
                   "Should not compare to others")
    XCTAssertFalse(message.contains("break your streak"),
                   "Should not threaten streak loss")
}

// Test 4: Next milestone is challenging but achievable
func testNextMilestoneIsBalanced() {
    let current = Milestone(target: 100)
    let next = MilestoneCalculator.next(after: current)

    // Should be 1.5x-3x current (challenging)
    XCTAssertGreaterThanOrEqual(next.target, current.target * 1.5)
    // Should not be impossible (< 10x)
    XCTAssertLessThan(next.target, current.target * 10)
}

// Test 5: Easy opt-out with no guilt
func testEasyOptOutMechanics() {
    let settings = SettingsView()

    // All toggles should be accessible
    XCTAssertTrue(settings.canToggleStreaks)
    XCTAssertTrue(settings.canToggleMilestones)
    XCTAssertTrue(settings.canToggleNotifications)

    // Disabling should not trigger shame messages
    settings.disableStreaks()
    XCTAssertNoShamingMessageShown()
}
```

---

## Summary: The Dopamine Loop Architect's Mission

Your job is to design **sustainable engagement loops that feel authentic**, not manipulative. Every milestone should:

1. ✅ Be **visible before completion** (anticipation)
2. ✅ Show **incremental progress** (multiple dopamine hits)
3. ✅ Result in **proportional celebration** (not exaggerated)
4. ✅ Connect to **user identity** (psychological stickiness)
5. ✅ Lead to **clear next challenge** (loop continuation)
6. ✅ Allow **easy opt-out** (user autonomy)
7. ✅ Never use **shame or artificial scarcity** (ethical boundary)

If you design loops this way, you'll build products that users love—not because they're addicted, but because they genuinely feel proud of their progress.

**That's the difference between sustainable dopamine and predatory manipulation.**
