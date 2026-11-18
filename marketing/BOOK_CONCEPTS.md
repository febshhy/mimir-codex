# Six design references → Mimir skills and evidence

Use this index to connect book concepts to Mimir skills and verification checks.

| Book / original publication | Verified accessible source | Extracted concepts and owning skill | Applied artifact / gate |
| --- | --- | --- | --- |
| Ralph Kimball & Margy Ross, *The Data Warehouse Toolkit*, 3rd ed. (2013) | [Wiley contents](https://www.wiley.com/en-us/the-data-warehouse-toolkit-the-definitive-guide-to-dimensional-modeling-3rd-edition-p-9781118732281), [Kimball Group](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/books/data-warehouse-dw-toolkit/) | [Detailed dimensional modeling synthesis](../.agents/skills/data-dimensional-modeling/references/KIMBALL_METHOD.md): process, four steps, grain, bus matrix, facts/dimensions, SCD, ETL and incremental integration | Grain/cardinality, source reconciliation, history and metric contract |
| Joe Reis & **Matt Housley**, *Fundamentals of Data Engineering* (2022) | [O'Reilly table of contents](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/) and [chapter 2](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/ch02.html) | [Detailed lifecycle synthesis](../.agents/skills/data-lifecycle/references/REIS_HOUSLEY_METHOD.md): five lifecycle stages, undercurrents, source/capture/storage/serving, TCO, failure, recovery | Source→consumer contract, idempotent replay, freshness/quality, permissions |
| Charles Wheelan, *Naked Statistics* (2013) | [Chapter listing](https://www.booktopia.com.au/naked-statistics-charles-wheelan/book/9780393071955.html) and public overview | [Detailed statistical reasoning synthesis](../.agents/skills/data-statistics/references/WHEELAN_METHOD.md): descriptive traps, probability, bias, sampling, uncertainty, regression and causal program evaluation | Population, estimand, bias review, valid interval and inference limits |
| Foster Provost & Tom Fawcett, *Data Science for Business* (2013) | [O'Reilly chapters](https://www.oreilly.com/library/view/data-science-for/9781449374273/) and [chapter 2 preview](https://www.oreilly.com/library/view/data-science-for/9781449374273/ch02.html) | [Detailed decision science synthesis](../.agents/skills/data-decision-science/references/PROVOST_FAWCETT_METHOD.md): task translation, validation/overfit, ranking, expected value, model proposal and deployment | Baseline, leakage-free evaluation, cost policy, impact vs prediction |
| Cole Nussbaumer Knaflic, *Storytelling with Data* (2015) | [Wiley chapter listing](https://www.wiley.com/en-us/storytelling-with-data-a-data-visualization-guide-for-business-professionals-p-9781119002062) | [Detailed communication synthesis](../.agents/skills/data-storytelling/references/KNAFLIC_METHOD.md): context, chart encoding, clutter, attention, narrative, case review | Verified message, appropriate chart, uncertainty and reader test |

The [chapter mapping](CHAPTER_TRACEABILITY.md) connects chapter topics to engineering decisions and checks.

## Cross-book synthesis

1. **Trace:** use the eight engineering foundations to follow real producer contracts, data lineage, consumers and failure boundaries. Apply detailed state/effect modeling only for consequential stateful applications.
2. **Define meaning:** use Kimball/Ross grain, conforming and historical semantics and an approved metric contract. Separate a business metric from the physical way it is stored.
3. **Evaluate evidence:** use Wheelan's skepticism about measurement/sampling and Provost/Fawcett's focus on decision costs, validation and baseline. Predictive performance is not evidence of causal benefit.
4. **Communicate:** apply Knaflic's context, encoding, attention and narrative to verified results, retaining denominator, uncertainty and data freshness.
5. **Deliver:** use Software Factory and Graph Protocol to coordinate one source-to-consumer change with clear owners and acceptance checks. See the [slice method](../.agents/skills/data-slicing/references/CROSS_TEAM_SLICES.md) and [templates](../docs/data/README.md).

## Rui Machado, Hélder Russa and Pedro Esmeriz — *Advanced SQL* (2026)

[O’Reilly book page](https://www.oreilly.com/library/view/advanced-sql/9798341627475/) and [eight-chapter verified topic map](../.agents/skills/advanced-sql/references/MACHADO_RUSSA_ESMERIZ_CHAPTER_MAP.md).

| Book theme | Mimir application |
| --- | --- |
| Modern SQL standards/dialects | Verify target engine/version before semi-structured, temporal, graph, ML or pipe syntax. |
| CTEs, recursion, windows | Write queries from output grain; define joins, cycle boundaries, frame, deterministic tie breaks. |
| Plans and performance | Inspect actual plan and measured bottleneck; compare result equivalence before/after tuning. |
| SQL architecture and governance | Design modular contract-bound producer-to-consumer SQL products with replay and observability. |
| 3NF/star/snowflake/OBT/graph | Compare update/read/history/traversal semantics and workload; do not impose a universal model. |
| Lakehouse, ingestion, medallion/semantic | Validate SQL transformations, metrics, owner/permissions, incremental and serve contracts. |
| SQL statistics/ML | Prove population, time cutoff and leakage-free features; validate inference/model separately. |
| SQL GenAI and extension syntax | Treat LLMs, embeddings, RAG/MCP, Pipe SQL/PRQL/Malloy as opt-in features with version, risk and cost checks. |

The [Advanced SQL skill](../.agents/skills/advanced-sql/SKILL.md) is the default starting point for SQL correctness and tuning.
