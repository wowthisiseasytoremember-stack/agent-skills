---
name: product-strategy-master
description: Master orchestrator for product planning, metrics, and roadmap strategy. Use when the user asks for high-level project planning, market analysis, or roadmap development. This skill coordinates sub-skills for OKRs, experiments, discovery, and launch readiness.
---

# Product Strategy Master

## Overview
This is the master orchestrator for the Product Strategy squad. It routes high-level product requests to the specialized sub-skills in the `product-team/` directory (vendored from alirezarezvani/claude-skills, MIT).

## Core Capabilities
When triggered, this skill will analyze the request and decide which of the following sub-skills to activate in parallel:

1.  **Strategy & Roadmapping:**
    *   `product-strategist`: Breaking OKRs into initiatives with success metrics.
    *   `roadmap-communicator`: Translating roadmap/sprint state into exec-facing narratives.
    *   `spec-to-repo`: Turning specs into repos / validating roadmap flows against code.

2.  **Discovery & Validation:**
    *   `product-discovery`: Structuring user research and feedback into product bets.
    *   `ux-researcher-designer`: Synthesizing user interviews into insights and designs.
    *   `competitive-teardown`: Ranking competitor moves by strategic threat.

3.  **Experiments & Metrics:**
    *   `experiment-designer`: A/B test design with sample size and decision rules.
    *   `product-analytics`: Defining KPIs, funnels, and health metrics.

4.  **Launch & Growth:**
    *   `product-manager-toolkit`: Cross-cutting PM workflows (launch, prioritization).
    *   `landing-page-generator`: Building launch landing pages.
    *   `saas-scaffolder`: Scaffolding SaaS products end to end.
    *   `ui-design-system`: Establishing a design system baseline.

## Workflow
1.  **Analyze Request:** Determine the depth and breadth of the product request.
2.  **Select Sub-Skills:** Choose 2-3 relevant sub-skills to run in parallel.
3.  **Synthesize Output:** Combine the outputs of the sub-skills into a cohesive product recommendation or plan.
