from __future__ import annotations

import argparse
import json
import os
import urllib.request
import urllib.error
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

# Load .env file if present (for local development)
_env_path = Path(__file__).parent.parent / ".env"
if _env_path.exists():
    with open(_env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


PASS_TYPES: dict[str, dict[str, Any]] = {
    "grounding": {
        "stages": [2, 4],
        "expected_outputs": [
            {"kind": "grounding_note", "description": "At least one new or updated grounding note"},
            {"kind": "scenario_update", "description": "At least one grounded scenario update or named case variant"},
        ],
    },
    "variant": {
        "stages": [5],
        "expected_outputs": [
            {"kind": "scenario_variant", "description": "At least one new branch variant or case"}
        ],
    },
    "comparison": {
        "stages": [6],
        "expected_outputs": [
            {"kind": "comparison_synthesis", "description": "At least one synthesis comparing variants or nodes"}
        ],
    },
    "maturity": {
        "stages": [7, 8, 9],
        "expected_outputs": [
            {"kind": "maturity_update", "description": "A branch maturity or structure judgment update"},
            {"kind": "loop_update", "description": "A loop-run update or maturity assessment"},
        ],
    },
    "discard": {
        "stages": [7],
        "expected_outputs": [
            {"kind": "discard_record", "description": "At least one discard or merge record"}
        ],
    },
    "capability-fit": {
        "stages": [9],
        "expected_outputs": [
            {"kind": "experiment", "description": "A capability-fit experiment artifact"},
            {"kind": "synthesis", "description": "A short synthesis on quality, delegation, or loss"},
        ],
    },
}


def get_model_config() -> dict[str, str]:
    """Get provider-agnostic model configuration from environment."""
    return {
        "backend": os.environ.get("META_MODEL_BACKEND", "openrouter"),
        "small": os.environ.get("META_MODEL_DEFAULT_SMALL", ""),
        "mid": os.environ.get("META_MODEL_DEFAULT_MID", ""),
        "strong": os.environ.get("META_MODEL_DEFAULT_STRONG", ""),
        "openrouter_api_key": os.environ.get("OPENROUTER_API_KEY", ""),
        "openrouter_base_url": os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        "openrouter_http_referer": os.environ.get("OPENROUTER_HTTP_REFERER", ""),
        "openrouter_app_name": os.environ.get("OPENROUTER_APP_NAME", "meta-autoresearch"),
    }


@dataclass
class RepoPaths:
    root: Path
    meta: Path
    branches: Path
    runs: Path
    generated: Path


def discover_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "docs" / "research-loop.md").exists() and (candidate / "research").is_dir():
            return candidate
    raise SystemExit("Could not find repository root from current working directory")


def repo_paths() -> RepoPaths:
    root = discover_repo_root()
    meta = root / "meta"
    return RepoPaths(
        root=root,
        meta=meta,
        branches=meta / "branches",
        runs=meta / "runs",
        generated=meta / "generated",
    )


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def relpath(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def branch_manifest_path(slug: str) -> Path:
    return repo_paths().branches / f"{slug}.json"


def run_manifest_path(run_id: str) -> Path:
    return repo_paths().runs / f"{run_id}.json"


def load_branch(slug: str) -> tuple[dict[str, Any], Path, RepoPaths]:
    paths = repo_paths()
    path = branch_manifest_path(slug)
    if not path.exists():
        raise SystemExit(f"Unknown branch '{slug}'. Expected manifest at {relpath(paths.root, path)}")
    return load_json(path), path, paths


def print_kv(key: str, value: Any) -> None:
    print(f"{key}: {value}")


def check_file_exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def branch_warnings(branch: dict[str, Any], paths: RepoPaths) -> list[str]:
    warnings: list[str] = []
    maturity = int(branch.get("maturity_level", 0))
    parent = branch.get("parent_artifact")
    if not parent or not check_file_exists(paths.root, parent):
        warnings.append("Missing or invalid parent_artifact")
    if not branch.get("structure_type"):
        warnings.append("Missing structure_type")
    if not branch.get("active_variants"):
        warnings.append("No active_variants recorded")
    if maturity >= 3 and len(branch.get("active_variants", [])) < 2:
        warnings.append("Comparative branch should have at least two active variants")
    if maturity >= 3 and not branch.get("loop_runs"):
        warnings.append("Level 3+ branch should have at least one loop run")
    if maturity >= 4 and not branch.get("discard_records"):
        warnings.append("Level 4 branch should show at least one discard record")
    if maturity >= 4 and not branch.get("key_syntheses"):
        warnings.append("Level 4 branch should have key_syntheses recorded")
    if maturity >= 4 and not branch.get("next_recommended_pass"):
        warnings.append("Level 4 branch should have next_recommended_pass set")
    for field in ["active_variants", "key_notes", "key_syntheses", "loop_runs", "discard_records"]:
        for rel in branch.get(field, []):
            if not check_file_exists(paths.root, rel):
                warnings.append(f"Referenced file missing: {rel}")
    strongest = branch.get("strongest_variant")
    if strongest and strongest not in branch.get("active_variants", []):
        warnings.append("strongest_variant is not listed in active_variants")
    weakest = branch.get("weakest_variant")
    if weakest and weakest != branch.get("parent_artifact") and weakest not in branch.get("active_variants", []):
        warnings.append("weakest_variant is neither the parent artifact nor an active variant")
    if maturity >= 4:
        for field in ["strongest_variant", "most_generative_variant", "weakest_variant"]:
            if not branch.get(field):
                warnings.append(f"Level 4 branch missing {field}")
    return warnings


def branch_manifests(paths: RepoPaths) -> list[tuple[dict[str, Any], Path]]:
    manifests: list[tuple[dict[str, Any], Path]] = []
    for path in sorted(paths.branches.glob("*.json")):
        manifests.append((load_json(path), path))
    return manifests


# =============================================================================
# Iteration 2: Context Compression
# =============================================================================


def get_file_mtime(path: Path) -> datetime | None:
    """Get file modification time, or None if file doesn't exist."""
    if path.exists():
        return datetime.fromtimestamp(path.stat().st_mtime)
    return None


def check_stale_generated(paths: RepoPaths, branch_slug: str) -> list[tuple[str, str, str]]:
    """
    Check if generated files are stale relative to their source manifests.
    
    Returns list of (generated_file, source_file, reason) tuples for stale files.
    """
    stale: list[tuple[str, str, str]] = []
    branch_path = paths.branches / f"{branch_slug}.json"
    
    if not branch_path.exists():
        return stale
    
    branch_mtime = get_file_mtime(branch_path)
    if not branch_mtime:
        return stale
    
    # Check branch dossier
    dossier_path = paths.generated / f"{branch_slug}-dossier.md"
    dossier_mtime = get_file_mtime(dossier_path)
    if dossier_mtime and dossier_mtime < branch_mtime:
        stale.append((
            relpath(paths.root, dossier_path),
            relpath(paths.root, branch_path),
            "dossier older than branch manifest"
        ))
    
    # Check branch snapshot
    snapshot_path = paths.generated / f"{branch_slug}-snapshot.md"
    snapshot_mtime = get_file_mtime(snapshot_path)
    if snapshot_mtime and snapshot_mtime < branch_mtime:
        stale.append((
            relpath(paths.root, snapshot_path),
            relpath(paths.root, branch_path),
            "snapshot older than branch manifest"
        ))
    
    # Check run packets for this branch
    for run_path in paths.runs.glob("*.json"):
        run_data = load_json(run_path)
        if run_data.get("branch_slug") != branch_slug:
            continue
        
        run_id = run_data.get("run_id", "")
        packet_md = paths.generated / f"{run_id}-packet.md"
        packet_json = paths.generated / f"{run_id}-packet.json"
        run_mtime = get_file_mtime(run_path)
        
        if not run_mtime:
            continue
        
        for packet_path in [packet_md, packet_json]:
            packet_mtime = get_file_mtime(packet_path)
            if packet_mtime and packet_mtime < run_mtime:
                stale.append((
                    relpath(paths.root, packet_path),
                    relpath(paths.root, run_path),
                    f"packet older than run manifest ({run_id})"
                ))
    
    # Check if artifacts referenced in branch have been modified after generated files
    branch_data = load_json(branch_path)
    for artifact_list in ["key_notes", "key_syntheses", "loop_runs", "discard_records", "active_variants"]:
        for artifact_rel in branch_data.get(artifact_list, []):
            artifact_path = paths.root / artifact_rel
            artifact_mtime = get_file_mtime(artifact_path)
            if not artifact_mtime:
                continue
            
            # Check against snapshot
            if snapshot_mtime and artifact_mtime > snapshot_mtime:
                stale.append((
                    relpath(paths.root, snapshot_path),
                    relpath(paths.root, artifact_path),
                    f"snapshot older than {artifact_list} artifact"
                ))
                break  # One warning per generated file is enough
    
    return stale


def command_branch_stale(args: argparse.Namespace) -> int:
    """Check for stale generated files."""
    paths = repo_paths()
    
    if args.slug:
        # Check specific branch
        branch_slugs = [args.slug]
    else:
        # Check all branches
        branch_slugs = [p.stem for p in paths.branches.glob("*.json")]
    
    all_stale: list[tuple[str, str, str, str]] = []  # (branch, generated, source, reason)
    
    for slug in branch_slugs:
        stale = check_stale_generated(paths, slug)
        for gen, src, reason in stale:
            all_stale.append((slug, gen, src, reason))
    
    if all_stale:
        print("Stale generated files detected:")
        for branch, gen, src, reason in all_stale:
            print(f"\n  Branch: {branch}")
            print(f"  Generated: {gen}")
            print(f"  Source: {src}")
            print(f"  Reason: {reason}")
        return 1
    else:
        print("No stale generated files detected.")
        return 0


def collect_branch_artifacts(branch: dict[str, Any], paths: RepoPaths) -> dict[str, list[dict[str, Any]]]:
    """
    Collect artifact metadata for a branch in a compact format.
    
    Returns dict with categorized artifact info including path, mtime, and summary.
    """
    artifacts: dict[str, list[dict[str, Any]]] = {
        "notes": [],
        "scenarios": [],
        "syntheses": [],
        "loop_runs": [],
        "discards": [],
    }
    
    def artifact_info(rel_path: str) -> dict[str, Any]:
        path = paths.root / rel_path
        mtime = get_file_mtime(path)
        return {
            "path": rel_path,
            "modified": mtime.isoformat() if mtime else None,
            "exists": path.exists(),
        }
    
    for rel in branch.get("key_notes", []):
        artifacts["notes"].append(artifact_info(rel))
    
    for rel in branch.get("active_variants", []):
        artifacts["scenarios"].append(artifact_info(rel))
    
    parent = branch.get("parent_artifact")
    if parent:
        artifacts["scenarios"].insert(0, {**artifact_info(parent), "parent": True})
    
    for rel in branch.get("key_syntheses", []):
        artifacts["syntheses"].append(artifact_info(rel))
    
    for rel in branch.get("loop_runs", []):
        artifacts["loop_runs"].append(artifact_info(rel))
    
    for rel in branch.get("discard_records", []):
        artifacts["discards"].append(artifact_info(rel))
    
    return artifacts


def artifact_index_markdown(branch: dict[str, Any], paths: RepoPaths) -> str:
    """Generate a compact artifact index in markdown format."""
    artifacts = collect_branch_artifacts(branch, paths)
    
    lines = [
        f"# Artifact Index: {branch['title']}",
        "",
        f"**slug:** `{branch['slug']}`",
        f"**generated:** {datetime.now().isoformat()}",
        "",
    ]
    
    for category, items in artifacts.items():
        if not items:
            continue
        
        lines.append(f"## {category.title()}")
        lines.append("")
        lines.append("| Path | Modified | Status |")
        lines.append("|------|----------|--------|")
        
        for item in items:
            status = "✓" if item["exists"] else "✗ missing"
            if item.get("parent"):
                status += " (parent)"
            modified = item["modified"][:10] if item["modified"] else "N/A"
            lines.append(f"| `{item['path']}` | {modified} | {status} |")
        
        lines.append("")
    
    # Summary
    total = sum(len(items) for items in artifacts.values())
    missing = sum(1 for items in artifacts.values() for item in items if not item["exists"])
    
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total artifacts:** {total}")
    lines.append(f"- **Missing files:** {missing}")
    lines.append(f"- **Branch maturity:** {branch.get('maturity_level', 'N/A')}")
    lines.append(f"- **Structure type:** `{branch.get('structure_type', 'N/A')}`")
    lines.append("")
    
    return "\n".join(lines)


def command_branch_index(args: argparse.Namespace) -> int:
    """Generate artifact index for a branch."""
    branch, _, paths = load_branch(args.slug)
    index_md = artifact_index_markdown(branch, paths)
    
    out = paths.generated / f"{branch['slug']}-artifact-index.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(index_md, encoding="utf-8", newline="\n")
    
    print(f"generated: {relpath(paths.root, out)}")
    return 0


def comparison_prep_markdown(branch: dict[str, Any], paths: RepoPaths) -> str:
    """
    Generate comparison prep material from branch state.
    
    Creates a compact summary of variants, key differences, and comparison dimensions.
    """
    lines = [
        f"# Comparison Prep: {branch['title']}",
        "",
        f"**slug:** `{branch['slug']}`",
        f"**structure type:** `{branch.get('structure_type', 'N/A')}`",
        f"**maturity:** {branch.get('maturity_level', 'N/A')} ({branch.get('maturity_note', '')})",
        "",
    ]
    
    # Variant summary table
    variants = branch.get("active_variants", [])
    parent = branch.get("parent_artifact")
    
    if parent:
        variants_with_parent = [parent] + variants
    else:
        variants_with_parent = variants
    
    lines.append("## Variants Overview")
    lines.append("")
    
    if variants_with_parent:
        lines.append("| Variant | Role | Status |")
        lines.append("|---------|------|--------|")
        
        strongest = branch.get("strongest_variant", "")
        most_generative = branch.get("most_generative_variant", "")
        weakest = branch.get("weakest_variant", "")
        
        for v in variants_with_parent:
            roles = []
            if v == parent:
                roles.append("parent")
            if v == strongest:
                roles.append("strongest")
            if v == most_generative:
                roles.append("most_generative")
            if v == weakest:
                roles.append("weakest")
            
            role_str = ", ".join(roles) if roles else "variant"
            exists = "✓" if check_file_exists(paths.root, v) else "✗ missing"
            short_path = v.split("/")[-1] if "/" in v else v
            lines.append(f"| `{short_path}` | {role_str} | {exists} |")
        
        lines.append("")
    
    # Key comparison dimensions from evaluation framework
    lines.append("## Comparison Dimensions")
    lines.append("")
    lines.append("Use these dimensions when comparing variants:")
    lines.append("")
    lines.append("1. **Evidence strength** - How well sources support claims")
    lines.append("2. **Internal coherence** - Causal structure clarity")
    lines.append("3. **Relevance** - Match to research question")
    lines.append("4. **Preparedness value** - Decision-usefulness")
    lines.append("5. **Novelty** - Expands search space vs restates familiar")
    lines.append("6. **Actionability** - Clear next research step")
    lines.append("7. **Status-quo challenge** - Questions dominant assumptions")
    lines.append("8. **Imaginative power** - Expands plausible range")
    lines.append("")
    
    # Open questions to guide comparison
    open_questions = branch.get("open_questions", [])
    if open_questions:
        lines.append("## Guiding Questions")
        lines.append("")
        for i, q in enumerate(open_questions[:5], 1):
            lines.append(f"{i}. {q}")
        lines.append("")
    
    # Previous syntheses
    key_syntheses = branch.get("key_syntheses", [])
    if key_syntheses:
        lines.append("## Previous Comparisons")
        lines.append("")
        for syn in key_syntheses[-3:]:
            lines.append(f"- `{syn.split('/')[-1]}`")
        lines.append("")
    
    # Recommended comparison approach
    lines.append("## Recommended Approach")
    lines.append("")
    if len(variants_with_parent) >= 2:
        lines.append(f"- Compare {len(variants_with_parent)} variants across 8 dimensions")
        lines.append("- Identify which variant is strongest vs most generative")
        lines.append("- Note where variants diverge in mechanism vs wording")
        lines.append("- Record curation decision: keep/revise/merge/discard per variant")
    else:
        lines.append("- Need more variants before meaningful comparison")
        lines.append("- Consider generating additional variants via `run new --type variant`")
    lines.append("")
    
    # Next step
    lines.append("## Next Step")
    lines.append("")
    lines.append(f"**Recommended pass:** `{branch.get('next_recommended_pass', 'N/A')}`")
    lines.append("")
    
    return "\n".join(lines)


def command_branch_compare_prep(args: argparse.Namespace) -> int:
    """Generate comparison prep material for a branch."""
    branch, _, paths = load_branch(args.slug)
    prep_md = comparison_prep_markdown(branch, paths)
    
    out = paths.generated / f"{branch['slug']}-comparison-prep.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(prep_md, encoding="utf-8", newline="\n")
    
    print(f"generated: {relpath(paths.root, out)}")
    return 0


# =============================================================================
# Iteration 3: Bounded Model Delegation
# =============================================================================


def call_openrouter(messages: list[dict[str, str]], model: str, config: dict[str, str]) -> str:
    """
    Call OpenRouter API with the given messages and model.
    
    Returns the response content or raises SystemExit on error.
    """
    api_key = config.get("openrouter_api_key", "")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY not set. Add it to .env file.")
    
    base_url = config.get("openrouter_base_url", "https://openrouter.ai/api/v1")
    http_referer = config.get("openrouter_http_referer", "")
    app_name = config.get("openrouter_app_name", "meta-autoresearch")
    
    url = f"{base_url}/chat/completions"
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 2000,
    }
    
    data = json.dumps(payload).encode("utf-8")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": http_referer,
        "X-Title": app_name,
    }
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            choices = result.get("choices", [])
            if choices:
                message = choices[0].get("message", {})
                return message.get("content", "")
            return ""
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise SystemExit(f"OpenRouter API error ({e.code}): {error_body}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Failed to reach OpenRouter API: {e.reason}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"Failed to parse API response: {e}")


def get_model_for_slot(slot: str) -> tuple[str, dict[str, str]]:
    """
    Get model ID and config for the given slot (small, mid, strong).
    
    Returns (model_id, config) tuple.
    """
    config = get_model_config()
    
    slot_map = {
        "small": config.get("small", ""),
        "mid": config.get("mid", ""),
        "strong": config.get("strong", ""),
    }
    
    model_id = slot_map.get(slot, "")
    if not model_id:
        raise SystemExit(f"Model slot '{slot}' not configured. Set META_MODEL_DEFAULT_{slot.upper()} in .env")
    
    return model_id, config


def summarize_note_task(content: str, file_path: str) -> str:
    """
    Create the system and user prompt for note summarization.
    
    Returns the formatted prompt for the model.
    """
    system_prompt = """You are assisting with meta-autoresearch, a method for exploring complex questions without premature closure.

Your task is to summarize a research note. Follow these guidelines:

1. **Extract key claims** - List the main assertions or observations (bullet points)
2. **Identify evidence** - Note what sources, cases, or data are referenced
3. **Surface uncertainties** - Flag what remains unclear or speculative
4. **Note connections** - Identify links to scenarios, branches, or other artifacts
5. **Preserve nuance** - Do not collapse uncertainty into false precision

Keep the summary concise (200-400 words). Use markdown formatting.

This is a support task. Your output will be reviewed by a human curator."""

    user_prompt = f"""Summarize this research note:

File: {file_path}

---
{content}
---

Provide your summary in this format:

## Key Claims
- ...

## Evidence Referenced
- ...

## Uncertainties
- ...

## Connections
- ...
"""
    
    return system_prompt, user_prompt


def command_delegate_summarize(args: argparse.Namespace) -> int:
    """
    Summarize a research note using a cheaper model.
    
    Output goes to meta/generated/ and is marked as draft.
    """
    paths = repo_paths()
    
    # Read input file
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = paths.root / args.input
    
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")
    
    content = input_path.read_text(encoding="utf-8")
    
    # Get model for small tasks
    model_id, config = get_model_for_slot("small")
    
    # Create prompts
    rel_path = relpath(paths.root, input_path)
    system_prompt, user_prompt = summarize_note_task(content, rel_path)
    
    # Call model
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    
    print(f"Calling {model_id} for summarization...")
    summary = call_openrouter(messages, model_id, config)
    
    if not summary:
        raise SystemExit("Model returned empty response")
    
    # Generate output filename
    stem = input_path.stem
    output_filename = f"{stem}-summary.md"
    output_path = paths.generated / output_filename
    
    # Write output with metadata header
    output_content = f"""<!-- GENERATED: do not treat as canonical research -->
<!-- Task: summarize-note -->
<!-- Model: {model_id} -->
<!-- Source: {rel_path} -->
<!-- Generated: {datetime.now().isoformat()} -->

# Summary: {input_path.name}

{summary}

---
*This is a generated support artifact. Treat as draft until reviewed.*
"""
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output_content, encoding="utf-8", newline="\n")
    
    print(f"generated: {relpath(paths.root, output_path)}")
    print(f"model: {model_id}")
    return 0


def command_delegate_extract_claims(args: argparse.Namespace) -> int:
    """
    Extract claims from a research artifact using a cheaper model.
    
    Output goes to meta/generated/ and is marked as draft.
    """
    paths = repo_paths()
    
    # Read input file
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = paths.root / args.input
    
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")
    
    content = input_path.read_text(encoding="utf-8")
    
    # Get model for small tasks
    model_id, config = get_model_for_slot("small")
    
    # Create prompts
    rel_path = relpath(paths.root, input_path)
    
    system_prompt = """You are extracting claims from research artifacts for meta-autoresearch.

Your task: identify distinct, testable claims in the text.

Guidelines:
1. One claim per bullet point
2. Preserve uncertainty qualifiers ("may", "suggests", "likely")
3. Distinguish between evidence-backed claims and speculation
4. Note when claims reference specific sources or cases

This is a support task. Output will be reviewed by human curator."""

    user_prompt = f"""Extract all claims from this artifact:

File: {rel_path}

---
{content}
---

Format each claim as:
- [Claim text] (evidence-backed | speculative) - [source if referenced]
"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    print(f"Calling {model_id} for claim extraction...")
    result = call_openrouter(messages, model_id, config)

    if not result:
        raise SystemExit("Model returned empty response for claim extraction")
    
    # Generate output filename
    stem = input_path.stem
    output_filename = f"{stem}-claims.md"
    output_path = paths.generated / output_filename
    
    output_content = f"""<!-- GENERATED: do not treat as canonical research -->
<!-- Task: extract-claims -->
<!-- Model: {model_id} -->
<!-- Source: {rel_path} -->
<!-- Generated: {datetime.now().isoformat()} -->

# Claims Extracted: {input_path.name}

{result}

---
*This is a generated support artifact. Treat as draft until reviewed.*
"""
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output_content, encoding="utf-8", newline="\n")
    
    print(f"generated: {relpath(paths.root, output_path)}")
    print(f"model: {model_id}")
    return 0


def command_branch_status(args: argparse.Namespace) -> int:
    branch, _, _ = load_branch(args.slug)
    print_kv("branch", branch["title"])
    print_kv("slug", branch["slug"])
    print_kv("structure_type", branch.get("structure_type", ""))
    print_kv("maturity_level", branch.get("maturity_level", ""))
    print_kv("maturity_note", branch.get("maturity_note", ""))
    print_kv("status", branch.get("status", ""))
    print_kv("next_recommended_pass", branch.get("next_recommended_pass", ""))
    print_kv("strongest_variant", branch.get("strongest_variant", ""))
    print_kv("most_generative_variant", branch.get("most_generative_variant", ""))
    print_kv("weakest_variant", branch.get("weakest_variant", ""))
    print("open_questions:")
    for item in branch.get("open_questions", []):
        print(f"- {item}")
    return 0


def command_branch_check(args: argparse.Namespace) -> int:
    branch, _, paths = load_branch(args.slug)
    warnings = branch_warnings(branch, paths)
    if warnings:
        print(f"Branch '{branch['slug']}' check: warnings")
        for item in warnings:
            print(f"- {item}")
        return 1
    print(f"Branch '{branch['slug']}' check: ok")
    return 0


def dossier_markdown(branch: dict[str, Any], warnings: list[str]) -> str:
    lines = [
        f"# {branch['title']} Dossier",
        "",
        f"- slug: `{branch['slug']}`",
        f"- structure type: `{branch.get('structure_type', '')}`",
        f"- maturity: `{branch.get('maturity_level', '')}` ({branch.get('maturity_note', '')})",
        f"- status: `{branch.get('status', '')}`",
        f"- next recommended pass: `{branch.get('next_recommended_pass', '')}`",
        "",
        "## Current shape",
        "",
        f"- parent artifact: `{branch.get('parent_artifact', '')}`",
        f"- strongest variant: `{branch.get('strongest_variant', '')}`",
        f"- most generative variant: `{branch.get('most_generative_variant', '')}`",
        f"- weakest variant: `{branch.get('weakest_variant', '')}`",
        "",
        "## Active variants",
        "",
    ]
    for item in branch.get("active_variants", []):
        lines.append(f"- `{item}`")
    lines.extend(["", "## Open questions", ""])
    for item in branch.get("open_questions", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Missing or risky items", ""])
    if warnings:
        for item in warnings:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.extend(["", "## Key artifacts", ""])
    for field in ["key_notes", "key_syntheses", "loop_runs", "discard_records"]:
        lines.append(f"**{field}**")
        for item in branch.get(field, []):
            lines.append(f"- `{item}`")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def command_branch_dossier(args: argparse.Namespace) -> int:
    branch, _, paths = load_branch(args.slug)
    warnings = branch_warnings(branch, paths)
    dossier = dossier_markdown(branch, warnings)
    out = paths.generated / f"{branch['slug']}-dossier.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(dossier, encoding="utf-8", newline="\n")
    print(relpath(paths.root, out))
    return 0


def command_branch_list(args: argparse.Namespace) -> int:
    paths = repo_paths()
    manifests = branch_manifests(paths)
    for branch, _ in manifests:
        line = f"{branch.get('slug','')} | L{branch.get('maturity_level','')} | {branch.get('structure_type','')} | next={branch.get('next_recommended_pass','')}"
        print(line)
    return 0


def branch_snapshot_markdown(branch: dict[str, Any], paths: RepoPaths) -> str:
    """Generate a compact branch snapshot in markdown format."""
    lines = [
        f"# Branch Snapshot: {branch['title']}",
        "",
        f"**slug:** `{branch['slug']}`",
        f"**maturity:** {branch.get('maturity_level', 'N/A')} ({branch.get('maturity_note', '')})",
        f"**structure type:** `{branch.get('structure_type', 'N/A')}`",
        f"**status:** {branch.get('status', 'N/A')}",
        f"**next pass:** {branch.get('next_recommended_pass', 'N/A')}",
        "",
        "## Key Variants",
        "",
        f"- strongest: `{branch.get('strongest_variant', 'N/A')}`",
        f"- most generative: `{branch.get('most_generative_variant', 'N/A')}`",
        f"- weakest: `{branch.get('weakest_variant', 'N/A')}`",
        "",
        "## Active Variants",
        "",
    ]
    for item in branch.get("active_variants", [])[:5]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Open Questions", ""])
    for item in branch.get("open_questions", [])[:3]:
        lines.append(f"- {item}")
    lines.extend(["", "## Recent Artifacts", ""])
    lines.append("**Notes:**")
    for item in branch.get("key_notes", [])[-3:]:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("**Syntheses:**")
    for item in branch.get("key_syntheses", [])[-3:]:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("**Loop Runs:**")
    for item in branch.get("loop_runs", [])[-3:]:
        lines.append(f"- `{item}`")
    return "\n".join(lines).strip() + "\n"


def command_branch_snapshot(args: argparse.Namespace) -> int:
    """Generate a compact branch snapshot."""
    branch, _, paths = load_branch(args.slug)
    snapshot_md = branch_snapshot_markdown(branch, paths)
    out = paths.generated / f"{branch['slug']}-snapshot.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(snapshot_md, encoding="utf-8", newline="\n")
    print(f"generated: {relpath(paths.root, out)}")
    return 0


def branch_snapshot_markdown(branch: dict[str, Any], paths: RepoPaths) -> str:
    """Generate a compact branch snapshot in markdown format."""
    lines = [
        f"# Branch Snapshot: {branch['title']}",
        "",
        f"**slug:** `{branch['slug']}`",
        f"**maturity:** {branch.get('maturity_level', 'N/A')} ({branch.get('maturity_note', '')})",
        f"**structure type:** `{branch.get('structure_type', 'N/A')}`",
        f"**status:** {branch.get('status', 'N/A')}",
        f"**next pass:** {branch.get('next_recommended_pass', 'N/A')}",
        "",
        "## Key Variants",
        "",
        f"- strongest: `{branch.get('strongest_variant', 'N/A')}`",
        f"- most generative: `{branch.get('most_generative_variant', 'N/A')}`",
        f"- weakest: `{branch.get('weakest_variant', 'N/A')}`",
        "",
        "## Active Variants",
        "",
    ]
    for item in branch.get("active_variants", [])[:5]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Open Questions", ""])
    for item in branch.get("open_questions", [])[:3]:
        lines.append(f"- {item}")
    lines.extend(["", "## Recent Artifacts", ""])
    lines.append("**Notes:**")
    for item in branch.get("key_notes", [])[-3:]:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("**Syntheses:**")
    for item in branch.get("key_syntheses", [])[-3:]:
        lines.append(f"- `{item}`")
    lines.append("")
    lines.append("**Loop Runs:**")
    for item in branch.get("loop_runs", [])[-3:]:
        lines.append(f"- `{item}`")
    return "\n".join(lines).strip() + "\n"


def command_branch_snapshot(args: argparse.Namespace) -> int:
    """Generate a compact branch snapshot."""
    branch, _, paths = load_branch(args.slug)
    snapshot_md = branch_snapshot_markdown(branch, paths)
    out = paths.generated / f"{branch['slug']}-snapshot.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(snapshot_md, encoding="utf-8", newline="\n")
    print(f"generated: {relpath(paths.root, out)}")
    return 0


def next_run_id(paths: RepoPaths, branch_slug: str, run_type: str) -> str:
    prefix = f"{date.today().isoformat()}-{branch_slug}-{run_type}"
    existing = sorted(paths.runs.glob(f"{prefix}*.json"))
    if not existing:
        return prefix
    return f"{prefix}-{len(existing) + 1}"


def command_run_new(args: argparse.Namespace) -> int:
    branch, _, paths = load_branch(args.branch)
    run_type = args.type
    if run_type not in PASS_TYPES:
        raise SystemExit(f"Unknown run type '{run_type}'")
    run_id = next_run_id(paths, branch["slug"], run_type)
    data = {
        "run_id": run_id,
        "date": date.today().isoformat(),
        "branch_slug": branch["slug"],
        "run_type": run_type,
        "question": args.question or (branch.get("open_questions") or [""])[0],
        "stages_targeted": PASS_TYPES[run_type]["stages"],
        "expected_outputs": PASS_TYPES[run_type]["expected_outputs"],
        "created_outputs": [],
        "completion_status": "planned",
        "notes": "",
        "next_step": branch.get("next_recommended_pass", ""),
    }
    path = run_manifest_path(run_id)
    write_json(path, data)
    print(f"created: {relpath(paths.root, path)}")
    print(f"branch: {branch['slug']}")
    print(f"type: {run_type}")
    print("expected outputs:")
    for item in data["expected_outputs"]:
        print(f"- {item['kind']}: {item['description']}")
    return 0


def load_run(run_id: str) -> tuple[dict[str, Any], Path, RepoPaths]:
    paths = repo_paths()
    path = run_manifest_path(run_id)
    if not path.exists():
        raise SystemExit(f"Unknown run '{run_id}'. Expected manifest at {relpath(paths.root, path)}")
    return load_json(path), path, paths


def run_packet_markdown(run: dict[str, Any], branch: dict[str, Any], paths: RepoPaths) -> str:
    """Generate a run packet in markdown format."""
    lines = [
        f"# Run Packet: {run['run_id']}",
        "",
        f"**branch:** `{run['branch_slug']}`",
        f"**type:** {run['run_type']}",
        f"**status:** {run.get('completion_status', 'planned')}",
        "",
        "## Question",
        "",
        run.get('question', 'N/A'),
        "",
        "## Targeted Stages",
        "",
    ]
    for stage in run.get("stages_targeted", []):
        lines.append(f"- Stage {stage}")
    lines.extend(["", "## Expected Outputs", ""])
    for item in run.get("expected_outputs", []):
        lines.append(f"- {item['kind']}: {item['description']}")
    lines.extend(["", "## Branch Context", ""])
    lines.append(f"**maturity:** {branch.get('maturity_level', 'N/A')} ({branch.get('maturity_note', '')})")
    lines.append(f"**structure type:** `{branch.get('structure_type', 'N/A')}`")
    lines.append(f"**next pass:** {branch.get('next_recommended_pass', 'N/A')}")
    lines.extend(["", "## Strongest Variant", ""])
    lines.append(f"`{branch.get('strongest_variant', 'N/A')}`")
    lines.extend(["", "## Created Outputs", ""])
    created = run.get("created_outputs", [])
    if created:
        for item in created:
            if isinstance(item, dict):
                lines.append(f"- {item.get('kind', '')}: {item.get('path', '')}")
    else:
        lines.append("- none yet")
    lines.extend(["", "## Notes", ""])
    notes = run.get("notes", "").strip()
    if notes:
        for line in notes.splitlines():
            lines.append(f"- {line}")
    else:
        lines.append("- none")
    return "\n".join(lines).strip() + "\n"


def command_run_packet(args: argparse.Namespace) -> int:
    """Generate a run packet in both markdown and JSON formats."""
    run, _, paths = load_run(args.run_id)
    branch, _, _ = load_branch(run["branch_slug"])
    packet_md = run_packet_markdown(run, branch, paths)
    out_md = paths.generated / f"{run['run_id']}-packet.md"
    out_json = paths.generated / f"{run['run_id']}-packet.json"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(packet_md, encoding="utf-8", newline="\n")
    packet_json = {
        "run_id": run["run_id"],
        "branch_slug": run["branch_slug"],
        "run_type": run["run_type"],
        "question": run.get("question", ""),
        "stages_targeted": run.get("stages_targeted", []),
        "expected_outputs": run.get("expected_outputs", []),
        "created_outputs": run.get("created_outputs", []),
        "completion_status": run.get("completion_status", "planned"),
        "notes": run.get("notes", ""),
        "branch_context": {
            "maturity_level": branch.get("maturity_level", ""),
            "maturity_note": branch.get("maturity_note", ""),
            "structure_type": branch.get("structure_type", ""),
            "next_recommended_pass": branch.get("next_recommended_pass", ""),
            "strongest_variant": branch.get("strongest_variant", ""),
        },
    }
    write_json(out_json, packet_json)
    print(f"generated: {relpath(paths.root, out_md)}")
    print(f"generated: {relpath(paths.root, out_json)}")
    return 0


def run_packet_markdown(run: dict[str, Any], branch: dict[str, Any], paths: RepoPaths) -> str:
    """Generate a run packet in markdown format."""
    lines = [
        f"# Run Packet: {run['run_id']}",
        "",
        f"**branch:** `{run['branch_slug']}`",
        f"**type:** {run['run_type']}",
        f"**status:** {run.get('completion_status', 'planned')}",
        "",
        "## Question",
        "",
        run.get('question', 'N/A'),
        "",
        "## Targeted Stages",
        "",
    ]
    for stage in run.get("stages_targeted", []):
        lines.append(f"- Stage {stage}")
    lines.extend(["", "## Expected Outputs", ""])
    for item in run.get("expected_outputs", []):
        lines.append(f"- {item['kind']}: {item['description']}")
    lines.extend(["", "## Branch Context", ""])
    lines.append(f"**maturity:** {branch.get('maturity_level', 'N/A')} ({branch.get('maturity_note', '')})")
    lines.append(f"**structure type:** `{branch.get('structure_type', 'N/A')}`")
    lines.append(f"**next pass:** {branch.get('next_recommended_pass', 'N/A')}")
    lines.extend(["", "## Strongest Variant", ""])
    lines.append(f"`{branch.get('strongest_variant', 'N/A')}`")
    lines.extend(["", "## Created Outputs", ""])
    created = run.get("created_outputs", [])
    if created:
        for item in created:
            if isinstance(item, dict):
                lines.append(f"- {item.get('kind', '')}: {item.get('path', '')}")
    else:
        lines.append("- none yet")
    lines.extend(["", "## Notes", ""])
    notes = run.get("notes", "").strip()
    if notes:
        for line in notes.splitlines():
            lines.append(f"- {line}")
    else:
        lines.append("- none")
    return "\n".join(lines).strip() + "\n"


def command_run_packet(args: argparse.Namespace) -> int:
    """Generate a run packet in both markdown and JSON formats."""
    run, _, paths = load_run(args.run_id)
    branch, _, _ = load_branch(run["branch_slug"])
    packet_md = run_packet_markdown(run, branch, paths)
    out_md = paths.generated / f"{run['run_id']}-packet.md"
    out_json = paths.generated / f"{run['run_id']}-packet.json"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(packet_md, encoding="utf-8", newline="\n")
    packet_json = {
        "run_id": run["run_id"],
        "branch_slug": run["branch_slug"],
        "run_type": run["run_type"],
        "question": run.get("question", ""),
        "stages_targeted": run.get("stages_targeted", []),
        "expected_outputs": run.get("expected_outputs", []),
        "created_outputs": run.get("created_outputs", []),
        "completion_status": run.get("completion_status", "planned"),
        "notes": run.get("notes", ""),
        "branch_context": {
            "maturity_level": branch.get("maturity_level", ""),
            "maturity_note": branch.get("maturity_note", ""),
            "structure_type": branch.get("structure_type", ""),
            "next_recommended_pass": branch.get("next_recommended_pass", ""),
            "strongest_variant": branch.get("strongest_variant", ""),
        },
    }
    write_json(out_json, packet_json)
    print(f"generated: {relpath(paths.root, out_md)}")
    print(f"generated: {relpath(paths.root, out_json)}")
    return 0


def run_manifests(paths: RepoPaths) -> list[tuple[dict[str, Any], Path]]:
    manifests: list[tuple[dict[str, Any], Path]] = []
    for path in sorted(paths.runs.glob("*.json")):
        manifests.append((load_json(path), path))
    return manifests


def run_check_result(run: dict[str, Any], paths: RepoPaths) -> tuple[list[str], list[str]]:
    expected = {item["kind"] for item in run.get("expected_outputs", [])}
    created = run.get("created_outputs", [])
    created_kinds: set[str] = set()
    missing_files: list[str] = []
    for item in created:
        if isinstance(item, dict):
            kind = item.get("kind", "")
            path = item.get("path", "")
            if kind:
                created_kinds.add(kind)
            if path and not check_file_exists(paths.root, path):
                missing_files.append(path)
    missing_kinds = sorted(expected - created_kinds)
    return missing_kinds, missing_files


def print_run_check(run: dict[str, Any], missing_kinds: list[str], missing_files: list[str]) -> None:
    print(f"run: {run['run_id']}")
    print(f"branch: {run['branch_slug']}")
    print(f"type: {run['run_type']}")
    print(f"completion_status: {run.get('completion_status', '')}")
    if missing_kinds:
        print("missing expected output kinds:")
        for item in missing_kinds:
            print(f"- {item}")
    else:
        print("missing expected output kinds:\n- none")
    if missing_files:
        print("missing files referenced by run:")
        for item in missing_files:
            print(f"- {item}")
    else:
        print("missing files referenced by run:\n- none")


def print_run_show(run: dict[str, Any], missing_kinds: list[str], missing_files: list[str]) -> None:
    print_kv("run", run.get("run_id", ""))
    print_kv("date", run.get("date", ""))
    print_kv("branch", run.get("branch_slug", ""))
    print_kv("type", run.get("run_type", ""))
    print_kv("completion_status", run.get("completion_status", ""))
    print_kv("question", run.get("question", ""))
    print_kv("next_step", run.get("next_step", ""))
    print("stages_targeted:")
    for item in run.get("stages_targeted", []):
        print(f"- {item}")
    print("expected_outputs:")
    for item in run.get("expected_outputs", []):
        kind = item.get("kind", "")
        desc = item.get("description", "")
        print(f"- {kind}: {desc}")
    print("created_outputs:")
    created = run.get("created_outputs", [])
    if created:
        for item in created:
            if isinstance(item, dict):
                print(f"- {item.get('kind', '')}: {item.get('path', '')}")
    else:
        print("- none")
    print("notes:")
    notes = run.get("notes", "").strip()
    if notes:
        for line in notes.splitlines():
            print(f"- {line}")
    else:
        print("- none")
    print("validation:")
    if missing_kinds:
        print("- missing expected output kinds:")
        for item in missing_kinds:
            print(f"  - {item}")
    else:
        print("- missing expected output kinds: none")
    if missing_files:
        print("- missing files referenced by run:")
        for item in missing_files:
            print(f"  - {item}")
    else:
        print("- missing files referenced by run: none")


def command_run_check(args: argparse.Namespace) -> int:
    run, _, paths = load_run(args.run_id)
    missing_kinds, missing_files = run_check_result(run, paths)
    print_run_check(run, missing_kinds, missing_files)
    return 1 if missing_kinds or missing_files else 0


def command_run_show(args: argparse.Namespace) -> int:
    run, _, paths = load_run(args.run_id)
    missing_kinds, missing_files = run_check_result(run, paths)
    print_run_show(run, missing_kinds, missing_files)
    return 0


def command_run_list(args: argparse.Namespace) -> int:
    paths = repo_paths()
    manifests = run_manifests(paths)
    for run, _ in manifests:
        if args.branch and run.get("branch_slug") != args.branch:
            continue
        if args.status and run.get("completion_status") != args.status:
            continue
        line = f"{run.get('run_id','')} | {run.get('branch_slug','')} | {run.get('run_type','')} | {run.get('completion_status','')}"
        print(line)
    return 0


def command_run_update(args: argparse.Namespace) -> int:
    run, path, paths = load_run(args.run_id)
    updated = False

    if args.status:
        run["completion_status"] = args.status
        updated = True
    if args.question is not None:
        run["question"] = args.question
        updated = True
    if args.next_step is not None:
        run["next_step"] = args.next_step
        updated = True
    if args.note is not None:
        existing = run.get("notes", "")
        run["notes"] = f"{existing}\n{args.note}".strip() if existing else args.note
        updated = True
    if args.clear_notes:
        run["notes"] = ""
        updated = True

    outputs = run.setdefault("created_outputs", [])
    existing_pairs = {
        (item.get("kind", ""), item.get("path", ""))
        for item in outputs
        if isinstance(item, dict)
    }
    for kind, rel in args.add_output or []:
        pair = (kind, rel)
        if pair not in existing_pairs:
            outputs.append({"kind": kind, "path": rel})
            existing_pairs.add(pair)
            updated = True

    if not updated:
        print("No changes requested.")
        return 0

    write_json(path, run)
    print(f"updated: {relpath(paths.root, path)}")
    return 0


def command_run_complete(args: argparse.Namespace) -> int:
    run, path, paths = load_run(args.run_id)
    missing_kinds, missing_files = run_check_result(run, paths)
    if (missing_kinds or missing_files) and not args.force:
        print_run_check(run, missing_kinds, missing_files)
        print("Run is not complete. Use --force to mark complete anyway.")
        return 1

    run["completion_status"] = "completed" if not (missing_kinds or missing_files) else "completed_with_gaps"
    write_json(path, run)
    print(f"updated: {relpath(paths.root, path)}")
    print(f"completion_status: {run['completion_status']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="meta", description="Meta-autoresearch method infrastructure CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    branch = subparsers.add_parser("branch", help="Branch state commands")
    branch_sub = branch.add_subparsers(dest="branch_command", required=True)

    branch_status = branch_sub.add_parser("status", help="Show branch status")
    branch_status.add_argument("slug")
    branch_status.set_defaults(func=command_branch_status)

    branch_check = branch_sub.add_parser("check", help="Validate branch hygiene")
    branch_check.add_argument("slug")
    branch_check.set_defaults(func=command_branch_check)

    branch_dossier = branch_sub.add_parser("dossier", help="Generate branch dossier")
    branch_dossier.add_argument("slug")
    branch_dossier.set_defaults(func=command_branch_dossier)

    branch_list = branch_sub.add_parser("list", help="List known branches")
    branch_list.set_defaults(func=command_branch_list)

    branch_snapshot = branch_sub.add_parser("snapshot", help="Generate compact branch snapshot")
    branch_snapshot.add_argument("slug")
    branch_snapshot.set_defaults(func=command_branch_snapshot)

    branch_stale = branch_sub.add_parser("stale", help="Check for stale generated files")
    branch_stale.add_argument("slug", nargs="?", default=None, help="Branch slug (optional, checks all if omitted)")
    branch_stale.set_defaults(func=command_branch_stale)

    branch_index = branch_sub.add_parser("index", help="Generate artifact index for a branch")
    branch_index.add_argument("slug")
    branch_index.set_defaults(func=command_branch_index)

    branch_compare_prep = branch_sub.add_parser("compare-prep", help="Generate comparison prep material")
    branch_compare_prep.add_argument("slug")
    branch_compare_prep.set_defaults(func=command_branch_compare_prep)

    # Iteration 3: Model delegation
    delegate = subparsers.add_parser("delegate", help="Delegated model tasks")
    delegate_sub = delegate.add_subparsers(dest="delegate_command", required=True)

    delegate_summarize = delegate_sub.add_parser("summarize-note", help="Summarize a research note")
    delegate_summarize.add_argument("input", help="Path to the note file")
    delegate_summarize.set_defaults(func=command_delegate_summarize)

    delegate_extract = delegate_sub.add_parser("extract-claims", help="Extract claims from an artifact")
    delegate_extract.add_argument("input", help="Path to the artifact file")
    delegate_extract.set_defaults(func=command_delegate_extract_claims)

    run = subparsers.add_parser("run", help="Run manifest commands")
    run_sub = run.add_subparsers(dest="run_command", required=True)

    run_packet = run_sub.add_parser("packet", help="Generate run packet in markdown and JSON")
    run_packet.add_argument("run_id")
    run_packet.set_defaults(func=command_run_packet)

    run_new = run_sub.add_parser("new", help="Create a new run manifest")
    run_new.add_argument("branch")
    run_new.add_argument("--type", required=True, choices=sorted(PASS_TYPES.keys()))
    run_new.add_argument("--question")
    run_new.set_defaults(func=command_run_new)

    run_check = run_sub.add_parser("check", help="Validate a run manifest")
    run_check.add_argument("run_id")
    run_check.set_defaults(func=command_run_check)

    run_show = run_sub.add_parser("show", help="Show a run manifest with validation summary")
    run_show.add_argument("run_id")
    run_show.set_defaults(func=command_run_show)

    run_list = run_sub.add_parser("list", help="List known run manifests")
    run_list.add_argument("--branch")
    run_list.add_argument("--status")
    run_list.set_defaults(func=command_run_list)

    run_update = run_sub.add_parser("update", help="Update a run manifest")
    run_update.add_argument("run_id")
    run_update.add_argument("--status", choices=["planned", "in_progress", "completed", "completed_with_gaps", "paused"])
    run_update.add_argument("--question")
    run_update.add_argument("--next-step")
    run_update.add_argument("--note")
    run_update.add_argument("--clear-notes", action="store_true")
    run_update.add_argument("--add-output", nargs=2, action="append", metavar=("KIND", "PATH"))
    run_update.set_defaults(func=command_run_update)

    run_complete = run_sub.add_parser("complete", help="Mark a run complete when checks pass")
    run_complete.add_argument("run_id")
    run_complete.add_argument("--force", action="store_true")
    run_complete.set_defaults(func=command_run_complete)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
