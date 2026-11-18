# Book chapters and engineering applications

See the [Advanced SQL chapter mapping](../.agents/skills/advanced-sql/references/MACHADO_RUSSA_ESMERIZ_CHAPTER_MAP.md) for SQL methods.

Use these tables to see how a chapter topic informs a design choice or a verification check. The [book concept index](BOOK_CONCEPTS.md) links the methods and sources.

## Ralph Kimball and Margy Ross — *The Data Warehouse Toolkit*, third edition (2013)

Published [chapter list](https://www.wiley.com/en-us/the-data-warehouse-toolkit-the-definitive-guide-to-dimensional-modeling-3rd-edition-p-9781118732281); [Kimball Group official techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/).

| Chapter / topic | Mimir application |
| --- | --- |
| 1. DW/BI and dimensional modeling primer | Separate transaction sources from analytic consumer contracts; choose model around business decisions. |
| 2. Modeling techniques overview | Select fact/dimension pattern, grain, history, conformance, measures and specialized bridges from a concrete need. |
| 3. Retail sales | Apply process → grain → dimensions → facts; verify a transaction-level known-answer fixture. |
| 4. Inventory | Compare flow vs snapshot facts, semi-additive inventory balances, bus matrix and conformed facts/dimensions. |
| 5. Procurement | Design history and slowly changing dimensions; test attribute-level Type 1/2 and effective-time boundaries. |
| 6. Order management | Trace order transaction, invoice and accumulating pipeline snapshot with separate grains and milestones. |
| 7. Accounting | Define financial period, ledger/budget meaning, hierarchy and controlled aggregation with reconciled totals. |
| 8. CRM | Model customer identity, multivalued attributes, bridges and cross-source identity ambiguity; test fanout. |
| 9. Human resources | Preserve privacy, employee history, headcount snapshot denominator and hierarchy semantics. |
| 10. Financial services | Design heterogeneous products and dimensions with documented subtype/supertype choices. |
| 11. Telecommunications | Subject candidate schemas to a formal review of grain, keys, dimensions and query paths. |
| 12. Transportation | Model location, role-playing date/time, local timezones and measured movement events. |
| 13. Education | Use transaction, accumulating and factless occurrence models where student/process question requires them. |
| 14. Healthcare | Handle retroactive events/corrections, claims and sensitive access, retaining as-of semantics. |
| 15. E-commerce | Connect clickstream and purchases at compatible identity/grain; inspect attribution and session gaps. |
| 16. Insurance | Avoid mixed-grain policy, premium, claim and accident facts; choose snapshot or event depending on question. |
| 17. DW/BI lifecycle | Plan data integration, platform and consumption tracks around one accepted product slice. |
| 18. Dimensional modeling tasks | Record collaborative modeling decisions, business examples, semantic approval and grain tests. |
| 19. ETL subsystems | Treat extract, conformity, presentation and operational management as observable boundary contracts. |
| 20. ETL design/development | Test historic load, incremental load, corrections, checkpoints and real-time tradeoffs separately. |
| 21. Big data analytics | Measure actual volume, model and query needs before introducing distributed complexity. |

## Joe Reis and Matt Housley — *Fundamentals of Data Engineering* (2022)

[O'Reilly detailed chapter list](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/).

| Chapter | Mimir application |
| --- | --- |
| 1. Data engineering described | Define engineering success as useful trustworthy data, with clear producers and consumers. |
| 2. Lifecycle | Trace generation, storage, ingestion, transformation and serving; apply cross-cutting undercurrents. |
| 3. Good data architecture | Examine failure, reversibility, scalability, loose coupling, security, FinOps and ownership. |
| 4. Technology choices | Compare existing vs new stack using actual team, latency, interoperability and TCO constraints. |
| 5. Generation/source systems | Verify upstream event/API/CDC semantics, event time, transaction and producer ownership. |
| 6. Storage | Choose storage format, partitioning, retention, consistency and replay based on workload. |
| 7. Ingestion | Document batch/stream, offset, duplicates, lateness, schema evolution, DLQ and recovery. |
| 8. Queries/modeling/transformation | Separate semantic modeling from physical optimization, verify joins and composable logic. |
| 9. Serving for analytics/ML/reverse ETL | Contract freshness, metrics, ML point-in-time usage and side-effect safety. |
| 10. Security and privacy | Test least privilege, protected attributes, encrypted boundaries, access and deletion flow. |
| 11. Future of data engineering | Reconsider technology when real changes justify it; avoid treating trends as requirements. |

## Charles Wheelan — *Naked Statistics* (2013)

[Ingram-supplied chapter listing](https://www.booktopia.com.au/naked-statistics-charles-wheelan/book/9780393071955.html). The Monty Hall treatment is listed as section 5½; probability pitfalls follow in ch. 6.

| Chapter / section | Mimir application |
| --- | --- |
| 1. What's the point? | Write the exact decision a statistic answers and what would change the decision. |
| 2. Descriptive statistics | Choose mean/median/quantiles/dispersion by distribution and decision. |
| 3. Deceptive description | Audit omissions, axis choices, group definitions, changing samples and misleading precision. |
| 4. Correlation | Distinguish prediction/association from effect of intervening on a variable. |
| 5. Basic probability | Define event, base rate, conditioning and possible dependent outcomes. |
| 5½. Monty Hall | Inspect the information-generating mechanism before applying intuitive probability. |
| 6. Problems with probability | Include tails, dependence, calibration and failure cost in operational decisions. |
| 7. Importance of data | Audit selection, survivorship, missingness, provenance and measurement. |
| 8. Central limit theorem | Report sampling uncertainty under plausible design assumptions, never assume raw normality. |
| 9. Inference | Name null, test, interval/error interpretation, multiplicity and decision impact. |
| 10. Polling | Identify target population, frame, nonresponse and non-sampling error. |
| 11. Regression | Check model assumptions, covariate meaning, coefficient units and out-of-sample diagnostics. |
| 12. Common regression mistakes | Test confounding, leakage, bad extrapolation and unjustified causation. |
| 13. Program evaluation | Define treatment/control counterfactual and credible experiment or observational identification. |

## Foster Provost and Tom Fawcett — *Data Science for Business* (2013)

[O'Reilly detailed chapter list](https://www.oreilly.com/library/view/data-science-for/9781449374273/).

| Chapter | Mimir application |
| --- | --- |
| 1. Data-analytic thinking | Define the business decision, current baseline, measurable value and available data. |
| 2. Business problems/solutions | Translate decision → task → data understanding/prep → model → evaluate → deploy. |
| 3. Predictive modeling and supervised segmentation | Specify target, instance, features, prediction cutoff and conditional pattern. |
| 4. Fitting a model | Compare simple function/tree/logistic baseline to more complex models by evidence. |
| 5. Overfitting and its avoidance | Use untouched test data and suitable time/entity split; prevent selection leakage. |
| 6. Similarity, neighbors and clusters | Examine representation, scaling, distance, stability and interpretability. |
| 7. What is a good model? | Use confusion matrix, prevalence, unequal costs and expected utility, not accuracy alone. |
| 8. Visualizing model performance | Select rank/lift/ROC/profit curves that fit the actual capacity and decision. |
| 9. Evidence and probabilities | Apply priors/base rates and conditional dependence; calibrate action probabilities. |
| 10. Representing and mining text | Audit representation limits, privacy, feature availability and semantic drift. |
| 11. Toward analytical engineering | Decompose policy/intervention value; distinguish targeting from incremental causal effect. |
| 12. Other tasks and techniques | Compare associations, profiles, recommendation and causal evaluation to business need. |
| 13. Data science and business strategy | Assess cost of owning, operating and governing the decision system. |
| 14. Conclusion | Keep people, privacy, ethics, limitations and actual action outcomes in the loop. |

## Cole Nussbaumer Knaflic — *Storytelling with Data* (2015)

[Wiley detailed chapter list](https://www.wiley.com/en-us/storytelling-with-data-a-data-visualization-guide-for-business-professionals-p-9781119002062), [author's chapter assets](https://www.storytellingwithdata.com/book/downloads).

| Chapter | Mimir application |
| --- | --- |
| 1. Importance of context | Identify audience, question, intended action, medium and relevant uncertainty. |
| 2. Choosing an effective visual | Select table/bar/line/scatter/distribution by comparison task and encoding truth. |
| 3. Clutter is your enemy | Remove decorative noise, preserve axis, base, units and uncertainties. |
| 4. Focus audience attention | Use direct labels and measured contrast, plus non-color alternatives. |
| 5. Think like a designer | Align typography, whitespace, hierarchy, readability and accessible annotations. |
| 6. Dissecting model visuals | Critique alternative charts and explain how layout shapes interpretation. |
| 7. Lessons in storytelling | Develop context → evidence → meaning → action narrative without overstating data. |
| 8. Pulling it all together | Review context, encoding, declutter, attention, design and conclusion as one artifact. |
| 9. Case studies | Run before/after comparison and a cold-reader interpretation test. |
| 10. Final thoughts | Institutionalize review and reuse of clear charts and well-defined metrics. |

## Check the result across boundaries

The chapter titles are **source-grounded**. The tests below are **Mimir prescriptions**, not claims of author endorsement.

- **Same unit at every edge:** source identity/version (Reis/Housley) → atomic fact grain (Kimball/Ross) → sample unit/estimand (Wheelan) → prediction instance and decision cutoff (Provost/Fawcett) → label/unit in the chart (Knaflic).
- **Time travels through the stack:** event vs load/effective time; snapshot history; sampling window; leakage-free feature cutoff; dashboard freshness label. Prove no future information enters an earlier decision.
- **Don't let business value disappear:** approved question → conformed metric → valid estimate → action utility vs baseline → clear communication. A technically valid pipeline is incomplete if nobody can safely use the output.
- **Multiple sources of failure:** code state/effect error, data transport redelivery, mixed-grain join, biased sampling, overfit model, misleading visualization. At least one realistic representative failure path should be checked when each is consequential.
