---
name: data-statistics
description: Audit descriptive statistics, measurement, sampling, probabilistic claims, uncertainty, regression, experiment analysis and observational inference.
---

# Statistical reasoning — define population, estimand, uncertainty and threats

**Authority:** Correct use and interpretation of evidence; it does not approve business actions or imply causality without a defensible design. Read [Wheelan concept extraction](references/WHEELAN_METHOD.md) for substantive statistical work and pair with `$data-decision-science` when selecting interventions.

## Work from the claim backward

1. Define decision, target **population**, sampling frame, unit, time period, observable outcome and **estimand** (quantity to estimate). Label the difference between a population fact, sample statistic, model prediction and causal effect.
2. Investigate how observations exist: missingness, survivor/selection/nonresponse bias, duplicates, measurement error, confounding, changes in definitions and data collection. The wrong sample cannot be rescued by a small p-value.
3. Describe distribution before fitting: n, missing counts, central tendency, dispersion, skew, units, outliers, denominator, subgroup composition and exposure. Means, medians, counts, rates and percentiles answer different questions.
4. Match method to claim: descriptive comparison, probability/risk, survey inference, regression, experimental estimate, or observational causal strategy. Clarify assumptions and dependence structure.
5. State uncertainty and alternatives. Confidence intervals, standard errors, posterior intervals and prediction intervals differ; explain which was actually computed. Do not call p-values the probability a null hypothesis is true.
6. Test robustness: baseline vs adjusted, segmentation, extreme values, multiplicity, relevant confounders, data leakage, sensitivity to assumptions, and falsification/negative controls when suitable.
7. Translate results into a bounded decision and a chart/report without certainty inflation; distinguish association from causation.

## Minimum evidence record

```text
Question / decision / approved claim:
Population, unit, sample and observation window:
Metric/estimand and numerator/denominator:
Collection, exclusions, missingness and known biases:
Study design and assumptions:
Method and observed estimate with interval / uncertainty:
Robustness and competing explanations:
Causal claim supported? yes/no + why:
What remains unknown; reproducing query/code/version:
```

Apply `$testing` to the computations, `$data-storytelling` to presentation and `$data-slicing` to operational handoffs. No claim of statistical significance establishes business value on its own.
