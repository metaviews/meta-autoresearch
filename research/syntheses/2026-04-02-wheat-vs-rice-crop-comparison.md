# Wheat vs. Rice: Crop Correlation Comparison

**Date:** 2026-04-02  
**Type:** Comparison synthesis  
**Branch:** breadbasket  
**Status:** draft

---

## Purpose

This synthesis compares wheat and rice correlation scenarios to test whether the correlation/transmission structure generalizes across crop families or whether crop-specific mechanisms require structure revision.

**Questions this answers:**
1. Do wheat and rice share the same correlation/transmission mechanism?
2. What crop-specific differences matter for the structure?
3. Should the breadbasket branch be crop-agnostic or crop-specific?

---

## Variants Compared

| Aspect | Wheat (Russia-Europe) | Rice (Southeast Asia) |
|--------|----------------------|----------------------|
| **Primary export nodes** | Russia, Europe | India, Thailand, Vietnam |
| **Trade share of production** | ~20%+ | ~5-10% (thinner) |
| **Exporter concentration** | Moderate (multiple exporters) | High (India ~40% of trade) |
| **Downstream dependence** | Broad (many importers) | Acute (staple for billions) |
| **Substitution possibilities** | Moderate (other grains) | Limited (cultural staple) |
| **Policy response** | Export restrictions documented | Export restrictions documented |
| **Price transmission speed** | Fast | Faster (thinner market) |

---

## Shared Mechanisms (Structure Holds)

Both crops exhibit the core correlation/transmission mechanism:

1. **Correlated production stress** — Hot-dry conditions affect multiple producing regions simultaneously
2. **Export restriction amplification** — Policy responses amplify physical shortfalls into trade shocks
3. **Importer vulnerability** — Import-dependent buyers face procurement stress, not just price increases
4. **Thin trade concentration** — Trade is a small slice of production, concentrating shocks

**Judgment:** The correlation/transmission structure **holds across both crops**. The mechanism is not wheat-specific.

---

## Crop-Specific Differences (Structure Refinement Needed)

However, rice exhibits **amplified** characteristics that refine the structure:

| Difference | Implication for Structure |
|------------|--------------------------|
| **Thinner trade share** (5-10% vs. 20%+) | Small production shortfalls create larger trade shocks |
| **Higher exporter concentration** (India ~40%) | Single-node failure matters more than in wheat |
| **Limited substitution** | Downstream food-security effects are faster and more acute |
| **Cultural staple status** | Political responses may be more aggressive (export bans) |

**Judgment:** Rice is not a different structure—it is a **more acute form** of the same structure.

---

## Structure Refinement: Two Subtypes

Based on this comparison, the correlation/transmission structure has **two subtypes**:

### Subtype A: Broad Correlation (Wheat)
- Multiple exporters with moderate concentration
- Trade share is significant but not extreme
- Substitution across grains is possible
- Downstream effects are economic and political

### Subtype B: Acute Correlation (Rice)
- High exporter concentration (one dominant node)
- Trade share is very thin
- Substitution is limited or culturally unacceptable
- Downstream effects are immediate food-security crises

**Method implication:** The structure type should be refined to distinguish these subtypes, not collapsed into one generic "correlation" category.

---

## What This Changes in the Branch

### Keep
- The core correlation/transmission structure name
- The mechanism logic (correlation → restriction → transmission)
- The downstream importer archetype framework (Egypt/Yemen now applies to rice too)

### Revise
- Add crop-specific grounding notes (wheat has Heino 2023, rice needs equivalent)
- Distinguish broad vs. acute correlation subtypes in future variants
- Update evaluation matrix to weight "thin trade" and "exporter concentration" more heavily

### Add
- Rice-specific importer archetypes (Philippines, Indonesia, Nigeria)
- Comparison with maize (third crop to test structure further)
- Cross-crop correlation scenario (wheat AND rice stress simultaneously)

---

## Curation Decisions

### Keep (Both Variants)
- **Russia-Europe wheat:** Strongest evidence base, clearest transmission mechanism
- **Southeast Asia rice:** Tests crop generalization, adds acute correlation subtype

### Revise
- **Northern wheat correlation shock:** May be redundant with Russia-Europe variant; consider merging
- **Rice scenario:** Needs stronger climate-yield evidence (currently relies on trade/policy evidence)

### Discard
- None yet—both variants are generative for different reasons

---

## Strongest and Most Generative

| Category | Variant | Rationale |
|----------|---------|-----------|
| **Strongest** | Russia-Europe wheat | Best evidence grounding, clearest mechanism |
| **Most Generative** | Southeast Asia rice | Opens crop generalization question, acute subtype |
| **Weakest** | Northern wheat correlation | Broader framing, less operational than Russia-Europe |

---

## Next Research Step

**Recommended pass:** `grounding`

**Why:** The rice variant needs stronger climate-yield evidence to match the wheat evidence base. Specifically:
- Climate-yield studies for South/Southeast Asian rice (parallel to Heino 2023 for wheat)
- Historical case of simultaneous India-Thailand-Vietnam stress (parallel to Russia 2010)
- Importer-specific grounding (Philippines, Indonesia procurement patterns)

**Expected outputs:**
- Rice climate-yield grounding note
- Rice exporter correlation evidence note
- Importer archetype variants (Philippines, Indonesia)

---

## Method Lesson

**What this teaches the method:**

1. **Structure types can have subtypes** — Not all correlation is equally acute; the method should distinguish intensity levels within a structure.

2. **Crop selection matters for structure testing** — Testing across crops with different trade dynamics (wheat vs. rice) reveals structure boundaries better than testing within one crop family.

3. **Acute cases are methodologically valuable** — Rice's thinner market and higher concentration make the correlation mechanism more visible, not less generalizable.

---

## Links

- Related runs:
  - `meta/runs/2026-04-02-breadbasket-comparison.json`
- Related scenarios:
  - `research/scenarios/2026-03-27-russia-europe-wheat-trade-shock.md`
  - `research/scenarios/2026-04-02-southeast-asia-rice-correlation-shock.md`
- Related syntheses:
  - `research/syntheses/2026-03-27-russia-europe-vs-russia-china-wheat-comparison.md`
  - `research/syntheses/2026-03-28-egypt-vs-yemen-importer-archetypes.md`
- Related components:
  - `mech:export-restriction-amplification`
  - `mech:supplier-cluster-concentration`
  - `region:russia-wheat`
  - `region:india-rice`

---

*This synthesis is a draft. It should be reviewed and either kept, revised, or discarded based on its usefulness for branch development.*
