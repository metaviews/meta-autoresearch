# Branch Maturity

## Purpose

This document provides a lightweight rubric for judging how mature a branch is inside the meta-autoresearch process.

It is not a ranking of importance. It is a way to assess how developed, grounded, comparable, and reusable a branch currently is.

## Why this exists

As the repository grows, branches can feel equally substantial even when they are not. A maturity rubric helps the project:

- distinguish strong families from early promising ones
- decide where to deepen next
- know when a branch is mature enough for loop repetition or scaling experiments
- avoid confusing conceptual promise with operational maturity

## Branch maturity dimensions

Use these dimensions qualitatively. A branch does not need to be perfect in all of them.

### 1. Framing clarity

- Is the branch mechanism clear?
- Is it more than a topical bucket?
- Does it resist collapse into generic language?

### 2. Evidence grounding

- Does the branch have source-backed notes?
- Is the core mechanism supported beyond broad plausibility?
- Are key evidence gaps visible?

### 3. Variant structure

- Does the branch have more than one meaningful variant or case?
- Are the variants structurally different rather than stylistically different?

### 4. Comparison depth

- Has the branch gone through a real comparison pass?
- Can it distinguish strongest, most generative, and most provisional variants?

### 5. Curation pressure

- Has the branch produced explicit `keep`, `revise`, `merge`, or `discard` judgments?
- Has pruning changed the branch materially?

### 6. Loop auditability

- Does the branch have a loop-run record?
- Can someone reconstruct how it changed over time?

### 7. Structural contribution

- Does the branch support, refine, or challenge an emerging structure type?
- Does it change the method, or only populate it with more content?

## Maturity levels

### Level 1: exploratory

The branch has a plausible idea, but little grounding and no real internal structure yet.

Typical signs:

- mostly abstract framing
- little or no case grounding
- no meaningful comparison

### Level 2: grounded

The branch has at least one named case or stronger evidence base and is no longer only conceptual.

Typical signs:

- one grounded variant or case
- improved coherence after evidence review
- still limited comparison structure

### Level 3: comparative

The branch has multiple meaningful variants and has been compared internally.

Typical signs:

- real comparison synthesis exists
- strongest and weakest variants are legible
- curation begins to sharpen the branch

### Level 4: method-shaping

The branch not only works on its own terms, but changes how the method understands structure, evaluation, or loop design.

Typical signs:

- branch supports an emerging structure type
- loop-run record is strong and reusable
- branch influences method documents, not only research artifacts

## Current provisional read

- `breadbasket` - Level 4: method-shaping
- `whiplash` - Level 3 to 4: comparative and method-shaping, but still somewhat lighter on chronology than breadbasket is on transmission
- `hydrologic` - Level 4: method-shaping, now strong enough to stabilize `design/rule conflict under volatility` as a distinct emerging structure type rather than only a comparative branch

## Working rule

Do not use maturity level as a proxy for importance. Some lower-maturity branches may be more conceptually valuable than higher-maturity ones. The point is to judge development state, not significance.

## Next use

Apply this rubric whenever:

- choosing which branch to deepen next
- deciding whether a branch is ready for loop repetition
- deciding whether a branch supports a distinct structure type strongly enough to formalize
