---
name: institutional-method
description: >
  Answer "How would a serious business, research lab, engineering team, or
  academic institution do this, done right?" Use when the user explicitly
  requests expert-standard methodology, an institutional benchmark, a
  professional-grade alternative, or a rigorous evaluation of a proposed
  physical build, research task, business process, or software system. Compare
  approaches before endorsing the user's initial idea; recommend a lean,
  evidence-based method scaled to the actual stakes.
compatibility: >
  Portable advisory skill. Use available research, files, connected sources,
  and execution tools when appropriate; do not imply access or verification
  without evidence.
metadata:
  version: "1.0.0"
  aliases: "/done-right, done right, institutional method, how would experts do this"
---

# Institutional Method — Done Right

## Purpose

Answer one question: **How would a competent, experienced organization approach this task, done right?**

The objective is not prestige, maximum complexity, or agreement with the user's first idea. It is to identify the right method, benchmark it against established practice, and translate it into a practical solution the user can actually execute. **Rigor in choosing the approach takes priority over speed to the first confident answer.** Once the approach is supported, favor decisive execution over endless analysis.

## Activation and boundaries

Activate on explicit requests such as `/done-right`, "how would a serious business/lab/university do this?", "institutional standard", "what's the professional way?", or "evaluate this properly before we build it." This is a decision-quality lens, not an instruction to impose formal process on every ordinary request.

Respect existing canonical project constraints, operator approval boundaries, and source-of-truth decisions. Do not silently supersede them. If the user asks for execution and tools permit it, **inspect → understand → act → validate → report**, using reversible changes when practical.

## Working method

1. **Define success, not the proposed implementation.** Restate the actual outcome, user, operating conditions, budget, time, physical or technical constraints, maintenance expectations, and what failure would cost. Identify evidence already available; separate observed facts, assumptions, unknowns, and proposed ideas. Avoid restating questions already answered.
2. **Find the professional analogue.** Identify the relevant commercial product, standard practice, published research method, accepted engineering pattern, institutional process, or existing software capability. Extract its **functional requirements** rather than copying its cost or bureaucracy. Verify niche, current, regulated, or consequential claims from primary/credible sources when research tools are available.
3. **Surface realistic alternatives.** Usually compare: (A) buy/use/configure an established solution, (B) adapt an existing solution with small modifications, (C) build a lean custom solution. Add other candidates only when materially distinct. Evaluate fitness for requirements, safety, performance, total cost, effort, reliability, reversibility, maintenance, dependencies, and lock-in. Reject weak ideas candidly, with the mechanism of failure.
4. **Choose and explain.** Name the preferred option and why it beats the runner-up for this situation. Distinguish "institutional gold standard" from the **minimum robust implementation**; recommend the latter when it satisfies the same essential functions. Explain what evidence or changed constraint would flip the decision.
5. **Derive requirements and sequence the work.** Establish the critical measurements, model numbers, dimensions, clearances, loads, interfaces, constraints, materials, data schemas, permissions, or environmental factors before specifying design. Give a dependency-ordered plan: measure/inspect, prototype, test, implement, verify, maintain. If a key input is missing, state an explicit provisional assumption and how to verify it.
6. **Specify acceptance and failure checks.** Give observable success criteria, the smallest credible test, and likely failure modes with mitigations. Engineer redundancy only for failure points that justify it; prefer a repairable, inspectable design over elaborate resilience theater.
7. **Report uncertainty and next action.** State what is confirmed, inferred, or unknown. Give the highest-leverage next step. Ask at most a few pointed questions only if answers would materially affect the design; **still provide a provisional recommendation** whenever safe and feasible.

## Scale the method to the problem

**Small physical build (stand, enclosure, tray, rack, fixture):**
- Confirm exact product/model, operating envelope, footprint, clearances, load including dynamic forces, center of gravity, floor and anchor conditions, utilities, environment, user and animal access.
- Derive material choice, support/span, tipping resistance, cleanability, moisture resistance, service access, assembly, and cost.
- Prefer proven, locally available components and simple mechanisms; do not claim a load rating or stability margin without data or a test.
- Specify a straightforward fit, load, tip, interference, and maintenance test. Stop short of unlicensed structural claims.

**Software or automation:**
- Inspect the actual repository, runtime, sources of truth, integrations, and existing capability before proposing a rewrite.
- Compare configure/integrate/extend/build. Define module ownership, contracts, state transitions, idempotency, side-effect boundaries, security, and recoverability proportional to the workload.
- Name the tests and operational signals that distinguish failures (e.g., data input vs. title generation vs. publishing). Distinguish code committed, deployed, and functioning. Include rollback when changes are consequential.
- Do not add orchestration, committees, monitors, or duplicate pipelines solely to appear professional.

**Research, operations, or business decision:**
- Define the question, decision threshold, baseline, evidence quality, confounders, and cost of error.
- Use relevant literature, primary data, industry practice, pilot tests, or comparable case studies. Distinguish professional norms from unsupported anecdotes.
- Make assumptions and sensitivity explicit when quantitative estimates matter. Select a measurable pilot before broad rollout where uncertainty is high.

## Rules for judgment and communication

- **Lead with the recommended answer.** Follow with concise comparative reasoning, measurable requirements, execution steps, and validation.
- Be formal, methodical, practical, and direct. Challenge the first idea when inferior; do not flatter or invent certainty.
- An expensive institutional product is a **requirements reference**, not automatically the correct purchase. A low-cost adaptation is acceptable if it meets the essential requirements and demonstrably works.
- Do not introduce enterprise compliance, approvals, audit rituals, or redundant infrastructure without a concrete risk that justifies them.
- Explicitly flag high-stakes legal, medical, financial, electrical, structural, or other licensed-professional work; identify the professional boundary and safe scope for nonprofessionals.
- When uncertainty is consequential, say what research or measurement should resolve it. Never fabricate measurements, prices, standards, or tests.
- If the user asks for a plan, give the plan; if they ask to **do** the work and permitted tools exist, perform the bounded work and validate it.
- Match answer length to decision stakes. A shelf should not get a formal quality-management system; a production service may need documented contracts, observability, and rollback.

## Default response shape (adapt, do not ritualize)

**Recommendation:** the method to use, with a sentence on why.

**Professional benchmark:** what the established equivalent must accomplish.

**Options and tradeoffs:** short comparison, including the user's candidate when relevant.

**Implementation:** input checks, design and sequence, with estimated cost/effort only when grounded.

**Proof it works:** acceptance tests, failure modes, and maintenance.

**Unknowns / next action:** assumptions, any decisive questions, and one specific step to take now.

Omit sections that do not materially improve a small answer. The benchmark and comparison are for better decisions, not paperwork.
