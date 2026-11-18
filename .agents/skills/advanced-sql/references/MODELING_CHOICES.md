# Data modeling in SQL — choose by semantics, workload and change

**Source connection:** Book chapter 4 covers 3NF, stars, snowflakes, one-big-table designs, lakehouse/ELT and semantic or knowledge graph models. Chapter 3 adds data contracts/products and chapter 5 adds medallion/consume layers. This selection framework is **Mimir synthesis**; use `$data-dimensional-modeling` for detailed Kimball practice and `$database-design` for persistence/engine decisions.

## First make the conceptual contract explicit

- **Identity:** what entity or event exists, which source owns it, natural/business/surrogate identifier, and how IDs merge or split.
- **Grain:** one row represents one what (event, line, snapshot, state version, feature at cutoff). Name key and allowed multiplicity.
- **Relationships:** functional dependencies, cardinality, optionality, referential actions, bridges and M:N rules.
- **Time:** event time, ingestion/availability time, effective/validity period, observation cutoff, mutation/late-arrival semantics, and timezone.
- **Measures:** units, currency conversion, additive/semi/non-additive, numerator/denominator, distinct entity and missingness semantics.
- **Change/security:** schema version, producer/consumer compatibility, deletion/retention, PII/row-level access and authorization owner.

## Compare forms without treating them as interchangeable

| Model | Useful when | Main risks/tradeoffs | Verification |
| --- | --- | --- | --- |
| **3NF / normalized relations** | Transactional updates, data integrity, bounded authoritative facts | Query complexity/joins for wide analytics; history is not automatic | Functional dependencies, update anomalies, key/FK constraints, transaction boundaries |
| **Star (fact + conformed dimensions)** | Reusable BI measures, drilldown, stable reporting dimensions | Mixed grain, SCD join fanout, unknown dimension members | Grain, unique dimensional keys, Type 2 as-of join, additive classification, reconciliation |
| **Snowflake dimensional** | Reused/hierarchical normalized dimension attributes justify extra structure | More joins and semantically complex paths | Bridge cardinality, hierarchy paths, query plan, consumer understanding |
| **One big table (OBT)** | Well-defined, stable, read-heavy consumer requiring few joins | Redundancy, update anomalies, exploding width, hidden grain changes and governance duplicates | Declared row grain, row/column evolution, source reconciliation and maintenance cost |
| **Lakehouse / medallion** | Multiple input formats, governed historical data and incremental ELT | Adds storage/table-format/compaction/orchestration operations | Source-to-curated identity, late/replay tests, versioning, compute/cost/profile evidence |
| **Semantic metric layer** | One definition across BI/API/ML consumers | Divergence between declared metric and executable SQL/permissions | Definition-to-SQL trace, conformed filters, time windows, row-level access and cross-tool comparison |
| **Knowledge graph / ontology** | First-class entities/relationships, multi-hop/semantic reasoning | Different identity, inference, query language and operations; RDF and property graphs are not identical | Type/edge semantics, traversal correctness, provenance, access and measured query performance |

A normalized operational source may feed a dimensional mart and a narrow consumer-friendly wide table. These are layers with different responsibilities. Do not choose a physical design from one “best” model ranking.

## Dimensional modeling details needed for SQL correctness

- Choose business process → fact grain → dimensions → facts, then define source mapping and update policy. A transaction fact and daily inventory snapshot cannot share a blind `SUM` policy across time.
- For Type 2 dimensions, join fact *event/effective time* to a non-overlapping dimension validity interval with an intentional boundary convention (typically `valid_from <= t AND t < valid_to`). A current-only join silently restates history.
- Conformed dimensions allow shared grouping; conformed facts require the **same measurement policy** as well. Cross-process comparisons may need separate aggregates at the same reporting grain before a join.
- Degenerate dimensions, bridge tables, junk dimensions, factless events and accumulating snapshots can be useful; only introduce when they preserve the consumer's actual event/history semantics.
- Add common aggregations at a defined lower/common grain before joining. Test one-to-many bridge allocations and summed proportions.
- Record late dimensions, restatements, deleted source events and as-known vs as-was history; dashboard metric revisions require compatible consumer rollout.

## Semantic modeling and graph considerations

- Distinguish SQL table schema (shape), domain semantics (what attributes and measures mean), and semantic execution (the exact authorized SQL generated for a metric).
- Treat a semantic metric as a tested contract: entity, grain, calculation, filters, time dimension, dimensions permitted, units, version and authorization policy.
- A graph relation is not automatically a relational foreign key. Property-graph queries, RDF/OWL ontology reasoning and SQL recursive traversal solve different problems; define required traversal, inference and guarantees before choosing one.
- Preserve existing relational tools where multi-hop/semantic inference does not justify a new graph platform.

## Model decision output

```text
Business process / consumer:
Existing model and why it succeeds/fails:
Proposed row grain / keys / temporal semantics / ownership:
Read and write patterns, scale and evolution constraints:
3NF vs star vs snowflake vs OBT vs lakehouse vs semantic/graph alternatives:
Chosen contract and explicit reconciliation strategy:
Data tests / versioning / backfill / reversal:
Observed plan/cost or Not measured; Known/Assumed/Unknown:
```

Use [model choice template](../../../../docs/data/SQL_MODEL_CHOICE_TEMPLATE.md) only when a material schema/model choice is being recorded.
