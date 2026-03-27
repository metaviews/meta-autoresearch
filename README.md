# Meta-Autoresearch

Meta-autoresearch is a research repository for developing a method of inquiry that resists premature closure.

The core idea comes from autoresearch in machine learning: fix a rigorous measure of success, allow wide exploration inside the search space, and let better structure emerge through iteration rather than forcing a conclusion in advance. This project extends that posture beyond model training into broader forms of research, using climate volatility as the first proving ground rather than the final scope.

## Why this exists

Much of what passes for research is really guided confirmation. We inherit an intuition, a political preference, a familiar model, or a desired outcome, then gather evidence until the result feels stable enough to defend. That pattern is often understandable. It is also increasingly inadequate in domains where historical continuity is breaking down.

Meta-autoresearch begins from a different posture:

- keep the measurement as stable as possible
- keep the directional search space as open as possible
- allow conclusions to emerge from contact with reality rather than from prior commitment

This repository is the working space for translating that posture into a usable method.

## v1 scope

Version 1 is a research repository, not a product.

The goal of this phase is to:

- define the method in practical terms
- test whether it can support disciplined scenario exploration
- use climate volatility as the first proving ground for a more general method
- document assumptions, experiments, and open questions in public

The goal of this phase is not to:

- ship a prediction engine
- claim authoritative climate forecasts
- automate judgment away from human curation
- pretend the method is proven before it has been stress-tested

## Initial domain: climate volatility

Climate volatility is the first domain because it concentrates the failure modes this method is meant to address. Historical baselines are becoming less reliable, stationarity is breaking down, and institutions still rely heavily on frames built for a more stable world.

The emphasis here is on scenario-space exploration rather than prediction. The question is not only "what will happen?" but also "what range of plausible configurations should we be prepared to think with?"

Prediction matters in some contexts, but this project is explicitly wary of prediction as the default posture. A singular target can narrow inquiry too early, encourage false precision, and train attention on one imagined future at the expense of the wider possibility space.

Climate is therefore the first proving ground, not the permanent identity of the project. The broader aim is to develop a method that can be used in other domains where premature closure, institutional bias, or target fixation distort inquiry.

## Repository map

- `README.md` - project overview and repo entry point
- `docs/foundation.md` - canonical long-form framing of the concept
- `docs/method.md` - operational description of the research loop
- `docs/research-loop.md` - first formal staged version of the loop now emerging in practice
- `docs/research-agenda.md` - active questions and near-term focus
- `docs/glossary.md` - working definitions for key terms
- `docs/research-tooling.md` - note on tools that would strengthen the research workflow
- `docs/evaluation-framework.md` - reusable rubric for comparing scenarios and making curation decisions
- `ROADMAP.md` - phased development plan for the research program
- `CONTRIBUTING.md` - norms for writing, sources, uncertainty, and edits
- `research/notes/` - working notes, source synthesis, and questions
- `research/scenarios/` - scenario drafts, variants, and recombinations
- `research/experiments/` - process experiments and evaluation attempts
- `research/loops/` - auditable records of full research-cycle runs
- `research/syntheses/` - comparisons, evaluations, and higher-order judgments across artifacts

## Working principles

- `rigor over certainty` - be strict about method, not about defending a conclusion
- `openness without vagueness` - entertain multiple directions without collapsing standards
- `human and AI as complements` - use AI for generation and remixing; keep human judgment explicit
- `scenario over prophecy` - explore possibility space rather than perform false precision
- `anti-target fixation` - do not let a singular forecast target collapse the search space too early
- `public iteration` - make the evolution of the thinking visible

## Current status

This repository is no longer only in a framing phase. The method, templates, evaluation rubric, and first research branches are now in place.

Current state:

- foundation, method, glossary, roadmap, and contribution docs are established
- the research workspace now supports notes, scenarios, experiments, and syntheses
- the first climate branches have been developed beyond abstract framing
- the project is now in `evidence grounding + evaluation refinement`, with early attention turning toward reusable structure types

## Current research branches

- `whiplash` - sequence failure, transition misreading, and category breakdown under non-stationarity
- `breadbasket` - correlation, transmission, buffers, trade, and unequal downstream exposure

These branches are not just topical clusters. They are being used to test whether the method can identify recurring epistemic structures that conventional inquiry tends to miss. Climate remains the current proving ground, but the methodological ambition is broader than climate.

## Start here

If you are new to the project, read these in order:

1. `README.md`
2. `docs/foundation.md`
3. `docs/method.md`
4. `docs/research-loop.md`
5. `docs/research-agenda.md`
6. `docs/evaluation-framework.md`

Then, for the most developed current work:

1. `research/syntheses/2026-03-27-initial-scenario-evaluation-matrix.md`
2. `research/syntheses/2026-03-27-whiplash-family-comparison.md`
3. `research/syntheses/2026-03-27-breadbasket-physical-stress-vs-policy-amplification.md`
4. `research/syntheses/2026-03-27-whiplash-vs-breadbasket-epistemic-structures.md`
5. `research/syntheses/2026-03-27-method-lessons-so-far.md`

## Contributing

Contributions are welcome, but this project values clarity of thought over speed. Before editing, read `CONTRIBUTING.md` and preserve the distinction between established framing, active hypotheses, and open questions.
