# Dossier Comparison Capability-Fit Pass

## Metadata

- title: Dossier Comparison Capability-Fit Pass
- date: 2026-03-28
- author: OpenCode
- status: completed
- experiment type: capability-fit
- loop stage(s) tested: 6, 7, 9

## Objective

Test whether local CLI support can prepare the inputs for a comparison-oriented pass by handling branch listing, branch dossier generation, and run listing without meaningful loss of methodological clarity.

## Motivation

The first capability-fit experiment showed that local tooling can absorb branch-state recovery and run scaffolding. The next question is whether it can also package a comparison pass: identify mature branches, surface strongest and weakest variants, and provide enough context for stronger-model judgment to begin at the comparison layer rather than the reconstruction layer.

## Inputs

- research question or context:
  - can branch listing plus dossier generation prepare the next comparison pass more efficiently than manual repo reconstruction?
- materials used:
  - `docs/method-infrastructure.md`
  - `meta/branches/breadbasket.json`
  - `meta/branches/hydrologic.json`
  - `meta/branches/whiplash.json`
  - `meta_autoresearch_cli/cli.py`
  - generated dossier outputs in `meta/generated/`
- user- or researcher-provided documents/resources:
  - none specific to this experiment
- prompts, instructions, or process rules:
  - keep the CLI responsible only for listing, dossier generation, and run-state inspection
  - treat selection and interpretation of the next comparison target as a higher-judgment task
- constraints:
  - no automatic branch selection
  - no auto-generated research conclusions from dossier content alone

## Preliminary literature review

Before running the main experiment, record how the starting evidence base was assembled.

- search scope:
  - internal repo manifests, dossiers, and run history
- online search terms or databases used:
  - none; this was an internal process experiment
- key web sources found:
  - none
- specific documents or resources supplied by the researcher:
  - none
- important exclusions or access limits:
  - the generated dossier files are support artifacts, not canonical research content
- early disagreements, tensions, or gaps in the literature:
  - the tension here is operational: whether packaging comparison inputs locally helps enough to justify maintaining that tooling layer

## Procedure

1. Use `branch list` to view all current branch states in one place.
2. Use `branch dossier` to generate current packets for at least two mature branches.
3. Use `run list` to inspect current recorded pass history.
4. Judge whether the generated packet is sufficient to begin a comparison-oriented pass without manual artifact reconstruction.
5. Record what remains judgment-heavy versus what has now been successfully delegated to local tooling.

If relevant, note where this experiment sits inside `docs/research-loop.md`.

Suggested baseline flow:

1. Define the research question and what the experiment is testing.
2. Run a preliminary online search to map the open evidence landscape.
3. Add any researcher-supplied documents, reports, PDFs, or canonical sources.
4. Compare open-web findings with supplied materials and note important overlap or disagreement.
5. Only then run the main scenario, prompt, workflow, or evaluation experiment.

## Provisional measurement

- evaluation criteria declared before running:
  - branch comparison candidates should be visible in one command
  - generated dossiers should surface enough state to begin a comparison pass
  - run history should be inspectable without raw file navigation
  - the tooling should still stop short of making the comparison judgment itself
- what counts as improvement:
  - lower session overhead before a comparison pass starts
  - clearer visibility into which branch is ready for what kind of next pass
  - easier inspection of whether the repo is overconcentrating on one branch
- what would count as failure or noise:
  - dossiers too thin to be useful
  - run listings that add little beyond folder browsing
  - pressure to let tooling decide the next comparison target automatically

## Outputs produced

- scenarios generated:
  - none directly
- notes or syntheses generated:
  - `research/syntheses/2026-03-28-dossier-comparison-capability-fit-findings.md`
- unexpected artifacts:
  - the current branch manifests are already informative enough that branch listing is useful before any fancy indexing exists

## Results

The local CLI layer now appears sufficient for `comparison prep`, not just basic run scaffolding. `branch list` quickly exposes maturity and next-pass distribution across the repo. `branch dossier` gives enough current-state detail to begin a comparison-oriented pass without re-reading every artifact immediately. `run list` provides a lightweight session history that helps show which branches are receiving recent attention.

The tooling still does not and should not decide what to compare next. But it now shortens the path to that judgment in a meaningful way.

## Interpretation

- what seems useful:
  - branch listing is a good high-level orienting tool
  - dossiers are now useful comparison-prep packets, not just internal summaries
  - run listing begins to make branch attention legible over time
- what seems weak or misleading:
  - dossiers are only as good as the branch manifests that feed them
  - run history is still shallow without richer status or tagging conventions
- what changed in your understanding of the method:
  - comparison prep is a valid local-tooling target because it packages state without pretending to package judgment
  - the method can gain throughput by giving stronger models cleaner entry points into each pass

## Next step

- repeat as-is: yes, for future comparison-oriented passes
- revise and rerun: yes; add stronger branch-check rules and perhaps a run/branch index command later
- discard approach: no
- fold into another workflow: yes; treat dossier generation as the default pre-step for comparison and maturity passes

## Links

- related syntheses:
  - `research/syntheses/2026-03-28-dossier-comparison-capability-fit-findings.md`
  - `research/syntheses/2026-03-28-cli-capability-fit-findings.md`
