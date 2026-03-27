# Evaluation Framework

## Purpose

This document makes the evaluation layer explicit for v1.

Meta-autoresearch does not need a perfect universal metric before it can function, but it does need a disciplined way to compare artifacts, prune weak directions, and avoid mistaking eloquence for progress.

It also needs to protect against institutional narrowing. Part of the point of this project is to surface lines of thought that are ignored, suppressed, or treated as implausible too early. The evaluation layer should therefore reward scenarios that challenge stale assumptions and expand imaginative range without collapsing into fantasy.

## What this framework evaluates

In v1, the main evaluated artifact is the `scenario`, though the same logic can later be adapted for notes, experiments, and syntheses.

This framework separates:

- `evidence strength` - how strongly the sources support the scenario's claims
- `scenario value` - how useful the scenario is as an exploratory or preparedness artifact

These should be tracked separately.

## Scoring scale

Use a simple 1-5 scale.

- `1` - weak
- `2` - limited
- `3` - moderate
- `4` - strong
- `5` - very strong

The point is not false precision. The point is to force legible comparative judgment.

## Core evaluation dimensions

### 1. Evidence strength

How well does the available evidence support the scenario's main claims?

- `1` - mostly speculative or weakly sourced
- `3` - partially grounded, but missing important case or literature support
- `5` - strongly grounded in multiple credible sources or cases

### 2. Internal coherence

Does the scenario make sense on its own terms?

- `1` - contradictory or muddled mechanism
- `3` - mostly coherent, but with notable weak links
- `5` - clear mechanism with strong causal structure

### 3. Relevance to the research question

Does the scenario help answer the current inquiry rather than drifting into adjacent material?

- `1` - weakly connected to the current question
- `3` - relevant but somewhat diffuse
- `5` - tightly matched to the stated inquiry

### 4. Preparedness value

Does the scenario surface useful planning, governance, or decision questions?

- `1` - interesting but not decision-useful
- `3` - raises some useful implications
- `5` - clearly sharpens preparedness thinking

### 5. Novelty and search-space value

Does the scenario reveal something default narratives tend to underweight?

- `1` - mostly restates familiar framing
- `3` - adds some useful variation
- `5` - meaningfully expands what the inquiry notices

### 6. Actionability for next research step

Is it clear what should happen next if this scenario is kept?

- `1` - unclear how to refine or test it
- `3` - some next steps are visible
- `5` - obvious next evidence, variant, or comparison pass exists

### 7. Status-quo challenge

Does the scenario productively challenge dominant institutional assumptions, conventional framing, or inherited baseline thinking?

- `1` - largely reproduces the status quo
- `3` - questions some standard assumptions, but within familiar bounds
- `5` - meaningfully challenges entrenched frames in a way that opens new inquiry

### 8. Imaginative power

Does the scenario expand what the inquiry can seriously imagine without detaching from disciplined reasoning?

- `1` - narrow, conventional, or conceptually inert
- `3` - somewhat generative, but still mostly inside familiar patterns
- `5` - materially expands the plausible imaginative range of the research

## Optional supporting dimensions

Use these when needed, but do not require them in every pass.

- source diversity
- geographic specificity
- vulnerability sensitivity
- policy relevance
- ease of decomposition into sub-scenarios

## Curation rubric

Each scenario pass should end with one of four curation outcomes.

### Keep

Use when the scenario is sufficiently coherent and useful to justify continued attention.

Typical pattern:

- moderate to strong evidence
- strong scenario value
- clear next step

### Revise

Use when the scenario is promising but currently too vague, too broad, weakly grounded, or overstated.

Typical pattern:

- strong idea, uneven support
- valuable mechanism, but unclear boundaries
- needs narrowing, grounding, or better structure

### Merge

Use when the scenario does not warrant independent attention and is better treated as a subtype or component of another family.

Typical pattern:

- overlaps strongly with another scenario
- adds detail more than distinct mechanism

### Discard

Use when the scenario does not justify more time.

Typical pattern:

- low evidence and low scenario value
- mostly rhetorical novelty
- no meaningful next step

## Working rule

Every comparison pass should try to identify at least one weaker direction to revise, merge, or discard. If every artifact is always kept, curation is probably too soft.

When a discard or merge is methodologically informative, record it explicitly in `research/discards/` so pruning remains visible and auditable.

## Evaluation output format

When applying this framework, each matrix should record:

- artifact name
- brief mechanism summary
- dimension scores
- short justification notes
- curation decision
- next step

## What this framework is for

This framework is not trying to simulate validation loss. It is trying to keep the inquiry honest while the method is still learning what good outputs look like.
