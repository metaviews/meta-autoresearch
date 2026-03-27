# Climate Scenario Comparison Pass

## Metadata

- title: Climate Scenario Comparison Pass
- date: 2026-03-27
- author: OpenCode
- status: completed
- experiment type: comparative generation and curation

## Objective

Test whether generating multiple competing climate-volatility scenarios produces a more useful research set than iterating only on a single initial scenario.

## Motivation

The first scenario pass produced one promising artifact, but the method risks overcommitting to the first coherent narrative it generates. A comparison pass is needed to widen the search space and make curation more explicit.

## Inputs

- research question or context:
  - climate volatility broadly understood as a preparedness problem
  - need for multiple scenario families rather than a single flagship scenario
- materials used:
  - `docs/method.md`
  - `research/notes/2026-03-27-climate-volatility-evidence-note.md`
  - `research/scenarios/2026-03-27-compound-seasonal-whiplash.md`
  - `research/scenarios/TEMPLATE.md`
- prompts, instructions, or process rules:
  - generate scenarios that compete on mechanism, not only style
  - keep one scenario focused on within-region sequencing and others on different system logics
  - force explicit curation notes and uncertainties for each scenario
- constraints:
  - no false precision
  - no unsupported local forecast claims
  - each scenario must imply a different preparedness question

## Procedure

1. Review the initial scenario and identify what mechanism it emphasizes.
2. Review a small evidence base on compound events, interacting risks, and crop-system volatility.
3. Generate additional scenarios that differ in mechanism rather than only in surface wording.
4. Compare the scenarios for plausibility, preparedness value, and distinctiveness.
5. Record whether the comparison pass improves the method's search-space coverage.

## Provisional measurement

- evaluation criteria declared before running:
  - distinct scenario mechanisms
  - plausibility grounded in at least one evidence class
  - usefulness for preparedness thinking
  - explicit uncertainties and curation logic
- what counts as improvement:
  - a scenario set that spans multiple climate-volatility mechanisms
  - clearer understanding of which scenario families deserve deeper development
- what would count as failure or noise:
  - multiple scenarios that are stylistic variants of the same idea
  - broader search space with weaker coherence
  - unsupported claims smuggled in through confident prose

## Outputs produced

- scenarios generated:
  - `research/scenarios/2026-03-27-compound-seasonal-whiplash.md`
  - `research/scenarios/2026-03-27-synchronous-breadbasket-stress.md`
  - `research/scenarios/2026-03-27-hydrologic-whiplash-and-design-failure.md`
- notes or syntheses generated:
  - `research/notes/2026-03-27-climate-volatility-evidence-note.md`
- unexpected artifacts:
  - the scenario set naturally organized itself around three mechanism families: sequencing, correlation, and infrastructure-design lag

## Results

The comparison pass improved the research set. The original seasonal-whiplash scenario remained useful, but it now sits within a clearer scenario family rather than acting as a catch-all. The breadbasket scenario tests correlation risk across regions and markets. The hydrologic-whiplash scenario tests design and operating-rule failure in infrastructure systems. Together they create a more legible starting map of climate-volatility mechanisms.

The pass also showed that minimal source grounding changes the writing: scenarios become less rhetorical and more useful when they are tied to explicit evidence classes early.

## Interpretation

- what seems useful:
  - comparison makes curation more honest because it forces selection between mechanisms
  - the scenario family structure gives the repo a better basis for future syntheses
  - adding a source note early improves discipline without requiring full literature review
- what seems weak or misleading:
  - the scenarios are still broad and not yet stress-tested against region-specific cases
  - comparison can create a false sense of coverage if too few mechanisms are sampled
- what changed in your understanding of the method:
  - scenario generation should move quickly from single artifacts to competing families
  - evidence notes are a useful bridge between philosophical framing and scenario drafting

## Next step

- repeat as-is: no
- revise and rerun: yes; do a targeted next pass on one scenario family with case evidence
- discard approach: no
- fold into another workflow: yes; use the three scenario families as the basis for the first synthesis document

## Links

- related notes: `research/notes/2026-03-27-climate-volatility-evidence-note.md`
- related scenarios:
  - `research/scenarios/2026-03-27-compound-seasonal-whiplash.md`
  - `research/scenarios/2026-03-27-synchronous-breadbasket-stress.md`
  - `research/scenarios/2026-03-27-hydrologic-whiplash-and-design-failure.md`
- follow-up experiments: none yet
