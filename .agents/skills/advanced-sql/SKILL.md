---
name: advanced-sql
description: Design, review, debug, test and optimize SQL queries, analytical schemas, semantic models, SQL pipelines, SQL-based statistics, ML feature queries and governed SQL/AI workloads. Use for joins, CTEs, window or recursive queries, query plans and dialect selection. Complement data-dimensional-modeling for business grain and database-design for physical indexing/engines. Do not require a warehouse migration or use every advanced feature.
---

# Advanced SQL — semantic correctness → measured query efficiency

**Authority:** The SQL representation and execution of an approved question, data contract or transformation. `$requirements` owns business rules; `$data-dimensional-modeling` owns analytic fact/metric meanings; `$database-design` owns engine and persistent physical-design choices; `$data-statistics` owns statistical inference; `$data-decision-science` owns ML decision validity; `$data-lifecycle`/`$data-operations` own running pipelines. Do not silently redefine these contracts to speed up a query.

**Method:** Start with the actual engine/version, target question and relevant tables. Use **only relevant** references: [query semantics](references/QUERY_REASONING.md), [model selection](references/MODELING_CHOICES.md), [execution plans and dialects](references/PERFORMANCE_AND_DIALECTS.md), [SQL pipelines and semantic layers](references/SQL_PIPELINES.md), [SQL in science, AI and emerging syntax](references/SQL_SCIENCE_AND_EMERGING.md). See [book-derived concept map](references/MACHADO_RUSSA_ESMERIZ_CHAPTER_MAP.md).

## The eight-step SQL review (scale to the task)

1. **Question and consumer:** state output and why it matters; distinguish a descriptive query, operational transformation, prediction dataset and write.
2. **Inputs and grain:** identify source authority, row meaning, unique keys, cardinalities, source version, null/duplicate policy, and event/effective/ingest time. Record what is unknown.
3. **Model fit:** choose existing normalized, star, snowflake, wide, lakehouse or semantic/graph representation by actual read/write patterns and change needs. Do not remodel when a query suffices.
4. **Relational correctness:** map each join's multiplicity, filtering stage, grouping level, aggregation and null semantics. Guard against silent row multiplication and denominator changes.
5. **Express clearly:** prefer the simplest readable set-based query. Use CTEs to structure reasoning, windows for row-relative calculations, recursion for bounded traversals, and subqueries/`EXISTS` for membership. CTEs do not automatically materialize or speed up queries.
6. **Validate results:** compare with small known-answer fixtures or an independent query; exercise 0/1/many matches, NULLs, ties, duplicate or late events and time boundaries. Check both row grain and aggregate reconciliation.
7. **Measure before tuning:** inspect real plan and runtime/cost/bytes at representative parameters and volume. Change one mechanism at a time; recheck output equivalence and concurrent/load behavior. Mark unmeasured claims unknown.
8. **Operationalize conditionally:** for shared SQL models add ownership, lineage, permissions, freshness, incremental/backfill semantics, tests, monitoring and compatible releases. For one-off analysis, keep a reproducible query and assumptions; no mandatory orchestration.

## Critical guards

- A correct SQL syntax or schema is not proof of correct business meaning. Know *one row represents what*, especially before `JOIN`, `COUNT`, `DISTINCT`, `AVG`, ratios and windows.
- `LEFT JOIN` can become an effective inner join when right-side filters are placed in `WHERE`; an `INNER JOIN` can multiply facts. Test both risks.
- `ROW_NUMBER()` and top-N need a **deterministic total order** to resolve ties. Window `ORDER BY` and window frame (`ROWS`/`RANGE`/`GROUPS`) are distinct; do not assume a cumulative frame expresses a whole partition.
- SQL uses three-valued logic: `NULL` is not an ordinary value. Be careful with `NOT IN` when the subquery contains NULL; prefer `NOT EXISTS` for anti-membership when appropriate. `COUNT(*)` differs from `COUNT(col)`.
- Casts, overflow, decimal precision, timestamps/timezones, implicit coercion, division by zero, collation, isolation and dialect behavior need explicit treatment when relevant.
- Avoid treating `SELECT *`, indexes, partitioning, caching, materialized views, OBT and streaming as universal optimizations. Protect correctness, authorization and maintainability first.
- A model feature must be **available at decision cutoff**; event time alone does not establish availability. A successful SQL training query is not evidence of model validity or causal impact.
- SQL-triggered generative AI may disclose governed content to an external service. Require permission, cost ceiling, grounding, output evaluation, and vendor/version-specific confirmation before enabling it.

## Focused output contract

```text
Consumer / question / intended output:
SQL engine + version + dialect constraints (known/unknown):
Input sources / owners / row grain / cardinality / time semantics:
Query/model choice, alternative and reason:
SQL + expected result shape and key invariants:
Small known-answer test + adversarial edge cases:
Observed plan, runtime and cost | Not measured:
Permissions / lineage / freshness / replay / rollback if operational:
Known | Assumed | Unknown | decision pending:
```

**Scope and provenance:** This method synthesizes *Advanced SQL: Implementing Modern Data Solutions and ML Applications* by Rui Machado, Hélder Russa and Pedro Esmeriz (O'Reilly, 2026), using the public publisher table of contents and chapter previews, then adds explicitly identified Mimir engineering checks. The book's full text is **not** included in this repository. These are original, practical instructions, not verbatim book examples and not a claim of exhaustive full-text coverage.
