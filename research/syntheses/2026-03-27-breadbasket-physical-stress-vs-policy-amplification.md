# Breadbasket Physical Stress vs Policy Amplification

## Metadata

- title: Breadbasket Physical Stress vs Policy Amplification
- date: 2026-03-27
- author: OpenCode
- status: draft
- type: branch synthesis

## Purpose

Clarify a central design question in the breadbasket branch: how much of the real preparedness problem comes from the physical climate shock itself, and how much comes from policy, trade, and market amplification after the shock arrives?

## Core distinction

The breadbasket branch now has enough structure to distinguish two layers of risk.

### 1. Physical stress

This is the climate layer:

- compound hot-dry growing-season conditions
- correlated stress across major crop regions
- reduced yields or lower production confidence

The current repo is strongest on this layer. Heino et al. (2023) and Gaupp et al. (2020) support the claim that correlated crop stress, especially for wheat, is a meaningful and growing concern.

### 2. Policy amplification

This is the system-response layer:

- export restrictions
- reserve strain
- procurement panic
- price escalation
- unequal downstream exposure

The branch is now becoming stronger on this layer through the Russia shock analog and MENA sensitivity literature, but it remains less fully grounded than the physical stress layer.

## Why the distinction matters

If the branch treats all downstream harm as if it were directly caused by climate alone, it becomes sloppy and overstated.

If it ignores policy amplification, it misses the actual preparedness failure, because importers and humanitarian systems often experience the shock through prices, trade constraints, and access problems rather than directly through the weather itself.

The correct framing is interactive:

- physical stress narrows supply and confidence
- policy and market responses determine how severe and uneven the downstream consequences become

## Current branch structure

### Parent family

- `research/scenarios/2026-03-27-synchronous-breadbasket-stress.md`

This remains the broad family statement: correlation matters because reduced substitutability can destabilize the system.

### First focused branch

- `research/scenarios/2026-03-27-northern-wheat-correlation-shock.md`

This adds the core interaction: physical wheat stress plus export restriction risk plus import dependence.

### First comparison variant

- `research/scenarios/2026-03-27-russia-europe-wheat-trade-shock.md`

This sharpens the question further by asking what happens when both the main transmission node and one of its major substitute export buffers are weakened together.

## Working judgment

At this stage, the branch should explicitly treat `physical stress` and `policy amplification` as separate but linked evaluation categories.

Why:

- some scenario variants may be stronger on climate evidence than on trade evidence
- some may be very useful preparedness prompts because they reveal amplification pathways even if the physical case remains only moderate
- keeping the categories separate makes the branch more honest and more operational

## Implications for further work

- future notes should specify whether a claim is about crop stress, trade structure, price transmission, or policy response
- future scenario variants should avoid implying that price spikes are mechanically proportional to yield loss
- comparisons should ask not only "which crop-region pair is most exposed?" but also "which policy responses make exposure worse or better?"

## Main conclusion

The breadbasket branch is strongest when it is framed as `correlation plus amplification`, not as climate stress alone.

That is the point where it most clearly serves the broader project: it uncovers how institutional and market assumptions suppress or misread risks that look manageable if each region is considered separately.

## Next move

Use the Russia-Europe wheat variant to test a more explicit importer and reserve lens, and only then build the next comparison against a production-buffer case such as Russia-China.

## Links

- related notes:
  - `research/notes/2026-03-27-breadbasket-regional-grounding-note.md`
  - `research/notes/2026-03-27-northern-wheat-shock-grounding-note.md`
  - `research/notes/2026-03-27-wheat-second-node-comparison-note.md`
- related scenarios:
  - `research/scenarios/2026-03-27-synchronous-breadbasket-stress.md`
  - `research/scenarios/2026-03-27-northern-wheat-correlation-shock.md`
  - `research/scenarios/2026-03-27-russia-europe-wheat-trade-shock.md`
- related syntheses:
  - `research/syntheses/2026-03-27-first-scenario-family-synthesis.md`
