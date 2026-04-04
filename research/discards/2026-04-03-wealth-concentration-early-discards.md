# Wealth-Concentration Early Discards: Transmission-Only Pruning

**Date:** 2026-04-03  
**Branch:** wealth-concentration  
**Type:** Discard record  
**Status:** archived

---

## Discarded Artifacts

### 1. Private-Credit Resilience Squeeze

**File:** `research/scenarios/2026-03-28-private-credit-resilience-squeeze.md`  
**Decision:** Merge into US Asset-Regime variant  
**Date:** 2026-04-03

**Why discarded:**
- Tests only transmission component of hybrid structure, not rule-conflict component
- Overlaps significantly with transmission mechanism covered in US Asset-Regime variant
- Marked as weakest variant in branch manifest
- Does not add distinct mechanism beyond what stronger variants already cover
- Private credit is a transmission channel within the broader asset-regime structure, not a distinct scenario

**What was learned:**
- Hybrid structure variants should test both transmission AND rule-conflict components, not just one
- Transmission-only variants are redundant when a stronger variant covers both components
- This is a general principle: hybrid structure branches should require both components for active variant status

**Impact on kept work:**
- US Asset-Regime: strongest variant, clearest hybrid mechanism (both transmission and rule-conflict)
- AI Compute Concentration: tests infrastructure subtype, geographic explicitness
- Pandemic Preparedness: tests biosecurity subtype, public good dimension
- India Last-Mile Credit Squeeze: tests transmission in developing economy context (distinct from US private credit)

---

### 2. Wealth-Concentration Structural Stress (Parent Scenario)

**File:** `research/scenarios/2026-03-28-wealth-concentration-structural-stress.md`  
**Decision:** Downgrade to organizational parent  
**Date:** 2026-04-03

**Why downgraded:**
- Parent scenario is too broad to be method-shaping
- Bounded variants (US Asset-Regime, AI Compute, Pandemic, India Credit) carry the structural signal
- This pattern holds across all branches (breadbasket, whiplash, hydrologic)

**What was learned:**
- Parent scenarios are useful for framing but not for method-shaping
- The branch became more useful when it shifted from parent-focused to variant-focused
- Non-climate branches especially need bounded grounding early; broad parent framing is insufficient

**Impact on kept work:**
- Variants carry the structural signal across 3 non-climate domains
- Parent remains as organizational anchor but not as active comparison target

---

## Curation Pressure Summary

| Variant | Decision | Rationale |
|---------|----------|-----------|
| Private-credit resilience squeeze | Merge into US Asset-Regime | Transmission-only, redundant |
| Wealth-concentration structural stress (parent) | Downgrade to organizational | Too broad for active comparison |
| US Asset-Regime | Keep (strongest) | Best evidence, clearest hybrid mechanism |
| AI Compute Concentration | Keep | Tests infrastructure subtype |
| Pandemic Preparedness | Keep (most generative) | Opens biosecurity subtype, public good |
| India Last-Mile Credit Squeeze | Keep | Tests developing economy transmission |

---

## Method Lesson

**What this discard teaches:**
- Hybrid structure variants must test both components (transmission + rule-conflict) to earn active status
- Transmission-only variants are redundant when a stronger variant covers both components
- This criterion should be added to branch-maturity.md for hybrid structure branches
- Non-climate branches need bounded grounding earlier than climate branches

---

## Links

- Related branch: `meta/branches/wealth-concentration.json`
- Related syntheses:
  - `research/syntheses/2026-04-02-finance-compute-pandemic-comparison.md`
  - `research/syntheses/2026-04-02-wealth-concentration-maturity-assessment.md`

---

*This discard record is archived. It documents explicit curation decisions for the wealth-concentration branch.*
