# Generated Output

This directory holds generated support artifacts from the CLI layer.

## Contents

- **Dossiers** - `*-dossier.md` - Full branch state summaries
- **Snapshots** - `*-snapshot.md` - Compact branch state packets
- **Artifact Indexes** - `*-artifact-index.md` - File listings with modification times
- **Comparison Prep** - `*-comparison-prep.md` - Variant tables and evaluation dimensions
- **Run Packets** - `*-packet.md`, `*-packet.json` - Run-specific prep materials
- **Summaries** - `*-summary.md` - Model-generated note summaries (Iteration 3)
- **Claims** - `*-claims.md` - Model-generated claim extractions (Iteration 3)

## Usage Rules

1. These files are **draft support artifacts**, not canonical research
2. All files include HTML comments marking task type, model, source, and timestamp
3. Files are git-ignored by default (except this README)
4. Regenerate stale files using `branch stale` to detect outdated output

## Regenerating

```bash
# Check for stale files
python -m meta_autoresearch_cli branch stale

# Regenerate specific artifacts
python -m meta_autoresearch_cli branch snapshot <slug>
python -m meta_autoresearch_cli branch index <slug>
python -m meta_autoresearch_cli branch compare-prep <slug>
python -m meta_autoresearch_cli run packet <run-id>
```
