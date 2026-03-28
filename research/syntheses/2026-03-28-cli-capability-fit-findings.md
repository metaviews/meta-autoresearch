# CLI Capability-Fit Findings

## Metadata

- title: CLI Capability-Fit Findings
- date: 2026-03-28
- author: OpenCode
- status: draft
- type: method synthesis

## Purpose

Summarize what the first capability-fit experiment shows about where local tooling can already replace coordination overhead and where stronger judgment is still required.

## Main finding

The first successful delegation target is not research judgment. It is `method overhead`.

That includes:

- branch-state recovery
- run scaffolding
- expected-output tracking
- dossier generation
- run inspection
- run completion checks

These tasks are structured enough to move into a local CLI without distorting the method.

## What the CLI can now do safely

- recover branch state from `meta/branches/*.json`
- validate branch hygiene against current expectations
- scaffold a run with expected outputs
- record created outputs and completion state
- show a run in a readable format without opening raw JSON

## What still clearly requires stronger judgment

- deciding whether a source changes the branch materially
- deciding whether a branch should be promoted or revised
- interpreting structure-type emergence
- writing final comparison syntheses
- deciding what deserves scale rather than only attention

## Why this matters

This is the first explicit evidence that process efficiency can improve before any serious research autonomy is attempted.

That matters because the project wants gradual scale, not a dramatic leap. The CLI already shows a path where modest local tooling increases useful throughput while preserving the method's central discipline.

## Capability-fit judgment

### Good candidate for local tooling now

- state tracking
- run lifecycle management
- branch dossier generation
- artifact validation

### Not yet a good candidate for local tooling alone

- source interpretation
- branch maturity judgment
- structure-type promotion
- final cross-branch synthesis

## Process implication

The next capability-fit experiments should stay bounded.

Good next tests:

- stronger branch-check rules
- branch index or run listing commands
- generated comparison tables from known manifests

Bad next tests right now:

- automatic scenario writing without review
- automatic structure-type classification
- automated promotion/demotion of branches

## Main conclusion

The first CLI layer succeeds because it reduces coordination cost without pretending to reduce epistemic cost.

That is the right kind of gain for this phase of the project.

## Links

- related experiments:
  - `research/experiments/2026-03-28-cli-capability-fit-pass.md`
- related syntheses:
  - `research/syntheses/2026-03-27-method-lessons-so-far.md`
  - `research/syntheses/2026-03-27-emerging-structure-types-comparison.md`
