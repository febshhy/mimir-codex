---
name: data-operations
description: Verify reliability, data quality, lineage, SLOs, reprocessing, migrations, privacy and operational recovery of pipelines, analytics and ML-serving systems.
---

# Data operations — observable quality and safe recovery

**Authority:** Operational checks and response for persistent data and derived products. `$testing` owns verification strategy; `$data-lifecycle` owns lifecycle layout; `$software-design-thinking` owns state/effect semantics; `$requirements` owns permitted impact.

## Define a real consumer contract

For important datasets/metrics/models, agree on: owner and escalation, schema and grain, integrity, completeness, validity, consistency, freshness, arrival lag, update/correction, allowed missingness, access/privacy, cost and retention, service objectives and what users see when stale. Choose high-value monitors; avoid global dashboards with no response owner. Do not invent thresholds: derive from known producer patterns and consumer needs, otherwise label them proposals.

## Failure matrix

| Failure | Detection | Response | Verify |
| --- | --- | --- | --- |
| Duplicate delivery | Grain/key uniqueness | Deduplicate/idempotent sink | Re-run produces same result |
| Missing / delayed source | Expected availability and watermark/lag | Mark stale, alert owner, replay once source returns | Reconcile covered interval |
| Schema break | Contract/version check | Quarantine incompatible payloads, coordinate producer | Compatibility fixture |
| Wrong joins or metric | Fanout/rate checks + trusted examples | Stop/suppress incorrect downstream claim, repair | Source-to-metric check |
| Partial write/replay | Checkpoint/commit audit | Recover or replay bounded window | Compare output to clean run |
| Unauthorized sensitive access | Permission/data-policy test and audit | Revoke, contain, investigate, remediate | Access retest and deletion proof where possible |
| Feature/model drift | Input, prediction and outcome metrics | Review impact, roll back/reroute, revalidate | Outcome vs baseline and subgroup checks |

Observe failures as **data correctness**, infrastructure health, and user-visible freshness separately. A completed job is not necessarily correct data. When historical recovery is unavailable, report lost scope explicitly; avoid invented exactly-once claims.

## Before release

Inspect migrations and dependencies; run version/compatibility tests; rehearse small backfill and retry; confirm restore point and rollback compatibility; check restricted access, retention and deletion propagation. For major changes, stage and compare old/new side by side with reconciliation before cutover. Do not delete source or old schema until consumers and rollback window are accounted for. Include data cost (compute/storage/egress), operational owners and intervention protocol. Record executed checks with actual revision, sample period and result.
