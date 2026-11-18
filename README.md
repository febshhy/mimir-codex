# Mimir

**Trace the change. Preserve the contract. Verify the result.**

Mimir gives Codex CLI a disciplined way to work across application code, data pipelines, analysis, and ML. It helps you trace the affected paths, make a focused change, and inspect the evidence behind the result. Use it with your existing project, data stack, and tests.

![An ancient stone well beneath the roots of Yggdrasil, surrounded by mist and moss.](marketing/mimir-well.webp)

**[Get started](marketing/SETUP.md)** · [See the method](marketing/HOW_IT_WORKS.md) · [Try a task](marketing/USAGE.md)

## Why Mimir?

A request that sounds small can change results in several places. A change to how checkout records a payment, for example, can affect ingestion, the revenue query, and the dashboard. Follow the change from the payment event to the number people use.

1. **Trace before editing.** Find the source records, the code that produces them, and the people who use the result. Check what one row represents and which timestamp governs the result.
2. **Change only what the task needs.** Choose one source-to-consumer change and agree on the contracts it crosses.
3. **Verify what changed.** Check the result against known records and exercise the failure paths that matter.

<picture>
  <source media="(max-width: 640px)" srcset="marketing/mimir-source-to-decision-mobile.svg">
  <img src="marketing/mimir-source-to-decision.svg" alt="A stone channel carries water from Mímir’s well to a basin above cultivated fields.">
</picture>

**Source records** → **Data pipeline** → **Verified result** → **Decision**

[See how the method handles captured revenue](marketing/HOW_IT_WORKS.md#example-captured-revenue-from-source-to-dashboard) · [Learn the engineering behind it](marketing/ENGINEERING_PLAYBOOK.md)

## Start in an existing project

Run these commands in **Linux Bash** or **WSL on Windows**. You need Bash 4.4+, Python 3.9+, Git, `jq`, and Codex CLI. [Check the setup prerequisites](marketing/SETUP.md#prerequisites).

**1. Get Mimir outside your application repository.**

```bash
mkdir -p "$HOME/tools"
git clone https://github.com/febshhy/mimir-codex.git "$HOME/tools/mimir-codex"
```

**2. Preview changes to your clean Git project.**

```bash
cd /path/to/your-project
bash "$HOME/tools/mimir-codex/scripts/mimir" start --project . --integrate-agents
```

**3. Review the plan, apply it, and verify installation.**

```bash
bash "$HOME/tools/mimir-codex/scripts/mimir" start --project . --integrate-agents --apply
bash .mimir/install.sh --verify
codex
```

Apply checks that the saved plan still matches the project. The installer preserves unrelated instructions and leaves your project's `docs/` directory alone.

For a [new project](marketing/SETUP.md#new-project), [global installation](marketing/SETUP.md#global-installation), or recovery, use the [setup guide](marketing/SETUP.md).

## Give Codex a first task

> Read `.mimir/AGENTS.md` and the relevant skills in `.agents/skills/`. Trace [business metric] from its source records to the report using real names. Identify the grain, timestamps, owners, and failure cases. Propose the smallest change and show how you would verify it against known records. Do not edit files yet.

For analyst, ingestion, dimensional modeling, ML, SQL tuning and notebook prompts, use [task examples](marketing/USAGE.md). The [book method index](marketing/BOOK_CONCEPTS.md) links the [chapter mapping](marketing/CHAPTER_TRACEABILITY.md) and [Advanced SQL chapter mapping](.agents/skills/advanced-sql/references/MACHADO_RUSSA_ESMERIZ_CHAPTER_MAP.md).

## Find the skills for your work

| Work | Skills to start with | What gets verified |
| --- | --- | --- |
| Data analyst | `$advanced-sql`, `$data-statistics`, `$data-storytelling` | Metric definitions, grain, bias, uncertainty and decision-ready charts. |
| Analytics engineer | `$data-dimensional-modeling`, `$advanced-sql` | Fact grain, history, keys, fanout, source reconciliation and semantic compatibility. |
| Data engineer | `$data-lifecycle`, `$data-operations` | Capture contracts, schema changes, retries, late data, replay and consumer freshness. |
| Data scientist | `$data-decision-science`, `$data-statistics`, `$marimo-notebooks` | Cutoffs/leakage, baselines, holdouts, reproducibility and decision value. |
| ML engineer | Those above plus `$software-design-thinking`, `$testing` | Serving contracts, fallbacks, monitoring and safe deployment/rollback. |
| Cross-team delivery | `$data-slicing`, `$graph-protocol` when warranted | One reviewable source-to-consumer slice, clear owners and acceptance evidence. |

Mimir ships **23 skills**. Choose skills by task. Use the [advanced application method](.agents/skills/software-design-thinking/references/ADVANCED-APPLICATION-DESIGN.md) for stateful services and the [Advanced SQL skill](.agents/skills/advanced-sql/SKILL.md) for data modeling, query semantics, and performance.

## The source-to-decision workflow

```ts
Business question or product behavior
  → actual source event / operational records (identity, time, version)
    → capture and data pipeline (freshness, replay, quality)
      → trusted model and metrics (grain, history, consumer contract)
        → query, analysis, feature or prediction (uncertainty, evaluation)
          → dashboard, API or action (meaning, access, fallback)
            → reconciliation, observation and safe recovery
```

Start with the smallest testable vertical slice. Assign an owner to each cross-team contract and reconcile results against known values. [See the data playbook.](marketing/DATA_PLAYBOOK.md)

## Project model defaults

| Session role | Configured model | Reasoning |
| --- | --- | --- |
| Main implementation | `gpt-6.2-sol` in `.codex/config.toml` | `low` |
| Optional independent review | `gpt-6-luna` in `.codex/agents/mimir_reviewer.toml` | `high` |

## Marimo-first notebook rule

Author notebooks as Marimo `.py` files and generate `.ipynb` deliverables with Marimo. For multiple input notebooks, compose a new Marimo `.py` using a reviewed manifest before exporting.

```bash
# Optional dependencies only for notebook work (Python compatible with marimo).
python -m pip install marimo nbformat
marimo edit notebooks/marimo/analysis.py
python scripts/mimir-notebooks export --source notebooks/marimo/analysis.py --output notebooks/generated/analysis.ipynb

# For multiple Marimo sources registered in notebooks/collection.json:
python scripts/mimir-notebooks bundle --manifest notebooks/collection.json
python scripts/mimir-notebooks verify --manifest notebooks/collection.json
python scripts/mimir-notebooks audit --root notebooks
```

Register each committed `.ipynb` in a manifest for the audit. Run the audit in CI and verify execution in the target Jupyter environment. See the [notebook skill](.agents/skills/marimo-notebooks/SKILL.md) and [composition contract](.agents/skills/marimo-notebooks/references/COMPOSITION_AND_EXPORT.md).

## Keep decisions and evidence in your control

Your project defines the expected behavior. Its tests, queries, and runtime checks provide the evidence. Use an isolated execution environment or a broker with scoped access for sensitive credentials. [Understand what counts as evidence](marketing/HOW_IT_WORKS.md#what-counts-as-evidence) · [Read the credential guidance](docs/security/CREDENTIAL_BOUNDARY.md)

## The name behind Mimir

Mimir takes its name from the figure associated with the well of wisdom in Norse mythology. The well in the illustration evokes the toolkit’s starting point. Find the source and understand what it can tell you before drawing a conclusion. [Mímir’s well in the Prose Edda](https://en.wikisource.org/wiki/Page%3AThe_Prose_Edda_%281916_translation_by_Arthur_Gilchrist_Brodeur%29.pdf/59)

[MIT license](LICENSE).
