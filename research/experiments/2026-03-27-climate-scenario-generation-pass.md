# Climate Scenario Generation Pass

## Metadata

- title: Climate Scenario Generation Pass
- date: 2026-03-27
- author: OpenCode
- status: completed
- experiment type: workflow and curation

## Objective

Test whether a lightweight meta-autoresearch pass can turn the broad climate volatility framing into a concrete first scenario without collapsing into prediction or vague abstraction.

## Motivation

The repository needs an initial worked example. Before scaling the process, it is useful to see whether a simple generation-and-curation pass can produce one scenario that is specific enough to inspect and broad enough to matter.

## Inputs

- research question or context:
  - climate volatility broadly understood as the first proving ground for the method
  - emphasis on scenario-space exploration rather than forecasting
- materials used:
  - `README.md`
  - `docs/foundation.md`
  - `docs/method.md`
  - `docs/research-agenda.md`
  - `research/scenarios/TEMPLATE.md`
- prompts, instructions, or process rules:
  - generate a first scenario that tests broad climate volatility
  - keep the artifact exploratory rather than predictive
  - make assumptions, evidence classes, curation logic, and uncertainties explicit
- constraints:
  - no claim of empirical completeness
  - no region-specific forecast unless supported by targeted evidence
  - produce something legible enough to reuse as a pattern

## Procedure

1. Review the project's framing documents and scenario template.
2. Identify a climate-volatility mechanism broad enough for v1 but concrete enough to structure a scenario.
3. Draft one scenario focused on compounding seasonal swings and institutional lag.
4. Self-curate the result against the provisional scenario criteria in `docs/method.md`.
5. Record what the pass reveals about the method's current strengths and gaps.

## Provisional measurement

- evaluation criteria declared before running:
  - plausibility given broad evidence classes
  - internal coherence of the mechanism
  - relevance to preparedness thinking
  - novelty beyond default climate narration
  - explicit handling of uncertainty
- what counts as improvement:
  - a scenario that surfaces a useful planning problem rather than restating that climate risk exists
  - a scenario structured well enough to guide follow-up research
- what would count as failure or noise:
  - generic alarm language with no mechanism
  - premature prediction masquerading as insight
  - a scenario so broad that it cannot generate next questions

## Outputs produced

- scenarios generated:
  - `research/scenarios/2026-03-27-compound-seasonal-whiplash.md`
- notes or syntheses generated:
  - none yet
- unexpected artifacts:
  - a need for clearer file naming and workspace conventions across research directories

## Results

The pass produced one scenario that appears directionally useful. The most promising element is the focus on sequence blindness: institutions may be better prepared for named hazards than for fast transitions between hazard categories. The scenario remained broad enough to fit the v1 agenda, but it also exposed a recurring tension: without case evidence, strong language can arrive too easily.

The pass also revealed that the repo needed a clearer naming convention before more artifacts were added.

## Interpretation

- what seems useful:
  - starting with a broad mechanism rather than a specific geography keeps the first scenario exploratory
  - forcing curation notes and failure modes into the document makes the artifact more honest
  - linking the scenario back to method criteria helps separate interesting writing from useful structure
- what seems weak or misleading:
  - the scenario still needs grounding in concrete cases or literature before it can support stronger claims
  - a single-pass generation flow risks preserving the model's first neat narrative instead of testing alternatives
- what changed in your understanding of the method:
  - the method benefits from producing a first artifact quickly, but it needs explicit comparative passes soon after
  - naming and traceability conventions matter earlier than expected because the research corpus will otherwise become hard to audit

## Next step

- repeat as-is: no
- revise and rerun: yes; run a second pass that generates multiple competing climate-volatility scenarios before selection
- discard approach: no
- fold into another workflow: yes; use this as the baseline for a comparative generation experiment

## Links

- related notes: none yet
- related scenarios: `research/scenarios/2026-03-27-compound-seasonal-whiplash.md`
- follow-up experiments: none yet
