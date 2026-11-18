# SQL for statistics, ML, GenAI and emerging query languages

**Source connection:** Book chapters 1 and 6–8 cover temporal/semi-structured/graph SQL, descriptive and inferential statistics, regression/outliers, SQL-driven feature engineering/training/deployment, GenAI SQL functions, embeddings/RAG/agents/MCP, and Pipe SQL, PRQL, Malloy. The operational selection and safety criteria here are **Mimir synthesis**. Use `$data-statistics` and `$data-decision-science` for inference/ML authority.

## Descriptive and inferential SQL

SQL can compute counts, distributions, percentiles, variability, covariances, correlations, basic regression aggregates and grouped time comparisons. Check:

- **Population and measurement:** target population, sample unit, inclusion/exclusion, missingness, unit weighting and snapshot; SQL will happily compute a precise answer for the wrong cohort.
- **Aggregation:** weighted vs unweighted measures, distinct people vs events, sample vs population standard deviation, numerical precision, output NULL policy and denominator zero.
- **Correlation/regression:** inspect selection, dependence, influential observations, time trends and confounding; do not label an association causal.
- **Normality/outliers:** distribution assumptions and transformation decisions; flag anomalies without deleting legitimate business cases silently.
- **Confidence intervals/hypothesis tests:** sampling design, clustering, multiple comparisons, effect size and assumptions matter. Warehouse-native statistical functions vary; independent statistical-tool validation is appropriate for consequential inference.
- **Privacy:** small-cell disclosure and aggregate sensitivity can still leak personal data.

A `p`-value, model score, or line chart does not prove a conclusion without design validity. For experiments, inference and causal claims the statistical skill remains decisive.

## Model-ready SQL datasets

Define **prediction unit, prediction time, label window, label availability, feature availability, entity resolution and exclusion policy** before writing feature SQL. For historical samples:

1. Form one row per entity × prediction cutoff (or stated alternate grain).
2. Limit each source fact to records **known/available by that cutoff**. A backfilled event with old event time may have been unavailable at the historical decision.
3. Use deterministic as-of windows to select the last valid feature (tie breakers for duplicates/revisions).
4. Ensure label events occur in the outcome horizon and were not used to construct contemporaneous features.
5. Use time/group split and untouched holdout as specified by `$data-decision-science`; compare to a naive baseline and business utility.
6. Verify offline/online feature parity and serving latency only for production use. Version transforms and feature freshness/drift monitors.

[Fixture-backed point-in-time query](../examples/asof_features.sql) shows the temporal availability criterion. The fixture proves a narrow example, not general model validity.

SQL-native ML training can reduce data movement and simplify governance in a suitable warehouse. It may also limit model choice, evaluation, reproducibility, portability or cost control. Compare to an existing Python/R pipeline on actual needs before migrating.

## Generative AI in SQL (conditional)

The book's chapter 7 includes LLM functions, embeddings, vector retrieval, RAG and SQL-mediated agents/MCP. These are optional; they are **not** part of the default SQL querying method.

- Decide whether a deterministic SQL query, search index or conventional classifier solves the task. Generate text only when the output really needs generation.
- Specify exact model/provider/version/region, external-data flow, authorization and permitted sensitive fields. Warehouse data may be sent to a third-party model depending on integration.
- For RAG, define document authority, partition/tenant filters, embedding version, retrieval recall/precision, chunk lineage and citation grounding. Row-level access must apply *before* retrieval and generation.
- Evaluate factuality, citation correctness, prompt injection resilience, refusals/safety, privacy leakage, failure fallback, latency and cost on representative cases; deterministic SQL checks alone are insufficient.
- Treat agent or MCP tool execution as permissioned side effects, with explicit owner, budget, idempotency/rollback and audit. Do not let generated SQL execute unrestricted data-changing statements.

## Emerging SQL syntax and portability

- Book chapter 8 treats **GoogleSQL Pipe Syntax** (linear sequence of relational operators) and alternatives such as **PRQL** and **Malloy**. Determine availability in the actual installed dialect and client tooling, then compare readability, generated SQL, errors, tests and migration costs.
- Pipe syntax changes expression style, not data semantics or execution proof. Declarative semantics and actual query plans still govern performance.
- Temporal, JSON/semi-structured, vector, graph and ML SQL functions are platform-specific; cite documentation with a tested version. Do not claim standard support from another engine's syntax.
- AI-assisted SQL generation is untrusted draft code. Review logical grain, execution costs, permissions and parameters before running it.
- Quantum-assisted optimization is a future-looking topic from the book's contents, not a production requirement or a supported Mimir capability.

## When not to force SQL

Use Python/R/other tools when reproducible scientific packages, iterative algorithms, simulations, specialized statistical assumptions, complex model governance or team competence make them more reliable. SQL remains valuable for controlled source/feature preparation and serving contracts. Use the smallest sufficient combination.
