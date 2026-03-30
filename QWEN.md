# Meta-Autoresearch Project Context

## Project Overview

**Meta-autoresearch** is a research repository developing a method of inquiry that resists premature closure. The core idea extends autoresearch from machine learning—fixing rigorous success measures while allowing open exploration—to broader forms of research, using **climate volatility** as the first proving ground.

### Key Principles
- **Rigor over certainty** - strict about method, not defending conclusions
- **Openness without vagueness** - entertain multiple directions without collapsing standards
- **Scenario over prophecy** - explore possibility space rather than perform false precision
- **Anti-target fixation** - don't let singular forecasts collapse the search space early
- **Human and AI as complements** - AI for generation/remixing; human judgment explicit
- **Public iteration** - make evolution of thinking visible

### Current Research Branches
| Branch | Domain | Structure Type | Maturity |
|--------|--------|----------------|----------|
| `whiplash` | climate volatility | sequence failure | Level 4 (method-shaping) |
| `breadbasket` | climate volatility | correlation/transmission failure | active |
| `hydrologic` | climate volatility | design/rule conflict under volatility | active |
| `wealth-concentration` | non-climate | comparative hybrid | Level 3 |

## Repository Structure

```
meta-autoresearch/
├── docs/                      # Canonical method documentation
│   ├── foundation.md          # Long-form conceptual framing
│   ├── method.md              # Operational research loop
│   ├── research-loop.md       # Staged 9-stage workflow
│   ├── evaluation-framework.md # Scenario scoring rubric
│   ├── branch-maturity.md     # Branch development rubric
│   ├── method-infrastructure.md # CLI design specification
│   ├── research-agenda.md     # Active questions
│   ├── glossary.md            # Working definitions
│   └── research-tooling.md    # Tool requirements
├── meta/                      # Structured state for CLI layer
│   ├── branches/              # Branch manifests (JSON)
│   ├── runs/                  # Run manifests (JSON)
│   └── generated/             # Generated dossiers/packets
├── meta_autoresearch_cli/     # Python CLI package
│   ├── __init__.py
│   ├── __main__.py
│   └── cli.py                 # Main CLI implementation
├── research/                  # Working corpus
│   ├── notes/                 # Source synthesis, questions
│   ├── scenarios/             # Scenario drafts/variants
│   ├── experiments/           # Process tests
│   ├── discards/              # Pruned/failed directions
│   ├── loops/                 # Full cycle audit records
│   └── syntheses/             # Cross-artifact comparisons
└── pyproject.toml             # Python packaging
```

## Building and Running

### Prerequisites
- Python 3.10+

### Installation
```bash
# Install as editable package
pip install -e .

# Or run directly without installation
python -m meta_autoresearch_cli <command>
```

### CLI Commands

**Branch commands:**
```bash
python -m meta_autoresearch_cli branch list
python -m meta_autoresearch_cli branch status <slug>
python -m meta_autoresearch_cli branch check <slug>
python -m meta_autoresearch_cli branch dossier <slug>
python -m meta_autoresearch_cli branch snapshot <slug>
python -m meta_autoresearch_cli branch stale [slug]       # Check stale generated (all branches if no slug)
python -m meta_autoresearch_cli branch index <slug>       # Generate artifact index table
python -m meta_autoresearch_cli branch compare-prep <slug> # Generate comparison prep material
```

**Run commands:**
```bash
python -m meta_autoresearch_cli run new <branch> --type <pass-type> [--question "..."]
python -m meta_autoresearch_cli run list [--branch <slug>] [--status <state>]
python -m meta_autoresearch_cli run show <run-id>
python -m meta_autoresearch_cli run check <run-id>
python -m meta_autoresearch_cli run update <run-id> --add-output <kind> <path>
python -m meta_autoresearch_cli run update <run-id> --note "..."
python -m meta_autoresearch_cli run complete <run-id> [--force]
python -m meta_autoresearch_cli run packet <run-id>
```

**Delegate commands** (Iteration 3 - requires OPENROUTER_API_KEY):
```bash
python -m meta_autoresearch_cli delegate summarize-note <path>    # Summarize a research note
python -m meta_autoresearch_cli delegate extract-claims <path>    # Extract claims from artifact
python -m meta_autoresearch_cli delegate branch-packet <slug>     # Generate complete branch packet
python -m meta_autoresearch_cli delegate run-prep <branch> --type <pass-type>  # Prepare for run type
python -m meta_autoresearch_cli delegate batch <task> <pattern>   # Batch process files (e.g., batch summarize-note 'research/notes/*.md')
```

**Orchestrator commands** (Phase 7 - Scaled-cycle automation):
```bash
python -m meta_autoresearch_cli orchestrator run <plan.json>      # Execute a run plan
python -m meta_autoresearch_cli orchestrator status               # Show cycle progress dashboard
python -m meta_autoresearch_cli orchestrator benchmark            # Benchmark model performance
```

**Model slots** (configured in `.env`):
- `small`: qwen/qwen3.5-flash-02-23 ($0.065/$0.26 per 1M, 1M context)
- `mid`: mistralai/mistral-small-2603 ($0.15/$0.60 per 1M, 262K context)
- `strong`: qwen/qwen3.5-plus-02-15 ($0.26/$1.56 per 1M, 1M context)

**Fallback models** (tried if primary times out):
- Configured via `META_MODEL_FALLBACK_SMALL`, `META_MODEL_FALLBACK_MID`, `META_MODEL_FALLBACK_STRONG`
- Default timeout: 90 seconds per model attempt

**Pass types:** `grounding`, `variant`, `comparison`, `maturity`, `discard`, `capability-fit`

### Model Configuration (Required for Delegation/Orchestrator)

Create `.env` file in project root:
```bash
# OpenRouter API key (required for model delegation)
OPENROUTER_API_KEY=your-key-here

# Primary models for each slot
META_MODEL_DEFAULT_SMALL=qwen/qwen3.5-flash-02-23
META_MODEL_DEFAULT_MID=mistralai/mistral-small-2603
META_MODEL_DEFAULT_STRONG=qwen/qwen3.5-plus-02-15

# Fallback models (comma-separated, tried if primary fails/times out)
META_MODEL_FALLBACK_SMALL=meta-llama/llama-3-8b-instruct,google/gemma-2-9b-it
META_MODEL_FALLBACK_MID=mistralai/mistral-7b-instruct,qwen/qwen3.5-flash-02-23
META_MODEL_FALLBACK_STRONG=qwen/qwen3.5-flash-02-23,meta-llama/llama-3-70b-instruct

# API timeout per model attempt (seconds)
META_MODEL_TIMEOUT=90

# Optional: OpenRouter configuration
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

## Development Conventions

### File Naming
- Date-first, lowercase, kebab-case: `YYYY-MM-DD-topic.md`
- Same-day variants: `-v2`, `-compare` suffixes

### Source Discipline
Distinguish source types:
- `assessed report`
- `peer-reviewed paper`
- `journalistic reporting`
- `researcher-provided canonical document`
- `working interpretation`

### Curation Decisions
Every scenario/experiment pass should end with explicit judgment:
- **Keep** - worth developing further
- **Revise** - promising but needs work
- **Merge** - better as part of another family
- **Discard** - not useful enough (record in `research/discards/`)

### Evaluation Dimensions (1-5 scale)
1. Evidence strength
2. Internal coherence
3. Relevance to research question
4. Preparedness value
5. Novelty and search-space value
6. Actionability for next step
7. Status-quo challenge
8. Imaginative power

### Research Loop (9 Stages)
1. Frame the inquiry
2. Assemble starting evidence base
3. Generate candidate branches
4. Ground the most promising branch
5. Create branch variants
6. Compare variants
7. Evaluate and curate
8. Synthesize across branches
9. Assess cycle maturity

### Manifest Structures

**Branch manifest** (`meta/branches/<slug>.json`):
- `slug`, `title`, `domain`, `structure_type`, `maturity_level`
- `status`, `parent_artifact`, `active_variants`
- `key_notes`, `key_syntheses`, `loop_runs`, `discard_records`
- `strongest_variant`, `most_generative_variant`, `weakest_variant`
- `open_questions`, `next_recommended_pass`, `last_updated`

**Run manifest** (`meta/runs/<run-id>.json`):
- `run_id`, `date`, `branch_slug`, `run_type`
- `question`, `stages_targeted`, `expected_outputs`
- `created_outputs`, `completion_status`, `notes`, `next_step`

### Branch Maturity Levels
- **Level 1-2**: Early exploration
- **Level 3**: Comparative (multiple variants, loop run recorded)
- **Level 4**: Method-shaping (discard records, key syntheses, clear next steps)

## Key Documentation Order

For new contributors, read in order:
1. `README.md` - Project overview
2. `docs/foundation.md` - Conceptual framing
3. `docs/method.md` - Operational method
4. `docs/research-loop.md` - 9-stage workflow
5. `docs/evaluation-framework.md` - Scoring rubric
6. `docs/branch-maturity.md` - Development levels
7. `docs/method-infrastructure.md` - CLI design
8. `CONTRIBUTING.md` - Contribution norms

## Current Development Focus

**Iteration 2: Context Compression** (COMPLETED)

Implemented:
- `branch snapshot` - compact branch packets
- `run packet` - generated packets for specific passes
- `branch index` - artifact index with modification times and existence checks
- `branch stale` - stale-state detection, warns when generated packets are older than source manifests
- `branch compare-prep` - comparison prep with variant tables, dimensions, and guiding questions

**Iteration 3: Bounded Model Delegation** (COMPLETED)

Implemented:
- `.env` configuration file with OpenRouter support
- Provider-agnostic model config (small/mid/strong slots)
- Fallback models with configurable timeout
- `delegate summarize-note <path>` - summarize research notes to 200-400 words
- `delegate extract-claims <path>` - extract claims with evidence/speculative tags
- Safety: all output to `meta/generated/`, marked as draft, never auto-sets maturity/curation

**Phase 6: Workflow Automation** (COMPLETED)

Implemented:
- `delegate branch-packet` - generate snapshot + index + compare-prep in one call
- `delegate run-prep` - prepare all materials for a run type
- `delegate batch` - process multiple files with glob patterns

**Phase 7A: Scaled-Cycle Orchestrator** (COMPLETED)

Implemented:
- `orchestrator run <plan.json>` - execute autonomous research cycles
- `orchestrator status` - show HTML dashboard with progress/costs
- `orchestrator benchmark` - test model performance to find fastest option
- Per-task timing tracking in cycle states
- Automatic fallback to alternate models on timeout/failure

Validation results (10-cycle test on whiplash):
- 10/10 cycles completed successfully
- ~2.7 minutes per cycle average
- ~$0.0032 cost per cycle
- 0 failures, 0 human interventions

See `docs/model-performance.md` for model configuration and benchmarking guide.

## Working Rules

- Infrastructure should automate method overhead, not method judgment
- Generated output goes to `meta/generated/`, not directly into `research/`
- Distinguish `evidence strength` from `scenario value`
- If every artifact is always kept, curation is too soft
- Treat AI output as material for judgment, not judgment itself
