---
name: flipscale-zero-knowledge-guardian
description: Enforces Zero-Knowledge privacy architecture. Use to ensure all user data is iCloud-only, on-device encrypted, and PII-free.
---

# FlipScale Zero-Knowledge Guardian

The "Protector" of user privacy. FlipScale is built on the promise that "The developer cannot see your sales." This skill ensures that promise is technically absolute.

## Privacy Invariants
1.  **iCloud-Only Sync**: No external database (Firebase, AWS, etc.). Use SwiftData + CloudKit exclusively.
2.  **PII-Free Storage**: Never store real names, emails, or physical addresses in the app's local records.
3.  **On-Device Encryption**: Use AES-256 for financial ledger fields before they sync to the cloud.
4.  **Local Biometrics**: FaceID/TouchID must happen locally on-device, never touching a server.

## Audit Workflow
When reviewing code:
- Check `UserPreferences` for any fields that could identify the human.
- Verify `SyncActor` logic ensures CloudKit is the sole destination.
- Ensure all API calls (e.g., Vision Hub) are hashed and anonymized.

---

## Iron Law of Privacy
**Your data, your device.** We are an operating system, not a data broker. If it identifies the user, it doesn't belong in our index.
