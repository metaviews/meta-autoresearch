# Initial Scenario Evaluation Matrix

## Metadata

- title: Initial Scenario Evaluation Matrix
- date: 2026-03-27
- author: OpenCode
- status: draft
- type: evaluation synthesis

## Purpose

Apply the v1 evaluation framework to the current climate scenario set so the project has an explicit comparison layer rather than only narrative synthesis.

## Scale

- 1 = weak
- 2 = limited
- 3 = moderate
- 4 = strong
- 5 = very strong

## Matrix

| Scenario | Evidence strength | Internal coherence | Relevance | Preparedness value | Novelty / search-space value | Actionability | Status-quo challenge | Imaginative power | Curation | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `research/scenarios/2026-03-27-compound-seasonal-whiplash.md` | 3 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | `revise` | Revised into a more bounded wet-to-hot-dry transition scenario; stronger than before, but it still needs named cases before it should move back to `keep`. |
| `research/scenarios/2026-03-27-synchronous-breadbasket-stress.md` | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | `keep` | Still the strongest family overall; it now has focused wheat variants, a trade-buffer vs production-buffer comparison, and a clearer downstream importer-exposure layer. |
| `research/scenarios/2026-03-27-hydrologic-whiplash-and-design-failure.md` | 4 | 5 | 5 | 5 | 4 | 5 | 5 | 4 | `keep` | Now grounded by a South East Queensland variant; still less mature than breadbasket, but meaningfully stronger and more actionable than the original abstract branch. |

## Notes by scenario

### Compound Seasonal Whiplash

- strongest contribution:
  - highlights sequence blindness and institutional lag rather than single-event thinking
- main weakness:
  - still lacks named case grounding even after narrowing the mechanism
- status-quo challenge:
  - productively challenges the institutional habit of treating hazards as separate seasonal boxes
- imaginative power:
  - expands the inquiry toward sequence logic and transition failure while staying more bounded than the earlier draft
- why `revise` instead of `keep`:
  - it is promising and now better bounded, but should gain named case support before getting equal status with the stronger families
- next step:
  - compare the Feather River and Upper Colorado variants to see whether the family holds across distinct mechanisms

### Synchronous Breadbasket Stress

- strongest contribution:
  - best current link between literature, climate mechanism, trade and policy amplification, and preparedness relevance
- main weakness:
  - the downstream layer is stronger now, but still needs tighter reserve and importer-case comparison beyond the current MENA note set
- status-quo challenge:
  - directly challenges localized, region-by-region food-risk framing by foregrounding correlation and system transmission
- imaginative power:
  - broadens the inquiry meaningfully, though it stays closer to current literature than the seasonal-whiplash scenario
- why `keep`:
  - the family is coherent, evidence-backed, and now mature enough to hold internal sub-branch comparison without collapsing into prediction
- next step:
  - compare how the Russia-Europe and Russia-China wheat variants differ at the importer and reserve level, then decide whether wheat remains the best lead crop

### Hydrologic Whiplash and Design Failure

- strongest contribution:
  - turns non-stationarity into a concrete standards and infrastructure problem
- main weakness:
  - still has only one named case and lacks internal comparison structure
- status-quo challenge:
  - sharply challenges the assumption that legacy design standards remain adequate under shifted distributions
- imaginative power:
  - extends the inquiry beyond hazard talk into rule-curve and standards failure, while staying grounded enough for preparedness work
- why `keep`:
  - the mechanism is strong, now has one grounded case, and is ready for a second-case comparison pass
- next step:
  - compare the South East Queensland case against a second basin or city type to see whether the branch holds across different institutional forms

## Provisional conclusions

- the current set is not redundant; the three scenarios occupy genuinely different mechanism families
- `synchronous breadbasket stress` remains the strongest current candidate and now has the most developed internal structure in the repo
- `hydrologic whiplash and design failure` is now more grounded and should remain active as the next branch to mature after breadbasket
- `compound seasonal whiplash` should stay in play, but under a `revise` gate until it is better grounded

## What this matrix changed

- it forced a distinction between scenario value and evidence strength
- it made status-quo challenge and imaginative range explicit parts of evaluation rather than implicit preferences
- it introduced a real pruning function into the method by downgrading one family from `keep` to `revise`
- it made the next research move more explicit: deepen the strongest family first rather than treating all families as equally ready
- it created a more disciplined path for weaker-but-promising families: narrow, ground, and test named regional variants
- it now gives the whiplash family a first real internal comparison: wet-to-fire versus recovery-to-shortage
- it now gives the breadbasket family a parallel internal comparison: trade-buffer versus production-buffer stress
- it now gives the hydrologic branch its first named-case grounding, making it ready for a true comparison pass rather than remaining only conceptual

## Links

- related framework: `docs/evaluation-framework.md`
- related synthesis: `research/syntheses/2026-03-27-first-scenario-family-synthesis.md`
- related scenarios:
  - `research/scenarios/2026-03-27-compound-seasonal-whiplash.md`
  - `research/scenarios/2026-03-27-feather-river-wet-to-fire-whiplash.md`
  - `research/scenarios/2026-03-27-upper-colorado-recovery-to-shortage-whiplash.md`
  - `research/scenarios/2026-03-27-synchronous-breadbasket-stress.md`
  - `research/scenarios/2026-03-27-northern-wheat-correlation-shock.md`
  - `research/scenarios/2026-03-27-russia-europe-wheat-trade-shock.md`
  - `research/scenarios/2026-03-27-russia-china-wheat-buffer-stress.md`
  - `research/scenarios/2026-03-27-hydrologic-whiplash-and-design-failure.md`
  - `research/scenarios/2026-03-27-seq-grid-and-wivenhoe-whiplash.md`
