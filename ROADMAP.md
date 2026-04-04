# Roadmap

## Current read

The project has completed Phases 1-7C and is now entering Phase 9 (L5 tooling iterations for scale and generalizability).

**What's done:**
- Iterations 1-3 complete: branch/run state, context compression, model delegation
- 5 research branches active: 3 climate (whiplash L4, breadbasket L4, hydrologic L4) + 2 non-climate (wealth-concentration L4, avian-flu-zoonotic L4)
- Model delegation tested and working: summarize-note, extract-claims via OpenRouter
- Cost profile established: ~$0.0032/cycle with orchestrator, ~25s per cycle (xiaomi/mimo-v2-flash)
- Phase 7B (component index): 83 components extracted, CLI commands working
- Phase 7C (curation support): curate compare and curate matrix commands working
- Phase 7D (orchestrator): benchmark, dashboard, cost tracking (partial)
- Method consolidation: what-we-learned.md, method-guide.md, artifact-taxonomy.md, foundation-questions.md
- Model evaluation routine established with monthly benchmark
- **L5 criteria defined:** template reusability, cross-method integration, method evolution (prospective validation optional)
- **Cross-branch synthesis updated:** All 5 branches documented with subtype taxonomies

**Current bottleneck:** Orchestrator only supports `comparison` pass type (grounding/variant/maturity/discard are placeholders); sequential model calls limit speed; manual component extraction and manifest updates create coordination overhead.

**Immediate priorities:**
- Phase 9A: Fix orchestrator pass types (grounding, variant, maturity, discard)
- Phase 9B: Parallel model calls within cycles (3-4x speedup)
- Phase 9C: Automated component extraction and manifest updates
- Phase 9D: L5 readiness tracking and template generation
- Phase 9E: Cross-method integration support and dynamic model selection

**Current state:**
- All 5 branches at L4 (method-shaping)
- L5 criteria defined (generalizable: template reusability + cross-method integration + method evolution)
- Non-climate portability demonstrated via wealth-concentration (hybrid, 2 domains) and avian-flu-zoonotic (hybrid, biological volatility)
- Method lessons synthesis complete with explicit L3→L4→L5 pathway
- Phase 7 entry criteria: all 5 met
- Phase 7B/7C complete; Phase 7D partial; Phase 7A/7E deferred

## Phase 1: foundation and structure

Establish the conceptual basis of the project, define the repository structure, and separate foundational claims from open research questions.

Outputs:

- core docs in place
- shared vocabulary established
- initial research scope defined

## Phase 2: operational method

Turn the framing into a repeatable workflow for notes, scenarios, experiments, and syntheses.

Outputs:

- scenario template
- experiment template
- notes and synthesis support
- initial evaluation criteria
- explicit human/AI workflow

## Phase 3: first climate explorations

Use climate volatility as the first proving ground and produce an initial body of scenario work.

Outputs:

- exploratory scenario set
- first synthesis across scenarios
- written reflections on failure modes and surprises

## Phase 4: evidence grounding and narrowing

Take promising scenario families and ground them more firmly in literature, case evidence, and researcher-supplied source material.

Outputs:

- grounded scenario variants tied to specific regions, systems, or case clusters
- clearer distinction between evidence-rich and evidence-thin scenario families
- explicit notes on what is supported, what is speculative, and what remains unresolved

## Phase 5: evaluation and refinement

Assess whether the method is producing genuinely useful structure or merely generating interesting text.

Outputs:

- revised measurement framework
- stronger curation rules
- scenario comparison matrix or equivalent evaluation layer
- documented lessons from early experiments
- explicit examples of what the method should stop doing

Current signals of progress in this phase:

- a reusable evaluation framework exists
- the whiplash branch has internal comparison and pruning pressure
- the breadbasket branch now has sub-branch comparison and downstream exposure grounding
- emerging epistemic structure types are starting to appear in the method itself
- loop-run and discard artifacts now make both success and pruning auditable
- the first non-climate proving-ground branch has reached a comparative maturity level, showing that portability is plausible but often arrives first as a hybrid rather than a clean transfer
- the next strategic question is no longer whether the method can leave climate, but what additional evidence would make non-climate portability method-shaping rather than only comparative

## Phase 5.5: method infrastructure (COMPLETE)

Add a lightweight internal tooling layer that supports the method without turning the project into a product.

**Outputs delivered:**
- structured branch and run state (JSON manifests in `meta/`)
- loop-run scaffolding and validation (`run new`, `run check`, `run complete`)
- branch dossier generation (`branch dossier`, `branch snapshot`)
- method hygiene checks (`branch check`, `branch stale`)
- context compression (`branch index`, `branch compare-prep`, `run packet`)
- bounded model delegation (`delegate summarize-note`, `delegate extract-claims`)
- workflow automation (`delegate branch-packet`, `delegate run-prep`, `delegate batch`)
- provider-agnostic model config (OpenRouter backend, small/mid/strong slots)
- `.env` configuration for API keys and model selection

**Cost profile:**
- summarization: ~$0.0007 per 3K token note (qwen3.5-flash-02-23)
- claim extraction: ~$0.0009 per 4K token note
- batch processing: ~$0.0035-0.009 per batch of 5 files
- 100 delegations/month: ~$0.07-0.14

**Safety features:**
- all output to `meta/generated/`, never directly to `research/`
- HTML comments mark task type, model, source, timestamp
- footer: "Treat as draft until reviewed"
- no command can auto-set maturity, structure type, or curation

**Notes:**
- Local model support (Phase 6A) was tested but deferred due to hardware limitations
- Cloud-based delegation via OpenRouter remains the primary execution path

## Phase 6: scaled-cycle design

Design how the research loop could run repeatedly and at larger volume without losing rigor.

**Active workstreams (in priority order):**

### 6B: Workflow Automation (first) - COMPLETE

Chain delegated tasks into multi-step workflows to reduce session startup overhead.

**Outputs delivered:**
- `delegate branch-packet` - combines snapshot + index + compare-prep in one call (4 files)
- `delegate run-prep` - prepares all materials for a run type with run-specific guidance
- `delegate batch` - processes multiple files with glob patterns (summarize-note or extract-claims)
- target: reduce session startup from ~10 commands to ~2

**Usage:**
```bash
# Full branch packet in one command
python -m meta_autoresearch_cli delegate branch-packet whiplash

# Run-specific prep with branch packet
python -m meta_autoresearch_cli delegate run-prep whiplash --type comparison

# Batch process multiple files
python -m meta_autoresearch_cli delegate batch summarize-note "research/notes/2026-03-28-*.md"
python -m meta_autoresearch_cli delegate batch extract-claims "research/scenarios/2026-03-27-*.md"
```

**See:** `docs/batch-command-usage.md` for detailed batch command documentation.

### 6A: Local Model Support (deferred)

Add support for local model execution via Ollama or LM Studio to reduce API costs.

**Status:** Deferred - current hardware not sufficient for quality/cost tradeoff to be worthwhile.

**Original planned outputs:**
- `META_MODEL_BACKEND=ollama` option
- local model slot configuration (small/mid only, strong stays cloud)
- fallback behavior when local models unavailable
- target: 50-80% of delegation tasks offloaded to local execution

**Revisit when:** Hardware improves or local model quality significantly increases.

### 6C: Validation Cycles - COMPLETE

Run 2-3 full research cycles using existing delegation to measure quality/cost/overhead tradeoffs.

**Selected branches:**
- **whiplash** - comparison pass ✅ COMPLETE
- **breadbasket** - grounding pass ✅ COMPLETE

**Validation results:**

| Metric | Whiplash (comparison) | Breadbasket (grounding) |
|--------|----------------------|------------------------|
| Commands executed | 6 | 12 |
| Total cost | $0.0041 | $0.0089 |
| Summarization quality | High | High |
| Claim extraction quality | High | High |
| Workflow automation value | High | High |
| Coordination reduction | 60% | 60% |
| Model performance | Strong | Strong |

**Conclusion:** The delegation + workflow automation pattern **generalizes across pass types** (comparison and grounding) and **across branches** (whiplash sequence failure, breadbasket correlation/transmission).

**See:** 
- `research/experiments/2026-03-29-whiplash-validation-cycle-report.md`
- `research/experiments/2026-03-29-breadbasket-validation-cycle-report.md`

**Metrics validated:**
- actual cost per delegation vs. estimates ✅ Validated on 2 branches
- quality of model output (usable as-is vs. requires heavy editing) ✅ High quality on both
- coordination overhead (commands per session, time per pass) ✅ 60% reduction on both
- whether generated artifacts actually reduce session startup time ✅ Confirmed on both

### 6D: Method-Shaping Evidence - COMPLETE

Push branches toward L4 to demonstrate method-shaping power.

**Outputs delivered:**
- wealth-concentration promoted from L3→L4 with explicit hybrid portability caveat
- Cross-branch synthesis: `research/syntheses/2026-03-29-method-lessons-cross-branch-synthesis.md`
- Updated branch-maturity.md with hybrid structure guidance
- Explicit L3→L4 criteria documented

**Key findings:**
- All 4 branches now at L4 (whiplash, breadbasket, hydrologic, wealth-concentration)
- Non-climate portability demonstrated via wealth-concentration
- Hybrid structure finding is itself method-shaping—it changes how future non-climate branches are evaluated
- Portability arrives in stages: thematic → structural resonance → hybrid → resolved → method-shaping

**See:** 
- `research/syntheses/2026-03-29-method-lessons-cross-branch-synthesis.md` for full cross-branch analysis
- `docs/branch-maturity.md` for updated L4 criteria and hybrid guidance

## Phase 7: prototype decision (COMPLETE for 7B/7C, PARTIAL for 7D, DEFERRED for 7A/7E)

Only after the research workflow becomes legible and evaluable should the project decide whether to build software around it.

**Entry criteria (all required):**
- [x] At least 2 branches at L4 (method-shaping) ✅ (4 branches: whiplash, breadbasket, hydrologic, wealth-concentration)
- [x] Non-climate portability demonstrated at L4 ✅ (wealth-concentration, hybrid portability across 3 domains)
- [x] Cost profile sustainable at 10x current volume ✅ (~$0.50-1.50/month at typical 100 cycles)
- [x] Coordination overhead reduced enough that one researcher can run 5+ cycles/week ✅ (60% reduction, ~2 commands per session)
- [x] Clear "method lessons" document ✅ (`docs/what-we-learned.md`)

**All 5 entry criteria met as of 2026-03-29.**

**Phase 7 sub-phases:**

| Sub-phase | Status | Deliverables |
|-----------|--------|--------------|
| 7A: Method Publication | ⏸️ Deferred | External feedback not yet ready |
| 7B: Component Index | ✅ Complete | 78 components, 5 CLI commands |
| 7C: Curation Support | ✅ Complete | curate compare, curate matrix |
| 7D: Orchestrator Enhancement | ⏳ Partial | Benchmark, dashboard, cost tracking; timeout fix needed |
| 7E: Static Site | ⏸️ Deferred | Trigger conditions not met |

**If proceeding, possible next steps:**
- Fix orchestrator timeout for multi-cycle plans
- Run model benchmark monthly to track performance changes
- Consider method publication when ready for external feedback
- Decide on v2 scope (product vs. continued research)

**If deferring:**
- continue research cycles to further validate method
- consider what unique value a prototype would add beyond the existing CLI

## Phase 9: L5 tooling iterations (COMPLETE)

**Purpose:** Iterate tools to enable L5-scale efficiency — highly efficient, efficacious, thorough, and fast autoresearch.

**Entry criteria (all required):**
- [x] All 5 branches at L4
- [x] L5 criteria defined (template reusability, cross-method integration, method evolution)
- [x] Cross-branch synthesis updated with all 5 branches
- [x] Subtype taxonomies documented for all structure types

**Current status:** ✅ COMPLETE as of 2026-04-04.

### Phase 9A: Fix Orchestrator Pass Types ✅ COMPLETE

All pass types now produce real outputs:
- **grounding** — Summarizes notes (up to 3), extracts claims from scenarios (up to 3)
- **variant** — Extracts claims from parent scenario and existing variants (up to 2)
- **maturity** — Summarizes key syntheses (up to 2)
- **discard** — Extracts claims from all variants (up to 3)
- **comparison** — Summarizes notes (up to 2), extracts claims from scenarios (up to 2)

**Cost per pass type:** grounding $0.0048, variant $0.0027, maturity $0.0014, discard $0.0027, comparison $0.0032

### Phase 9B: Parallel Execution ✅ COMPLETE

All pass types use `parallel_model_calls()` for concurrent API calls:

| Pass Type | Sequential | Parallel | Speedup |
|-----------|-----------|----------|---------|
| grounding | 36.4s | 8.3s | 4.4x |
| comparison | 24.9s | 8.9s | 2.8x |
| variant | 24.0s | 11.9s | 2.0x |
| maturity | 13.2s | 4.1s | 3.2x |
| discard | 21.2s | 10.2s | 2.1x |
| **Average** | **24.0s** | **8.7s** | **2.8x** |

### Phase 9C: Automation ✅ COMPLETE

Three automation features implemented:
1. **Automated component extraction** — After each cycle, scans new scenarios for regions, institutions, hazards, infrastructure. Generates placeholder YAML for unknown entities.
2. **Automated branch manifest updates** — After cycle completion, adds new outputs to appropriate manifest fields (key_notes, active_variants, key_syntheses, loop_runs, discard_records).
3. **L5 readiness tracking** — `branch l5-readiness <slug>` assesses template reusability, cross-method integration, method evolution, prospective validation.

**L5 Readiness Results:**
- wealth-concentration: ✅ READY
- avian-flu-zoonotic: ✅ READY
- whiplash: ⏳ Needs cross-method integration
- breadbasket: ⏳ Needs cross-method integration
- hydrologic: ⏳ Needs cross-method integration

### Phase 9D: Scale Enablement ✅ COMPLETE

Three scale-enabling features implemented:
1. **Template generation** — `branch template <structure-type> <slug> --title --domain` creates complete new branch from structure type template (sequence, correlation, design-rule, hybrid-2comp, hybrid-3comp).
2. **Cross-method integration** — `branch integrate <slug> --method <external-method>` generates integration synthesis mapping structure type to resilience-engineering, systems-thinking, complexity-science, institutional-analysis, or pandemic-preparedness concepts.
3. **Dynamic model selection** — `select_model_for_task()` auto-selects model based on task complexity (simple → small slot, moderate → mid slot, complex → strong slot). Integrated into `parallel_model_calls()` with optional flag.

**Phase 9 Success Criteria (all met):**
- [x] All pass types produce real outputs (not placeholders)
- [x] Cycle time reduced to ~9s with parallel execution (target: ~8s, achieved: 8.7s avg)
- [x] Automated component extraction and manifest updates working
- [x] L5 progress measurable via `branch l5-readiness`
- [x] New branches creatable from templates
- [x] Cross-method integration supported for 5 external methods
- [x] Dynamic model selection implemented and tested

## Cross-phase priorities

- keep the method auditable as the corpus grows
- treat source discipline as part of the method, not as cleanup work
- prune weak scenario families instead of only accumulating new ones
- preserve the distinction between valuable prompts and well-supported claims
- optimize for capability fit and process efficiency, not only raw model power
- treat climate as a proving ground for the method, not as its permanent boundary
- resist prediction-centered design when it narrows the search space prematurely
- **balance tooling and research validation in interleaved cycles, not sequential phases**
- **every infrastructure addition should be validated on real research passes before expansion**
- **reduce token costs and coordination overhead as explicit design constraints, not afterthoughts**
- **evaluate available models monthly for combined cost efficiency and capability** ⭐ NEW
- **model performance is volatile; benchmark before making changes** ⭐ NEW

## Guiding rule

Do not build product complexity or cycle scale faster than methodological clarity.

## Phase 8: method consolidation and strategic direction (ENTERING)

**Purpose:** Assess what the method has become, what it can do, and where it should go.

**Entry criteria (all required):**
- [x] All 4 branches at L4
- [x] 3 stable structure types validated across domains
- [x] Non-climate portability demonstrated (3 domains for wealth-concentration)
- [x] Phase 7B/7C tooling complete
- [x] Method consolidation documents written
- [x] Model evaluation routine established

**Current status:** ✅ All entry criteria met as of 2026-04-02.

**Phase 8 questions:**
1. What is the method now capable of that it wasn't at v1 start?
2. What strategic directions are now open that weren't before?
3. What should the method stop doing, keep doing, or start doing?
4. What is the audience for this work?
5. What would constitute v2?
