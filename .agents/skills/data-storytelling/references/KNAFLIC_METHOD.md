# Storytelling with Data — concept extraction and engineering translation

**Source scope:** Cole Nussbaumer Knaflic, *Storytelling with Data: A Data Visualization Guide for Business Professionals* (2015). Original synthesis based on the publisher's chapter index and description and available O'Reilly contents. The full book was not supplied.

- Wiley publisher and detailed chapter listing: https://www.wiley.com/en-us/storytelling-with-data-a-data-visualization-guide-for-business-professionals-p-9781119002062
- Author's companion chapter materials: https://www.storytellingwithdata.com/book/downloads
- O'Reilly chapter index: https://www.oreilly.com/library/view/storytelling-with-data/9781119002253/

## 1. Context is part of the specification (ch. 1)

A visualization is effective only for a particular audience and purpose. Ask: **who**, **what they know**, **what they need to decide/do**, **why now**, and **what evidence is sufficient**. A daily operations monitor needs scanability and exception handling; a leadership decision memo needs a conclusion, tradeoffs and uncertainty; an exploration notebook is allowed to remain open-ended. Choose a *so what?* statement after validating the analysis. Do not bury the key answer in an appendix or ask charts to resolve an unapproved decision rule.

## 2. Choose the encoding for the cognitive task (ch. 2)

| Question | Candidate chart | Main validity check |
| --- | --- | --- |
| Exact numbers / small lookup | Table with deliberate alignment | Unit, period and denominator are visible |
| Compare category magnitudes | Sorted aligned bars or dot plot | Common zero baseline when bar length encodes magnitude |
| Trend and change over ordered time | Line / small multiples | Even time spacing or explicit irregular timestamps |
| Shape / variability | Histogram, box/dot distribution | Bin choice, sampling and outlier treatment |
| Relationship | Scatter with appropriate scale | Association, confounding, overlap and sample size |
| Part-to-whole | Simple normalized bars for few categories | Categories exhaustive/mutually exclusive if claimed |
| Multiple groups | Small multiples, limited highlighted lines | Same meaningful scales across panels |

A table may beat a chart when the user needs a precise value. Avoid overloaded dual axes, 3D effects, perceptual area distortions, and a pie chart merely because data sum to 100%. Choose chart type **after** knowing the audience question and the measurement unit. Calendar, map and network visuals are special-purpose, not defaults.

## 3. Remove clutter without removing evidence (ch. 3)

Simplify visual framing, chartjunk, unnecessary legends, axis clutter and excessive precision. Use consistent number format, units and direct labels. Do **not** remove baseline, uncertainty, sample size, data caveat or disaggregation when omission would mislead. Check that visual simplification preserves the same factual claim.

## 4. Direct attention deliberately (ch. 4)

Preattentive attributes (position, length, contrast, color, weight) can guide scanning. Establish a quiet reference field and one or few emphasized observations. Use color consistently, with textual/dash/shape redundancy so no conclusion depends only on hue. Contrast can emphasize both a meaningful change and an erroneous conclusion; decide what deserves emphasis based on verified evidence. A highlighted outlier must have a baseline and should not imply significance without a test or argument.

## 5. Think like a designer and develop a narrative (chs. 5–8)

Alignment, whitespace, typography and visual hierarchy reduce effort. A useful analytical story often follows **context → tension/problem → evidence → implication → action**, with a headline that states the defensible conclusion. Design for viewing environment (mobile screen, report, projector, print), and provide concise direct annotations. Consider purposeful ordering of material; when uncertainty or assumptions determine interpretation, state them alongside the result. Interactive dashboards need empty/loading/error/stale states, not just polished success screenshots. For a live GUI use `$gui-design-thinking`, not a static slide template as state model.

## 6. Case-review and iterative communication (chs. 6, 9–10)

Review real examples by asking what someone will read first, whether comparisons are fair, and whether the conclusion survives a neutral alternative display. Test with a person unfamiliar with the analysis. Misreadings often reveal ambiguous labels, unexplained units, insufficient context, or missing uncertainty. Preserve the source dataset/version and exact query behind a chart; a visually coherent chart can still be factually wrong.

### Worked micro-brief (proposed)

Audience: operations lead deciding whether to investigate a funnel decline. Source: semantic measure with numerator/denominator and sample. Design: trend line with prior-period baseline, same eligible population, annotation at release date and accompanying small breakdown of denominator by channel. Caption: observed change and uncertainty; explicitly avoid attributing it to the release without causal evidence. Next action: verify instrumentation change and segment movement before mitigation. If data freshness or definition changes, show a visible status and suppress the strong claim.
