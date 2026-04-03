# AI Compute Concentration Structural Stress

## Metadata

- title: AI Compute Concentration Structural Stress
- date: 2026-04-02
- author: OpenCode
- status: draft
- scenario type: non-climate comparative variant
- domain slice: political economy of technology, AI development, compute concentration, chip supply chains

## Research question

How might concentration of AI compute resources create a preparedness failure not mainly because compute is scarce in absolute terms, but because concentrated access to training infrastructure, chip supply, and energy capacity shapes who can develop frontier AI systems and under what constraints?

## Why this scenario exists

The wealth-concentration branch has demonstrated non-climate portability in financial/political economy (asset regimes, private credit). This variant tests whether the method generalizes to a different non-climate domain: technology and AI. Compute concentration shares structural features with wealth concentration (compounding advantages, access asymmetry, hidden transmission channels) but differs in key ways (geographic concentration, energy dependence, regulatory lag).

## Framing and assumptions

- baseline assumptions:
  - frontier AI training requires very large compute clusters (10,000+ GPUs)
  - chip supply (especially advanced nodes) is geographically concentrated
  - energy capacity and cooling infrastructure constrain where compute can be deployed
- assumptions that depart from default narratives:
  - the main issue is not only compute cost but access to training infrastructure at scale
  - concentration creates fragility through single points of failure (chip fabs, energy grids, talent clusters)
  - regulatory lag means rules are designed for distributed software, not concentrated hardware
- boundaries of the scenario:
  - this is a structural stress scenario, not a forecast of AI capabilities or timelines
  - the focus is on compute concentration as a political economy problem, not technical AI safety

## Scenario logic

Compute for frontier AI training concentrates in a small number of actors (large tech companies, well-funded startups, state-backed labs) because the capital, chip access, and energy requirements exceed what most organizations can deploy. This concentration is not merely financial—it is geographic (chip fabs in Taiwan, energy in specific regions), infrastructural (data center capacity), and regulatory (export controls, energy permitting).

As concentration increases, the system changes qualitatively. A small number of actors control the infrastructure that shapes AI development trajectories. Supply chain disruptions (chip fab outage, energy grid stress, cooling water shortage) affect not just one company but the entire frontier development landscape. Regulatory responses designed for distributed software (antitrust, safety rules) fail to address concentrated hardware dependencies.

The preparedness failure lies in treating compute as a commodity that markets will efficiently allocate. If compute is instead a concentrated infrastructure with compounding access advantages and single points of failure, then focusing only on cost misses the deeper mechanisms that concentrate capability and transmit fragility.

## Grounding

- Reports show frontier AI training runs now require 10,000-100,000+ GPUs
- TSMC produces the vast majority of advanced AI chips (90%+ of leading-edge semiconductors)
- Data center power demand is growing rapidly, with some regions facing grid capacity constraints
- Export controls on AI chips create geographic access asymmetries
- A small number of companies account for most frontier AI training runs

These sources support a compute concentration scenario in which access, not just cost, shapes development trajectories and creates systemic fragility.

## Signals and evidence classes

- signals already visible:
  - increasing compute requirements for frontier AI
  - geographic concentration of chip manufacturing
  - data center energy and cooling constraints
  - export controls creating access asymmetries
- evidence classes consulted:
  - AI compute trend reports
  - semiconductor industry analysis
  - data center energy and infrastructure reports
  - AI governance and export control materials
- missing evidence:
  - tighter data on compute concentration across actors
  - clearer case material on how supply disruptions propagate through AI development
  - stronger analysis of regulatory lag and design/rule mismatch

## Provisional evaluation

- plausibility: high; compute concentration trends are well documented
- internal coherence: high; the mechanism parallels wealth concentration while differing in key ways
- relevance: high; this tests whether the method generalizes beyond financial/political economy
- preparedness value: high; it points toward supply chain resilience, geographic diversification, energy planning
- novelty: high; it reframes AI development as infrastructure concentration, not just capability race
- status-quo challenge: high; it challenges the assumption that AI development is broadly distributed
- imaginative power: medium-high; it expands the branch into technology political economy

## Curation notes

- current curation gate:
  - keep (tests non-climate portability in new domain)
- why keep this scenario:
  - it tests whether wealth-concentration structure generalizes to technology
  - it adds a second non-climate domain beyond financial/political economy
  - it enables comparison between financial and compute concentration mechanisms
- what should be refined next:
  - compare directly against US asset-regime variant to identify structure similarities
  - add specific grounding cases (chip fab disruption, data center energy constraint)
  - clarify whether compute concentration is hybrid structure (transmission + rule-conflict) like wealth
- what might cause this scenario to be revised or merged:
  - if compute concentration proves fundamentally different from wealth concentration (not just domain variation)
  - if the scenario becomes too speculative without sufficient evidence grounding

## Uncertainties and failure modes

- key uncertainties:
  - how quickly compute requirements will grow vs. supply expansion
  - whether geographic diversification of chip manufacturing reduces concentration
  - how regulatory responses will evolve and whether they address concentration or entrench it
- where this could be misleading:
  - it could imply compute concentration is more stable than it is (rapid technical change could disrupt)
  - it could overstate hardware concentration if algorithmic efficiency improves dramatically
- what would challenge the scenario most:
  - evidence that compute access is becoming more distributed (cloud, efficiency gains)
  - evidence that concentration does not create fragility (redundancy, substitution available)

## Links

- related notes:
  - `research/notes/2026-03-28-wealth-concentration-grounding-note.md`
  - `research/notes/2026-03-28-wealth-transmission-channels-note.md`
- related experiments:
  - `research/experiments/2026-03-29-whiplash-validation-cycle-report.md`
- related syntheses:
  - `research/syntheses/2026-03-28-wealth-concentration-structure-mapping.md`
  - `research/syntheses/2026-03-29-method-lessons-cross-branch-synthesis.md`
- related scenarios:
  - `research/scenarios/2026-03-28-wealth-concentration-structural-stress.md`
  - `research/scenarios/2026-03-28-us-asset-regime-and-wealth-lock-in.md`

## Components used

- `mech:balance-sheet-compounding` — adapted to compute access compounding
- `mech:stationarity-mismatch` — regulation designed for distributed software faces concentrated hardware
- `region:us-wealth` — adapted to US tech concentration
- `inst:tsmc` — chip manufacturing concentration (new component)
- `infra:data-center-compute` — compute infrastructure (new component)
- `hazard:chip-supply-disruption` — supply chain risk (new component)
