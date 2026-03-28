# Method

## Purpose

This document translates the project's philosophical framing into an operational research loop.

Meta-autoresearch is a method for exploring complex questions without rushing to a conclusion. It combines stable evaluation criteria, broad directional exploration, explicit human curation, and iterative accumulation.

## Core commitments

- `fixed measurement` - define evaluation criteria before deep iteration and resist redefining them to suit results
- `open search space` - explore multiple explanatory directions, including unlikely or uncomfortable ones
- `emergent structure` - allow patterns, categories, and stronger hypotheses to arise from iteration
- `explicit curation` - record where human judgment enters and what it chooses to keep, combine, or discard
- `traceable reasoning` - preserve assumptions, sources, uncertainty, and changes in framing
- `anti-target fixation` - do not let a singular prediction target or expected answer prematurely narrow the inquiry

## The unit of work

The main working unit in v1 is the `scenario`.

A scenario is not a prediction. It is a structured account of a plausible configuration, pathway, or risk pattern inside a defined domain. Scenarios can be:

- exploratory
- comparative
- stress-test oriented
- recombinatory

The supporting units are:

- `note` - a working thought, source synthesis, or question
- `experiment` - a test of process, prompt structure, evaluation, or curation workflow
- `synthesis` - a higher-order document that compares or combines multiple scenarios or notes

The method is designed to be domain-general where appropriate. Climate volatility is the current proving ground, not the limit of what meta-autoresearch is for.

## Against prediction fixation

This project is not anti-forecast in every context. It is anti-default-prediction as the organizing posture of inquiry.

The reason is methodological:

- prediction can invite false precision before the system is understood well enough
- singular targets can collapse the search space too early
- institutions often optimize around the forecast they can name, not the range of structures they should be prepared for

Meta-autoresearch therefore prefers scenario-space exploration, structural comparison, and explicit curation before any move toward narrow forecasting claims.

## Human and AI roles

AI is used for:

- generating initial scenario variants
- broadening the search space
- remixing scenario components
- summarizing source material
- proposing classifications or comparisons

Humans remain responsible for:

- setting the inquiry frame
- deciding what counts as a useful measurement
- curating which outputs matter
- assessing whether a scenario is interesting, coherent, or misleading
- deciding what to publish, combine, revise, or abandon

The point is not to remove human judgment. The point is to make judgment visible and better supported.

## Baseline workflow

1. Define the question.
2. Define the provisional measurement.
3. Generate multiple scenario directions.
4. Curate the most useful directions.
5. Refine, combine, or stress-test selected scenarios.
6. Record what changed and why.
7. Reassess the measurement only if there is a documented reason.

For the current staged version of this workflow as it has emerged in practice, see `docs/research-loop.md`.

## Iteration logic

The project is not trying to get the perfect cycle right on the first pass. It is trying to iteratively design a cycle that becomes reliable enough to repeat at larger scale.

The intended progression is:

1. prototype the workflow carefully
2. observe where the cycle produces signal, drift, or rhetorical noise
3. revise the workflow and repeat
4. keep only the parts that survive repeated contact with evidence and curation
5. scale the cycle only when its failure modes are better understood

This means the early repository is not separate from the method. It is the method's training ground.

The next step in that training is modest infrastructure. The project now has enough method clarity to justify a small tooling layer that reduces coordination overhead, preserves branch state, and makes each pass more complete without automating judgment away.

## Emerging structure types

One goal of v1 is not only to generate useful scenarios, but to identify recurring kinds of epistemic failure.

Three provisional types have already started to emerge:

- `sequence failure` - the risk becomes visible only when conditions are understood as a chain rather than as separate events or seasons
- `correlation/transmission failure` - the risk becomes visible only when distributed nodes are understood as one coupled system rather than as separate local problems
- `design/rule conflict under volatility` - the risk becomes visible when inherited operating rules, allocation frameworks, thresholds, or infrastructure purposes no longer fit the system dynamics they were built to manage

These are not final categories. They are early candidates for reusable structure types that future branches can test, refine, or overturn.

The third type matters because emergence does not only happen in events or scenarios. It can also happen in the mismatch between formal system design and current reality. In those cases, the research process is not mainly surfacing a new outcome. It is surfacing a hidden conflict between rule architecture and changed conditions.

The long-term aim is for those structure types to travel beyond climate where the fit is real and the method remains honest.

## Measurement in v1

The hardest part of applying autoresearch outside machine learning is measurement. In v1, the measurement will often be provisional and partly qualitative, but it still needs to be explicit.

Initial evaluation criteria for scenarios should include:

- plausibility given available evidence
- internal coherence
- relevance to the research question
- usefulness for preparedness or decision-making
- novelty relative to default narratives
- ability to reveal overlooked interactions or second-order effects
- ability to challenge status-quo assumptions that may reflect institutional bias
- imaginative range that expands what can be seriously considered without abandoning discipline

Not every criterion will matter equally in every experiment. What matters is that the criteria are declared before iterative selection begins.

## Evidence versus scenario value

This project should distinguish between two different judgments:

- `evidence strength` - how strongly the available sources support the claims inside a scenario
- `scenario value` - how useful the scenario is for exploration, preparedness, or exposing hidden assumptions

A scenario can be highly useful as a research prompt while still being weakly evidenced. A scenario can also be well evidenced but not especially valuable. These should not be collapsed into one score.

## Curation gates

Each meaningful scenario pass should end with an explicit curation decision:

- `keep` - worth developing further in roughly its current form
- `revise` - promising, but too vague, weakly grounded, or overextended
- `merge` - better treated as part of another scenario family
- `discard` - not useful enough to justify further attention

The reason for the decision should be recorded. If a synthesis or comparison pass never discards anything, the method is probably not curating hard enough.

## Source discipline

Research artifacts should distinguish among source types rather than treating all inputs as equivalent.

Useful working categories include:

- `assessed report`
- `peer-reviewed paper`
- `journalistic reporting`
- `researcher-provided canonical document`
- `working interpretation`

This classification helps prevent eloquent summaries from appearing stronger than their actual evidence base.

## Research loop discipline

To keep the process honest, each scenario or experiment should try to preserve:

- the question being explored
- the sources or evidence classes consulted
- the assumptions introduced
- the reason a scenario was kept, changed, merged, or discarded
- the uncertainties that remain unresolved

This creates an audit trail for emergence. Without that trail, the method risks becoming aesthetic intuition disguised as process.

## Human and model scaling strategy

The method is expected to use different model tiers at different stages.

- high-capability models are useful early for designing workflows, pressure-testing concepts, and exploring the shape of the cycle itself
- lower-cost or local models may become useful later for running repeated generation, classification, comparison, or drafting passes at larger volume
- humans remain responsible for framing, curation, evaluation design, and deciding when a lower-cost loop is trustworthy enough to use

Model choice should be guided by three things at once:

- `capability fit` - use the weakest model that can still do the task well enough
- `process efficiency` - design the loop so expensive capability is used only where it meaningfully improves the result
- `accessibility` - prefer a workflow that can eventually be run by more people, on cheaper infrastructure, or with local models, rather than one that depends permanently on high-end access

The broader aim is not simply to move from one expensive model to one cheaper model. It is to develop a method that can allocate work across a diverse model ecosystem with different strengths, weaknesses, interfaces, and costs.

The point is not to scale generation immediately. The point is to first design a cycle that deserves to be scaled.

In practice, this means:

1. use stronger models to prototype the loop
2. identify what parts of the loop are robust versus brittle
3. migrate robust sub-tasks to cheaper or local execution only when quality loss is acceptable and visible
4. keep high-stakes curation and method redesign under stronger human and model supervision

The project is not trying to imitate compute intensity for its own sake. It is trying to discover where capability density is actually necessary and where the process can be made leaner without losing rigor.

That means model allocation is itself part of the method. Over time, the project should become better at deciding which tasks belong to frontier models, which to local models, which to task-specific tools, and which should remain primarily human.

## What success looks like in v1

Success in this phase does not mean proving the method universally.

It means demonstrating that the repository can:

- produce scenario explorations that are more varied and useful than default framing alone
- make human curation legible rather than hidden
- hold open multiple lines of inquiry without drifting into vagueness
- develop a sharper operational definition of measurement over time
- reveal which parts of the cycle can eventually be repeated at scale and which parts resist automation

## Known risks

- measurement drift
- scenario proliferation without useful selection
- treating eloquence as evidence
- mistaking novelty for insight
- blurring the boundary between exploration and conclusion
- scaling weak cycles too early
- handing cheap models tasks that still require stronger judgment

These risks are not side issues. They are central design constraints.
