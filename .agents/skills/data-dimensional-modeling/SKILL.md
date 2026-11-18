---
name: data-dimensional-modeling
description: Design or review business-facing analytical models, facts, dimensions, historical changes, conformed definitions, marts, and semantic-layer compatibility.
---

# Dimensional modeling — business process → grain → conformed analytical contract

**Authority:** Analytic table design and conformance. `$requirements` owns business meaning and acceptance; `$database-design` owns physical storage choices; `$software-design-thinking` retains domain invariants and effects; `$data-statistics` owns statistical inference. Read [the method](references/KIMBALL_METHOD.md) when modeling is material.

## Four design decisions, in order

1. **Business process:** identify a measurable event or process, actual users and decisions. Inventory adjacent processes in a bus matrix; do not design isolated dashboards first.
2. **Grain:** finish: *One row represents exactly …* Specify entity, event/state, time, version and multiplicity. Grain is an invariant and becomes the basis of acceptance tests. Never mix incompatible grains in one fact.
3. **Dimensions:** identify who/what/where/when/how attributes; conformed dimensions shared across processes, role-playing dates, degenerate identifiers, and unknown members. Decide business/natural, surrogate, and durable identity explicitly.
4. **Facts:** classify additive, semi-additive and non-additive measures; transaction, periodic snapshot, accumulating snapshot or factless event. Define numerator/denominator and allowed aggregation levels for every metric.

## Operational decisions

- Determine SCD policy **per attribute**: preserve original (0), overwrite (1), historical row (2), prior value (3), mini-dimension (4), history table (5), hybrid (6), or dual Type 1/2 keys (7) only when justified. Type 2 needs stable business identity, surrogate row version, non-overlapping validity intervals and late-change handling.
- Specify event time vs ingestion/load time, timezone, effective time, late records, retroactive changes, tombstones, duplicates, corrections and backfill policy. A historical dashboard needs explicit *as-was* versus *as-is* semantics.
- Use conformed dimensions **and conformed facts** across marts. Semantic metrics must share definitions/filters, not merely column names. Identify bridge tables and allocation rules when dimensions are multivalued or hierarchical; expose fanout risk.
- Keep OLTP truth and analytics serving distinct. Star schemas are a strong default for stable BI consumption, **not** a mandate for every staging/stream/feature/operational dataset. Compare physical choices to measured workload and existing stack.
- Separate source staging, integrated modeling and consumption layers when useful. A layer without a distinct contract or consumer is overhead.

## Required output when significant

```text
Process / consumer / decision:
Bus-matrix row / shared dimensions:
Grain statement (one row = ...):
Fact type / measures / additivity / metric semantics:
Dimensions / keys / SCD by attribute / history semantics:
Source lineage / event and system time / late and correction policy:
Data tests / migration / reconciliation / backfill / rollback:
Cost, query pattern and alternatives:
Known | Assumed | Unknown | Decision pending:
```

## SQL implementation handoff

Use `$advanced-sql` when implementing or reviewing joins, as-of dimensions, window logic, consumer query shape or plan performance. This skill owns business grain and additive meaning; SQL execution must preserve those contracts. Compare independent many-side aggregates before joining, test late Type 2 boundaries and measure actual query cost if optimizing.

## Verification

- Unit-test key mapping and validity intervals. Assert uniqueness **at the declared grain**, required foreign-key resolution, and no unintended fanout.
- Reconcile totals/counts and selected entities with sources and previous approved results. Probe empty windows, double delivery, corrected events, late arriving facts/dimensions, Type 2 boundary timestamps and restatements.
- Validate metric semantics at several levels and compare against trusted business examples. Test backfill/re-run equivalence and retention permissions. Do not assert correctness merely because SQL executes.

**References:** [Kimball and Ross concept extraction](references/KIMBALL_METHOD.md); `$data-lifecycle`; `$data-slicing` for product-wide slices.
