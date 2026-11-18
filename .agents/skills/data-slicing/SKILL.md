---
name: data-slicing
description: Plan vertical, end-to-end product changes that cross application/software, data engineering, analytics, experimentation, ML and communication with explicit interface ownership and verifiable handoffs.
---

# Full-stack data slicing — one decision, one end-to-end checked thread

**Authority:** Defines *delivery slices and handoffs*; it does not redefine product requirements, domain invariants, data metrics, statistical inference or worker graph semantics. Use `$software-design-thinking` for shared engineering principles and conditional application state/effects; `$graph-protocol` continues to own delegated A/E/R. Read [cross-team slicing method](references/CROSS_TEAM_SLICES.md). A [schema-3 work plan example](PLAN_DATA_EXAMPLE.json) shows delegation without confusing it with data lineage.

## Choose one user-visible decision or action

Examples: trusted paid-order revenue by day, a risk-scored intervention with human review, a pipeline freshness warning visible on a dashboard. Identify consumer, owner, change impact, latency, correctness and which **single** business question this slice answers. Start with the smallest real source flow; avoid horizontal plans that deliver a warehouse before any trustworthy use.

## Slice contract (show only necessary owners)

```text
Outcome and decision owner:
Application producer / event/version / transaction semantics:
Dataset and grain / source and transformation owner:
Metric/estimand / query and semantic owner:
Statistical/model claim and permitted action (if any):
Presentation or API consumer and operating owner:
Dependency edges, handoff acceptance and review:
Failure/replay/correction, rollback and privacy:
End-to-end acceptance fixture + observable result:
```

**Data slicing differs from task-delegation graph.** A vertical slice is a *business deliverable across domains*. The factory DAG is a *schedule of task nodes*. Decompose vertical slices into A/E/R work nodes only when dependencies justify delegation. Do not divide solely by job title; assign boundaries at independently testable contracts.

## What crosses teams

- Product/app engineering owns transaction semantics and event/API emission. It publishes versions and change notices, including deletes/corrections and deploy/rollback compatibility.
- Data engineering owns capture, durability, lineage, reprocessing, storage and transformation execution; it does not invent business metric meaning.
- Analytics engineering/analyst partners own fact grain, conformed dimensions/semantic definitions and decision-readable checks with business owners.
- Data science owns target, feature/label cutoff, validation, expected value and model-impact evaluation when applicable; it does not convert offline accuracy into an approved policy.
- Business/UI/content partners own purpose, exposure, communication and action flow; interface claims must match validated data.
- The same person may own several boundaries; **ownership is a contract, not headcount allocation**.

## Stop conditions

Block only affected changes when producer version, denominator, identity, permissions or impact policy is unknown. Contract compatibility, idempotent replay, point-in-time behavior and reconciliation must be tested at the joint boundary. Do not allow a green unit-test suite in each team to substitute for the end-to-end consumer check.
