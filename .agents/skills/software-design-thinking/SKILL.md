---
name: software-design-thinking
description: >-
  Engineering foundations for data analysis, analytics engineering, data pipelines,
  data science, machine learning, and application/software changes. Use for
  non-trivial correctness, contracts, structure, dependencies, failure handling,
  or architecture decisions. Scale depth to risk; load advanced application design
  only for stateful or effectful workflows. Not needed for trivial edits.
---

# Engineering Foundations — software discipline for full-stack data

**Call graphs in handoffs:** When work or a finding depends on how code runs,
include or reference the relevant source-derived trace in assignments, returns,
and reviews. Follow **Call Graph Output** in the Mimir coordinator instructions
(`AGENTS.md` in the release or `.mimir/AGENTS.md` in an installed project).

**Aim:** make the smallest useful outcome correct, understandable, testable, and operable.
Use approved requirements as authority; distinguish **Known | Unknown | Assumption | Decision**.
Do not infer business rules, metric definitions, permission, or model intervention policy.
A design artifact should be no larger than its risk and handoffs require.

## Choose depth by consequence, not job title

- **Level 1 — analytical:** read-only SQL, notebooks, reports, exploratory analysis, offline experiments. Define meaning, grain, assumptions, reproducibility, validation and evidence. No mandatory state machine, dependency interface or retry architecture.
- **Level 2 — production data:** scheduled ingestion, transformation, shared datasets, incremental models, features, backfills. Add owners, persisted checkpoints, compatibility, observability, replay, recovery and operational limits as applicable.
- **Level 3 — stateful/effectful application or ML service:** producer transactions, APIs, online inference, shared writers, consequential automated actions. Apply [advanced application design](references/ADVANCED-APPLICATION-DESIGN.md); add [concurrency](references/CONCURRENCY.md) or [effects and recovery](references/EFFECTS-AND-RECOVERY.md) only when their conditions exist.

A high-impact analytic metric may need stricter verification than a low-risk application endpoint. Use the **smallest sufficient model**; escalate depth when impact, change scope or poor fault detectability requires it.

## 1. Define the problem and acceptance

State consumer/decision, approved expected outcome, inputs, outputs, constraints and who owns approval. Record unknown source behavior explicitly. For a data question, distinguish a request for a number from the decision that number supports. Name the acceptance example or observation that will establish success.

## 2. Define the data contracts

Specify only meaningful shapes and boundaries: **schema, grain, keys/identity, units, time semantics** (event, processing and effective time), nullability, source/version and owner. Record compatibility obligations for persisted or shared data. For ML, include feature/label observation time and serving contracts when relevant. A schema that parses can still contain wrong business facts.

## 3. State correctness rules

Write checkable business and technical invariants: uniqueness at the claimed grain, valid ranges, joins without unintended fanout, reconciled totals, temporal cutoffs, permissions, or transition legality where applicable. Distinguish a requirement from an implementation choice. Duplicate checks across an independent producer and consumer boundary may be intentional defense in depth; remove only redundant checks without a distinct purpose.

## 4. Trace the real workflow

Trace **source → capture → transform → model/analysis → consumer/action**; name changed code, queries, jobs, datasets and owners when inspected. Mark unobserved edges *proposed* or *unknown*. Keep this lineage graph separate from application state transitions and `$graph-protocol` worker/task dependencies. Use a vertical business slice, not a horizontal platform build, when data teams and software teams must coordinate.

## 5. Keep computation understandable and testable

Prefer explicit, deterministic transformations for the same inputs and documented versions, where feasible. Separate external reads/writes, clocks and randomness when they make meaningful logic hard to test. Do **not** require a `decide()` function, interfaces, dependency injection, abstract type hierarchies or multiple layers for simple SQL, scripts or notebooks. Fix sources of nondeterminism that matter to reproducibility (snapshots, random seeds, versions).

## 6. Handle failures in proportion to impact

For relevant boundaries, consider malformed, missing, late, duplicate, reordered, corrected and deleted data; partial writes; retries; interruption; and upstream contract changes. Name the response: detect, reject, retry, quarantine, reconcile, compensate or recover. For read-only work, document limitations rather than invent runtime machinery. For repeatable writes, specify identity, idempotency, checkpoint and replay behavior; bound retries and define the responsible owner. Do not claim exactly-once outcomes without evidence.

## 7. Verify every important claim

Match evidence to the claim: known-answer fixture, unit/property check, schema/contract check, reconciliation, temporal leakage test, statistical uncertainty, holdout/baseline, boundary integration test, operational alert or user-visible acceptance. Run the checks that exist and record actual results. Different owners can independently validate the same invariant. A green pipeline, a fitting model or syntactically valid SQL does not establish correct meaning or real-world benefit.

## 8. Deliver and change incrementally

Build the smallest useful **end-to-end vertical slice** and confirm its consumer outcome. Make ownership, dependencies and handoff acceptance explicit. Prefer existing stack, reversible changes and compatible rollouts. For consequential changes, plan monitoring, migration, recovery and rollback; record hard-to-reverse decisions using `$adr` when justified. Revisit affected contracts and checks when evidence changes; do not automatically redo unrelated sections.

## Routing and outputs

- **Analyst / analytics engineer:** `$data-dimensional-modeling` for grain and metrics, `$data-statistics` for inference, `$data-storytelling` for the result; use `$database-design` only for physical modeling or workload issues.
- **Data engineer:** `$data-lifecycle` and `$data-operations` for source/consumer boundaries, ingestion, quality, freshness, replay, recovery and ownership.
- **Data scientist / ML:** `$data-decision-science` and `$data-statistics` for targets, time cutoff, leakage, baselines, evaluation, uncertainty and decision value; `$data-operations` for operational pipelines or serving.
- **Cross-team:** `$data-slicing` for producer-to-decision contracts, `$graph-protocol` **only when task delegation is useful**, `$requirements` for approved behavior and `$testing` for evidence.
- **Stateful application:** use [advanced application design](references/ADVANCED-APPLICATION-DESIGN.md) and [Mimir integration](references/MIMIR-INTEGRATION.md) for structural decisions. Advanced techniques are options with triggers, not mandatory analytical steps.

**Minimum useful output:** outcome and contract; actual or proposed flow; applicable invariants and failure assumptions; owner/hand-offs when relevant; acceptance evidence and unresolved unknowns. Expand only if the risk or task needs it.
