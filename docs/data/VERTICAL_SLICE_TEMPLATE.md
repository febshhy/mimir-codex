# Vertical data slice: <single user outcome>

Status: Proposed / Approved / Implemented / Verified / Partial

**Consumer / decision:** <person, action, business question>

**Value and acceptance:** <approved behavior and a numerically checkable known-answer fixture>

**Production/data lineage (source-inspected, proposed otherwise):**

```ts
<producer function / event>
  → <capture/job/checkpoint>
    → <modeled table and grain>
      → <metric, analysis, feature or model>
        → <dashboard, API or decision>
```

| Boundary | Contract (key, grain, times, version) | Owner | Failure/rollback | Handoff check |
| --- | --- | --- | --- | --- |
| Producer → landing | | | | |
| Landing → model | | | | |
| Model → metric / feature | | | | |
| Product → consumer | | | | |

**Engineering contracts/invariants:** <apply eight-principle core; link advanced application state/effects reference only when relevant>

**Statistical limits/decision approval:** <or N/A with reason>

**Privacy, retention, consent and audience:**

**Plan for late, duplicate, corrected and deleted data:**

**Tests:** <reconciliation query, replay, compatibility, actual results and inspected revision>

**Known | Assumed | Unknown | Blocked:**
