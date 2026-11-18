# Data contract: <producer → consumer>

Status / owner / reviewers:

Purpose, consuming decisions and accepted boundaries:

Record/field meaning; sample schema and **schema version**:

Identity, uniqueness and **one row/event represents**:

`occurred_at` / `effective_at` / `ingested_at`, timezone and clock policy:

Arrival mode (batch, API, CDC, event); expected volume, periodicity, watermark and latency:

Insert/update/delete/tombstone and correction behavior; ordering and duplicate/redelivery semantics:

Nullability, missing values, units, currencies, enumerations, encoding, compatibility rules:

Durability, retry/offset commit, replay horizon, backfill and retention:

Sensitivity classification, lawful use, access roles, minimization, deletion/opt-out propagation:

Consumer behavior for absence, staleness, partial load or incompatible version:

Quality assertions and measurable acceptance fixture:

Versioned change notice owner, rollout order, rollback and deprecation:

Known / Assumed / Unknown:
