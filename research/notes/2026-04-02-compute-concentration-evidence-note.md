# Compute Concentration Evidence Note

**Date:** 2026-04-02  
**Branch:** wealth-concentration  
**Type:** Grounding note  
**Status:** draft

---

## Purpose

This note grounds the AI compute concentration scenario in evidence about chip supply, data center infrastructure, and geographic concentration, parallel to how WID data grounds the US asset-regime variant.

**Question:** What evidence supports concentrated compute access creating compounding advantages and systemic fragility?

---

## Evidence Base

### 1. Chip Manufacturing Concentration

**Source:** Industry analysis (TSMC reports, semiconductor industry associations)  
**Finding:** TSMC produces 90%+ of leading-edge semiconductors (7nm and below), including virtually all advanced AI chips.

**Key findings:**
- TSMC Taiwan: ~90% of advanced chip production
- Samsung (Korea): Remaining share of advanced production
- Intel (US): Lagging in advanced nodes, transitioning to foundry model
- Geographic concentration: Taiwan is seismic and geopolitical risk zone

**Relevance:** Supports the geographic concentration mechanism—compute access depends on single geographic node.

---

### 2. AI Training Compute Requirements

**Source:** AI lab reports, industry analysis  
**Finding:** Frontier AI training now requires 10,000-100,000+ GPUs, creating massive capital and infrastructure barriers.

**Scale examples:**
- GPT-4 class models: Estimated 25,000-100,000 H100-equivalent GPUs
- Training runs cost: $50M-$500M+ for frontier models
- Cluster requirements: Specialized networking (InfiniBand), cooling, power (100MW+ facilities)

**Relevance:** Supports the access compounding mechanism—only well-funded actors can deploy frontier-scale compute.

---

### 3. Data Center Power and Cooling Constraints

**Source:** Utility reports, data center industry analysis  
**Finding:** AI data centers require 10-100x more power per rack than traditional data centers, creating siting and grid constraints.

**Key findings:**
- Power density: AI racks require 40-100kW vs. 5-10kW for traditional
- Grid capacity: Many regions cannot support 100MW+ facilities without major upgrades
- Cooling requirements: Water consumption 1-5 million gallons/day for large facilities
- Lead time: 2-4 years from site selection to operation

**Relevance:** Supports the infrastructure concentration mechanism—compute cannot be deployed everywhere, creating geographic bottlenecks.

---

### 4. Export Controls and Access Asymmetry

**Source:** US government export control announcements, industry reports  
**Finding:** Export controls on advanced AI chips create geographic access asymmetries, concentrating capability in approved regions.

**Key restrictions:**
- China restrictions (2022-2024): Advanced AI chips (A100, H100) and manufacturing equipment restricted
- Entity list: Specific Chinese AI companies blocked from accessing advanced chips
- Allied coordination: Netherlands (ASML), Japan joined export control framework

**Relevance:** Supports the regulatory concentration mechanism—policy explicitly concentrates compute access by geography.

---

### 5. Cloud Provider Concentration

**Source:** Cloud market share reports, AI infrastructure analysis  
**Finding:** Three cloud providers (AWS, Azure, GCP) control majority of cloud compute, with AI-specific capacity even more concentrated.

**Market dynamics:**
- Cloud capex: Hyperscalers account for majority of data center investment
- AI chip allocation: Priority to largest customers and strategic partners
- Vertical integration: Cloud providers designing custom AI chips (TPU, Trainium, Maia)

**Relevance:** Supports the access stratification mechanism—even within cloud, AI compute access is tiered.

---

### 6. Capital Concentration for AI Infrastructure

**Source:** Investment reports, AI funding analysis  
**Finding:** AI infrastructure investment is concentrated in a small number of well-funded actors.

**Investment patterns:**
- Frontier AI labs: OpenAI, Anthropic, Google DeepMind, Meta account for majority of frontier training runs
- Capital requirements: $1B+ raised for competitive frontier development
- Compute partnerships: Exclusive deals between labs and cloud providers

**Relevance:** Supports the compounding advantage mechanism—those with compute access attract more capital, which buys more compute.

---

## Key Findings

| Claim | Evidence Strength | Source Type |
|-------|-------------------|-------------|
| Chip manufacturing is geographically concentrated (TSMC Taiwan) | High | Industry reports, trade data |
| Frontier AI requires 10,000-100,000+ GPUs | High | Lab reports, industry analysis |
| Data center power/cooling creates siting constraints | High | Utility reports, industry analysis |
| Export controls create geographic access asymmetry | High | Government announcements, trade data |
| Cloud compute is concentrated (hyperscalers) | High | Market share reports |
| AI infrastructure investment is concentrated | High | Funding databases, investment reports |

---

## Tensions and Gaps

### What the Evidence Supports
- Compute concentration is real and measurable
- Geographic bottlenecks (TSMC, grid capacity) are documented
- Export controls explicitly concentrate access
- Capital requirements create barriers to entry

### What Remains Uncertain
- **Substitution possibilities:** Can alternative chips (non-TSMC, non-leading-edge) work for AI training?
- **Efficiency gains:** Will algorithmic improvements reduce compute requirements faster than concentration increases?
- **Geographic diversification:** Will TSMC Arizona, Intel foundry, European fabs reduce concentration?

### Missing Evidence
- Quantified compute access distribution (who has how much)
- Specific cases of compute constraints blocking AI development
- Timeline for geographic diversification (TSMC Arizona ramp)

---

## Implications for Compute Concentration Scenario

### What This Grounding Supports
1. **Geographic concentration:** TSMC Taiwan is documented single point of failure
2. **Infrastructure constraints:** Power and cooling limit where compute can be deployed
3. **Access compounding:** Capital requirements and chip allocation create winner-take-more dynamics
4. **Regulatory lag:** Export controls designed for traditional tech face AI-specific concentration

### What Needs More Work
1. **Specific disruption cases:** Documented examples of compute constraints blocking development
2. **Diversification timeline:** When will TSMC Arizona, Intel foundry reduce concentration?
3. **Efficiency trajectory:** Will algorithmic gains outpace concentration?

---

## Comparison to Financial Concentration

| Aspect | Financial (US Asset-Regime) | Compute (AI Infrastructure) |
|--------|----------------------------|----------------------------|
| **Concentration type** | Asset ownership, wealth shares | Compute access, chip allocation |
| **Timescale** | Decades of accumulation | Years of infrastructure buildout |
| **Geographic concentration** | Moderate (global, US-heavy) | High (TSMC Taiwan, specific sites) |
| **Substitution** | Financial assets can shift forms | Hardware-constrained, limited substitution |
| **Regulatory design** | Rules for distributed ownership | Rules for distributed software |
| **Evidence base** | WID data (quantified shares) | Industry reports (less quantified) |

**Assessment:** Compute concentration evidence is **stronger on geographic specificity** but **weaker on quantified distribution** compared to financial concentration.

---

## Recommended Next Steps

1. **Quantify compute distribution** — Who has how much compute (estimated GPU counts by lab/company)
2. **Document constraint cases** — Specific examples of compute blocking AI development
3. **Geographic diversification tracking** — TSMC Arizona, Intel foundry timelines and capacity
4. **Third domain comparison** — Biotech lab capacity or energy storage concentration

---

## Links

- Related scenarios:
  - `research/scenarios/2026-04-02-ai-compute-concentration-stress.md`
  - `research/scenarios/2026-03-28-us-asset-regime-and-wealth-lock-in.md`
- Related syntheses:
  - `research/syntheses/2026-04-02-finance-vs-compute-concentration.md`
- Related components:
  - `mech:compute-access-compounding`
  - `region:tsmc-taiwan`
  - `infra:data-center-compute`
  - `hazard:chip-supply-disruption`
- External sources:
  - TSMC annual reports
  - US export control announcements (BIS)
  - Cloud market share reports (Synergy, Gartner)

---

*This grounding note is a draft. It should be reviewed and either kept, revised, or discarded based on its usefulness for scenario development.*
