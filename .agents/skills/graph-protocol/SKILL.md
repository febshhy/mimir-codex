---
name: graph-protocol
description: Delegate bounded multi-agent work as typed task graphs using A, E, R, with structure at boundaries and comparison on return.
---

# Graph Protocol — canonical orchestration skill

The original ten-section method in `references/PROTOCOL.md` is authoritative. Read it before designing multi-agent work. `references/V3-CONTRACT.md` is only the mechanical representation; it cannot override the original method.

**Scope of graph authority:** A/edges express task flow and named worker outputs; E covers delegation breakpoints; R covers the worker's subgraph, method, verification and WHY. These are *execution/delegation* requirements, not approved product requirements or domain invariants. Take business behavior from `$requirements` and domain/UI/database contracts from their owning methods (`AGENTS.md`). If a worker discovers an unresolved product policy, report it to the coordinator for the requirements Question Gate; do not settle it by rewriting the task graph. Shared words such as "happy path" and "dependency" do not transfer decision authority. Keep the original A/E/R structure unchanged.

**Execution-flow reporting:** Use the shared `AGENTS.md` **Call Graph Output** convention when showing delegation execution flows in a project overview, architecture summary or code explanation: plain-text `ts` fences, hierarchical indented `→` arrows, separate Production and Tests sections if different. A display trace is illustrative only; the required delegated/implemented A/E/R structures and schema-3 comparison remain authoritative.

1. Define task nodes, each node's single owner, and explicit data-dependency edges. Name the output carried by every edge (§1).
2. Draw A as the successful execution flow: independent nodes can run in parallel; a dependent node starts only after its required inputs are accepted (§2–3).
3. Mark E where handoff can fail through wrong context, missing input, or misinterpretation. The coordinator owns handoff quality and mitigations (§4).
4. Give every worker R: its assigned subgraph, applicable design method, verification command, inputs, and WHY (§5).
5. A small task may use one inline node, but it still uses A, E, and R. The prompt carries the planned subgraph; the worker returns the implemented graph with actual nodes, flows, breakpoints, and named output values (§6, §10).
6. **Trust nothing at the boundary. Trust everything inside.** The worker owns its subgraph until structured return; do not insert controller decisions into that work (§6, §8).
7. Record the plan before spawning. Collect controller observations around the work with `scripts/factory begin/end/run`; logs, leases, and receipts wrap the graph and are not task flow (§7).
8. Compare planned and returned nodes, flows, and breakpoints, then check verification before acceptance (§9). For delegated WRITEs, a different reviewer gathers diff/source/check evidence for coordinator review.

Use `scripts/factory init`, `prompt`, `begin/end/run`, and `validate`. The controller runs on Linux using Bash+jq; it needs no Python or Go runtime. Schema version 3 is mandatory. For a trivial single-agent task, keep the method but avoid an unnecessary multi-node execution graph.

For each delegated WRITE, include a bounded A/E/R assignment and use fresh agent context (`fork_turns: none`). A different Luna agent gathers diff/source/check evidence; the coordinating Sol agent independently reviews it and accepts only through the schema-3 factory gate. Do not equate a valid receipt with acceptance. When runtime understanding is needed, provide a source-derived `ts` Call Graph Output with the actual entry point and indented `→` calls; label unimplemented paths proposed and separate Production and Tests when they differ. Fixture validation of a hook is not live Codex runtime verification.

The Mimir PreToolUse hook checks the current model against launch target profile/model pairs and requires `fork_turns = "none"`; it routes controlled command/edit/write tools by current model. PreToolUse does not document a caller profile field, so the hook cannot identify the caller's agent profile. Fixtures use documented fields but do not establish live Codex runtime enforcement. The reviewer profile disables supported shell, app, plugin, memory, and permission-request capabilities; those flags do not prove a live sandbox.
