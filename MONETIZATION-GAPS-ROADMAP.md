# MONETIZATION GAPS ??? 5-Session Roadmap (v4)

**Created:** 2026-08-19 10:58 UTC
**Updated:** 2026-08-19 12:25 UTC (v4 ??? kit adoption integrated; Session 1 narrowed)
**Source sessions:** `~/Sessions/20260819_105825_*`, `~/Sessions/20260819_113500_*`, `~/Sessions/20260819_114500_*`, `~/Sessions/20260819_121000_*`
**Origin:** Synthesis of THREE resource dumps + 9-initiative portfolio review + critical corrections + `monetization-kit/` adoption
**Status:** proposed (Session 1 redesigned with kit integration)
**Owner:** Justin + agents

---

## Critical corrections (cumulative)

**v3 correction:** Luna is real. AI is a tool, not the persona. Session 1 split into Track A (real Luna + AI obscuration) and Track B (AI fork A/B test, deferred).

**v4 correction:** A pre-built `monetization-kit/` was dropped via taildrop containing production-grade TypeScript code (ledger, webhooks, /go/ router, FTC disclosure, LiteLLM sync, 5 runbooks, 22 tests). This IS the "Revenue Router v1" I told Justin to discard as a from-scratch build. But adopting it = "use existing tool," which aligns with shipping-beats-starting. Roadmap rewritten to integrate kit adoption per session.

---

## Audit summary (v4 ??? 4 dumps + 1 kit)

| Source | Date | What | Verdict |
|---|---|---|---|
| Dump 1 | 2026-08-19 10:58 | 6 monetization primitives | ~60% dropped |
| Dump 2 | 2026-08-19 11:35 | AI companion, agency tools, Gumroad, "Build the Router" | "Build the Router" advice redirected to kit adoption |
| CompanionRank search | 2026-08-19 11:45 | AI companion market stats | Benchmarks integrated (ARPU, retention, conversion, geo) |
| Dump 3 (re-paste) + zip file | 2026-08-19 12:00 | Same as Dump 2 + `monetization-kit/` code drop | Kit adopted; re-paste redundant (already audited) |
| `monetization-kit/` | 2026-08-19 12:10 | 28 items, production-grade TS code + 5 runbooks + LiteLLM config | **Adopt per cherry-pick map below** |

### Discarded permanently (v4)

- Build the custom Revenue Router (kit provides this ??? adopt instead)
- SaaS/API metering (no SaaS in portfolio)
- Newsletter monetization (no newsletter in 9 initiatives)
- X/Twitter Creator Revenue Sharing (unreliable for adult)
- Survivorship-biased revenue anecdotes
- "Day 1-7" tactical plans (covered by kit runbooks + Session 1-5)
- AI companion apps targeting companion users (Character.AI etc. data useful for fork pattern only; Luna is real)
- Telegram/Discord community monetization (no Discord yet)
- Kit explicitly does NOT cover: Prebid/GAM (no traffic), Kill Bill (Lago covers), Discord Server Shop, WP Content Autopilot, NotionNext ??? agreed, no action

---

## Kit cherry-pick map

Adoption per roadmap session. **Don't write custom code for anything the kit covers.**

| Kit component | Maps to session | Action |
|---|---|---|
| `runbook/C-fanvue-operator.md` | **Session 1** Track A | ADOPT wholesale (PPV-in-welcome ~25% unlock, geo-block, automated messages, OAuth+PKCE, webhook sig verification) |
| `affiliate-layer/` (Disclosure, go-redirect, offers, ftc-copy) | **Session 1** cross-pod funnel + **Session 4** affiliate doctrine | ADOPT ??? wire `/go/luna-fanvue` from erotica-site immediately |
| `runbook/B-seo-affiliate-stack.md` | **Session 3** + **Session 4** | ADOPT ??? pairs with WP Content Autopilot decision |
| `runbook/D-video-commerce.md` | **Session 3** | ADOPT ??? YT eligibility + TikTok Shop pilot + own-store hedge |
| `runbook/E-mobile-iap.md` | **Session 2** | ADOPT ??? RevenueCat default; CANCELLATION???EXPIRATION warning baked in |
| `revenuecat-webhooks.ts` + `lemonsqueezy-webhooks.ts` | **Session 2** + Tier 2 digital goods | ADOPT ??? production-tested |
| `litellm/config.yaml` + `litellm-sync.ts` | **Tier 2 Track B** | ADOPT when Track B launches |
| `money-path/ledger.ts` + `schema.sql` | **Tier 2 Track B** + any future SaaS | ADOPT ??? append-only, idempotency, reserve???settle all done |
| `runbook/A-llm-api-stack.md` | **Tier 2 Track B** | ADOPT |
| `entitlements.ts` (PLANS, price???plan map) | Tier 2 + future SaaS | ADOPT ??? reusable plan tier shape |

**What the kit does NOT cover (Session 1 gaps to build):**
1. Real-person compliance for Luna (2257, KYC, identity protection) ??? kit's runbook/C covers platform ToS only
2. AI face-obscuration pipeline (Session 1A) ??? kit has no image-gen code
3. Multi-platform identity persistence for Luna (real-person, not SaaS) ??? kit's affiliate layer is content???affiliate, not persona???multi-platform
4. Whale detection (Session 1D) ??? kit doesn't have creator-economy metrics

---

## The 5-session sequence (v4)

### Session 1 ??? Luna (real) + AI face obscuration + Fanvue operator + real-person compliance (FIRST)

**Goal:** Ship AI face-obscuration pipeline for Luna, codify real-person compliance, adopt Fanvue operator runbook from kit, wire cross-pod /go/ router for Luna funnel, expand to multi-platform distribution.

**Why first:** Luna is the live revenue stream. Kit adoption cuts Session 1 effort by ~40% (runbook C + affiliate layer = no custom code). Only 4 gaps remain for Session 1 to build custom: face obscuration, compliance, multi-platform identity, whale detection.

#### 1A. AI face obscuration pipeline (custom build)

**What kit doesn't cover.** Justin is real, AI is tool. Same character DNA ??? 4 obscuration modes for content production at scale.

**Tool chain:**
- Base model: SDXL or Flux (recommend Flux unless specific LoRA needed)
- IP-Adapter for face reference (preserves identity when desired)
- ControlNet OpenPose for pose consistency
- Per-mode LoRA training pipeline (~$2/model, 10-20 reference images each)
- Output QC: identity-leak detection, artifact check, consistency check
- Storage: versioned outputs (original + per-mode variants, audit trail)

**Modes (4 starting set):**
- Artistic painterly (oil-painting style, identity-preserved)
- Trippy psychedelic (high-distortion, surreal aesthetic)
- Obscure silhouette (full identity protection, body visible)
- Cinematic grade (film-look, identity preserved, color-graded)

**Workflow:** ComfyUI (recommended for visual control) or custom CLI for batch processing.

**Deliverable:** `undercontent/docs/LUNA-FACE-OBSCURATION-PIPELINE.md` ??? full spec + setup recipes + per-mode LoRA training data structure

#### 1B. Real-person compliance doctrine (custom build)

**What kit doesn't cover.** Kit's runbook/C covers platform ToS only.

- 2257 record-keeping (CFR Part 75) ??? all depictions of real Luna must have age-verification records
- KYC / age verification ??? Luna = real, 19, ID on file. Where stored, who accesses, retention
- Platform ToS variability on stylization ??? some platforms treat heavily-stylized faces as still-identifying (DMCA, impersonation claims)
- Fan-trust disclosure ??? how to handle "is this AI?" questions without losing parasocial premium
- Persona rights ??? Luna = Justin. No platform can revoke "their" character
- Multi-platform payment processor risk ??? Stripe/PayPal explicit bans on much of vertical; crypto payment rails as contingency

**Deliverable:** `agent-skills/REAL-PERSON-COMPLIANCE-DOCTRINE.md` ??? adult + identity-protection + payment processor risk doctrine + checklist

#### 1C. Fanvue automation ??? ADOPT kit runbook/C

**What kit covers.** Adopt wholesale; no custom code needed beyond integration.

- Fanvue operator runbook C: PPV-in-welcome ~25% unlock average, geo-block setup, automated messages config
- OAuth + PKCE via official Next.js starter (pin `X-Fanvue-API-Version: 2025-06-26`)
- Webhook `creator.message.received` ??? draft reply ??? `POST /chats/:userUuid/message`
- n8n `@fanvue/n8n-nodes-fanvue` if no custom server wanted
- 4-tier pricing review (existing Free/$9.99/$14.99/$24.99) against real-person ARPU benchmarks ($20-100/mo typical; current cap is low; consider $49.99 whale tier)
- Fanvue Creator Referral Program activation
- Supercreator Izzy in **assist mode** only (autopilot erodes parasocial premium for real Luna)

**Deliverable:** `undercontent/docs/FANVUE-AUTOMATION-PLAYBOOK.md` ??? fanvue-operator runbook + Luna-specific config

#### 1D. Whale detection + ARPU/retention tracking (custom build)

**What kit doesn't cover.** Kit handles SaaS money-path, not creator-economy metrics.

**Whale signals (from CompanionRank April 2026):**
- Session frequency 5+/day (5-15% of users are heavy users = whale tier)
- PPV buy rate (high-converting whales buy 80%+ of PPVs offered)
- DM engagement depth (length, frequency, personal-share rate)
- Custom content request rate

**Real-person benchmarks:**
- Free-to-paid: 3-8% median, 10-15% stretch
- Day-1 retention: 40-60%, Day-7: 15-30%, Day-30: 8-18%
- ARPU target: $30+ on heavy users by Q1 2027
- 60-75% of paid revenue via mobile IAP ??? verify Luna's split

**Deliverable:** `agent-skills/WHALE-DETECTION-DOCTRINE.md` ??? whale signal definitions + tracking schema

#### 1E. Multi-platform doctrine (custom build)

**What kit doesn't cover.** Kit's affiliate-layer is content???affiliate, not persona???multi-platform identity persistence.

- Platform comparison matrix (Fanvue/Fansly/ManyVids/JustForFans/MYM)
- Per-platform compliance differences (each has different ToS on adult + AI-stylization)
- Cross-posting automation
- Cross-platform identity persistence ??? Luna same on every platform, persona bible consistency
- Per-platform analytics aggregation

**Deliverable:** `agent-skills/REAL-PERSON-MULTIPLATFORM-DOCTRINE.md`

#### 1F. Cross-pod /go/ router ??? ADOPT kit affiliate-layer

**What kit covers.** Wire immediately.

- Mount `createGoHandler` at `/go/:slug`
- Add `offers.json` with Luna entry: `{"luna-fanvue": {"slug": "luna-fanvue", "network": "fanvue", "destination": "https://fanvue.com/luna", ...}}`
- Add `<Disclosure />` to erotica-site pages with affiliate links (Luna is the destination, not Amazon ??? but pattern is identical)
- erotica-site story ??? `/go/luna-fanvue?src=story&pos=bio` ??? 302 to Fanvue profile with click log

**Deliverable:** erotica-site implementation: `/go/[slug]/route.ts` + Disclosure component on author pages

**Pre-reqs for Session 1:**
- [ ] Confirm River is real or AI fork
- [ ] Reference dataset: 10-20 Luna photos per style mode
- [ ] Decide: ComfyUI vs custom CLI vs web UI
- [ ] Budget approval: base model compute ($0 local, ~$20-50/mo hosted)
- [ ] Multi-platform accounts: Fansly + ManyVids (Fanvue already live)
- [ ] Kit installed in working repo: `cp -r monetization-kit ~/Projects/undercontent/vendor/monetization-kit`

**Success criteria:**
- 3+ obscuration modes trained with consistent style
- Output QC pipeline catches identity leaks
- 4-tier pricing reviewed against ARPU benchmarks
- Welcome message templates deployed (3+ variants per source)
- Fanvue Creator Referral Program links live
- Real-person compliance docs reviewed and adopted
- Multi-platform: Fanvue + 1 other active (Fansly or ManyVids)
- Whale detection tracking deployed
- erotica-site /go/luna-fanvue wired and logging clicks
- Kit's runbook/C integrated (PPV-in-welcome, geo-block, automated messages)

**Effort:** 3-4 hours (down from 4-5 due to kit adoption)

---

### Session 2 ??? Mobile/desktop monetization audit

**Goal:** Identify which of 15+ existing apps are ready for paid tiers vs. killed/merged. Codify doctrine. Adopt kit's mobile IAP runbook E + RevenueCat webhook handler.

**Kit adoption:**
- runbook/E-mobile-iap.md ??? RevenueCat default; CANCELLATION???EXPIRATION warning
- `revenuecat-webhooks.ts` ??? production-tested event handlers
- Lemon Squeezy `lemonsqueezy-webhooks.ts` for desktop/web

**Apps in scope:** Feline-Calorie-Planner, AquaTrack / FloraTrack / BioTrackCore, KJV devotional, organism-atlas, biodiorama, abigail-app, auto-subs, email-triage, dental-claims-automation, homeschool-compass, purrfect-pair-tasks, paper-inventory, soul-conservatory, the-conservatory, Score, Anno + FlipScale/RORK-iFlip reference

**Payment stack decision tree:**
- Outcome-value pricing: 1-10% of outcome value
- 3-tier template: Basic/Pro/Premium, middle = 70% of buyers
- Conversion targets: 2-5% visitor???buyer, 3-5% buyer???review
- Stacks: RevenueCat (cross-platform mobile + paywall UI), StoreKit 2 (iOS-only), Google Play Billing (Android-only), Lemon Squeezy (web/desktop), Paddle (web sub + MoR), Stripe Billing + OpenMeter/Lago (high-volume metering)

**Deliverables:**
- `agent-skills/MOBILE-APP-MONETIZATION-AUDIT.md` ??? per-app table
- `agent-skills/PAYMENT-STACK-DOCTRINE.md` ??? decision tree + kit webhook handler recipes

**Success criteria:**
- Every app has a row with state + recommended stack
- 3-5 apps marked "monetize within 30 days"
- 2-3 apps marked "kill or merge"
- Pricing ladder template ready

**Effort:** 3-4 hours

---

### Session 3 ??? Video commerce + programmatic SEO

**Goal:** Short ??? product ??? commission flywheel + database-driven SEO pages. Adopt kit's runbook D (video commerce) and runbook B (SEO/affiliate).

**Kit adoption:**
- runbook/D-video-commerce.md ??? YT eligibility + TikTok Shop pilot + own-store hedge
- runbook/B-seo-affiliate-stack.md ??? `/go/` router already wired from Session 1, just add affiliate offers
- affiliate-layer offers.json extension (Amazon Associates, TikTok Shop, etc.)

**Custom work:**
- pSEO architecture (database-driven pages: city ?? service ?? attribute matrices)
- WP Content Autopilot evaluation (build vs install)
- Apply both to meme-merch + shame-seo

**Deliverables:**
- `content-factory/docs/CONTENT-TO-COMMERCE-FLYWHEEL.md`
- `agent-skills/PSEO-ARCHITECTURE-DOCTRINE.md`
- Kit offers.json extended with meme-merch + shame-seo offers
- 1 sample pSEO matrix for shame-seo

**Success criteria:**
- content-factory routes any Short to a product link
- meme-merch has at least one product live in TikTok Shop Open Collaboration
- pSEO matrix generates ???50 indexable URLs

**Effort:** 3-4 hours

---

### Session 4 ??? Affiliate program doctrine + event schema

**Goal:** Codify when to RECRUIT affiliates TO your brand. Kit's affiliate-layer provides the runtime; session adds the doctrine + per-project integration.

**Kit adoption:**
- `affiliate-layer/` (full): `/go/:slug` router, Disclosure component, FTC copy, offers.json, schema.sql
- runbook/B-seo-affiliate-stack.md

**Custom work:**
- Decision tree: self-host Refferq vs Impact/CJ/Awin
- Per-project offer sets (shame-seo, meme-merch, erotica-site, service-businesses)
- Event schema doctrine (page_view, cta_click, link_click, email_submit, etc. + minimum fields + SQL schemas)
- Cross-pod attribution dashboard

**Deliverables:**
- `agent-skills/AFFILIATE-PROGRAM-DOCTRINE.md` ??? decision tree + Refferq setup if self-hosting
- `agent-skills/EVENT-SCHEMA-DOCTRINE.md` ??? unified event taxonomy
- Per-project offers.json files
- FTC disclosure adoption across monetized pages

**Success criteria:**
- Decision tree answers self-host-vs-network question
- /go/ deployed and logging on at least 3 projects
- Event schema adopted by at least 3 pods
- Cross-pod attribution dashboard working

**Effort:** 3 hours (down from 3-4 due to kit adoption)

---

### Session 5 ??? Ad network progression

**Goal:** Lock Display Ads revenue lever across content sites. Kit says: don't bother with Prebid/GAM until 100k+ sessions. Agreed.

**Scope:**
- AdSense Auto Ads (start here)
- Ezoic migration criteria (10K+ daily visits)
- Prebid.js + GAM (only at 100K+/day)
- Apply to: erotica-site, shame-seo, meme-merch landing pages

**Deliverable:** `agent-skills/AD-NETWORK-PROGRESSION.md` ??? decision tree + migration triggers

**Effort:** 1 hour

---

## Tier 2 ??? later, not urgent

- **B.** AI fork A/B test (Track B) ??? adopt money-path + litellm + runbook/A when launched. A/B signal: ARPU per AI fork vs Luna. >50% Luna ARPU = scale; <25% = kill.
- **F.** Service-business Stripe Billing setup ??? adopt money-path webhook handlers
- **G.** Gumroad / Payhip product positioning ??? pair with kit's Lemon Squeezy handlers
- **H.** Affitor skills install ??? affiliate content ops automation
- **I.** Stripe usage-billing ??? kit covers SaaS path; add OpenMeter only if multi-dimension invoicing needed
- **J.** Newsletter monetization (Beehiiv)
- **K.** Reddit Ads as paid acquisition
- **L.** Discord Server Subscriptions
- **M.** Multi-language personas (post-Track A)
- **N.** Persona marketplace / licensing (post-Track B)

---

## Tracking

- Session log: `~/Sessions/<timestamp>_*/summary.md` per session
- Evidence: `~/Projects/ecosystem-command-center/initiative-evidence.json`
- CHANGELOG: top-of-project entry per touched project
- Resume: `.handoff/LATEST.md` if interrupted mid-session
- Kit location: `~/Projects/undercontent/vendor/monetization-kit` (Session 1) or shared `~/Projects/vendor/monetization-kit` (cross-pod)

## Resume protocol

If stopped mid-session, write `.handoff/LATEST.md` to active project with: WIP / Open Qs / Files Touched / Next.

---

## Next session: **1 (Luna real + AI obscuration + Fanvue operator + real-person compliance)**

**Why first:** Live revenue. Kit adoption cuts effort by ~40%. Only 4 custom gaps remain.

**Start trigger:** River status confirmed + LoRA reference dataset provided + kit installed in working repo.

**Kit install command:**
```bash
mkdir -p ~/Projects/undercontent/vendor
cp -r /home/ichabod/tmp/zip-audit/monetization-kit ~/Projects/undercontent/vendor/monetization-kit
cd ~/Projects/undercontent/vendor/monetization-kit && npm test
```

---

## Version history

- **v1** (2026-08-19 10:58 UTC) ??? 5-session sequence A???E (mobile audit, video commerce, affiliate doctrine, Fanvue playbook, ad network)
- **v2** (2026-08-19 11:35 UTC) ??? Reordered: Session 1 = AI companion + agency + compliance. Discarded "Build the Revenue Router" advice.
- **v3** (2026-08-19 11:55 UTC) ??? Critical correction: Luna is real. Session 1 = Track A only (Luna real + AI obscuration); Track B deferred to Tier 2. Real-person compliance doctrine.
- **v4** (2026-08-19 12:25 UTC) ??? **Kit adoption integrated.** Session 1 narrowed from 5 sub-sections to 6 (with 3 adopting kit wholesale). Effort down from 4-5 hrs to 3-4 hrs. Cherry-pick map per session added. Kit's `runbook/C-fanvue-operator.md` adopted for Session 1C. Kit's `affiliate-layer/` adopted for Session 1F + Session 4.
