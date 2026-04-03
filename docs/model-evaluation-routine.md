# Model Evaluation Routine

**Status:** draft  
**Date:** 2026-04-02  
**Type:** Method infrastructure note

---

## Purpose

This note establishes model evaluation as a regular routine for the meta-autoresearch method.

The model landscape changes rapidly: new models emerge, existing models are revised, and pricing shifts frequently. The method's cost efficiency and output quality depend on staying current with these changes.

---

## Why This Matters

### Cost Efficiency

The method's validation cycles depend on delegated model tasks. Model selection directly affects:
- **Cost per cycle** — Currently ~$0.0032/cycle with qwen3.5-flash
- **Duration per cycle** — Currently ~90-140s/cycle
- **Output quality** — Affects downstream synthesis and curation accuracy

A 3.8x speedup (gemini-2.5-flash-lite vs. qwen3.5-flash) was found through benchmarking, reducing cycle time from ~90s to ~25s.

### Capability Fit

Different models excel at different tasks:
- **Summarization** — Requires coherence and source attribution
- **Claim extraction** — Requires distinguishing evidence from speculation
- **Comparison drafting** — Requires structured reasoning across variants
- **Structure typing** — Requires high-stakes judgment

The method should use the weakest model that can do each task well enough.

### Pricing Volatility

Model pricing changes frequently:
- New models launch at promotional prices
- Existing models adjust pricing based on demand
- Context window changes affect effective cost

The method should track these changes and adjust accordingly.

---

## Evaluation Routine

### Frequency

**Monthly:** Run `orchestrator benchmark` to test current models against fallbacks.

**Quarterly:** Full evaluation across all three slots (small, mid, strong) with new model candidates.

**Ad-hoc:** When new models are announced or pricing changes are reported.

### Benchmark Tasks

Use these tasks to evaluate models:

| Task | Slot | Test Content | Quality Criteria |
|------|------|--------------|------------------|
| Summarize note | Small | 3K token grounding note | Key claims identified, sources attributed, uncertainties captured |
| Extract claims | Small | 4K token scenario | Evidence vs. speculative distinguished, sources noted |
| Comparison prep | Mid | Branch packet + variants | Structured comparison, evaluation dimensions applied |
| Structure typing | Strong | Cross-branch synthesis | Structure types correctly identified, method lessons extracted |

### Evaluation Metrics

| Metric | Measurement | Target |
|--------|-------------|--------|
| **Duration** | Seconds per task | Minimize (within quality constraints) |
| **Cost** | $ per task (input + output tokens) | Minimize (within quality constraints) |
| **Quality** | Human review score (1-5) | ≥4 for small/mid, ≥4.5 for strong |
| **Reliability** | Success rate (no empty responses) | ≥95% |
| **Context window** | Max tokens | Sufficient for task (3K+ for small, 10K+ for mid, 50K+ for strong) |

### Decision Criteria

**Switch model if:**
- New model is ≥2x faster at same quality and cost
- New model is ≥50% cheaper at same quality and speed
- New model is ≥0.5 quality points higher at same cost and speed
- Current model becomes unavailable or pricing increases >50%

**Keep current model if:**
- Quality difference is <0.3 points
- Cost difference is <20%
- Speed difference is <2x
- Current model is reliable and well-understood

---

## Current Model Configuration (as of 2026-04-02)

### Small Slot
| Model | Duration | Cost per 1M | Status |
|-------|----------|-------------|--------|
| **xiaomi/mimo-v2-flash** | **2.54s** | varies | ✅ Primary (benchmark winner 2026-04-02) |
| qwen/qwen3.5-flash-02-23 | 3.21s | $0.065/$0.26 | ⚠️ Fallback 1 |
| google/gemini-2.5-flash-lite | 7.03s | $0.075/$0.30 | ⚠️ Fallback 2 |

### Mid Slot
| Model | Duration | Cost per 1M | Status |
|-------|----------|-------------|--------|
| mistralai/mistral-small-2603 | TBD | $0.15/$0.60 | ✅ Primary |
| mistralai/mistral-7b-instruct | TBD | varies | ⚠️ Fallback 1 |
| qwen/qwen3.5-flash-02-23 | TBD | $0.065/$0.26 | ⚠️ Fallback 2 |

### Strong Slot
| Model | Duration | Cost per 1M | Status |
|-------|----------|-------------|--------|
| qwen/qwen3.5-plus-02-15 | TBD | $0.26/$1.56 | ✅ Primary |
| qwen/qwen3.5-flash-02-23 | TBD | $0.065/$0.26 | ⚠️ Fallback 1 |
| meta-llama/llama-3-70b-instruct | TBD | varies | ⚠️ Fallback 2 |

---

## Benchmark Command

```bash
# Run benchmark for small slot (default)
python -m meta_autoresearch_cli orchestrator benchmark

# Results show duration, output length, and ranking
# Run monthly to catch model changes and pricing shifts
```

**Output:** Table of models ranked by speed, with duration and output length.

**Note:** Model performance varies over time. The benchmark from 2026-04-02 showed xiaomi/mimo-v2-flash as fastest (2.54s), but earlier the same day gemini-2.5-flash-lite was fastest (1.75s). Re-run benchmark before making model changes.

---

## Tracking Changes

Maintain a log of model changes:

| Date | Change | Reason | Impact |
|------|--------|--------|--------|
| 2026-04-02 (2) | Switched small slot to xiaomi/mimo-v2-flash | 2.54s vs 7.03s (gemini), 2.8x faster | Cycle time reduced further |
| 2026-04-02 (1) | Switched small slot to gemini-2.5-flash-lite | 1.75s vs 6.73s (qwen), 3.8x faster | Cycle time reduced from ~90s to ~25s |
| 2026-04-02 | Fixed delegate extract-claims bug | Unpacking error in get_model_for_slot | Claims extraction now works |

---

## Future Considerations

### Model Categories to Watch

1. **New model launches** — OpenRouter regularly adds new models at promotional prices
2. **Pricing changes** — Existing models adjust pricing based on demand and competition
3. **Context window increases** — Larger context windows enable bigger tasks per call
4. **Quality improvements** — New model versions may justify switching even at same cost
5. **Regional availability** — Some models may be available in some regions but not others

### Evaluation Automation

Future enhancements could include:
- Automated benchmark scheduling (monthly reminder)
- Quality scoring automation (LLM-as-judge for output quality)
- Cost tracking integration (actual costs from model calls vs. estimates)
- Fallback testing (automated testing of fallback models when primary fails)

---

## Links

- `.env` — Current model configuration
- `docs/method-infrastructure.md` — CLI design specification
- `docs/model-performance.md` — Model configuration and benchmarking guide
- `meta/orchestrator/` — Cycle state files with actual model usage and costs

---

*This note should be reviewed quarterly and updated based on benchmark results and model landscape changes.*
