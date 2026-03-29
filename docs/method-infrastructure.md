# Method Infrastructure

## Purpose

This document specifies the first infrastructure layer for meta-autoresearch.

The goal is not to automate research wholesale. The goal is to reduce method overhead so each pass can complete more useful work while preserving audibility, curation, and epistemic discipline.

## Why this layer exists

The current bottleneck is not idea generation. It is interaction bandwidth.

Too much cycle state currently has to be reconstructed across sessions:

- which branch is strongest
- which variant is most provisional
- which artifacts are missing
- what pass type should happen next
- what evidence or pruning still needs to be made explicit

The first CLI layer is meant to reduce that overhead.

## Design goal

Increase `work per pass` modestly by moving from artifact-by-artifact coordination toward run-level coordination.

That means the tooling should help with:

- state
- scaffolding
- validation
- packetization

It should not replace judgment.

## Non-goals

This first layer is not:

- an autonomous research system
- a web app
- a general product platform
- a database-first architecture
- model orchestration for full-cycle autonomy
- automatic research writing without review

## Core principles

- `method first` - infrastructure should support the loop already documented in `docs/research-loop.md`
- `judgment stays visible` - human and high-capability model judgment remain explicit
- `state becomes legible` - branch and run status should be recoverable in one step
- `small surface area` - solve the most repetitive coordination problems first
- `right-sized capability` - do not add more software complexity than the method currently justifies
- `allocation-aware design` - build the process so work can later be assigned across diverse model and tool types rather than locked to one system

## First layer scope

The first layer should do five things.

### 1. Scaffold a run

Create the structured state for a new pass against a branch.

Expected result:

- a run manifest
- declared pass type
- expected outputs

### 2. Track branch state

Make current branch status explicit and recoverable.

Expected result:

- current maturity
- current structure type
- strongest and weakest variants
- open questions
- next recommended pass

### 3. Validate method hygiene

Check whether the branch or run is missing expected artifacts.

Expected result:

- warnings for missing grounding notes, loop runs, comparison syntheses, or discard records

### 4. Generate a branch dossier

Produce a compact packet for the next session.

Expected result:

- current branch summary
- missing pieces
- recommended next move
- key artifact links

### 5. Support later capability tiering

Make it easier to identify which bounded sub-tasks might later move to cheaper or local models.

Expected result:

- explicit separation between judgment-heavy and support-heavy steps
- clearer future routing across multiple model classes, not just one expensive model and one cheap fallback

## Proposed technical shape

- language: `Python`
- manifest format: `JSON`
- dependency strategy: stdlib-first where possible
- first execution mode: local CLI, likely via `python -m ...`

## Proposed state layout

- `meta/branches/` - branch manifests
- `meta/runs/` - run manifests
- `meta/generated/` - generated dossiers or summaries

Research artifacts remain in `research/`. The `meta/` directory should hold structured state, not canonical research content.

## Proposed branch manifest

Minimum fields:

- `slug`
- `title`
- `domain`
- `structure_type`
- `maturity_level`
- `status`
- `parent_artifact`
- `active_variants`
- `key_notes`
- `key_syntheses`
- `loop_runs`
- `discard_records`
- `strongest_variant`
- `most_generative_variant`
- `weakest_variant`
- `open_questions`
- `next_recommended_pass`
- `last_updated`

## Proposed run manifest

Minimum fields:

- `run_id`
- `date`
- `branch_slug`
- `run_type`
- `question`
- `stages_targeted`
- `expected_outputs`
- `created_outputs`
- `completion_status`
- `notes`
- `next_step`

## First pass types to encode

- `grounding`
- `variant`
- `comparison`
- `maturity`
- `discard`
- `capability-fit`

Each pass type should imply expected artifact classes and minimum completion checks.

## First CLI commands

### `run new`

Creates a new run manifest for a branch and pass type.

### `run check`

Checks whether a run produced the expected artifacts.

### `run show`

Shows a run manifest in a more readable form, including current outputs, notes, and validation summary.

### `run list`

Lists known run manifests, optionally filtered by branch or status.

### `run update`

Updates a run manifest with created outputs, notes, status, or next-step changes.

### `run complete`

Marks a run complete once its required outputs are present, or explicitly records completion with gaps when forced.

### `branch status`

Shows current branch state in a concise, human-readable form.

### `branch list`

Lists known branches with current maturity, structure type, and next recommended pass.

### `branch check`

Validates branch hygiene against the loop and maturity expectations.

### `branch dossier`

Generates a next-pass packet summarizing branch state, missing pieces, and likely next work.

## First validation rules

Examples:

- a `grounding` run should create at least one grounding note or equivalent grounded scenario update
- a `comparison` run should create at least one comparison synthesis
- a `Level 3+` branch should have a loop-run artifact
- a branch with meaningful pruning should have at least one discard record
- a `Level 4` branch should connect clearly to a structure-type synthesis or method-level consequence

## What this should improve

- less time reconstructing branch state across sessions
- more complete passes
- more consistent branch comparison
- clearer visibility into what deserves scale and what only deserves attention
- a better foundation for model allocation across a broad and changing AI ecosystem

## What success looks like

The first infrastructure layer is successful if it can:

- start a new run in one command
- recover branch state in one command
- reveal missing artifacts in one command
- generate a useful next-pass packet
- remain understandable by directly reading the manifest files

## Build order

1. create the docs and state model
2. add branch manifests
3. add run manifests
4. implement `run new`
5. implement `branch status`
6. implement `run check`
7. implement `branch dossier`

## Initial implementation status

The first slice of this layer is now present in the repository.

Implemented:

- branch manifests in `meta/branches/`
- run scaffolding in `meta/runs/`
- `branch status`
- `branch list`
- `branch check`
- `branch dossier`
- `run new`
- `run check`
- `run show`
- `run list`
- `run update`
- `run complete`

Current invocation style:

- `python -m meta_autoresearch_cli branch status <slug>`
- `python -m meta_autoresearch_cli branch list`
- `python -m meta_autoresearch_cli branch check <slug>`
- `python -m meta_autoresearch_cli branch dossier <slug>`
- `python -m meta_autoresearch_cli run new <branch> --type <pass-type>`
- `python -m meta_autoresearch_cli run check <run-id>`
- `python -m meta_autoresearch_cli run show <run-id>`
- `python -m meta_autoresearch_cli run list [--branch <slug>] [--status <state>]`
- `python -m meta_autoresearch_cli run update <run-id> --add-output <kind> <path>`
- `python -m meta_autoresearch_cli run complete <run-id>`

This should still be treated as a support layer, not a final interface.

## Working rule

This layer should automate method overhead, not method judgment.

If the software starts making the process less legible, more opaque, or more autonomous than the current method can justify, it is growing too fast.

## Next iteration

The next infrastructure iteration should target a pressing operational problem: frontier-model token usage and account limits.

The goal is not to replace the frontier model suddenly. The goal is to reduce how much high-cost context and low-complexity work reach it in the first place, then begin bounded delegation of clearly safer tasks to cheaper models.

This next phase should happen in two steps.

### Iteration 2: context compression

Purpose:

- reduce token overhead before a frontier model sees the work
- package branch and run state into smaller, cleaner packets
- lower repeated context reconstruction costs across sessions

Planned additions:

- `branch snapshot` - a more compact branch packet than the current dossier
- `run packet` - a generated packet for one specific pass, including branch state, expected outputs, and only the most relevant artifacts
- `artifact index` - a compact listing of branch notes, scenarios, syntheses, loop runs, discards, and recent runs
- `stale-state detection` - warnings when manifests or generated packets appear out of date
- `comparison prep` - generated comparison tables or summaries from current branch state and selected artifacts

Success criteria:

- a new pass can start from one compact generated packet rather than many manual reads
- branch reconstruction costs fewer frontier-model tokens
- stale branch state becomes visible automatically

### Iteration 3: bounded model delegation

Purpose:

- begin offloading clearly bounded support tasks to more affordable models
- preserve frontier-model use for interpretation, curation, and method judgment

This should use provider-agnostic configuration, with OpenRouter as the first backend.

#### Configuration approach

Recommended environment variables:

- `META_MODEL_BACKEND=openrouter`
- `META_MODEL_DEFAULT_SMALL=<model-id>`
- `META_MODEL_DEFAULT_MID=<model-id>`
- `META_MODEL_DEFAULT_STRONG=<model-id>`
- `OPENROUTER_API_KEY=<key>`
- `OPENROUTER_BASE_URL=https://openrouter.ai/api/v1`

Optional:

- `OPENROUTER_HTTP_REFERER=<url>`
- `OPENROUTER_APP_NAME=meta-autoresearch`

The method should not be tightly coupled to OpenRouter. OpenRouter should be the first backend, not the permanent architecture.

#### Good first delegated tasks

- note summarization
- scenario summarization
- claim extraction
- run-packet compression
- comparison-prep drafting
- branch-manifest suggestions
- evaluation-prefill suggestions

#### Tasks that should remain human or frontier-model tasks for now

- structure-type judgment
- branch-maturity promotion
- curation decisions
- final synthesis
- strategic branch direction

#### Safety rules

- generated model output should go to `meta/generated/`, not directly into `research/`
- generated output should always record task type, model slot, source artifacts, and timestamp
- no delegated command should automatically set branch maturity, structure type, or curation outcomes
- no delegated command should automatically rewrite canonical research artifacts

#### Success criteria

- at least one real pass uses a cheaper model for bounded prep work
- frontier-model token usage decreases meaningfully for that pass
- judgment visibility remains intact
- delegated outputs remain clearly marked as draft/generated

## Recommended build order from here

1. implement Iteration 2 context compression features
2. add provider-agnostic model configuration
3. add OpenRouter as the first backend
4. implement one delegated command such as `summarize-note`
5. implement one delegated comparison-prep command
6. run a real capability-fit test on those delegated tasks before expanding further
