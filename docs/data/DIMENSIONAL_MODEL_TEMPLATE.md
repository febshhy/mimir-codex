# Dimensional model: <business process>

Approved question/consumer and accountable definition owner:

Bus matrix link / conformed dimensions and facts:

**Grain:** one row represents exactly <...>

| Fact / measure | Meaning and units | Additivity | Allowed aggregation | Evidence |
| --- | --- | --- | --- | --- |
| | | additive / semi / non | | |

Fact type: transaction / periodic snapshot / accumulating snapshot / factless (why):

| Dimension | Business identity | Surrogate or durable key | SCD policy by attribute | Unknown/late behavior |
| --- | --- | --- | --- | --- |
| | | | | |

Historical semantics: event vs effective vs load time; as-was/as-is, validity intervals:

Bridge/join multiplicity and allocation guards:

Source lineage, corrections, retractions, backfill, retention:

Performance, partition/index/storage choices based on observed workload:

Checks: grain uniqueness; 1-to-1 history key resolution; fanout; reconciliation; replay:

Migration / compatible dual read / rollback / consuming dashboards:

Known / Assumed / Unknown:
