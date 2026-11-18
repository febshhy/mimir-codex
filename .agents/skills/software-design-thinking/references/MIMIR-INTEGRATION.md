# Mimir integration — project-specific extensions

The default method is the eight-principle [Engineering Foundations](../SKILL.md). This reference adds Mimir-specific procedures; apply them only when the trigger fits. For complex stateful application behavior, use [advanced application design](ADVANCED-APPLICATION-DESIGN.md) selectively rather than imposing its 15 sections on routine data work.

## Requirements, artifact and design depth

- Link applicable requirement IDs from `$requirements` and any accepted ADRs. For requirements or decisions not yet resolved, mark Known / Unknown / Assumption / Decision; never invent identifiers.
- Treat approved product behavior as input to engineering design, not as a policy it may amend. Derive applicable data invariants, calculations and, where needed, commands and effects; if a proposed invariant implies a new business rule or contradicts the approved contract, return the question to `$requirements` before committing to the affected design. Do not convert an implementation preference into a requirement.
- Dependency vocabulary is shared but authority is not: the domain method owns logical/resource dependencies, `$database-design` owns their persisted implementation, and `$graph-protocol` owns worker/task dependencies. Its `R` is a worker prompt completeness check, not a product requirement. See `AGENTS.md` for the authority map.
- Default output is a fit-for-purpose note: outcome, contracts, flow, correctness rules, relevant failures, owners/handoffs, checks and unknowns. A module-level `AGENTS.md` under `## Design` may be required for substantial module changes; it is a *project recording format*, not a mandatory data-analysis artifact. If a brief module card cannot contain the explanation, link to the detailed design. A 60-line card limit is a review heuristic, not a reason to delete important constraints.
- A module card, when useful, may record `Requirements`, `Depth`, `Language`, `Depends on`, `Volatility`, `Shapes`, `Invariants`, `Flow`, `Errors`, `Needs/Owners`, `Claims`. Do not force absent categories into fabricated content. `Depth: small` can be shorter.
- `Depends on: X -> conform` means the module adopts X's contract; `translate` means it maps X at a real boundary. Give each shared shape an owner. Treat volatile dependencies with care.

## Change boundaries and coupling

- For Level 3 application changes, prefer a cohesive module with a modest public interface, meaningful hidden behavior and stable contract. A single implementation may merit an interface at a real boundary. Delete pass-through wrappers that add no contract or responsibility; do not impose these structures on simple SQL and notebooks.
- Audit duplicated rules, repeated parameter groups, scattered small changes, misplaced owners, hubs and dependencies on volatile modules. A high fan-in module can be legitimate when stable and narrow.
- Classify consequential decisions by reversal cost. For difficult-to-reverse data, public contracts, or destructive operations, record an ADR and a migration/rollback strategy; use `$software-factory` critical handling when applicable.
- When updating persisted data or public interfaces, prefer staged expand → migrate → contract with explicit compatibility windows, measurement and rollback/recovery plans where feasible. Do not presume all changes can be reversed after data loss.

## Evaluate consequential structure decisions

Use this evaluation only when a structural choice materially affects dependencies,
contracts, testability, future changes, or reversal cost; do not create a design
exercise for routine local edits.

- Name the concrete current requirement and credible change scenarios. Distinguish
  observed change pressure from speculation; optimize for the current need unless
  a future change has sufficient evidence or impact.
- Compare the existing/simple design with the smallest useful alternative. Inspect
  which responsibilities change together, coupling across ownership boundaries,
  cohesion, and whether a dependency belongs to a stable contract.
- Introduce an interface or indirection for a real behavioral, ownership, security,
  failure, or independently replaceable boundary. Multiple implementations are not
  a prerequisite, and anticipated reuse alone is not enough.
- Check whether a proposed abstraction preserves substitutability: inputs,
  outputs, errors, ordering, effects, resource ownership, and other applicable
  observable promises. Evaluate verification cost, operational complexity,
  maintenance, migration, and reversibility alongside implementation effort.
- Prefer the smallest justified solution. Record material alternatives and their
  tradeoffs in the existing design artifact or an ADR only when the ADR trigger
  applies; never invent historical rationale. The eight-principle core remains
  authoritative; advanced state/effect modeling is conditional.

## Premortem, security and compatibility

- For a consequential design, name credible analytical or production failures and map each to a data/behavior invariant, response strategy, verification check or accepted risk.
- At real trust boundaries, examine spoofing, tampering, repudiation, disclosure, denial/exhaustion and privilege escalation where applicable. Record durable findings in project-owned `docs/security/` if it exists.
- Public APIs can have undocumented consumers. Inspect usage, versioning, error behavior, ordering and timing before changing an observable contract. Never silently change another owner's model.

## Verification and optional formal proof

- Link claims to appropriate checks through `$testing`. Depending on the work, use known-answer fixtures, reconciliation, data-quality tests, temporal validation, statistical checks, holdouts, behavioral/property tests or real boundary checks. Property-based/generated-sequence tests are valid for state machines, parsers and invariants **without Bend**; avoid redundant cases.
- If Bend is explicitly enabled and a particular pure invariant is selected for proof, follow `$bend-proof` proof-first order and conformance tests against production. Formal proof of a model does not prove production implementation; ordinary tests do not prove every execution.
- Prototype thin end-to-end slices early where safe; preserve proof-first order only for selected formal models. Update affected data/contract/state graphs when a new fact changes the design; do not require an application graph for a read-only query.

## Call graph presentation

For project overviews, architecture summaries, code explanations and displayed execution traces, follow `AGENTS.md` **Call Graph Output** when showing a call path: a plain-text `ts` block with indented `→` steps, plus separate Production and Tests sections when they differ. Derive paths from actual code and tests or mark them proposed/unknown. Format does not prove correctness. Trace data lineage for data workflows; model detailed state and effect graphs only when needed.

## Separation from GUI

`$software-design-thinking` owns general correctness, domain contracts and applicable application commands/effects. `$gui-design-thinking` owns surfaces, human moves, view/navigation state, focus and UI effects. Map a UI event to a domain command through an explicit boundary, and map the typed outcome back to a UI event. Do not conflate `Submitting` (UI) with `Paid` (domain). `$visual-design` presents the GUI contract without modifying its transitions.


## Cross-functional data delivery (Mimir extension)

Use the Level 3 advanced reference **when** a data request introduces consequential state transitions, multi-writer coordination, external effects or complex API/service failure semantics. For source-to-consumer work use `$data-slicing` for cross-team contracts; `$data-lifecycle` owns data movement, `$data-dimensional-modeling` analytical grain, `$data-statistics` inference and `$data-decision-science` model decisions. Graph Protocol remains a worker-delegation plan rather than the dataflow graph. Use a business-meaningful thin slice with a known-answer check and representative failure/replay case **when relevant**.
