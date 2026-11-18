# Notebook quality by data role

## Data analyst — question to reproducible result

- Start with a measurable question, intended audience, population, definition of the metric, and freshness requirement.
- Use parameterized, bounded, read-only SQL; inspect grain, join fanout, missing values, filters and periods before plotting.
- Include a known-answer query or fixture to check sums, denominators and category coverage. Explicitly state assumptions, selection and measurement limitations.
- Conclude with clearly supported results, uncertainty, and an explanation that a reader can follow without reading every code cell. Use `$data-storytelling` for chart and message guidance.

## Data engineer — source to debugging evidence

- Prefer notebook code that reads and inspects the same production transformation functions, not a rewrite of business logic hidden in cells.
- Show keys, event/ingest/effective timestamps, duplicates, schema drift, nulls, failed records and reconciliation. Bound I/O and explain sample representativeness.
- Do not build durable ingestion or mutate production storage as an automatic reactive cell. Move operational jobs to regular versioned Python/SQL pipelines with tests, retries, checkpoints, tracing and access control.
- For materialization or replay demonstrations use disposable datasets with explicit idempotency, cleanup and approval.

## Data scientist / ML engineer — evidence to decision

- Define target, label horizon, prediction timestamp, feature availability, entity/time split and leakage checks before training.
- Seed stochastic steps and record dependency/data/model versions; do not claim full determinism from a seed alone.
- Evaluate a simple baseline and final model against a fixed holdout; include relevant calibration, error slices and utility/cost assumptions rather than only accuracy.
- Expensive training and online model deployment belong in controlled jobs. A notebook may describe and reproduce controlled experiments but must not silently deploy or retrain on every widget change.

## Cross-role acceptance

At handoff, identify source ownership, output grain, quality/validation owner, privacy/freshness restrictions, actual tests run, and limitations. Export the same verified source for recipients; no manual Jupyter patch as a separate delivery branch.
