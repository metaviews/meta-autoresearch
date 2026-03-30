# Model Performance and Fallbacks

**Added:** 2026-03-29  
**Feature:** Fallback models + per-task timing + model benchmarking

---

## Problem

API latency varies significantly based on:
- Model provider load
- Time of day
- Network conditions
- Rate limiting

A model that takes 5 seconds at 3am might take 60+ seconds at peak hours.

## Solution

### 1. Configurable Fallback Models (`.env`)

Configure fallback models in your `.env` file:

```bash
# Primary models
META_MODEL_DEFAULT_SMALL=qwen/qwen3.5-flash-02-23
META_MODEL_DEFAULT_MID=mistralai/mistral-small-2603
META_MODEL_DEFAULT_STRONG=qwen/qwen3.5-plus-02-15

# Fallback models (comma-separated, tried in order if primary fails)
META_MODEL_FALLBACK_SMALL=meta-llama/llama-3-8b-instruct,google/gemma-2-9b-it
META_MODEL_FALLBACK_MID=mistralai/mistral-7b-instruct,qwen/qwen3.5-flash-02-23
META_MODEL_FALLBACK_STRONG=qwen/qwen3.5-flash-02-23,meta-llama/llama-3-70b-instruct

# Timeout per model attempt (seconds)
META_MODEL_TIMEOUT=90
```

**Behavior:**
- Tries primary model first
- If timeout/error/rate-limit, tries next fallback
- Returns actual model used (may be fallback)
- Records duration for performance tracking

### 2. Per-Task Timing

Each cycle tracks timing per API call in `meta/orchestrator/*.json`:

```json
{
  "task_timings": [
    {
      "task": "summarize-note",
      "source": "research/notes/2026-03-27-feather-river.md",
      "model": "qwen/qwen3.5-flash-02-23",
      "duration_seconds": 12.4
    },
    {
      "task": "extract-claims",
      "source": "research/scenarios/2026-03-27-whiplash.md",
      "model": "meta-llama/llama-3-8b-instruct",
      "duration_seconds": 8.2
    }
  ]
}
```

**Why this matters:**
- Identifies which models are actually fast for our workloads
- Detects when a model is having a slow day
- Enables data-driven model selection

### 3. Model Benchmark Command

Test your configured models to find the fastest:

```bash
python -m meta_autoresearch_cli orchestrator benchmark
```

Tests models from your `.env` configuration (primary + fallbacks for small slot).

**Example output:**
```
=== Model Benchmark ===
Task: Summarize research note (~100 tokens)
Timeout: 90s per model

Testing qwen/qwen3.5-flash-02-23...
  ✓ qwen/qwen3.5-flash-02-23: 8.42s, 342 chars
Testing meta-llama/llama-3-8b-instruct...
  ✓ meta-llama/llama-3-8b-instruct: 5.21s, 298 chars
Testing google/gemma-2-9b-it...
  ✓ google/gemma-2-9b-it: 3.87s, 315 chars

=== Results ===

Fastest: google/gemma-2-9b-it (3.87s)

| Model | Duration | Output Length |
|-------|----------|---------------|
| google/gemma-2-9b-it | 3.87s | 315 chars |
| meta-llama/llama-3-8b-instruct | 5.21s | 298 chars |
| qwen/qwen3.5-flash-02-23 | 8.42s | 342 chars |
```

**Use cases:**
- Run before starting a large batch to pick best model
- Run periodically to detect performance changes
- Compare cost vs. speed tradeoffs

---

## Recommended Model Configurations

### For Speed (lowest latency)
```bash
META_MODEL_DEFAULT_SMALL=google/gemma-2-9b-it
META_MODEL_DEFAULT_MID=mistralai/mistral-small-2603
META_MODEL_DEFAULT_STRONG=qwen/qwen3.5-plus-02-15
```

### For Quality (best output)
```bash
META_MODEL_DEFAULT_SMALL=qwen/qwen3.5-flash-02-23
META_MODEL_DEFAULT_MID=mistralai/mistral-small-2603
META_MODEL_DEFAULT_STRONG=anthropic/claude-sonnet-4.6
```

### For Cost (lowest $/task)
```bash
META_MODEL_DEFAULT_SMALL=meta-llama/llama-3-8b-instruct
META_MODEL_DEFAULT_MID=qwen/qwen3.5-flash-02-23
META_MODEL_DEFAULT_STRONG=qwen/qwen3.5-plus-02-15
```

---

## Fallback Strategy

Current fallback chain for `small` slot:
1. `qwen/qwen3.5-flash-02-23` (primary)
2. `meta-llama/llama-3-8b-instruct` (fallback 1)
3. `google/gemma-2-9b-it` (fallback 2)

**Timeout:** 90 seconds per model before trying next

**When to adjust:**
- If fallback is triggered frequently, increase timeout or change primary
- If primary is consistently slow, run benchmark and update default
- If a model consistently fails, remove from rotation

---

## Metrics to Track

In cycle state files (`meta/orchestrator/*.json`):

| Field | What it tells you |
|-------|-------------------|
| `task_timings[].duration_seconds` | How long each API call took |
| `task_timings[].model` | Which model actually responded |
| `task_timings[].task` | What type of task (summarize/extract) |
| `duration_seconds` (cycle total) | End-to-end cycle time |
| `cost_estimate` | Accumulated API costs |

**Analysis queries:**
- Average time per task type
- Fallback trigger rate
- Model performance over time
- Cost per cycle at scale

---

## Next Steps

1. **Run benchmark daily** - Model performance varies; track over time
2. **Adjust fallbacks based on data** - Use actual timings, not assumptions
3. **Add more fallback options** - Consider regional providers, local models
4. **Implement smart routing** - Route to fastest available model automatically

---

*Performance data will be collected in cycle states. Review `meta/orchestrator/*.json` files to analyze your specific results.*
