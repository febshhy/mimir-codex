# How Mimir works

**Mimir coordinates source-grounded engineering and data analysis around one verifiable outcome.** It supplies instructions, focused skills, optional local orchestration and review contracts.

[Overview](../README.md) · [Install](SETUP.md) · [Use on a task](USAGE.md)

## From question to evidence

| Stage | Typical work | Inspectable evidence |
| --- | --- | --- |
| **Define** | Identify the business question or behavior, owner, grain, time, success criteria and unknowns. | Approved contract and explicit assumptions. |
| **Trace** | Follow relevant application source, ingestion, models, queries, notebooks and consumers as they exist. | Actual file paths, queries, lineage, and gaps marked unknown. |
| **Choose** | Compare the smallest change with credible alternatives using the existing stack. | Tradeoffs, risks, acceptance plan. |
| **Implement** | Modify only the agreed slice; keep boundaries and ownership clear. | Reviewable source diff and versioned contracts. |
| **Verify** | Run the relevant fixture, test, reconciliation, model evaluation and operational check. | Commands and observed results. |
| **Communicate** | Present the metric, decision, limitations and safe next step. | Reproducible output and a consumer-oriented explanation. |

The default [engineering skill](../.agents/skills/software-design-thinking/SKILL.md) contains eight principles. Mimir loads advanced application state/effect methods only when the task warrants them.

## Skills by task

| Task | Main skills | Distinct correctness question |
| --- | --- | --- |
| Investigate a SQL metric | `$advanced-sql`, `$data-dimensional-modeling` | Does the query retain its approved grain, join cardinality and time meaning? |
| Produce a reliable dataset | `$data-lifecycle`, `$data-operations` | Can it handle schema changes, late events, replay and failure? |
| Analyze a trend or experiment | `$data-statistics`, `$data-storytelling` | Which inference and communication are justified by the evidence? |
| Evaluate a prediction | `$data-decision-science`, `$data-statistics` | Is the holdout leakage-free and does the decision improve on a baseline? |
| Author or combine notebooks | `$marimo-notebooks` | Are the Marimo `.py` sources reproducible and the `.ipynb` exports generated? |
| Change event-producing software | `$software-design-thinking`, `$data-slicing` | Are producer state, event and consumer meanings compatible? |

One person may perform several roles. The [data playbook](DATA_PLAYBOOK.md) details data contracts and vertical slices; the [engineering playbook](ENGINEERING_PLAYBOOK.md) covers cross-role foundations.

## Example: captured revenue, from source to dashboard

```ts
Checkout capture event with identity, time and version
  → ingestion with deduplication and late-event policy
    → fact at one approved payment-capture grain
      → approved daily metric (currency, timezone, denominator as applicable)
        → dashboard with definition, freshness and access controls
          → source reconciliation, backfill and change monitoring
```

The producer owner establishes event meaning. Data engineering owns ingest/replay. Analytics owns the fact grain and agreed metric implementation. The consumer owner accepts the presented meaning and stale-state behavior. A known-answer fixture and source reconciliation support a scoped result.

## Delegation, review and permissions

For a small task, a single engineer or analyst and a focused test may be sufficient. For work crossing independent boundaries, [Graph Protocol](../.agents/skills/graph-protocol/SKILL.md) can describe responsibilities and handoffs. Its optional `scripts/factory` controller validates declared task records and local evidence. Codex handles agent scheduling.

A project-local reviewer is configured in [`.codex/agents/mimir_reviewer.toml`](../.codex/agents/mimir_reviewer.toml). Assign the reviewer an independent review task when needed.

Project installation inserts a **short instruction reference** into the active root `AGENTS.md`, and installs the full coordinator guide as `.mimir/AGENTS.md`. Ask Codex to read the full installed guide when you start a Mimir task. [Setup](SETUP.md#how-codex-reads-the-installed-guidance).

## What counts as evidence?

| Claim | Useful support |
| --- | --- |
| A source path exists | Inspected code at a known revision. |
| A result is numerically right for tested rows | Approved meaning + query + reconciliation/known-answer cases. |
| A statistical or ML finding holds | Reproducible data, suitable design, uncertainty/baseline checks. |
| A notebook is generated properly | Registered Marimo source, CLI export, source parity/audit. |
| A delegated task passed local review | Recorded handoff, actual diff and executed checks. |
| A formal property was proved | Reviewed law and checked model assumptions. |

Use sandboxing, scoped credentials, and approval controls for the execution environment. [Credential boundary](../docs/security/CREDENTIAL_BOUNDARY.md).

[Setup](SETUP.md) · [Task examples](USAGE.md) · [Overview](../README.md)
