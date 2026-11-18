# Full-stack data engineering playbook

**Follow one change from its source to the person who uses the result.** Apply the [engineering foundations](ENGINEERING_PLAYBOOK.md) at each boundary. Establish what a row means, which time it represents, who owns it, and how to check the result.

## Trace one change from source to decision

```ts
Business consumer (question, action, authorized meaning)
  → Software producer (state, outbox/event/API, keys, version, permissions)
    → Lifecycle engineering (source, capture, replay, storage, transform, serve)
      → Analytical contract (fact grain, conformed dimensions, metric/history)
        → Evidence (descriptive estimate / experiment / predictive baseline)
          → Consumer (dashboard, API, model-influenced decision)
            → Observations (metric reconciliation, freshness, impact, recovery)
```

A data professional may perform multiple stages. Assign an accountable owner to each boundary. When an application state change drives data, use `$software-design-thinking` for the shared core and the appropriate data skills for downstream semantics. Add the [advanced application walkthrough](ADVANCED_APPLICATION_WALKTHROUGH.md) only for consequential state/effects.

## Choose a path for the task

| Outcome | Skills to load | Evidence that matters |
| --- | --- | --- |
| Add an event to an API and dashboard | software design, data slicing/lifecycle, dimensional modeling, testing | Producer schema compatibility, grain, replay, query and UI state |
| Fix duplicated revenue | dimensional modeling, advanced SQL, lifecycle, operations, testing | Declare grain, known-answer replay, fanout and source reconciliation |
| Review a slow cohort query | advanced SQL, statistics, database-design only for physical changes | Correct denominator and null/window semantics, real plan/cost comparison, equivalent result |
| Compare star vs OBT vs normalized model | advanced SQL, dimensional modeling, database-design | Ownership, row grain and change semantics; representative query cost and migration burden |
| Define a churn rate | requirements, dimensional modeling, statistics, storytelling | Cohort, observation period, numerator/denominator, bias and uncertainty |
| Evaluate a marketing experiment | requirements, statistics, decision science, storytelling | Randomization/assignment, estimand, interval, errors and action costs |
| Put a model in an application | software design, lifecycle, decision science, operations, testing | Cutoff/leakage, baseline, output contract, fallback and online impact |
| Compose analysis/ML notebooks into Jupyter deliverable | marimo-notebooks, statistics/advanced-sql/decision-science as relevant | Marimo `.py` source and manifest, `marimo check`, known-answer tests, generated `.ipynb` parity, no direct JSON editing |
| Change a dashboard layout only | GUI, visual design, content writing as applicable | UI/readability/accessibility; don't rebuild data platform |

## Check data quality and plan recovery

Define what a row means and which use is allowed. Test uniqueness, completeness, temporal validity, non-null constraints **only where the meaning requires it**, and reconciliation. Determine if data were late or deleted, if dimensions changed and whether the consumer expects restatement. When uncertainty is material, state the population/estimand/sampling conditions and stop causal overclaiming.

Choose minimal observability that can answer incidents: source lag, landing lag, rejected records, duplicates, schema failures, last good partition, consumer freshness and actual observed correctness checks. Define recovery checkpoints and permitted writes. Protect user data with least privilege and an actual isolation boundary.

## Deliver one complete slice

1. Retrieve approved meaning and existing source/code. Mark unknown producer, metric or authorization decisions.
2. Trace one **vertical** source-to-consumer path, including software state and data lineage, with end-to-end expected numeric result.
3. Compare smallest alternatives in current stack; add technology only where needed for measurable latency, cost, safety or maintainability.
4. Implement thin versioned contract, quality checks, and failure-safe/replay behavior; coordinate app and data release order.
5. Observe one happy and representative unhappy path at relevant boundary, document rollback, then widen consumer coverage/scale.
6. Communicate a decision using statistics and narrative that the evidence supports.

Use [Advanced SQL query/model/performance methods](../.agents/skills/advanced-sql/SKILL.md), [book concept notes](BOOK_CONCEPTS.md), [cross-team slice algorithm](../.agents/skills/data-slicing/references/CROSS_TEAM_SLICES.md) and [source-specific templates](../docs/data/README.md).

## Author and export notebooks

Use `$marimo-notebooks` for analyst, data engineering and ML notebook work. Author Marimo `.py` sources and generate Jupyter `.ipynb` exports. When one delivery notebook must include multiple Marimo source notebooks, use a reviewed ordered manifest to produce a composed Marimo `.py`; lint that composition and export it through Marimo. Validate the final exported notebook before handoff; use separate deliverables when independent notebooks cannot be safely composed. In CI, run `python scripts/mimir-notebooks audit --root notebooks`; this requires a manifest for every delivered `.ipynb` and fails on stale or unregistered exports.
