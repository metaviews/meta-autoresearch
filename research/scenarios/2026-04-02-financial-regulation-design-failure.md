# Financial Regulation Design Failure

## Metadata

- title: Financial Regulation Design Failure
- date: 2026-04-02
- author: OpenCode
- status: draft
- scenario type: non-climate design/rule conflict variant
- domain slice: political economy, financial regulation, banking supervision, shadow banking

## Research question

How might financial regulation designed for stable, slow-moving banking systems create preparedness failures when facing rapid volatility in non-bank financial intermediation, not because regulators are incompetent, but because the rules themselves assume conditions that no longer exist?

## Why this scenario exists

The hydrologic branch has demonstrated design/rule conflict in climate infrastructure (reservoir rules for stationarity face non-stationarity). This variant tests whether the structure travels to non-climate infrastructure: financial regulation.

Financial regulation shares structural features with hydrologic design/rule conflict:
- **Rules designed for stability:** Banking regulation built on assumptions of slow-moving, deposit-funded institutions
- **Reality is volatile:** Non-bank financial intermediation (NBFI) operates with different dynamics (wholesale funding, faster runs, less transparency)
- **Adaptation lag:** Regulatory frameworks adapt slower than financial innovation

## Framing and assumptions

- baseline assumptions:
  - Banking regulation (Basel, Dodd-Frank) designed for traditional deposit-funded banks
  - Non-bank financial intermediation (hedge funds, private credit, money market funds) operates outside traditional framework
  - NBFI now systemically significant (FSB reports very large footprint)
- assumptions that depart from default narratives:
  - the main failure is not regulatory capture or incompetence but structural mismatch
  - rules designed for banks cannot simply be "extended" to NBFI without redesign
  - financial stability depends on regulatory architecture fitting current system, not legacy system
- boundaries of the scenario:
  - this is a design/rule conflict scenario, not a forecast of specific crisis
  - the focus is on regulatory architecture mismatch, not specific policy failures

## Scenario logic

Financial regulation accumulates layers of rules optimized for traditional banking: deposit insurance, capital requirements, liquidity coverage, stress testing. These rules assume slow-moving depositors, transparent balance sheets, and regulatory access to information. The system works adequately when most financial intermediation flows through regulated banks.

But non-bank financial intermediation grows to equal or exceed traditional banking in some segments (private credit, money market funding, hedge fund leverage). NBFI operates with wholesale funding (can run in days, not weeks), less transparency (private markets), and regulatory blind spots (shadow banking). The 2023 Silicon Valley Bank collapse showed how fast runs can occur even in regulated banks when social media and digital banking accelerate deposit flight.

The preparedness failure lies in treating NBFI as "shadow" banking that should be regulated like traditional banks. If NBFI is fundamentally different (wholesale funding, private valuations, complex interconnections), then extending bank rules may fail to address the actual mechanisms. The regulatory architecture itself—the categories, reporting requirements, intervention triggers—assumes a system that no longer dominates.

## Grounding

- FSB reports NBFI footprint is very large and growing (global monitoring reports)
- IMF identifies private credit at $2.1 trillion with borrower stress concerns
- SVB collapse (2023) showed speed of modern bank runs despite regulatory framework
- 2008 crisis showed shadow banking vulnerabilities; post-crisis reforms focused on banks, not NBFI
- BIS research on regulatory arbitrage and balance-sheet buffers delaying but not eliminating stress

These sources support a financial regulation design failure scenario in which regulatory architecture mismatches current financial system structure.

## Signals and evidence classes

- signals already visible:
  - NBFI growth exceeding traditional banking in some segments
  - Regulatory reports flagging NBFI vulnerabilities (FSB, IMF, BIS)
  - SVB run speed exceeding regulatory response capacity
  - Private credit borrower stress (IMF assessments)
- evidence classes consulted:
  - FSB NBFI monitoring reports
  - IMF financial stability reports
  - BIS working papers on regulatory arbitrage
  - Post-mortem analyses of SVB, 2008 crisis
- missing evidence:
  - tighter quantification of NBFI interconnections with regulated banks
  - clearer case material on specific regulatory mismatches (not just "gaps")
  - stronger analysis of whether post-2008 reforms addressed or displaced risk

## Provisional evaluation

- plausibility: high; regulatory mismatch is documented by FSB, IMF, BIS
- internal coherence: high; design/rule conflict mechanism parallels hydrologic structure
- relevance: high; this tests whether design/rule conflict travels to non-climate domain
- preparedness value: high; it points toward regulatory architecture redesign, not just extension
- novelty: high; it reframes financial stability as regulatory fit problem, not just supervision
- status-quo challenge: high; it challenges the assumption that existing frameworks can be "extended" to NBFI
- imaginative power: medium-high; it expands hydrologic branch into financial regulatory architecture

## Curation notes

- current curation gate:
  - keep (tests non-climate portability of design/rule conflict)
- why keep this scenario:
  - it tests whether design/rule conflict structure generalizes beyond climate infrastructure
  - it adds financial regulation as parallel to water infrastructure
  - it enables comparison between climate and financial design/rule conflicts
- what should be refined next:
  - add specific regulatory mismatch cases (NBFI reporting gaps, intervention triggers)
  - compare against hydrologic variants to identify structure similarities
  - clarify whether financial regulation is hybrid or pure design/rule conflict
- what might cause this scenario to be revised or merged:
  - if financial regulation proves fundamentally different (political economy dominates design)
  - if evidence shows regulatory frameworks are adapting fast enough to NBFI growth

## Uncertainties and failure modes

- key uncertainties:
  - how fast NBFI is growing relative to regulatory adaptation
  - whether political economy constraints prevent regulatory redesign
  - how much interconnection exists between NBFI and traditional banks
- where this could be misleading:
  - it could imply regulators are passive when they actively choose enforcement priorities
  - it could understate political economy factors (industry lobbying, regulatory capture)
- what would challenge the scenario most:
  - evidence that NBFI is becoming more regulated, not less
  - evidence that existing frameworks are adequate for current NBFI structure

## Links

- related notes:
  - `research/notes/2026-03-27-seq-hydrologic-whiplash-grounding-note.md`
  - `research/notes/2026-03-27-upper-colorado-hydrologic-design-note.md`
- related experiments:
  - `research/experiments/2026-03-29-whiplash-validation-cycle-report.md`
- related syntheses:
  - `research/syntheses/2026-03-27-hydrologic-branch-comparison.md`
  - `research/syntheses/2026-03-27-emerging-structure-types-comparison.md`
- related scenarios:
  - `research/scenarios/2026-03-27-hydrologic-whiplash-and-design-failure.md`
  - `research/scenarios/2026-03-27-seq-grid-and-wivenhoe-whiplash.md`
  - `research/scenarios/2026-03-27-upper-colorado-compact-and-storage-whiplash.md`

## Components used

- `mech:stationarity-mismatch` — rules built for stability face volatility
- `infra:regulatory-framework` — financial regulatory architecture (new component)
- `inst:fsb-imf-bis` — international financial oversight (new component)
- `hazard:regulatory-arbitrage` — risk migration to less-regulated segments (new component)
