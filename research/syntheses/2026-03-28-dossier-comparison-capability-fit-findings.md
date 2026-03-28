# Dossier Comparison Capability-Fit Findings

## Metadata

- title: Dossier Comparison Capability-Fit Findings
- date: 2026-03-28
- author: OpenCode
- status: draft
- type: method synthesis

## Purpose

Summarize what the second capability-fit experiment shows about local support for comparison prep.

## Main finding

`Comparison prep` is now a plausible local-tooling responsibility.

Not comparison judgment itself, but the setup for it.

That includes:

- listing branch maturity and next-pass distribution
- generating dossier packets for candidate branches
- listing run history so recent branch attention is visible

## What this means

The process can now divide more cleanly:

### Local tooling can handle

- state aggregation
- branch packet generation
- run history inspection
- basic maturity-aware warnings

### Stronger judgment still handles

- choosing which comparison matters most
- deciding whether a branch is truly overdeveloped or underdeveloped
- interpreting what a comparison changes in the method

## Why this is useful

This shifts a comparison pass from:

- reconstruct the branch manually
- remember which variant is strongest
- remember which artifacts exist
- remember what the branch is missing

to:

- inspect the dossier
- inspect branch/run lists
- start the real judgment work earlier

## Capability-fit judgment

### Good candidate for local tooling now

- branch list
- branch dossier
- run list
- run inspection

### Still not a good candidate for local tooling alone

- branch-priority selection
- structure-type comparison
- maturity promotion decisions
- final method synthesis

## Main conclusion

The first CLI layer is now doing two useful things safely:

1. reducing pass overhead
2. creating better entry conditions for comparison and maturity work

That is an important incremental gain. It means the method is beginning to separate `preparing a pass` from `judging a pass`, which is exactly the kind of modularity that later model allocation will need.

## Links

- related experiments:
  - `research/experiments/2026-03-28-dossier-comparison-capability-fit-pass.md`
  - `research/experiments/2026-03-28-cli-capability-fit-pass.md`
- related syntheses:
  - `research/syntheses/2026-03-28-cli-capability-fit-findings.md`
