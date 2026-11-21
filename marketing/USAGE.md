# Use Mimir on a real task

**Tell Codex the outcome you need. Mimir supplies the engineering procedure.** Start with the report, dataset, model, or application behavior you want to change.

[Overview](../README.md) · [Installation](SETUP.md) · [How it works](HOW_IT_WORKS.md)

## First session

Start a Codex session in the installed project using the app, IDE extension, or CLI. Use this prompt for your first task.

> Read `.mimir/AGENTS.md` and the relevant skill instructions under `.agents/skills/`. Inspect the repository first. State relevant unknowns and do not edit files until the scope and acceptance checks are clear.

Review the proposed change and ask for the executed checks and their scope.

For delegated engineering work, GPT-6.2 Sol coordinates and independently reviews; GPT-6 Luna performs bounded implementation and evidence tasks. Start subagents with fresh context (`fork_turns: none`) and include A/E/R assignment, evidence outputs, and explicit acceptance criteria. For each delegated WRITE, a different Luna agent collects the diff, source, and check evidence. Sol reviews it and accepts only through the schema-3 factory gate. When a runtime path needs explanation, provide a source-derived `ts` call trace with the real entry point and indented `→` calls; separate Production and Tests when their wiring differs. Mark unimplemented paths proposed.

The configured hook checks the current model, exact target profile/model pairings for launches, `fork_turns: none`, and Luna-model command/edit/write routing. PreToolUse does not document a caller profile field, so the hook cannot identify the caller's agent profile. Fixtures exercise these documented field checks; they do not verify live Codex hook execution or enforcement. The reviewer profile disables supported shell, app, plugin, memory, and permission-request capabilities, but feature flags do not prove a live sandbox.

## Task examples

Replace the text in square brackets with your own context. Review the proposed scope and checks before asking Codex to make changes.

### Data analyst — investigate a metric

> Analyze [business question] for [population/time period] using the existing approved metric. Inspect row grain, joins, denominators, null handling, missingness, freshness and alternative explanations. Produce a reproducible query, known-answer check and chart that shows relevant uncertainty.

### Analytics engineer — build a model

> For [business process], inspect the existing source records and consumers. Apply the dimensional design process: business process, grain, dimensions, facts. Check conformed dimensions, Type 2 history where needed, source reconciliation, incrementality and compatibility. Compare with the current normalized/OBT alternative only when relevant. Propose one reversible thin slice.

### Data engineer — recover a pipeline

> Inspect [pipeline/dataset] source availability, checkpoint, watermark, event and availability timestamps, accepted/rejected records and consumer freshness. Diagnose duplicate, late and missing records. Propose bounded replay and reconciliation with owners and rollback; do not execute destructive backfills without approval.

### Advanced SQL — fix correctness or performance

> Review [query] using `$advanced-sql`. Trace the grain and join cardinality of each input. Test duplicate rows, equal-amount transactions, NULL handling, anti-joins, and ordering where they affect the result. Use the target engine’s execution plan to guide tuning and rerun the result checks after each change.

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

## Decide whether the result is ready

- Did the outcome, business meaning and relevant boundaries receive explicit approval?
- Are the file paths, source records, metric/feature grain and timestamps verified or marked unknown?
- Are checks reported with **command, observed result and scope**, including failures and tests not run?
- Is the change reviewable and reversible, with release ordering and recovery appropriate to the risk?
- For notebooks, are `.ipynb` outputs traceable to Marimo `.py` sources through a manifest?

For code changes, inspect `git status --short`, `git diff --stat`, and `git diff --check` as applicable.

[Data playbook](DATA_PLAYBOOK.md) · [Engineering foundations](ENGINEERING_PLAYBOOK.md) · [Install/recover](SETUP.md)
