# Component Index

**Purpose:** Structured, reusable components extracted from research artifacts.

**Component types:**
- `region` — Named geography or planning area
- `mechanism` — Causal logic or failure pattern
- `institution` — Organization, agency, or governance body
- `infrastructure` — Physical or operational system
- `evidence` — Source class or documented signal
- `hazard` — Risk type or stress condition

---

## Components by Type

### Regions

| ID | Name | Domain | Related Branches |
|----|------|--------|------------------|
| `region:feather-river` | Feather River corridor | climate volatility | whiplash |
| `region:upper-colorado` | Upper Colorado Basin | climate volatility | whiplash, hydrologic |
| `region:russia` | Russia (wheat export node) | climate volatility | breadbasket |
| `region:europe` | European wheat belt | climate volatility | breadbasket |
| `region:china` | China (wheat buffer) | climate volatility | breadbasket |
| `region:egypt` | Egypt (wheat importer) | climate volatility | breadbasket |
| `region:yemen` | Yemen (wheat importer) | climate volatility | breadbasket |
| `region:seq` | Southeast Queensland | climate volatility | hydrologic |
| `region:us` | United States | political economy | wealth-concentration |
| `region:india` | India | political economy | wealth-concentration |

---

### Mechanisms

| ID | Name | Structure Type | Description |
|----|------|----------------|-------------|
| `mech:wet-to-fire` | Wet-to-fire transition | sequence failure | Wet period creates vegetation growth, then hot-dry creates fire risk |
| `mech:recovery-to-shortage` | Apparent recovery masking shortage | sequence failure | Recovery phase creates false sense of security before shortage |
| `mech:export-restriction-amplification` | Export restriction amplifies physical stress | correlation/transmission | Export node stress amplified by policy response |
| `mech:dual-node-correlation` | Two substitute buffers fail together | correlation/transmission | Correlated stress on primary and substitute nodes |
| `mech:stationarity-mismatch` | Rules built for stationarity face non-stationarity | design/rule conflict | Infrastructure rules fail under changed conditions |
| `mech:transmission-squeeze` | Credit/reserve transmission under stress | correlation/transmission | Financial transmission channels fail under stress |
| `mech:asset-regime-lock-in` | Asset rules concentrate wealth | hybrid | Asset regime design concentrates wealth under volatility |

---

### Institutions

| ID | Name | Domain | Related Branches |
|----|------|--------|------------------|
| `inst:cal-fire` | CAL FIRE | climate volatility | whiplash |
| `inst:eu-commission` | European Commission (agriculture) | climate volatility | breadbasket |
| `inst:usda-ers` | USDA Economic Research Service | climate volatility | breadbasket |
| `inst:seq-water-grid` | SEQ Water Grid | climate volatility | hydrologic |
| `inst:federal-reserve` | Federal Reserve | political economy | wealth-concentration |
| `inst:nbfc` | Non-Banking Financial Companies (India) | political economy | wealth-concentration |

---

### Infrastructure

| ID | Name | Type | Related Branches |
|----|------|------|------------------|
| `infra:wivenhoe-dam` | Wivenhoe Dam | reservoir | hydrologic |
| `infra:feather-river-canyon` | Feather River Canyon | transmission corridor | whiplash |
| `infra:black-sea-export` | Black Sea export infrastructure | trade node | breadbasket |
| `infra:private-credit` | Private credit markets | financial | wealth-concentration |

---

### Evidence Classes

| ID | Name | Type | Related Branches |
|----|------|------|------------------|
| `evidence:california-water-watch` | California Water Watch | state monitoring | whiplash |
| `evidence:cal-fire-incident` | CAL FIRE incident records | state records | whiplash |
| `evidence:ipcc-assessment` | IPCC assessments | international assessment | whiplash, breadbasket |
| `evidence:heino-2023` | Heino et al. (2023) climate-yield study | peer-reviewed paper | breadbasket |
| `evidence:usda-wheat-trade` | USDA wheat trade analysis | government report | breadbasket |

---

### Hazards

| ID | Name | Domain | Related Branches |
|----|------|--------|------------------|
| `hazard:wildfire` | Wildfire | climate volatility | whiplash |
| `hazard:drought` | Drought | climate volatility | whiplash, hydrologic |
| `hazard:flood` | Flooding | climate volatility | whiplash, hydrologic |
| `hazard:wheat-shortfall` | Wheat production shortfall | climate volatility | breadbasket |
| `hazard:price-spike` | Price formation shock | climate volatility | breadbasket |
| `hazard:credit-squeeze` | Credit availability squeeze | political economy | wealth-concentration |

---

## Usage

Components are used to:
1. **Generate scenarios** — Combine region + mechanism + evidence
2. **Compare branches** — Find shared components across domains
3. **Search patterns** — "Show all sequence failure mechanisms"
4. **Identify gaps** — "What regions have no components yet?"

**CLI commands:**
```bash
# Build component index from YAML files
python -m meta_autoresearch_cli component index

# Search for components
python -m meta_autoresearch_cli component search <query>

# List components by type
python -m meta_autoresearch_cli component list --type <type>

# Suggest components for a new branch
python -m meta_autoresearch_cli component suggest <branch-slug>
```

---

*This index is auto-generated from `meta/components/*.yaml` files. Edit individual YAML files, not this index.*
