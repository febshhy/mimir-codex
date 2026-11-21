---
name: data-lifecycle
description: Trace, design, implement and operate generation-to-serving data systems; use for source contracts, ingestion, pipelines, transformations, storage, orchestration and data architecture.
---

# Data engineering lifecycle — trace data from generation to use

**Call graphs in handoffs:** When work or a finding depends on how code runs,
include or reference the relevant source-derived trace in assignments, returns,
and reviews. Follow **Call Graph Output** in the Mimir coordinator instructions
(`AGENTS.md` in the release or `.mimir/AGENTS.md` in an installed project).

**Authority:** Engineering design across **generation → storage → ingestion → transformation → serving**. The order is a lifecycle inventory, not always the literal order of a pipeline. Use `$software-design-thinking` for applicable contracts, invariants and failure reasoning; reserve advanced state/effect models for genuinely stateful workflows. Use `$data-operations` for runtime, privacy and quality gates. Read [lifecycle concepts](references/REIS_HOUSLEY_METHOD.md) for substantial tasks.

## Source-to-consumer contract

Identify each actual boundary: producer owner → event/record and schema/version → capture mode/offset → transport/landing → durable state/storage → transformations/lineage → served dataset/metric/model/API → consuming action. Show actual inspected functions/jobs/tables; label hypothesized edges. Include the **software/application data team** as upstream/downstream owners: API/event changes and analytical contract changes must be reviewed together.

At each boundary ask: who owns it; what is the grain; event, processing and effective time; whether records can be late, duplicated, updated, deleted or reordered; SLO, freshness and retention; identity/key policy; schema compatibility; authorization, privacy and cost; and the failure/replay route.

## SQL-centric transforms and semantic execution

For SQL-first ingestion/transforms, use `$advanced-sql` to verify query grain, time predicates, dedup/windows, incremental semantics and model/semantic query equality. `$data-lifecycle` remains owner of end-to-end pipeline behavior, freshness and replay. A successful dbt or warehouse run does not establish metric validity.

## Make technology choices from constraints

Compare current stack first. Evaluate volume and burst, bounded vs unbounded flow, source impact, durability, latency, consistency, query pattern, costs (including egress/on-call), security, operating skill, migration/rollback. Choose batch by default if it meets the latency objective; streaming only when its end-to-end benefit pays for state, replay, ordering and operations. Treat CDC and managed ingestion as choices, not guarantees.

## Build a thin vertical slice

```text
Business decision + approved metric
  → producer contract (including source app event/API where affected)
    → small representative captured sample
      → durable, replayable ingestion/checkpoint
        → deterministic transform and grain/quality checks
          → governed consumer (dashboard/model/API)
            → observed answer, lineage and freshness alert
```

A staged technical milestone without a usable checked consumer is not a complete product slice. Parallelize independent owners only when contracts and data handoffs are concrete; `$data-slicing` defines cross-discipline execution.

## Verify recovery, repeat execution and effects where applicable

Use Engineering Foundations for deterministic transforms, contracts and validation. For durable or effectful pipelines, assess initial load, steady state, transient failure, partial commit, redelivery, schema change, replay, backfill, correction, retention deletion and consumer rollback as relevant; use advanced state/effect design only when necessary. Be explicit when only at-least-once delivery is available; make *business outcomes* effectively once by stable IDs and idempotent writes, where required and feasible. Record unknown upstream semantics.

Deliver: lifecycle trace, contract matrix, alternatives, replay/backfill plan, named runbooks/owners and actual checks. Do not require a separate orchestration platform or new technology when the existing process meets the contract.
