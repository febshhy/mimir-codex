# Git and Pull-Request Procedure

Follow the **Trunk-based GitOps** contract in the coordinator instructions.
Luna owns Git and hosting tool calls. Sol accepts the reviewed candidate and
coordinates authorized delivery.

## 1. Workspace and branches

Use the integration branch defined in `AGENTS.md` or repository policy. If none is defined, treat `main` as the default integration branch. When remote delivery is in scope and remote access is available, fetch the remote integration branch and confirm its tip before creating a task branch or reusing an assigned checkout. Record the inspected base; if the remote tip cannot be checked, mark it unknown rather than treating the local branch as current.

Do not commit or push directly to the integration branch during ordinary task work.

Use the assigned branch and workspace when they exist.

Use one short-lived branch for one reviewable task.

Use `agent/<task-id>-<short-slug>` when the task has an identifier.

Use `agent/<short-slug>` when the task has no identifier.

Use one active writer for one workspace.

Use separate worktrees for concurrent writers.

Keep independent tasks on separate branches.

Never discard work from another task.

Do not use `git reset --hard` without explicit authorization.

Do not use `git clean -fd` without explicit authorization.

Do not use `git push --force`.

Use `--force-with-lease` only for an explicitly authorized history rewrite.

## 2. Change discipline

Implement the requested behavior and necessary support changes.

Avoid unrelated refactoring, formatting, and dependency changes.

Change a lockfile only when a required dependency change changes it.

Stage only files that belong to the task.

Do not use `git add -A` in a shared or dirty workspace.

## 3. Commits

Use Conventional Commits 1.0.0.

Use this format:

```text
type(scope): imperative description
```

Allowed types are `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, and `revert`.

Use a short scope when it improves meaning.

Start the description with a lowercase imperative verb.

Do not end the subject with a period.

Keep the complete subject at or below 72 characters.

Use a commit body when the reason or tradeoff needs explanation.

When a delegated node produced the change, add the trailers `Node: <task_name>` and `Evidence: <log or packet path>`.

Use `Refs: TASK-123` when a task identifier exists.

Mark a breaking change with `!` and a `BREAKING CHANGE:` footer.

Use the configured agent identity.

Do not impersonate a human author or reviewer.

Before each commit, run:

```text
git status --short
git diff --check
git add -- <explicit-paths>
git diff --cached --check
git diff --cached
```

Review the staged diff before the commit.

## 4. Pull requests

Push only the task branch.

Use one pull request for one coherent change.

Use a Conventional Commit title.

Include the task, summary, validation results, risks, and rollback notes when they apply.

Identify schema, migration, compatibility, and feature-flag changes.

Do not approve your own work.

Do not bypass required reviews, CI checks, or branch protection.

Use the configured merge method and merge queue.

## 5. Candidate acceptance and delivery

The coordinator owns delivery. Remote pushes, publication, and other remote
mutations require explicit authorization under `AGENTS.md`. When delivery is
authorized, keep pre-merge candidate acceptance separate from delivery and
cleanup:

- The pre-merge candidate record ends with review and verification evidence for
  one identified candidate head. Validate its schema-3 graph before accepting
  that candidate. A changed head requires a new candidate review and affected
  checks to be rerun.
- A repository change is complete only after the accepted head is merged to the
  remote integration branch and that merge is observed. A local commit or local
  merge alone is incomplete; report any blocker that prevents remote completion.
- Pass the accepted reviewed head and candidate validation evidence as named
  inputs to a separate schema-3 delivery record. The delivery flow records the
  head-checked merge (or merge-queue result) before cleanup. Capture the PR URL
  and resulting merge commit when available. Do not start cleanup while a
  merge is queued or unobserved.
- Bind the accepted candidate to its exact commit SHA, tree SHA, and inspected
  base SHA. Record the GitHub PR head SHA, merged state/time, reported merge
  commit SHA, and observed remote integration branch SHA as separate evidence.
  Require exact PR-head equality with the accepted commit; a matching tree does
  not make a different commit equivalent. Verify the accepted base is an
  ancestor of the candidate. The PR base ref must name the expected integration
  branch; its base SHA may have advanced since candidate review and is not the
  reviewed base identity. Recheck the live remote integration branch SHA at
  validation time, and verify that branch contains the reported merge commit.
  If the branch moved since observation, refresh the observation and repeat
  this integration check before acceptance. `scripts/verify_delivery.py` performs these
  read-only checks from accepted candidate JSON (`commit`, `tree`, `base`), a
  GitHub PR JSON response, and observed remote-ref JSON (`name`, `sha`).
- Give each delegated node an A/E/R subgraph with named inputs, outputs, owner,
  and exact verification argv. After it returns, compare the implemented A/E/R
  with the assigned subgraph before accepting its outputs or starting a
  successor. Use schema 3 for delegated writes and multi-dependent work; a
  single eligible read or routine command can carry A/E/R inline. Every
  delegated write requires independent review and observed checks.

Mimir's current `scripts/factory` snapshots `HEAD` and rejects a node when
`HEAD` changes during that node. Do not run a merge inside a regular factory
`run` node. Until the controller supports a Git-transition observation, record
the authorized merge command and its result separately, then initialize a
post-merge schema-3 record with the observed merge result as a named input for
trunk verification and cleanup. Do not claim that this post-merge record
observed the merge itself.

## 6. Post-merge cleanup

After the merge is observed, verify that the integration branch contains the
reported merge commit. For squash merges, confirm the host reports the PR as
merged and that the merged PR covers the reviewed head.

Delete a task-owned remote branch only after checking that it points to the
reviewed head and has no dependent PRs. Return the local checkout to the
integration branch and fast-forward it only when safe. Remove the local task
branch or task-created worktree only after confirming it has no unrelated or
uncommitted work. Preserve it and report why if cleanup could discard work or
affect another task. Create tags only when the task explicitly authorizes a
release or tag.

Check local and remote refs after cleanup. Confirm the task branch is absent on
both, or report the exact cleanup blocker. For older branches, verify their tip
against a merged PR and check for worktrees and dependent PRs before retiring
them.

## 7. Completion report

Report the task identifier when it exists.

Report the branch and final commit SHA when commits exist.

Report the pull-request link when it exists.

Report validation commands and results.

Report known risks and outstanding work.

Report merge or deployment status when you know it.
