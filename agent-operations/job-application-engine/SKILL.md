---
name: job-application-engine
description: "Deterministic happy-path engine for submitting job applications across Greenhouse (Remix/React-Select), Ashby (React controlled/YesNo/Autocomplete), BambooHR, and Lever via live Chrome CDP. Contains exact DOM recipes, selector workarounds, React state triggers, reCAPTCHA callbacks, candidate truth boundaries, and proof-of-submission logging. Use when executing job applications or automating ATS submissions."
version: 1.2.0
metadata:
  tags: [job-search, ats-automation, greenhouse, ashby, bamboohr, lever, browser-automation, playwright, cdp]
---

# Job Application Engine — Happy-Path ATS Submission Playbook

This skill defines the battle-tested, deterministic automation recipes for submitting job applications directly through live browser automation (Playwright connected to Chrome CDP on `http://127.0.0.1:9333`).

It is designed so that any agent (even context-constrained or "dumber" agents) can follow the happy-path steps without falling into the common traps of modern Applicant Tracking Systems (ATS).

---

## 1. Core Architecture & Runtime Primitives

### Chrome CDP Connection, Discovery & Tab Lifecycle
Never launch a headless Chromium from scratch if a persistent user profile is active. Always verify CDP health on port 9333 using dynamic binary resolution (`shutil.which`) and connect to the existing Chrome instance to maintain authentication sessions, human cookies, and bypass bot protections.

Always manage newly opened tabs inside `try ... finally` blocks to prevent tab accumulation and memory leaks across batch submissions.

```python
import asyncio
from playwright.async_api import async_playwright
from cdp_health import ensure_cdp_ready

async def get_browser_page(cdp_url="http://127.0.0.1:9333", keep_open=False):
    # 1. Pre-flight health check with dynamic binary discovery
    if not ensure_cdp_ready(9333, auto_launch=False):
        raise RuntimeError("Chrome CDP daemon not reachable on port 9333.")

    # 2. Connect over CDP
    p = await async_playwright().start()
    browser = await p.chromium.connect_over_cdp(cdp_url)
    context = browser.contexts[0]
    
    # 3. CRITICAL: Do NOT clobber active human-solve tabs (e.g. Lever hCaptcha, logins)!
    target_page = None
    new_page_created = False
    for page in context.pages:
        if "lever.co" not in page.url and "about:blank" in page.url:
            target_page = page
            break
    if not target_page:
        target_page = await context.new_page()
        new_page_created = True

    # 4. Auto-accept unexpected dialogs to prevent freezing
    target_page.on("dialog", lambda dialog: asyncio.create_task(dialog.accept()))
        
    return p, browser, target_page, new_page_created
```

---

## 2. Platform Recipes & Critical Gotchas

### A. Ashby (`jobs.ashbyhq.com`)

Ashby is built on React with custom controlled inputs, hidden anti-bot heuristics, and non-standard form controls.

#### 1. React Controlled Inputs (Never use `.value = ...`)
Setting element `.value = ...` in JavaScript will **NOT** update React component state. When you click Submit, the form acts as if fields are empty.
* **Fix**: Use Playwright's `page.fill(selector, text)` followed by `page.press(selector, 'Tab')`.
* **Gotcha**: Do NOT attempt `HTMLInputElement.prototype.value` hacks on `textarea` (it throws `TypeError: Illegal invocation`).

#### 2. Numeric Selector Syntax Error
Ashby uses field UUIDs as IDs (e.g. `id="33d03287-45bf-4e0a-bbe1-0c8ec4b42a71"`).
* **Trap**: `page.click("#33d03...")` throws `SyntaxError: Failed to execute 'querySelector' on 'Document': '#33d03...' is not a valid selector.`
* **Fix**: ALWAYS use attribute bracket selectors: `page.click('[id="33d03287-45bf-4e0a-bbe1-0c8ec4b42a71"]')`.

#### 3. The Location Autocomplete Spam Trap
Submitting an Ashby application without selecting from the Location dropdown flags the submission as "possible spam" and silently drops or rejects it.
* **Fix**:
  ```python
  # Must type slowly, wait for popup results, and click
  loc_input = page.locator('input.ashby-application-form-input-autocomplete, input[placeholder*="location" i]')
  if await loc_input.count() > 0:
      await loc_input.first.click()
      await loc_input.first.type("Garden Grove, CA", delay=40)
      await asyncio.sleep(1.0)
      popup_opt = page.locator('.ashby-application-form-input-autocomplete-popup-result, [role="option"]')
      if await popup_opt.count() > 0:
          await popup_opt.first.click()
      else:
          await page.keyboard.press("Enter")
  ```

#### 4. Scoped Yes/No Question Buttons (Prevent Global Collision)
Ashby boolean questions use `<button>` elements with class `button.ashby-application-form-input-yesno-option`.
* **Trap**: A global query `page.click('button:has-text("Yes")')` clicks the *first* Yes button on the entire page, causing conflicts across multiple questions (e.g. Work Auth vs Visa Sponsorship vs Relocation).
* **Fix**: Scope clicks to the question container by matching header text with regular expressions:
  ```python
  async def answer_scoped_yes_no(page, question_regex: str, answer_yes: bool) -> bool:
      rx = re.compile(question_regex, re.I)
      containers = page.locator('.ashby-application-form-field, fieldset, div[class*="FormField"]')
      count = await containers.count()
      target_text = "Yes" if answer_yes else "No"
      for i in range(count):
          container = containers.nth(i)
          text = await container.inner_text()
          if rx.search(text):
              btn = container.locator(f'button.ashby-application-form-input-yesno-option:has-text("{target_text}")').first
              if await btn.is_visible():
                  await btn.click()
                  return True
      return False
  ```

---

### B. Greenhouse Modern / Remix (`job-boards.greenhouse.io`)

Modern Greenhouse job boards run on Remix and use `react-select` comboboxes, invisible reCAPTCHA Enterprise, and dynamic field injections.

#### 1. React-Select Single & Multi-Select Comboboxes
Inputs like `#country`, `#candidate-location`, and custom survey questions are NOT native `<select>` tags.
* **Fix (Single)**:
  ```python
  async def fill_react_select(page, container_sel, search_text, match_text=None):
      loc = page.locator(container_sel).first
      await loc.click()
      await asyncio.sleep(0.3)
      await loc.locator('input').type(search_text, delay=30)
      await asyncio.sleep(0.6)
      opt = page.locator(f'div[class*="-option"]:has-text("{match_text or search_text}")').first
      if await opt.count() > 0:
          await opt.click()
      else:
          await page.keyboard.press("Enter")
  ```
* **Fix (Multi-Select)**: Check for existing `.select__multi-value__label` tags before typing to prevent duplicate values.

#### 2. EEO Demographic Survey Handling
Forms frequently mandate EEO self-identification (Gender, Race, Veteran, Disability).
* **Standard**: Justin's profile mandates choosing "Decline to self-identify" / "Prefer not to answer" for all sensitive attributes.
* **Fix**: Heuristically scan for fields containing `gender`, `race|ethnic`, `veteran`, or `disabilit` and select the corresponding decline option from either native `<select>` or `react-select`.

#### 3. Dynamic Cover Letter Requirement
Some postings require a Cover Letter (`Cover Letter *`). If so, click `button:has-text("Enter manually")` to expose `#cover_letter_text` rather than failing file upload:
```python
manual_btn = target_page.locator('button:has-text("Enter manually")').first
if await manual_btn.count() > 0 and await manual_btn.is_visible():
    await manual_btn.click()
    await asyncio.sleep(0.4)
    await target_page.fill('#cover_letter_text', cover_letter_body)
```

#### 4. Invisible reCAPTCHA Enterprise
Greenhouse uses invisible reCAPTCHA Enterprise (`size="invisible"`). It triggers automatically on submit. Do not attempt manual token injection unless the form explicitly errors with a challenge.

---

### C. BambooHR (`*.bamboohr.com/careers/*`)

#### 1. Microsoft Fabric UI Dropdowns
BambooHR dropdowns are wrapped in custom toggle buttons:
```python
await page.click('button[aria-label*="State"]')
await page.click('div[role="option"]:has-text("California")')
```

#### 2. Dual File Upload DOM Trap
BambooHR typically has Input 0 for Cover Letter (required) and Input 1 for Resume.
* **Trap**: Uploading to Input 0 removes that file input from the DOM, shifting Input 1.
* **Fix**: Always re-query `await page.query_selector_all('input[type=file]')` before uploading the second file.

#### 3. reCAPTCHA v2 Callback
Setting `textarea#g-recaptcha-response` is NOT enough for BambooHR. You must fire the internal client callback:
```python
await page.evaluate(f'''() => {{
    document.querySelector("textarea[id=\'g-recaptcha-response\']").value = "{token}";
    if (window.___grecaptcha_cfg && window.___grecaptcha_cfg.clients[0]) {{
        window.___grecaptcha_cfg.clients[0].S.S.callback("{token}");
    }}
}}''')
```

---

## 3. Candidate Profile Authority & Truth Boundaries

Before applying to ANY job, profile data MUST be loaded via `candidate_loader.py` adhering to `~/Projects/job-search/PROFILE_AUTHORITY.md`.

### Core Facts
* **Name**: Justin Ryan (legal surname: Gonek)
* **Email**: `justin@scoreapp.pro`
* **Phone**: `310.465.8228` (E.164: `+13104658228`)
* **Location**: Garden Grove, CA (Orange County) | postal: `""` (resolve privately per form if mandatory; never inject stale LA placeholders like `90012` or `92840`)
* **Work Authorization**: US Citizen | No sponsorship required now or in future
* **Availability**: Immediate to 2 weeks
* **LinkedIn**: `https://linkedin.com/in/justinrgonek`
* **GitHub**: `https://github.com/wowthisiseasytoremember-stack`
* **Portfolio**: `https://justinryan.work`

### Strict Invariants (DO NOT CROSS)
1. **Degree**: UMPI Bachelor's is "finalization pending". NEVER mark formally conferred. If binary Yes/No conferred degree is required, answer accurately or note Associate degree completed (History).
2. **Quarantined Credentials**: Never claim PMP, ITIL, CSP, or Google Data Analytics certificates.
3. **Cannabis Platform**: Do not claim Cannabis POS, seed-to-sale, METRC, or BioTrack system administration.
4. **Engineering Role**: Justin coordinates distributed technical operations and builds practical automation (Python, APIs, Linux, n8n, SQL). Never pretend to be the software engineer of record.
5. **Metrics**: Avenor is 180+ implementations across 35+ countries; T-Mobile is 100+ active B2B accounts. Never inflate or invent venture ARR/book values.

---

## 4. Execution & Verification Protocol

Every application execution must follow this 6-step checklist:

1. **Dead-Job Circuit Breaker**:
   - Check if page redirected or contains text like `"Job has expired"`, `"No longer accepting applications"`, or Greenhouse `?error=true`. Abort early if closed.
2. **Pre-Submit Validation**:
   - Verify every required field (`[required]`, `[aria-required="true"]`) is non-empty.
   - Capture `/tmp/<company>_pre_submit.png`.
3. **Submit Action**:
   - Click submit button: `button[type="submit"]` or `button:has-text("Submit application")`.
4. **Post-Submit Confirmation**:
   - Poll for up to 25s for confirmation indicators:
     - URL contains `/confirmation` or `thank-you`
     - Page content contains `"Thank you for applying"`, `"application has been received"`, or `"submitted successfully"`.
   - Capture full-page confirmation screenshot: `/tmp/<company>_submitted_success.png`.
5. **Evidence Archival**:
   - Copy screenshot to `tracking/evidence/<company>-submitted-<YYYYMMDD>.png`.
6. **Durable Logging**:
   - Append submission record to `tracking/TRACKER.csv`:
     ```csv
     <YYYY-MM-DD HH:MM:SS>,<Company>,<Role>,<Salary>,<Driver>,<URL>,APPLIED,,,<Notes & Confirmation Text>; screenshot: tracking/evidence/<screenshot>.png
     ```
   - Update `leads/leads.db` if matching record exists:
     ```sql
     UPDATE leads SET stage = 'applied', submit_count = 1, last_submit_at = datetime('now') WHERE id = <lead_id>;
     ```
