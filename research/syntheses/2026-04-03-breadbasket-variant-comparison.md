# Breadbasket Variant Comparison: Wheat vs. Rice, Continental vs. Archipelago

**Date:** 2026-04-03  
**Type:** Comparison synthesis  
**Branch:** breadbasket  
**Status:** draft

---

## Purpose

This synthesis compares all breadbasket variants across two dimensions: crop type (wheat vs. rice) and importer geography (continental vs. archipelago). It tests whether the correlation/transmission structure holds across these variations and identifies subtypes.

**Questions this answers:**
1. Does correlation/transmission hold across wheat and rice?
2. Do importer archetypes (continental state, fragile commercial, archipelago) reveal different transmission channels?
3. What subtypes emerge from this comparison?

---

## Variants Compared

| Aspect | Russia-Europe Wheat | Russia-China Wheat | Egypt Wheat | Yemen Wheat | SE Asia Rice | Philippines Rice |
|--------|---------------------|--------------------|-------------|-------------|--------------|-----------------|
| **Crop** | Wheat | Wheat | Wheat | Wheat | Rice | Rice |
| **Role** | Exporter correlation | Buffer loss | Continental importer | Fragile importer | Exporter correlation | Archipelago importer |
| **Mechanism** | Dual-node correlation | Buffer loss confidence | Fiscal amplification | Commercial fragmentation | Exporter correlation + thin trade | Archipelago distribution |
| **Trade share** | ~20%+ | ~20%+ | ~50% of consumption | ~80% of consumption | ~5-10% | ~10-15% of consumption |
| **Transmission** | Export restrictions → price spike | Stock conservation → demand shift | Subsidy burden → fiscal crisis | FX/port constraints → acute shortage | Thin market → acute price spike | Distribution logistics → island-level shortage |
| **Evidence strength** | High (Heino 2023, USDA) | Moderate (IndexMundi, USDA FAS) | High (FAO, World Bank) | High (FAO, ReliefWeb) | Moderate (FAO, trade data) | Moderate (USDA FAS, NFA) |
| **Status** | Strongest variant | Generative variant | Continental archetype | Fragile archetype | Crop generalization | Archipelago archetype |

---

## Crop Comparison: Wheat vs. Rice

### Shared Mechanisms
Both crops exhibit correlation/transmission failure:
1. **Exporter concentration** — Few major exporters means disruptions have outsized impact
2. **Trade restriction amplification** — Export bans cascade through global markets
3. **Import-dependent vulnerability** — Countries relying on imports face supply gaps

### Key Differences

| Difference | Wheat | Rice |
|------------|-------|------|
| **Trade share** | 20%+ of production | 5-10% of production |
| **Market depth** | Deep, liquid markets | Thin, illiquid markets |
| **Substitution** | Possible (other grains) | Limited (cultural staple) |
| **Exporter count** | More diversified (Russia, EU, US, Australia) | Highly concentrated (India 40%, Thailand+Vietnam 35%) |
| **Price elasticity** | Moderate | Low (cultural/political pressure) |

**Judgment:** ✅ **Structure holds across both crops.** Correlation/transmission mechanism is the same, but rice has **higher amplification** due to thin markets and concentrated exporters.

**Subtype identified:** 
- **Broad correlation** (wheat) — More diversified exporters, deeper markets, substitution possible
- **Acute correlation** (rice) — Concentrated exporters, thin markets, limited substitution

---

## Importer Geography Comparison: Continental vs. Archipelago vs. Fragile

### Continental State Procurement (Egypt)
- Large-scale state purchasing (GASC tenders)
- Fiscal amplification channel (subsidy burden converts procurement to fiscal crisis)
- Political feedback loop (bread prices trigger political responses)
- Moderate logistics complexity (Nile corridor, ports)

### Fragile Commercial (Yemen)
- Fragmented commercial importing
- FX and port constraints
- Conflict overlay
- Acute consequence threshold (famine risk)

### Archipelago State (Philippines)
- State + private procurement mix
- **Distribution logistics amplification** — Rice must reach 7,000+ islands
- Limited domestic fallback (85-90% self-sufficient, imports fill marginal but critical gap)
- High logistics complexity (inter-island shipping)

**Judgment:** ✅ **Importer geography affects transmission channel, not structure applicability.** All three exhibit correlation/transmission failure, but the dominant transmission channel varies:
- Continental: fiscal amplification
- Fragile: commercial fragmentation
- Archipelago: distribution logistics

**Subtype identified:**
- **Fiscal amplifier** (Egypt) — Procurement stress → fiscal crisis
- **Acute fragile** (Yemen) — Procurement failure → immediate humanitarian crisis
- **Logistics amplifier** (Philippines) — Procurement stress → distribution cascade

---

## Overall Structure Assessment

### Correlation/Transmission Structure Validated

The structure holds across:
- **Two crop types** (wheat, rice)
- **Three importer geographies** (continental, fragile, archipelago)
- **Multiple transmission channels** (fiscal, commercial, logistics)

### Subtype Taxonomy

| Dimension | Subtype | Characteristics | Example |
|-----------|---------|-----------------|---------|
| **Crop** | Broad correlation | Diversified exporters, deep markets, substitution possible | Wheat |
| | Acute correlation | Concentrated exporters, thin markets, limited substitution | Rice |
| **Importer** | Fiscal amplifier | State procurement, subsidy burden, political feedback | Egypt |
| | Acute fragile | Commercial fragmentation, FX/port constraints, conflict | Yemen |
| | Logistics amplifier | Distribution cascade, limited fallback, high complexity | Philippines |

### What This Changes in the Branch

**Keep:**
- All variants (each reveals different subtype combination)
- Correlation/transmission structure name

**Revise:**
- Add subtype taxonomy to branch documentation
- Update evaluation matrix to weight "market depth" and "distribution complexity" for rice/archipelago cases

**Add:**
- Maize as third crop test (does correlation structure hold?)
- Cross-crop simultaneous stress scenario (wheat AND rice stress together)

---

## Curation Decisions

### Keep
- Russia-Europe wheat (strongest: best evidence, clearest mechanism)
- SE Asia rice (most generative: opens crop generalization, thin market dynamics)
- Egypt (continental archetype: fiscal amplification)
- Yemen (fragile archetype: acute consequences)
- Philippines (archipelago archetype: logistics cascade)

### Revise
- Russia-China wheat (buffer loss mechanism overlaps with Russia-Europe; needs clearer distinction)
- Northern wheat correlation (broad framing, redundant with Russia-Europe)

### Merge
- Consider merging Northern wheat into parent scenario (redundant with Russia-Europe)

### Discard
- Northern wheat as standalone variant (merge into parent)

---

## Strongest and Most Generative

| Category | Variant | Rationale |
|----------|---------|-----------|
| **Strongest** | Russia-Europe wheat trade shock | Best evidence grounding, clearest dual-node mechanism |
| **Most Generative** | SE Asia rice correlation shock | Opens crop generalization, thin market dynamics, acute correlation subtype |
| **Weakest** | Northern wheat correlation shock | Broad framing, overlaps with Russia-Europe, less operationally specific |

---

## Next Research Step

**Recommended pass:** `variant`

**Why:** The branch now has strong subtype taxonomy. Next step is to test whether structure holds for a third crop (maize) and to develop cross-crop simultaneous stress scenario.

**Expected outputs:**
- Maize correlation variant (third crop test)
- Cross-crop simultaneous stress scenario (wheat AND rice stress)
- Subtype taxonomy documentation for branch-maturity.md

---

## Method Lesson

**What this teaches the method:**

1. **Structure subtypes can be multi-dimensional** — Breadbasket has subtypes on two dimensions (crop type, importer geography), creating a subtype matrix rather than a linear taxonomy.

2. **Thin markets amplify correlation** — Rice's 5-10% trade share means small disruptions create large price impacts. The method should track market depth as a subtype parameter.

3. **Distribution logistics matter for importers** — Archipelago importers face cascading distribution failures beyond procurement. The method should track logistics complexity as a subtype parameter.

4. **Cross-crop comparison validates structure generality** — If correlation/transmission holds across wheat and rice (very different market dynamics), it likely generalizes to other staple crops.

---

## Links

- Related branches:
  - `meta/branches/breadbasket.json`
- Related variants:
  - `research/scenarios/2026-03-27-russia-europe-wheat-trade-shock.md`
  - `research/scenarios/2026-04-02-southeast-asia-rice-correlation-shock.md`
  - `research/scenarios/2026-04-02-philippines-rice-import-stress.md`
- Related components:
  - `mech:supplier-cluster-concentration`
  - `mech:procurement-squeeze`
  - `region:philippines-rice`
  - `hazard:logistics-disruption`

---

*This synthesis is a draft. It should be reviewed and either kept, revised, or discarded based on its usefulness for branch development.*
