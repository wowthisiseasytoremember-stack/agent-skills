---
name: product-strategy-master
description: Master orchestrator for product planning, metrics, and roadmap strategy. Use when the user asks for high-level project planning, market analysis, or roadmap development. This skill coordinates sub-skills for OKRs, sprint planning, and user journey validation.
---

# Product Strategy Master

## Overview
This is the master orchestrator for the Product Strategy squad. It is designed to handle complex, high-level product requests by decomposing them into specific tasks and delegating them to the specialized sub-skills in the `product-strategy/` directory.

## Core Capabilities
When triggered, this skill will analyze the request and decide which of the following sub-skills to activate in parallel:

1.  **Planning & Roadmapping:**
    *   `okr-breakdown-alignment`: Aligning goals with high-level OKRs.
    *   `sprint-story-planner`: Generating Jira-ready tickets from vague ideas.
    *   `timeline-critical-path-planner`: Building roadmaps and identifying bottlenecks.
    *   `feature-launch-plan-generator`: Creating pre/post-launch checklists.

2.  **Analysis & Validation:**
    *   `user-journey-validator`: Ensuring the codebase supports the roadmap flow.
    *   `user-interview-synthesis`: Turning raw feedback into product bets.
    *   `competitor-feature-tracker`: Ranking threats and engineering lift.
    *   `data-privacy-impact-assessment`: Checking for GDPR/PII risks.

3.  **Metrics & Success:**
    *   `metrics-kpi-designer`: Defining leading and lagging indicators.
    *   `ab-test-design-success-criteria`: Designing tests with sample size and duration.
    *   `burn-down-velocity-translator`: Executive-friendly health summaries.

## Workflow
1.  **Analyze Request:** Determine the depth and breadth of the product request.
2.  **Select Sub-Skills:** Choose 2-3 relevant sub-skills to run in parallel.
3.  **Synthesize Output:** Combine the outputs of the sub-skills into a cohesive product recommendation or plan.
