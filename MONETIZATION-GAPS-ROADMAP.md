# MONETIZATION GAPS — 5-Session Roadmap

**Created:** 2026-08-19 10:58 UTC
**Source session:** `~/Sessions/20260819_105825_*`
**Origin:** Synthesis of resource dump + 9-initiative portfolio review
**Status:** proposed (not yet started)
**Owner:** Justin + agents

---

## Audit summary

Resource dump covered 6 monetization primitives:
1. LLM/SaaS/API (Stripe Billing, OpenMeter, Lago, LiteLLM, BricksLLM, Unkey, Moesif, Kong, AWS API Gateway, AI SaaS Starter Kit, LastSaaS, OpenStarterKit)
2. Mobile/desktop (RevenueCat, StoreKit, Play Billing, Lemon Squeezy, Polar, Paddle, Discord Premium)
3. Affiliate/content (Refferq, Amazon Associates, FTC, TikTok Shop, YouTube Shopping, Fanvue referral, Fanvue settings, Affitor)
4. Web/SEO/ads (AdSense Auto Ads, Prebid, Ezoic, Google Search Central, WP Content Autopilot, NotionNext, Payload, NextFaster)
5. Adult/video (Fanvue docs, Fanvue first-$10k, X adult, Reddit NSFW, YouTube monetization, TikTok Shop, Instagram monetization)
6. Community (Reddit Contributor, Rewardful case study, Telegram funnel, Discord Server Shop)

After auditing against the **9 active initiatives** (ebay-store, biotrack, content-factory, business-intel, career, agent-infra, server-infra, personal-data, monetization), I dropped ~60% as no-fit. Kept what maps to existing projects.

### Dropped permanently (Tier 3)

- All SaaS/API metering resources — no SaaS in portfolio
- Most SaaS starter kits — wrong shape
- Discord Premium Apps — no Discord community yet
- Polar / AWS API Gateway / BricksLLM / Kong / Unkey — no fit
- Most Hacker News threads — entertainment, not actionable
- All confidence-level annotations + rate-limit preamble
- Reddit revenue screenshots — unverified

---

## The 5-session sequence

Sessions run in order: **A → B → C → D → E**. Each is self-contained and produces its own deliverable. Resume from any session via `.handoff/LATEST.md` in the active project.

### Session A — Mobile/desktop monetization audit (FIRST)

**Goal:** Identify which of the 15+ existing apps are ready for paid tiers and which should be killed/merged. Codify doctrine so future apps ship with monetization from day one.

**Scope:** Audit each app for current state (scaffold / working / launched), store presence, existing monetization, user base, retention signals, monetization potential. Recommend payment stack per app.

**Apps in scope (from `monetization.apps` family):**
- Feline-Calorie-Planner (canonical cat app)
- AquaTrack / FloraTrack / BioTrackCore (the-conservatory is the user surface)
- KJV devotional (DailyDevotionKJVForWomen)
- organism-atlas, biodiorama, abigail-app, auto-subs, email-triage, dental-claims-automation, homeschool-compass, purrfect-pair-tasks, paper-inventory, soul-conservatory, the-conservatory, Score, Anno
- Reference cluster: FlipScale, RORK-iFlip (legacy, audit only)

**Payment stack decision tree:**
- Cross-platform mobile + need A/B testing + paywall UI → **RevenueCat**
- iOS-only + need total control → **StoreKit 2 direct**
- Android-only + need total control → **Google Play Billing direct**
- Web/desktop digital download → **Lemon Squeezy** (license keys, MoR-light)
- Web subscription + international tax/VAT headache → **Paddle** (MoR)
- High-volume API/credit metering → **Stripe Billing + OpenMeter / Lago**

**Deliverables:**
- `agent-skills/MOBILE-APP-MONETIZATION-AUDIT.md` — per-app table with state, recommended stack, priority
- `agent-skills/PAYMENT-STACK-DOCTRINE.md` — decision tree + setup recipes for RevenueCat / StoreKit / Play Billing / Lemon Squeezy / Paddle

**Success criteria:**
- Every app in `monetization.apps` family has a row with state + recommended stack
- 3-5 apps marked "monetize within 30 days" with concrete next action
- 2-3 apps marked "kill or merge" with reasoning
- Doctrine doc covers all 4-5 stacks with decision tree

**Effort:** 3-4 hours

---

### Session B — Video commerce doctrine (YouTube Shopping + TikTok Shop Affiliate)

**Goal:** Build the missing link between your Shorts pipeline and your POD/digital products. Short → product → commission flywheel.

**Scope:**
- YouTube Shopping setup (Shopify channel integration or Merchant Center direct)
- TikTok Shop Affiliate Open Collaboration setup
- Commerce-flywheel doctrine in content-factory: how a published Short becomes a Shop link becomes revenue
- Apply to meme-merch POD products

**Deliverables:**
- `content-factory/docs/CONTENT-TO-COMMERCE-FLYWHEEL.md` — doctrine + setup recipes
- TikTok Shop Seller Center setup checklist (steps + commission-rate guidance)
- YouTube Shopping eligibility + setup checklist

**Success criteria:**
- content-factory knows how to route any Short to a product link
- meme-merch has at least one product live in TikTok Shop Open Collaboration
- 1 sample Short → product page flow documented end-to-end

**Effort:** 3 hours

---

### Session C — Affiliate program doctrine (Refferq self-hosted vs. Impact/CJ/Awin)

**Goal:** Codify when to RECRUIT affiliates TO your brand (not just be one). Self-hosted open-source path vs. networks.

**Scope:**
- When does a project need its own affiliate program? (criteria: traffic, repeat purchase, brand pull, niche)
- Refferq setup (clone, install, env vars, Postgres URL, JWT secret, Resend, optional Stripe, Prisma generate/db push/seed, admin SQL)
- When Impact / CJ / Awin makes more sense than self-hosting
- FTC-compliant disclosure automation
- Apply doctrine to: shame-seo, meme-merch, erotica-site, service-businesses (laconic, local-growth-labs, ai-slop-refactor-agency, keystone-ops)

**Deliverables:**
- `agent-skills/AFFILIATE-PROGRAM-DOCTRINE.md` — decision tree + setup recipes
- `agent-skills/refferq/` — docker-compose + env template + admin SQL ready to clone
- FTC disclosure snippet library (HTML, Markdown, video description patterns)

**Success criteria:**
- Decision tree answers "self-host Refferq or use Impact/CJ?" for any new project
- Refferq ready-to-deploy artifact (compose + env + admin onboarding)
- FTC compliance library covers web, video, social posts

**Effort:** 3 hours

---

### Session D — Fanvue automation + referral playbook

**Goal:** Codify the conversion loop for Luna/River and future personas. Pricing tiers mean nothing if welcome → PPV → retention isn't scripted.

**Scope:**
- Intro video doctrine (per persona, AI-generated or filmed)
- Automated welcome message templates (segment by source: from-erotica-story / from-IG-TikTok / from-Reddit)
- PPV ladder (price/content matrix per persona; tied to existing 4-tier pricing)
- DM funnel (welcome → preference segmentation → paid unlock offer → retention cadence)
- Fanvue Creator Referral Program activation for Luna + River
- Cross-pod routing (erotica-site story → Fanvue DM via tracked link)

**Deliverables:**
- `undercontent/docs/FANVUE-AUTOMATION-PLAYBOOK.md` — full playbook
- Welcome message template library (3+ variants per persona)
- PPV price/content ladder per persona
- Fanvue referral activation checklist (one page per creator)
- Cross-pod UTM convention for erotica-site → Fanvue routing

**Success criteria:**
- Any new persona can be launched in <24 hours using the playbook
- Fanvue referral links live for Luna + River, commission attribution working
- Cross-pod funnel tied to DM automation (one tracked link per story → DM sequence)

**Effort:** 3 hours

---

### Session E — Ad network progression doctrine (quick win)

**Goal:** Lock the Display Ads revenue lever across content sites to a concrete progression. erotica-site already has "Display Ads 50-70%" with no stack.

**Scope:**
- AdSense Auto Ads setup (10 min/any site — start here)
- Ezoic migration criteria (when 10K+ daily visits; +20-50% RPM uplift expected; ads.txt manager; cloud integration)
- Prebid.js + Google Ad Manager setup (when 100K+/day; price granularity; bidder adapters; analytics adapters)
- Apply to: erotica-site, shame-seo, meme-merch landing pages, future content sites

**Deliverables:**
- `agent-skills/AD-NETWORK-PROGRESSION.md` — decision tree + setup recipes per tier + migration triggers (visit thresholds, RPM ceilings)

**Success criteria:**
- Any new content site knows which ad tier to start at based on traffic level
- Migration triggers documented (e.g., "switch from AdSense to Ezoic when daily visits > 10K AND RPM < $2")
- Setup snippets ready to copy per tier

**Effort:** 1 hour

---

## Tier 2 — later, not urgent (Session F-I)

- **F.** Service-business Stripe Billing setup — laconic, local-growth-labs, ai-slop-refactor-agency, keystone-ops (charge recurring for any retainer clients)
- **G.** MoR digital product monetization (Paddle / Lemon Squeezy) — applies if Anno, KJV devotional, or any digital download ships a paid tier
- **H.** Affitor skills install — affiliate content ops automation for shame-seo + meme-merch
- **I.** Stripe usage-billing spike — only if estate-scout / railroad-valuator / local-revenue-engine become credit-metered

---

## Tracking

- **Session log:** each session writes to its own `~/Sessions/<timestamp>_*/summary.md`
- **Evidence:** add count + brief to `~/Projects/ecosystem-command-center/initiative-evidence.json` after each session
- **CHANGELOG:** append entry at top of the touched project's CHANGELOG
- **Resume:** if a session is interrupted, write `.handoff/LATEST.md` in the active project
- **MASTER.md:** update per-project state when completed
- **Skill loader:** newly created skills aren't visible mid-session — use absolute paths; next session sees them

## Resume protocol

After Session A lands, its deliverable becomes the input for Session B. If you stop mid-session, write `.handoff/LATEST.md` to the touched project with:
- Work In Progress (what's done, what's not)
- Open Questions (anything blocked on Justin)
- Files Touched (so you can `git diff` on resume)
- Next (first action when you return)

---

## Next session: **A (mobile app monetization audit)**

**Why first:** highest ROI per hour, biggest blast radius across the 15+ apps in `monetization.apps`. Foundational — every future app monetization decision uses the doctrine doc.

**Start trigger:** Justin says "go" on Session A, or the next /handoff after the SKILLS-AUDIT close-out.