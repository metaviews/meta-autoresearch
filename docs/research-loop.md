# Research Loop

## Purpose

This document formalizes the working loop that has started to emerge in practice.

It is not the final version of the method. It is the first reusable description of the cycle that currently seems to produce the best results in the repository.

The loop is written in a domain-general way on purpose. Climate is the current proving ground, but the cycle is meant to be usable in other domains where scenario exploration is more honest than premature prediction.

The next phase of the project adds modest method infrastructure around this loop. The aim is to support the loop with better state, scaffolding, and validation, not to automate away the judgment inside it.

## The loop at a glance

1. frame the inquiry
2. assemble the starting evidence base
3. generate candidate branches
4. ground the most promising branch
5. create meaningful variants inside that branch
6. compare the variants
7. evaluate and curate the branch
8. synthesize across branches
9. assess whether the cycle is mature enough to repeat or scale

## Stage 1: Frame the inquiry

### Goal

Define what is being explored, why it matters, and what kind of output the cycle is trying to produce.

### Typical outputs

- research question
- scope boundaries
- provisional measurement criteria
- decision about the initial unit of work

### Gate to continue

- is the question clear enough to generate against?
- are the boundaries tight enough to prevent immediate vagueness?
- has the inquiry been framed in a way that avoids premature prediction or target fixation?

## Stage 2: Assemble the starting evidence base

### Goal

Build the minimum source base needed to prevent the first pass from drifting into elegant unsupported prose.

### Typical outputs

- one or more source-backed notes
- record of open-web search and researcher-supplied materials
- early evidence tensions or gaps

### Gate to continue

- do we have enough grounding to generate bounded scenarios?
- do we know what is supported versus still speculative?

## Stage 3: Generate candidate branches

### Goal

Produce multiple scenario directions that differ in mechanism, not only in wording.

### Typical outputs

- exploratory scenario set
- early curation notes
- first family labels if they start to emerge

### Gate to continue

- are the branches meaningfully distinct?
- did generation expand the search space instead of multiplying stylistic variants?
- did the cycle resist collapsing too early around one expected outcome?

## Stage 4: Ground the most promising branch

### Goal

Take one promising branch and anchor it in stronger evidence, case material, or clearer system logic.

### Typical outputs

- grounding note
- revised parent scenario
- bounded candidate contexts, regions, or systems

### Gate to continue

- is the branch still too broad to test?
- has grounding made the branch more honest instead of merely more detailed?

## Stage 5: Create branch variants

### Goal

Test whether the branch survives translation into multiple named cases or mechanism variants.

### Typical outputs

- regional variants
- node comparisons
- subtype scenarios

### Gate to continue

- do the variants reveal a real family structure?
- are the differences structural, or only rhetorical?

## Stage 6: Compare the variants

### Goal

Use comparison to decide what the branch actually is, which variant is strongest, and which mechanism is most useful.

### Typical outputs

- comparison synthesis
- stronger sense of best-evidenced versus most generative variants
- clearer next-step priorities

### Gate to continue

- does comparison produce sharper curation?
- is at least one variant clearly weaker, more provisional, or in need of revision?
- in a new domain, does comparison clarify whether the branch is resolving toward a dominant structure or remaining a meaningful hybrid?

## Stage 7: Evaluate and curate the branch

### Goal

Apply the formal evaluation layer so the branch is judged explicitly rather than impressionistically.

### Typical outputs

- scored comparison against `docs/evaluation-framework.md`
- curation outcomes: `keep`, `revise`, `merge`, `discard`
- branch-specific next step
- discard or merge records when pruning is meaningful enough to preserve

### Gate to continue

- is the branch worth deeper investment?
- does the evidence support the level of confidence implied?

## Stage 8: Synthesize across branches

### Goal

Look above any one branch to identify what kind of epistemic structure the branch may be revealing.

### Typical outputs

- cross-branch comparison
- emerging structure types
- method lessons about how different branches behave

### Gate to continue

- has the work revealed a genuinely reusable structure, or only more domain content?
- does the branch change the method, or only populate it?
- if the branch is outside climate, has portability been demonstrated through repeated grounding and comparison rather than assumed from thematic similarity alone?

## Stage 9: Assess cycle maturity

### Goal

Decide whether the cycle is ready to be repeated more systematically or partially migrated to cheaper models.

### Typical outputs

- list of robust steps versus brittle steps
- quality risks for scaling
- decision about whether to rerun, deepen, branch, or stop
- decision about which steps require frontier capability and which can be right-sized to cheaper or local execution

### Gate to continue

- are the failure modes understood well enough to repeat the loop?
- would scaling produce more signal or just more noise?
- does the current design depend on unnecessary model capability or cost?

## Roles across the loop

### Human role

- frame the inquiry
- decide curation thresholds
- identify overclaiming
- decide when a branch is mature enough to deepen or prune

### High-capability model role

- early branch generation
- comparison drafting
- synthesis drafting
- pressure-testing the shape of the loop itself
- tasks where failure from weaker models would distort the method more than it would save resources

This category may include different frontier or premium models over time rather than one fixed provider or interface.

### Lower-cost or local model role later

- repeated bounded generation
- classification and clustering passes
- drafting comparative tables or summaries
- support work once the loop structure is already stable

This category may also include diverse model types rather than one fallback system: local models, cheaper hosted models, domain-specific tools, or simpler non-LLM processing when the task is well structured.

The target is not only lower inference cost. It is a process where capability is allocated deliberately, so the loop can stay rigorous while becoming more accessible to run.

Some coordination work around the loop can also be delegated to lightweight local tooling before any model delegation is attempted. That includes state tracking, run scaffolding, and hygiene checks.

As the ecosystem changes, the loop should be able to reassign work without changing its epistemic standards. The method should be portable across model stacks, not silently coupled to one family of tools.

## Minimum viable successful loop

A loop should not count as successful just because it produced interesting scenarios.

At minimum, a good loop should produce:

- one bounded branch
- one grounding note
- more than one branch variant or comparison target
- one explicit curation judgment
- one synthesis explaining what the branch taught the method

## Signs the loop is not working

- scenarios remain broad after grounding
- variants differ mostly in style, not mechanism
- curation never produces `revise`, `merge`, or `discard`
- evidence notes do not materially change the scenarios
- syntheses only summarize artifacts instead of sharpening judgment

## Signs the loop may be ready to scale later

- branch creation repeatedly produces distinct mechanisms
- grounding consistently narrows branches rather than bloating them
- comparison reliably improves curation
- evaluation decisions become more stable across passes
- humans can identify which sub-tasks are robust enough to delegate
- the loop can name which stages truly need frontier capability and which do not

## Suggested file pattern for one loop

- `research/notes/` - evidence notes and case notes
- `research/scenarios/` - parent branch plus variants
- `research/experiments/` - explicit method tests of the loop
- `research/discards/` - explicit records of pruned or failed directions
- `research/loops/` - audit records of one full run through the loop
- `research/syntheses/` - branch comparison, evaluation, and cross-branch lessons

## Working rule

Do not treat this loop as fixed doctrine. Treat it as the current best version of the cycle. It should be revised whenever practice shows a stage is missing, redundant, or out of order.

That includes revising the loop for efficiency. A better loop is not only one that is more rigorous. It is also one that uses capability more deliberately and remains feasible for broader use.
