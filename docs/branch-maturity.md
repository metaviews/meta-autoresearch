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
- explicit subtype distinctions documented (if variants cluster by mechanism)

### Level 5: generalizable

The branch's structure type is genuinely generalizable — it can be templated for independent use, integrated with other research methods, triggers method evolution, and optionally receives prospective validation from real-world events.

**L5 Criteria (All Required):**

- **Template reusability** — Method guide is clear enough for external researcher to independently create a new branch using this branch as template; new branch reaches L3+
- **Cross-method integration** — Structure type maps to and integrates with concepts from at least one other research method (resilience engineering, systems thinking, complexity science); integration produces insights neither method could produce alone
- **Method evolution** — Branch triggers revision of method documents that goes beyond adding content (e.g., new structure type, new loop stage, new evaluation dimension, new maturity criterion)

**L5 Criteria (Optional Validator):**

- **Prospective validation** — Branch identifies specific risk pathway or structural vulnerability; real-world event validates the pathway; post-event analysis confirms the structure type predicted the failure mode

**Why prospective validation is optional, not required:**
The method's purpose is to identify emergent phenomena that conventional analysis tends to ignore. Requiring prospective validation would limit the method to phenomena that have already manifested, import confirmation bias from existing research culture, and penalize branches that identify genuinely novel risks. Prospective validation influences confidence but does not limit what qualifies as L5.

Typical signs:

- structure type validated across 2+ domains (e.g., climate + non-climate)
- branch template reusable by another researcher
- method documents explicitly reference this branch's structure
- hybrid structure (if applicable) documented as stable form with all components tested
- structure type integrated with at least one external research method
- method has evolved (new stage, dimension, or criterion) triggered by this branch

## Hybrid structure criteria

For branches with hybrid structure_type (e.g., correlation/transmission + design/rule conflict):

- **All components must be tested** — A variant that tests only one component does not earn active status
- **Hybrid stability documented** — Is the hybrid a stable form or intermediate state?
- **Component interaction mapped** — How do the components interact? Are they independent or compounding?
- **Non-climate grounding earlier** — Hybrid branches outside climate need named cases sooner

### Multi-component hybrids (3+ components)

The avian-flu-zoonotic branch revealed that hybrids can have more than 2 components:

- **Component count matters** — 2-component hybrids (wealth-concentration) differ from 3-component hybrids (HPAI)
- **Complexity scales with components** — More components require more grounding evidence
- **Each component needs validation** — Cross-branch comparison should validate each component against existing structure types
- **L4 requires all components tested** — A 3-component hybrid needs grounding for all three components before L4

## Non-climate portability criteria

For branches testing non-climate domains:

- **Bounded grounding required earlier** — Non-climate branches need named cases before variant generation
- **Hybrid status legitimate** — Non-climate branches may arrive as hybrid; this is intermediate, not failure
- **Three domains shows pattern** — One domain is suggestive, two is a pattern, three demonstrates method-shaping
- **Public good dimension tracked** — If the domain has public good dimensions (e.g., health security), document how this affects structure

## Current provisional read

- `breadbasket` - Level 4: method-shaping, now strong at both upstream wheat-node comparison and downstream importer-archetype mapping, making it the clearest branch for deciding when a mature line should stop expanding and start redirecting attention
- `whiplash` - Level 4: method-shaping, now strong enough to stabilize `sequence failure` as a reusable structure with grounded variants, explicit pruning context, and a full loop record
- `hydrologic` - Level 4: method-shaping, now strong enough to stabilize `design/rule conflict under volatility` as a distinct emerging structure type rather than only a comparative branch
- `wealth-concentration` - Level 4: method-shaping (hybrid portability demonstrated), first non-climate proving-ground branch; demonstrated that portability may arrive as hybrid before resolving to dominant structure; influenced method understanding of how structure types travel across domains
- `avian-flu-zoonotic` - Level 3: comparative, first biological volatility branch; 3-component hybrid (correlation + sequence + design/rule) validated against existing structure types; cross-branch comparisons confirmed component similarity with breadbasket and whiplash

## Hybrid structures

Non-climate portability may arrive as a **hybrid** of multiple structure types rather than mapping cleanly to one.

**Key findings:**
- Hybrid status is legitimate, not a failure mode
- Portability may arrive in stages: thematic → structural resonance → hybrid → resolved → method-shaping
- The hybrid finding itself is methodologically valuable—it changes how future non-climate branches are evaluated
- Multi-component hybrids (3+) are possible and require more grounding than 2-component hybrids

**For future branches:**
- Test for hybrid status explicitly during structure mapping
- Do not force branches into single-structure boxes if overlap is real
- Hybrid at L3 is expected; hybrid at L4 needs to demonstrate method influence (as wealth-concentration did)
- Multi-component hybrids (3+) need grounding for all components before L4

## Working rule

Do not use maturity level as a proxy for importance. Some lower-maturity branches may be more conceptually valuable than higher-maturity ones. The point is to judge development state, not significance.

## Method influence tracking

L4 branches should influence method documents, not just research artifacts. Track influence type:

- **Direct influence** — Branch findings triggered revision to method documents (this document, evaluation-framework.md, research-loop.md)
- **Indirect influence** — Branch findings referenced in cross-branch synthesis but no method document revision

**Examples:**
- wealth-concentration: Direct (hybrid structure guidance added to this document)
- hydrologic: Direct (design/rule conflict subtype distinctions added to evaluation-framework.md)
- breadbasket: Indirect (importer archetype findings in synthesis, no method doc revision yet)
- whiplash: Direct (sequence subtype distinctions added to evaluation-framework.md)
- avian-flu-zoonotic: Direct (multi-component hybrid criteria added to this document, biological volatility accommodation added to evaluation-framework.md)

## Next use

Apply this rubric whenever:

- choosing which branch to deepen next
- deciding whether a branch is ready for loop repetition
- deciding whether a branch supports a distinct structure type strongly enough to formalize
