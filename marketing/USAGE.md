# Use Mimir on a real task

**Start with a clear outcome. Choose only the skills and checks your task needs.** Mimir serves data analysts, data engineers, analytics engineers, data scientists, ML engineers and application engineers working on data contracts.

[Overview](../README.md) · [Installation](SETUP.md) · [How it works](HOW_IT_WORKS.md)

## First session

Run `codex` from the target project root and start with this prompt.

> Read `.mimir/AGENTS.md` and the relevant skill instructions under `.agents/skills/`. Inspect the repository first. State relevant unknowns and do not edit files until the scope and acceptance checks are clear.

Review the proposed change and ask for the executed checks and their scope.

## Full-stack data prompts

### Data analyst — investigate a metric

> Analyze [business question] for [population/time period] using the existing approved metric. Inspect row grain, joins, denominators, null handling, missingness, freshness and alternative explanations. Produce a reproducible query, known-answer check and chart that shows relevant uncertainty.

### Analytics engineer — build a model

> For [business process], inspect the existing source records and consumers. Apply the dimensional design process: business process, grain, dimensions, facts. Check conformed dimensions, Type 2 history where needed, source reconciliation, incrementality and compatibility. Compare with the current normalized/OBT alternative only when relevant. Propose one reversible thin slice.

### Data engineer — recover a pipeline

> Inspect [pipeline/dataset] source availability, checkpoint, watermark, event and availability timestamps, accepted/rejected records and consumer freshness. Diagnose duplicate, late and missing records. Propose bounded replay and reconciliation with owners and rollback; do not execute destructive backfills without approval.

### Advanced SQL — fix correctness or performance

> Review [query] using `$advanced-sql`. State each input grain and join cardinality. Test duplicates, equal-amount transactions, NULL/anti-join behavior and deterministic order. Inspect the **actual** SQL dialect and representative execution plan before tuning; verify equivalent result after every optimization.

### Data scientist — evaluate a model

> Frame [decision] with action alternatives, label definition, available-at feature cutoff, baseline, action cost and evaluation window. Audit leakage/selection bias, use an appropriate time/group-aware split, and report uncertainty and expected decision utility.

### ML engineer — move to serving

> Review [offline model] for online inference. Define input/output schemas, feature availability, model version, latency, authorization, fallbacks, drift/quality monitors and staged rollback. Test a failure path and assess whether the existing serving stack is sufficient. Do not publish or enable actions without approval.

### Notebook authoring — Marimo first

> Create a Marimo `.py` notebook for [analysis], with a reproducible data/metric contract, checks and a well-supported conclusion. Use `$marimo-notebooks` to export through Marimo and run the manifest audit for any committed deliverable.

### Notebook composition — multiple sources to one export

> Combine `01_source.py`, `02_analysis.py` and `03_story.py` with a reviewed ordered manifest. Fail on conflicting Marimo cell globals or unsupported top-level statements; run `marimo check` on the composed `.py`, export through Marimo and verify generated `.ipynb` parity. If safe composition is impossible, keep separate notebooks.

### Cross-team slice — software to dashboard

> Trace [producer event] through [capture/transform/model/dashboard] in actual source. Define event identity/version, fact grain, business metric, temporal meaning and owner at each boundary. Plan the smallest end-to-end consumer-visible change, including duplicate and late data, reconciliation, compatibility and recovery tests. Use the advanced application method only for consequential state/effects.

## Other supported software tasks

| Task | Prompt pattern |
| --- | --- |
| Bug fix | Reproduce [bug], trace the actual failure, make the smallest fix and run targeted tests. Report remaining unknowns. |
| Authorization | Trace all relevant report/API/export access boundaries, verify allowed and denied paths, and keep secrets outside the agent identity. |
| UI/dashboard | Trace loading, empty, stale, denied and error states; preserve keyboard/accessibility behavior and the existing design system. |
| Migration | Review affected readers/writers, downtime, rollback, backfill, contract versions and explicit production approval. |
| Formal rule | Draft candidate Bend laws only for a reviewed, critical invariant; keep model proof separate from production tests. |
| Product copy | State the supported audience, decision and verified behavior; remove unsupported claims and confusing language. |

## Acceptance checklist

- Did the outcome, business meaning and relevant boundaries receive explicit approval?
- Are the file paths, source records, metric/feature grain and timestamps verified or marked unknown?
- Are checks reported with **command, observed result and scope**, including failures and tests not run?
- Is the change reviewable and reversible, with release ordering and recovery appropriate to the risk?
- For notebooks, are `.ipynb` outputs traceable to Marimo `.py` sources through a manifest?

For code changes, inspect `git status --short`, `git diff --stat`, and `git diff --check` as applicable.

[Data playbook](DATA_PLAYBOOK.md) · [Engineering foundations](ENGINEERING_PLAYBOOK.md) · [Install/recover](SETUP.md)
