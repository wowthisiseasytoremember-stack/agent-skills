# ZERO-FS HANDOFF PROMPTS — Sprint 2/3 + Persona Bible support

**Audience:** Frontier-reasoning agents with **zero filesystem access** to ichabod/surfacebook, but with `webfetch` tool and chat context.

**Tier ordering:** Frontier reasoning → Synthesis → Research. Each prompt has full schema + contract so the agent produces a precise deliverable.

**Reference pattern:** Each prompt references GitHub raw URLs (e.g. `raw.githubusercontent.com/wowthisiseasytoremember-stack/crawlkit/master/...`) since the zero-FS agent has no ichabod access.

---

# P1 — Reddit Age-Gate DOM Audit (time-sensitive)

**Tier:** Frontier reasoning
**Effort:** 1-2 hrs
**Why this matters:** `crawlkit/age_gates.py` (Sprint 3) ships a `RedditAgeGate` handler that clicks "I am 18+" via CSS selector. Reddit redesigns their age-gate periodically. If the selector breaks, `ssc_crawl.py` and the Reddit adapter in `ccarchive` fail silently (fail-open is good for prod but bad for visibility). An independent audit BEFORE Sprint 3 ships catches drift.

## Goal

Produce a **DOM audit report** of Reddit's current age-gate interstitial (2026), with: current selectors, drift history, fragility classification, and a recommended selector strategy for the new `RedditAgeGate.dismiss()` method.

## Context you need

Read these to ground yourself (use `webfetch` with raw GitHub URLs):
- `https://raw.githubusercontent.com/wowthisiseasytoremember-stack/crawlkit/master/docs/SPRINT-3-BROWSER-DETAIL.md` — proposed `RedditAgeGate` design (the CSS selector `button[type="submit"]`)
- `https://raw.githubusercontent.com/wowthisiseasytoremember-stack/ccarchive/master/ccarchive/browser.py` — current inline age-gate logic (what we're replacing)

**Do NOT assume** Reddit's age-gate DOM hasn't changed since the existing code was written. Verify against current state.

## Output schema

Output a single markdown document with these sections:

```markdown
# Reddit Age-Gate DOM Audit — 2026-MM-DD

## 1. Current state (as of audit date)
- **Interstitial URL pattern(s):** which URLs trigger the gate (e.g. /r/<sub> top.json HTML view, NSFW subs, /search?q=)
- **DOM structure:** HTML tree from entry to "I am 18+" button (paste real HTML, not paraphrased)
- **Button selector(s) tested:** try at least 3 candidates:
  - `button[type="submit"]`
  - `button:has-text("I am 18")` (Playwright text selector)
  - `[data-testid="age-gate-confirm"]` (if present)
  - any others you find
- **Which selector(s) actually worked:** with evidence (HTTP status after click, page content, network response)

## 2. Drift history (last 12 months)
- Search Reddit's frontend changes (search Reddit Design, r/redditdesign, Reddit status blog)
- Note any documented redesign of NSFW / age-gate flow
- Note any A/B test variants

## 3. Fragility classification
For each selector:
- **Stable** — unlikely to change (semantic markup, ARIA attributes, framework-standard)
- **At-risk** — likely to change (CSS classes, position-based selectors)
- **Brittle** — already changed once, will change again (text-based, generic element types)

## 4. Recommended selector strategy
For `RedditAgeGate.dismiss()` (Python async method):
```python
async def dismiss(self, page) -> bool:
    """Recommended strategy: list of fallbacks in order."""
    selectors = [
        # Primary: ...
        # Fallback 1: ...
        # Fallback 2: ...
    ]
    for sel in selectors:
        try:
            await page.wait_for_selector(sel, timeout=2000)
            await page.click(sel)
            return True
        except Exception:
            continue
    return False  # fail-open
```

Provide the actual selector list with rationale for ordering.

## 5. Test cases for the new implementation
- URL patterns that MUST trigger dismissal
- URL patterns that MUST NOT trigger dismissal
- Edge cases (login wall, MFA prompt, language variants)

## 6. Monitoring recommendation
How would we detect silent drift in prod? Suggest 1-2 probes (e.g. daily canary crawl that asserts the click succeeded; log scrape for "age gate not dismissed" events).
```

## Hard constraints

- DO NOT run a live Reddit interaction yourself (you're zero-FS, no Playwright)
- DO use webfetch on Reddit's HTML pages (top.json, /r/<sub>) to inspect current DOM
- DO NOT recommend selectors that depend on Reddit-specific URL patterns (use generic selectors)
- DO recommend fail-open behavior

## Verification criteria

- [ ] All 6 sections present
- [ ] At least 3 selectors tested with evidence
- [ ] Drift history cites specific sources (Reddit blog, GitHub issues, etc.)
- [ ] Recommended strategy has ≥3 fallback selectors with rationale
- [ ] Test cases are concrete URLs + expected outcomes
- [ ] Monitoring recommendation has at least one prod probe

## Example snippet

```markdown
## 1. Current state

URL `/r/stupidslutsclub` (NSFW, no auth) returns interstitial HTML containing:

```html
<section class="interstitial">
  <h1>You must be 18+ to enter</h1>
  <button type="submit" class="btn btn-primary">I am 18+</button>
</section>
```

**Selectors tested:**
| Selector | Works? | Notes |
|---|---|---|
| `button[type="submit"]` | ✓ | Clicks but only the first one on page (login button) |
| `button:has-text("I am 18")` | ✓ | Reliable, text-stable |
| `.interstitial button` | ✓ | Brittle — depends on `.interstitial` class |

**Recommended:** primary `button:has-text("I am 18")`; fallback `button.btn-primary` after `h1:has-text("18+")` parent.
```

---

# P2 — Sprint 2/3 Plan Critique (gap-finding on my own work)

**Tier:** Frontier reasoning
**Effort:** 2 hrs
**Why this matters:** I (orchestrator) wrote SPRINT-2-STORAGE-DETAIL.md and SPRINT-3-BROWSER-DETAIL.md. Independent review catches blind spots before we burn 10 hrs implementing.

## Goal

Produce a **structured critique** of the Sprint 2 + Sprint 3 plans, with: gaps, missing risks, ordering issues, and recommended additions.

## Context you need

- `https://raw.githubusercontent.com/wowthisiseasytoremember-stack/crawlkit/master/docs/SPRINT-2-STORAGE-DETAIL.md`
- `https://raw.githubusercontent.com/wowthisiseasytoremember-stack/crawlkit/master/docs/SPRINT-3-BROWSER-DETAIL.md`
- `https://raw.githubusercontent.com/wowthisiseasytoremember-stack/crawlkit/master/docs/PHASE-2-EXTRACTION-PLAN.md`

## Output schema

```markdown
# Sprint 2/3 Plan Critique — 2026-MM-DD

## Overall verdict
One of: READY-TO-SHIP / NEEDS-MINOR-FIXES / NEEDS-REWORK

## Per-sprint verdict
### Sprint 2 — STORAGE
- Verdict: ...
- Top 3 gaps: ...

### Sprint 3 — BROWSER + PROBE + AGE_GATES
- Verdict: ...
- Top 3 gaps: ...

## Cross-cutting issues
- Sprint ordering: should X happen before Y?
- Dependency risks: what if Phase 1 modules change?
- Missing coverage: tests we don't have

## Specific gaps (numbered list)

For each gap:
- **G{N}:** title
- **Severity:** critical / major / minor
- **Description:** what's missing or wrong
- **Suggested fix:** concrete recommendation

## Risks I missed (numbered list)

Same format as gaps but for risks.

## Additions recommended
- New test cases the plans don't include
- New docs sections
- New code paths to extract

## What I should NOT change
- Decisions that look wrong but are intentional (e.g. "we subclass CDPSession" might look like a wart but is required for backwards compat)
```

## Hard constraints

- DO NOT rewrite the plans (that's the orchestrator's job); find gaps, don't replace
- DO cite specific line numbers / sections when calling out issues
- DO consider backwards compat impact (ccarchive scripts, tests, CLI) — these plans affect production
- DO consider cross-project impact (Sprint 2 storage.py will be used by future projects — does the API support that?)

## Verification criteria

- [ ] Verdict given for both sprints
- [ ] At least 5 specific gaps cited with line references
- [ ] At least 3 missed risks identified
- [ ] Cross-cutting ordering analysis present
- [ ] "What NOT to change" section prevents accidental churn

---

# P3 — Persona Bible Section Drafts (heavy synthesis)

**Tier:** Synthesis
**Effort:** 4-6 hrs (depends on MMR slice plan feedback)
**Why this matters:** The persona bible (`docs/LUNA-PERSONA-BIBLE.md`) is the smut-gen thread's main deliverable. Sections 1-9 will be synthesized from catboy2/3 docs + matrix findings. Doing the synthesis now (before Sprint 2/3 ships) parallelizes with infra work.

## Goal

Draft **all 9 sections** of `docs/LUNA-PERSONA-BIBLE.md` based on catboy2/3 voice docs + Justin's voice corrections.

## Context you need

The catboy2/3 docs are at:
- `~/Projects/ccarchive/data/reddit_caption_snapshot_2026-08-17/` (matrix corpus) — NOT on GitHub (gitignored)
- `~/Downloads/extracted_catboy3/` and `~/Downloads/extracted_catboy2/` — also NOT on GitHub

**This is the issue.** The catboy2/3 docs are LOCAL on ichabod, not on GitHub. The zero-FS agent CANNOT access them.

**Two options:**
- A) If the orchestrator pastes the relevant content from catboy2/3 docs into this prompt's "Context" section, the agent has full ground truth
- B) Skip P3 entirely — too risky to synthesize voice docs without primary source

**Recommendation:** Run P3 ONLY if the orchestrator pastes the source material. Otherwise defer.

## Output schema (per section)

Each section of the bible has this shape:
```markdown
## Section N — <name>

### What
1-2 sentence summary.

### Where it comes from
- Source: catboy3/<doc>.md, lines X-Y
- OR: Justin's correction (2026-08-19)
- OR: catboy2/<doc>.md

### Rule statement
The rule, stated as a checkable constraint. Example: "Voice must use 'u'/'ur' instead of 'you'/'your' at >70% rate in lowercase-text-speak posts."

### Examples (canonical)
2-5 example phrases that nail the rule.

### Anti-patterns (canonical)
2-5 examples that violate the rule.

### Empirical backing (when matrix lands)
- Voice marker density in top-10%: <pending slice>
- Banned vocab rate: <pending slice>
- Engagement correlation: <pending slice>
```

The 9 sections (with current best understanding):
1. Voice register (first-person confessional GFE)
2. POV consistency
3. Sentence rhythm + vocabulary
4. Scene construction patterns
5. Hook patterns (8 templates)
6. Closing patterns
7. Banned + anti-patterns (descriptive female terms, non-consent, "Daddy" cap, pee)
8. Cross-pod tone delta (erotica-site vs Fanvue vs X vs Reddit)
9. LLM system prompt (consolidated)

## Hard constraints

- DO NOT add voice rules not in the source material
- DO cite every claim with `[source: catboy3/rivers_story_01.md line 47]` format
- DO distinguish "Justin-confirmed" rules from "catboy inferred" rules
- DO use `pending` placeholders for sections needing matrix data

## Verification criteria

- [ ] All 9 sections drafted
- [ ] Every claim has a source citation
- [ ] Justin's corrections are explicitly marked (`[Justin-confirmed]`)
- [ ] Empirical sections have `pending` placeholders, not made-up numbers
- [ ] Each section follows the schema (What / Where / Rule / Examples / Anti-patterns / Empirical)

---

# P4 — Female-Body-Term Regex Validation (precision frontier work)

**Tier:** Frontier reasoning (precision)
**Effort:** 2 hrs
**Why this matters:** The matrix extractor uses regex to classify "descriptive" vs "aspirational" female body terms. False positives/negatives directly bias the persona bible's empirical findings. Worth an independent regex audit.

## Goal

Audit the regex patterns in `undercontent/scripts/matrix_extract.py` and produce: test cases with expected outputs, false-positive/negative analysis, suggested revisions.

## Context you need

- `https://raw.githubusercontent.com/wowthisiseasytoremember-stack/undercontent/master/scripts/matrix_extract.py` — find the `FEMALE_ASPIRATIONAL` and `FEMALE_DESCRIPTIVE` regex constants

## Output schema

```markdown
# Female-Body-Term Regex Audit — 2026-MM-DD

## Test corpus
A list of 30+ test sentences, each with expected classification:
- "do i look like a girl in this?" → aspirational
- "her tits were huge" → descriptive
- ...etc.

## Current regex behavior
For each test sentence, output:
- Sentence
- FEMALE_DESCRIPTIVE match count
- FEMALE_ASPIRATIONAL match count
- Classified register (descriptive / aspirational / mixed / none)
- Expected register
- PASS / FAIL

## Failure analysis
- List sentences where current classification FAILS the expected
- Root cause for each failure
- False positives (current says "descriptive" but shouldn't be)
- False negatives (current says "none" but should be "aspirational")

## Suggested regex revisions
```python
# Current
FEMALE_ASPIRATIONAL = re.compile(...)
FEMALE_DESCRIPTIVE = re.compile(...)

# Revised
FEMALE_ASPIRATIONAL = re.compile(...)  # addresses: <gap 1>, <gap 2>
FEMALE_DESCRIPTIVE = re.compile(...)   # addresses: <gap 3>
```

## Justin's 5 canonical examples (verify these classify correctly)
- "do i look like a girl in this?"
- "would you fuck me wearing this?"
- "do i look better in this than your gf?"
- "my friend told me i have girls hips"
- "would i look cute with tiny tits lol"

For each: regex output + verification.

## New edge cases worth adding
- "i feel pretty today" — should this count as aspirational?
- "she said my hips look like a girl's" — reported speech vs direct
- "would u rather date me or your ex" — comparison but not female-body
- 5+ more you generate
```

## Hard constraints

- DO NOT change the regex without showing the test case that demonstrates the bug
- DO use real test sentences (not made-up)
- DO include both true positives (correct classification) AND false positives (wrong classification)
- DO consider context (e.g. "girl" alone might not be female-body-term — it's just the word)

## Verification criteria

- [ ] 30+ test sentences with expected outputs
- [ ] Current regex behavior documented for each
- [ ] At least 5 failure cases with root cause
- [ ] Suggested regex revisions include diff from current
- [ ] Justin's 5 canonical examples all pass
- [ ] New edge cases surface (not all current behavior is correct)

---

# P5 — PRAW vs JSON API Rate Limit Analysis (2026 research)

**Tier:** Research + recommendation
**Effort:** 1-2 hrs
**Why this matters:** `ccarchive/scripts/crawl_json_api.py` uses Reddit cookies for auth. Reddit can change auth requirements anytime. PRAW is the official library. Need to know: stay with cookies, migrate to PRAW, or both?

## Goal

Produce a 2026-current comparison of Reddit auth methods (cookies, PRAW, OAuth) for read-only corpus crawling. Recommendation + migration plan.

## Context you need

- `https://raw.githubusercontent.com/wowthisiseasytoremember-stack/ccarchive/master/scripts/crawl_json_api.py` — current cookies-based implementation
- `https://raw.githubusercontent.com/wowthisiseasytoremember-stack/reputation-mvp/master/src/reputation_mvp/scrapers/reddit.py` — existing PRAW implementation in portfolio
- Reddit API docs: https://www.reddit.com/dev/api/
- Reddit Rules: https://www.redditinc.com/policies/data-api-terms

## Output schema

```markdown
# Reddit Auth Comparison (2026) — for corpus crawling

## TL;DR recommendation
One paragraph: stay / migrate / hybrid, with reasoning.

## Method comparison

### Method 1: Cookie auth (current state)
- Rate limits (per minute, per day): cite docs
- Cost: free
- Reliability (session expiry, ban risk): cite Reddit policies
- Privacy: cookies include session token
- Implementation complexity (lines of code)

### Method 2: PRAW (official Python wrapper)
- Same dimensions

### Method 3: OAuth2 script app
- Same dimensions

### Method 4: Third-party (Apify, etc.)
- Same dimensions

## Recommendation
- Short-term (next 6 months): ...
- Medium-term (6-12 months): ...
- Long-term (12+ months): ...

## Migration plan (if any)
- Code changes required
- Files affected
- Backwards compat approach
- Risk assessment

## Open questions for Justin
- Bullet list of decisions only he can make
```

## Hard constraints

- DO use 2026-current data (Reddit changes policies frequently — verify against current docs)
- DO include rate limit NUMBERS, not just "rate limited"
- DO consider that `crawl_json_api.py` already works — recommendation should be cost/benefit, not "must migrate"
- DO NOT recommend any approach that violates Reddit's Terms of Service

## Verification criteria

- [ ] All 4 methods compared across 5 dimensions
- [ ] Recommendation has short/medium/long-term
- [ ] Migration plan (if any) lists specific files + lines
- [ ] Citations to Reddit policy pages present
- [ ] Open questions are specific to Justin's context

---

# P6 — SQLite WAL + Python Multiprocessing Edge Cases (failure modes)

**Tier:** Research + frontier
**Effort:** 2 hrs
**Why this matters:** Sprint 2 adds 2 new concurrency tests to `crawlkit/tests/test_concurrent_writes.py`. Edge cases that aren't tested = production bugs waiting to happen. Independent edge-case enumeration improves test coverage.

## Goal

Enumerate SQLite WAL mode edge cases when used with Python multiprocessing. Suggest additional tests for Sprint 2.

## Context you need

- `https://raw.githubusercontent.com/wowthisiseasytoremember-stack/crawlkit/master/docs/SPRINT-2-STORAGE-DETAIL.md` — proposed concurrency tests
- SQLite WAL docs: https://www.sqlite.org/wal.html
- Python multiprocessing docs: https://docs.python.org/3/library/multiprocessing.html
- SQLite Python docs: https://docs.python.org/3/library/sqlite3.html

## Output schema

```markdown
# SQLite WAL Multiprocessing Edge Cases

## Edge case enumeration
For each edge case:
- **EC{N}:** title
- **Trigger condition:** what creates this scenario
- **Behavior:** what SQLite does
- **Test recommendation:** new test to add to Sprint 2
- **Severity:** critical / major / minor

## Categories to cover
1. Process forking + WAL mode
2. SQLite version compatibility (3.7+, 3.40+, 3.45+)
3. Python version compatibility (3.10, 3.11, 3.12)
4. Connection pool exhaustion
5. Long-running writers blocking readers
6. Disk-full / I/O error scenarios
7. Network filesystem (NFS) behavior
8. Process death mid-transaction
9. Schema migration during writes
10. Backup during active writes (sqlite3 .backup API)

## Specific test cases to add
Concrete Python snippets for 5-10 additional tests beyond the 2 already planned.

## Risk ranking
Top 5 most likely production failures with mitigations.
```

## Hard constraints

- DO focus on REAL edge cases (production-relevant), not theoretical ones
- DO include code snippets for suggested tests
- DO cite SQLite/Python version where behavior changes
- DO NOT recommend switching SQLite libraries (e.g. apsw) without strong justification

## Verification criteria

- [ ] At least 10 edge cases enumerated
- [ ] Each has trigger + behavior + test recommendation + severity
- [ ] At least 5 concrete test snippets provided
- [ ] Top 5 risks ranked with mitigations
- [ ] Version-specific behavior noted where relevant

---

# P7 — Cross-Project Migration Guide for crawlkit (synthesis)

**Tier:** Synthesis (strategy)
**Effort:** 3-4 hrs
**Why this matters:** crawlkit 0.2.0 will ship after Sprint 4. Phase 3 (cross-project migration) needs a playbook. aquascrape, fish-atlas-scraper, job-search, shame-seo are the named candidates. Independent strategy review helps prioritize.

## Goal

Produce a per-project migration plan for crawlkit adoption. For each candidate project: what's reusable, what needs rewrite, what stays custom, recommended migration order.

## Context you need

- `https://raw.githubusercontent.com/wowthisiseasytoremember-stack/crawlkit/master/README.md`
- `https://raw.githubusercontent.com/wowthisiseasytoremember-stack/crawlkit/master/AGENTS.md`
- `https://raw.githubusercontent.com/wowthisiseasytoremember-stack/crawlkit/master/docs/PHASE-2-EXTRACTION-PLAN.md`
- For each candidate project, fetch their README/AGENTS via `webfetch`:
  - `aquascrape`: `https://raw.githubusercontent.com/wowthisiseasytoremember-stack/aquascrape/master/AGENTS.md` (if exists; else README)
  - `fish-atlas-scraper`: same pattern
  - `job-search`: same pattern
  - `shame-seo`: same pattern
  - (These repos may not all be public — check first; if private, note and infer from project name)

## Output schema

```markdown
# crawlkit Cross-Project Migration Guide

## Recommended migration order
Rank 4 projects by ROE for adopting crawlkit:
- #1: <project> — <one-line reason>
- #2: <project> — <one-line reason>
- ...

## Per-project plan

### Project: aquascrape
- **Current state:** <1-paragraph summary>
- **Reusable from crawlkit:** bulleted list with line numbers
- **Needs rewrite:** bulleted list
- **Stays custom:** bulleted list
- **Migration effort:** hours estimate
- **Risk:** what could break
- **Migration steps:** numbered list
- **First PR:** smallest viable migration

(Repeat for each project)

## Shared patterns
Patterns common across all migrations:
- Browser session setup
- Adapter registration
- Storage backend choice
- CLI integration
- Test migration

## What NOT to migrate
For each project, what's worth keeping custom (domain logic, niche-specific stuff).

## Migration validation
How to know a project has been successfully migrated:
- All crawlkit tests pass against the project's data
- Project-specific tests still pass
- Performance parity or improvement vs pre-migration
- Backwards compat with existing project consumers
```

## Hard constraints

- DO NOT recommend migration if cost > benefit (be honest)
- DO consider the project's domain (aquascrape is hobbyist; shame-seo is monetization — different stakes)
- DO consider that the project owner (Justin) may have other priorities
- DO include rollback plans

## Verification criteria

- [ ] 4 projects ranked by ROE with one-line reasoning
- [ ] Each project has all 8 sub-sections
- [ ] "What NOT to migrate" sections present
- [ ] Migration validation criteria are concrete (not vague)
- [ ] Rollback plans included

---

# Quick-reference: which prompt for which situation

| If you have time for... | Run prompt |
|---|---|
| 1-2 hrs, time-sensitive | P1 (Reddit DOM audit) |
| 2 hrs, design quality | P2 (Sprint plan critique) |
| 4-6 hrs, high-ROE prep | P3 (Persona bible drafts) — REQUIRES source paste |
| 2 hrs, precision | P4 (Regex audit) |
| 1-2 hrs, future-proofing | P5 (Auth comparison) |
| 2 hrs, test coverage | P6 (SQLite edge cases) |
| 3-4 hrs, strategy | P7 (Migration guide) |

**Order to run if doing all:** P1 → P2 → P5 → P4 → P6 → P7 → P3 (P3 last because it benefits from P1-P7's outputs)
