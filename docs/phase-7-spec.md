# Phase 7 Tooling Specification

**Status:** draft  
**Date:** 2026-04-02  
**Type:** Infrastructure plan

---

## Purpose

This document specifies Phase 7 tooling requirements based on the consolidated method from v1.

It answers:
1. What tooling would make the method more usable?
2. What should be built vs. what should remain manual?
3. What is the minimum viable Phase 7 scope?

---

## Context

### What v1 Achieved

- 4 research branches at L3+ (3 at L4: whiplash, breadbasket, hydrologic)
- 3 stable epistemic structure types (sequence, correlation, design/rule)
- Non-climate portability demonstrated (wealth-concentration at L3)
- CLI infrastructure for branch/run state, delegation, orchestration
- Method documentation consolidated (what-we-learned, method-guide, artifact-taxonomy, foundation-questions)

### What v1 Learned About Tooling

- Infrastructure should automate coordination overhead, not method judgment
- Generated artifacts stay in `meta/generated/`, marked as draft
- Model delegation works but requires context compression first
- 10-cycle test: ~$0.003/cycle, 0 failures, ~2.7 minutes per cycle
- 60% coordination overhead reduction from workflow automation

### The Phase 7 Question

**Should the project build product complexity around the method?**

The roadmap identifies possible next steps:
- Static site for publishing scenarios and syntheses
- Lightweight research tooling for scenario generation and curation
- Structured data model for reusable scenario components
- Model orchestration for repeated research cycles

---

## Design Principles

### From v1 Method Lessons

1. **Do not automate judgment** — Tools reduce coordination overhead, not curation responsibility
2. **Keep method auditable** — Every tool action should leave a trace
3. **Distinguish draft from final** — Generated output is never auto-published
4. **Optimize for capability fit** — Use weakest model that can do the task well enough
5. **Preserve human/AI division** — AI generates, human curates

### For Phase 7

1. **Publishing should serve the method** — Not the other way around
2. **Tooling should enable cycles** — Not add overhead
3. **Structure should be reusable** — Components, not just documents
4. **Audience matters** — Tools should match intended users

---

## Tooling Options

### Option 1: Static Site for Publishing

**Purpose:** Make scenarios and syntheses publicly accessible.

**What it would do:**
- Generate static HTML from markdown artifacts
- Organize by branch, structure type, maturity level
- Include method documentation (what-we-learned, method-guide, etc.)
- Distinguish public vs. internal artifacts

**What it would NOT do:**
- Auto-publish drafts (all output marked draft until reviewed)
- Publish grounding notes or loop-run records (internal process artifacts)
- Allow comments or interaction (read-only publication)

**Technical approach:**
- Use existing static site generator (MkDocs, Hugo, Jekyll)
- Configure publication rules in `mkdocs.yml` or similar
- Publish to GitHub Pages or Netlify

**Effort estimate:** 2-3 days for initial setup

**Value:**
- Makes method accessible to external users
- Creates accountability for claims
- Enables collaboration and critique

**Risk:**
- Publishing before method is fully validated
- Artifacts are drafts, not final claims
- May create pressure to publish over curate

**Recommendension:** **Defer until after v1 validation is complete.** First publish method findings as a paper or long-form essay, then build site if audience demand warrants it.

---

### Option 2: Structured Data Model for Scenario Components

**Purpose:** Make scenario components reusable across branches.

**What it would do:**
- Extract structured data from scenarios (regions, mechanisms, evidence types)
- Enable cross-branch component search ("show all sequence failure cases")
- Support scenario generation from reusable components
- Track component reuse across artifacts

**Data model sketch:**
```yaml
Component:
  id: unique-identifier
  type: region | mechanism | evidence | institution
  name: human-readable name
  description: markdown
  related_branches: [slug1, slug2]
  related_artifacts: [path1, path2]
  metadata:
    domain: climate volatility | political economy | ...
    structure_type: sequence | correlation | design/rule | hybrid
```

**What it would NOT do:**
- Auto-generate scenarios without human curation
- Replace markdown artifacts (structured data is index, not replacement)
- Enforce component usage (components are suggestions, not requirements)

**Technical approach:**
- Add `meta/components/` directory with YAML manifests
- CLI command: `component index` — build component index
- CLI command: `component search <query>` — find relevant components
- CLI command: `component suggest <branch>` — suggest components for new branch

**Effort estimate:** 3-5 days for initial implementation

**Value:**
- Makes cross-branch patterns more legible
- Reduces duplication across scenarios
- Enables more systematic scenario generation

**Risk:**
- Over-structuring early-stage research
- Components may not generalize across domains
- May encourage component assembly over genuine insight

**Recommendation:** **Build minimal version.** Start with simple component indexing (no generation), test on existing branches, expand only if components prove reusable.

---

### Option 3: Model Orchestration Dashboard

**Purpose:** Monitor and manage repeated research cycles.

**What it would do:**
- Show cycle progress dashboard (already exists: `orchestrator status`)
- Track costs per branch, per cycle, per task type
- Alert on failed cycles or unusual cost patterns
- Support A/B testing of model configurations

**What it would NOT do:**
- Auto-start cycles without human initiation
- Auto-curate output (all output still requires human review)
- Replace CLI (dashboard is view layer, CLI remains primary interface)

**Technical approach:**
- Extend existing `orchestrator status` command
- Add HTML output with better visualization
- Add cost tracking to run manifests
- Add optional email/Slack alerts for failures

**Effort estimate:** 2-3 days for dashboard enhancement

**Value:**
- Makes cycle costs and success rates visible
- Enables faster debugging of failed cycles
- Supports decision-making about model allocation

**Risk:**
- Dashboard without substance (if cycles aren't actually running)
- May encourage cycle volume over cycle quality
- Adds complexity without clear method benefit

**Recommendation:** **Enhance existing orchestrator status.** Add cost tracking and better HTML visualization, but don't build separate dashboard app.

---

### Option 4: Research Tooling for Scenario Generation and Curation

**Purpose:** Support scenario generation and curation workflow.

**What it would do:**
- `scenario generate <branch>` — Generate new scenario variants from components
- `scenario compare <variant1> <variant2>` — Side-by-side comparison
- `curate suggest <branch>` — Suggest keep/revise/discard based on evaluation
- `evidence check <scenario>` — Verify evidence citations match sources

**What it would NOT do:**
- Auto-publish scenarios (all output to `meta/generated/`)
- Auto-curate (suggestions only, human makes final decision)
- Replace human judgment (tools support, not automate)

**Technical approach:**
- Extend CLI with `scenario` and `curate` subcommands
- Use model delegation for generation and comparison
- Integrate with component index for reusable elements

**Effort estimate:** 4-6 days for initial implementation

**Value:**
- Reduces scenario generation overhead
- Makes comparison more systematic
- Supports explicit curation workflow

**Risk:**
- May encourage scenario proliferation without curation
- Generation quality depends on model capability
- May create false confidence in tool output

**Recommendation:** **Build curation tools first, generation second.** Curation support (evaluation matrix helper, comparison table generator) is higher value than generation (which already works via delegation).

---

## Minimum Viable Phase 7

Based on analysis above, here is the minimum viable Phase 7 scope:

### Phase 7A: Method Publication (Highest Priority)

**Goal:** Make method findings accessible without building full site.

**Deliverables:**
1. Publish `what-we-learned.md` as long-form essay (e.g., LessWrong, Substack, or academic preprint)
2. Create simple landing page (GitHub README links to method docs)
3. Gather feedback from external readers

**Effort:** 1-2 days  
**Timeline:** Immediate

**Success criteria:**
- At least 3 external readers provide substantive feedback
- Feedback informs whether fuller publication (site) is warranted

---

### Phase 7B: Component Index (Medium Priority)

**Goal:** Make cross-branch patterns more legible.

**Deliverables:**
1. `meta/components/` directory with YAML manifests for existing branches
2. CLI command: `component index` — build component index
3. CLI command: `component search <query>` — find relevant components

**Effort:** 2-3 days  
**Timeline:** After 7A feedback

**Success criteria:**
- Components extracted from all 4 branches
- Search returns relevant results for test queries
- Components help generate at least one new scenario variant

---

### Phase 7C: Curation Support (Medium Priority)

**Goal:** Reduce curation overhead without automating judgment.

**Deliverables:**
1. CLI command: `curate compare <variant1> <variant2>` — side-by-side comparison table
2. CLI command: `curate matrix <branch>` — generate evaluation matrix draft
3. CLI command: `curate suggest <branch>` — suggest keep/revise/discard based on scores

**Effort:** 2-3 days  
**Timeline:** After 7B

**Success criteria:**
- Comparison tables reduce manual formatting time by 50%
- Evaluation matrix draft is 80%+ usable (minor edits only)
- Curation suggestions align with human judgments 70%+ of time

---

### Phase 7D: Orchestrator Enhancement (Low Priority)

**Goal:** Better visibility into cycle costs and progress.

**Deliverables:**
1. Cost tracking in run manifests
2. Enhanced `orchestrator status` with HTML table
3. Optional alerts for failed cycles

**Effort:** 1-2 days  
**Timeline:** After 7C, if cycles are running frequently

**Success criteria:**
- Cost per cycle is tracked and visible
- Failed cycles are detected within 1 hour
- Dashboard is actually used (not just built)

---

### Phase 7E: Static Site (Lowest Priority / Conditional)

**Goal:** Full publication infrastructure.

**Trigger conditions (all required):**
- 7A feedback is positive (external readers find method valuable)
- At least 2 non-climate branches at L4 (currently 1 of 2 needed)
- Method documentation is stable (no major revisions in 30 days)

**Deliverables:**
1. Static site generator configured (MkDocs or Hugo)
2. Publication rules (what's public vs. internal)
3. Deployment pipeline (GitHub Pages or Netlify)

**Effort:** 2-3 days  
**Timeline:** Only if trigger conditions met

**Success criteria:**
- Site is live and accessible
- Public artifacts are clearly distinguished from drafts
- Site traffic and engagement justify maintenance effort

---

## What NOT to Build in Phase 7

### Avoid These (For Now)

1. **Full scenario auto-generation**
   - Why: Generation already works via delegation; auto-generation risks quality loss
   - Instead: Enhance curation tools, let humans decide what to generate

2. **Interactive collaboration features**
   - Why: Method is still being validated; collaboration adds complexity
   - Instead: Gather feedback on published method docs first

3. **Custom database or backend**
   - Why: Markdown + YAML + JSON is working; databases add ops overhead
   - Instead: Keep file-based state, add indexing only if needed

4. **Mobile apps or rich clients**
   - Why: CLI is working and accessible; mobile is solution in search of problem
   - Instead: Improve CLI documentation and usability

5. **Automated quality control**
   - Why: Quality judgment must stay human; automation creates false confidence
   - Instead: Make quality criteria more explicit in evaluation framework

---

## Decision Framework

Use this framework to decide whether to proceed with each Phase 7 element:

| Question | If Yes | If No |
|----------|--------|-------|
| Does this reduce coordination overhead? | Build | Skip |
| Does this automate method judgment? | Skip | Consider |
| Does this enable external feedback? | Prioritize | Defer |
| Does this add ops complexity? | Scrutinize | Proceed |
| Would researchers actually use this? | Build | Skip |

---

## Recommended Sequence

**Immediate (next 2 weeks):**
1. Publish `what-we-learned.md` as essay (7A)
2. Gather external feedback
3. Decide on component index based on feedback

**Short-term (1-2 months):**
1. Build component index if feedback positive (7B)
2. Build curation support tools (7C)
3. Run 5+ cycles using new tools to validate

**Medium-term (3-6 months):**
1. Enhance orchestrator if cycles are frequent (7D)
2. Consider static site if trigger conditions met (7E)
3. Decide on v2 scope (product vs. continued research)

---

## Open Questions

1. **Who is the audience for Phase 7 tooling?**
   - Researchers applying the method?
   - Institutions stress-testing assumptions?
   - General public seeking scenario exploration?

2. **What is the success metric for Phase 7?**
   - Number of external users?
   - Number of cycles run?
   - Quality of scenarios produced?
   - Method improvements from feedback?

3. **When is Phase 7 complete?**
   - After all 5 sub-phases (7A-7E)?
   - After method is published and validated?
   - After v2 product decision is made?

4. **What would change the Phase 7 plan?**
   - Negative external feedback (would pause publication)
   - Technical blockers (would simplify scope)
   - Unexpected use patterns (would reprioritize features)

---

## Links

- `docs/what-we-learned.md` — Method findings to publish
- `docs/method-guide.md` — Guide for external users
- `docs/artifact-taxonomy.md` — Artifact reference
- `docs/foundation-questions.md` — Philosophical anchor
- `ROADMAP.md` — Full project roadmap
- `docs/method-infrastructure.md` — CLI design specification

---

*This specification is a draft. Revise based on external feedback from 7A publication before proceeding to 7B.*
