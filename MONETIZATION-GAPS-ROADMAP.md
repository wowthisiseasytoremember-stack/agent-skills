# MONETIZATION GAPS — 5-Session Roadmap (v3)

**Created:** 2026-08-19 10:58 UTC
**Updated:** 2026-08-19 11:55 UTC (v3 — Track A only for Session 1; Track B deferred)
**Source sessions:** `~/Sessions/20260819_105825_*`, `~/Sessions/20260819_113500_*`, `~/Sessions/20260819_114500_*`
**Origin:** Synthesis of THREE resource dumps + 9-initiative portfolio review + portfolio corrections
**Status:** proposed (Session 1 redesigned)
**Owner:** Justin + agents

---

## Critical correction (v3)

**Luna is real.** Justin IS Luna (real 19-year-old femboy). AI is a TOOL for face obscuration / style transfer on his existing photos, not the persona itself.

This splits Session 1 into two tracks with completely different tech, compliance, and unit economics:

| | Track A (PRIMARY) | Track B (EXPERIMENTAL, deferred to Tier 2) |
|---|---|---|
| **Subject** | Justin/Luna (real) | AI-generated personas (no relation to Justin) |
| **AI role** | Privacy / style tool | Persona creation engine |
| **Identity** | PRESERVED (with selective obscuration) | CREATED from scratch |
| **Compliance** | 2257 CFR Part 75, KYC, identity verification | AI-persona disclosure, age verification per UK Online Safety Act / EU AI Act / US state laws |
| **Persona IP** | Justin owns Luna outright | Justin owns LoRA + LLM config + voice clone |
| **Unit economics** | ARPU $20-100/mo, whale rate HIGHER, PPV conversion HIGHER, lower scale ceiling | ARPU $5-30/mo, whale rate LOWER, infinite scale ceiling |
| **Production model** | Time-bounded (one of you) | Automated (24/7 DM, image gen) |

**Session 1 = Track A only.** Track B is now a Tier 2 spike after Track A is stable.

---

## Audit summary (cumulative across all 3 dumps)

Three resource dumps received, audited against 9-initiative portfolio:

**Dump 1** (2026-08-19 10:58): 6 monetization primitives — LLM/SaaS/API, mobile/desktop, affiliate/content, web/SEO/ads, adult/video, community. ~60% dropped as no-fit.

**Dump 2** (2026-08-19 11:35): AI companion architecture, OF/Fanvue agency tooling, Gumroad/Payhip, "Build the Revenue Router" advice. Cherry-picked pricing ladder, pSEO, event schema, compliance. Discarded "Build the Router."

**Dump 3 / search** (2026-08-19 11:45): AI companion market data — CompanionRank April 2026 statistics ($2-4B market, 30-50% YoY growth, 20-30M MAU on Character.AI, 70%+ male, 60-70% aged 18-34, 17% freemium-to-premium top, 60-75% paid revenue via mobile IAP, ElevenLabs Voice Library at $22/mo Creator plan, multi-platform distribution across 5-8 platforms, LoyalFans blocks AI in 2026).

### Discarded permanently (cumulative)

- Build the custom Revenue Router (off-shelf composition wins: Dub.co + Plausible + Airtable + Stripe)
- SaaS/API metering (no SaaS in portfolio)
- Newsletter monetization (no newsletter in 9 initiatives)
- X/Twitter Creator Revenue Sharing (unreliable for adult)
- Survivorship-biased revenue anecdotes
- "Day 1-7" tactical plans (covered by Session 1-5 Week 1-4)
- AI companion apps targeting companion users (Character.AI etc. data is useful for fork pattern, but Justin's Luna is real)
- Telegram/Discord community monetization (no Discord yet)

---

## The 5-session sequence (v3)

Sessions run in order: **1 → 2 → 3 → 4 → 5**. Each is self-contained. Resume from any via `.handoff/LATEST.md` in the active project.

---

### Session 1 — Luna (real) + AI face obscuration + Fanvue automation + real-person compliance (FIRST)

**Goal:** Ship a working AI face-obscuration pipeline for Luna's photo content, codify real-person compliance, automate Fanvue DM/PPV/retention with Supercreator assist-mode, and expand to multi-platform distribution. Live revenue impact.

**Why first:** Luna is the live revenue stream. ARPU upside from real-person benchmarks ($20-100/mo, vs current $24.99 sub cap). AI obscuration unblocks identity-safe content production at scale. Real-person compliance is non-negotiable from day 1.

**Why this had to be split from Track B:** Track A and Track B use completely different tool chains, different compliance frameworks, and different unit economics. Building them together would conflate privacy-preservation with identity-creation.

#### 1A. AI face obscuration pipeline (the new core)

**Tool chain:**
- Base model: SDXL or Flux (Flux is newer + better quality; SDXL has more community LoRAs — recommend Flux unless specific LoRA needed)
- IP-Adapter for face reference (preserves identity when desired; tunable strength for "look like me" vs "obscured but recognizably me")
- ControlNet OpenPose for pose consistency
- Per-mode LoRA training pipeline (~$2/model, 10-20 reference images each)
- Output QC: identity-leak detection, artifact check, consistency check
- Storage: versioned outputs (original + per-mode variants, audit trail)

**Modes (4 starting set):**
- Artistic painterly (oil-painting style, identity-preserved)
- Trippy psychedelic (high-distortion, surreal aesthetic)
- Obscure silhouette (full identity protection, body visible)
- Cinematic grade (film-look, identity preserved, color-graded)

**Workflow:** ComfyUI (recommended for visual control) or custom CLI for batch processing. Web UI only if Justin wants non-technical use.

**Deliverable:** `undercontent/docs/LUNA-FACE-OBSCURATION-PIPELINE.md` — full spec + setup recipes + per-mode LoRA training data structure

#### 1B. Real-person compliance doctrine

- **2257 record-keeping (CFR Part 75):** all depictions of real Luna must have age-verification records maintained. Storage location, retention period, access controls.
- **KYC / age verification:** Luna is real, 19, ID on file. Where stored, who accesses, retention.
- **Platform ToS variability on stylization:** some platforms treat heavily-stylized faces as still-identifying (affects discoverability, DMCA, impersonation claims). Per-platform checklist.
- **Fan-trust disclosure:** how to handle "is this AI?" questions without losing parasocial premium. Honest framing (artistic stylization) vs misleading framing (raw photos).
- **Persona rights:** Luna = Justin. No platform can revoke "their" character because Luna IS you. Document ownership.
- **Multi-platform payment processor risk:** each platform = different processor. Adult payment processor tightening is real (Stripe/PayPal explicit bans on much of vertical). Crypto payment rails as contingency (already discussed in earlier version).

**Deliverable:** `agent-skills/REAL-PERSON-COMPLIANCE-DOCTRINE.md` — adult + identity-protection + payment processor risk doctrine + checklist

#### 1C. Fanvue automation + multi-platform expansion

**For Luna (real):**
- **4-tier pricing review** against real-person ARPU benchmarks ($20-100/mo typical; current $24.99 cap is entry-tier; consider whale tier at $49.99)
- **PPV ladder** per existing undercontent/TODO
- **Custom content 5-10x subscription rule** (existing)
- **Welcome message templates** (3+ variants, segmented by source: from-erotica-story / from-IG / from-Reddit)
- **DM automation via Supercreator Izzy** in **assist mode** (helps craft replies, NOT autopilot — autopilot wrong for real Luna because it implies non-human on other end, erodes parasocial premium)
- **Fanvue Creator Referral Program activation**

**Multi-platform distribution (real-person):**
- Fanvue primary
- **Fansly, ManyVids, JustForFans, MYM** as overflow (NOT LoyalFans — they block AI but Justin should diversify regardless)
- Cross-platform identity persistence — Luna same on every platform, persona bible consistency
- Cross-posting automation

**Deliverable:** `undercontent/docs/FANVUE-AUTOMATION-PLAYBOOK.md` — full playbook for Luna real-person

#### 1D. Whale detection + ARPU/retention tracking

**Whale signals (from CompanionRank data):**
- Session frequency 5+/day (5-15% of users are heavy users = whale tier)
- PPV buy rate (high-converting whales buy 80%+ of PPVs offered)
- DM engagement depth (length, frequency, personal-share rate)
- Custom content request rate

**Real-person benchmarks (from CompanionRank April 2026):**
- Free-to-paid conversion: 3-8% median, 10-15% stretch
- Day-1 retention: 40-60%
- Day-7 retention: 15-30%
- Day-30 retention: 8-18%
- ARPU target: $30+ on heavy users by Q1 2027 (currently unknown)
- 60-75% of paid revenue via mobile IAP — verify Luna's split

**Deliverable:** `agent-skills/WHALE-DETECTION-DOCTRINE.md` — whale signal definitions + tracking schema

#### 1E. Multi-platform doctrine (real-person)

- Platform comparison matrix (Fanvue/Fansly/ManyVids/JustForFans/MYM)
- Per-platform compliance differences (each has different ToS on adult + AI-stylization)
- Cross-posting automation
- Cross-platform identity persistence
- Per-platform analytics aggregation

**Deliverable:** `agent-skills/REAL-PERSON-MULTIPLATFORM-DOCTRINE.md`

**Pre-reqs for Session 1:**
- [ ] Confirm River is real or AI-generated fork (affects session scope)
- [ ] Reference dataset of Luna photos for LoRA training (10-20 per mode)
- [ ] Decide: ComfyUI vs custom CLI vs web UI for pipeline
- [ ] Budget approval: ElevenLabs Creator plan ($22/mo, ONLY if voice needed for real Luna — likely NOT needed for Track A; deferred to Track B)
- [ ] Budget approval: base model compute ($0 if local SDXL/Flux, ~$20-50/mo if hosted)
- [ ] Multi-platform accounts: at least Fansly + ManyVids (Fanvue already live)

**Success criteria:**
- 3+ obscuration modes trained with consistent style
- Output QC pipeline catches identity leaks
- 4-tier pricing reviewed against ARPU benchmarks
- Welcome message templates deployed (3+ variants per source segment)
- Fanvue Creator Referral Program links live
- Compliance docs reviewed and adopted
- Multi-platform: Fanvue + 1 other platform active (Fansly or ManyVids)
- Whale detection tracking deployed

**Effort:** 4-5 hours

---

### Session 2 — Mobile/desktop monetization audit

**Goal:** Identify which of the 15+ existing apps are ready for paid tiers and which should be killed/merged. Codify doctrine so future apps ship with monetization from day one.

**Scope:** Audit each app for current state, store presence, existing monetization, user base, retention signals, monetization potential.

**Apps in scope:**
- Feline-Calorie-Planner, AquaTrack / FloraTrack / BioTrackCore, KJV devotional (DailyDevotionKJVForWomen), organism-atlas, biodiorama, abigail-app, auto-subs, email-triage, dental-claims-automation, homeschool-compass, purrfect-pair-tasks, paper-inventory, soul-conservatory, the-conservatory, Score, Anno + reference cluster (FlipScale, RORK-iFlip)

**Payment stack decision tree + pricing ladder:**
- Outcome-value pricing: 1-10% of outcome value (NEVER build-time)
- 3-tier template: Basic/Pro/Premium, middle = "most popular" (70% of buyers choose middle)
- Conversion targets: 2-5% visitor→buyer, 3-5% buyer→review
- Stacks: RevenueCat (cross-platform mobile + paywall UI), StoreKit 2 (iOS-only total control), Google Play Billing (Android-only), Lemon Squeezy (web/desktop digital), Paddle (web subscription + international tax/MoR), Stripe Billing + OpenMeter/Lago (high-volume API/credit metering)

**Deliverables:**
- `agent-skills/MOBILE-APP-MONETIZATION-AUDIT.md` — per-app table with state, recommended stack, priority
- `agent-skills/PAYMENT-STACK-DOCTRINE.md` — decision tree + setup recipes + pricing ladder template

**Success criteria:**
- Every app has a row with state + recommended stack
- 3-5 apps marked "monetize within 30 days"
- 2-3 apps marked "kill or merge" with reasoning
- Pricing ladder template ready to apply to any new app

**Effort:** 3-4 hours

---

### Session 3 — Video commerce + programmatic SEO (pSEO)

**Goal:** Build the missing link between Shorts pipeline and POD/digital products. Short → product → commission flywheel + database-driven SEO pages.

**Scope:**
- YouTube Shopping setup (Shopify channel integration or Merchant Center direct)
- TikTok Shop Affiliate Open Collaboration setup
- Commerce-flywheel doctrine in content-factory
- pSEO architecture pattern (database-driven pages: city × service × attribute matrices)
- WP Content Autopilot evaluation (build vs install)
- Apply both to meme-merch + shame-seo

**Deliverables:**
- `content-factory/docs/CONTENT-TO-COMMERCE-FLYWHEEL.md` — Short → product doctrine
- `agent-skills/PSEO-ARCHITECTURE-DOCTRINE.md` — database-driven SEO pages pattern + WP Content Autopilot install/build decision
- TikTok Shop Seller Center setup checklist
- YouTube Shopping eligibility + setup checklist
- 1 sample pSEO matrix implemented for shame-seo

**Success criteria:**
- content-factory routes any Short to a product link
- meme-merch has at least one product live in TikTok Shop Open Collaboration
- pSEO matrix generates ≥50 indexable URLs from a 5×3×2×3 attribute spread

**Effort:** 3-4 hours

---

### Session 4 — Affiliate program doctrine + event schema

**Goal:** Codify when to RECRUIT affiliates TO your brand. Unified event taxonomy for cross-pod attribution.

**Scope:**
- Refferq setup vs. Impact/CJ/Awin decision
- FTC-compliant disclosure automation
- Event schema doctrine (page_view, cta_click, link_click, email_submit, checkout_started, etc. + minimum fields + SQL schemas)
- Apply to: shame-seo, meme-merch, erotica-site, service-businesses

**Deliverables:**
- `agent-skills/AFFILIATE-PROGRAM-DOCTRINE.md`
- `agent-skills/EVENT-SCHEMA-DOCTRINE.md`
- `agent-skills/refferq/` (docker-compose + env template + admin SQL)
- FTC disclosure snippet library

**Success criteria:**
- Decision tree answers "self-host Refferq or use Impact/CJ?" for any new project
- Refferq ready-to-deploy artifact
- Event schema adopted by at least 3 pods (undercontent, erotica-site, shame-seo)
- Cross-pod attribution dashboard working

**Effort:** 3-4 hours

---

### Session 5 — Ad network progression doctrine

**Goal:** Lock the Display Ads revenue lever across content sites to a concrete progression.

**Scope:**
- AdSense Auto Ads (start here, 10 min/any site)
- Ezoic migration criteria (10K+ daily visits; +20-50% RPM uplift)
- Prebid.js + Google Ad Manager (100K+/day)
- Apply to: erotica-site, shame-seo, meme-merch landing pages, future content sites

**Deliverables:**
- `agent-skills/AD-NETWORK-PROGRESSION.md` — decision tree + setup recipes + migration triggers

**Success criteria:**
- Any new content site knows which ad tier to start at based on traffic
- Migration triggers documented

**Effort:** 1 hour

---

## Tier 2 — later, not urgent (Track B + others)

- **B.** AI fork A/B testing (Track B) — LoRA training per fork, multi-persona LLM router, ElevenLabs Voice Library integration, token unlocks, full automation. ONLY after Track A is stable. A/B test signal: ARPU per persona vs Luna. If AI forks convert >50% of Luna ARPU, scale; if <25%, kill.
- **F.** Service-business Stripe Billing setup — laconic, local-growth-labs, ai-slop-refactor-agency, keystone-ops
- **G.** Gumroad / Payhip product positioning doctrine — applies when Anno, KJV devotional, or any digital download ships a paid tier
- **H.** Affitor skills install — affiliate content ops automation for shame-seo + meme-merch
- **I.** Stripe usage-billing spike — only if estate-scout / railroad-valuator / local-revenue-engine become credit-metered
- **J.** Newsletter monetization (Beehiiv) — spike if aether-bloom / bookmarks evolves into newsletter
- **K.** Reddit Ads as paid acquisition — spike after Session 4 lands
- **L.** Discord Server Subscriptions — only if Discord community materializes
- **M.** Multi-language personas (Spanish Luna for LatAm, Japanese Luna for anime segment) — post-Track A
- **N.** Persona marketplace / licensing (sell Luna/River as kits to other Fanvue creators) — post-Track B if forks proven

---

## Tracking

- **Session log:** each session writes to its own `~/Sessions/<timestamp>_*/summary.md`
- **Evidence:** add count + brief to `~/Projects/ecosystem-command-center/initiative-evidence.json` after each session
- **CHANGELOG:** append entry at top of the touched project's CHANGELOG
- **Resume:** if a session is interrupted, write `.handoff/LATEST.md` in the active project
- **MASTER.md:** update per-project state when completed

## Resume protocol

After Session 1 lands, its deliverable becomes the input for Session 2. If you stop mid-session, write `.handoff/LATEST.md` to the touched project with: Work In Progress / Open Questions / Files Touched / Next.

---

## Next session: **1 (Luna real + AI obscuration + Fanvue automation + real-person compliance)**

**Why first:** Live revenue impact (Luna is live, ARPU upside from real-person benchmarks). AI obscuration unblocks identity-safe content at scale. Real-person compliance is non-negotiable from day 1.

**Start trigger:** Justin confirms River status + approves pre-reqs (LoRA reference dataset, pipeline tooling choice, multi-platform accounts).

---

## Version history

- **v1** (2026-08-19 10:58 UTC) — 5-session sequence A→E (mobile audit, video commerce, affiliate doctrine, Fanvue playbook, ad network)
- **v2** (2026-08-19 11:35 UTC) — Reordered: Session 1 = AI companion + agency + compliance. Sessions 2-5 absorb pricing ladder, pSEO, event schema. Discarded "Build the Revenue Router" advice.
- **v3** (2026-08-19 11:55 UTC) — **Critical correction: Luna is real, AI is tool not persona.** Session 1 split into Track A (PRIMARY: Luna real + AI obscuration) and Track B (TIER 2: AI fork A/B test). Session 1 now Track A only. Compliance renamed (REAL-PERSON-COMPLIANCE-DOCTRINE.md). New deliverables: LUNA-FACE-OBSCURATION-PIPELINE.md, REAL-PERSON-MULTIPLATFORM-DOCTRINE.md, WHALE-DETECTION-DOCTRINE.md. Pre-reqs added (River status, LoRA reference dataset, pipeline tooling choice, multi-platform accounts). Multi-platform matrix updated to Fansly/ManyVids/JustForFans/MYM (NOT LoyalFans). ARPU/retention benchmarks from CompanionRank April 2026 added.