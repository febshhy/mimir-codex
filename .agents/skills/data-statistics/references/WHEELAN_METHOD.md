# Naked Statistics — concept extraction and engineering translation

**Source scope:** Charles Wheelan, *Naked Statistics: Stripping the Dread from the Data* (2013). The book was not uploaded. This original synthesis is informed by the available chapter listing and public overviews; it does not imply access to every chapter or reproduce the book's text.

- Chapter-level table of contents (Ingram-supplied retail listing): https://www.booktopia.com.au/naked-statistics-charles-wheelan/book/9780393071955.html
- Accessible critical overview: https://www.supersummary.com/naked-statistics/summary/

## 1. Description is an engineered choice (chs. 1–3)

Summary statistics compress complex data. Choose mean when additive expectation is meaningful and skew/outliers are understood; median for typical values in skewed populations; quantiles to describe tail experiences; variance/standard deviation for dispersion; and rates with explicit exposure/denominator. Averages across heterogeneous groups can conceal distribution changes. State units, time period, weighting, exclusions and segmentation. A seemingly precise figure can come from a flawed measurement process. Watch for presentation traps: truncation of axes, selectively chosen baselines, survivorship, nominal rather than inflation-adjusted values and changes in category definition. Test how the same result looks under plausible alternative aggregations.

## 2. Association, probability and risk (chs. 4–6)

Correlation is useful for prediction but does not identify causality. Confounding, reversed direction, trends and selection can create observed correlations; an intervention on X is not implied by a relationship between X and Y. A probability forecast needs an event definition, relevant base rate, conditioning information, dependence assumptions and calibration. Distinguish mutually exclusive from independent events; do not multiply dependent probabilities as if independent. Expected value is the weighted value of outcomes and helps compare decisions but does not by itself describe tail risk, risk tolerance or irreversibility. Look for fragile normality assumptions and rare but costly failure modes. The Monty Hall example illustrates why conditioning on the information-generating process matters more than intuition.

## 3. Data quality and sampling (ch. 7)

The data creation process is part of the inference. Inspect target population, collection frame, source changes, missing cases, measurement validity and selection; ask *who or what could never enter this dataset?* Examples: survivorship bias in active customers, survey nonresponse, convenience samples, publication/selection effects and time-based censoring. Classify missingness mechanism as unknown unless justified. A large biased sample can produce a very precise wrong answer. Validate deduplication and sample inclusion against raw data; treat data provenance as critical metadata.

## 4. Sampling distributions and inferential claims (chs. 8–10)

Sampling variability changes across samples. The central limit theorem can justify approximations for suitable independent/weakly dependent data under its conditions; it does **not** say all raw data are normal or that big n fixes bias. Standard deviation describes data spread; standard error describes an estimator's sampling variability. An interval conveys precision conditional on model/design assumptions. A frequentist 95% confidence interval describes a procedure's long-run coverage, not a 95% probability attached to a fixed parameter. A p-value is the probability, under a specified null model, of a result at least as extreme as observed; it is not P(null is true). Control Type I/II errors, sample-size/power, multiple comparisons and peeking when consequential. Poll margins of error often exclude non-sampling error, coverage, wording effects and nonresponse. Check design effects/cluster sampling where relevant.

## 5. Regression and its failure cases (chs. 11–12)

Regression quantifies conditional relationships under model assumptions. Review outcome units, candidate covariates, transformations, multicollinearity, high-leverage points, autocorrelation/cluster dependence, extrapolation, missing data and model instability. Conditioning on a collider or post-treatment variable can introduce bias. Omitted confounders and reverse causality undermine causal interpretation. Training and checking on the same data overstates performance. Interpret coefficients in correct scale/units; report uncertainty and out-of-sample residual diagnostics where relevant. Prefer a simple interpretable model that answers the decision to a complicated model without evidence of benefit.

## 6. Evaluation of interventions (ch. 13)

To claim an intervention changes outcomes, define a **counterfactual**. Prefer randomized assignment with correct unit and randomization checks when feasible. For observational interventions, document selection/identification assumptions and test sensitivity; comparisons before/after may confound policy effect with trends and seasonality. Distinguish intention-to-treat from treatment-on-treated where relevant. Report effect size, uncertainty, practical impact, harms and whether the study covers the decision population. A negative or inconclusive result is useful evidence, not an automatic error.

## Engineerable acceptance checks

- A daily conversion rate uses **eligible sessions** as denominator, with attribution and timezone agreed; do not silently switch to users.
- A spike chart includes numerator/denominator trends and coverage changes; compare with a baseline and confidence bounds if inferential claims are made.
- An A/B test guards assignment unit and exposure, checks for sample-ratio mismatch, avoids peeking/multiple testing mistakes, and reports an interval on the predeclared metric.
- A predictive regression is validated out-of-sample and remains labeled **associational** unless causal identification is justified.
- A survey report includes population/fieldwork/sample construction, response mechanism and limits of margin of error.
