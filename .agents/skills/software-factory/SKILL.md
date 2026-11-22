---
name: software-factory
description: Orchestrate software and data product delivery from a user goal through requirements, architecture, coding, independent review, tests and graph-based acceptance. Trigger for building, editing, debugging or refactoring software, data pipelines, metrics, dashboards and models.
---

# AI software factory — coordinator lifecycle

**Call graphs in handoffs:** When work or a finding depends on how code runs,
include or reference the relevant source-derived trace in assignments, returns,
and reviews. Follow **Call Graph Output** in the Mimir coordinator instructions
(`AGENTS.md` in the release or `.mimir/AGENTS.md` in an installed project).

**Authority:** only the main Codex agent orchestrates, schedules, integrates, and accepts; workers execute bounded nodes. Approved behavior stays with `$requirements`/reviewed `LAWS.bend`, domain and GUI contracts with their skills, verification with `$testing`, and delegated A/E/R with `$graph-protocol`. No worker approves new product policy.

## Sol/Luna agent workflow

Follow **Model ownership and scheduling** in the coordinator instructions.
Luna owns web search and operational tool calls. Sol dispatches ready work and
resumes on worker results or blockers. Use native notifications or a blocking
receive when there is no independent work. Keep status polling out of agent
coordination.

- GPT-6.2 Sol coordinates the task, decides material issues, and independently reviews changes.
- Delegate substantive routine work to GPT-6 Luna at the first eligible point, including read-only work and small fixes. Use `mimir_routine` with fresh context (`fork_turns: none`) and bounded A/E/R. Luna owns routine inspection, edits, commands, tests, Git, and monitoring through completion.
- When execution depends on a material decision, delegate fact collection to Luna, resolve the decision as Sol, and return execution to Luna. Record the specific blocker if no substantive Luna assignment is eligible.
- For every delegated WRITE, a different Luna agent collects diff, source, and check evidence. Sol reviews that evidence and accepts only through the schema-3 factory gate.
- If an agent needs execution context, provide a source-derived Call Graph Output with the real entry point and indented `→` calls in a `ts` block. Show Production and Tests separately when their wiring differs. Mark proposed paths as proposed; do not claim runtime verification from fixtures.
- A is the successful task flow: name each node's single owner and each output passed along an edge. Independent nodes may run in parallel; dependents start only after required inputs are accepted. E records handoff breakpoints (wrong context, missing input, misinterpretation) and coordinator-owned mitigations. R gives each worker its assigned subgraph, applicable design method, verification command, inputs, and WHY. A small task can use one inline node with the same A/E/R channels.
- The coordinator records the planned subgraph before spawning; the worker owns it until returning the implemented graph with actual nodes, flows, breakpoints, and named outputs. The coordinator compares planned and returned nodes, flows, and breakpoints and checks verification before acceptance. Logs, leases, and receipts wrap the graph as evidence; they are not task flow. Use a source-derived call graph in R context when runtime understanding is needed.

In the tracked Mimir clone, `.codex/config.toml` sets Sol as coordinator, enables multi-agent tools, and sets `sandbox_mode = "workspace-write"`, `approval_policy = "on-request"`, and `approvals_reviewer = "auto_review"`. The configured hook checks the current model against launch target profile/model pairings and requires `fork_turns = "none"`; it routes controlled command/edit/write tools by current model. PreToolUse does not document a caller profile field, so the hook cannot identify the caller's profile. The reviewer profile disables supported shell, app, plugin, memory, and permission-request capabilities, but those flags do not prove a live sandbox. Project installation retains model/routing hooks and agent profiles but omits those three approval keys from generated project config. This is a Mimir clone-scoped adaptation and does not claim to reproduce Heimdall's installer verbatim. Explain project/hook trust during setup. Desktop users choose **Approve for me** in the current chat where available. Fixtures exercise documented event fields but do not establish live Codex runtime enforcement.

```text
Inspect goal/repo → Retrieve authorized behavior
  → Classify direct | graph | critical
    → Discover/design only needed scope + unknowns
      → Tidy first | after | later | never (only if justified)
        → Delegate inline A/E/R OR plan DAG and delegate ready nodes
          → Verify (incl. independent review for delegated WRITE)
            → Compare planned and returned A/E/R + actual changes
              → Complete | Partial(reason) | Blocked(reason)
```

## Classification and design

- **Direct:** one eligible read or routine command → Luna with inline A/E/R. Sol handles coordinator decisions and necessary preflight or recovery.
- **Graph:** multi-module/dependencies or delegated WRITE → `$graph-protocol` schema-3 READ/RUN/WRITE DAG with explicit owners, named output edges, A/E/R prompts, file ownership and verification argv.
- **Critical:** auth, security, money, migrations, destruction, consequential correctness → stronger evidence, rollback/recovery and approval where required; not automatically more agents.

For data products include one source-to-consumer slice from `$data-slicing`; select `$data-lifecycle`, `$data-dimensional-modeling`, `$data-statistics`, `$data-decision-science`, `$data-storytelling` and `$data-operations` only as applicable. A pipeline DAG is not the worker DAG. Require producer/consumer compatibility and actual metric or prediction evidence across team boundaries.

Determine depth from impact if wrong, contract significance and existing detection strength (`AGENTS.md` selective audit). Use `$requirements` for material ambiguity, `$software-design-thinking` for domain structure, `$gui-design-thinking` for functional UI, `$visual-design` for presentation, `$content-writing` for substantive copy, `$evidence-research` for blocking external evidence, `$adr` for hard-to-reverse decisions. Keep unknowns explicit; no invented behavior or requirements. For structure use `$repository-work` tidy sequencing, bounded to the requested work; update governing design graph first when its contracts change.

## Delegated graph execution

```text
Plan A/E/R → scripts/factory init --plan <plan.json> --graph .work/graphs/<task>.json
  → ready? → prompt (planned subgraph) → begin / run → end --return (implemented graph) → independent reviewer
    → actual tests/diff → scripts/factory validate --graph <record>
```

Dispatch only ready nodes; a dependent node starts after its required inputs are accepted. READ/RUN use `run --return -- <argv>`; WRITE uses `prompt`, `begin` and `end --return`. Use `mimir_routine` for routine READ, RUN, and WRITE work; independent review uses `mimir_reviewer` when installed or separate `default` read-only reviewer. Check different identities and actual observations: a role label does not enforce independence. **Factory leases an entire Git worktree:** serialize nodes in one worktree, even disjoint files. Parallel WRITE requires prepared isolated worktrees, disjoint ownership and deliberate integration. Read `references/LIFECYCLE.md` for examples and critical release boundary.

## Selected Bend2 gate

```text
User-reviewed LAWS.bend (+ normative SPEC.bend assumptions)
  → model/proof WRITE → scripts/factory proof passes real law/proof pair
    → production WRITE → model-to-production conformance
      → integration/effect checks → final acceptance
```

Smoke proof never qualifies. Law or normative-assumption changes return to operator approval; do not silently replace failed formal verification with tests. If Bend unavailable or model cannot faithfully express selected scope, block or request explicit rescope. Other behavior uses ordinary approved requirements and tests.

## Acceptance and report

Run the actual applicable build/lint/tests and representative data/metric reconciliation or model evaluation when changed, inspect Git diff and independent delegated-WRITE review, then compare every planned node, flow, and breakpoint with the returned schema-3 graph. Reject missing evidence, contradicting observation, required but absent review, invalid graph, or failed checks. Graph comparison is not application correctness. Report changed paths, approved requirement coverage, executed commands/results, review/evidence, unresolved risks and approvals. Include source-derived call-graph slices when `AGENTS.md` requires them; mark stale/unverified evidence, use the project's inspected revision and keep logs in `.work/`. Never claim a command/proof ran without observation, delete required checks to save tokens, or copy full logs into worker prompts. `jq` is required by the controller; optional tools never change the A/E/R contract.
