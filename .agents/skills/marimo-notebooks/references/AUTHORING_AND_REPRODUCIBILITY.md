# Authoring and reproducibility — Marimo first

## Notebook architecture

- Prefer small notebooks that answer one explicit question. A notebook should have a visible contract: input references, effective date, intended audience, analytic claim, assumptions, output and known-answer tests.
- Use ordinary `.py` modules for shared joins, validation, statistics, feature transformations, and business rules. Notebooks orchestrate and explain those modules rather than contain a second untested implementation.
- Use Marimo's cells for declarations and controlled computations. Global names should have a unique defining cell; underscore-prefixed temporary variables are cell-local in Marimo. Do not depend on execution history or the visual position of a cell for correctness.
- Keep expensive queries and model training behind deliberate controls. Marimo's dependency reactivity may re-run affected cells; setting a lazy execution policy, appropriate UI controls, caching with defined invalidation and pure functions can avoid unintended workload. None makes writes safe by itself.
- Put configuration in explicit parameters or config files. Specify credentials by approved runtime integration, never literals in notebook source, metadata, generated outputs, logs or prompts. Never commit real customer records simply to make a notebook self-contained.
- Record environment and package constraints, random seeds, model and feature versions, sampling windows and data snapshot/partition identifiers. A fixed random seed alone does not make external datasets or GPU kernels reproducible.

## Validating findings

- **Analysts:** validate denominator, row grain, filters, window boundaries, missingness, source versions, outliers, visual encodings and uncertainty. Separate exploratory findings from approved conclusions.
- **Data engineers:** assert schema, keys, duplicate/late record policy, timestamp semantics, reconciliation, checkpoint and idempotency if the notebook materializes data. Prefer read-only debugging and standalone pipeline code for actual jobs.
- **ML and data scientists:** define as-of availability of each feature, label horizon, entity/time splits, leakage tests, reproducible baseline, holdout discipline, metrics appropriate to utility, group coverage and evaluation uncertainty.
- **Everyone:** test a small fixture with known expected values and at least one failure case. Mark unrun warehouse-dependent tests explicitly. Source lint, kernel execution, numerical quality and production validation are distinct forms of evidence.

## Export / migration

- `marimo edit notebook.py` creates or edits the source notebook.
- `marimo check notebook.py` checks Marimo's supported static rules.
- `marimo export ipynb notebook.py -o generated/notebook.ipynb` generates a Jupyter artifact; do not write JSON or use `nbformat` to author it. The output format may not preserve reactive UI and dependency behavior.
- `marimo convert existing.ipynb -o notebook.py` is a **read-only import from legacy Jupyter** to a new Marimo source; examine and fix the converted source, run checks and only then regenerate deliverables. Conversion does not validate original notebook semantics.
- Marimo's editor offers automatic ipynb snapshots under `__marimo__/`; disable this when you want one controlled output path, or treat such snapshots as generated only and keep them out of commits.

Sources: https://docs.marimo.io/guides/coming_from/jupyter/ ; https://docs.marimo.io/guides/reactivity/ ; https://docs.marimo.io/guides/scripts/ ; https://docs.marimo.io/guides/exporting/jupyter_notebook/
