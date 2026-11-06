# Conversation preservation inventory — 2026-11-06

Status: PARTIALLY COMPLETE. This is a **findability ledger** for the free-AI-provider conversation, not a claim that the original message was archived verbatim. Source thread originated 2026-11-05; review date 2026-11-06. No source binary assets were supplied or produced.

Canonical discussion and file collection: https://github.com/wowthisiseasytoremember-stack/agent-skills/pull/17

| Item produced or decided | Existing durable home | Preservation state / next action |
|---|---|---|
| Original 19-provider matrix (8 text/API; 8 web image; 3 GPU), quoted quotas/auth/catches | Derived assessment in `research/free-ai-provider-assessment-2026-11-05.md` | **GAP: not verbatim**; original chat remains only source. Preserve exact raw message to authorized GitHub or Drive archive, with attribution and dated unverified status. |
| Exact providers named | This inventory below | Names captured; quotas and claims need verification. |
| CDP / Google SSO checklist, browser profile, provider-specific action sequence, verification report JSON, safety notes | This inventory's checklist outline and local-agent brief | **GAP: full original code block and JSON not yet preserved verbatim.** Do not execute checklist blindly. |
| Corrections to Chutes, Featherless, SeaArt, Tensor, PixAI, Civitai and Lightning | This inventory and derived assessment | Captured as **user-supplied 2026 claims**, not verified. |
| New-provider notes for Pollinations, Puter, DuckDuckGo, TetisAI, nokeep, Hugging Face Spaces, Open Generative AI GitHub | This inventory | Captured as leads; validate independently. |
| Assessment decision: shared capability discovery and bounded provider fallback, NOT signup spree | `research/free-ai-provider-assessment-2026-11-05.md` | Committed on PR #17 branch. |
| Three factual correction leads (OpenRouter limits; Puter user-pays; Pollinations API authentication) with URLs | Derived assessment | Committed; re-verify before use. |
| Architecture sketch: provider metadata / verification / capability router / ledger | Assessment + `research/free-ai-provider-local-agent-implementation-brief-2026-11-06.md` | Committed; **proposed only**, no live system. |
| Uses for 6925 RELAY offline headlines/transcripts/comment drafts; Content Factory thumbnails/storyboards; Ichabod; agent-skills | Assessment + brief | Committed; no production activation. |
| Decision to delegate implementation to another agent and avoid conflict | PR #17 comment https://github.com/wowthisiseasytoremember-stack/agent-skills/pull/17#issuecomment-6673283108 | Posted; next agent must claim owner and link canonical implementation. |
| Concrete implementation objective, bounds, logical expected paths, acceptance and test cases | `research/free-ai-provider-local-agent-implementation-brief-2026-11-06.md` | Committed; self-contained for local model. |
| Security decisions: secrets out of git/logs, no unapproved billing/account creation, no stealth/ToS evasion, protect livestream | Assessment + prior handoff + brief | Committed. |
| Open questions: existing gateway owner? permitted providers? quotas? output rights? best pilot? | Brief; original preservation gap tracked separately | Unresolved until assigned implementation owner / verified test. |
| Source material and external citations | Official links in assessment; original message contained nonresolvable `[reference:39]` etc. placeholders | Do not present opaque reference IDs as citations; seek dated primary URLs. |
| Code/config produced in conversation | No executable code/config was created. Only illustrative JSON and shell/JS commands inside user-supplied checklist | No deployable code to commit; full snippet archival gap remains. |
| Binary images/PDFs/spreadsheets | None in conversation | No Drive upload needed for binaries. |

## Full research subject index (findability)

**Text/API:** OpenRouter, Venice.ai, AI Horde, Pollinations.ai, Puter.js, DuckDuckGo AI Chat, Featherless.ai, Chutes.ai.

**Web image:** Perchance, SeaArt, Tensor.art, PixAI, Civitai, Mage.space, TetisAI, nokeep.ai, Hugging Face Spaces (9 named image options, rather than the earlier rough count of 8).

**Cloud compute:** Kaggle Notebooks, Lightning.ai, Google Colab.

**Extra self-hosted lead:** Open Generative AI (GitHub).

**User-provided correction claims, unverified:** Chutes early 200/day offer ended March 2026; Featherless 3-day/100k-token trial then paid; SeaArt 130 stamina/day potentially 0 for some; Tensor around 50 credits/day; PixAI claim-based variable daily credits; Civitai Blue Buzz SFW only; Lightning standard ~22 GPU hours/month and possible initial 80-hour grant.

**Original checklist sections:** Chrome on localhost:9222 with persistent authenticated Google browser profile; Google login preflight; provider-specific login/account/key and minimal check for eight text providers, eight checklist image providers, and three GPU services; JSON report with provider reachability/login/quota; no credential automation, rate limits and encrypted secrets, restrictions on age gates. The original contains instructions referencing anti-detection and tunneling; these are **not approved execution requirements** and must be reviewed for service rules. Do not interpret Google SSO being present as consent to create accounts or keys.

**Illustrative code snippets in original:** `puter.ai.chat("hello")`; anonymous AI Horde key `0000000000`; `GET https://openrouter.ai/api/v1/models`; `GET https://aihorde.net/api/v2/status/heartbeat`; `GET https://text.pollinations.ai/hello` (possibly stale); ComfyUI `/prompt`; `!nvidia-smi`; Chrome debugging/profile flags; example provider JSON keys. These are archival references, **not tested or recommended commands**.

## Recommended next steps
1. **Preserve exact original raw source** as a dated unverified archival artifact with visible access controls, no edits to the content, and permanent link. The exact payload was previously rejected by the GitHub connector. Until then, the conversation-clearing test FAILS.
2. Implementation owner checks PR #17 and repo claims; records canonical issue/PR link before modifying code. Do not duplicate existing gateway work.
3. Owner does dated primary-source verification; documents actual provider eligibility and an offline pilot. Keep runtime disabled.
4. Update this inventory with exact archive URL, checksums if available, and pilot issue/PR and close outstanding preservation issue only after readback.

### Findability test
A reader with only this document can identify the project, the decision, intended architecture, limits, owner coordination, and what's missing. They **cannot recover the full exact source matrix and CDP instructions yet**. That is an explicit outstanding failure, not a completed archival claim.
