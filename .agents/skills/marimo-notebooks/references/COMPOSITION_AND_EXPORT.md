# Multi-Marimo composition and generated Jupyter delivery

**Important:** Marimo documents `marimo export ipynb` for one Marimo Python notebook. It does not document a general command that merges independent Marimo notebooks into one code-preserving Jupyter notebook. The following composer is **Mimir-specific**, deliberately narrower and fail-closed.

## Workflow

1. Keep each authored notebook as `notebooks/marimo/*.py`. Never edit `.ipynb` as the source. Use paths without secrets.
2. Create an **ordered** `notebooks/collection.json`:

```json
{
  "schema": 1,
  "sources": ["marimo/01_question.py", "marimo/02_analysis.py"],
  "composed": ".build/combined.py",
  "output": "generated/combined.ipynb"
}
```

3. `python scripts/mimir-notebooks bundle --manifest notebooks/collection.json` writes the generated Marimo `.py` from whole `@app.cell` functions; runs `marimo check`; then runs `marimo export ipynb` to create the final `.ipynb` atomically. **It never manually creates Jupyter JSON.**
4. `python scripts/mimir-notebooks verify --manifest notebooks/collection.json` regenerates a temporary export and compares it to the existing output. Use this in CI or a local pre-commit check whenever a generated Jupyter file is committed. The output may differ if computation reads time-varying input or produces nondeterministic outputs; solve reproducibility at the source, not by patching `.ipynb`.
5. For a release with one or more committed notebooks, run `python scripts/mimir-notebooks audit --root notebooks`. It discovers all `collection.json` manifests below `notebooks/`, rejects any `.ipynb` that is not declared by one, rejects missing generated outputs, and runs Marimo-backed verification for every declared export. This makes manual editing, creation, and stale exports fail CI. This audit requires Marimo installed, since it must re-export rather than assume provenance from a filename. Each export must be manifest-managed, even for one source. Keep third-party/legacy notebooks outside the audited tree until converted.
6. To export one notebook for a temporary or untracked handoff, use `python scripts/mimir-notebooks export --source notebooks/marimo/01_question.py --output notebooks/generated/01_question.ipynb`. Pass `--verify` to validate an existing artifact without editing it.

## Collision/compatibility policy

- Both sources must use standard Python Marimo file shape (`import marimo`, `app = marimo.App(...)`, `@app.cell`, optional main guard). The composer rejects all unsupported top-level code rather than silently omitting semantics. It cannot safely compose custom setup cells, import hooks or unconstrained Python modules.
- All cell-defined public globals must be unique across sources. Repeated standard `import marimo as mo; return (mo,)` cells are deduplicated; other repeated definitions cause failure. Named `@app.cell` function names also must not collide. The Marimo linter is the authoritative dependency check.
- If notebook A assumes an output from notebook B, declare that dependency via the same Marimo global name, and keep source order intentional for readers. The Marimo exporter uses topological ordering by default when necessary for executable Jupyter output.
- The composer preserves cell source, not the original app-level configuration, layout, independently saved UI state, or notebook-specific environment. The combined notebook is a *new notebook*. Check it and review the exported narrative. For complex independent notebooks prefer separately generated `.ipynb` deliverables.
- The export command may execute notebook code depending on exporter options and Marimo version. Treat any export as potentially executing untrusted or costly code. Use read-only credentials and isolated infrastructure for sensitive work; do not run exported notebooks as a hidden step of CI without approval.
- If external Jupyter consumers require interactive widgets, validate them in an actual Jupyter environment. Neither an `.ipynb` file nor JSON parity proves widget compatibility or runtime correctness.

## Generated-file discipline

Generated `.build/combined.py` and `generated/combined.ipynb` must never be manually edited. Committed `.ipynb` files must match a documented generator and manifest. Review source `.py` diffs. If exporting fails, retain the last good artifact until the source is corrected. CI should check the source and verify that committed exports are fresh; a commit hook alone cannot enforce this policy against every actor.

Sources: https://docs.marimo.io/guides/exporting/jupyter_notebook/ ; https://docs.marimo.io/guides/reactivity/ ; https://docs.marimo.io/api/app/

## Example CI gate

```bash
python scripts/mimir-notebooks audit --root notebooks
```

The audit fails when Marimo is unavailable, a committed export has drifted, a manifest is missing, or an export was produced outside this workflow. For a standalone notebook, declare a manifest with one source and run `bundle`.
