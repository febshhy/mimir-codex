---
name: data-decision-science
description: Frame business decisions as analytics/ML tasks; evaluate predictive models, ranking, expected value, experimentation, deployment and human decision processes.
---

# Decision science — business action → task → validation → expected value

**Authority:** Decision framing and model-use evaluation. `$requirements` owns business policy, `$data-statistics` owns inference, `$software-design-thinking` owns application effects, `$data-lifecycle` owns dependable feature/data delivery.

1. Write the decision, actor, action options, constraints, **baseline** and what loss/value each outcome produces. Determine whether a report, rule, experiment or predictive model is actually needed.
2. Translate into task: description, ranking, classification, regression, clustering, text or causal evaluation. Specify prediction target and timestamp, eligible population, feature availability **at decision time**, label horizon, costs of false actions, and who may override.
3. Audit examples and provenance: target leakage, post-outcome fields, historical policy bias, selection, proxy/ethical concerns, group coverage and concept drift. Set train/validation/test separation by entity and time appropriate to deployment.
4. Start with a naive or current-process baseline. Use simple models first; increase complexity only if out-of-sample performance or operational value justifies it.
5. Evaluate **decision utility**, not only accuracy: confusion matrix, class prevalence, ranking/lift, precision/recall, calibration, costs/benefits, capacity and decision thresholds; use uncertainty and subgroup analysis. Prevent overfitting to evaluation data.
6. Plan deployment, user-facing decision loop, monitoring, retraining/revalidation triggers, safe fallback and rollback. If causal benefit is sought, test impact with experiments or defensible causal methods.

Read [Provost/Fawcett extraction](references/PROVOST_FAWCETT_METHOD.md). The output must include: decision table, dataset/time contract, baseline, evaluation design, expected-value assumptions, acceptable harms, deployment/recovery and unknowns. Unsupported model quality never becomes a promised business result.
