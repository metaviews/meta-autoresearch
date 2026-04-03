# Climate Policy Whiplash

## Metadata

- title: Climate Policy Whiplash
- date: 2026-04-02
- author: OpenCode
- status: draft
- scenario type: hybrid sequence variant (agentic response to non-agentic change)
- domain slice: climate volatility, policy transitions, adaptation planning, regulatory whiplash

## Research question

How might climate policy transitions (mitigation-to-adaptation, adaptation-to-emergency) create preparedness failures not because either policy direction is wrong, but because the transition between policy regimes occurs faster than infrastructure, capital, and institutional adaptation is possible?

## Why this scenario exists

The whiplash branch has demonstrated sequence failure in pure climate cases (wet-to-fire, recovery-to-shortage) and pure policy cases (COVID reopening, monetary tightening). This variant tests a **hybrid sequence**: agentic policy response to non-agentic climate change.

This matters because:
- Climate policy is the intersection of physical and political dynamics
- Policy transitions may amplify rather than absorb climate whiplash
- Hybrid sequences may be the most common form in practice

## Framing and assumptions

- baseline assumptions:
  - Climate policy shifts between mitigation (reduce emissions), adaptation (prepare for impacts), and emergency response
  - Each policy regime requires different infrastructure, capital allocation, and institutional expertise
  - Policy transitions occur through elections, crises, and changing public opinion
- assumptions that depart from default narratives:
  - the main failure is not policy direction but transition velocity between regimes
  - climate policy whiplash can amplify physical climate whiplash (e.g., adaptation cuts before disaster, emergency spending after)
  - actors optimize for current policy regime, creating vulnerability to transition
- boundaries of the scenario:
  - this is a sequence failure scenario, not a critique of specific climate policies
  - the focus is on transition dynamics, not policy evaluation

## Scenario logic

A region experiences a period of mitigation-focused policy (carbon pricing, renewable subsidies, emissions targets) long enough that actors optimize for its continuation. Utilities invest in renewables, manufacturers electrify, financial institutions price carbon. Then conditions shift (economic stress, political change, visible adaptation failures) and policy rapidly transitions to adaptation or emergency mode.

The preparedness failure is not that mitigation was wrong or adaptation is wrong. The failure is that the transition creates whiplash: capital allocated for mitigation becomes stranded, adaptation infrastructure was not built during mitigation period, institutional expertise is mismatched to new regime.

The hybrid nature amplifies the problem: physical climate whiplash (e.g., flood followed by drought) triggers policy whiplash (adaptation-to-emergency), creating compound stress on institutions that must respond to both physical and policy transitions simultaneously.

## Grounding

- Australia: Climate policy shifts between mitigation (carbon tax 2012-2014) and repeal, creating investment uncertainty
- US: Federal climate policy oscillation between administrations (Paris Agreement entry/exit/re-entry)
- EU: Fit for 55 package represents major policy shift requiring rapid adaptation from industry
- Post-disaster patterns: Emergency spending after disasters (flood, fire) followed by return to normalcy before adaptation complete

These cases support a climate policy whiplash scenario in which transition velocity, not policy direction, creates preparedness failure.

## Signals and evidence classes

- signals already visible:
  - Climate policy volatility across multiple jurisdictions
  - Investment uncertainty cited as barrier to climate action
  - Post-disaster emergency spending followed by adaptation gaps
- evidence classes consulted:
  - Climate policy databases (Net Zero Tracker, Climate Action Tracker)
  - Investment uncertainty literature
  - Post-disaster recovery case studies
- missing evidence:
  - tighter quantification of policy transition frequency
  - clearer attribution of investment delays to policy uncertainty vs. other factors
  - stronger case material on compound physical + policy whiplash

## Provisional evaluation

- plausibility: high; climate policy volatility is well documented
- internal coherence: high; the hybrid sequence mechanism is clear (physical triggers policy, both create stress)
- relevance: high; this tests whether whiplash structure handles mixed agentic/non-agentic cases
- preparedness value: high; it points toward policy stability mechanisms, adaptive planning
- novelty: high; it reframes climate policy risk as sequence failure, not policy evaluation
- status-quo challenge: high; it challenges partisan framing (good policy vs. bad policy) in favor of transition dynamics
- imaginative power: medium-high; it expands the branch into hybrid sequences

## Curation notes

- current curation gate:
  - keep (tests hybrid sequence structure)
- why keep this scenario:
  - it tests whether whiplash structure handles agentic + non-agentic hybrid
  - it connects climate and policy variants within same scenario
  - it enables comparison with pure climate and pure policy cases
- what should be refined next:
  - add specific case evidence (Australia carbon tax repeal, US Paris Agreement oscillation)
  - compare against pure climate and pure policy variants to identify hybrid-specific mechanisms
  - clarify whether hybrid is more dangerous than pure sequences or just different
- what might cause this scenario to be revised or merged:
  - if hybrid proves indistinguishable from pure policy whiplash
  - if evidence shows policy transitions are slow enough that adaptation is feasible

## Uncertainties and failure modes

- key uncertainties:
  - how fast climate policy transitions actually occur
  - whether physical or policy whiplash dominates in compound cases
  - how much investment is actually stranded vs. adaptable
- where this could be misleading:
  - it could imply all policy change creates whiplash (some transitions are gradual)
  - it could understate physical climate impacts relative to policy impacts
- what would challenge the scenario most:
  - evidence that climate policy is stable enough that transitions are predictable
  - evidence that compound physical + policy whiplash is rare

## Links

- related notes:
  - `research/notes/2026-03-27-feather-river-whiplash-grounding-note.md`
  - `research/notes/2026-04-02-policy-whiplash-case-studies.md`
- related experiments:
  - `research/experiments/2026-03-29-whiplash-validation-cycle-report.md`
- related syntheses:
  - `research/syntheses/2026-03-27-whiplash-family-comparison.md`
  - `research/syntheses/2026-04-02-climate-vs-policy-sequence-comparison.md`
- related scenarios:
  - `research/scenarios/2026-03-27-feather-river-wet-to-fire-whiplash.md`
  - `research/scenarios/2026-04-02-policy-regime-whiplash.md`

## Components used

- `mech:wet-to-fire` — climate sequence failure (analog)
- `mech:policy-regime-whiplash` — policy sequence failure (analog)
- `mech:climate-policy-hybrid` — hybrid agentic/non-agentic sequence (new component)
- `hazard:policy-transition` — climate policy volatility (new component)
