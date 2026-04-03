# Breadbasket Comparison Loop Run

**Date:** 2026-04-02  
**Branch:** breadbasket  
**Run type:** comparison  
**Status:** complete

---

## Cycle Summary

This loop run compared wheat and rice correlation scenarios to test whether the correlation/transmission structure generalizes across crop families.

**Question:** Does the correlation/transmission structure hold across wheat and rice, or are there crop-specific mechanisms that require structure revision?

---

## Stages Completed

### Stage 1: Frame the inquiry
- Defined comparison question (crop generalization test)
- Identified variants to compare (Russia-Europe wheat, Southeast Asia rice)
- Set success criteria (structure holds vs. requires revision)

### Stage 2: Assemble starting evidence
- Reviewed existing wheat evidence base (Heino 2023, Russia 2010 case, USDA data)
- Reviewed existing rice evidence base (FAO, USDA rice outlook, export restriction cases)
- Identified evidence gaps (rice climate-yield studies weaker than wheat)

### Stage 3: Generate candidate branches
- Not applicable (comparison pass, not generation)

### Stage 4: Ground the most promising branch
- Not applicable (comparison pass, not grounding)

### Stage 5: Create branch variants
- Generated Southeast Asia rice correlation shock variant
- Extracted 3 new components (India-rice, Southeast Asia-rice, rice export restriction)

### Stage 6: Compare the variants
- Generated comparison table via `curate compare` command
- Wrote comparison synthesis (`2026-04-02-wheat-vs-rice-crop-comparison.md`)
- Identified shared mechanisms and crop-specific differences

### Stage 7: Evaluate and curate
- Both variants marked "keep"
- Rice variant needs stronger climate-yield grounding (recommended next pass)
- Structure refined: broad correlation (wheat) vs. acute correlation (rice) subtypes

### Stage 8: Synthesize across branches
- Not applicable (single-branch comparison)

### Stage 9: Assess cycle maturity
- Structure holds across crops (validation success)
- Subtype distinction adds precision without fragmentation
- Ready for next comparison (maize? cross-crop simultaneous stress?)

---

## Artifacts Produced

| Artifact | Path | Status |
|----------|------|--------|
| Run manifest | `meta/runs/2026-04-02-breadbasket-comparison.json` | created |
| Scenario variant | `research/scenarios/2026-04-02-southeast-asia-rice-correlation-shock.md` | created |
| Comparison synthesis | `research/syntheses/2026-04-02-wheat-vs-rice-crop-comparison.md` | created |
| Component: India-rice | `meta/components/region-india-rice.yaml` | created |
| Component: Southeast Asia-rice | `meta/components/region-southeast-asia-rice.yaml` | created |
| Component: Rice export restriction | `meta/components/hazard-rice-export-restriction.yaml` | created |
| Comparison table | `meta/generated/comparison-wheat-vs-rice.md` | created |

---

## Curation Decisions

### Keep
- Russia-Europe wheat trade shock (strongest variant)
- Southeast Asia rice correlation shock (most generative for structure testing)

### Revise
- Northern wheat correlation shock (may be redundant with Russia-Europe)
- Rice scenario (needs stronger climate-yield grounding)

### Discard
- None this cycle

---

## Robust vs. Brittle Steps

### Robust
- Component extraction (YAML schema works well)
- Comparison table generation (`curate compare` command)
- Structure subtype distinction (broad vs. acute)

### Brittle
- Rice evidence grounding (climate-yield studies not as strong as wheat)
- Importer archetype extension (need Philippines, Indonesia cases)

---

## Readiness for Scaling

**This loop could be repeated** for:
- Maize correlation testing (third crop)
- Cross-crop simultaneous stress (wheat AND rice)
- Importer archetype comparison (Philippines vs. Egypt)

**Not ready to scale to cheaper models:**
- Evidence synthesis requires strong model capability
- Structure refinement requires human judgment

---

## Next Recommended Pass

**For breadbasket branch:** `grounding`

**Why:** Rice variant needs stronger climate-yield evidence to match wheat evidence base.

**Expected outputs:**
- Rice climate-yield grounding note
- Rice exporter correlation evidence note
- Importer archetype variants (Philippines, Indonesia)

---

## Method Lessons

1. **Crop selection matters for structure testing** — Testing across crops with different trade dynamics reveals structure boundaries better than testing within one crop family.

2. **Acute cases are methodologically valuable** — Rice's thinner market makes the correlation mechanism more visible, not less generalizable.

3. **Subtypes refine without fragmenting** — Distinguishing broad vs. acute correlation adds precision without creating separate structure types.

---

*This loop-run record is complete. It should be referenced in the branch manifest and used for future cycle planning.*
