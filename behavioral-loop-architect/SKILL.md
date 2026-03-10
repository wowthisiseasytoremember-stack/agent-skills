---
name: behavioral-loop-architect
description: Use when designing dopamine loops, gamification mechanics, or psychological engagement systems to motivate resellers while avoiding predatory patterns
---

# Behavioral Loop Architect

Designs FlipScale's behavioral engagement system: gamification, dopamine loops, win/loss psychology, and reseller motivation. Based on behavioral economics and ethical UX design.

## Core Psychology Principles

### 1. Dopamine Loop (4-Stage)

**Stage 1: Trigger** (Cue)
- "Ding!" notification for new sale
- Visual indicator of profit milestone

**Stage 2: Action** (Behavior)
- Open app to see the sale
- Tap to log transaction

**Stage 3: Reward** (Feedback)
- See profit number increase
- Haptic celebration (victory buzz)
- Animation pulse

**Stage 4: Investment** (Commitment)
- Save the item
- List similar items
- Set profit goal

### Example: The Sale Notification Loop

```swift
struct SaleNotificationFlow {
    // TRIGGER: User receives sale alert
    func notifySale(_ item: InventoryItem) {
        let notification = UNMutableNotificationContent()
        notification.title = "Sold! 🎉"
        notification.body = "Your \(item.name) sold for \(item.sellingPrice.formatted())"
        notification.badge = NSNumber(value: UIApplication.shared.applicationIconBadgeNumber + 1)

        // ACTION: User taps notification, opens app
        // REWARD: See dashboard update live
        // INVESTMENT: Prompt to add another similar item
    }

    // REWARD: Victory celebration in UI
    func celebrateSale(_ item: InventoryItem) {
        // Haptic feedback
        HapticManager.shared.playSuccess()

        // Animation
        withAnimation(.tier1Bounce) {
            self.showVictoryPulse = true
        }

        // Sound (optional)
        // AudioManager.shared.playWinSound()

        // Progress update
        self.updateProfitStreak()
        self.checkMilestones()
    }
}
```

### 2. Win Framing (Behavioral Economics)

**Key insight:** Resellers are motivated by WINS, not avoiding LOSSES.

❌ **Loss Framing (Demoralizing)**
```
"You have $2,147 in slow-moving inventory.
These items aren't selling. Consider reducing prices."
```

✅ **Win Framing (Motivating)**
```
"$2,147 waiting to be unlocked.
Similar items sold in avg 18 days.
Suggest: Drop to $49 → avg 8-day sale."
```

### 3. Progress Visualization

Show progress toward goals:

```swift
struct ProgressCard: View {
    let currentProfit: Decimal
    let monthlyGoal: Decimal

    var progressPercent: Double {
        Double(currentProfit) / Double(monthlyGoal) * 100
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            // Show progress bar
            ProgressView(value: progressPercent / 100)
                .tint(.tier1Casual)

            // Show achievement message
            HStack {
                Text("\(Int(progressPercent))% to \(monthlyGoal.formatted()) goal")
                    .font(.caption)

                if progressPercent >= 50 {
                    Image(systemName: "flame.fill")
                        .foregroundColor(.red)
                }
            }
        }
    }
}
```

### 4. Streak Psychology

Streaks motivate continued engagement:

```swift
struct StreakTracker {
    var currentStreak: Int = 0
    var bestStreak: Int = 0
    var lastLogDate: Date?

    mutating func logSale() {
        let today = Calendar.current.startOfDay(for: Date())

        if let lastLog = lastLogDate {
            let lastDay = Calendar.current.startOfDay(for: lastLog)
            let daysDiff = Calendar.current.dateComponents([.day], from: lastDay, to: today).day ?? 0

            if daysDiff == 1 {
                currentStreak += 1
            } else if daysDiff > 1 {
                currentStreak = 1  // Reset
            }
        } else {
            currentStreak = 1
        }

        bestStreak = max(currentStreak, bestStreak)
        lastLogDate = Date()
    }
}

// Display in UI
Text("🔥 \(tracker.currentStreak) day streak")
    .font(.headline)
    .foregroundColor(.orange)
```

### 5. Tier Progression (Motivation)

Users want to advance tiers:

```swift
struct TierProgressionView: View {
    @State var user: User

    var body: some View {
        VStack(spacing: 16) {
            // Current tier with celebration
            HStack {
                Text("You're at Tier \(user.tier.displayName)")
                    .font(.headline)

                if user.tier.isLowest {
                    Text("Get \($itemsUntilNextTier) more items → Tier 2")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }

            // Progress to next tier
            if user.tier != .enterprise {
                ProgressView(
                    value: Double(user.itemCount) / Double(user.nextTierThreshold)
                )

                Text("\(user.itemCount) / \(user.nextTierThreshold) items")
                    .font(.caption)
            } else {
                Text("🏆 You've reached the top tier!")
                    .font(.caption)
                    .foregroundColor(.green)
            }
        }
    }
}
```

## Ethical Guardrails (Anti-Dark Patterns)

### ✅ DO: Motivation Without Coercion

```swift
// GOOD: Show progress, let user decide
VStack {
    Text("Monthly goal: $500")
    ProgressView(value: 0.75)
    Text("You're on track! 25% to go.")
}

// BAD: Artificial urgency or FOMO
// ❌ "Only \(23 - user.itemCount) items left before tier expires!"
// ❌ Limited-time bonus for logging items
// ❌ Scarcity messaging on features
```

### ✅ DO: Celebrate Wins Without Shaming Losses

```swift
// GOOD: Positive framing
"You sold 3 items this week! Great momentum."

// BAD: Shaming
// ❌ "You haven't logged an item in 3 days. Don't break your streak!"
// ❌ "Other resellers are doing better than you."
```

### ✅ DO: Allow Opting Out

```swift
// Users should be able to disable:
UserDefaults.standard.set(false, forKey: "enableStreaks")
UserDefaults.standard.set(false, forKey: "enableNotifications")
UserDefaults.standard.set(false, forKey: "enableAchievements")

// No penalties for disabling
```

## Gamification Elements (2026 Standards)

| Element | Purpose | Implementation |
|---------|---------|-----------------|
| **Streaks** | Consistency | Days logging sales |
| **Milestones** | Achievement | $500/$1k/$5k lifetime profit |
| **Badges** | Mastery | "Speed Seller" (3 sales/week) |
| **Leaderboards** | Social (Optional) | Top resellers by region |
| **Tiers** | Progression | Casual → Enterprise |

### Example: Badge System

```swift
enum Badge: String, Codable {
    case speedSeller        // 3+ sales per week
    case highROI           // Avg ROI > 100%
    case consistentSeller  // 30-day sales streak
    case profitMachine     // $1000+ total profit
    case timeHunter        // Found item <5 min after listing
    case smartPricer       // Sold within 5% of market avg
}

struct BadgeProgress {
    let badge: Badge
    let progress: Double  // 0.0 to 1.0
    let requirementText: String
}

func checkBadges(user: User) -> [Badge] {
    var earned: [Badge] = []

    if user.weeklySalesCount >= 3 {
        earned.append(.speedSeller)
    }

    if user.averageROI > 1.0 {
        earned.append(.highROI)
    }

    if user.currentStreak >= 30 {
        earned.append(.consistentSeller)
    }

    return earned
}
```

## Notification Strategy (Respectful)

Only notify for:
- ✅ Real sale (user wants to know immediately)
- ✅ Milestone reached (natural celebration moment)
- ✅ Price drop recommendation (actionable, not spammy)

Never notify for:
- ❌ "Don't forget to log items!"
- ❌ "Other resellers are logging more than you"
- ❌ "Your streak is at risk"
- ❌ Artificial urgency

```swift
enum NotificationType {
    case sale(item: String, price: Decimal)          // ✅ Notify
    case milestoneReached(amount: Decimal)           // ✅ Notify
    case priceDropOpportunity(suggestion: String)    // ✅ Notify
    case dailyReminder                               // ❌ Don't notify
    case streakWarning                               // ❌ Don't notify
}

func shouldNotify(_ type: NotificationType) -> Bool {
    switch type {
    case .sale, .milestoneReached, .priceDropOpportunity:
        return true
    default:
        return false
    }
}
```

## Avoiding Predatory Design

**Red flags for dark patterns:**
- ❌ Making unsubscribe hard
- ❌ Arbitrary scarcity ("Only X items left!")
- ❌ Shame-based messaging
- ❌ Artificial streaks that reset
- ❌ FOMO notifications
- ❌ Subscriptions hiding in settings

**FlipScale approach:**
- ✅ Be transparent about notifications
- ✅ Allow easy opt-out
- ✅ Celebrate genuine wins only
- ✅ No shame, only motivation
- ✅ Reward consistency, not addiction

## Testing Behavioral Loops

```swift
func testBehavioralLoop_VictoryFeedback() {
    let user = User()

    // User logs a sale
    user.logSale(item)

    // Check that reward triggers
    XCertAssertEqual(user.receivedNotification, true)
    XCertAssertEqual(hapticFired, true)
    XCertAssertEqual(animationTriggered, true)

    // Check that streak updated
    XCertAssertEqual(user.currentStreak, 1)

    // Check that investment opportunity appears
    XCertAssertEqual(suggestedNextItems.isEmpty, false)
}

func testEthicalGuards_NoShamingMessages() {
    let user = User(itemsLogged: 0, daysInactive: 5)

    let message = generateEngagementMessage(for: user)

    // Should never shame
    XCertAssertFalse(message.contains("others"))
    XCertAssertFalse(message.contains("streak at risk"))
    XCertAssertFalse(message.contains("Don't break"))
}
```

## Real-World Example: Daily Session

```
9:00 AM: User opens app (trigger: motivation, $500 goal)
         Dashboard shows: 60% to monthly goal, 🔥 7-day streak

9:02 AM: User logs item sold for $89 (action)

9:03 AM: ✅ REWARD
         - "Nice flip! 🎉" notification
         - Haptic victory buzz
         - Profit number animates: $4,582 → $4,671
         - Milestone popup: "🎉 Crossed $4,500! You're crushing it"
         - 8-day streak shown

9:04 AM: INVESTMENT
         - App suggests: "Users who sold this category also sold..."
         - Shows similar items in inventory
         - User feels motivated to list the similar item

9:15 AM: User lists second item, dopamine loop repeats
```

## References

- Cialdini, R. (2021). *Influence: The Psychology of Persuasion*
- BJ Fogg: Behavioral Model (trigger → motivation → ability)
- Nir Eyal: *Hooked* (but ethical interpretation)
- Docs/Product/Design/BEHAVIORAL_LOOPS.md - Full spec

