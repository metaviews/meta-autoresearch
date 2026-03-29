# Batch Command Usage Guide

**Added:** 2026-03-29  
**Command:** `python -m meta_autoresearch_cli delegate batch <task> <pattern>`

---

## Overview

The `batch` command processes multiple files with a single delegation task, reducing the need to run individual commands for each file.

---

## Usage

### Summarize multiple notes
```bash
# All notes from a specific date
python -m meta_autoresearch_cli delegate batch summarize-note "research/notes/2026-03-28-*.md"

# All grounding notes
python -m meta_autoresearch_cli delegate batch summarize-note "research/notes/*grounding-note.md"

# All notes in a branch (using grep-like pattern)
python -m meta_autoresearch_cli delegate batch summarize-note "research/notes/*whiplash*.md"
```

### Extract claims from multiple scenarios
```bash
# All scenarios from a specific date
python -m meta_autoresearch_cli delegate batch extract-claims "research/scenarios/2026-03-27-*.md"

# All breadbasket scenarios
python -m meta_autoresearch_cli delegate batch extract-claims "research/scenarios/*breadbasket*.md"
```

---

## Output

The batch command provides:
1. **Progress tracking** - Shows `[n/total] Processing <file>...` for each file
2. **Summary statistics** - Reports successful and failed counts
3. **File mapping** - Lists source -> destination for each generated file
4. **Error reporting** - Lists any files that failed with error messages

Example output:
```
Found 7 file(s) matching 'research/notes/2026-03-28-*.md'
Task: summarize-note

[1/7] Processing research/notes/2026-03-28-egypt-wheat-procurement-note.md...
[2/7] Processing research/notes/2026-03-28-india-nbfc-transmission-note.md...
...

============================================================
Batch processing complete
  Successful: 7
  Failed: 0

Generated files:
  research/notes/2026-03-28-egypt-wheat-procurement-note.md -> meta/generated/2026-03-28-egypt-wheat-procurement-note-summary.md
  ...
```

---

## Limitations

### Timeout

The default timeout is 120 seconds (2 minutes). Each delegation task takes ~15-30 seconds depending on file size.

**Rule of thumb:**
- `summarize-note`: ~15-20 seconds per file
- `extract-claims`: ~20-30 seconds per file

**Recommended batch sizes:**
- `summarize-note`: Up to 6-8 files per batch
- `extract-claims`: Up to 4-6 files per batch

For larger batches, split into multiple commands:
```bash
# Instead of one large batch:
python -m meta_autoresearch_cli delegate batch summarize-note "research/notes/*.md"  # May timeout

# Run smaller batches:
python -m meta_autoresearch_cli delegate batch summarize-note "research/notes/2026-03-27-*.md"
python -m meta_autoresearch_cli delegate batch summarize-note "research/notes/2026-03-28-*.md"
```

### No Parallel Processing

Files are processed sequentially, not in parallel. This is intentional:
- Prevents API rate limiting
- Makes progress tracking clearer
- Easier to resume from failures

---

## Best Practices

### 1. Use date-based patterns
```bash
# Good: Specific date ranges
python -m meta_autoresearch_cli delegate batch summarize-note "research/notes/2026-03-28-*.md"

# Risky: All notes (may be too many)
python -m meta_autoresearch_cli delegate batch summarize-note "research/notes/*.md"
```

### 2. Check file count before running
```bash
# First, see what matches
dir research\notes\2026-03-28-*.md

# Then run the batch command
python -m meta_autoresearch_cli delegate batch summarize-note "research/notes/2026-03-28-*.md"
```

### 3. Monitor progress
Watch the `[n/total]` output. If it slows down significantly, the API may be rate-limiting.

### 4. Handle failures gracefully
If some files fail, the command continues processing the rest. Check the "Errors:" section at the end and re-run failed files individually:
```bash
# If a file failed, process it individually
python -m meta_autoresearch_cli delegate summarize-note research/notes/2026-03-28-problem-note.md
```

---

## Cost Estimates

Based on OpenRouter pricing for qwen/qwen3.5-flash-02-23:

| Task | Avg. Tokens | Cost/File | Batch of 5 | Batch of 10 |
|------|-------------|-----------|------------|-------------|
| `summarize-note` | ~3K | $0.0007 | $0.0035 | $0.007 |
| `extract-claims` | ~4K | $0.0009 | $0.0045 | $0.009 |

**Note:** Actual costs vary based on file size and model output length.

---

## Comparison: Individual vs. Batch

### Before (individual commands)
```bash
python -m meta_autoresearch_cli delegate summarize-note research/notes/2026-03-28-note1.md
python -m meta_autoresearch_cli delegate summarize-note research/notes/2026-03-28-note2.md
python -m meta_autoresearch_cli delegate summarize-note research/notes/2026-03-28-note3.md
python -m meta_autoresearch_cli delegate summarize-note research/notes/2026-03-28-note4.md
python -m meta_autoresearch_cli delegate summarize-note research/notes/2026-03-28-note5.md
```

### After (batch command)
```bash
python -m meta_autoresearch_cli delegate batch summarize-note "research/notes/2026-03-28-*.md"
```

**Time saved:** ~5 commands → 1 command  
**Cognitive load:** No need to type each filename

---

## Troubleshooting

### "No files matching pattern"
- Check that the pattern uses forward slashes (`/`) not backslashes (`\`)
- Verify files exist: `dir research\notes\*.md`
- Try a simpler pattern first: `research/notes/*.md`

### Timeout during batch
- Reduce batch size (split into multiple commands)
- Run during off-peak hours (API may be faster)
- Process files individually if only a few

### "Model returned empty response"
- This is usually a temporary API issue
- Re-run the failed file individually
- If persistent, check OpenRouter status

---

## Future Enhancements (Proposed)

1. **`--timeout` flag** - Allow custom timeout per batch
2. **`--parallel` flag** - Process N files in parallel (with rate limiting)
3. **`--resume` flag** - Skip already-generated outputs
4. **`--dry-run` flag** - Show what would be processed without running

---

*Guide generated 2026-03-29. Pricing based on OpenRouter rates as of this date.*
