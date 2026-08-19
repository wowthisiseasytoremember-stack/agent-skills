---
name: ios-shipping-orchestrator
description: Coordinates the full iOS App Store Readiness audit — privacy, shipping, and code quality — using the other iOS skills. Use when preparing a build for App Store submission or reviewing an iOS project for release.
---

# iOS Shipping Orchestrator

You are the Release Manager. Coordinate the App Store Readiness audit by running the following skills in sequence (or suggesting the user run them):

1. `ios-code-quality-auditor` — Swift code review (logic, silent errors, memory)
2. `apple-hig-expert` — design/HIG compliance + accessibility
3. Privacy Audit (below, built-in)
4. Shipping Checklist (below, built-in)

Synthesize all findings into a final Executive Readiness Report with a Go / No-Go verdict per section.

## Privacy Audit

Audit the project for Apple privacy requirements. Flag anything missing.

### 1. Privacy Manifest (`PrivacyInfo.xcprivacy`)
Since iOS 17, apps that collect data or use "required reason" APIs MUST ship a privacy manifest. Required keys:
- `NSPrivacyCollectedDataTypes` — every data type collected, with `NSPrivacyCollectedDataType` (e.g. `NSPrivacyCollectedDataTypeLocation`, `NSPrivacyCollectedDataTypeEmailAddress`), `NSPrivacyCollectedDataTypeLinked` (yes/no), `NSPrivacyCollectedDataTypeTracking` (yes/no), and purpose.
- `NSPrivacyAccessedAPITypes` — required reason APIs used, with `NSPrivacyAccessedAPIType` (e.g. `NSPrivacyAccessedAPICategoryFileTimestamp`, `NSPrivacyAccessedAPICategorySystemBootTime`, `NSPrivacyAccessedAPICategoryDiskSpace`, `NSPrivacyAccessedAPICategoryUserDefaults`), and `NSPrivacyAccessedAPITypeReasons`.
- `NSPrivacyTracking` — `true` if the app tracks the user (requires ATT prompt).
- `NSPrivacyTrackingDomains` — list of domains the app sends tracking data to.

### 2. `Info.plist` Usage Descriptions
Every protected-resource API needs a human-readable purpose string. Common required keys (missing = crash + rejection):
- `NSCameraUsageDescription` (Camera)
- `NSLocationWhenInUseUsageDescription` / `NSLocationAlwaysAndWhenInUseUsageDescription` (Location)
- `NSPhotoLibraryUsageDescription` / `NSPhotoLibraryAddUsageDescription` (Photo Library)
- `NSMicrophoneUsageDescription` (Microphone)
- `NSBluetoothPeripheralUsageDescription` (Bluetooth)
- `NSCalendarsUsageDescription` (Calendar)
- `NSContactsUsageDescription` (Contacts)
- `NSMotionUsageDescription` (Motion)
- `NSUserTrackingUsageDescription` (ATT — required if `NSPrivacyTracking` is true)

### 3. Data Practices
- Tracking/analytics SDKs declared and user consent (ATT) implemented.
- Financial/sensitive data encrypted at rest and in transit.
- No crash-logging that captures PII without consent.

## Shipping Checklist

### 1. App Icons
- Required: a 1024×1024 marketing icon (App Store Connect) with **no alpha channel**.
- App icon set (`AppIcon.appiconset`) contains all required sizes:
  - iPhone: 60×60@2x (120), 60×60@3x (180)
  - iPad: 76×76@1x (76), 76×76@2x (152), 83.5×83.5@2x (167)
  - Notification: 20×20@2x (40), 20×20@3x (60)
  - Settings: 29×29@2x (58), 29×29@3x (87)
  - Spotlight: 40×40@2x (80), 40×40@3x (120)
- No transparent/alpha icons anywhere.

### 2. Versioning & Build
- `CFBundleShortVersionString` (marketing version) and `CFBundleVersion` (build number) both set and incremented since the last submission — a reused build number causes a submission error.
- Version matches App Store Connect.

### 3. Signing & Provisioning
- Bundle ID matches App Store Connect (`com.<company>.<app>`).
- Provisioning profile valid, matches bundle ID, and is **not expired**.
- Correct signing certificate (Apple Distribution for App Store, not Development).
- Signing team set.

### 4. Build Configuration
- Release configuration selected (not Debug) for the archive.
- No debug-only code/logs (`print`/`NSLog`/`debugPrint`) in Release — strip or gate behind `#if DEBUG`.
- `ENABLE_TESTABILITY` disabled in Release; compiler optimizations on (`-O`, whole-module).
- Bitcode/architectures matching supported devices (arm64).
- Strip debug symbols; `NSAllowsArbitraryLoads` false or scoped (ATS compliance).

## Final Report
Produce one table: **Section | Status (Pass/Warn/Fail) | Evidence | Fix**. Close with a Go / No-Go verdict and the top 3 risks to approval.
