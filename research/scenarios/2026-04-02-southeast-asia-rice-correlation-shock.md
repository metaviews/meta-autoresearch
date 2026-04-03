# Southeast Asia Rice Correlation Shock

## Metadata

- title: Southeast Asia Rice Correlation Shock
- date: 2026-04-02
- author: OpenCode
- status: draft
- scenario type: crop comparison variant
- domain slice: climate volatility, rice trade, export restrictions, correlated production stress

## Research question

How might correlated hot-dry stress across major Southeast Asian rice-producing regions create a preparedness failure not because global rice disappears, but because the world's largest rice exporters simultaneously restrict trade while import-dependent buyers face acute substitution limits?

## Why this scenario exists

The breadbasket branch has strong wheat structure through Russia-Europe-China variants. This rice variant tests whether the correlation/transmission mechanism generalizes to a different crop with distinct trade geography, stock dynamics, and downstream exposure. Rice matters differently than wheat: fewer exporters, thinner trade share of production, more acute downstream food-security effects.

## Framing and assumptions

- baseline assumptions:
  - rice trade is a much smaller share of production than wheat (around 5-10% vs. 20%+)
  - India, Thailand, and Vietnam together account for a very large share of global rice exports
  - rice is a staple for billions, especially in Asia and Africa, with limited substitution at scale
- assumptions that depart from default narratives:
  - the key risk is not absolute rice shortage but trade restriction clustering in a thin market
  - rice price shocks transmit faster to food insecurity than wheat because poor households spend larger budget shares on rice
- boundaries of the scenario:
  - this is a stress-test scenario, not a forecast of a specific monsoon season
  - the focus is on export-node correlation and downstream transmission, not on every rice-producing region

## Scenario logic

A given monsoon season produces hot-dry stress across multiple major rice-exporting regions in South and Southeast Asia. India faces enough production pressure to consider or impose export restrictions (as it has done before). Thailand and Vietnam also underperform, reducing the system's ability to compensate through substitution within the exporter cluster.

The absolute production loss may be modest as a share of global rice production. But because trade is a thin slice of total production, even small shortfalls concentrate in the export market. Import-dependent buyers (Philippines, Indonesia, Bangladesh, Nigeria, and others) face tender failures, price spikes, and procurement stress.

The preparedness failure lies in assuming that rice markets will absorb correlated exporter stress the way wheat markets might. In rice, the buffer is thinner, the exporter concentration is higher, and the downstream food-security transmission is faster and more acute.

## Grounding

- FAO and USDA report that rice trade is around 5-10% of production, much thinner than wheat
- India, Thailand, and Vietnam together account for over half of global rice exports
- India has imposed rice export restrictions in recent years (2023 non-basmati ban)
- Philippines and Indonesia are among the largest rice importers, with limited domestic buffers
- Rice price shocks transmit rapidly to food insecurity in low-income importing regions

These sources support a rice variant in which exporter correlation matters disproportionately because the trade slice is thin and downstream dependence is acute.

## Signals and evidence classes

- signals already visible:
  - increasing hot-dry stress risk in South and Southeast Asian rice regions
  - history of rice export restrictions amplifying price shocks
  - high downstream sensitivity in rice-importing regions
- evidence classes consulted:
  - FAO rice market monitoring
  - USDA rice outlook and trade data
  - rice price transmission and food-security literature
  - historical export restriction cases (India 2023, 2007-08 rice crisis)
- missing evidence:
  - stronger evidence on how climate correlation specifically affects India-Thailand-Vietnam simultaneously
  - tighter case material on downstream procurement stress in specific importing regions

## Provisional evaluation

- plausibility: high; the exporter-concentration and thin-trade mechanisms are well documented
- internal coherence: high; the rice-specific transmission logic is clear and distinct from wheat
- relevance: high; this tests whether breadbasket structure generalizes beyond wheat
- preparedness value: high; it points toward monitoring exporter clustering and rice-specific buffers
- novelty: high; it reframes rice as a distinct correlation-risk crop, not just "another grain"
- status-quo challenge: high; it challenges the assumption that grain buffers behave similarly across crops
- imaginative power: medium-high; it expands the branch into crop-specific transmission dynamics

## Curation notes

- current curation gate:
  - keep (pending comparison with wheat variants)
- why keep this scenario:
  - it tests crop generalization of the correlation/transmission structure
  - it sharpens the branch by foregrounding crop-specific trade dynamics
  - it adds a second crop family to the breadbasket branch
- what should be refined next:
  - compare directly against Russia-Europe wheat variant to identify structure similarities and differences
  - add specific importer cases (Philippines, Nigeria) to parallel Egypt/Yemen wheat variants
- what might cause this scenario to be revised or merged:
  - if rice proves too distinct from wheat to share the same branch structure
  - if later evidence shows rice correlation risk is dominated by a single exporter (India) rather than multi-node correlation

## Uncertainties and failure modes

- key uncertainties:
  - how often India-Thailand-Vietnam stress would be simultaneous enough to matter
  - how much rice substitution is possible at scale (wheat, maize, cassava)
  - how much importer resilience exists through reserves or alternative sourcing
- where this could be misleading:
  - it could imply rice and wheat transmission are identical when rice is thinner and more acute
  - it could overstate correlation if monsoon patterns remain sufficiently diversified
- what would challenge the scenario most:
  - evidence that rice export restrictions are uncorrelated across major exporters
  - evidence that downstream buyers can substitute away from rice quickly enough to absorb shocks

## Links

- related notes:
  - `research/notes/2026-03-27-breadbasket-regional-grounding-note.md`
  - `research/notes/2026-03-27-mena-wheat-importer-exposure-note.md`
- related experiments:
  - `research/experiments/2026-03-27-climate-scenario-comparison-pass.md`
- related syntheses:
  - `research/syntheses/2026-03-27-breadbasket-physical-stress-vs-policy-amplification.md`
  - `research/syntheses/2026-03-27-russia-europe-vs-russia-china-wheat-comparison.md`
- related scenarios:
  - `research/scenarios/2026-03-27-synchronous-breadbasket-stress.md`
  - `research/scenarios/2026-03-27-northern-wheat-correlation-shock.md`
  - `research/scenarios/2026-03-27-russia-europe-wheat-trade-shock.md`

## Components used

- `mech:supplier-cluster-concentration` — exporter clustering in thin trade market
- `mech:export-restriction-amplification` — policy response amplifies physical stress
- `region:india-rice` — primary export node (new component)
- `region:southeast-asia-rice` — secondary export cluster (new component)
- `hazard:rice-shortfall` — production shortfall in staple crop (new component)
