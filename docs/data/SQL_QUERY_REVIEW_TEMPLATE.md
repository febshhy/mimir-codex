# SQL query / performance review — optional record

> Use for a material or shared query. A small read-only fix can be one query and one tested expected result. This template is reference-only; Mimir never installs it into an application's `docs/` automatically.

## 1. Consumer and question

- Purpose, business owner and approved definition:
- Result grain (one row represents):
- Inputs / revision / source owner:
- Database engine, version, SQL dialect (known/unknown):
- Freshness, row-level access, sensitivity:

## 2. Relational correctness

| Join / transformation | Input grain | Expected multiplicity | Nulls and duplicates | Check |
| --- | --- | --- | --- | --- |
| | | | | |

- Filters before/after aggregation; output columns and units:
- Event, effective and availability time; timezone/bounds:
- Expected output rows and test fixture (0/1/many, missing match, ties, NULL, late events):
- Independent known-answer total and query:
- Meaning of zero, NULL, unknown and suppressed result:

## 3. Query/design alternatives

- Current SQL/query structure:
- Alternative: CTE, preaggregate, `EXISTS`, window, recursor, semantic contract, different model or no change:
- Why this choice avoids complexity or hidden fanout:
- Changes to grain, compatibility, privacy or access (should be none unless authorized):

## 4. Execution evidence (when performance matters)

- Engine/query plan and sample data size:
- Before: runtime, bytes/scanned partitions, shuffle, cost, concurrency (or **not measured**):
- Hypothesis and one changed access mechanism:
- After: same metrics/conditions (or **not measured**):
- Result equivalence, plan stability and refresh/write costs:

## 5. Release evidence (shared models only)

- Owner/lineage/consumer tests:
- Incremental processing, replay/backfill, monitoring/freshness:
- Version, rollout/rollback, date and responsible reviewer:
- Known | Assumed | Unknown | decision pending:
