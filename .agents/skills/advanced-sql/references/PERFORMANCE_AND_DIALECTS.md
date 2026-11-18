# SQL performance — diagnose the actual bottleneck

**Source connection:** Book chapter 2 emphasizes indexes, cost-based plans, rewriting, caching/materialized views, anti-patterns and BigQuery/Snowflake differences; chapters 3/5 discuss scale and operations. The procedure below is **Mimir synthesis** informed by engine documentation.

## Baseline and measure

1. Capture *engine, version, data revision, SQL text/parameters*, table statistics, row counts and skew; declare latency, concurrency, cost and freshness objective.
2. Check semantic correctness and authorization before tuning. Capture a trusted expected result at the same snapshot.
3. Inspect **actual** query/profile plan (when safe): estimated vs actual rows, scan/pruning, filters, joins, hash/sort, exchange/shuffle, spills, skew and materialization.
4. Form one falsifiable bottleneck hypothesis, e.g. join multiplies rows, partition filter not pushed down, sort spills, repeated expensive aggregate, stale planner statistics.
5. Apply one targeted change; measure representative before/after and recheck result equivalence and access. Include cold/warm cache and concurrency conditions when they matter.
6. Record tradeoffs: write amplification, storage, refresh lag, compute credits/slots, plan stability, maintenance burden and reversibility.

## Common interventions — conditional, not prescriptions

- **Projection:** retrieve needed columns. For columnar warehouses, `SELECT * LIMIT 10` can still scan excessive data; check platform billing/query behavior.
- **Filtering:** make partition/date predicates usable by pruning. Examine functions/casts around partition keys and correctness of time boundary. Avoid assuming predicate pushdown always occurs.
- **Join reduction:** reduce fanout at correct business grain, preaggregate independent many-side tables, eliminate unnecessary joins and investigate skewed keys. Do not push down a filter that changes outer-join meaning.
- **Windows:** filter to relevant population first where semantically sound; avoid unnecessary wide partitions/sorts; use deterministic order and correct frame before tuning.
- **CTEs:** improve readability; materialization/inlining/reuse differ by dialect/version. Diagnose repeated work rather than claiming CTEs are always slow or fast.
- **Indexes:** in PostgreSQL and similar engines, inspect workload/selectivity for composite, partial, expression or covering indexes; weigh write/maintenance. Sequential scans may be correct for small/high-coverage queries.
- **Partitions/clustering:** match frequent filters and physical mechanism. Table partitioning and clustering introduce cost and operational choices; benchmark before changing.
- **Materialized views/summary tables:** useful for repeated expensive work if refresh policy, staleness, access, correctness and invalidation are explicit. Result caching may already serve the workload.
- **Concurrency/credits:** resource contention can dominate a fast single-query plan. Check queue time, slot/warehouse sizing and limits separately from SQL rewriting.

## Dialect matrix (verify against installed version)

| Capability | PostgreSQL-style row store | BigQuery-style columnar warehouse | Snowflake-style warehouse |
| --- | --- | --- | --- |
| Query analysis | `EXPLAIN`; `EXPLAIN ANALYZE` **executes** statement | Query plan, stage steps, job statistics, bytes processed/slot time | Query Profile, partitions scanned, spills and resource/warehouse state |
| Typical access work | Appropriate index and statistics vs sequential scan | Column projection, partition filters, clustering, shuffle reduction | Micro-partition pruning, clustering **only when warranted**, warehouse/queue considerations |
| Materialization | Views, materialized views, version-dependent CTE behavior | Scheduled/materialized views and engine-specific limitations | Materialized views, result caching and warehouse-specific tradeoffs |
| Query language | SQL functions vary by version | GoogleSQL, vendor extensions such as Pipe SQL | Snowflake SQL and vendor features |

Never copy vendor syntax or planner assumptions across these columns without an explicit dialect check. `QUALIFY`, `IGNORE NULLS`, `MERGE`, approximate aggregates, arrays/JSON, interval syntax, recursive limits and pipeline functions may differ. No unsupported dialect claim should be treated as a book fact.

## Safety of profiling

`EXPLAIN ANALYZE` for PostgreSQL executes the statement; data-modifying statements can have effects. Obtain permission and use a safe environment/rollback plan. Query plans omit some client/network costs. Sensitive SQL literals and sample values may appear in logs/profiles; apply access controls.

## Performance evidence record

```text
Statement/commit; engine/version; dataset and statistics age:
SLO/cost baseline, execution date and representative parameters:
Current plan, scanned bytes/rows, shuffles/spills and observed latency:
Hypothesis → change → comparable plan/measurements:
Correctness regression and security scope check:
Storage/write/refresh/maintenance cost; rollback:
Unknown platform capabilities or inaccessible production metrics:
```

Primary documentation: [PostgreSQL EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html); [PostgreSQL window functions](https://www.postgresql.org/docs/current/functions-window.html); [BigQuery compute best practices](https://cloud.google.com/bigquery/docs/best-practices-performance-compute); [BigQuery query plans](https://cloud.google.com/bigquery/docs/query-plan-explanation); [Snowflake table considerations](https://docs.snowflake.com/en/user-guide/table-considerations).
