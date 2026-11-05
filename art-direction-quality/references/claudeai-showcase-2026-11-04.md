# Source review: AI-built interfaces that do not feel generic (2026-11-04)

**Source:** [r/ClaudeAI thread: Show me Claude Code projects that DON'T look vibecoded](https://www.reddit.com/r/ClaudeAI/comments/1xnnqkg/show_me_claude_code_projects_that_dont_look/).

**Purpose:** Capture examples, meaningful disagreements and actionable implications behind the [Art Direction & Visual Quality skill](../SKILL.md). This is a **dated research snapshot**, not a current ranking of the linked sites, a claim that a particular technology made the result, or evidence of broad user consensus. Participants self-selected; comments are qualitative, sometimes conflicting; some links can change or break.

## Examples worth borrowing from — and what not to copy

| Example | What contributors showed/said | Transferable lesson | Caution |
| --- | --- | --- | --- |
| [Sadok Cervantes — playable Game Boy Color portfolio](https://sadok.mx/) | Commenter describes lengthy, carefully referenced prompting and a detailed 3D model. Live site exposes a **plain all-projects list** and keyboard/game controls alongside the 3D mode. | A **single expressive organizing metaphor** plus thoughtfully sourced assets creates recognizability; provide functional fallback navigation. | The claim about agent orchestration and prompts is self-reported. A 3D gimmick is not right for every conversion-oriented project. |
| [Shapefinder — mouse finder](https://shapefinder.cc/) | A focused guided sequence asks hand/grip/budget questions and narrows a large product catalog. Commenters praised result relevance and useful filtering; one flagged a dark-mode asset problem. | Originality can come from **interaction design and domain expertise**, not visual spectacle. QA must include actual device themes. | Reported recommendation accuracy is anecdotal, not a measured benchmark. |
| [What's In Their Bag archive](https://www.whatsintheirbag.com/) | Rich cross-linked catalog of musicians, albums, episodes, and quotes. Commenters liked the archive, yet identified a generated-sounding tagline and the creator acknowledged generated copy. | **Real content, rich relationships, editorial usefulness** can carry a site. Strong UX still benefits from human copy editing. | Do not assume the whole site was automatically generated or all copy is poor. |
| [Jordan's Camp portfolio](https://jordanscamp.site/) | Owner describes a 3D space with a 2D blog through a laptop, guided by a frontend engineer's conception of structure. | Expressive 3D can coexist with a simpler reading route. Match medium to purpose. | Claims about development process and job impact are owner-reported. |
| [Italian Brawls](https://italianbrawls.it/) | Browser fighting game with distinctive subject matter and smooth phone performance reported by commenters. Other commenters thought AI character art was obvious. | **Fun, responsiveness and a strong premise** can succeed even when AI provenance is visually noticeable. | “Doesn't look AI-made” is not the real success metric if users enjoy and complete the experience. |
| [Gadavra — Soft](https://gadavra.itch.io/soft) | Developer says reference art direction is applied to every game UI element; image assets and repeated screenshot review drive polish. Also reports a crash in comments. | One **visual language, applied everywhere**, with handpicked assets and frequent screenshot feedback, yields coherence. | Self-reported workflow; visual polish does not guarantee runtime stability. |
| [TileSet](https://tileset.com/) | Maker says a UX designer reviews AI-built work and actively adjusts its appearance. Live site presents social proof embed product features and examples. | Human design review can be a specialized **quality gate** instead of rewriting the whole build. | This is testimony about process, not proof that the product's outcomes are superior. |
| [NovaDeck](https://novadeck.dev/) | Builder describes iterative prompts; respondents still flagged stock font, palette and staccato copy as generic. | **Iterating implementation without changing art direction or language** can preserve template identity. | The site could not be independently opened during this snapshot; criticism is sourced to the thread, not our own visual audit. |

## Repeated themes from the discussion

1. **Reference-first direction**: several recommend showing an actual Figma design, screenshots or an explicit inspiration reference rather than vague “make it beautiful” prompts.
2. **Secondary-screen leakage**: a reply notes that unmocked empty, error, loading and settings screens quickly revert to model defaults.
3. **Copy is the giveaway**: marketing snippets such as “Good company. Great radio.”, repetitive short paired sentences and prominent all-caps eyebrow labels drew unusually consistent criticism.
4. **Visual coherence is more than component reuse**: the Gadavra developer explicitly describes applying a source art style to *every* prompt, window and button.
5. **Evidence must be visual**: the same developer recommends inspecting rendered screenshots, testing states and finding cropped text, incorrect art and broken interactions.
6. **Subjective aesthetic judgments differ**: some called Italian Brawls obviously AI-made but still delightful; a few criticized conventional sites for excessive polish or similarity to popular games.
7. **Default patterns aren't inherently wrong**: generic palettes, rounding, shadows and cards become weak when adopted without a reason. A restrained business utility may legitimately use them.

## Design rules derived from themes (interpretive, not Reddit facts)

- Brand + outcome + visual reference before components.
- Art direction as a documented contract, not a single hero screenshot.
- Reference fidelity throughout all screens and states.
- Purposeful licensed images/assets and task-appropriate interaction.
- Full editorial rewrite of visible copy, including system messages.
- Screenshot and device review as a release gate.
- Different tradeoff policies for expressive portfolios, utilitarian dashboards and editorial/video packages.
- Preserve approved creative decisions; don't overwrite prior work with a generic universal aesthetic.
- Capture examples in a source-backed reference file and change the operating skill only when repeated evidence or a concrete failure warrants it.

## Applied examples for current project classes

| Project class | Direction | Acceptance check |
| --- | --- | --- |
| Professional portfolio | Expressive hook if it demonstrates capability; readable projects and direct contact always accessible | Contact/resume reached on mobile and keyboard without a 3D dependency |
| Biological collection tool | Organism photography/metadata and taxonomy hierarchy, not decorative biotech imagery | Users can locate, compare and update an organism; all empty/invalid states coherent |
| Lash service website | Real work samples, service specificity, trust and conversion | Booking/service action prominent and operational on iPhone |
| Video/shorts graphics | Continue the approved editorial brand, refine rhythm, contrast and animation | Burned subs and logo readable at phone size; clip metadata accurate |
| Operations dashboard | Semantic status, evidence, provenance and obvious next action | Error/empty/loading state tested; data semantics correct |

## What this review did not verify

- No author source code or production analytics were audited.
- No objective usability study, controlled A/B test or participant sampling occurred.
- The examples were inspected through publicly accessible page text and comments, **not systematic full-device visual screenshots**.
- We cannot verify claims about exact agent orchestration, percentages of generated code, development duration or actual visitor outcomes.
- A live website can differ from its Reddit description after this snapshot.

**Maintenance:** cite this page when justifying a future design rule. Revisit when a project produces actual before/after screenshots, user task observations or measurable performance outcomes. Prefer direct product evidence over Reddit taste alone.
