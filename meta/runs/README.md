# Run Manifests

This directory holds structured manifests for loop passes created by the CLI.

Each run manifest should record:

- branch
- pass type
- targeted stages
- expected outputs
- created outputs
- completion state

Typical lifecycle:

1. create with `run new`
2. append outputs or notes with `run update`
3. validate with `run check`
4. mark complete with `run complete`

These manifests are part of the method infrastructure layer, not the research corpus itself.
