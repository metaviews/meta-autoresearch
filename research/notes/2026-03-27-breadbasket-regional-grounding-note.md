# Breadbasket Regional Grounding Note

## Metadata

- title: Breadbasket Regional Grounding Note
- date: 2026-03-27
- author: OpenCode
- status: draft
- type: case note

## Purpose

Add region-specific grounding to the `correlated breadbasket stress` family using the strongest currently available sources in the repo.

## Core takeaways

### 1. The breadbasket-risk literature is already region-specific in structure

Gaupp et al. (2020) do not only argue for a generic global food risk. Their analysis uses region-specific agricultural production data and evaluates major breadbaskets over time. The paper explicitly highlights global dependence on a limited set of major food-producing regions and shows increasing risk of simultaneous failure for wheat, maize, and soybean crops across the breadbaskets analyzed.

Why this matters:

- it supports treating breadbasket stress as a real spatial correlation problem rather than as a metaphor for global food fragility
- it gives the scenario family a direct bridge from global systems language to named production regions

### 2. Wheat risk is especially salient in northern-latitude production regions

Heino et al. (2023) report that wheat showed the strongest increase in co-occurring hot and dry conditions during the growing season, with the probability in global wheat production regions rising from less than 1% in the early 1980s to around 5% in 2009 in their analysis. They also report that wheat yield reductions from co-occurring heat and drought were larger in relatively cool regions, including Russia and China.

Why this matters:

- it grounds the scenario family in a specific regional pattern instead of a vague global aggregate
- it suggests northern breadbaskets should not be treated as simple beneficiaries of warming narratives

### 3. Maize and soybean risk also map onto major producing regions

Heino et al. (2023) report that maize showed the largest overall susceptibility to climate variations, with strong explanatory power in major producing areas including North America and China. The same paper reports that hot-dry conditions reduced maize yields in almost all climate-bin-specific models, with large reductions in places such as East Asia and eastern Europe. For soybean, the paper highlights important exposed regions in North and South America as well as eastern Asia.

Why this matters:

- the breadbasket family can be grounded in region clusters rather than one crop or one continent
- it supports scenario variants built around cross-region combinations such as North America plus China for maize or the Americas plus eastern Asia for soybean

### 4. The family is strongest when treated as correlation-plus-transmission

The literature gathered so far supports two layers at once:

- climate layer: co-occurring hot-dry extremes and synchronized stress across important production zones
- systems layer: food-system fragility increases when more than one major producing region is stressed at the same time

The sources are stronger on the first layer than on the downstream policy-and-market transmission layer, but they are already enough to justify keeping the scenario family active.

## Region clusters worth using next

- wheat: Russia, China, Europe, North America
- maize: North America, China, East Asia, eastern Europe
- soybean: North America, South America, eastern Asia

These clusters are not forecasts. They are candidate grounding regions for next-pass scenario variants.

## What this note supports

- refining `research/scenarios/2026-03-27-synchronous-breadbasket-stress.md` with regional examples
- creating future scenario variants around specific crop-region combinations
- treating correlation risk as a first-order preparedness question rather than an afterthought

## What this note does not support

- the claim that all breadbaskets are failing at once
- a precise claim about near-term food-system collapse
- strong statements about price or conflict transmission without more specific evidence

## Open questions

- which crop-region combination is most useful for the next grounded scenario variant?
- what evidence best connects synchronized production stress to trade, reserve, and price behavior?
- how should the repo distinguish climate correlation from policy amplification?

## Sources

1. Gaupp, F., Hall, J., Hochrainer-Stigler, S., et al., 2020. *Changing risks of simultaneous global breadbasket failure.* `https://www.nature.com/articles/s41558-019-0600-z`
2. Heino, M., Kinnunen, P., Anderson, W., et al., 2023. *Increased probability of hot and dry weather extremes during the growing season threatens global crop yields.* `https://www.nature.com/articles/s41598-023-29378-2`

## Links

- related scenarios: `research/scenarios/2026-03-27-synchronous-breadbasket-stress.md`
- related experiments: `research/experiments/2026-03-27-climate-scenario-comparison-pass.md`
- related syntheses: `research/syntheses/2026-03-27-first-scenario-family-synthesis.md`
