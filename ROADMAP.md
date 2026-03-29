# Roadmap

## Current read

The project has completed the foundational setup, built the first repeatable research workflow, and developed two meaningful climate branches with internal comparison structure.

That means the immediate task is no longer basic exploration. It is to improve the quality of the cycles: stronger grounding, clearer curation, sharper measurement, and better evidence that the method changes what gets noticed.

Practical read of the roadmap now:

- Phases 1-3 are complete enough to serve as the working foundation
- Phase 4 is actively underway
- Phase 5 has begun in an early form through the evaluation framework and scenario matrix
- Phase 6 is not yet implemented, but the repo is now producing the kind of structured cycles that can later be tested for scale
- the immediate bridge between Phase 5 and Phase 6 is a small `method infrastructure` layer that reduces coordination overhead and makes runs easier to repeat

## Phase 1: foundation and structure

Establish the conceptual basis of the project, define the repository structure, and separate foundational claims from open research questions.

Outputs:

- core docs in place
- shared vocabulary established
- initial research scope defined

## Phase 2: operational method

Turn the framing into a repeatable workflow for notes, scenarios, experiments, and syntheses.

Outputs:

- scenario template
- experiment template
- notes and synthesis support
- initial evaluation criteria
- explicit human/AI workflow

## Phase 3: first climate explorations

Use climate volatility as the first proving ground and produce an initial body of scenario work.

Outputs:

- exploratory scenario set
- first synthesis across scenarios
- written reflections on failure modes and surprises

## Phase 4: evidence grounding and narrowing

Take promising scenario families and ground them more firmly in literature, case evidence, and researcher-supplied source material.

Outputs:

- grounded scenario variants tied to specific regions, systems, or case clusters
- clearer distinction between evidence-rich and evidence-thin scenario families
- explicit notes on what is supported, what is speculative, and what remains unresolved

## Phase 5: evaluation and refinement

Assess whether the method is producing genuinely useful structure or merely generating interesting text.

Outputs:

- revised measurement framework
- stronger curation rules
- scenario comparison matrix or equivalent evaluation layer
- documented lessons from early experiments
- explicit examples of what the method should stop doing

Current signals of progress in this phase:

- a reusable evaluation framework exists
- the whiplash branch has internal comparison and pruning pressure
- the breadbasket branch now has sub-branch comparison and downstream exposure grounding
- emerging epistemic structure types are starting to appear in the method itself
- loop-run and discard artifacts now make both success and pruning auditable
- the first non-climate proving-ground branch has reached a comparative maturity level, showing that portability is plausible but often arrives first as a hybrid rather than a clean transfer
- the next strategic question is no longer whether the method can leave climate, but what additional evidence would make non-climate portability method-shaping rather than only comparative

## Phase 5.5: method infrastructure

Add a lightweight internal tooling layer that supports the method without turning the project into a product.

Outputs:

- structured branch and run state
- loop-run scaffolding and validation
- branch dossier generation for the next pass
- clearer visibility into what is missing from a branch or run
- better separation between judgment-heavy work and support-heavy work

Near-term continuation of this phase:

- Iteration 2: context compression for branch snapshots, run packets, and comparison prep
- Iteration 3: bounded affordable-model delegation via provider-agnostic config, with OpenRouter as the first backend

## Phase 6: scaled-cycle design

Design how the research loop could run repeatedly and at larger volume without losing rigor.

Outputs:

- a staged cycle design for repeated generation, curation, grounding, and synthesis
- clear division between high-capability model use for method design and lower-cost model use for larger-scale execution
- guardrails for scaling without multiplying noise, drift, or false confidence
- criteria for when a cycle is mature enough to be repeated programmatically or with cheaper models
- a process design that stays accessible enough to run without permanent dependence on frontier-model budgets
- explicit model-allocation rules that can route work across multiple model and tool types as the ecosystem evolves

The first CLI layer planned in `docs/method-infrastructure.md` is the intended bridge into this phase.

## Phase 7: prototype decision

Only after the research workflow becomes legible and evaluable should the project decide whether to build software around it.

Possible next steps:

- static site for publishing scenarios and syntheses
- lightweight research tooling for scenario generation and curation
- structured data model for reusable scenario components
- model orchestration for repeated research cycles

## Cross-phase priorities

- keep the method auditable as the corpus grows
- treat source discipline as part of the method, not as cleanup work
- prune weak scenario families instead of only accumulating new ones
- preserve the distinction between valuable prompts and well-supported claims
- optimize for capability fit and process efficiency, not only raw model power
- treat climate as a proving ground for the method, not as its permanent boundary
- resist prediction-centered design when it narrows the search space prematurely

## Guiding rule

Do not build product complexity or cycle scale faster than methodological clarity.
