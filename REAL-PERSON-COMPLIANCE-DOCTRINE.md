# REAL-PERSON COMPLIANCE DOCTRINE

**Created:** 2026-08-19 12:35 UTC
**Owner:** Justin + agents
**Status:** active doctrine
**Applies to:** any project where Justin (or any real, identifiable person) appears in monetized content
**Does NOT apply to:** AI-fork personas (Track B — River) — those use the AI-persona compliance framework (separate doc, to be written)

---

## Why this exists

Kit's `runbook/C-fanvue-operator.md` covers platform ToS for Fanvue and X — that's necessary but NOT sufficient for **real-person** monetization.

When the persona is the operator themselves, additional compliance applies:
- 2257 record-keeping (federal record-keeping requirement for depictions of real adults in commercial sexual content)
- KYC / age verification records (you must be able to prove age)
- Identity protection (the whole reason for face obscuration)
- Platform-specific variability on what counts as "stylized vs identifiable"
- Persona rights (YOU own Luna, no platform can revoke "their" character)
- Payment processor risk (each platform = different processor, different ToS)

If you skip this layer, the failure modes are:
- FTC action (no disclosure / wrong disclosure)
- 2257 violation (no records on real-person content)
- Platform ban (account compromised = all 4 personas gone, all history lost)
- Chargeback wave (card disputes → processor freezes funds → legal exposure)
- Identity leak (the explicit risk that started this whole pipeline)

## Hard constraints (from undercontent/AGENTS.md Decomposition Addendum)

These are non-negotiable for any Luna (real-person) content:

- [ ] All depicted persons are 18+ — Luna is real, 19, KYC records on file
- [ ] Consent and rights are documented — Luna = Justin, written self-consent record required
- [ ] No deceptive impersonation — never claim AI character is real person or vice versa
- [ ] No minors / "barely legal" positioning — explicit ban
- [ ] No explicit material in prohibited profile areas (X avatar/banner, List banners, Community covers, live video)
- [ ] Geo-blocking considered — block jurisdictions with restrictive adult laws
- [ ] Subreddit/community rules checked before posting
- [ ] Platform monetization rules separated from traffic rules
- [ ] EXIF stripped from all uploaded images (`exiftool -all=`)
- [ ] Face-visible ratio ≤ 20% on Luna assets
- [ ] AI content tagged #AIGenerated on Fanvue — never deny being AI
- [ ] Partner written consent + age-verification records required before any partner content

## 2257 record-keeping (CFR Part 75)

**Who this applies to:** All producers of sexually explicit content depicting real, identifiable persons.

**For Luna:**
- Primary records custodian: Justin (operator)
- Required records:
  - Luna's (operator's) legal name + alias ("Luna")
  - Date of birth (verify 18+)
  - Government-issued ID copy (passport, driver's license)
  - Self-consent statement (signed, dated)
  - Photo sample with date stamp (proves the depiction)
  - Statement that records are kept at the operator's address

**Storage:**
- Encrypted at rest (AES-256 minimum)
- Offline backup (encrypted USB or external drive in safe)
- Cloud backup only with end-to-end encryption (e.g., Tresorit, Cryptomator)
- Retention: minimum 5 years from content publication date (some jurisdictions require 7)
- Access: only the operator + legal counsel

**What's NOT required:**
- Records for AI-generated content (no real person depicted) — River (Track B) doesn't need 2257 records
- Records for stylized art that doesn't depict an identifiable real person (oil painting of fictional character)

**Practical setup:**
```
~/secure/luna-2257/
├── README.md                           # this doctrine reference
├── records.json                        # encrypted index
├── ids/
│   ├── passport.pdf.enc                 # age verification ID
│   └── drivers_license.pdf.enc          # secondary ID
├── consent/
│   ├── self-consent-2026-XX-XX.pdf.enc  # signed consent statement
│   └── notarized-version.pdf.enc        # if notarized (recommended)
├── samples/
│   ├── 2026-08-19_001.png              # dated photo sample per major shoot
│   └── 2026-08-19_002.png
└── keys/
    └── gpg-public-key.asc               # for future disclosure if required
```

Use `gpg --symmetric --cipher-algo AES256` for encryption. Store passphrase in password manager (1Password / Bitwarden / KeePass).

## KYC / age verification

**For Luna's Fanvue account:**
- Real ID submitted to Fanvue during creator signup
- Persona email via ProtonMail (per AGENTS.md)
- Age verification record (same as 2257 records above)
- Geo-block for non-served jurisdictions

**Cross-platform age verification:**
- Fanvue: handled at signup
- X: birth date in profile settings (no AV provider required for adult creator track IF labeled correctly)
- Reddit: not required for non-verification subs; skip verification subs until partner/consent templates exist

**Crypto payment rails (per AGENTS.md "Do Not" — no Stripe for adult):**
- XMR primary, BTC backup for tips
- Round numbers only
- Non-custodial wallets
- Convert to fiat regularly ($500 threshold per AGENTS.md)
- Document crypto earnings separately for tax (US: IRS treats as ordinary income)

## Platform-specific variability on stylization

**The core question:** when does "stylized art of me" cross into "identifiable real person"?

Per X Adult Content policy (verified May 2024):
- Heavy stylization (LoRA-trained artistic painterly mode) = NOT identifiable = treated as art
- Light stylization (LoRA at 0.7 identity preservation, recognizable features) = may be flagged for some platforms
- Minimal stylization (LoRA at 0.1, mostly original photo with effects) = identifiable = full disclosure + KYC records

**Per-platform checklist:**

| Platform | Luna artistic painterly | Luna trippy | Luna obscure silhouette | Luna cinematic |
|---|---|---|---|---|
| **Fanvue** | OK with #AIGenerated tag | OK with tag | OK with tag | OK with tag |
| **X** | OK if labeled (not avatar/banner) | OK if labeled | OK if labeled | OK if labeled |
| **Bluesky** | OK with adult label | OK with adult label | OK with adult label | OK with adult label |
| **Reddit** | OK in most subs (verify per sub) | OK in most subs | OK in most subs | OK in most subs |
| **Telegram** | OK | OK | OK | OK |
| **Discord** | OK (per server rules) | OK | OK | OK |
| **Meta (FB/IG)** | AVOID (Meta stricter) | AVOID | AVOID | AVOID |

If Luna's stylized art gets mistaken for a photo of an identifiable third party, you have an impersonation / harassment issue. Always confirm output doesn't accidentally look like a specific public figure.

## Persona rights

**Luna = Justin.** Documented:

1. **Operator self-consent statement** — signed, dated, notarized (recommended)
2. **Operator owns Luna IP** — Luna is not a platform-owned character; if Fanvue / X bans the account, you retain all rights to the character
3. **No platform can revoke "their" character** — because it's yours
4. **Persona bible is operator property** — voice rules, face caps, hard limits are YOUR constraints, not platform rules

This matters because:
- If Fanvue bans Luna's account, you can move to Fansly (Track B River can't, but Luna Track A can)
- If X tightens adult content rules, you can pivot to Telegram + Bluesky without losing Luna
- If any co-founder / VA / agency gets compromised, you can revoke access and Luna stays intact

## Multi-platform payment processor risk

**Per-platform processor landscape:**

| Platform | Processor | Adult-friendly? | Risk |
|---|---|---|---|
| Fanvue | Fanvue's own + Stripe Elements (behind the scenes) | YES (Fanvue specializes) | Low — Fanvue designed for this |
| Fansly | Fansly's own | YES (but BANS AI personas per 2025) | N/A for Luna Track A? Actually allows real-person creators. Could be overflow. |
| LoyalFans | LoyalFans' own | YES | Low — adult-friendly |
| OnlyFans | OF's own | YES | Low |
| X (Tips) | Stripe | NO for adult (Stripe freezes) | HIGH — use crypto instead |
| Reddit | None | N/A | None |
| Telegram | Stripe via bot OR crypto | Depends | Use crypto |
| Direct website (Shopify/independent) | Stripe | NO for adult | Use CCBill/Segpay/crypto |

**Mitigation per platform:**
- NEVER use Stripe for adult revenue (AGENTS.md "Do Not")
- Activate CCBill OR Segpay as backup high-risk processor (apply early — long underwriting)
- Activate Coinbase Commerce / BTCPay Server as crypto backup
- Test each processor with $1 transaction end-to-end before launch

**Per AGENTS.md "Pitfalls":**
> Skipping the $1 payment processor test: Activate and test at least one Tier 2 processor (Easy Pay Direct, CCBill, or Segpay) and one Tier 3 (Coinbase Commerce, BTCPay Server, CashApp/Venmo/Zelle) with a $1 transaction end-to-end before launch.

## Fan-trust disclosure (the "is this AI?" question)

**Real Luna fan concern:** "Wait, is the person I'm chatting with the same person in the photos?"

**Honest answer:** "It's stylized art of me — I keep my actual face private for safety. The voice messages are me (if voice cloning approved), the DMs are me, the custom content is my writing."

**Frame to use (per AGENTS.md voice rules):**
- Never claim "I'm a real person and these are unedited photos"
- Never claim "I'm 100% AI" if it's actually stylized art of you
- Rotate disclosure tags on Track A: `[illustrated]`, `rendered, not a photo`, `art, not photography`, `stylized piece —`
- For Track B River: clearly state "AI-generated character. everything here is synthetic — no real person depicted"

**If asked directly "are you AI?":**
- For Luna Track A: "Stylized art of me. Real person, AI aesthetic."
- For River Track B: "Yes, AI-generated character. No real person depicted."

## Adult content age verification tooling (UK Online Safety Act / EU AI Act / US state laws)

**2026 regulatory landscape:**
- UK Online Safety Act — age verification mandatory for adult content accessed by UK users
- EU AI Act — AI-generated intimate content requires age verification + disclosure
- US state laws (Texas, Utah, others) — age verification for adult content
- All spreading through 2027

**Implications for Luna:**
- If Luna content is accessible in UK/EU, age verification required
- Third-party AV providers (Yoti, Age-Verify, Veratad) can be integrated at the platform level
- For direct website (Luna's own landing page): need AV gate before any adult content
- For platform-based (Fanvue/OnlyFans): handled at signup, no action needed

**If you build Luna's own landing page:**
- Use a third-party AV provider as the front gate
- Block VPN/proxy traffic (some jurisdictions)
- Geo-block high-restriction states (per AGENTS.md — geographic risk)
- Log AV verification attempts (for compliance audit)

## Checklist for launching Luna Track A content

Per-session, before any publish:

- [ ] EXIF stripped (`exiftool -all=`)
- [ ] Provenance logged (prompt, model, seed, timestamp, operator)
- [ ] Face-visible ratio check (≤20% Luna assets)
- [ ] Disclosure tag applied (rotated from approved list)
- [ ] Voice rules respected (Luna voice: she/her, "hehe"/"uwu" max one)
- [ ] Hard limits respected (no slurs, no minors, no in-person claims)
- [ ] Age markers in prompt (adult context)
- [ ] Free-use phrasing not (banned phrasings)
- [ ] Banned "Daddy" density (1 per 50 posts)
- [ ] Platform-specific ToS verified for the channel
- [ ] Geo-block active for the account
- [ ] 2257 records updated if new shoot/sample
- [ ] Consent on file (always — for Luna = self-consent)

Quarterly review:

- [ ] 2257 records audit (complete, encrypted, accessible)
- [ ] KYC records audit (Fanvue, X, any platform)
- [ ] AV provider logs reviewed (if applicable)
- [ ] Crypto earnings reconciled with fiat conversions
- [ ] Platform ToS reviewed for changes (Fanvue announces policy changes via RSS)
- [ ] Tax prep: quarterly estimated taxes + self-employment tax
- [ ] Backup integrity verified (encrypted, recoverable)

## Open items

- [ ] Justin: write + sign self-consent statement (template below)
- [ ] Justin: get notarized version (recommended)
- [ ] Justin: set up encrypted 2257 records storage (`~/secure/luna-2257/`)
- [ ] Justin: submit KYC to Fanvue (real ID + age verification)
- [ ] Justin: activate CCBill OR Segpay as backup high-risk processor
- [ ] Justin: activate Coinbase Commerce / BTCPay Server as crypto backup
- [ ] Justin: test $1 transaction on each Tier 2 + Tier 3 processor end-to-end
- [ ] Justin: choose AV provider (Yoti, Age-Verify, Veratad) IF Luna's own landing page is built
- [ ] Agent: build AV gate template (Hugo shortcode + Netlify Function) for future Luna landing page
- [ ] Agent: build 2257 records audit script (checks completeness, encryption status, retention)

## Self-consent template (for Justin to fill)

```
SELF-CONSENT STATEMENT

I, [Legal Name], born [DOB], holder of [ID type + number], residing at
[address], hereby consent to the creation, distribution, and monetization
of adult content depicting my likeness under the persona "Luna" (a
stylized-art rendering of myself).

I confirm that:
- I am 18 years of age or older (currently 19 years old)
- I am the sole operator of the "Luna" persona
- I retain full intellectual property rights to the Luna persona
- I understand the platform-specific monetization risks
- I have set up 2257 record-keeping per CFR Part 75
- I have KYC records on file at all platforms where Luna content is monetized

This consent is given freely, without coercion, and may be revoked at any
time by ceasing publication and notifying platforms to remove content.

Signed: _________________________  Date: _____________

Witness (optional): _________________________  Date: _____________

Notary (recommended): _________________________  Date: _____________
```

Notarization is recommended but not federally required. Some states have specific requirements — consult an adult-industry attorney per AGENTS.md "Hard Constraints":

> No revenue flows until adult-industry attorney consult — neither LLC is formed yet; attorney required before any revenue.

## Reference

- `undercontent/AGENTS.md` Decomposition Addendum — hard constraints (foundation)
- `undercontent/MASTER-PLAN.md` — entity structure, attorney consult
- Kit `runbook/C-fanvue-operator.md` — platform ToS (subset of this doctrine)
- `multiple-money-plans/persona-content/video-clip-pipeline.md` — provenance log pattern
- `catboy2/BUILD-PLAN.md` — entity separation
- `catboy2/femboy/personas/COMPOSITION-SPEC.md` — face caps, identity framing
- 18 U.S.C. § 2257 and 28 CFR Part 75 — federal record-keeping requirements
- FTC Endorsement Guides — disclosure requirements
- UK Online Safety Act 2023 — age verification for adult content
- EU AI Act 2024 — AI-generated intimate content requirements
- Texas HB 1181 (2023), Utah SB 287 (2023) — US state AV laws