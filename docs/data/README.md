# Example data product records (reference templates)

Mimir ships these files as **release examples only**; the project installer does not copy or create an application's `docs/` content. An operator explicitly authorizes any writing into an application repository's `docs/` directory. Use the smallest relevant subset, following local conventions. One page and a tested query can be sufficient for a small change.

| Need | Template |
| --- | --- |
| End-to-end software + data team delivery | [Vertical slice](VERTICAL_SLICE_TEMPLATE.md) |
| Producer/consumer handoff | [Data contract](DATA_CONTRACT_TEMPLATE.md) |
| Business process and analytic schema | [Dimensional model](DIMENSIONAL_MODEL_TEMPLATE.md) |
| SQL query correctness, windows, plan, dialect and performance | [SQL query review](SQL_QUERY_REVIEW_TEMPLATE.md) |
| 3NF/star/snowflake/OBT/lakehouse/semantic design comparison | [SQL model choice](SQL_MODEL_CHOICE_TEMPLATE.md) |
| KPI / metric definition | [Metric specification](METRIC_TEMPLATE.md) |
| Statistical analysis / experiment | [Statistical analysis](ANALYSIS_TEMPLATE.md) |
| Predictive model, expected value or decision action | [Model decision](MODEL_DECISION_TEMPLATE.md) |
| Data-driven report or dashboard | [Story brief](STORY_BRIEF_TEMPLATE.md) |
| Freshness/quality, replay and recovery | [Operations](OPERATIONS_TEMPLATE.md) |

Templates are reminders of decision points, **not** an artifact quota. Mark Known / Assumed / Unknown. Link to observed test runs, dataset snapshots and approved product definitions rather than asserting completion from a template.
