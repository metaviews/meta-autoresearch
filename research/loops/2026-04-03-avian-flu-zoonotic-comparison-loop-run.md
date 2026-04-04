# Avian Flu Zoonotic Comparison Loop Run

**Date:** 2026-04-03  
**Branch:** avian-flu-zoonotic  
**Run type:** comparison  
**Status:** complete

---

## Cycle Summary

This loop run established a new domain proving-ground (biological volatility) with HPAI H5N1 and zoonotic transmission as the test case. Three bounded variants were generated to test whether HPAI follows correlation/transmission, sequence failure, design/rule conflict, or hybrid structure.

**Question:** What structure type does HPAI follow: correlation (US dairy trade amplification), sequence (wild bird transmission pathway), design/rule conflict (sea lion biosecurity mismatch), or hybrid?

---

## Stages Completed

### Stage 1: Frame the inquiry
- Defined comparison question (structure type identification)
- Identified three variants testing different structure hypotheses
- Set success criteria (identify best-fitting structure type)

### Stage 2: Assemble starting evidence
- Created grounding note (HPAI zoonotic transmission evidence base)
- Identified structure type hypotheses from grounding (correlation, sequence, design/rule, hybrid)
- Documented evidence gaps (trade quantification, transmission dynamics, biosecurity adequacy)

### Stage 3: Generate candidate branches
- Not applicable (first cycle for new branch)

### Stage 4: Ground the most promising branch
- Not applicable (first cycle, grounding already done in Stage 2)

### Stage 5: Create branch variants
- Generated three bounded variants:
  - US Dairy Herd Outbreak (correlation/transmission hypothesis)
  - Wild Bird Migration Pathway (sequence failure hypothesis)
  - South American Sea Lion Mass Mortality (design/rule conflict hypothesis)
- Extracted initial components (to be expanded as branch develops)

### Stage 6: Compare the variants
- Generated comparison table via `curate compare` command
- Wrote comparison synthesis (`2026-04-03-hpai-structure-type-comparison.md`)
- Identified hybrid structure as best fit (3 components: correlation + sequence + design/rule)

### Stage 7: Evaluate and curate
- All three variants marked "keep" (each reveals different structure component)
- Sea Lion variant needs stronger agricultural disruption connection
- Wild Bird variant needs quantified sequential risk

### Stage 8: Synthesize across branches
- HPAI hybrid structure has 3 components (vs. wealth-concentration's 2)
- Biological volatility is different driver from climate volatility
- New domain portability worked from first branch (unlike wealth-concentration which needed multiple passes)

### Stage 9: Assess cycle maturity
- L1 (exploratory) → ready for L2 (grounded)
- Structure type identified (hybrid with 3 components)
- Ready for next grounding pass to strengthen each component

---

## Artifacts Produced

| Artifact | Path | Status |
|----------|------|--------|
| Branch manifest | `meta/branches/avian-flu-zoonotic.json` | created |
| Run manifest | `meta/runs/2026-04-03-avian-flu-zoonotic-comparison.json` | created |
| Grounding note | `research/notes/2026-04-03-hpai-zoonotic-grounding-note.md` | created |
| Scenario variant | `research/scenarios/2026-04-03-us-dairy-herd-hpai-outbreak.md` | created |
| Scenario variant | `research/scenarios/2026-04-03-wild-bird-migration-hpai-pathway.md` | created |
| Scenario variant | `research/scenarios/2026-04-03-south-american-sea-lion-hpai-mortality.md` | created |
| Comparison synthesis | `research/syntheses/2026-04-03-hpai-structure-type-comparison.md` | created |
| Branch packet | `meta/generated/avian-flu-zoonotic-*.md` (4 files) | created |

---

## Curation Decisions

### Keep
- All three variants (each reveals different structure component)
- Parent scenario (organizational anchor for HPAI branch)

### Revise
- Sea Lion variant (needs stronger agricultural disruption connection)
- Wild Bird variant (needs quantified sequential risk accumulation)

### Discard
- None this cycle

---

## Robust vs. Brittle Steps

### Robust
- Structure type identification (hybrid emerged clearly from three variants)
- Bounded named cases (US dairy, wild bird flyways, sea lions are well-documented)
- Comparison methodology (three-way comparison worked well)

### Brittle
- Agricultural disruption connection for sea lion variant (wildlife biosecurity is narrower than agriculture)
- Transmission dynamics quantification (cattle-to-cattle R0 not yet well understood)

---

## Readiness for Scaling

**This loop established a new domain proving-ground.** The method can now:
- Test biological volatility as a driver different from climate or financial
- Accommodate multi-component hybrids (3 components vs. previous 2)
- Identify structure type from first cycle (faster than wealth-concentration which needed multiple passes)

**Not ready to scale to cheaper models:**
- Structure identification requires strong model capability
- New domain needs human judgment for grounding adequacy

---

## Next Recommended Pass

**For avian-flu-zoonotic branch:** `grounding`

**Why:** Each hybrid component needs stronger evidence:
- Correlation: trade restriction cascade quantification
- Sequence: transmission stage probabilities
- Design/rule: biosecurity protocol inadequacy documentation

**Expected outputs:**
- HPAI trade restriction evidence note
- HPAI transmission chain quantification note
- Biosecurity protocol adequacy assessment

---

## Method Lessons

1. **Multi-component hybrids are possible** — HPAI reveals 3 structure components operating simultaneously. The method should accommodate hybrids with more than 2 components.

2. **Biological volatility is different from climate volatility** — Viral evolution, host jumping, and wild bird reservoir create dynamics that climate non-stationarity does not. The method handles this, but structure types need biological adaptation.

3. **New domain portability can work immediately** — Unlike wealth-concentration which needed multiple passes to stabilize, HPAI's hybrid structure emerged immediately from three bounded variants. This may be because the evidence base is more current and active.

---

*This loop-run record is complete. It should be referenced in the branch manifest and used for future cycle planning.*
