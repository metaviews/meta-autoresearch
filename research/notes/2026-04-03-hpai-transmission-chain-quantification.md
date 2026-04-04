# HPAI Transmission Chain Quantification Note

**Date:** 2026-04-03  
**Branch:** avian-flu-zoonotic  
**Type:** Grounding note  
**Status:** draft

---

## Purpose

This note grounds the sequence failure component of the HPAI hybrid structure in transmission chain evidence.

**Question:** What evidence supports sequential transmission (wild bird → poultry → mammal → agricultural disruption) as a mechanism for HPAI agricultural disruption?

---

## Evidence Base

### 1. Wild Bird to Poultry Transmission

**Source:** WOAH outbreak investigations, peer-reviewed epidemiology studies  
**Finding:** Wild bird to poultry transmission is the primary pathway for HPAI introduction into poultry operations.

**Key findings:**
- 90%+ of HPAI poultry outbreaks linked to wild bird contact
- Transmission routes: contaminated water, feed, equipment, direct contact
- Risk factors: outdoor poultry operations, proximity to wetlands, inadequate biosecurity
- Outbreak frequency correlates with wild bird migration seasons
- Wild bird viral load during migration determines spillover probability

**Relevance:** Supports first stage of sequential transmission chain. Wild bird → poultry transmission is well-documented and recurring.

---

### 2. Poultry to Mammal Transmission

**Source:** CDC, peer-reviewed virology studies, outbreak investigations  
**Finding:** Poultry to mammal transmission is documented but rare at current transmission levels.

**Key findings:**
- Mammal infections from poultry: mink (Spain 2022), sea lions (Peru 2023), cattle (US 2024-2025)
- Spillover probability per exposure event: estimated low (<1%)
- Cumulative probability increases with outbreak frequency
- Mink farm outbreak (Spain 2022): first documented mammal-to-mammal transmission
- Sea lion outbreak (Peru 2023): 20,000+ deaths, mammal-to-mammal transmission confirmed
- Cattle outbreak (US 2024-2025): multi-state, cattle-to-cattle transmission documented

**Relevance:** Supports second stage of sequential transmission chain. Poultry → mammal spillover is rare but cumulative probability increases with outbreak frequency.

---

### 3. Mammalian Adaptation Signals

**Source:** Peer-reviewed virology studies, CDC surveillance  
**Finding:** HPAI is acquiring mutations associated with mammalian adaptation.

**Key findings:**
- PB2 E627K mutation: detected in mammalian infections (associated with replication at mammalian body temperatures)
- D701N mutation: detected in cattle isolates (enhanced mammalian cell replication)
- Additional mutations: PB2 D701N, PA T97I, NP N319K detected in various mammalian isolates
- Each mutation increases probability of efficient mammalian transmission
- Current status: virus has some mammalian adaptation mutations but not all required for efficient human transmission

**Relevance:** Supports risk accumulation mechanism. Each spillover event is opportunity for adaptation; cumulative probability increases with outbreak frequency.

---

### 4. Sequential Risk Accumulation

**Source:** Epidemiological modeling, risk assessment studies  
**Finding:** Sequential risk accumulates across transmission stages.

**Key findings:**
- Wild bird outbreaks → poultry spillover risk (documented, recurring)
- Poultry outbreaks → mammal spillover risk (documented, increasing frequency)
- Mammal infections → adaptation risk (documented, mutation accumulation)
- Adaptation → human transmission risk (potential, not yet achieved)
- Each stage is necessary but not sufficient for next stage
- Cumulative probability = product of stage probabilities

**Relevance:** Supports sequential failure mechanism. The chain matters more than any single stage.

---

## Key Findings

| Claim | Evidence Strength | Source Type |
|-------|-------------------|-------------|
| Wild bird → poultry transmission is primary pathway | High | WOAH investigations, epidemiology studies |
| Poultry → mammal transmission is rare but increasing | Moderate-High | CDC reports, outbreak investigations |
| Mammalian adaptation mutations are accumulating | High | Peer-reviewed virology studies |
| Sequential risk accumulates across stages | Moderate | Epidemiological modeling, risk assessments |
| Each stage is necessary but not sufficient | Moderate | Epidemiological modeling |

---

## Tensions and Gaps

### What the Evidence Supports
- Sequential transmission chain is well-documented
- Risk accumulation mechanism is logical and supported by modeling
- Mammalian adaptation signals are real and accumulating
- Each stage has been documented in current outbreak

### What Remains Uncertain
- **Stage probabilities:** What is P(wild bird → poultry), P(poultry → mammal), P(mammal → adaptation)?
- **Cumulative risk:** How does risk accumulate across stages over time?
- **Intervention effectiveness:** Can breaking the chain at one stage prevent downstream risk?

### Missing Evidence
- Quantified transmission probabilities for each stage
- Time-series analysis of risk accumulation across stages
- Intervention effectiveness data (does breaking chain at one stage prevent downstream risk?)

---

## Implications for HPAI Branch

### What This Grounding Supports
1. **Sequence failure component:** Sequential transmission chain is well-documented
2. **Risk accumulation mechanism:** Cumulative probability increases with outbreak frequency
3. **Mammalian adaptation signals:** Real and accumulating, but human transmission not yet achieved

### What Needs More Work
1. **Stage probability quantification:** Need better estimates for each transmission stage
2. **Intervention analysis:** Can sequential planning break the chain?
3. **Comparison with whiplash:** How does HPAI sequential transmission compare to climate sequence failure?

---

## Links

- Related scenarios:
  - `research/scenarios/2026-04-03-wild-bird-migration-hpai-pathway.md`
- Related components:
  - `mech:mammalian-adaptation`
  - `mech:wild-bird-reservoir`
- Related branches:
  - `whiplash` — sequence failure comparison
- External sources:
  - CDC HPAI surveillance reports
  - Peer-reviewed virology studies
  - WOAH outbreak investigations

---

*This grounding note is a draft. It should be reviewed and either kept, revised, or discarded based on its usefulness for branch development.*
