# Exclusion Rules for App Store Submission

To ensure an iOS project is "squeaky clean" for Apple's App Store submission, the following categories of files should be moved out of the main project structure and into an archive or documentation folder.

## 1. Internal Documentation & Notes
*   Markdown files containing roadmaps, todos, and project planning (`ROADMAP.md`, `TODO.md`, `PLAN_*.md`).
*   Architecture audits and state reports (`*_AUDIT.md`, `*_REPORT.md`).
*   Draft specifications and competitor analysis.

## 2. Tool-Specific History & Cache
*   AI tool history files (e.g., `.aider.chat.history.md`, `.aider.input.history`).
*   Terminal history files (`.zsh_history`, etc.).
*   Local configuration for development tools (`.aider.conf.yml`).

## 3. Development Scripts & Utilities
*   Shell scripts for local automation (`run.sh`, `setup_directories.sh`, `final_commit.sh`).
*   Python scripts for data processing or testing (`process_flippd_images.py`, `test_env.py`).
*   Node.js scripts used for local tasks.

## 4. Unused Assets & Remnants
*   Temporary directories (`app/` React Native remnants, `temp/`, `test_assets/`).
*   Placeholder files (0-byte files, `.DS_Store`).
*   Unused zip files or large archives (`Lexend.zip`).

## 5. Sensitive Information
*   `.env` files (should never be in the project root or tracked).
*   Any file containing API keys, secrets, or internal server URLs.

## 6. Recommended Structure
*   `_Archive/`: For all internal docs, notes, and legacy files.
*   `Scripts/`: For essential development scripts (if they must be kept).
*   `SmartFlipInventoryAR/`: The primary Xcode project folder containing only:
    *   `.swift` source files.
    *   `.xcassets` asset catalogs.
    *   `.lproj` localization files.
    *   `.plist` configuration files.
    *   `.entitlements` entitlement files.
    *   `.xcprivacy` privacy manifests.
