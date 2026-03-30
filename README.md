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
- `docs/branch-maturity.md` - lightweight rubric for judging how developed a branch is in the method
- `docs/method-infrastructure.md` - plan for the first CLI layer that reduces method overhead without automating judgment
- `ROADMAP.md` - phased development plan for the research program
- `CONTRIBUTING.md` - norms for writing, sources, uncertainty, and edits
- `pyproject.toml` - Python packaging entry point for the method infrastructure CLI
- `meta/` - structured branch and run state for the CLI layer
- `research/notes/` - working notes, source synthesis, and questions
- `research/scenarios/` - scenario drafts, variants, and recombinations
- `research/experiments/` - process experiments and evaluation attempts
- `research/discards/` - explicit records of pruned, merged, or failed directions
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

The method, templates, evaluation rubric, and CLI infrastructure are now in place.

Current state:

- foundation, method, glossary, roadmap, and contribution docs are established
- the research workspace supports notes, scenarios, experiments, syntheses, loops, and discards
- four research branches active: `whiplash` (L4), `breadbasket`, `hydrologic`, `wealth-concentration` (L3)
- **Iteration 1 complete**: branch/run state tracking, method hygiene checks
- **Iteration 2 complete**: context compression (snapshot, index, stale detection, compare-prep)
- **Iteration 3 complete**: bounded model delegation via OpenRouter (summarize-note, extract-claims)
- model allocation is now operational: small/mid/strong slots with cost-aware routing
- generated artifacts stay in `meta/generated/`, marked as draft, never auto-set curation

## Current research branches

- `whiplash` - sequence failure, transition misreading, and category breakdown under non-stationarity
- `breadbasket` - correlation, transmission, buffers, trade, and unequal downstream exposure
- `hydrologic` - design/rule conflict under volatility in infrastructure, storage, and operating systems
- `wealth-concentration` - first non-climate proving-ground branch; currently a comparative hybrid between transmission and rule-conflict structures

These branches are not just topical clusters. They are being used to test whether the method can identify recurring epistemic structures that conventional inquiry tends to miss. Climate remains the current proving ground, but the methodological ambition is broader than climate.

The current non-climate result matters: portability appears real, but it does not look instantaneous or clean. The first non-climate branch has become a `Level 3 comparative proving-ground run`, which suggests that cross-domain transfer may initially arrive as a hybrid branch that only later resolves toward a dominant structure type.

The current method-level read is therefore sharper than before:

- `Level 3 non-climate portability` means the method can travel, ground itself, compare internally, and remain structurally useful outside climate
- `Level 4 non-climate portability` would mean a non-climate branch changes the method itself rather than only validating it

## Start here

If you are new to the project, read these in order:

1. `README.md`
2. `docs/foundation.md`
3. `docs/method.md`
4. `docs/research-loop.md`
5. `docs/research-agenda.md`
6. `docs/evaluation-framework.md`
7. `docs/branch-maturity.md`
8. `docs/method-infrastructure.md`

Then, for the most developed current work:

1. `research/syntheses/2026-03-27-initial-scenario-evaluation-matrix.md`
2. `research/syntheses/2026-03-27-whiplash-family-comparison.md`
3. `research/syntheses/2026-03-27-breadbasket-physical-stress-vs-policy-amplification.md`
4. `research/syntheses/2026-03-27-whiplash-vs-breadbasket-epistemic-structures.md`
5. `research/syntheses/2026-03-27-method-lessons-so-far.md`

## CLI

The method-infrastructure CLI layer reduces coordination overhead without automating judgment.

### Setup

1. Install Python 3.10+
2. (Optional) Add API key to `.env` for delegated tasks:
   ```
   OPENROUTER_API_KEY=your-key-here
   ```

### Branch Commands

```bash
python -m meta_autoresearch_cli branch list
python -m meta_autoresearch_cli branch status <slug>
python -m meta_autoresearch_cli branch check <slug>
python -m meta_autoresearch_cli branch dossier <slug>
python -m meta_autoresearch_cli branch snapshot <slug>
python -m meta_autoresearch_cli branch stale [slug]       # Check stale generated files
python -m meta_autoresearch_cli branch index <slug>       # Generate artifact index
python -m meta_autoresearch_cli branch compare-prep <slug> # Generate comparison prep
```

### Run Commands

```bash
python -m meta_autoresearch_cli run new <branch> --type <pass-type>
python -m meta_autoresearch_cli run list [--branch <slug>] [--status <state>]
python -m meta_autoresearch_cli run show <run-id>
python -m meta_autoresearch_cli run check <run-id>
python -m meta_autoresearch_cli run update <run-id> --add-output <kind> <path>
python -m meta_autoresearch_cli run complete <run-id>
python -m meta_autoresearch_cli run packet <run-id>
```

### Delegate Commands (requires API key)

```bash
python -m meta_autoresearch_cli delegate summarize-note <path>
python -m meta_autoresearch_cli delegate extract-claims <path>
python -m meta_autoresearch_cli delegate branch-packet <slug>
python -m meta_autoresearch_cli delegate run-prep <branch> --type <pass-type>
python -m meta_autoresearch_cli delegate batch <task> <pattern>   # Batch process files
```

### Orchestrator Commands (Phase 7 - Scaled-cycle automation)

```bash
python -m meta_autoresearch_cli orchestrator run <plan.json>       # Execute autonomous cycles
python -m meta_autoresearch_cli orchestrator status                # Show progress dashboard
python -m meta_autoresearch_cli orchestrator benchmark             # Test model performance
```

Pass types: `grounding`, `variant`, `comparison`, `maturity`, `discard`, `capability-fit`

See `docs/method-infrastructure.md` for the design intent and full command reference.
See `docs/model-performance.md` for model configuration and benchmarking guide.

## Contributing

Contributions are welcome, but this project values clarity of thought over speed. Before editing, read `CONTRIBUTING.md` and preserve the distinction between established framing, active hypotheses, and open questions.
