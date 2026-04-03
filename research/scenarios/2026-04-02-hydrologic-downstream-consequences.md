# Hydrologic Design Failure Downstream Consequences

## Metadata

- title: Hydrologic Design Failure Downstream Consequences
- date: 2026-04-02
- author: OpenCode
- status: draft
- scenario type: downstream consequences variant
- domain slice: climate volatility, water systems, agricultural stress, energy-water nexus, urban supply

## Research question

How might hydrologic design/rule conflict under volatility create downstream preparedness failures not only in water infrastructure itself, but in agriculture, hydropower, urban supply, and ecological systems that depend on reliable water management?

## Why this scenario exists

The hydrologic branch has strong infrastructure-internal structure (reservoir rules, dam operations, design standards). But the branch manifest asks: "What downstream preparedness consequences should be added so the branch is less infrastructure-internal?" This variant connects design/rule conflict to downstream systems that depend on water management functioning as expected.

## Framing and assumptions

- baseline assumptions:
  - agriculture, hydropower, urban supply, and ecology all depend on predictable water management
  - farmers plant crops, cities grow, power plants are sited based on expected water availability and timing
  - reservoir operating rules mediate between upstream conditions and downstream expectations
- assumptions that depart from default narratives:
  - the main failure may not be infrastructure breakdown but the cascading effects when infrastructure cannot deliver expected water services
  - downstream systems may be more vulnerable than the water infrastructure itself
- boundaries of the scenario:
  - this is a downstream stress scenario, not a replacement for infrastructure-focused variants
  - the focus is on design/rule conflict transmission to dependent systems

## Scenario logic

A basin experiences wet-dry sequence stress that exposes the mismatch between reservoir operating rules and current climate volatility. Operators shift from flood-control mode to drought-response mode faster than downstream users can adapt.

The infrastructure does not catastrophically fail. But it stops delivering water services in the expected patterns. Agricultural users who planted water-intensive crops based on historical allocation patterns face sudden restrictions. Hydropower operators must choose between maintaining minimum flows for ecology and generating power for peak demand. Urban utilities that assumed reliable upstream storage face quality problems (sediment, temperature, algal blooms) that treatment plants were not designed to handle.

The preparedness failure lies in treating water infrastructure as the endpoint of risk assessment. In this scenario, the infrastructure adapts (slowly, imperfectly) but the downstream systems that depended on predictable water services face acute stress. The design/rule conflict propagates through water-dependent sectors.

## Grounding

- SEQ Water Grid experience: drought-to-flood transitions affected agricultural allocations and urban restrictions
- Upper Colorado Compact: structural shortage means downstream users (agriculture, municipalities) face cuts that rules did not anticipate
- California experience: wet years followed by dry years create planting decisions that become unsustainable
- Hydropower operators in multiple basins report volatility in generation due to rule-curve mismatches

These sources support a downstream consequences variant in which design/rule conflict propagates to agriculture, energy, and urban systems.

## Signals and evidence classes

- signals already visible:
  - agricultural water restrictions following rule changes
  - hydropower generation volatility under wet-dry transitions
  - urban water quality problems linked to reservoir operating shifts
- evidence classes consulted:
  - water management case studies (SEQ, Upper Colorado, California)
  - agriculture-water dependence literature
  - energy-water nexus reports
  - urban water supply resilience materials
- missing evidence:
  - tighter quantification of downstream economic losses from rule-curve mismatch
  - clearer attribution of specific agricultural failures to hydrologic design conflict vs. direct climate stress

## Provisional evaluation

- plausibility: high; downstream dependence on water management is well documented
- internal coherence: high; the transmission from infrastructure to downstream is clear
- relevance: high; this directly addresses the branch open question about downstream consequences
- preparedness value: high; it points toward cross-sector coordination and downstream buffering
- novelty: medium-high; most hydrologic scenarios focus on infrastructure, not downstream transmission
- status-quo challenge: high; it challenges sectoral silos in water risk assessment
- imaginative power: medium-high; it expands the branch into multi-sector preparedness

## Curation notes

- current curation gate:
  - keep (addresses explicit branch open question)
- why keep this scenario:
  - it makes the hydrologic branch less infrastructure-internal
  - it connects design/rule conflict to concrete downstream impacts
  - it enables comparison with breadbasket downstream variants (Egypt, Yemen)
- what should be refined next:
  - add specific regional grounding (e.g., Upper Colorado agriculture, SEQ urban supply)
  - compare against hydrologic infrastructure variants to identify which downstream systems are most vulnerable
- what might cause this scenario to be revised or merged:
  - if downstream impacts prove to be direct climate effects rather than infrastructure-mediated
  - if the scenario becomes too broad and loses the design/rule conflict mechanism

## Uncertainties and failure modes

- key uncertainties:
  - how much downstream stress is infrastructure-mediated vs. direct climate impact
  - which downstream sectors are most vulnerable to rule-curve mismatch
  - how quickly downstream users can adapt to changed water management patterns
- where this could be misleading:
  - it could imply infrastructure operators control outcomes more than they actually do
  - it could understate direct climate effects on agriculture and ecology
- what would challenge the scenario most:
  - evidence that downstream users already plan for high water management volatility
  - evidence that rule-curve changes are slow enough that adaptation is feasible

## Links

- related notes:
  - `research/notes/2026-03-27-seq-hydrologic-whiplash-grounding-note.md`
  - `research/notes/2026-03-27-upper-colorado-hydrologic-design-note.md`
- related experiments:
  - `research/experiments/2026-03-27-climate-scenario-comparison-pass.md`
- related syntheses:
  - `research/syntheses/2026-03-27-hydrologic-branch-comparison.md`
  - `research/syntheses/2026-03-27-emerging-structure-types-comparison.md`
- related scenarios:
  - `research/scenarios/2026-03-27-hydrologic-whiplash-and-design-failure.md`
  - `research/scenarios/2026-03-27-seq-grid-and-wivenhoe-whiplash.md`
  - `research/scenarios/2026-03-27-upper-colorado-compact-and-storage-whiplash.md`

## Components used

- `mech:stationarity-mismatch` — rules built for stationarity face non-stationarity
- `mech:wet-dry-sequence-failure` — infrastructure designed for single hazard faces both
- `infra:reservoir-rule-curves` — operating rules that mediate downstream delivery
- `hazard:agricultural-drought` — downstream agricultural impact
- `region:upper-colorado` — basin with documented downstream allocation stress
