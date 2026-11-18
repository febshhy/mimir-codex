# SQL-driven data products — contracts and operations

**Source connection:** Book chapters 3 and 5 cover modular SQL pipelines, data contracts, batch/stream/ETL/ELT choices, lakehouse/Iceberg, medallion modeling with dbt, orchestration, consume/semantic layers, governance and operational anti-patterns. The concrete policies below are **Mimir synthesis**. Use `$data-lifecycle`, `$data-operations` and `$data-slicing` for cross-system work.

## Define one source-to-consumer slice

```text
Source event/API/CDC or batch file (identity, version, owner)
  -> ingestion (offset/checkpoint, duplicate/late handling, durable landing)
  -> raw/bronze (source-preserving history and restricted access)
  -> clean/silver (typed, deduplicated, reconciled, corrections)
  -> modeled/gold (declared process grain, dimensions, validated measures)
  -> semantic/consume contract (metric SQL, dimensions, permissions, version)
  -> BI/ML/API consumer (freshness and decision requirements)
```

This is one possible layered shape, not a required number of stages or technologies. Only create layers with a real different contract or operational responsibility.

## Architectural choices

| Approach | Use if | Review |
| --- | --- | --- |
| Batch | Freshness permits scheduled work | Restart/replay, time windows, deletes and as-of results |
| Streaming | End-to-end latency actually requires it | Ordering, watermark, late data, state, exactly/effectively-once semantics, cost |
| ETL | Needed transformations/validations before target write | Failure isolation, tested staging, recovery and source effect |
| ELT | Target SQL engine is appropriate for transformations | Data access, storage duplication, compute and model test cost |
| Managed sharing / zero-ETL | Source and destination offer verified change propagation | CDC semantics, schema evolution, trust boundary, latency and platform dependence |
| Data product / mesh ownership | Multiple domains can sustain actual contracts | Named producer, consumer, SLO, product interface; avoid job-title silos |
| Lakehouse tables (e.g. Iceberg) | Open table semantics and historical/stream/batch access justify operations | Snapshot/version isolation, compaction, table maintenance, delete/retention policies |

Prefer the current stack unless a measured or approved requirement rules it out. Avoid monolithic scripts, unnecessary interfaces, undocumented dependencies and manual-only “recovery”.

## Data and semantic contract

Each shared output needs: owner and business consumer; schema and compatibility policy; one-row grain and keys; event/effective/ingest time; freshness window; missing/duplicate/correction behavior; metric definition and supported dimensions; null policy; sensitivity and row/column permissions; lineage; test coverage; retention/deletion; deprecation/version migration. A semantically correct metric still requires **execution equivalence** across tools and access contexts.

Typical materializations:
- staging: source-like, typed and versioned, preserve provenance;
- intermediate: meaningful bounded joins/dedup with explicit cardinalities;
- dimensional/serving: grain-stable facts/dimensions and semantic definitions;
- consumer: documented read contract, freshness and permissions.

## Incremental and historical behavior

- Choose unique row identity and high-water mark/offset. Event time and arrival time differ; late records need a lookback or correction protocol.
- Declare upsert/append/delete behavior, isolation of target writes and what happens after a commit-but-timeout.
- Test the same input applied twice and a partial run followed by replay. Confirm downstream totals and historical snapshots agree with a bounded full rebuild.
- Backfill should be bounded, auditable, access-controlled and recoverable; include cost, snapshots and consumer coordination.
- Expose last good partition/version, freshness, rejected records, row-volume change, duplicate/reconciliation alerts and model failure signal relevant to users.

## Security and change management

- Data minimization and least privilege at source, storage, transformation, BI/feature/LLM interfaces. SQL syntax checks do not substitute for authorization.
- Version or stage incompatible producer and semantic changes; use consumer contract tests and a rollout/rollback sequence.
- Separate SQL transformation configuration from secrets; do not log PII as part of example fixtures or profiling.
- Test lineage and governance claims against actual system capabilities; a diagram or dbt documentation alone does not enforce access.

## Verification gate

At minimum for a material change: (1) one known-answer event from producer through consumer, (2) a missing/duplicate/late or correction case, (3) conformed grain/metric and consumer permissions, (4) observable failure and replay/rollback plan, and (5) evidence recorded at actual environment/revision. For small read-only work use only applicable checks.
