# Advanced stateful-application walkthrough

**Optional reference for stateful services, transactional producers and production ML serving.**

Use [Engineering Foundations](../.agents/skills/software-design-thinking/SKILL.md) for the core design questions and the [data playbook](DATA_PLAYBOOK.md) for grain, lineage, statistics, and cross-team delivery.

[Engineering foundations](ENGINEERING_PLAYBOOK.md) · [Mimir overview](../README.md) · [Data playbook](DATA_PLAYBOOK.md)

## Advanced stateful application walkthrough

For a stateful application with important external effects, six questions make a useful deeper analysis:

```text
1. CONTRACT     What must the system guarantee? Who approves it?
      ↓
2. MODEL        What are the valid data shapes, states, and transitions?
      ↓
3. DECISION     Given state and input, what result should follow?
      ↓
4. BOUNDARY     Who owns state and executes external effects?
      ↓
5. RECOVERY     What happens on failure, duplication, and interruption?
      ↓
6. EVIDENCE     What check supports each important claim?
```

Start with the contract, then define the state, effect owners, failure handling, and verification the workflow needs.

### A running example: report exports

Assume a product owner has approved these **illustrative** requirements:

- An authorized person can request an asynchronous CSV export of a report.
- A person must be authorized when requesting **and downloading** an export.
- Repeating the same request with the same idempotency key must not create a second export job.
- A job can finish successfully or report a failure. A client can inspect its status.

## 1. Contract — define success before structure

**Basis: design by contract and requirements traceability.** The product contract defines observable obligations. The implementation explains *how* they hold; the implementation is not the authority that invents them.

Separate four kinds of knowledge:

| Status | Meaning | Example |
| --- | --- | --- |
| Known | Approved requirement or inspected fact | An export request needs authorization. |
| Unknown | Missing answer that changes correctness | Does permission revocation invalidate an already-generated export? |
| Assumption | Explicit, unapproved working premise | Exports will be generated asynchronously. |
| Decision | An authorized choice made after comparison | Reuse the application's existing job table. |

For each obligation, describe a condition that can be observed or checked:

```text
C1: Unauthorized actors cannot create a report export.
C2: Unauthorized actors cannot download an export artifact.
C3: (same actor, same key, same request) → same job identity.
C4: (same actor, same key, different request) → conflict.
```

Agree on the meaning and owner of each contract before implementation. For C3, define the idempotency key scope and request fingerprint.

**Apply it:** Trace every entry point that can create or deliver an export: API calls, background jobs, downloadable links, and other real paths found in the source. Record uncertain paths as unknown. Ask for a product decision where the uncertainty changes an observable result.

**When to stop:** Do not choose a data model to resolve a missing product rule. Return the question to the requirement owner. See [`$requirements`](../.agents/skills/requirements/SKILL.md).

## 2. Model — types, invariants, and state machines

**Basis: algebraic data types, state invariants, and finite-state transition systems.** Types describe possible values; invariants constrain valid states; a transition function describes allowed changes.

Use distinct types for distinct meanings, even when their storage representation looks alike:

```text
ActorId ≠ ReportId ≠ JobId ≠ ArtifactRef

ExportStatus =
    Queued
  | Running(AttemptId)
  | Ready(ArtifactRef)
  | Failed(Reason)

ExportJob = {
  id: JobId,
  actor: ActorId,
  report: ReportId,
  status: ExportStatus,
  version: Version
}
```

A **sum type** (variant) makes mutually exclusive states explicit. It avoids combinations such as `isReady = true` and `isFailed = true`. In a language without native variants, enforce the same rule with constructors, validation, and focused tests.

An **invariant** is a predicate that every reachable valid state must satisfy:

```text
Inv(job):
  job.status = Ready(ref) → ref identifies a recorded artifact
  job.status = Running(a) → a is an identified processing attempt
```

Do not assume a type declaration guarantees the first rule. An external artifact may disappear even when `Ready(ref)` is well-typed; persistence and integrity checks are still required.

A **state machine** makes legality explicit:

```text
Queued  --Claim-->     Running
Running --Complete-->  Ready
Running --Fail-->      Failed
```

Transitions not listed are rejected or deliberately ignored according to the contract. An interrupted `Running` job needs a recovery policy before production use; the graph above describes normal transitions only.

A state machine can be written as `δ : State × Event → State | Error`. A stronger version makes the required context and requested effects explicit.

**Apply it:** List every datum that survives a function call. Assign it to input, domain state, or an owned resource. Identify illegal combinations and all legal state transitions before introducing classes or database tables. See [`$software-design-thinking`](../.agents/skills/software-design-thinking/SKILL.md).

## 3. Decision — functional core, typed errors, and effects

**Basis: referential transparency, explicit data flow, and result-based error composition.** A decision is easiest to test when identical inputs produce identical outputs. Database calls, clocks, randomness, and networks belong outside that decision.

The **Functional Core / Imperative Shell** pattern separates these two responsibilities:

```text
Input + trusted facts + State
              ↓
          decide(...)
          /       \
 Ok(NewState, Effects)  Err(DomainError)
          ↓
   Imperative shell
          ↓
 Persist / send / schedule → typed observation → next decision
```

A language-neutral signature is:

```text
decide : (State, Command, Facts) → Ok(State', Effect*) | Err(Error)
```

`Facts` includes any current time, authorization result, or external response the decision requires. The shell obtains those facts from the appropriate boundary. No hidden database connection or ambient clock is read inside `decide`.

**Railway-oriented programming** describes composing operations that have success and failure paths. `Result<Success, Error>` or `Either<Error, Success>` makes an expected failure part of a function's output. A later success-only step runs only when the earlier step succeeded.

```text
parse request
  → Ok(parsed)     → validate input → Ok(command) → decide
  → Err(BadInput)  ──────────────────────────────→ respond with error
```

Represent expected domain failures in the result and surface unexpected defects separately.

**Effects as data** allow the core to request an action without executing it:

```text
Effect = SaveJob(job) | RecordAudit(event) | ScheduleWork(jobId)
```

Effect declarations must include meaningful ordering and durability requirements. For an accepted export, the database transaction must commit the job and its duplicate-key record before the API reports that the request was accepted. A separate queue is optional: an existing database-backed worker can claim queued jobs.

**Apply it:** Extract a pure decision only when it contains meaningful rules. A trivial wrapper around a database call does not need a new functional-core abstraction. See the [effects and recovery reference](../.agents/skills/software-design-thinking/references/EFFECTS-AND-RECOVERY.md).

## 4. Boundary — dependency inversion, ownership, and modules

**Basis: dependency inversion and information hiding.** The stable policy defines what it needs; the volatile implementation supplies it. An interface is useful when it hides a meaningful external, ownership, failure, security, or replacement boundary.

```text
Export policy / decision
   ├─ needs: current access decision
   ├─ needs: stored job snapshot
   └─ emits: requested effects
                     │
               imperative shell
                 ├─ authorization service
                 ├─ job repository
                 ├─ CSV generator
                 └─ artifact storage
```

The dependency direction is conceptual: **the domain's needs should not be determined by one storage or network client API**. Ports and adapters are one implementation technique. A function parameter, an ordinary module, or an existing application interface can be sufficient.

### One owner per mutable resource

A useful ownership rule is:

```text
For each mutable resource r: |Owner(r)| = 1
```

For the export example, the job repository is the single writer for the durable job record and the database enforces its transactions; a worker owns its identified processing attempt; artifact storage owns the stored bytes. Request handlers issue commands rather than maintaining another authoritative job copy. Shared ownership requires explicit coordination and consistency rules.

**Information hiding** means the public module contract stays small while the implementation absorbs complexity. Keep the transaction, deduplication, and job-claim mechanics behind an operation meaningful to callers. Delete pass-through layers that add no contract.

**Design for change:** Name a plausible change before adding abstraction. For example, if artifact storage may change independently, a stable storage port may help. If there is one simple call and no meaningful boundary, wrapping it in several interfaces increases maintenance cost.

**Tidy First?** separates structural cleanup from behavior change. Tidy before when a small rearrangement lowers immediate risk; tidy after when new behavior clarifies the structure; postpone or omit when the benefit is unclear. Preserve separately checkable evidence of behavior where the change matters.

**Apply it:** Draw the direction of dependencies, identify the owner of each persistent resource, and explain why every new abstraction exists. See [Mimir's design integration reference](../.agents/skills/software-design-thinking/references/MIMIR-INTEGRATION.md) and [`$repository-work`](../.agents/skills/repository-work/SKILL.md).

## 5. Recovery — design for duplicate and uncertain outcomes

**Basis: distributed failure semantics, idempotency, and concurrency control.** An operation can succeed remotely even when the caller receives no response. A timeout alone does not prove failure.

```text
Effect attempt
  ├─ ConfirmedSuccess(value) → advance state
  ├─ ConfirmedFailure(error) → translate / recover / fail
  └─ UnknownOutcome(opId)    → inspect / reconcile before retry
```

### Idempotency

For an operation identified by key `k`, the intended externally visible effect of repeating the same valid request should match that of one request. This is a semantic contract, not merely a retry loop.

For report exports, define:

- Key scope: `(actor, key)` or another approved scope.
- Fingerprint: canonical report identity and material export parameters.
- Duplicate rule: same fingerprint returns the same job; conflicting fingerprint is rejected.
- Persistence: a database uniqueness constraint or equivalent **atomic** mechanism prevents concurrent duplicates.
- Retention: the system defines when keys expire and what happens afterward.

Creating one job does **not** imply that the worker executes exactly once. Worker retries, process crashes, and storage uploads can cause repeated attempts. Design artifact names, cleanup, and commit transitions accordingly.

### Concurrency and recovery

Two workers can claim the same queued record unless the claim is atomic. Use an appropriate database transaction, conditional update, version check, or queue lease already supported by the system.

```text
Claim(jobId, expectedVersion)
  → success: one worker owns this attempt
  → conflict: read fresh state; do not run the stale attempt
```

An interrupted attempt needs lease expiry, reconciliation, or a deliberate manual recovery path. Define what happens when a job completes but the worker crashes before recording `Ready`. Retry only when failure is plausibly transient and repeating the operation is safe; bound attempts and elapsed time, with one owner of the retry policy.

For each expected error, choose an explicit strategy: propagate, translate, recover, or retry. For a durable database change plus outgoing message, a **transactional outbox** can prevent losing the intent to send. It adds storage, delivery, deduplication, and operations work; use it only when the problem requires it. Compensation, cancellation, and retries also need explicit ownership. In particular, cancellation does not reverse an already committed remote effect.

**Apply it:** Test concurrent duplicate requests, lost responses, late results, process restart, and partial completion. Prefer the simplest recoverable design supported by the existing stack. See [concurrency](../.agents/skills/software-design-thinking/references/CONCURRENCY.md) and [effects and recovery](../.agents/skills/software-design-thinking/references/EFFECTS-AND-RECOVERY.md).

## 6. Evidence — verify the claim you intend to make

**Basis: the distinction between a specification, an observation, and a proof.** Every important claim needs an appropriately scoped check.

| Claim | Useful verification | What it establishes |
| --- | --- | --- |
| Denied actors cannot create jobs | Contract/boundary tests for denied cases | The tested authorization paths reject them. |
| Illegal job transitions are rejected | Unit or property tests over states/events | The model preserves the tested transitions and invariants. |
| Same key produces one job under races | Concurrent requests against the real database | The observed transaction/uniqueness behavior. |
| Download rechecks access | Integration test through the real download boundary | The tested access rule at delivery. |
| Interrupted work can resume safely | Restart and recovery exercise | The exercised failure scenario. |
| A formal law holds for a Bend model | Actual reviewed `LAWS.bend` and verified `PROOF.bend` | The stated property for the checked model and assumptions. |

Verify storage transactions against the actual storage system.

Testing is most useful when linked to the original claim:

```text
Approved contract → Design invariant → Implementation boundary
                                            ↓
                                      Executed check
                                            ↓
                                   Observed result + scope
```

**Formal verification** is a separate, optional mechanism. Where a pure invariant can be modeled faithfully, Mimir uses reviewed `LAWS.bend`, a model, and `PROOF.bend`. The approved law specifies the selected behavior; the proof addresses the model; production conformance still needs verification.

**Apply it:** Report passed, failed, inconclusive, and not-run checks with their actual scope. Link claims to evidence at the inspected revision. See [`$testing`](../.agents/skills/testing/SKILL.md) and the [Bend proof guide](../proofs/README.md).

## 7. Apply the foundations to specialized work

Apply the relevant domain method to each specialized task.

| Work | Primary foundation | Additional questions | Skill |
| --- | --- | --- | --- |
| User interfaces | State + decisions | Who owns draft, focus, URL, loading, and error state? Can every reachable event be handled? | [`$gui-design-thinking`](../.agents/skills/gui-design-thinking/SKILL.md) |
| Databases | Ownership + recovery | What is the workload, authoritative fact, transaction boundary, migration, and restore strategy? | [`$database-design`](../.agents/skills/database-design/SKILL.md) |
| Security | Contracts + boundaries | Which actor is authorized at each entry point? What is the actual trust boundary? | [`$software-design-thinking`](../.agents/skills/software-design-thinking/SKILL.md), [credential boundary](../docs/security/CREDENTIAL_BOUNDARY.md) |
| Coordinated agent work | Dependencies + evidence | Which tasks truly depend on others? Who owns each write, and who independently reviews it? | [`$graph-protocol`](../.agents/skills/graph-protocol/SKILL.md), [`$software-factory`](../.agents/skills/software-factory/SKILL.md) |
| Architecture decisions | Contract + change cost | What alternatives were considered, and what would make the choice worth revisiting? | [`$adr`](../.agents/skills/adr/SKILL.md) |
| Research | Known / unknown + evidence | What claim needs a source? What conflicts or uncertainty remain? | [`$evidence-research`](../.agents/skills/evidence-research/SKILL.md) |
| Writing and visual design | Reader contract + state | What must the person understand or do? Does presentation match actual behavior? | [`$content-writing`](../.agents/skills/content-writing/SKILL.md), [`$visual-design`](../.agents/skills/visual-design/SKILL.md) |

## Work the example from end to end

A small export implementation can follow this sequence:

```text
Approved export contract
  → Trace actual request, worker, and download entry points
  → Model JobState and legal transitions
  → Parse request and check authorization at the real boundary
  → Pure decision: accept, reuse key, reject, or request job creation
  → Database transaction: create one durable queued job per scoped key
  → Worker atomically claims job; generates and records artifact
  → Download rechecks authorization and serves a recorded artifact
  → Tests cover acceptance, denial, duplicates, races, interruption
  → Report observed results, unknown outcomes, and uncovered paths
```

A useful **first vertical slice** is request → durable queued job → status lookup, with a denied-case test. Then add worker completion, download authorization, and recovery. Each increment should leave a useful, testable behavior. Avoid introducing a message broker, workflow engine, or secondary database unless the actual workload justifies one.

### A conditional stateful-application worksheet

Use these questions only when the task benefits from explicit application state/effect modeling:

1. **Contract:** What must be true, who approved it, and what remains unknown?
2. **State:** What data persists? What are the legal states and invariants?
3. **Decision:** Which rules can be expressed as pure inputs → result?
4. **Boundary:** Who owns each mutable resource and performs each effect?
5. **Recovery:** What if an operation fails, runs twice, arrives late, or stops midway?
6. **Evidence:** Which real check supports each important acceptance claim?
7. **Change cost:** Is this the smallest design that meets the need? How will it be maintained or reversed?

For a one-line change, answer briefly. For an authorization or payment workflow, write down the state graph, ownership, failure outcomes, and checks before editing.

## Further reading and original sources

These sources explain the foundations behind the method. Mimir's linked skills above define its specific operational rules.

- [David Parnas, *On the Criteria to Be Used in Decomposing Systems into Modules* (1972)](https://doi.org/10.1145/361598.361623) — information hiding and module boundaries.
- [Gary Bernhardt, *Boundaries* (2012)](https://www.destroyallsoftware.com/talks/boundaries) — simple values, isolation, and functional/imperative boundaries.
- [Scott Wlaschin, *Railway Oriented Programming*](https://swlaschin.gitbooks.io/fsharpforfunandprofit/content/posts/recipe-part2.html) — explicit success/failure composition.
- [Martin Fowler, *Patterns of Enterprise Application Architecture*](https://martinfowler.com/eaaCatalog/) — domain, service, and persistence patterns.
- [Klaus Iglberger, *C++ Software Design*](https://www.oreilly.com/library/view/c-software-design/9781098113155/ch01.html) — dependencies, abstraction, testability, and design for change; principles apply beyond C++.
- [Kent Beck, *Tidy First?*](https://www.oreilly.com/library/view/tidy-first/9781098151232/) — evaluating and timing structural changes.
- [RFC 9110, §9.2.2: Idempotent Methods](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2) — the precise HTTP meaning of idempotency.
- [Amazon Builders' Library, *Making retries safe with idempotent APIs*](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) — client-request identity, duplicates, and retry behavior.

[Install Mimir](SETUP.md) · [How Mimir works](HOW_IT_WORKS.md) · [Return to README](../README.md)
