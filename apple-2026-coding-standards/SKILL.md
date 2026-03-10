---
name: apple-2026-coding-standards
description: Use when writing Swift code to ensure Swift 6 strict concurrency, modern concurrency patterns, actor model safety, and compliance with FlipScale architecture standards
---

# Apple 2026 Coding Standards

Enforces Swift 6 strict concurrency model, actor-based architecture, and modern async/await patterns. Eliminates race conditions, ensures thread-safe code, and prevents unsafe concurrency antipatterns.

## Core Swift 6 Principles

- **Strict Concurrency Checking:** Compile with `-strict-concurrency=complete`
- **Actors for Shared State:** Never use `DispatchQueue` or locks for mutable state
- **@MainActor UI Sync:** All UI mutations must happen on main thread
- **Sendable Conformance:** Data crossing concurrency boundaries must be `Sendable`
- **async/await Only:** No callbacks, closures, or completion handlers
- **AsyncStream for Sequences:** Replace delegate patterns with AsyncStream
- **No Force Unwraps:** Use `try?`, `guard let`, or `if let` for optionals
- **Data Isolation:** Each actor owns its mutable state exclusively

## Quick Reference: Swift 6 Concurrency Patterns

| Pattern | Use Case | Correct Approach |
|---------|----------|-----------------|
| **Main Thread UI** | Update SwiftUI views, animation, alerts | `@MainActor` on ViewModel |
| **Shared State** | Database, cache, ledger | `actor` type with `await` access |
| **Background Work** | Network, file I/O, computation | `Task { await }` in background pool |
| **Data Flow** | Events, sequences over time | `AsyncStream<Value>` |
| **Concurrent Tasks** | Parallel network calls | `async let x = task1(); async let y = task2()` |
| **Thread Checking** | Debug concurrency bugs | `Dispatch.assert(queue: .main)` removed; use `MainActor` instead |

## Complete Code Example: Swift 6 Safe Actor Pattern

This CoreFinancial-like pattern is the gold standard for FlipScale financial models:

```swift
import Foundation

// ✅ CORRECT: Sendable data model
struct LedgerEntry: Sendable, Codable {
    let id: UUID
    let amount: Decimal
    let timestamp: Date
    let description: String
}

// ✅ CORRECT: Actor for financial state isolation
actor FinancialLedger {
    private var entries: [LedgerEntry] = []
    private var currentBalance: Decimal = Decimal(0)

    // Isolated state - safe from race conditions
    nonisolated let id: UUID

    init(id: UUID = UUID()) {
        self.id = id
    }

    // Public interface: async methods only
    func recordEntry(_ entry: LedgerEntry) async throws {
        guard entry.amount != 0 else { throw LedgerError.zeroAmount }
        entries.append(entry)
        currentBalance += entry.amount
    }

    func getBalance() async -> Decimal {
        currentBalance
    }

    func getAllEntries() async -> [LedgerEntry] {
        entries  // Safe copy due to Sendable
    }

    func reconcile() async throws -> Decimal {
        let calculatedBalance = entries.reduce(Decimal(0)) { sum, entry in
            sum + entry.amount
        }
        guard calculatedBalance == currentBalance else {
            throw LedgerError.reconciliationMismatch
        }
        return currentBalance
    }
}

// ✅ CORRECT: MainActor ViewModel for UI coordination
@MainActor
final class FinancialViewModel: ObservableObject {
    @Published var displayBalance: String = "$0.00"
    @Published var entries: [LedgerEntry] = []
    @Published var isLoading: Bool = false
    @Published var errorMessage: String? = nil

    private let ledger: FinancialLedger

    init(ledger: FinancialLedger) {
        self.ledger = ledger
    }

    // @MainActor ensures UI updates happen on main thread
    func addExpense(_ amount: Decimal, description: String) {
        isLoading = true
        errorMessage = nil

        Task {
            do {
                let entry = LedgerEntry(
                    id: UUID(),
                    amount: -amount,  // Negative for expense
                    timestamp: Date(),
                    description: description
                )

                // Cross actor boundary: await required
                try await ledger.recordEntry(entry)

                // Update UI after actor operation completes
                let newBalance = await ledger.getBalance()
                displayBalance = formatCurrency(newBalance)

                // Refresh entries list
                entries = await ledger.getAllEntries()

            } catch {
                errorMessage = error.localizedDescription
            }

            isLoading = false
        }
    }

    func refreshBalance() {
        Task {
            let balance = await ledger.getBalance()
            displayBalance = formatCurrency(balance)
            entries = await ledger.getAllEntries()
        }
    }

    private func formatCurrency(_ amount: Decimal) -> String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .currency
        formatter.currencyCode = "USD"
        return formatter.string(from: amount as NSDecimalNumber) ?? "$0.00"
    }
}

// ✅ CORRECT: AsyncStream for event streams (replace delegates)
actor FinancialEventStream {
    typealias Listener = (FinancialEvent) -> Void

    private var stream: AsyncStream<FinancialEvent>?
    private var continuation: AsyncStream<FinancialEvent>.Continuation?

    func subscribe() -> AsyncStream<FinancialEvent> {
        let (stream, continuation) = AsyncStream<FinancialEvent>.makeStream()
        self.stream = stream
        self.continuation = continuation
        return stream
    }

    func emit(_ event: FinancialEvent) {
        continuation?.yield(event)
    }

    func close() {
        continuation?.finish()
    }
}

// ✅ CORRECT: Sendable enum for events
enum FinancialEvent: Sendable {
    case entryAdded(LedgerEntry)
    case balanceChanged(Decimal)
    case reconciliationCompleted(success: Bool)
}

// ✅ CORRECT: Using the stream in a Task
func listenToFinancialEvents(from eventStream: FinancialEventStream) async {
    let events = await eventStream.subscribe()

    for await event in events {
        switch event {
        case .entryAdded(let entry):
            print("Entry recorded: \(entry.description)")
        case .balanceChanged(let newBalance):
            print("Balance updated: \(newBalance)")
        case .reconciliationCompleted(let success):
            print("Reconciliation: \(success ? "Success" : "Failed")")
        }
    }
}

enum LedgerError: Error, LocalizedError {
    case zeroAmount
    case reconciliationMismatch

    var errorDescription: String? {
        switch self {
        case .zeroAmount:
            return "Entry amount cannot be zero"
        case .reconciliationMismatch:
            return "Ledger balance does not match calculated total"
        }
    }
}
```

## @MainActor Usage Guidelines

### When to Use @MainActor

```swift
// ✅ CORRECT: UI-coordinating ViewModels
@MainActor
final class LedgerViewModel {
    @Published var balance: Decimal

    // All methods run on main thread automatically
    func updateBalance() async {
        // Safe to update @Published properties directly
        let newBalance = await calculateNewBalance()
        self.balance = newBalance  // No race condition
    }
}

// ✅ CORRECT: SwiftUI Views use @MainActor implicitly
struct LedgerView: View {
    @StateObject private var viewModel: LedgerViewModel

    var body: some View {
        // All UI updates are on main thread by default
        Text("Balance: \(viewModel.balance)")
    }
}
```

### When NOT to Use @MainActor

```swift
// ❌ WRONG: Blocking I/O on main thread
@MainActor
final class DataService {
    func loadData() {
        let data = try JSONDecoder().decode(...)  // BLOCKS MAIN THREAD
    }
}

// ✅ CORRECT: Keep background work off main thread
actor DataService {
    func loadData() async throws -> Data {
        // Runs in background, returns safely to caller
        return try JSONDecoder().decode(...)
    }
}
```

## AsyncStream Best Practices

### Replace Delegates with AsyncStream

```swift
// ❌ OLD: Delegate pattern (unsafe, hard to test)
protocol DownloadDelegate: AnyObject {
    func downloadDidStart()
    func downloadDidProgress(_ progress: Double)
    func downloadDidComplete(_ data: Data)
    func downloadDidFail(_ error: Error)
}

class Downloader {
    weak var delegate: DownloadDelegate?
    func start() { ... }
}

// ✅ NEW: AsyncStream (safe, composable, testable)
actor Downloader {
    typealias Progress = (current: Int64, total: Int64)

    func download(url: URL) -> AsyncStream<DownloadEvent> {
        AsyncStream { continuation in
            Task {
                do {
                    continuation.yield(.started)

                    let (data, response) = try await URLSession.shared.data(from: url)
                    continuation.yield(.completed(data))
                    continuation.finish()

                } catch {
                    continuation.yield(.failed(error))
                    continuation.finish()
                }
            }
        }
    }
}

enum DownloadEvent: Sendable {
    case started
    case progress(current: Int64, total: Int64)
    case completed(Data)
    case failed(Error)
}

// Usage
let downloader = Downloader()
for await event in await downloader.download(url: url) {
    switch event {
    case .started:
        print("Download started")
    case .progress(let current, let total):
        print("Progress: \(current)/\(total)")
    case .completed(let data):
        print("Download complete: \(data.count) bytes")
    case .failed(let error):
        print("Download failed: \(error)")
    }
}
```

### AsyncStream for Polling/Retry Logic

```swift
// ✅ CORRECT: AsyncStream for periodic operations
actor FinancialSyncService {
    func syncWithRetry(url: URL, maxRetries: Int = 3) -> AsyncStream<SyncEvent> {
        AsyncStream { continuation in
            Task {
                var retries = 0

                while retries < maxRetries {
                    do {
                        let data = try await fetchData(url: url)
                        continuation.yield(.success(data))
                        continuation.finish()
                        return

                    } catch {
                        retries += 1
                        continuation.yield(.retry(attempt: retries))

                        if retries >= maxRetries {
                            continuation.yield(.failed(error))
                            continuation.finish()
                            return
                        }

                        try await Task.sleep(for: .seconds(retries * 2))
                    }
                }
            }
        }
    }
}

enum SyncEvent: Sendable {
    case success(Data)
    case retry(attempt: Int)
    case failed(Error)
}
```

## Common Mistakes to Avoid

### ❌ Mistake 1: DispatchQueue for State (WRONG)

```swift
// ❌ OLD PATTERN - Never do this
class BadLedger {
    private let queue = DispatchQueue(label: "ledger")
    private var balance: Decimal = 0

    func addAmount(_ amount: Decimal) {
        queue.sync {
            balance += amount  // Uses locks - SLOW and DEADLOCK PRONE
        }
    }
}

// ✅ CORRECT - Use actor instead
actor GoodLedger {
    private var balance: Decimal = 0

    func addAmount(_ amount: Decimal) async {
        balance += amount  // Actor isolation - SAFE and FAST
    }
}
```

### ❌ Mistake 2: Callbacks Instead of async/await

```swift
// ❌ OLD PATTERN - Callback hell
func fetchBalance(completion: @escaping (Decimal?, Error?) -> Void) {
    URLSession.shared.dataTask(with: url) { data, _, error in
        if let error = error {
            completion(nil, error)
            return
        }
        // Hard to test, pyramid of doom, escaping closure memory issues
        completion(Decimal(0), nil)
    }.resume()
}

// ✅ CORRECT - Use async/await
func fetchBalance() async throws -> Decimal {
    let (data, _) = try await URLSession.shared.data(from: url)
    return Decimal(0)  // Easy to read, easy to test, no memory leaks
}
```

### ❌ Mistake 3: Unsafe Sendable (WRONG)

```swift
// ❌ WRONG - Class not Sendable across actor boundaries
class MutableLedger {  // Not thread-safe!
    var entries: [LedgerEntry] = []
}

@MainActor
func processBatch(ledger: MutableLedger) {  // COMPILER ERROR
    // Can't pass mutable class across main/background boundary
}

// ✅ CORRECT - Struct or class conforming to Sendable
struct ImmutableEntry: Sendable {
    let id: UUID
    let amount: Decimal
}

@MainActor
func processBatch(entries: [ImmutableEntry]) {  // OK - Sendable
    // Can safely pass immutable struct across boundaries
}
```

### ❌ Mistake 4: Missing Actor Isolation

```swift
// ❌ WRONG - Race condition on `balance`
actor BadLedger {
    var balance: Decimal = 0

    nonisolated func getBalance() -> Decimal {  // ⚠️ nonisolated bypasses actor isolation!
        return balance  // RACE CONDITION - can be mutated while reading
    }
}

// ✅ CORRECT - Mark as async to maintain isolation
actor GoodLedger {
    var balance: Decimal = 0

    func getBalance() async -> Decimal {
        return balance  // Safe - atomic read
    }
}
```

### ❌ Mistake 5: Force Unwraps in Concurrent Code

```swift
// ❌ WRONG - Crashes on nil
actor BadProcessor {
    func process(_ data: Data?) async {
        let json = try JSONDecoder().decode(
            LedgerEntry.self,
            from: data!  // CRASH if nil
        )
    }
}

// ✅ CORRECT - Guard against nil
actor GoodProcessor {
    func process(_ data: Data?) async throws {
        guard let data = data else {
            throw ProcessingError.noData
        }

        let json = try JSONDecoder().decode(
            LedgerEntry.self,
            from: data
        )
    }
}
```

## Strict Concurrency Compilation Errors

When you see these errors with `-strict-concurrency=complete`, here's how to fix them:

| Error | Cause | Fix |
|-------|-------|-----|
| `sending 'self' requires that 'ViewModel' conforms to 'Sendable'` | Non-Sendable class crossing actor boundary | Wrap in `@MainActor` or make `final` |
| `data is not concurrent-value-safe; this is an error in Swift 6` | Mutable class without isolation | Convert to `struct` or `actor` |
| `call to actor-isolated instance method 'method()' in a nonisolated context requires 'async'` | Forgot `await` | Add `await` or wrap in `Task` |
| `cannot assign to property: setter is not available in actor-isolated context` | Trying to mutate from `nonisolated` | Remove `nonisolated` or make method isolated |
| `cannot capture mutable 'self' in closure` | Closure capturing mutable actor state | Use `@Sendable` closure or refactor |

## Swift 6 Migration Checklist

Before committing concurrency code:

- [ ] Compile with `-strict-concurrency=complete` - zero errors
- [ ] All mutable state is in `actor` types
- [ ] All UI updates use `@MainActor`
- [ ] No `DispatchQueue`, `NSLock`, or `pthread_mutex` for state
- [ ] All `async` functions are `await`-ed at call site
- [ ] No callbacks - use `async/await` or `AsyncStream`
- [ ] All data crossing boundaries conforms to `Sendable`
- [ ] No `!` force unwraps - use `try?`, `guard`, or `if let`
- [ ] @Published only in @MainActor classes
- [ ] No `weak self` - actors don't have retain cycles

## Testing Concurrent Code

```swift
// ✅ CORRECT: Test actor isolation
func testConcurrentAccess() async {
    let ledger = FinancialLedger()

    // Concurrent tasks on same actor - safe
    async let task1 = ledger.recordEntry(entry1)
    async let task2 = ledger.recordEntry(entry2)
    async let task3 = ledger.recordEntry(entry3)

    _ = try await (task1, task2, task3)

    let balance = await ledger.getBalance()
    XCTAssertEqual(balance, Decimal(300))
}

// ✅ CORRECT: Test MainActor updates
@MainActor
func testViewModelUpdate() async {
    let ledger = FinancialLedger()
    let viewModel = FinancialViewModel(ledger: ledger)

    // @MainActor ensures UI updates happen synchronously in test
    viewModel.displayBalance = "$0.00"
    XCTAssertEqual(viewModel.displayBalance, "$0.00")
}
```

## Anti-Patterns Forbidden in Swift 6

| Anti-Pattern | Why Forbidden | Alternative |
|--------------|---------------|-------------|
| `var shared = MyClass()` (global mutable) | Race conditions in concurrent code | `actor GlobalState { ... }` |
| `DispatchQueue.main.sync { }` | Deadlocks, blocks main thread | Use `@MainActor` |
| `weak var delegate: Delegate?` callbacks | Unsafe memory, hard to reason about | Use `AsyncStream<Event>` |
| `@escaping` closures with mutable capture | Memory safety issues | Use `async/await` functions |
| `URLSession` with `completionHandler` | Old callback pattern | Use `async/await` API |
| `OperationQueue` for state sync | Legacy, heavyweight | Use `actor` for state, Tasks for work |
| Manual `NSLock` protection | Error-prone, slow | Let actor handle isolation |
| Force unwraps `!` on optionals | Crash risk in production | Use `try?`, `guard let`, `??` |

## References

- [Swift Concurrency Documentation](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency)
- [SE-0366: Swift Strict Concurrency Checking](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0366-swift-strict-concurrency-checking.md)
- [Actor Model in Swift](https://developer.apple.com/videos/play/wwdc2021/10133/)
- Apple 2026 Architect - /Docs/Development/APPLE_2026_ARCHITECTURE.md
- Code Quality Guide - /Docs/Technical/CODE_QUALITY_GUIDE.md

