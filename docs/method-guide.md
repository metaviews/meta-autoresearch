# Method Guide: How to Apply Meta-Autoresearch

**Status:** draft  
**Date:** 2026-04-02  
**Type:** Method guide

---

## Purpose

This document is a practical guide for applying the meta-autoresearch method to a new domain or research question.

It answers:
1. How do I start a new branch?
2. What are the structure types and how do I recognize them?
3. What does the maturity model (L1-L4) look like with examples?
4. What are common failure modes and how do I fix them?

---

## Getting Started

### Prerequisites

Before starting a new branch, ensure you have:

- [ ] A research question that resists premature closure (not a prediction target)
- [ ] Climate volatility or another domain where historical baselines are breaking down
- [ ] Willingness to generate multiple distinct directions before curating
- [ ] Commitment to explicit curation (keep/revise/discard with reasoning)

### When NOT to Use This Method

This method is **not** appropriate for:

- Authoritative forecasting (use domain-specific prediction models)
- Questions with settled scientific consensus
- Work that requires a single definitive answer quickly
- Domains where stationarity still holds and baselines are reliable

---

## Starting a New Branch

### Step 1: Frame the Inquiry

**Goal:** Define what you're exploring and why it matters.

**Create:**
- A branch slug (lowercase, kebab-case, e.g., `wealth-concentration`)
- A working title
- A provisional structure type hypothesis (or "unknown" if exploratory)
- A research question

**Example:**
```
Slug: wealth-concentration
Title: Wealth Concentration
Domain: political economy
Structure type: unknown (exploratory)
Question: How does wealth concentration create structural fragility that conventional analysis misses?
```

**Gate to continue:** Is the question clear enough to generate against without collapsing into prediction?

---

### Step 2: Assemble Starting Evidence

**Goal:** Build minimum source base to prevent unsupported prose.

**Create:**
- 1-2 grounding notes synthesizing available evidence
- Record of sources (assessed reports, peer-reviewed papers, journalistic reporting)
- Early tensions or gaps in the evidence

**File pattern:** `research/notes/YYYY-MM-DD-topic-grounding-note.md`

**Gate to continue:** Do you have enough grounding to generate bounded scenarios, not just broad speculation?

---

### Step 3: Generate Candidate Branches

**Goal:** Produce multiple scenario directions that differ in mechanism.

**Create:**
- 3-5 exploratory scenarios with distinct mechanisms
- Early curation notes on which feel most promising

**File pattern:** `research/scenarios/YYYY-MM-DD-parent-scenario.md`

**Gate to continue:** Are the branches meaningfully distinct (not just stylistic variants)?

---

### Step 4: Ground the Most Promising Branch

**Goal:** Anchor one promising branch in stronger evidence and named cases.

**Create:**
- Revised parent scenario with clearer boundaries
- 1-2 grounding notes with specific regions, systems, or cases
- Explicit statement of what is supported vs. speculative

**File pattern:** `research/notes/YYYY-MM-DD-bounded-case-grounding-note.md`

**Gate to continue:** Is the branch still too broad to test, or has grounding made it more honest?

---

### Step 5: Create Branch Variants

**Goal:** Test whether the branch survives translation into multiple named cases.

**Create:**
- 2-4 regional or mechanism variants
- Each variant should be a bounded case (not a broad scenario)

**File pattern:** `research/scenarios/YYYY-MM-DD-bounded-variant.md`

**Gate to continue:** Do the variants reveal a real family structure (not just rhetorical differences)?

---

### Step 6: Compare the Variants

**Goal:** Use comparison to decide which variant is strongest and what the branch actually is.

**Create:**
- Comparison synthesis distinguishing strongest/weakest variants
- Explicit judgment on which mechanism is most useful
- Structure mapping (if non-climate: test against existing structure types)

**File pattern:** `research/syntheses/YYYY-MM-DD-branch-comparison.md`

**Gate to continue:** Does comparison produce sharper curation? Is at least one variant clearly weaker?

---

### Step 7: Evaluate and Curate

**Goal:** Apply formal evaluation so the branch is judged explicitly.

**Create:**
- Evaluation matrix scoring all variants across 8 dimensions (see `docs/evaluation-framework.md`)
- Curation decisions: keep/revise/discard for each variant
- Branch-specific next step

**File pattern:** `research/syntheses/YYYY-MM-DD-branch-evaluation-matrix.md`

**Gate to continue:** Is the branch worth deeper investment? Does evidence support confidence level?

---

### Step 8: Synthesize Across Branches

**Goal:** Identify what epistemic structure the branch reveals.

**Create:**
- Cross-branch comparison (if multiple branches exist)
- Emerging structure types reflection
- Method-level lesson: what does this branch teach the method?

**File pattern:** `research/syntheses/YYYY-MM-DD-method-lesson.md`

**Gate to continue:** Has the work revealed a reusable structure, or only more domain content?

---

### Step 9: Assess Cycle Maturity

**Goal:** Decide whether the cycle is ready to be repeated or scaled.

**Create:**
- Loop-run record documenting the full cycle
- List of robust vs. brittle steps
- Decision: rerun, deepen, redirect, or stop

**File pattern:** `research/loops/YYYY-MM-DD-branch-loop-run.md`

**Gate to continue:** Are failure modes understood well enough to repeat? Would scaling produce signal or noise?

---

## Structure Type Reference

Use this reference to recognize which structure type your branch may be revealing.

### Sequence Failure

**Recognizing features:**
- Risk emerges from a **chain of conditions**, not isolated events
- The **transition mechanism** between states carries the risk
- Conventional analysis treats phases/seasons as separate problems

**Questions to ask:**
- What sequence of conditions would create failure that no single condition would predict?
- What transition (wet-to-dry, stable-to-volatile, growth-to-contraction) is conventionally misunderstood?
- What baseline assumptions treat sequence elements as independent?

**Example:** Whiplash (climate) — Fast wet-to-dry transitions create risks that neither wet nor dry seasons alone would predict.

---

### Correlation/Transmission Failure

**Recognizing features:**
- Risk emerges from **coupled systems**, not isolated nodes
- **Transmission pathways** amplify rather than absorb shocks
- Conventional analysis treats distributed problems as local/independent

**Questions to ask:**
- What distributed nodes are more correlated than conventional analysis assumes?
- What transmission pathways (trade, finance, information) could amplify local shocks?
- What downstream exposure varies by institutional capacity, not just by dependence?

**Example:** Breadbasket (climate) — Synchronous crop failures across regions create systemic risk that regional analysis alone would miss.

---

### Design/Rule Conflict Under Volatility

**Recognizing features:**
- Risk emerges from **mismatch between rules and reality**
- Infrastructure or institutions designed for **stationarity** face **non-stationarity**
- The conflict is invisible to operators inside the system

**Questions to ask:**
- What rules, thresholds, or allocation frameworks were designed for conditions that no longer exist?
- What infrastructure purpose conflicts with current system dynamics?
- What breakdown would be second-order (not the event itself, but institutional failure in response)?

**Example:** Hydrologic (climate) — Water infrastructure rules designed for drought face reality of whiplash flooding.

---

### Hybrid Structures

**Recognizing features:**
- Branch overlaps multiple structure types
- Different variants map to different structures
- Resolution to single structure is unclear after grounding

**Questions to ask:**
- Does the branch reveal multiple structures at different levels of analysis?
- Is hybrid status an intermediate form (needs more grounding) or stable outcome (inherently multi-structure)?
- What would resolution look like, and is it necessary?

**Example:** Wealth-concentration (political economy) — Overlaps correlation/transmission (wealth flows) and design/rule conflict (asset regimes built for different conditions).

**Guidance:** Hybrid status is legitimate. Don't force single-structure mapping if the branch genuinely reveals multiple structures. Document the hybrid and let future grounding clarify resolution.

---

## Maturity Model (L1-L4)

Use this rubric to judge branch maturity and identify next steps.

### Level 1: Early Exploration

**Characteristics:**
- Broad exploratory scenarios
- Limited grounding in named cases
- No formal comparison or curation

**Artifacts:**
- Parent scenario (1-2)
- Early notes (optional)

**Next step:** Ground in bounded cases

---

### Level 2: Bounded Grounding

**Characteristics:**
- At least one grounding note with named cases
- Parent scenario revised with clearer boundaries
- Early variant generation

**Artifacts:**
- Parent scenario (revised)
- Grounding note (1-2)
- Early variants (1-2)

**Next step:** Generate more variants and compare

---

### Level 3: Comparative

**Characteristics:**
- Multiple grounded variants (2+)
- Internal comparison exists
- Explicit curation decisions
- Loop-run record exists

**Artifacts (all required):**
- Grounded variants (2+)
- Comparison synthesis
- Evaluation matrix
- Loop-run record
- Discard record (at least one)

**Next step:** Deepen, redirect, or push to L4

**Example:** Wealth-concentration achieved L3 with 4 variants, 5 syntheses, explicit curation, and loop record.

---

### Level 4: Method-Shaping

**Characteristics:**
- All L3 criteria met
- Supports or clarifies a reusable structure type
- Influences method documents (not just research artifacts)
- Loop-run record is strong enough to be reused as template

**Artifacts (all L3 +):**
- Cross-branch synthesis or method-level reflection
- Structure mapping that changes how structure is understood
- Method document influence (e.g., this guide, what-we-learned.md)

**Next step:** Publish, redirect, or test portability

**Example:** Whiplash, breadbasket, and hydrologic achieved L4 by stabilizing sequence failure, correlation/transmission, and design/rule conflict as reusable structure types.

---

## Common Failure Modes and Fixes

### Failure Mode 1: Scenarios Remain Broad After Grounding

**Symptoms:**
- Grounding notes don't materially narrow the parent scenario
- Variants are still too broad to be testable
- "Grounding" is just adding detail, not adding boundaries

**Fix:**
- Require named cases (specific regions, systems, institutions)
- Ask: "What would make this scenario falsifiable?"
- Split broad scenarios into multiple bounded variants

---

### Failure Mode 2: Variants Differ Only in Style

**Symptoms:**
- Variants have different wording but same underlying mechanism
- Comparison synthesis can't distinguish strongest from weakest
- All variants score similarly on evaluation matrix

**Fix:**
- Generate variants with different mechanisms, not different examples
- Ask: "What would make one variant right and another wrong?"
- Consider discarding and regenerating variants

---

### Failure Mode 3: Curation Never Produces Discards

**Symptoms:**
- All variants are marked "keep" or "revise"
- No discard records exist
- Evaluation matrix produces similar scores across all variants

**Fix:**
- Require at least one `discard` or `revise` per mature branch
- Ask: "What variant is least useful and why?"
- If every artifact is always kept, curation is too soft

---

### Failure Mode 4: Evidence Notes Don't Change Scenarios

**Symptoms:**
- Grounding notes are summaries, not challenges
- Scenarios written before grounding remain unchanged after
- Evidence is decorative, not constraining

**Fix:**
- Write grounding notes **before** generating variants
- Ask: "What does this evidence rule out?"
- Revise parent scenario if grounding contradicts initial framing

---

### Failure Mode 5: Syntheses Only Summarize

**Symptoms:**
- Comparison syntheses list differences without judging them
- No sharpening of judgment across artifacts
- Syntheses are never referenced by later work

**Fix:**
- Require explicit strongest/weakest judgments in every comparison
- Ask: "What decision does this synthesis enable?"
- Treat syntheses as decision tools, not summaries

---

### Failure Mode 6: Hybrid Status Causes Paralysis

**Symptoms:**
- Branch can't decide between structure types
- Structure mapping produces multiple equally-plausible fits
- Progress stalls waiting for resolution

**Fix:**
- Accept hybrid as legitimate intermediate (or stable) status
- Document the hybrid explicitly: "This branch overlaps X and Y"
- Let future grounding clarify resolution (or don't require it)

---

### Failure Mode 7: Method Influence Is Assumed, Not Demonstrated

**Symptoms:**
- Branch claims L4 without changing method documents
- Structure type is asserted, not stabilized through use
- "Method-shaping" is self-declared, not evidenced

**Fix:**
- L4 requires external validation: does another branch use this structure?
- Ask: "What method document does this branch change?"
- Write method-level reflection that demonstrates influence

---

## CLI Commands for Branch Development

Use these commands to support branch development:

```bash
# Create branch manifest (manual, then update)
# Edit meta/branches/<slug>.json

# Check branch status
python -m meta_autoresearch_cli branch status <slug>

# Run method hygiene check
python -m meta_autoresearch_cli branch check <slug>

# Generate branch packet (snapshot + index + compare-prep)
python -m meta_autoresearch_cli delegate branch-packet <slug>

# Start a new run (grounding, variant, comparison, maturity, discard)
python -m meta_autoresearch_cli run new <slug> --type <pass-type>

# Complete a run and update branch state
python -m meta_autoresearch_cli run complete <run-id>
```

---

## Minimum Viable Successful Branch

A branch should not count as successful just because it produced interesting scenarios.

At minimum, a good branch should produce:

- [ ] One bounded branch (not just broad parent scenario)
- [ ] One grounding note with named cases
- [ ] More than one variant or comparison target
- [ ] One explicit curation judgment (keep/revise/discard)
- [ ] One synthesis explaining what the branch taught the method

---

## Links

- `docs/foundation.md` — Conceptual framing
- `docs/method.md` — Operational method description
- `docs/research-loop.md` — 9-stage workflow
- `docs/evaluation-framework.md` — Scoring rubric
- `docs/branch-maturity.md` — Maturity level rubric
- `docs/what-we-learned.md` — Method findings synthesis
- `meta/branches/` — Branch manifests
- `research/loops/` — Loop-run records

---

*This guide is a living document. Revise when practice shows a step is missing, redundant, or out of order.*
