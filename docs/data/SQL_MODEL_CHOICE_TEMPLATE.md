# SQL data-model choice — optional record

> This is a decision aid for a consequential model change. It is not a requirement to introduce a new schema, graph engine, materialization or ADR. The project installer does not write application `docs/`.

## Problem and existing fit

- Approved consumers/questions, product meaning and owners:
- Existing sources, constraints and why the current model does/does not work:
- One row represents (event/entity/snapshot/version):
- Keys, identity/relationship cardinality and integrity:
- Event/effective/ingest/availability time and history semantics:
- Measures, additivity, units, aggregation and metric definitions:
- Access/privacy/retention boundaries:

## Representations considered

| Candidate | Strength for this workload | New update/anomaly risk | Query/performance/ops evidence | Migration/reversal cost |
| --- | --- | --- | --- | --- |
| Existing schema unchanged | | | | |
| 3NF / normalized | | | | |
| Star or snowflake | | | | |
| One big table / consumer projection | | | | |
| Lakehouse / medallion layers | | | | |
| Semantic layer or graph | | | | |

Only fill relevant rows. Do not treat all options as direct substitutes; a platform may contain more than one.

## Decision and validation

- Selected model and rejected alternative(s), with reasons:
- Change in fact grain/keys, temporal and schema contract:
- Conformed dimensions/metrics and consumers (if analytic):
- Update/late event/delete/backfill behavior:
- Known-answer row examples and reconciliation with source:
- Fanout/uniqueness/Type 2 intervals and metric tests:
- Query plan/cost and concurrency impact (measured or not measured):
- Deployment/compatibility/rollback and accountable owners:
- Known | Assumed | Unknown:
