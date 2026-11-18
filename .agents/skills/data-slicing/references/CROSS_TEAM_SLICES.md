# Cross-functional vertical slicing — engineering method

This is **Mimir's integration guidance**, informed by Engineering Foundations, optional advanced application design, Graph Protocol and the five book-informed data methods. It is not an attributed framework or quotation from any one book.

## Separate three graphs

1. **Application/domain graph** (`$software-design-thinking` when applicable): command → decision → effect → result, with state and failures where needed. This is optional for read-only analysis and authoritative for modeled application behavior when used.
2. **Data lineage/semantic graph** (`$data-lifecycle` + modeling): producer → ingest/transform → fact/metric/feature → analysis or action, with grain, time, source and version at each edge.
3. **Work delegation graph** (`$graph-protocol`): A/E/R nodes and named outputs, ownership and verification, with `scripts/factory` evidence gates when delegated WRITE is used.

Never confuse the data DAG with a delegation DAG. A pipeline can be logically correct but assigned to the wrong teams; a task graph can pass validation while a sum is double-counted. Both need independent checks.

## Slice design algorithm

1. **Value:** name consumer, specific decision/action, expected value or accepted KPI and time horizon. Retrieve approved policy; do not manufacture target values.
2. **Thin path:** trace actual producer, transport, transformation, store, metric/model and surface; mark missing paths unknown.
3. **Choose one grain and timeframe:** select one use case/entity cohort, one trusted source, a short but representative history, one business metric and one consumer. Add cases only to control high-risk variation.
4. **Name cross-boundary contracts:** event schema/version; IDs, timestamp semantics, deletes and corrections; historical grain/key conventions; exact numerator/denominator; model cutoff if any; access classification and retention. Attach a named owner and test to each.
5. **Model failure:** delayed, duplicated, missing, malformed, revised and out-of-order source; stale feature; partial deploy; backfill/replay; wrong denominator; dashboard cache; redacted access. Decide when to stop serving vs mark stale vs fallback. Keep irreversible business actions behind approval.
6. **Deliver and observe:** full thread with a minimal fixture and known answer, source-to-consumer reconciliation, freshness/volume/quality signal, failure alarm owner and recovery procedure.
7. **Expand horizontally:** add more process rows to the bus matrix, cohorts/metrics, batch windows or predictions only after the first slice is trusted.

## Example: one revenue KPI from a software product

**Proposed scope:** daily captured revenue (not bookings, invoiced or recognized revenue). The product owner must approve meaning; no prior approval is assumed.

```ts
Application payment-captured transaction
  → outbox event(payment_id, order_id, amount_minor, currency, captured_at, version)
    → durable consumer + offset checkpoint
      → dedupe payment_id and track corrections/refunds as distinct event semantics
        → fct_payment_captured (one payment capture per row)
          → metric captured_revenue by defined local business day and currency
            → dashboard with numerator, label, last refreshed, lineage and source reference
```

Handoffs: app owner verifies transactional outbox and version compatibility; DE owner verifies replay/dedupe and lag; analytics owner verifies currency/timezone, grain and reconciliation; dashboard owner validates display, stale state and access; QA/reviewer validates sample source row through served measure. For net revenue, refund events and policies require a **separate** approved slice. Cross-currency aggregation requires a conversion policy; do not guess one.

Example joint fixture: source has payment A=100 and B=200 (same currency/day), duplicated A delivery and one late event. Expected analytic capture = 300 only after B arrives, with explicit freshness indicator before that. A source correction or refund does not silently mutate the meaning of captured revenue. Verify full replay gives the same answer; test source schema v1/v2 and downgrade compatibility.

## Example: customer-contact prediction slice

```ts
Approved outreach decision and costs
  → source account/consent + activity snapshots (point-in-time)
    → versioned features, training examples and labels
      → baseline + candidate model with time/group holdout
        → calibrated score, threshold and human-review action
          → recorded action and randomized/no-contact holdout if causal value is sought
            → monitored impact, drift, opt-outs and rollback
```

A model can be useful as an **offline exploration** without production serving; use a smaller slice in that case. Do not promote to automatic interventions on predictive accuracy alone. If the producer has no reliable historical snapshot, block claims of historical backtest validity until an alternative design is reviewed.

## Example: business question without a new pipeline

If the existing trusted warehouse already answers a question, the slice can be **query → data validation → statistical inference → annotated chart → decision**. No streaming service, data platform migration or feature store is necessary. Keep software tests for queries and computational logic; keep analyst review for meaning and inference.

## Example work DAG, when delegation actually helps

```text
wave 1: READ producer shape + READ existing metric lineage
   → gate documented contract and unknowns
wave 2: WRITE producer compatibility + WRITE versioned ingestion in isolated worktrees (only if independent)
   → gate integration schema and replay fixture
wave 3: WRITE dimensional fact + semantic metric
   → gate grain/reconciliation
wave 4: WRITE dashboard or scoring consumer + end-to-end check
   → independent review + factory validate
```

An illustrative, schema-3-valid [cross-team plan](../PLAN_DATA_EXAMPLE.json) shows the producer → landing → metric → independent-review sequence. Its file paths and commands are placeholders: replace them after inspecting the actual project. The scheduler must still obey schema-3 delegated/implemented A/E/R, only one active node per worktree, explicit output edges and independent review. A parallel plan is optional; direct single-agent work is preferred for small changes.
