# Engineering foundations for full-stack data

**Use the smallest amount of engineering structure that can establish a correct, maintainable result.** Mimir's default [`$software-design-thinking`](../.agents/skills/software-design-thinking/SKILL.md) provides eight principles for engineering and data work.

[Overview](../README.md) · [Full-stack data playbook](DATA_PLAYBOOK.md) · [Tasks](USAGE.md) · [Optional stateful-application walkthrough](ADVANCED_APPLICATION_WALKTHROUGH.md)

## Eight principles, selected by consequence

| Principle | Data-focused application | Minimum useful evidence |
| --- | --- | --- |
| 1. Define the problem | State consumer, decision, population, constraints and owner. | Approved question and acceptance criteria. |
| 2. Define contracts | Specify source schema, **row grain**, identity, keys, units, time semantics and permitted use. | Contract and representative records. |
| 3. Establish correctness | Define business invariants and meaningful exceptions. Schema compliance alone is insufficient. | Known-answer or reconciliation checks. |
| 4. Trace the flow | Follow producer → capture → transform → consumption and handoffs actually present. | Source-grounded lineage and unknown edges. |
| 5. Make calculation testable | Prefer deterministic queries/functions; isolate clocks, random seeds, external reads and writes where useful. | Reproducible query, fixture or experiment. |
| 6. Handle real failures | Address duplicates, late data, partial writes, stale results, retries and recovery **when applicable**. | Failure-specific test and responsible owner. |
| 7. Verify with evidence | Check semantics, numerical results, statistical validity and the observed runtime within tested scope. | Command, result, time and limitations. |
| 8. Deliver one thin slice | Ship a useful source-to-consumer increment with compatibility and rollback considered. | Consumer acceptance and safe next change. |

## Choose the right engineering depth

| Situation | Default approach | Add when needed |
| --- | --- | --- |
| Analyst query, report, notebook | Metric/grain definition, sampling and SQL checks, reproducible outputs. | Data freshness, privacy or impact-specific reviews. |
| Dimensional mart or production pipeline | Above plus data contracts, quality, replay, changes to history, observability and recovery. | Transactional semantics and concurrency for shared writes. |
| Offline ML evaluation | Cohort, label/cutoff, point-in-time features, leakage checks, baselines, proper split and reproducibility. | Serving and monitoring only when deploying. |
| Online predictions or stateful producer | Full application state, effect ownership, access control, fallback, rollout/rollback and live monitoring. | [Advanced walkthrough](ADVANCED_APPLICATION_WALKTHROUGH.md) and [advanced method](../.agents/skills/software-design-thinking/references/ADVANCED-APPLICATION-DESIGN.md). |

## Example: one revenue change across teams

For a captured-revenue dashboard, reconcile one date against a known set of captures.

1. **Producer:** confirm the actual event ID, version, currency, time, permission and retry semantics in the application source.
2. **Ingestion:** keep original IDs, handle replay and duplicates, and expose late/missing records rather than silently dropping them.
3. **Model:** declare a capture fact at the approved grain and history policy; keep refunds and net revenue separate until defined.
4. **Query:** use the approved aggregation with a small fixture that detects one-to-many join fanout and equal-amount `SUM(DISTINCT ...)` errors.
5. **Consumer:** show the metric period, freshness and definition; compare with independently sourced totals before release.
6. **Delivery:** agree on cross-team contract owners and a reversible deployment order. State unobserved paths as unknown.

Follow the [cross-team slicing method](../.agents/skills/data-slicing/references/CROSS_TEAM_SLICES.md) when work crosses teams.

## Practical verification by discipline

| Work | Appropriate check |
| --- | --- |
| SQL query | Known-answer fixture, row counts, NULL/join/window semantics; actual engine plan if tuning. |
| Dimensional model | Grain, history interval, fact additivity, source reconciliation and consumer compatibility. |
| Experiment | Assignment, estimand, sample size, confounding, intervals and uncertainty. |
| Predictive model | Time-aware split, leakage inspection, baseline, utility and drift/serving review when relevant. |
| Marimo notebook | Source `.py`, `marimo check`, source/output manifest, regenerated Jupyter export. |
| Production pipeline | Replay/late data, freshness, affected consumers, idempotency and recovery exercises. |

Use the [Advanced SQL skill](../.agents/skills/advanced-sql/SKILL.md), [Marimo notebook skill](../.agents/skills/marimo-notebooks/SKILL.md), [data playbook](DATA_PLAYBOOK.md) and [documentation templates](../docs/data/README.md) for detail. If a task needs explicit state machines, typed result handling or effects-as-data, consult the [optional application walkthrough](ADVANCED_APPLICATION_WALKTHROUGH.md).

[Setup](SETUP.md) · [Use Mimir](USAGE.md) · [Back to overview](../README.md)
