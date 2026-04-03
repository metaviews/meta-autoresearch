# Wealth-Concentration Comparison Loop Run

**Date:** 2026-04-02  
**Branch:** wealth-concentration  
**Run type:** comparison  
**Status:** complete

---

## Cycle Summary

This loop run compared financial and compute concentration scenarios to test whether the hybrid concentration structure (correlation/transmission + design/rule conflict) generalizes across non-climate domains.

**Question:** Does the concentration structure hold across financial and compute domains, or does compute introduce fundamentally different mechanisms?

---

## Stages Completed

### Stage 1: Frame the inquiry
- Defined comparison question (hybrid structure generalization test)
- Identified variants to compare (US asset-regime, AI compute concentration)
- Set success criteria (hybrid holds vs. compute resolves to single structure)

### Stage 2: Assemble starting evidence
- Reviewed existing finance evidence (WID 2022 report, asset regime analysis)
- Reviewed existing compute evidence (TSMC concentration, data center scaling)
- Identified evidence gaps (compute concentration evidence weaker than finance)

### Stage 3: Generate candidate branches
- Not applicable (comparison pass, not generation)

### Stage 4: Ground the most promising branch
- Not applicable (comparison pass, not grounding)

### Stage 5: Create branch variants
- Generated AI compute concentration variant
- Extracted 5 new components (TSMC Taiwan, data center compute, chip supply disruption, compute access compounding, export control regime)

### Stage 6: Compare the variants
- Generated comparison table via `curate compare` command
- Wrote comparison synthesis (`2026-04-02-finance-vs-compute-concentration.md`)
- Identified shared mechanisms and domain-specific differences

### Stage 7: Evaluate and curate
- Both variants marked "keep"
- Compute variant needs stronger case evidence (recommended next pass)
- Structure refined: financial concentration vs. infrastructure concentration subtypes

### Stage 8: Synthesize across branches
- Hybrid structure is stable, not transitional
- Non-climate portability strengthening (two domains show same structure)

### Stage 9: Assess cycle maturity
- Structure holds across domains (validation success)
- Subtype distinction adds precision without fragmentation
- Ready for third domain test (biotech? energy?)

---

## Artifacts Produced

| Artifact | Path | Status |
|----------|------|--------|
| Run manifest | `meta/runs/2026-04-02-wealth-concentration-comparison.json` | created |
| Scenario variant | `research/scenarios/2026-04-02-ai-compute-concentration-stress.md` | created |
| Comparison synthesis | `research/syntheses/2026-04-02-finance-vs-compute-concentration.md` | created |
| Component: TSMC Taiwan | `meta/components/region-tsmc-taiwan.yaml` | created |
| Component: Data center compute | `meta/components/infra-data-center-compute.yaml` | created |
| Component: Chip supply disruption | `meta/components/hazard-chip-supply-disruption.yaml` | created |
| Component: Compute access compounding | `meta/components/mech-compute-access-compounding.yaml` | created |
| Component: Export control regime | `meta/components/inst-export-control-regime.yaml` | created |
| Comparison table | `meta/generated/comparison-finance-vs-compute.md` | created |

---

## Curation Decisions

### Keep
- US Asset-Regime (strongest financial grounding)
- AI Compute Concentration (most generative for infrastructure subtype)

### Revise
- Private-Credit Squeeze (may be redundant with transmission component)
- Compute scenario (needs stronger case evidence: fab disruptions, energy constraints)

### Discard
- None this cycle

---

## Robust vs. Brittle Steps

### Robust
- Component extraction (YAML schema works well)
- Comparison table generation (`curate compare` command)
- Subtype distinction (financial vs. infrastructure concentration)

### Brittle
- Compute evidence grounding (specific cases not well documented)
- Geographic concentration evidence (TSMC data center locations need verification)

---

## Readiness for Scaling

**This loop could be repeated** for:
- Biotech lab capacity concentration
- Energy storage concentration
- Third non-climate domain test

**Not ready to scale to cheaper models:**
- Structure analysis requires strong model capability
- Hybrid refinement requires human judgment

---

## Next Recommended Pass

**For wealth-concentration branch:** `grounding`

**Why:** Compute variant needs stronger case evidence to match finance evidence base.

**Expected outputs:**
- Compute concentration case studies note (TSMC, data center constraints)
- Geographic concentration evidence note
- Third domain variant (biotech or energy)

---

## Method Lessons

1. **Hybrid structures can be stable** — The method initially assumed hybrids might resolve to single structures. This comparison suggests hybrid is a legitimate stable form for concentration phenomena.

2. **Infrastructure concentration is more explicit** — Physical constraints (chips, energy, geography) make the concentration mechanism more visible than financial abstraction.

3. **Non-climate portability is strengthening** — Two non-climate domains (finance, compute) now show the same hybrid structure, suggesting the method travels beyond climate.

---

*This loop-run record is complete. It should be referenced in the branch manifest and used for future cycle planning.*
