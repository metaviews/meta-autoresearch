# Research Workspace

This directory holds the working corpus for v1.

## Structure

- `research/notes/` - source synthesis, open questions, and partial interpretations
- `research/scenarios/` - structured scenario drafts and recombinations
- `research/experiments/` - tests of workflow, prompts, evaluation, and curation
- `research/discards/` - explicit records of failed, merged, or pruned directions
- `research/loops/` - auditable records of one full research cycle
- `research/syntheses/` - higher-order comparisons across scenarios, notes, and experiments

Use `docs/evaluation-framework.md` when you need to compare scenarios explicitly or make keep/revise/merge/discard decisions.

Use `docs/research-loop.md` as the current reference for how notes, scenarios, experiments, and syntheses fit together inside one repeatable cycle.

## Naming convention

Use date-first, lowercase, kebab-case filenames so the corpus stays sortable and easy to scan.

- notes: `YYYY-MM-DD-topic.md`
- scenarios: `YYYY-MM-DD-topic.md`
- experiments: `YYYY-MM-DD-topic.md`
- discards: `YYYY-MM-DD-topic.md`
- loops: `YYYY-MM-DD-topic.md`
- syntheses: `YYYY-MM-DD-topic.md`

If more than one file shares the same topic on the same day, add a short suffix such as `-v2` or `-compare`.

Examples:

- `2026-03-27-climate-baselines-note.md`
- `2026-03-27-compound-seasonal-whiplash.md`
- `2026-03-27-climate-scenario-generation-pass.md`

## Working rule

Keep the filename stable and use the document metadata to track status changes. That preserves links and keeps iteration legible.

## Research inputs

Experiments and notes can draw from both:

- open-web and library searches
- researcher-provided documents, reports, PDFs, and canonical source files

Treat both as legitimate inputs, but record which materials came from which channel so the research trail stays clear.
