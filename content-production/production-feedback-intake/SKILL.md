---
name: production-feedback-intake
description: >-
  Ingest noncanonical agent, human, or automated feedback about content
  production. Break long reviews into source-linked individual claims, detect
  duplicates and contradictions, separate reliable technical constraints
  from aesthetic preferences and local bug reports, and route only approved
  recommendations into existing project production profiles. Trigger on
  "ingest editorial feedback", "other agents reviewed the edit", "production
  polish recommendations", "turn agent critique into standards", and
  cross-project media quality feedback.
compatibility: >-
  Portable read-only review skill. Optional durable Git/Drive persistence.
  No production service, publisher, media tools or credentials required.
metadata:
  version: "0.1.0"
  aliases: "ingest production feedback, editorial feedback review"
---

# Production Feedback Intake — noncanonical by default

## Goal

Convert mixed-source critique into **usable, reversible production knowledge** without treating every advisor's instruction as a new rule. Work across commentary, educational/video content, voiceovers, written pieces and different brands. Do **not** impose the same treatment or format on every product.

**Ingestion is not approval, implementation, publication, deployment or skill activation.** A mature content production system has fewer shared invariants and clearer per-format recipes—not a growing universal list of filters and gates.

## Intake sequence

1. **Provenance:** record source name, owner if known, date, privacy level, raw content hash or durable ref, version, and whether it is an observation, proposal or instruction. Preserve the original privately if it contains sensitive project/media details. Never publish private incident logs or unverified allegations in shared skills.
2. **Atomize:** split a 500-line critique into independently decidable claims. Keep exactly one action or proposition per record. Give each a stable ID and line/source anchor. Deduplicate repetitions while preserving distinct alternatives and source attributions.
3. **Type each claim:** `technical_constraint`, `observed_defect`, `editorial_principle`, `style_option`, `format_parameter`, `platform_requirement`, `factual_claim`, `implementation_proposal` or `unsupported_assertion`.
4. **Normalize scope:** `cross_content`, `video_only`, `audio_only`, `written_only`, `project_specific`, `format_specific`, `individual_asset`. Use exclusions as well as inclusion: a face-centered political thumbnail rule is not a reptile/plant thumbnail rule.
5. **Reconcile:** locate repeated/overlapping ideas and **direct contradictions**. Compare independently against source code, files, final media, platform docs, user-approved style, and measured viewer outcomes when accessible. Prefer evidence of actual production behavior to confident critique prose.
6. **Recommend, not promote:** mark `candidate`, `supported_noncanonical`, `disputed`, `conditional`, `rejected`, `already_satisfied`, `superseded`. Do not write adopted/canonical just because multiple agents agree. Record what missing evidence or owner decision would change the classification.
7. **Route to an existing owner and spec:** existing editorial/playbook/brand config and GitHub PR before creating any new artifact or ticket. Do not edit active local work. For cross-project use, publish only the **generalized method**; preserve project-specific records in the project’s private repository.
8. **Act once evidence warrants it:** if the user authorized implementation, perform an isolated smallest useful production change; request actual local media only for A/V or hardware-bound decisions. Keep any new work on an owner-safe branch. Do not create a second renderer or publishing lane to consume advice.
9. **Evaluate results:** the best output is a better clip, source-true title/cover, readable caption, clean sound or correct metadata—not a larger test/gate inventory. Record before/after effects and limitations when measurable. A technical unit test does not prove better editorial taste.

## Record format

Use one JSON object per independent candidate; prefer a project-owned `normalized.json` and a concise `DECISION_MAP.md` when no existing evidence schema fits:

```json
{
  "id": "F001",
  "source": {"ref": "<durable private source>", "lines": "L10-L22"},
  "claim": "A meaningful recommendation in one sentence",
  "type": "editorial_principle",
  "scope": ["video", "long_form"],
  "excludes": ["animal-specimen timelapse"],
  "conflicts_with": ["F003"],
  "status": "candidate",
  "evidence": "source proposal only",
  "owner": "existing editor/brand owner",
  "decision": null,
  "promotion_evidence": null,
  "production_write_authorized": false
}
```

Separate `status` (the evidence disposition) from `decision` (the actual owner’s explicit adopted/rejected choice), and separate **all** of those from deployment state. Use source hashes/immutable commits so one critique cannot overwrite a later revision.

## Decision hierarchy

- **Hard technical invariant:** may be recommended broadly after independent verification (e.g. input/output timing identity, no mislabeled sources, valid caption clock), but still does not authorize edits to an installed service.
- **Format/profile rule:** choose per brand and output (9:16 HOT Short, 16:9 episode, wildlife macro, spoken podcast, article, etc.). Contradictory suggestions may both be right for different profiles.
- **Creative experiment:** choose a reversible visual/audio comparison with a success criterion; no global filter chain based on an untested aesthetic opinion.
- **Project-specific bug:** route to that project's existing issue/PR and do not pollute the shared skill.
- **Unsupported/incorrect claim:** retain with explanation so a cold agent does not rediscover or blindly implement it.

Examples to watch for: input GOP cuts vs segment encoding; loudness measurement vs a universally asserted LUFS target; static title card vs Ken Burns; stings vs music beds; editorial chronology vs capture timestamps; title promises vs exact rendered content; legal claims made only by MP4 metadata.

## Cross-project profile inheritance

Keep profiles **per output**, not one universal media profile.

```
Shared content invariants
  ├── political commentary / hot vertical short
  ├── commentary / edited long-form
  ├── animal and plant education / macro vertical
  ├── documentary explainer / landscape
  ├── spoken audio / podcast
  └── written / social content
```

Common invariants: truthful provenance, coherent structure, accessible and readable presentation, source-compatible media processing, platform-appropriate delivery. Do **not** inherit stylistic opinions (faces, loudness numbers, transitions, colors, hooks, music, typography) without matching the chosen product profile.

## Stop conditions and reporting

- Stop promotion when project ownership, source integrity, media, rights, or existing status is unknown. **Do not stop extraction or independent analysis** for that reason.
- Never claim a design or sound change is proven by a renderer test alone.
- Never infer that many agreeing LLM outputs constitute multiple independent experiments.
- Do not unilaterally alter publish authority, first comments/replies, credentials, release timing, user identity or rights claims.
- Keep the result compact: counts of unique records, meaningful conflicts, strongest reusable candidates, rejected overreach, project-specific routes, and **one recommended next production improvement**.

This skill is a method for evaluating feedback. It intentionally contains **no universal FFmpeg preset or canonical editorial taste rubric**.
