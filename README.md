# Mimir

**Full-stack data work, from source contracts to verified decisions.**

Mimir is a local **Codex CLI instruction and skill toolkit** for data analysts, analytics engineers, data engineers, data scientists, ML engineers, and the application engineers who produce or consume their data. It gives these roles a shared approach to contracts, correctness, testable changes, reliable SQL, meaningful models and cross-team delivery.

[Install](marketing/SETUP.md) · [How it works](marketing/HOW_IT_WORKS.md) · [Task examples](marketing/USAGE.md) · [Data playbook](marketing/DATA_PLAYBOOK.md) · [Engineering foundations](marketing/ENGINEERING_PLAYBOOK.md)

## Who uses which part?

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

## Quick start — Linux / WSL

Requirements for installation: Bash 4.4+, Python 3.9+, Git, `jq`, coreutils and an independently installed Codex CLI. Keep the **extracted Mimir release outside the target Git project**.

```bash
# Run from your existing Git project root. Replace with the actual extracted path.
cd /path/to/your-git-project
MIMIR_SRC=/path/to/extracted/mimir-codex

# Save and inspect a plan. This preview does not edit your project.
bash "$MIMIR_SRC/scripts/mimir" start --project . --integrate-agents

# Apply only the reviewed plan and verify the installed files.
bash "$MIMIR_SRC/scripts/mimir" start --project . --integrate-agents --apply
bash .mimir/install.sh --verify
codex
```

For a new directory, use `start` or `new`; for an existing Git repository, use `start` or `adopt`. Installations do not populate the target project's `docs/` directory. They reject collisions with unrelated managed files, including `.codex/config.toml`. See [setup, removal and recovery](marketing/SETUP.md).

The project installer adds a reference to the active root instructions and stores the coordinator guide at `.mimir/AGENTS.md`. Start a Mimir task with *“Read `.mimir/AGENTS.md` and the applicable skills in `.agents/skills/` before planning the change.”*

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

## First task to try

> Read the installed Mimir guidance, then inspect the actual source-to-consumer path for [business metric]. Identify event/schema ownership, grain, join cardinality, timestamps, metric definition, consumers and relevant tests. Mark missing evidence as unknown. Propose one thin change with a numerical known-answer check, a late/duplicate-data case, and a bounded recovery plan. Do not edit yet.

For analyst, ingestion, dimensional modeling, ML, SQL tuning and notebook prompts, use [task examples](marketing/USAGE.md). The [book method index](marketing/BOOK_CONCEPTS.md) links the [chapter mapping](marketing/CHAPTER_TRACEABILITY.md) and [Advanced SQL chapter mapping](.agents/skills/advanced-sql/references/MACHADO_RUSSA_ESMERIZ_CHAPTER_MAP.md).

## Security

Configure sandboxing and scoped credential access in the execution environment. [Credential boundary](docs/security/CREDENTIAL_BOUNDARY.md)

[MIT license](LICENSE).
