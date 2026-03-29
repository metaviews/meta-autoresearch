# Method State

This directory holds structured state for the method infrastructure layer.

## Structure

- `meta/branches/` - JSON branch manifests (maturity, variants, syntheses, etc.)
- `meta/runs/` - JSON run manifests (pass type, expected outputs, completion status)
- `meta/generated/` - Generated support artifacts (dossiers, snapshots, summaries, claims)

## Usage

### View Branch State
```bash
python -m meta_autoresearch_cli branch list
python -m meta_autoresearch_cli branch status <slug>
python -m meta_autoresearch_cli branch check <slug>
```

### View Run State
```bash
python -m meta_autoresearch_cli run list
python -m meta_autoresearch_cli run show <run-id>
```

### Generate Support Artifacts
```bash
python -m meta_autoresearch_cli branch snapshot <slug>
python -m meta_autoresearch_cli branch index <slug>
python -m meta_autoresearch_cli run packet <run-id>
```

### Check for Stale Generated Files
```bash
python -m meta_autoresearch_cli branch stale
```

Research artifacts remain in `research/`. The `meta/` directory exists to reduce coordination overhead and make branch and run state recoverable across sessions.
