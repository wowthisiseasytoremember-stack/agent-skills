---
name: user-journey-validator
description: Validates that the codebase actually supports a specific user journey or roadmap flow, identifying gaps and "Roadmap Risks".
---
# User Journey Validator

**Purpose:** Check if the code actually supports the roadmap journey.

When provided with a Target User Journey (e.g., "Sign up → Enter Payment → Confirm"):
1. Trace this flow through the current directory structure, README, and relevant source files.
2. Identify any gaps where a step is documented or planned but no corresponding function, view, or logic exists in the code.
3. Report these missing steps as "Roadmap Risks" in plain English.
