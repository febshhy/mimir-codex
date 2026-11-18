# Rui Machado, Hélder Russa, Pedro Esmeriz — *Advanced SQL* (2026): concept map

**Source and evidence boundary.** O'Reilly lists *Advanced SQL: Implementing Modern Data Solutions and ML Applications*, by Rui Machado, Hélder Russa and Pedro Esmeriz, July 2026, ISBN 9798341627475 (digital edition). This file maps **all eight publisher-listed chapters** and their relevant published section headings, cross-checked against available O'Reilly chapter previews. The complete text was **not supplied or accessible**. Therefore the book's actual detailed advice, derivations, code, benchmarks and examples beyond preview are unknown. Do **not** call this a full-text extraction, claim the authors endorse Mimir's rules, or infer chapter content more narrowly than the published preview supports.

**Legend:** *Book topic* = verified publisher heading/preview, condensed and paraphrased. *Mimir application* = independent design/verification guidance derived from that topic and broader engineering knowledge. Links point to the corresponding O'Reilly pages.

## Ch. 1 — Evolution of SQL (modern SQL breadth)

[Publisher chapter preview](https://www.oreilly.com/library/view/advanced-sql/9798341627475/ch01.html)

- **Book topics:** historical SQL standards (SQL-86/89/92, 1999, 2003–08, 2011–16, 2023 graph developments), multipurpose SQL, semi-structured and unstructured data, temporal handling, analytic/OLAP windows, graph navigation, SQL/ML/LLM integrations, embedded DuckDB analytics and dialect evolution.
- **Mimir application:** record engine/version/dialect; choose SQL for relational/temporal/analytic work where supported. Treat vendor functions as opt-in; verify actual dialect and types, rather than inferring cross-platform portability or standards compliance from a chapter title.
- **Tests:** date/time and timezone result, JSON missing key, null semantics and version-specific syntax; confirm proprietary features before use.

## Ch. 2 — Advanced SQL Techniques (querying and performance)

[Publisher chapter preview](https://www.oreilly.com/library/view/advanced-sql/9798341627475/ch02.html)

- **Book topics:** CTE factoring, recursive CTEs for hierarchies/iteration, advanced window queries; indexes/access, cost-based plans, rewrites, caches/materialized views, query anti-patterns, and BigQuery versus Snowflake tuning. Preview explicitly mentions PostgreSQL and cloud-warehouse comparisons.
- **Mimir application:** name logical steps with CTEs, state termination/cycle policy for recursion, make window partition/order/frame explicit, inspect row multiplicity before aggregation, use real plans and measured workloads when optimizing.
- **Tests:** duplicate and null join keys, recursive termination, tied rank, exact rolling frame, before/after output equivalence and cost, materialization/staleness policy.
- **See:** [query reasoning](QUERY_REASONING.md), [performance and dialects](PERFORMANCE_AND_DIALECTS.md).

## Ch. 3 — Architecting SQL-Driven Solutions (systems and governance)

[Publisher chapter preview](https://www.oreilly.com/library/view/advanced-sql/9798341627475/ch03.html)

- **Book topics:** modular SQL pipelines, data contracts, batch vs streaming, ETL/ELT, zero-ETL/sharing, data mesh/products, traditional/cloud scaling, concurrency/isolation, hybrid/multi-cloud, separation of storage/transformation/orchestration, testing, monitoring/lineage, security/governance and avoidable architecture coupling.
- **Mimir application:** design a producer-to-consumer slice with explicit owner/contract, prefer batch when its freshness meets needs, separate semantic and physical guarantees, add tests and release/rollback methods without mandating a new platform.
- **Tests:** schema evolution, pipeline retry/replay, failure and recovery, privacy/access check, cost comparison, correctness across independent components.
- **See:** [SQL pipelines](SQL_PIPELINES.md) and `$data-slicing`.

## Ch. 4 — Advanced Data Modeling with SQL (model alternatives)

[Publisher chapter preview](https://www.oreilly.com/library/view/advanced-sql/9798341627475/ch04.html)

- **Book topics:** 3NF; dimensional star and snowflake; one-big-table denormalization; lakehouse and ELT; knowledge graph/semantic modeling; Neo4j/Cypher, RDF/OWL, SQL/property graphs and their complementary roles. Preview uses an HR employee/department setting and discusses tradeoffs.
- **Mimir application:** compare row identity/grain, read/write patterns, history and ownership; 3NF for update-safe sources, star for stable analytics, OBT for justified read-optimized views, graph/ontology only for real relationship/inference requirements.
- **Tests:** update anomalies, referential/cardinality invariants, mixed-grain fanout, SCD effective-time join, aggregation and semantic consistency; benchmark actual query patterns.
- **See:** [modeling choices](MODELING_CHOICES.md), `$data-dimensional-modeling` and `$database-design`.

## Ch. 5 — Building Data Engineering Solutions with SQL (working platform)

[Publisher chapter preview](https://www.oreilly.com/library/view/advanced-sql/9798341627475/ch05.html)

- **Book topics:** GCP-based environment, SQL-centric ingestion, Spark Structured Streaming and Flink SQL, batch ingestion, lakehouse storage/Apache Iceberg, SQL/dbt silver and gold medallion transformations, Cloud Workflows/orchestration, stable consume layer, SQL-first semantic execution, testable semantic contracts, governance and dbt documentation/lineage/exposures.
- **Mimir application:** separate source-preserving landing, validated model and governed consumption where boundaries justify them; define one executable metric contract; test both data correctness and authorization.
- **Tests:** replay/partial load, source reconciliation, metric equality across tools, lineage/version ownership, freshness and least privilege.
- **See:** [SQL pipelines](SQL_PIPELINES.md), `$data-lifecycle`.

## Ch. 6 — SQL in Data Science (beyond extraction)

[Publisher chapter preview](https://www.oreilly.com/library/view/advanced-sql/9798341627475/ch06.html)

- **Book topics:** statistical descriptions, correlation/association, regression from aggregates, outliers, normality tests, intervals for the mean, two-sample and multi-group comparisons; SQL feature engineering, model creation/training, evaluation, deployment and monitoring. Preview explicitly positions SQL as a possible analytical/ML environment rather than only an extractor.
- **Mimir application:** verify population and sampling/weighting assumptions; form point-in-time correct features and labels; validate model quality and business utility independently of SQL syntax. Choose in-warehouse ML vs other tools by task/operations evidence.
- **Tests:** nulls and denominator, split/leakage, time availability, statistically appropriate uncertainty, baseline, deployment/feature parity/drift.
- **See:** [SQL for science/AI](SQL_SCIENCE_AND_EMERGING.md), `$data-statistics`, `$data-decision-science`.

## Ch. 7 — Generative AI in SQL (governed AI workloads)

[Publisher chapter preview](https://www.oreilly.com/library/view/advanced-sql/9798341627475/ch07.html)

- **Book topics:** LLM functions, embeddings and search; RAG grounding, SQL-based agents and MCP, production evaluation/monitoring, costs/performance, deployment patterns, safety/privacy and production readiness.
- **Mimir application:** consider LLM-in-SQL only for real generative requirements; require governed retrieval, least privilege, explicit external processor boundary, evaluation, provenance and cost/latency control.
- **Tests:** unauthorized retrieval, stale or wrong evidence, prompt injection, hallucination, errors/timeouts and budget; keep side effects outside unconstrained generated SQL.
- **See:** [SQL for science/AI](SQL_SCIENCE_AND_EMERGING.md).

## Ch. 8 — Innovations in SQL Syntax and the Future of SQL (portable evaluation)

[Publisher chapter preview](https://www.oreilly.com/library/view/advanced-sql/9798341627475/ch08.html)

- **Book topics:** GoogleSQL Pipe Syntax and operators, real-world use and style, PRQL, Malloy, AI/autonomous databases, future declarative governance and speculative quantum-assisted optimization.
- **Mimir application:** evaluate new syntax against current compiler/dialect support, readability, generated plan, portability, team debugging cost and reversibility. Treat future-looking topics as research, not a reason to migrate.
- **Tests:** equivalent SQL output on representative fixture, real plan/cost, tooling compatibility and unsupported-syntax fallback.
- **See:** [SQL for science/AI](SQL_SCIENCE_AND_EMERGING.md).

## Cross-chapter implementation rules (Mimir synthesis)

1. **Correctness first:** Ch. 4 row grain and time semantics govern Ch. 2 joins/windows; query speed never justifies silent change of metric or cohort.
2. **Access method is workload-dependent:** Ch. 2 index/pruning/cache choices must reflect Ch. 3 platform/concurrency and Ch. 5 orchestration/freshness costs.
3. **One consumer contract:** Ch. 3 data agreements + Ch. 5 semantic execution + Ch. 4 metric grain should agree from producer to model output.
4. **SQL can support science but does not validate inference:** Ch. 6 numeric computations require independent design/split/statistical evidence.
5. **New interfaces need new controls:** Ch. 7 external LLM calls and Ch. 8 dialect/compiler transformations each introduce security, audit and version boundaries.
6. **Incremental delivery:** test a small end-to-end slice across software, data engineering, analyst/ML and consumer; retain an actual known-answer reconciliation and rollback plan when operational.

## Additional technical documentation (not the book)

- [PostgreSQL window-function frames](https://www.postgresql.org/docs/current/functions-window.html)
- [PostgreSQL EXPLAIN and execution effects](https://www.postgresql.org/docs/current/sql-explain.html)
- [BigQuery query-performance best practices](https://cloud.google.com/bigquery/docs/best-practices-performance-compute)
- [Snowflake table/clustering decisions](https://docs.snowflake.com/en/user-guide/table-considerations)

**Extraction status:** full public chapter table of contents mapped (8/8 chapters); chapter previews checked; full-text extraction **not verified**. A licensed full copy would be needed to attribute more detailed chapter arguments or specific examples to the authors.
