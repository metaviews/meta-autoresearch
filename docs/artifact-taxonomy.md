# Artifact Taxonomy: What the Method Produces

**Status:** draft  
**Date:** 2026-04-02  
**Type:** Method reference

---

## Purpose

This document catalogs the artifacts the meta-autoresearch method naturally produces and distinguishes useful artifacts from ceremonial ones.

It answers:
1. What are the core artifact types and their purposes?
2. What is the minimum viable artifact set for a "complete" branch?
3. What makes an artifact useful vs. ceremonial?
4. Where does each artifact live in the repository?

---

## Artifact Categories

Artifacts are organized into four categories:

| Category | Purpose | Examples |
|----------|---------|----------|
| **State** | Track branch/run state and metadata | Branch manifests, run manifests |
| **Research** | Core research content | Notes, scenarios, experiments |
| **Judgment** | Curation and evaluation decisions | Syntheses, evaluation matrices, discards |
| **Audit** | Process records and history | Loop-run records |

---

## State Artifacts

### Branch Manifest

**Location:** `meta/branches/<slug>.json`  
**Required:** Yes, for all branches  
**Maturity threshold:** L1+

**Purpose:** Structured state tracking for a research branch.

**Key fields:**
```json
{
  "slug": "whiplash",
  "title": "Whiplash",
  "domain": "climate volatility",
  "structure_type": "sequence failure",
  "maturity_level": 4,
  "status": "active",
  "parent_artifact": "research/scenarios/2026-03-27-compound-seasonal-whiplash.md",
  "active_variants": [...],
  "key_notes": [...],
  "key_syntheses": [...],
  "loop_runs": [...],
  "discard_records": [...],
  "strongest_variant": "...",
  "most_generative_variant": "...",
  "weakest_variant": "...",
  "open_questions": [...],
  "next_recommended_pass": "comparison",
  "last_updated": "2026-03-28"
}
```

**What makes it useful:**
- Points to actual artifacts (not orphaned references)
- `next_recommended_pass` is specific and actionable
- `strongest/weakest_variant` reflect actual curation judgments
- Updated after each run completion

**What makes it ceremonial:**
- References artifacts that don't exist or are outdated
- `last_updated` is stale while branch is "active"
- `open_questions` are vague or never revisited
- Maturity level doesn't match actual artifacts

**CLI support:**
```bash
python -m meta_autoresearch_cli branch status <slug>
python -m meta_autoresearch_cli branch check <slug>
python -m meta_autoresearch_cli branch snapshot <slug>
```

---

### Run Manifest

**Location:** `meta/runs/<run-id>.json`  
**Required:** Yes, for all runs  
**Maturity threshold:** L1+

**Purpose:** Track state of a single research pass through the loop.

**Key fields:**
```json
{
  "run_id": "20260327-whiplash-comparison-001",
  "date": "2026-03-27",
  "branch_slug": "whiplash",
  "run_type": "comparison",
  "question": "Which whiplash variant is strongest and why?",
  "stages_targeted": ["stage-6-compare"],
  "expected_outputs": ["comparison-synthesis"],
  "created_outputs": ["research/syntheses/2026-03-27-whiplash-family-comparison.md"],
  "completion_status": "completed",
  "notes": "...",
  "next_step": "run complete"
}
```

**Run types:**
- `grounding` — Anchor branch in evidence
- `variant` — Generate new variants
- `comparison` — Compare existing variants
- `maturity` — Assess cycle maturity
- `discard` — Explicit pruning pass
- `capability-fit` — Test model allocation

**What makes it useful:**
- Clear question and expected outputs
- Actual outputs match expected outputs
- `next_step` is specific
- Completion status reflects reality

**What makes it ceremonial:**
- Run created but never completed
- Expected outputs don't match actual outputs
- No clear question or purpose

**CLI support:**
```bash
python -m meta_autoresearch_cli run new <branch> --type <pass-type>
python -m meta_autoresearch_cli run show <run-id>
python -m meta_autoresearch_cli run check <run-id>
python -m meta_autoresearch_cli run complete <run-id>
python -m meta_autoresearch_cli run packet <run-id>
```

---

## Research Artifacts

### Grounding Note

**Location:** `research/notes/YYYY-MM-DD-topic-grounding-note.md`  
**Required:** Yes, for L2+  
**Maturity threshold:** L2+

**Purpose:** Evidence base for a bounded case or research question.

**Structure:**
```markdown
# Topic Grounding Note

## Metadata
- date: YYYY-MM-DD
- branch: <slug>
- status: draft

## Purpose
What question or case this note grounds.

## Evidence Base
Synthesis of sources (assessed reports, peer-reviewed papers, journalistic reporting).

## Key Findings
What the evidence supports vs. what remains speculative.

## Tensions and Gaps
What the evidence doesn't resolve.

## Implications for Scenarios
How this grounding should constrain or redirect scenario generation.
```

**What makes it useful:**
- Distinguishes source types (assessed report vs. journalistic reporting)
- Explicitly states what is supported vs. speculative
- Materially changes scenario generation (not just decorative)
- Referenced by scenarios and syntheses

**What makes it ceremonial:**
- Summary without constraints (doesn't rule anything out)
- Source types not distinguished
- Written after scenarios (decorative, not grounding)
- Never referenced by later artifacts

**Example:** `research/notes/2026-03-27-feather-river-whiplash-grounding-note.md`

---

### Scenario (Parent and Variant)

**Location:** `research/scenarios/YYYY-MM-DD-scenario-name.md`  
**Required:** Yes, for all branches  
**Maturity threshold:** L1+

**Purpose:** Structured account of a plausible configuration, pathway, or risk pattern.

**Structure:**
```markdown
# Scenario Title

## Metadata
- date: YYYY-MM-DD
- branch: <slug>
- type: parent | variant
- status: draft

## Purpose
What configuration or risk pattern this scenario explores.

## Mechanism
How the scenario unfolds (the causal logic).

## Bounded Case (variants only)
Specific region, system, or institution.

## Evidence Base
What sources support this scenario.

## What This Scenario Reveals
What conventional analysis would miss.

## Uncertainties
What remains unresolved or speculative.

## Relationships
- Parent: (if variant)
- Variants: (if parent)
```

**Parent vs. Variant:**
- **Parent:** Broad scenario family (e.g., "compound seasonal whiplash")
- **Variant:** Bounded case within the family (e.g., "Feather River wet-to-fire whiplash")
- **Method insight:** Structural signal lives in variants, not parents

**What makes it useful:**
- Clear mechanism (not just description)
- Bounded case with named specifics (variants)
- Explicit about what conventional analysis misses
- Distinguishes evidence from speculation

**What makes it ceremonial:**
- Broad scenario without boundaries
- Mechanism is vague or post-hoc
- Could be deleted without loss to branch understanding
- Never referenced by syntheses

**Examples:**
- Parent: `research/scenarios/2026-03-27-compound-seasonal-whiplash.md`
- Variant: `research/scenarios/2026-03-27-feather-river-wet-to-fire-whiplash.md`

---

### Experiment

**Location:** `research/experiments/YYYY-MM-DD-experiment-name.md`  
**Required:** No  
**Maturity threshold:** L2+

**Purpose:** Test of process, prompt structure, evaluation, or curation workflow.

**Structure:**
```markdown
# Experiment Title

## Metadata
- date: YYYY-MM-DD
- type: process | prompt | evaluation | curation
- status: draft

## Question
What the experiment is testing.

## Method
How the test was structured.

## Results
What happened.

## Judgment
Whether the experiment succeeded and what it means.

## Implications
What should change (or not) based on results.
```

**What makes it useful:**
- Clear hypothesis about process improvement
- Results are measurable or observable
- Judgment is explicit (success/failure/partial)
- Implications are acted upon

**What makes it ceremonial:**
- Experiment without clear question
- Results are vague ("seemed to work")
- No judgment or implications
- Never referenced by later work

**Example:** `research/experiments/2026-03-29-whiplash-validation-cycle-report.md`

---

## Judgment Artifacts

### Comparison Synthesis

**Location:** `research/syntheses/YYYY-MM-DD-branch-comparison.md`  
**Required:** Yes, for L3+  
**Maturity threshold:** L3+

**Purpose:** Compare variants to distinguish strongest/weakest and clarify branch structure.

**Structure:**
```markdown
# Branch Comparison

## Metadata
- date: YYYY-MM-DD
- branch: <slug>
- status: draft

## Purpose
What this comparison is deciding.

## Variants Compared
List of variants with brief descriptions.

## Comparison Dimensions
Criteria used for comparison (evidence, coherence, novelty, etc.).

## Judgments
- Strongest variant: X (why)
- Most generative variant: Y (why)
- Weakest variant: Z (why)

## Structure Implications
What the comparison reveals about branch structure.

## Next Step
Recommended pass based on comparison.
```

**What makes it useful:**
- Explicit strongest/weakest judgments
- Comparison dimensions are clear
- Structure implications are specific
- Next step is actionable

**What makes it ceremonial:**
- Lists differences without judging them
- All variants scored similarly (no differentiation)
- Never referenced by branch manifest or later syntheses
- "Strongest" judgment doesn't match branch manifest

**Examples:**
- `research/syntheses/2026-03-27-whiplash-family-comparison.md`
- `research/syntheses/2026-03-28-wealth-concentration-internal-comparison.md`

---

### Evaluation Matrix

**Location:** `research/syntheses/YYYY-MM-DD-branch-evaluation-matrix.md`  
**Required:** Yes, for L3+  
**Maturity threshold:** L3+

**Purpose:** Scored comparison across 8 evaluation dimensions.

**Structure:**
```markdown
# Evaluation Matrix

## Metadata
- date: YYYY-MM-DD
- branch: <slug>
- status: draft

## Variants Evaluated
List of all variants.

## Evaluation Dimensions (1-5 scale)
1. Evidence strength
2. Internal coherence
3. Relevance to research question
4. Preparedness value
5. Novelty and search-space value
6. Actionability for next step
7. Status-quo challenge
8. Imaginative power

## Scores and Rationale
Table with scores and brief rationale for each.

## Curation Decisions
- Variant A: keep (why)
- Variant B: revise (what, why)
- Variant C: discard (why)

## Next Step
Recommended pass based on evaluation.
```

**What makes it useful:**
- Scores vary (not all 4s and 5s)
- Rationale explains scores
- Curation decisions include at least one `revise` or `discard`
- Next step follows from evaluation

**What makes it ceremonial:**
- All variants scored similarly
- Rationale is generic ("well written")
- All variants marked "keep"
- Never referenced by branch manifest

**Example:** `research/syntheses/2026-03-29-wealth-concentration-evaluation-matrix.md`

---

### Discard Record

**Location:** `research/discards/YYYY-MM-DD-discard-name.md`  
**Required:** Yes, for L4  
**Maturity threshold:** L4

**Purpose:** Explicit record of pruned or failed directions.

**Structure:**
```markdown
# Discard Record

## Metadata
- date: YYYY-MM-DD
- branch: <slug>
- status: archived

## What Was Discarded
Description of scenario, variant, or direction.

## Why Discarded
Explicit reasoning (not useful enough, weakly grounded, redundant, etc.).

## What Was Learned
Even discarded directions may have taught something.

## Relationship to Kept Work
How kept variants improved because of this discard.
```

**What makes it useful:**
- Reasoning is specific (not "didn't work out")
- Clear what was learned (even from failure)
- Referenced by branch manifest
- Helps explain why kept variants are stronger

**What makes it ceremonial:**
- Vague reasoning ("not the right fit")
- No clear learning
- Never referenced elsewhere
- Feels like punishment rather than curation

**Examples:**
- `research/discards/2026-03-27-early-climate-discards.md`
- `research/discards/2026-03-28-wealth-concentration-discards.md`

---

### Cross-Branch Synthesis

**Location:** `research/syntheses/YYYY-MM-DD-cross-branch-synthesis.md`  
**Required:** No, but recommended for L4+  
**Maturity threshold:** L4

**Purpose:** Compare multiple branches to extract method-level lessons.

**Structure:**
```markdown
# Cross-Branch Synthesis

## Metadata
- date: YYYY-MM-DD
- branches: [slug1, slug2, ...]
- status: draft

## Purpose
What method question this synthesis addresses.

## Branch Overview
Table comparing branches (domain, structure type, maturity).

## Structure Type Stability
What structure types have emerged and how stable they are.

## Cross-Domain Findings
What portability or generalization looks like.

## Method Lessons
What the method should stop, keep, and start doing.

## Open Questions
What remains unresolved about the method.
```

**What makes it useful:**
- Compares at least 2-3 branches
- Extracts method-level lessons (not just domain content)
- Produces stop/keep/start recommendations
- Referenced by method documents

**What makes it ceremonial:**
- Only summarizes branches without extracting lessons
- No stop/keep/start recommendations
- Never referenced by method documents
- Written for only one branch (not cross-branch)

**Examples:**
- `research/syntheses/2026-03-29-method-lessons-cross-branch-synthesis.md`
- `research/syntheses/2026-03-27-emerging-structure-types-comparison.md`

---

## Audit Artifacts

### Loop-Run Record

**Location:** `research/loops/YYYY-MM-DD-branch-loop-run.md`  
**Required:** Yes, for L3+  
**Maturity threshold:** L3+

**Purpose:** Audit trail of a full research cycle through the 9-stage loop.

**Structure:**
```markdown
# Loop-Run Record

## Metadata
- date: YYYY-MM-DD
- branch: <slug>
- status: complete

## Cycle Summary
Brief description of what this loop accomplished.

## Stages Completed
1. Frame the inquiry: (what happened)
2. Assemble evidence: (what happened)
3. Generate candidates: (what happened)
...
9. Assess cycle maturity: (what happened)

## Artifacts Produced
List of all artifacts created in this loop.

## Curation Decisions
What was kept, revised, discarded, and why.

## Robust vs. Brittle Steps
Which loop steps worked well vs. which struggled.

## Readiness for Scaling
Whether this loop could be repeated or scaled.

## Next Recommended Pass
What should happen next.
```

**What makes it useful:**
- All 9 stages are documented (even if briefly)
- Artifacts produced are listed and linked
- Curation decisions are explicit
- Robust/brittle assessment is honest
- Next pass is specific

**What makes it ceremonial:**
- Stages are copy-pasted without具体内容
- Artifacts list is incomplete
- Curation decisions are vague
- Robust/brittle assessment is missing
- Never referenced by branch manifest

**Examples:**
- `research/loops/2026-03-27-whiplash-loop-run.md`
- `research/loops/2026-03-28-wealth-concentration-loop-run.md`

---

## Minimum Viable Artifact Set

### For a "Complete" Branch (L3+)

A branch should have at minimum:

| Artifact | Count | Purpose |
|----------|-------|---------|
| Branch manifest | 1 | State tracking |
| Grounding note | 1-2 | Evidence base |
| Scenario variants | 2+ | Bounded cases |
| Comparison synthesis | 1 | Strongest/weakest judgment |
| Evaluation matrix | 1 | Scored evaluation |
| Loop-run record | 1 | Audit trail |
| Discard record | 1 | Explicit pruning |

**Total:** 7-8 artifacts minimum for L3

---

### For Method-Shaping (L4)

A branch should additionally have:

| Artifact | Count | Purpose |
|----------|-------|---------|
| Cross-branch synthesis | 1+ | Method-level lesson |
| Structure mapping | 1 | Tests against existing types |
| Method document influence | 1+ | Changes method docs |

**Total:** 10+ artifacts for L4

---

## What Makes Artifacts Useful vs. Ceremonial

### Useful Artifacts

- **Produce real decisions** — keep/revise/discard with reasoning
- **Distinguish strongest from weakest** — not all variants scored equally
- **Change future branch behavior** — later work references this artifact
- **Are referenced by later artifacts** — branch manifest, syntheses, etc.
- **Could not be deleted without loss** — actual content, not filler

### Ceremonial Artifacts

- **Only summarize without sharpening judgment** — lists without decisions
- **Never referenced after creation** — orphaned after initial writing
- **Don't produce curation pressure** — all variants are "keep"
- **Could be deleted without loss** — no one would notice

---

## File Naming Conventions

- **Date-first:** `YYYY-MM-DD-topic.md`
- **Lowercase, kebab-case:** `wealth-concentration-evaluation-matrix.md`
- **Same-day variants:** `-v2`, `-compare` suffixes
- **Type indicators:** `-note`, `-scenario`, `-synthesis`, `-loop-run`

**Examples:**
- `2026-03-27-feather-river-whiplash-grounding-note.md`
- `2026-03-27-whiplash-family-comparison.md`
- `2026-03-27-whiplash-loop-run.md`

---

## Repository Structure

```
meta-autoresearch/
├── meta/
│   ├── branches/           # Branch manifests (JSON)
│   ├── runs/               # Run manifests (JSON)
│   └── generated/          # Generated packets (HTML, draft)
├── research/
│   ├── notes/              # Grounding notes, evidence synthesis
│   ├── scenarios/          # Parent scenarios and variants
│   ├── experiments/        # Process tests and validation
│   ├── discards/           # Pruned/failed directions
│   ├── loops/              # Full cycle audit records
│   └── syntheses/          # Comparisons, evaluations, cross-branch
└── docs/                   # Method documentation
```

---

## Links

- `docs/method.md` — Operational method description
- `docs/research-loop.md` — 9-stage workflow
- `docs/evaluation-framework.md` — Scoring rubric
- `docs/branch-maturity.md` — Maturity level rubric
- `docs/method-guide.md` — Practical application guide
- `meta/branches/` — Branch manifests
- `research/loops/` — Loop-run records

---

*This taxonomy is a living document. Revise when new artifact types emerge or existing types prove inadequate.*
