# CLI Capability-Fit Pass

## Metadata

- title: CLI Capability-Fit Pass
- date: 2026-03-28
- author: OpenCode
- status: completed
- experiment type: capability-fit
- loop stage(s) tested: 1, 7, 9

## Objective

Test whether branch-state recovery and run scaffolding can be offloaded to the new local CLI layer without meaningful loss of judgment quality.

## Motivation

The project wants gradual scale, not abrupt autonomy. A good first capability-fit test is therefore not scenario generation itself, but the overhead around each pass: recovering branch state, checking hygiene, generating a dossier, scaffolding a run, and tracking completion.

## Inputs

- research question or context:
  - can the local CLI absorb stateful coordination work so stronger model effort stays focused on framing, evidence interpretation, and synthesis?
- materials used:
  - `docs/method-infrastructure.md`
  - `docs/research-loop.md`
  - `meta/branches/whiplash.json`
  - `meta_autoresearch_cli/cli.py`
  - `research/notes/2026-03-28-upper-colorado-whiplash-chronology-note.md`
  - `research/scenarios/2026-03-27-upper-colorado-recovery-to-shortage-whiplash.md`
- user- or researcher-provided documents/resources:
  - none specific to this experiment
- prompts, instructions, or process rules:
  - keep the CLI responsible only for state, scaffolding, validation, and inspection
  - keep judgment-heavy tasks with the stronger model
  - use one real branch pass as the test case
- constraints:
  - no attempt to automate synthesis judgment itself
  - no dependence on external services

## Preliminary literature review

Before running the main experiment, record how the starting evidence base was assembled.

- search scope:
  - internal repo state, current loop documentation, and existing branch artifacts
- online search terms or databases used:
  - none; this was an internal capability-fit pass
- key web sources found:
  - none
- specific documents or resources supplied by the researcher:
  - none
- important exclusions or access limits:
  - no external benchmark dataset; the experiment uses the current repo as its test environment
- early disagreements, tensions, or gaps in the literature:
  - the main tension is practical rather than scholarly: how much coordination overhead can move to local tooling without becoming opaque

## Procedure

1. Use the CLI to recover `whiplash` branch state with `branch status` and `branch dossier`.
2. Start a real grounding pass with `run new`.
3. Complete a real branch improvement by adding chronology/operator evidence to the Upper Colorado whiplash case.
4. Use `run update`, `run check`, and `run complete` to track the pass.
5. Add a `run show` command and validate that run inspection becomes easier than reading raw JSON.
6. Judge which parts of the pass were successfully delegated to local tooling and which still required strong-model judgment.

If relevant, note where this experiment sits inside `docs/research-loop.md`.

Suggested baseline flow:

1. Define the research question and what the experiment is testing.
2. Run a preliminary online search to map the open evidence landscape.
3. Add any researcher-supplied documents, reports, PDFs, or canonical sources.
4. Compare open-web findings with supplied materials and note important overlap or disagreement.
5. Only then run the main scenario, prompt, workflow, or evaluation experiment.

## Provisional measurement

- evaluation criteria declared before running:
  - branch state should be recoverable in one command
  - run expectations should be scaffolded without manual JSON editing
  - run completion should be checkable locally
  - stronger-model effort should still be required for evidence interpretation and maturity judgment
- what counts as improvement:
  - less session time spent reconstructing branch state
  - cleaner pass completion with visible expected outputs
  - easier run inspection after the fact
- what would count as failure or noise:
  - CLI state becomes harder to understand than reading the repo directly
  - the CLI encourages fake completeness without real artifacts
  - the tool starts pretending to make research judgments on its own

## Outputs produced

- scenarios generated:
  - none directly by the CLI; the experiment piggybacked on a real whiplash grounding pass
- notes or syntheses generated:
  - `research/notes/2026-03-28-upper-colorado-whiplash-chronology-note.md`
  - `research/syntheses/2026-03-28-cli-capability-fit-findings.md`
- unexpected artifacts:
  - a `run show` command became clearly necessary once multiple real runs existed

## Results

The CLI successfully absorbed branch-state recovery, dossier generation, run scaffolding, run inspection, and run completion. Those tasks no longer required message-by-message reconstruction. The stronger model still had to perform the hard parts: deciding what evidence mattered, how to interpret relief-versus-constraint chronology, and whether the whiplash branch merited promotion.

This is the desired result. The experiment did not show that the method can be automated. It showed that the method can be made easier to operate.

## Interpretation

- what seems useful:
  - branch manifests and run manifests reduce coordination overhead meaningfully
  - `run show` makes manifest inspection much more usable during active work
  - the CLI helps package a pass into something auditable without reducing methodological visibility
- what seems weak or misleading:
  - the current CLI still depends on manual branch-manifest updates after major judgment calls
  - run manifests can report completion without saying much about quality unless the linked artifacts are actually read
- what changed in your understanding of the method:
  - the first automation layer should stay tightly scoped around coordination and validation
  - modest infrastructure can already increase useful work per pass without threatening the method's epistemic posture

## Next step

- repeat as-is: yes, for future real passes
- revise and rerun: yes; add stronger branch-check rules and maybe a `run index` or `run list` command
- discard approach: no
- fold into another workflow: yes; treat capability-fit as an ongoing thread inside method infrastructure rather than as a one-off experiment

## Links

- related notes:
  - `research/notes/2026-03-28-upper-colorado-whiplash-chronology-note.md`
- related scenarios:
  - `research/scenarios/2026-03-27-upper-colorado-recovery-to-shortage-whiplash.md`
- related syntheses:
  - `research/syntheses/2026-03-28-cli-capability-fit-findings.md`
  - `research/syntheses/2026-03-27-method-lessons-so-far.md`
