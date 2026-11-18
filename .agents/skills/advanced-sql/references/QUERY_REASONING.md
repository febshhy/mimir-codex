# Effective SQL querying — meaning before cleverness

**Source connection:** Book chapter 2 covers CTEs, recursion, advanced windows and query rewriting; chapter 6 connects SQL to analytical/statistical work. The detailed review rules and examples here are **Mimir synthesis**, not purported quotations from the full book. Parent skill: [Advanced SQL](../SKILL.md).

## Build a query from the result backwards

1. Define output grain and consumer: e.g. `(order_id)` or `(customer_id, month)`. Write expected column semantics and whether zero-count entities must appear.
2. Identify authoritative input grain and keys. For every relation, mark cardinality with respect to the output: 1:1, 1:N, N:1, M:N, optional.
3. Establish temporal logic: event/created/effective time, source availability, timezone, inclusive/exclusive interval and current vs historical interpretation.
4. Filter at the intended semantic stage. Filtering entities **before** aggregation and filtering aggregates **after** aggregation answer different questions.
5. Normalize the intermediate grain **before joining** independent 1:N child tables. `SUM(DISTINCT amount)` is not a reliable fanout repair because equal legitimate amounts can exist.
6. Add SQL features only when they express actual requirements; validate the intermediate result's row counts and uniqueness after each material boundary.

## Relational semantics and failure patterns

| Feature | Appropriate use | Failure / check |
| --- | --- | --- |
| `INNER JOIN` | Required matching entity | Many matches duplicate left facts; compare row counts and key uniqueness. |
| `LEFT JOIN` | Preserve all left entities | A right-table predicate in `WHERE` can discard unmatched rows; put right-side eligibility in `ON` when preserving left entities. |
| `EXISTS` / `NOT EXISTS` | Membership/anti-membership | Prefer to joining when no child attributes are needed; verify correlated predicate and NULL behavior. |
| `UNION ALL` / `UNION` | Concatenate / distinct rows | Deduplication can remove legitimate repeated events; select based on event identity. |
| `GROUP BY` / `HAVING` | Roll up at a stated grain | Distinct entity denominator, empty groups and weighting can change the answer. |
| `COUNT(*)` vs `COUNT(x)` | All rows vs non-null x | `COUNT(x)` ignores NULL; test intentional denominator. |
| `CASE`/`COALESCE` | Explicit missing-value business rule | A missing value may differ from business zero; don't hide unknown data. |
| `DISTINCT` | Intentional set semantics | Avoid as a blanket repair for incorrect joins. |
| `NOT IN` | Membership without NULL hazards | NULL in subquery can make exclusion unknown; `NOT EXISTS` generally offers clearer semantics. |
| `LIMIT` / `FETCH` | Bounded result | Without total `ORDER BY`, row selection need not be reproducible. |

### Independent one-to-many groups: prevent fanout

Order lines and refund events are both many-to-one with orders. Aggregate each to *one row per order* **before** joining their totals. `SUM(DISTINCT x)` is wrong if two valid lines have the same amount. See the [net revenue SQL example](../examples/net_revenue.sql).

### Nulls and denominators

- `NULL = NULL` is unknown; use explicit supported null-safe comparison only when required by the business contract. Distinguish nullable join keys from invalid foreign keys.
- `WHERE x <> 0` discards NULL; choose whether that is correct.
- Ratios use `numerator / NULLIF(denominator, 0)` or equivalent. Whether to present NULL, 0, or “not enough data” is a business/reporting decision.
- Simple averages of group averages are usually not weighted averages. Preserve underlying sum and count where safe to aggregate.
- `COUNT(DISTINCT ...)` can be expensive and may ignore NULL; state distinctness definition and approximation policy.

## CTEs, subqueries and recursion

- Use ordinary CTEs to name **semantic steps**, not to make a query longer. Engine/version controls whether materialization occurs; measure rather than assume.
- Use correlated `EXISTS` for presence, aggregation for summarizing children, and conditional aggregates for mutually exclusive categories. Avoid correlated per-row work that is costly in the actual plan; engines may rewrite it.
- Recursive CTEs need an anchor, terminating condition, traversal identity, treatment of duplicates, and cycle policy. Ensure finite traversal with validated graph constraints or visited-set logic. `UNION` may prevent repeats of an identical projected row; adding depth/path columns can defeat that property.
- Graph-shaped SQL supports hierarchy use cases, but a general knowledge graph/ontology may need separate semantics and query support. Do not force recursion when a simple join or precomputed closure suffices.

## Window functions: separate row grouping from frame membership

- `PARTITION BY` defines independent groups; `ORDER BY` defines sequence; the **frame** determines which ordered rows contribute to frame-sensitive calculations.
- `ROW_NUMBER()` selects a latest/versioned row only with a deterministic tie-break sequence (e.g. `event_at DESC, received_at DESC, event_id DESC`).
- `RANK`/`DENSE_RANK` preserve ties, `ROW_NUMBER` does not. Choose according to the requested top-N semantics.
- `LAG`/`LEAD` compare adjacent rows. Confirm gap handling, time bucketing and stable ordering before treating adjacency as a time interval.
- `ROWS BETWEEN ...` counts rows; `RANGE` uses ordering-value distance or peer groups depending on dialect; `GROUPS` uses peer groups where supported. Inspect default frame, especially with `LAST_VALUE`.
- Running totals, rolling windows and whole-partition metrics are different. Always make the frame explicit when an unexpected default could alter results.

## Query answer verification

- Create a 5–15 row fixture with one missing match, a duplicated key, ties, NULL values and a boundary timestamp; calculate the expected result by hand.
- Cross-check with a different formulation (independent aggregation or manual reconciliation), not only the same CTE refactored.
- For incremental/historical logic, compare a full recomputation with the incremental output on a bounded input.
- Assert uniqueness at final grain, no unexpected row loss/fanout, measures within domain bounds, and stable results for the chosen snapshot.

References: [PostgreSQL window frames](https://www.postgresql.org/docs/current/functions-window.html); [SQL example](../examples/latest_order_event.sql).
