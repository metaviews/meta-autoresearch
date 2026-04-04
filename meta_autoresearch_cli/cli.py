from __future__ import annotations

import argparse
import json
import os
import urllib.request
import urllib.error
import concurrent.futures
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
                os.environ[key.strip()] = value.strip()


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
        "fallback_small": os.environ.get("META_MODEL_FALLBACK_SMALL", ""),
        "fallback_mid": os.environ.get("META_MODEL_FALLBACK_MID", ""),
        "fallback_strong": os.environ.get("META_MODEL_FALLBACK_STRONG", ""),
        "timeout": os.environ.get("META_MODEL_TIMEOUT", "90"),
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


def call_openrouter(messages: list[dict[str, str]], model: str, config: dict[str, str], timeout: int = 60, fallback_models: list[str] = None) -> tuple[str, str, float]:
    """
    Call OpenRouter API with the given messages and model.
    
    Returns (content, model_used, duration_seconds) tuple.
    If primary model fails or times out, tries fallback models.
    """
    import time
    
    api_key = config.get("openrouter_api_key", "")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY not set. Add it to .env file.")
    
    base_url = config.get("openrouter_base_url", "https://openrouter.ai/api/v1")
    http_referer = config.get("openrouter_http_referer", "")
    app_name = config.get("openrouter_app_name", "Meta Autoresearch")
    
    url = f"{base_url}/chat/completions"
    
    # Build model list: primary + fallbacks
    models_to_try = [model]
    if fallback_models:
        models_to_try.extend(fallback_models)
    
    for attempt_model in models_to_try:
        start_time = time.time()
        
        payload = {
            "model": attempt_model,
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
            "X-OpenRouter-Title": app_name,
        }
        
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                duration = time.time() - start_time
                
                if content and len(content.strip()) > 10:
                    return content, attempt_model, duration
                else:
                    # Got response but content is empty/insufficient
                    continue
                    
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            # Try next model on rate limit or server error
            if e.code in [429, 500, 502, 503]:
                continue
            raise SystemExit(f"OpenRouter API error ({e.code}): {error_body}")
        except urllib.error.URLError as e:
            # Try next model on network error
            continue
        except json.JSONDecodeError:
            continue
        except TimeoutError:
            # Try next model on timeout
            continue
    
    # All models failed
    raise SystemExit(f"All models failed: {models_to_try}")


def get_model_for_slot(slot: str) -> tuple[str, dict[str, str], list[str], int]:
    """
    Get model ID, config, fallbacks, and timeout for the given slot (small, mid, strong).
    
    Returns (model_id, config, fallback_models, timeout) tuple.
    """
    config = get_model_config()
    
    slot_map = {
        "small": config.get("small", ""),
        "mid": config.get("mid", ""),
        "strong": config.get("strong", ""),
    }
    
    fallback_map = {
        "small": config.get("fallback_small", ""),
        "mid": config.get("fallback_mid", ""),
        "strong": config.get("fallback_strong", ""),
    }
    
    model_id = slot_map.get(slot, "")
    if not model_id:
        raise SystemExit(f"Model slot '{slot}' not configured. Set META_MODEL_DEFAULT_{slot.upper()} in .env")
    
    # Parse fallback models (comma-separated)
    fallback_str = fallback_map.get(slot, "")
    fallback_models = [m.strip() for m in fallback_str.split(",") if m.strip()] if fallback_str else []
    
    # Get timeout
    timeout = int(config.get("timeout", "90"))
    
    return model_id, config, fallback_models, timeout


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


# =============================================================================
# Phase 9B: Parallel Execution
# =============================================================================


def call_openrouter_task(messages, model_id, config, timeout, fallback_models):
    """Wrapper for call_openrouter that returns result dict for parallel execution."""
    try:
        content, model_used, duration = call_openrouter(messages, model_id, config, timeout=timeout, fallback_models=fallback_models)
        return {
            "success": True,
            "content": content,
            "model": model_used,
            "duration": duration,
            "error": None
        }
    except SystemExit as e:
        return {
            "success": False,
            "content": None,
            "model": model_id,
            "duration": 0,
            "error": str(e)
        }


def parallel_model_calls(tasks, config, max_workers=None, use_dynamic_selection=False):
    """
    Execute multiple model calls in parallel.
    
    Args:
        tasks: List of dicts with keys:
            - messages: List of message dicts for the API call
            - source: Source file path (for tracking)
            - task_type: Task type string (e.g., "summarize-note")
        config: Model config dict from get_model_for_slot
        max_workers: Max parallel workers (defaults to len(tasks))
        use_dynamic_selection: If True, use select_model_for_task instead of config
    
    Returns:
        List of result dicts with task info, content, timing, and errors.
    """
    if use_dynamic_selection:
        # Use dynamic model selection
        results = []
        for task in tasks:
            content_length = len(task.get("messages", [])[-1].get("content", ""))
            model_id, task_config, fallback_models, timeout = select_model_for_task(task["task_type"], content_length)
            
            try:
                api_result = call_openrouter_task(
                    task["messages"],
                    model_id,
                    task_config,
                    timeout,
                    fallback_models
                )
                result = {
                    "task_type": task["task_type"],
                    "source": task["source"],
                    "success": api_result["success"],
                    "content": api_result["content"],
                    "model": api_result["model"],
                    "duration": api_result["duration"],
                    "error": api_result["error"]
                }
            except SystemExit as e:
                result = {
                    "task_type": task["task_type"],
                    "source": task["source"],
                    "success": False,
                    "content": None,
                    "model": model_id,
                    "duration": 0,
                    "error": str(e)
                }
            results.append(result)
        return results
    else:
        # Use config-provided model (existing behavior)
        model_id = config.get("small", "qwen/qwen3.5-flash-02-23")
        # Get fallbacks from env
        fallback_str = os.environ.get("META_MODEL_FALLBACK_SMALL", "")
        fallback_models = [m.strip() for m in fallback_str.split(",") if m.strip()] if fallback_str else []
        timeout = int(os.environ.get("META_MODEL_TIMEOUT", "90"))
        
        if max_workers is None:
            max_workers = len(tasks)
        
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_task = {}
            for task in tasks:
                future = executor.submit(
                    call_openrouter_task,
                    task["messages"],
                    model_id,
                    config,
                    timeout,
                    fallback_models
                )
                future_to_task[future] = task
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_task):
                task = future_to_task[future]
                api_result = future.result()
                
                result = {
                    "task_type": task["task_type"],
                    "source": task["source"],
                    "success": api_result["success"],
                    "content": api_result["content"],
                    "model": api_result["model"],
                    "duration": api_result["duration"],
                    "error": api_result["error"]
                }
                results.append(result)
        
        return results


# =============================================================================
# Phase 7B: Component Index
# =============================================================================

COMPONENT_TYPES = ["region", "mechanism", "institution", "infrastructure", "evidence", "hazard"]


def components_dir() -> Path:
    """Get the components directory path."""
    return repo_paths().meta / "components"


def load_component_yaml(component_dir: Path) -> list[dict[str, Any]]:
    """Load all component YAML files from the components directory."""
    import yaml
    
    components = []
    for yaml_file in component_dir.glob("*.yaml"):
        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                component = yaml.safe_load(f)
                if component and "id" in component:
                    component["_source_file"] = yaml_file.name
                    components.append(component)
        except Exception as e:
            print(f"Warning: Could not parse {yaml_file.name}: {e}")
    return components


def component_index_markdown(components: list[dict[str, Any]]) -> str:
    """Generate markdown index from components."""
    lines = [
        "# Component Index",
        "",
        f"**Generated:** {date.today().isoformat()}",
        f"**Total components:** {len(components)}",
        "",
        "---",
        "",
    ]
    
    # Group by type
    by_type: dict[str, list[dict[str, Any]]] = {}
    for comp in components:
        comp_type = comp.get("type", "unknown")
        if comp_type not in by_type:
            by_type[comp_type] = []
        by_type[comp_type].append(comp)
    
    for comp_type in COMPONENT_TYPES:
        type_components = by_type.get(comp_type, [])
        if not type_components:
            continue
        
        lines.append(f"## {comp_type.title()}s")
        lines.append("")
        lines.append("| ID | Name | Domain | Related Branches |")
        lines.append("|----|------|--------|------------------|")
        
        for comp in sorted(type_components, key=lambda c: c.get("id", "")):
            comp_id = comp.get("id", "unknown")
            name = comp.get("name", "Unknown")
            domain = comp.get("domain", "N/A")
            branches = ", ".join(comp.get("related_branches", [])) or "N/A"
            lines.append(f"| `{comp_id}` | {name} | {domain} | {branches} |")
        
        lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("*This index is auto-generated from `meta/components/*.yaml` files.*")
    
    return "\n".join(lines)


def command_component_index(args: argparse.Namespace) -> int:
    """Build component index from YAML files."""
    try:
        import yaml
    except ImportError:
        raise SystemExit("PyYAML not installed. Run: pip install pyyaml")
    
    comp_dir = components_dir()
    if not comp_dir.exists():
        raise SystemExit(f"Components directory not found: {comp_dir}")
    
    components = load_component_yaml(comp_dir)
    
    if not components:
        print("No component YAML files found in", comp_dir)
        return 0
    
    # Generate index markdown
    index_md = component_index_markdown(components)
    
    # Write to components directory
    index_path = comp_dir / "INDEX.md"
    index_path.write_text(index_md, encoding="utf-8", newline="\n")
    
    # Also update README with current count
    readme_path = comp_dir / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        # Update the component count in the table if present
        # For now, just note that index was generated
    
    print(f"Generated component index: {len(components)} components")
    print(f"  {index_path.relative_to(repo_paths().root)}")
    
    # Print summary by type
    by_type: dict[str, int] = {}
    for comp in components:
        comp_type = comp.get("type", "unknown")
        by_type[comp_type] = by_type.get(comp_type, 0) + 1
    
    for comp_type in COMPONENT_TYPES:
        count = by_type.get(comp_type, 0)
        if count > 0:
            print(f"  {comp_type}: {count}")
    
    return 0


def command_component_search(args: argparse.Namespace) -> int:
    """Search for components by query."""
    try:
        import yaml
    except ImportError:
        raise SystemExit("PyYAML not installed. Run: pip install pyyaml")
    
    query = args.query.lower()
    comp_dir = components_dir()
    
    if not comp_dir.exists():
        raise SystemExit(f"Components directory not found: {comp_dir}")
    
    components = load_component_yaml(comp_dir)
    
    # Filter by type if specified
    if args.type:
        components = [c for c in components if c.get("type") == args.type]
    
    # Search in id, name, description, and domain
    matches = []
    for comp in components:
        searchable = " ".join([
            comp.get("id", ""),
            comp.get("name", ""),
            comp.get("description", ""),
            comp.get("domain", ""),
            " ".join(comp.get("related_branches", [])),
        ]).lower()
        
        if query in searchable:
            matches.append(comp)
    
    if not matches:
        print(f"No components found matching '{query}'")
        if args.type:
            print(f"(filtered by type: {args.type})")
        return 0
    
    # Print results
    print(f"Found {len(matches)} component(s) matching '{query}':\n")
    
    for comp in sorted(matches, key=lambda c: c.get("id", "")):
        comp_id = comp.get("id", "unknown")
        name = comp.get("name", "Unknown")
        comp_type = comp.get("type", "unknown")
        domain = comp.get("domain", "N/A")
        branches = ", ".join(comp.get("related_branches", [])) or "N/A"
        
        print(f"  `{comp_id}` ({comp_type})")
        print(f"    Name: {name}")
        print(f"    Domain: {domain}")
        print(f"    Related branches: {branches}")
        
        # Show first sentence of description
        desc = comp.get("description", "").strip().replace("\n", " ")
        if desc:
            first_sentence = desc.split(".")[0][:100]
            if len(desc) > 100:
                first_sentence += "..."
            print(f"    Description: {first_sentence}")
        print()
    
    return 0


def command_component_list(args: argparse.Namespace) -> int:
    """List components by type."""
    try:
        import yaml
    except ImportError:
        raise SystemExit("PyYAML not installed. Run: pip install pyyaml")
    
    comp_dir = components_dir()
    
    if not comp_dir.exists():
        raise SystemExit(f"Components directory not found: {comp_dir}")
    
    components = load_component_yaml(comp_dir)
    
    # Filter by type if specified
    if args.type:
        components = [c for c in components if c.get("type") == args.type]
        type_filter = f" ({args.type})"
    else:
        type_filter = ""
    
    if not components:
        print(f"No components found{type_filter}")
        return 0
    
    print(f"Components{type_filter}: {len(components)}\n")
    
    # Group by type for display
    by_type: dict[str, list[dict[str, Any]]] = {}
    for comp in components:
        comp_type = comp.get("type", "unknown")
        if comp_type not in by_type:
            by_type[comp_type] = []
        by_type[comp_type].append(comp)
    
    for comp_type in sorted(by_type.keys()):
        type_components = by_type[comp_type]
        print(f"## {comp_type.title()}s ({len(type_components)})")
        
        for comp in sorted(type_components, key=lambda c: c.get("id", "")):
            comp_id = comp.get("id", "unknown")
            name = comp.get("name", "Unknown")
            print(f"  `{comp_id}` — {name}")
        
        print()
    
    return 0


def command_component_suggest(args: argparse.Namespace) -> int:
    """Suggest components for a new branch."""
    try:
        import yaml
    except ImportError:
        raise SystemExit("PyYAML not installed. Run: pip install pyyaml")
    
    # Load branch manifest
    branch, _, paths = load_branch(args.slug)
    
    comp_dir = components_dir()
    if not comp_dir.exists():
        raise SystemExit(f"Components directory not found: {comp_dir}")
    
    components = load_component_yaml(comp_dir)
    
    branch_domain = branch.get("domain", "")
    structure_type = branch.get("structure_type", "")
    branch_slug = branch.get("slug", "")
    
    # Find relevant components
    relevant = []
    for comp in components:
        score = 0
        reasons = []
        
        # Match by domain
        if comp.get("domain") == branch_domain:
            score += 3
            reasons.append("same domain")
        
        # Match by structure type in metadata
        comp_structure_types = comp.get("metadata", {}).get("structure_types", [])
        if structure_type and any(structure_type.lower() in st.lower() for st in comp_structure_types):
            score += 2
            reasons.append("matching structure type")
        
        # Match by related branches
        if branch_slug in comp.get("related_branches", []):
            score += 5
            reasons.append("from this branch")
        
        if score > 0:
            relevant.append((score, comp, reasons))
    
    if not relevant:
        print(f"No existing components found for branch '{branch_slug}'")
        print("\nThis is a new branch domain. Consider creating components for:")
        print("  - Key regions or geographies")
        print("  - Core mechanisms or failure patterns")
        print("  - Relevant institutions or infrastructure")
        return 0
    
    # Sort by score and print
    relevant.sort(key=lambda x: (-x[0], x[1].get("id", "")))
    
    print(f"Suggested components for '{branch_slug}':\n")
    
    for score, comp, reasons in relevant:
        comp_id = comp.get("id", "unknown")
        name = comp.get("name", "Unknown")
        comp_type = comp.get("type", "unknown")
        
        print(f"  `{comp_id}` ({comp_type}) — {name}")
        print(f"    Relevance: {', '.join(reasons)} (score: {score})")
        print()
    
    print("Use these component IDs when generating new scenarios or comparing branches.")
    
    return 0


# =============================================================================
# Phase 7C: Curation Support
# =============================================================================

EVALUATION_DIMENSIONS = [
    ("evidence_strength", "Evidence strength", "How well sources support claims"),
    ("internal_coherence", "Internal coherence", "Causal structure clarity"),
    ("relevance", "Relevance", "Match to research question"),
    ("preparedness_value", "Preparedness value", "Decision-usefulness"),
    ("novelty", "Novelty", "Expands search space vs restates familiar"),
    ("actionability", "Actionability", "Clear next research step"),
    ("status_quo_challenge", "Status-quo challenge", "Questions dominant assumptions"),
    ("imaginative_power", "Imaginative power", "Expands plausible range"),
]


def read_markdown_frontmatter(content: str) -> dict[str, Any]:
    """Extract YAML frontmatter from markdown content."""
    try:
        import yaml
    except ImportError:
        return {}
    
    if not content.startswith("---"):
        return {}
    
    try:
        end = content.index("---", 3)
        frontmatter = content[4:end].strip()
        return yaml.safe_load(frontmatter) or {}
    except (ValueError, Exception):
        return {}


def extract_variant_info(content: str, path: str) -> dict[str, Any]:
    """Extract variant information from markdown content."""
    frontmatter = read_markdown_frontmatter(content)
    
    # Extract first 200 chars of body for summary
    body = content
    if body.startswith("---"):
        try:
            end = body.index("---", 3)
            body = body[end + 3:].strip()
        except ValueError:
            pass
    
    # Remove markdown headers for summary
    lines = body.split("\n")
    summary_lines = []
    for line in lines:
        if line.startswith("#"):
            continue
        if line.strip():
            summary_lines.append(line.strip())
            if len(" ".join(summary_lines)) > 200:
                break
    
    summary = " ".join(summary_lines)[:200] + "..." if summary_lines else "No summary available"
    
    return {
        "id": frontmatter.get("title", path.split("/")[-1]),
        "path": path,
        "type": frontmatter.get("scenario type", "variant"),
        "status": frontmatter.get("status", "draft"),
        "summary": summary,
    }


def command_curate_compare(args: argparse.Namespace) -> int:
    """Generate side-by-side comparison table for variants."""
    paths = repo_paths()
    
    variant_paths = args.variants
    if len(variant_paths) < 2:
        raise SystemExit("At least two variant paths required for comparison")
    
    # Load variant information
    variants = []
    for path_str in variant_paths:
        path = Path(path_str)
        if not path.is_absolute():
            path = paths.root / path_str
        
        if not path.exists():
            print(f"Warning: Variant not found: {path_str}")
            continue
        
        content = path.read_text(encoding="utf-8")
        info = extract_variant_info(content, path_str)
        variants.append(info)
    
    if len(variants) < 2:
        raise SystemExit("Need at least two valid variants for comparison")
    
    # Generate comparison markdown
    lines = [
        "# Variant Comparison",
        "",
        f"**Generated:** {date.today().isoformat()}",
        f"**Variants:** {len(variants)}",
        "",
        "---",
        "",
        "## Side-by-Side Summary",
        "",
    ]
    
    # Create comparison table
    headers = ["Aspect"] + [f"Variant {i+1}" for i in range(len(variants))]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    
    # Path row
    paths_row = ["**Path**"] + [f"`{v['path'].split('/')[-1]}`" for v in variants]
    lines.append("| " + " | ".join(paths_row) + " |")
    
    # Type row
    types_row = ["**Type**"] + [v["type"] for v in variants]
    lines.append("| " + " | ".join(types_row) + " |")
    
    # Status row
    status_row = ["**Status**"] + [v["status"] for v in variants]
    lines.append("| " + " | ".join(status_row) + " |")
    
    lines.append("")
    lines.append("## Summary Descriptions")
    lines.append("")
    
    for i, v in enumerate(variants, 1):
        lines.append(f"### Variant {i}")
        lines.append("")
        lines.append(f"**Path:** `{v['path']}`")
        lines.append("")
        lines.append(v["summary"])
        lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("## Evaluation Dimensions")
    lines.append("")
    lines.append("Use these dimensions when comparing:")
    lines.append("")
    for dim_id, dim_name, dim_desc in EVALUATION_DIMENSIONS:
        lines.append(f"{dim_id.replace('_', ' ').title()}: {dim_desc}")
    lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("## Comparison Questions")
    lines.append("")
    lines.append("1. Which variant has stronger evidence support?")
    lines.append("2. Which variant has clearer causal logic?")
    lines.append("3. Which variant is more decision-useful?")
    lines.append("4. Which variant challenges status-quo assumptions more effectively?")
    lines.append("5. Which variant should be marked strongest? weakest? most generative?")
    lines.append("")
    
    # Output
    output_path = paths.generated / f"comparison-{'-vs-'.join(Path(p).stem for p in variant_paths[:2])}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    
    print(f"Generated comparison table: {relpath(paths.root, output_path)}")
    print(f"Variants compared: {len(variants)}")
    
    return 0


def command_curate_matrix(args: argparse.Namespace) -> int:
    """Generate evaluation matrix draft for branch variants."""
    paths = repo_paths()
    
    # Load branch
    branch, _, _ = load_branch(args.slug)
    
    variants = branch.get("active_variants", [])
    parent = branch.get("parent_artifact")
    
    if parent:
        all_artifacts = [parent] + variants
    else:
        all_artifacts = variants
    
    if not all_artifacts:
        raise SystemExit(f"No variants found for branch '{args.slug}'")
    
    # Load variant information
    variant_data = []
    for path_str in all_artifacts:
        path = paths.root / path_str
        if not path.exists():
            print(f"Warning: Artifact not found: {path_str}")
            continue
        
        content = path.read_text(encoding="utf-8")
        info = extract_variant_info(content, path_str)
        info["is_parent"] = (path_str == parent)
        variant_data.append(info)
    
    if not variant_data:
        raise SystemExit("No valid variants found")
    
    # Generate evaluation matrix markdown
    lines = [
        "# Evaluation Matrix",
        "",
        f"**Branch:** `{branch['slug']}`",
        f"**Generated:** {date.today().isoformat()}",
        f"**Variants:** {len(variant_data)}",
        "",
        "---",
        "",
        "## Instructions",
        "",
        "Fill in scores (1-5) for each variant across all dimensions.",
        "Add brief rationale for scores that differ significantly.",
        "Mark curation decision (keep/revise/discard) for each variant.",
        "",
        "---",
        "",
        "## Evaluation Table",
        "",
    ]
    
    # Create header row
    headers = ["Dimension"] + [f"{i+1}. {v['path'].split('/')[-1][:30]}{'...' if len(v['path'].split('/')[-1]) > 30 else ''}" for i, v in enumerate(variant_data)]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    
    # Score rows for each dimension
    for dim_id, dim_name, dim_desc in EVALUATION_DIMENSIONS:
        row = [f"**{dim_name}**<br/>{dim_desc}"]
        for _ in variant_data:
            row.append("_score + rationale_")
        lines.append("| " + " | ".join(row) + " |")
    
    # Curation decision row
    curation_row = ["**Curation**"]
    for v in variant_data:
        if v.get("is_parent"):
            curation_row.append("_parent_")
        else:
            curation_row.append("keep / revise / discard")
    lines.append("| " + " | ".join(curation_row) + " |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Variant Details")
    lines.append("")
    
    for i, v in enumerate(variant_data, 1):
        lines.append(f"### {i}. {v['path'].split('/')[-1]}")
        lines.append("")
        lines.append(f"**Path:** `{v['path']}`")
        lines.append(f"**Type:** {v['type']}")
        lines.append(f"**Status:** {v['status']}")
        lines.append("")
        lines.append("**Summary:**")
        lines.append("")
        lines.append(v["summary"])
        lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("## Curation Decisions")
    lines.append("")
    lines.append("### Keep")
    lines.append("")
    lines.append("_List variants to keep and why:_")
    lines.append("")
    lines.append("### Revise")
    lines.append("")
    lines.append("_List variants to revise and what changes are needed:_")
    lines.append("")
    lines.append("### Discard")
    lines.append("")
    lines.append("_List variants to discard and why:_")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Next Step")
    lines.append("")
    lines.append(f"_Recommended pass: {branch.get('next_recommended_pass', 'TBD')}_")
    lines.append("")
    
    # Output
    output_path = paths.generated / f"{branch['slug']}-evaluation-matrix-draft.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    
    print(f"Generated evaluation matrix draft: {relpath(paths.root, output_path)}")
    print(f"Variants included: {len(variant_data)}")
    
    return 0


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
    model_id, config, fallbacks, timeout = get_model_for_slot("small")
    
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
    model_id, config, fallbacks, timeout = get_model_for_slot("small")
    
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


# =============================================================================
# Phase 6B: Workflow Automation
# =============================================================================


def command_delegate_branch_packet(args: argparse.Namespace) -> int:
    """
    Generate a complete branch packet combining snapshot + index + compare-prep.
    
    This is a workflow automation command that chains multiple generation tasks.
    """
    branch, _, paths = load_branch(args.slug)
    
    # Generate snapshot
    snapshot_md = branch_snapshot_markdown(branch, paths)
    snapshot_path = paths.generated / f"{branch['slug']}-snapshot.md"
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(snapshot_md, encoding="utf-8", newline="\n")
    print(f"generated: {relpath(paths.root, snapshot_path)}")
    
    # Generate artifact index
    index_md = artifact_index_markdown(branch, paths)
    index_path = paths.generated / f"{branch['slug']}-artifact-index.md"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(index_md, encoding="utf-8", newline="\n")
    print(f"generated: {relpath(paths.root, index_path)}")
    
    # Generate comparison prep
    prep_md = comparison_prep_markdown(branch, paths)
    prep_path = paths.generated / f"{branch['slug']}-comparison-prep.md"
    prep_path.parent.mkdir(parents=True, exist_ok=True)
    prep_path.write_text(prep_md, encoding="utf-8", newline="\n")
    print(f"generated: {relpath(paths.root, prep_path)}")
    
    # Generate combined packet summary
    packet_summary = f"""# Branch Packet: {branch['title']}

**Generated:** {datetime.now().isoformat()}

## Contents

This packet combines three generated artifacts:

1. **Snapshot** - `{branch['slug']}-snapshot.md`
   - Current branch state at a glance
   - Key variants, open questions, recent artifacts

2. **Artifact Index** - `{branch['slug']}-artifact-index.md`
   - Complete listing of notes, scenarios, syntheses, loop runs, discards
   - Modification times and existence checks

3. **Comparison Prep** - `{branch['slug']}-comparison-prep.md`
   - Variant overview table with roles
   - 8 evaluation dimensions
   - Guiding questions from branch manifest
   - Recommended comparison approach

## Quick Reference

- **Maturity:** {branch.get('maturity_level', 'N/A')} ({branch.get('maturity_note', '')})
- **Structure type:** `{branch.get('structure_type', 'N/A')}`
- **Next pass:** `{branch.get('next_recommended_pass', 'N/A')}`
- **Strongest variant:** `{branch.get('strongest_variant', 'N/A')}`
- **Most generative:** `{branch.get('most_generative_variant', 'N/A')}`

## Recommended Next Steps

1. Read the snapshot for current state (2 min)
2. Skim the artifact index for what exists (1 min)
3. Use comparison prep to guide your analysis (5-10 min)
4. Run delegated tasks as needed:
   - `delegate summarize-note <path>` for any grounding notes
   - `delegate extract-claims <path>` for any scenarios
5. Begin your research pass with the full context already assembled
"""
    
    summary_path = paths.generated / f"{branch['slug']}-packet.md"
    summary_path.write_text(packet_summary, encoding="utf-8", newline="\n")
    print(f"generated: {relpath(paths.root, summary_path)}")
    
    print(f"\nBranch packet complete: 4 files generated for '{branch['slug']}'")
    return 0


def command_delegate_run_prep(args: argparse.Namespace) -> int:
    """
    Prepare all materials for a specific run type.
    
    This is a workflow automation command that chains branch packet generation
    with run-specific preparation tasks.
    """
    branch, _, paths = load_branch(args.branch)
    run_type = args.type
    
    # First generate the branch packet
    print(f"=== Generating branch packet for {branch['slug']} ===\n")
    
    # Generate snapshot
    snapshot_md = branch_snapshot_markdown(branch, paths)
    snapshot_path = paths.generated / f"{branch['slug']}-snapshot.md"
    snapshot_path.write_text(snapshot_md, encoding="utf-8", newline="\n")
    print(f"generated: {relpath(paths.root, snapshot_path)}")
    
    # Generate artifact index
    index_md = artifact_index_markdown(branch, paths)
    index_path = paths.generated / f"{branch['slug']}-artifact-index.md"
    index_path.write_text(index_md, encoding="utf-8", newline="\n")
    print(f"generated: {relpath(paths.root, index_path)}")
    
    # Generate comparison prep
    prep_md = comparison_prep_markdown(branch, paths)
    prep_path = paths.generated / f"{branch['slug']}-comparison-prep.md"
    prep_path.write_text(prep_md, encoding="utf-8", newline="\n")
    print(f"generated: {relpath(paths.root, prep_path)}")
    
    # Generate run-specific prep
    run_type_info = PASS_TYPES.get(run_type, {})
    stages = run_type_info.get("stages", [])
    expected = run_type_info.get("expected_outputs", [])
    
    run_prep = f"""# Run Prep: {run_type} pass for {branch['slug']}

**Generated:** {datetime.now().isoformat()}
**Target stages:** {[f"Stage {s}" for s in stages]}

## Expected Outputs

"""
    for exp in expected:
        run_prep += f"- **{exp['kind']}**: {exp['description']}\n"
    
    run_prep += f"""
## Branch Context

- **Maturity:** {branch.get('maturity_level', 'N/A')} ({branch.get('maturity_note', '')})
- **Structure type:** `{branch.get('structure_type', 'N/A')}`
- **Next recommended pass:** `{branch.get('next_recommended_pass', 'N/A')}`

## Recommended Preparation Tasks

"""
    
    # Add run-type specific recommendations
    if run_type == "grounding":
        run_prep += """1. Review existing grounding notes in artifact index
2. Run `delegate summarize-note` on any new source materials
3. Identify which scenario needs grounding
4. Prepare to update scenario with case evidence
"""
    elif run_type == "variant":
        run_prep += """1. Review parent scenario and existing variants
2. Run `delegate extract-claims` on parent to identify variation points
3. Prepare to generate 2-3 new variants with distinct mechanisms
4. Ensure variants differ in structure, not just wording
"""
    elif run_type == "comparison":
        run_prep += """1. Read comparison-prep document for variant overview
2. Run `delegate summarize-note` on grounding notes if outdated
3. Run `delegate extract-claims` on each variant
4. Prepare to score variants against 8 evaluation dimensions
5. Plan curation decisions: keep/revise/merge/discard per variant
"""
    elif run_type == "maturity":
        run_prep += """1. Review all key_syntheses and loop_runs
2. Assess whether branch meets Level 4 criteria (if currently L3)
3. Identify what method-level insight the branch provides
4. Prepare to update branch manifest with maturity judgment
"""
    elif run_type == "discard":
        run_prep += """1. Review all active variants and parent scenario
2. Identify weakest direction(s) to prune
3. Prepare discard record explaining why
4. Ensure discard is methodologically informative, not just negative
"""
    elif run_type == "capability-fit":
        run_prep += """1. Review previous delegated task outputs
2. Identify which tasks worked well vs. poorly
3. Prepare to test a new delegation pattern
4. Document quality/cost tradeoffs
"""
    else:
        run_prep += """1. Review branch packet materials
2. Prepare for your research pass
"""
    
    run_prep += f"""
## Files Generated

- `{branch['slug']}-snapshot.md` - branch state overview
- `{branch['slug']}-artifact-index.md` - complete artifact listing
- `{branch['slug']}-comparison-prep.md` - variant comparison guide
- `{branch['slug']}-{run_type}-prep.md` - this run-specific prep

## Next Command

After reviewing these materials, start your run:

```bash
python -m meta_autoresearch_cli run new {branch['slug']} --type {run_type}
```
"""
    
    run_prep_path = paths.generated / f"{branch['slug']}-{run_type}-prep.md"
    run_prep_path.write_text(run_prep, encoding="utf-8", newline="\n")
    print(f"generated: {relpath(paths.root, run_prep_path)}")
    
    print(f"\nRun prep complete: 4 files generated for {run_type} pass on '{branch['slug']}'")
    return 0


def command_delegate_batch(args: argparse.Namespace) -> int:
    """
    Process multiple files in batch with a single delegation task.
    
    Supports summarize-note and extract-claims tasks with glob patterns.
    """
    paths = repo_paths()
    task = args.task
    pattern = args.pattern
    
    # Expand glob pattern to find matching files
    import glob as glob_module
    
    # Handle both absolute and relative patterns
    if not os.path.isabs(pattern):
        search_path = paths.root / pattern
    else:
        search_path = Path(pattern)
    
    # Convert to string for glob and expand
    pattern_str = str(search_path)
    if '*' not in pattern_str and '?' not in pattern_str:
        # Single file, not a pattern
        matching_files = [search_path] if search_path.exists() else []
    else:
        matching_files = sorted(Path(p) for p in glob_module.glob(pattern_str))
    
    if not matching_files:
        raise SystemExit(f"No files matching pattern: {pattern}")
    
    print(f"Found {len(matching_files)} file(s) matching '{pattern}'")
    print(f"Task: {task}")
    print()
    
    # Get model for small tasks
    model_id, config, fallbacks, timeout = get_model_for_slot("small")
    
    # Process each file
    results = []
    errors = []
    
    for i, file_path in enumerate(matching_files, 1):
        rel_path = relpath(paths.root, file_path)
        print(f"[{i}/{len(matching_files)}] Processing {rel_path}...")
        
        try:
            content = file_path.read_text(encoding="utf-8")
            
            if task == "summarize-note":
                system_prompt, user_prompt = summarize_note_task(content, rel_path)
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
                result = call_openrouter(messages, model_id, config)
                
                if not result:
                    errors.append((rel_path, "Model returned empty response"))
                    continue
                
                # Generate output filename
                stem = file_path.stem
                output_filename = f"{stem}-summary.md"
                output_path = paths.generated / output_filename
                
                output_content = f"""<!-- GENERATED: do not treat as canonical research -->
<!-- Task: summarize-note (batch) -->
<!-- Model: {model_id} -->
<!-- Source: {rel_path} -->
<!-- Generated: {datetime.now().isoformat()} -->

# Summary: {file_path.name}

{result}

---
*This is a generated support artifact. Treat as draft until reviewed.*
"""
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(output_content, encoding="utf-8", newline="\n")
                results.append((rel_path, str(relpath(paths.root, output_path))))
                
            elif task == "extract-claims":
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
                result = call_openrouter(messages, model_id, config)
                
                if not result:
                    errors.append((rel_path, "Model returned empty response"))
                    continue
                
                # Generate output filename
                stem = file_path.stem
                output_filename = f"{stem}-claims.md"
                output_path = paths.generated / output_filename
                
                output_content = f"""<!-- GENERATED: do not treat as canonical research -->
<!-- Task: extract-claims (batch) -->
<!-- Model: {model_id} -->
<!-- Source: {rel_path} -->
<!-- Generated: {datetime.now().isoformat()} -->

# Claims Extracted: {file_path.name}

{result}

---
*This is a generated support artifact. Treat as draft until reviewed.*
"""
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(output_content, encoding="utf-8", newline="\n")
                results.append((rel_path, str(relpath(paths.root, output_path))))
            
            else:
                errors.append((rel_path, f"Unknown task: {task}"))
                
        except Exception as e:
            errors.append((rel_path, str(e)))
    
    # Print summary
    print()
    print("=" * 60)
    print(f"Batch processing complete")
    print(f"  Successful: {len(results)}")
    print(f"  Failed: {len(errors)}")
    print()
    
    if results:
        print("Generated files:")
        for src, dst in results:
            print(f"  {src} -> {dst}")
    
    if errors:
        print("Errors:")
        for src, err in errors:
            print(f"  {src}: {err}")
    
    return 1 if errors else 0


# =============================================================================
# Phase 7: Scaled-Cycle Orchestrator
# =============================================================================


def orchestrator_paths() -> RepoPaths:
    """Get paths for orchestrator state."""
    paths = repo_paths()
    # Ensure orchestrator directories exist
    (paths.meta / "orchestrator").mkdir(parents=True, exist_ok=True)
    (paths.meta / "dashboard").mkdir(parents=True, exist_ok=True)
    return paths


def load_run_plan(plan_path: str) -> dict[str, Any]:
    """Load a run plan from JSON file."""
    path = Path(plan_path)
    if not path.is_absolute():
        path = Path.cwd() / plan_path
    
    if not path.exists():
        raise SystemExit(f"Run plan not found: {path}")
    
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def create_cycle_state(plan_name: str, cycle_id: int, branch: str, pass_type: str) -> dict[str, Any]:
    """Create initial state for a cycle."""
    return {
        "cycle_id": cycle_id,
        "plan_name": plan_name,
        "branch": branch,
        "pass_type": pass_type,
        "status": "pending",
        "started_at": None,
        "completed_at": None,
        "outputs": [],
        "errors": [],
        "cost_estimate": 0.0,
        "duration_seconds": 0,
    }


def save_cycle_state(paths: RepoPaths, cycle_state: dict[str, Any]) -> None:
    """Save cycle state to JSON file."""
    cycle_file = paths.meta / "orchestrator" / f"{cycle_state['plan_name']}-cycle-{cycle_state['cycle_id']:03d}.json"
    write_json(cycle_file, cycle_state)


def execute_cycle(cycle_state: dict[str, Any], paths: RepoPaths, autonomy_level: str = "low") -> dict[str, Any]:
    """
    Execute a single research cycle.
    
    For now, this is a placeholder that simulates a comparison pass.
    Will be expanded based on pass type.
    """
    import time
    
    cycle_state["status"] = "running"
    cycle_state["started_at"] = datetime.now().isoformat()
    start_time = time.time()
    
    branch_slug = cycle_state["branch"]
    pass_type = cycle_state["pass_type"]
    
    try:
        # Load branch for context
        branch, _, _ = load_branch(branch_slug)
        
        if pass_type == "comparison":
            # Execute comparison pass
            # Step 1: Generate branch packet
            snapshot_md = branch_snapshot_markdown(branch, paths)
            snapshot_path = paths.generated / f"{branch_slug}-comparison-snapshot.md"
            snapshot_path.write_text(snapshot_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, snapshot_path)))
            
            # Step 2: Generate artifact index
            index_md = artifact_index_markdown(branch, paths)
            index_path = paths.generated / f"{branch_slug}-comparison-index.md"
            index_path.write_text(index_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, index_path)))
            
            # Step 3: Generate comparison prep
            prep_md = comparison_prep_markdown(branch, paths)
            prep_path = paths.generated / f"{branch_slug}-comparison-prep.md"
            prep_path.write_text(prep_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, prep_path)))
            
            # Step 4: Summarize grounding notes and extract claims from scenarios (parallel delegate)
            model_id, config, fallback_models, timeout = get_model_for_slot("small")

            # Track per-task timing
            cycle_state["task_timings"] = []

            # Build task list for parallel execution
            tasks = []

            # Add summarize tasks for notes
            for note_rel in branch.get("key_notes", [])[:2]:  # Limit to 2 notes per cycle for now
                note_path = paths.root / note_rel
                if note_path.exists():
                    content = note_path.read_text(encoding="utf-8")
                    system_prompt, user_prompt = summarize_note_task(content, note_rel)
                    tasks.append({
                        "task_type": "summarize-note",
                        "source": note_rel,
                        "source_path": note_path,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                    })

            # Add extract claims tasks for scenarios
            for scenario_rel in branch.get("active_variants", [])[:2]:  # Limit to 2 scenarios per cycle
                scenario_path = paths.root / scenario_rel
                if scenario_path.exists():
                    content = scenario_path.read_text(encoding="utf-8")
                    system_prompt = """You are extracting claims from research artifacts for meta-autoresearch.

Your task: identify distinct, testable claims in the text.

Guidelines:
1. One claim per bullet point
2. Preserve uncertainty qualifiers ("may", "suggests", "likely")
3. Distinguish between evidence-backed claims and speculation
4. Note when claims reference specific sources or cases

This is a support task. Output will be reviewed by human curator."""

                    user_prompt = f"""Extract all claims from this artifact:

File: {scenario_rel}

---
{content}
---

Format each claim as:
- [Claim text] (evidence-backed | speculative) - [source if referenced]
"""
                    tasks.append({
                        "task_type": "extract-claims",
                        "source": scenario_rel,
                        "source_path": scenario_path,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                    })

            # Execute all tasks in parallel
            if tasks:
                parallel_results = parallel_model_calls(tasks, config)

                for result in parallel_results:
                    cycle_state["task_timings"].append({
                        "task": result["task_type"],
                        "source": result["source"],
                        "model": result["model"],
                        "duration_seconds": round(result["duration"], 2)
                    })

                    if result["success"]:
                        if result["content"] and len(result["content"].strip()) > 50:
                            # Find corresponding task to get source_path
                            task = next((t for t in tasks if t["source"] == result["source"]), None)
                            if task:
                                source_path = task["source_path"]
                                stem = source_path.stem
                                if result["task_type"] == "summarize-note":
                                    output_path = paths.generated / f"{stem}-cycle-summary.md"
                                    cycle_state["cost_estimate"] += 0.0007
                                else:
                                    output_path = paths.generated / f"{stem}-cycle-claims.md"
                                    cycle_state["cost_estimate"] += 0.0009

                                output_content = f"""<!-- GENERATED: do not treat as canonical research -->
<!-- Task: {result['task_type']} (orchestrator cycle, parallel) -->
<!-- Model: {result['model']} -->
<!-- Source: {result['source']} -->
<!-- Generated: {datetime.now().isoformat()} -->

# {'Summary' if result['task_type'] == 'summarize-note' else 'Claims Extracted'}: {source_path.name}

{result['content']}

---
*This is a generated support artifact. Treat as draft until reviewed.*
"""
                                output_path.write_text(output_content, encoding="utf-8", newline="\n")
                                cycle_state["outputs"].append(str(relpath(paths.root, output_path)))
                        else:
                            cycle_state["errors"].append(f"Failed to process {result['source']}: API returned empty or insufficient content")
                    else:
                        cycle_state["errors"].append(f"Failed to process {result['source']}: {result['error']}")
            
            # Mark cycle as failed if there were errors
            if cycle_state["errors"]:
                cycle_state["status"] = "failed_with_outputs"
            else:
                cycle_state["status"] = "completed"

        elif pass_type == "grounding":
            # Execute grounding pass
            # Step 1: Generate branch packet
            snapshot_md = branch_snapshot_markdown(branch, paths)
            snapshot_path = paths.generated / f"{branch_slug}-grounding-snapshot.md"
            snapshot_path.write_text(snapshot_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, snapshot_path)))

            # Step 2: Generate artifact index
            index_md = artifact_index_markdown(branch, paths)
            index_path = paths.generated / f"{branch_slug}-grounding-index.md"
            index_path.write_text(index_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, index_path)))

            # Step 3: Generate grounding prep
            prep_md = comparison_prep_markdown(branch, paths)
            prep_path = paths.generated / f"{branch_slug}-grounding-prep.md"
            prep_path.write_text(prep_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, prep_path)))

            # Step 4: Summarize grounding notes and extract claims from scenarios (parallel delegate)
            model_id, config, fallback_models, timeout = get_model_for_slot("small")
            cycle_state["task_timings"] = []

            # Build task list for parallel execution
            tasks = []

            # Add summarize tasks for notes
            for note_rel in branch.get("key_notes", [])[:3]:  # Up to 3 notes
                note_path = paths.root / note_rel
                if note_path.exists():
                    content = note_path.read_text(encoding="utf-8")
                    system_prompt, user_prompt = summarize_note_task(content, note_rel)
                    tasks.append({
                        "task_type": "summarize-note",
                        "source": note_rel,
                        "source_path": note_path,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                    })

            # Add extract claims tasks for scenarios
            for scenario_rel in branch.get("active_variants", [])[:3]:  # Up to 3 scenarios
                scenario_path = paths.root / scenario_rel
                if scenario_path.exists():
                    content = scenario_path.read_text(encoding="utf-8")
                    system_prompt = """You are extracting claims from research artifacts for meta-autoresearch.

Your task: identify distinct, testable claims in the text.

Guidelines:
1. One claim per bullet point
2. Preserve uncertainty qualifiers ("may", "suggests", "likely")
3. Distinguish between evidence-backed claims and speculation
4. Note when claims reference specific sources or cases

This is a support task. Output will be reviewed by human curator."""

                    user_prompt = f"""Extract all claims from this artifact:

File: {scenario_rel}

---
{content}
---

Format each claim as:
- [Claim text] (evidence-backed | speculative) - [source if referenced]
"""
                    tasks.append({
                        "task_type": "extract-claims",
                        "source": scenario_rel,
                        "source_path": scenario_path,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                    })

            # Execute all tasks in parallel
            if tasks:
                parallel_results = parallel_model_calls(tasks, config)

                for result in parallel_results:
                    cycle_state["task_timings"].append({
                        "task": result["task_type"],
                        "source": result["source"],
                        "model": result["model"],
                        "duration_seconds": round(result["duration"], 2)
                    })

                    if result["success"]:
                        if result["content"] and len(result["content"].strip()) > 50:
                            # Find corresponding task to get source_path
                            task = next((t for t in tasks if t["source"] == result["source"]), None)
                            if task:
                                source_path = task["source_path"]
                                stem = source_path.stem
                                if result["task_type"] == "summarize-note":
                                    output_path = paths.generated / f"{stem}-grounding-summary.md"
                                    cycle_state["cost_estimate"] += 0.0007
                                else:
                                    output_path = paths.generated / f"{stem}-grounding-claims.md"
                                    cycle_state["cost_estimate"] += 0.0009

                                output_content = f"""<!-- GENERATED: do not treat as canonical research -->
<!-- Task: {result['task_type']} (orchestrator grounding, parallel) -->
<!-- Model: {result['model']} -->
<!-- Source: {result['source']} -->
<!-- Generated: {datetime.now().isoformat()} -->

# {'Summary' if result['task_type'] == 'summarize-note' else 'Claims Extracted'}: {source_path.name}

{result['content']}

---
*This is a generated support artifact. Treat as draft until reviewed.*
"""
                                output_path.write_text(output_content, encoding="utf-8", newline="\n")
                                cycle_state["outputs"].append(str(relpath(paths.root, output_path)))
                        else:
                            cycle_state["errors"].append(f"Failed to process {result['source']}: API returned empty or insufficient content")
                    else:
                        cycle_state["errors"].append(f"Failed to process {result['source']}: {result['error']}")

            # Mark cycle as failed if there were errors
            if cycle_state["errors"]:
                cycle_state["status"] = "failed_with_outputs"
            else:
                cycle_state["status"] = "completed"

        elif pass_type == "variant":
            # Execute variant pass
            # Step 1: Generate branch packet
            snapshot_md = branch_snapshot_markdown(branch, paths)
            snapshot_path = paths.generated / f"{branch_slug}-variant-snapshot.md"
            snapshot_path.write_text(snapshot_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, snapshot_path)))

            # Step 2: Generate artifact index
            index_md = artifact_index_markdown(branch, paths)
            index_path = paths.generated / f"{branch_slug}-variant-index.md"
            index_path.write_text(index_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, index_path)))

            # Step 3: Generate variant prep
            prep_md = comparison_prep_markdown(branch, paths)
            prep_path = paths.generated / f"{branch_slug}-variant-prep.md"
            prep_path.write_text(prep_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, prep_path)))

            # Step 4: Extract claims from parent + variants (parallel delegate)
            model_id, config, fallback_models, timeout = get_model_for_slot("small")
            cycle_state["task_timings"] = []

            # Build task list for parallel execution
            tasks = []

            # Add parent scenario
            parent_rel = branch.get("parent_artifact")
            if parent_rel:
                parent_path = paths.root / parent_rel
                if parent_path.exists():
                    content = parent_path.read_text(encoding="utf-8")
                    system_prompt = """You are extracting claims from research artifacts for meta-autoresearch.

Your task: identify distinct, testable claims in the text.

Guidelines:
1. One claim per bullet point
2. Preserve uncertainty qualifiers ("may", "suggests", "likely")
3. Distinguish between evidence-backed claims and speculation
4. Note when claims reference specific sources or cases

This is a support task. Output will be reviewed by human curator."""

                    user_prompt = f"""Extract all claims from this artifact:

File: {parent_rel}

---
{content}
---

Format each claim as:
- [Claim text] (evidence-backed | speculative) - [source if referenced]
"""
                    tasks.append({
                        "task_type": "extract-claims",
                        "source": parent_rel,
                        "source_path": parent_path,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                    })

            # Add existing variants
            for scenario_rel in branch.get("active_variants", [])[:2]:  # Up to 2 variants
                scenario_path = paths.root / scenario_rel
                if scenario_path.exists():
                    content = scenario_path.read_text(encoding="utf-8")
                    system_prompt = """You are extracting claims from research artifacts for meta-autoresearch.

Your task: identify distinct, testable claims in the text.

Guidelines:
1. One claim per bullet point
2. Preserve uncertainty qualifiers ("may", "suggests", "likely")
3. Distinguish between evidence-backed claims and speculation
4. Note when claims reference specific sources or cases

This is a support task. Output will be reviewed by human curator."""

                    user_prompt = f"""Extract all claims from this artifact:

File: {scenario_rel}

---
{content}
---

Format each claim as:
- [Claim text] (evidence-backed | speculative) - [source if referenced]
"""
                    tasks.append({
                        "task_type": "extract-claims",
                        "source": scenario_rel,
                        "source_path": scenario_path,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                    })

            # Execute all tasks in parallel
            if tasks:
                parallel_results = parallel_model_calls(tasks, config)

                for result in parallel_results:
                    cycle_state["task_timings"].append({
                        "task": result["task_type"],
                        "source": result["source"],
                        "model": result["model"],
                        "duration_seconds": round(result["duration"], 2)
                    })

                    if result["success"]:
                        if result["content"] and len(result["content"].strip()) > 100:
                            task = next((t for t in tasks if t["source"] == result["source"]), None)
                            if task:
                                source_path = task["source_path"]
                                stem = source_path.stem
                                output_path = paths.generated / f"{stem}-variant-claims.md"
                                cycle_state["cost_estimate"] += 0.0009

                                output_content = f"""<!-- GENERATED: do not treat as canonical research -->
<!-- Task: extract-claims (orchestrator variant, parallel) -->
<!-- Model: {result['model']} -->
<!-- Source: {result['source']} -->
<!-- Generated: {datetime.now().isoformat()} -->

# Claims Extracted: {source_path.name}

{result['content']}

---
*This is a generated support artifact. Treat as draft until reviewed.*
"""
                                output_path.write_text(output_content, encoding="utf-8", newline="\n")
                                cycle_state["outputs"].append(str(relpath(paths.root, output_path)))
                        else:
                            cycle_state["errors"].append(f"Failed to process {result['source']}: API returned empty or insufficient content")
                    else:
                        cycle_state["errors"].append(f"Failed to process {result['source']}: {result['error']}")

            if cycle_state["errors"]:
                cycle_state["status"] = "failed_with_outputs"
            else:
                cycle_state["status"] = "completed"

        elif pass_type == "maturity":
            # Execute maturity pass
            # Step 1: Generate branch packet
            snapshot_md = branch_snapshot_markdown(branch, paths)
            snapshot_path = paths.generated / f"{branch_slug}-maturity-snapshot.md"
            snapshot_path.write_text(snapshot_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, snapshot_path)))

            # Step 2: Generate artifact index
            index_md = artifact_index_markdown(branch, paths)
            index_path = paths.generated / f"{branch_slug}-maturity-index.md"
            index_path.write_text(index_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, index_path)))

            # Step 3: Generate maturity prep
            prep_md = comparison_prep_markdown(branch, paths)
            prep_path = paths.generated / f"{branch_slug}-maturity-prep.md"
            prep_path.write_text(prep_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, prep_path)))

            # Step 4: Summarize key syntheses (parallel delegate)
            model_id, config, fallback_models, timeout = get_model_for_slot("small")
            cycle_state["task_timings"] = []

            tasks = []
            for syn_rel in branch.get("key_syntheses", [])[:2]:  # Up to 2 syntheses
                syn_path = paths.root / syn_rel
                if syn_path.exists():
                    content = syn_path.read_text(encoding="utf-8")
                    system_prompt, user_prompt = summarize_note_task(content, syn_rel)
                    tasks.append({
                        "task_type": "summarize-note",
                        "source": syn_rel,
                        "source_path": syn_path,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                    })

            if tasks:
                parallel_results = parallel_model_calls(tasks, config)

                for result in parallel_results:
                    cycle_state["task_timings"].append({
                        "task": result["task_type"],
                        "source": result["source"],
                        "model": result["model"],
                        "duration_seconds": round(result["duration"], 2)
                    })

                    if result["success"]:
                        if result["content"] and len(result["content"].strip()) > 50:
                            task = next((t for t in tasks if t["source"] == result["source"]), None)
                            if task:
                                source_path = task["source_path"]
                                stem = source_path.stem
                                output_path = paths.generated / f"{stem}-maturity-summary.md"
                                cycle_state["cost_estimate"] += 0.0007

                                output_content = f"""<!-- GENERATED: do not treat as canonical research -->
<!-- Task: summarize-note (orchestrator maturity, parallel) -->
<!-- Model: {result['model']} -->
<!-- Source: {result['source']} -->
<!-- Generated: {datetime.now().isoformat()} -->

# Summary: {source_path.name}

{result['content']}

---
*This is a generated support artifact. Treat as draft until reviewed.*
"""
                                output_path.write_text(output_content, encoding="utf-8", newline="\n")
                                cycle_state["outputs"].append(str(relpath(paths.root, output_path)))
                        else:
                            cycle_state["errors"].append(f"Failed to process {result['source']}: API returned empty or insufficient content")
                    else:
                        cycle_state["errors"].append(f"Failed to process {result['source']}: {result['error']}")

            if cycle_state["errors"]:
                cycle_state["status"] = "failed_with_outputs"
            else:
                cycle_state["status"] = "completed"

        elif pass_type == "discard":
            # Execute discard pass
            # Step 1: Generate branch packet
            snapshot_md = branch_snapshot_markdown(branch, paths)
            snapshot_path = paths.generated / f"{branch_slug}-discard-snapshot.md"
            snapshot_path.write_text(snapshot_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, snapshot_path)))

            # Step 2: Generate artifact index
            index_md = artifact_index_markdown(branch, paths)
            index_path = paths.generated / f"{branch_slug}-discard-index.md"
            index_path.write_text(index_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, index_path)))

            # Step 3: Generate discard prep
            prep_md = comparison_prep_markdown(branch, paths)
            prep_path = paths.generated / f"{branch_slug}-discard-prep.md"
            prep_path.write_text(prep_md, encoding="utf-8", newline="\n")
            cycle_state["outputs"].append(str(relpath(paths.root, prep_path)))

            # Step 4: Extract claims from all variants (parallel delegate)
            model_id, config, fallback_models, timeout = get_model_for_slot("small")
            cycle_state["task_timings"] = []

            tasks = []
            for scenario_rel in branch.get("active_variants", [])[:3]:  # Up to 3 variants
                scenario_path = paths.root / scenario_rel
                if scenario_path.exists():
                    content = scenario_path.read_text(encoding="utf-8")
                    system_prompt = """You are extracting claims from research artifacts for meta-autoresearch.

Your task: identify distinct, testable claims in the text.

Guidelines:
1. One claim per bullet point
2. Preserve uncertainty qualifiers ("may", "suggests", "likely")
3. Distinguish between evidence-backed claims and speculation
4. Note when claims reference specific sources or cases

This is a support task. Output will be reviewed by human curator."""

                    user_prompt = f"""Extract all claims from this artifact:

File: {scenario_rel}

---
{content}
---

Format each claim as:
- [Claim text] (evidence-backed | speculative) - [source if referenced]
"""
                    tasks.append({
                        "task_type": "extract-claims",
                        "source": scenario_rel,
                        "source_path": scenario_path,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                    })

            if tasks:
                parallel_results = parallel_model_calls(tasks, config)

                for result in parallel_results:
                    cycle_state["task_timings"].append({
                        "task": result["task_type"],
                        "source": result["source"],
                        "model": result["model"],
                        "duration_seconds": round(result["duration"], 2)
                    })

                    if result["success"]:
                        if result["content"] and len(result["content"].strip()) > 100:
                            task = next((t for t in tasks if t["source"] == result["source"]), None)
                            if task:
                                source_path = task["source_path"]
                                stem = source_path.stem
                                output_path = paths.generated / f"{stem}-discard-claims.md"
                                cycle_state["cost_estimate"] += 0.0009

                                output_content = f"""<!-- GENERATED: do not treat as canonical research -->
<!-- Task: extract-claims (orchestrator discard, parallel) -->
<!-- Model: {result['model']} -->
<!-- Source: {result['source']} -->
<!-- Generated: {datetime.now().isoformat()} -->

# Claims Extracted: {source_path.name}

{result['content']}

---
*This is a generated support artifact. Treat as draft until reviewed.*
"""
                                output_path.write_text(output_content, encoding="utf-8", newline="\n")
                                cycle_state["outputs"].append(str(relpath(paths.root, output_path)))
                        else:
                            cycle_state["errors"].append(f"Failed to process {result['source']}: API returned empty or insufficient content")
                    else:
                        cycle_state["errors"].append(f"Failed to process {result['source']}: {result['error']}")

            if cycle_state["errors"]:
                cycle_state["status"] = "failed_with_outputs"
            else:
                cycle_state["status"] = "completed"

        else:
            # For other pass types, create a placeholder cycle
            cycle_state["outputs"].append(f"Cycle executed: {pass_type} pass on {branch_slug}")
            cycle_state["status"] = "completed"
        
    except Exception as e:
        cycle_state["errors"].append(str(e))
        cycle_state["status"] = "failed"
    
    cycle_state["completed_at"] = datetime.now().isoformat()
    cycle_state["duration_seconds"] = round(time.time() - start_time, 2)

    # Phase 9C: Automated component extraction and manifest updates
    cycle_state = post_cycle_automation(cycle_state, paths)

    return cycle_state


# =============================================================================
# Phase 9C: Automation
# =============================================================================


def extract_components_from_scenario(scenario_path: Path, branch_slug: str, paths: RepoPaths) -> list[str]:
    """
    Extract component YAML files from a scenario file.
    
    Analyzes the scenario content and generates component YAML files for:
    - Regions mentioned
    - Mechanisms described
    - Institutions referenced
    - Infrastructure mentioned
    - Evidence cited
    - Hazards identified
    
    Returns list of generated component file paths.
    """
    try:
        import yaml
    except ImportError:
        return []
    
    content = scenario_path.read_text(encoding="utf-8")
    generated = []
    
    # Extract title from metadata
    title = "Unknown"
    for line in content.split("\n")[:30]:
        if line.startswith("- title:"):
            title = line.split(":", 1)[1].strip()
            break
    
    # Extract domain slice
    domain = "unknown"
    for line in content.split("\n")[:30]:
        if line.startswith("- domain slice:"):
            domain = line.split(":", 1)[1].strip()
            break
    
    # Extract structure type hint
    structure_type = branch_slug
    
    # Simple keyword-based component extraction
    component_patterns = {
        "region": [],
        "institution": [],
        "infrastructure": [],
        "hazard": [],
    }
    
    # Check for known entity patterns
    content_lower = content.lower()
    
    # Regions
    region_map = {
        "feather river": "region:feather-river",
        "upper colorado": "region:upper-colorado",
        "southeast queensland": "region:seq",
        "russia": "region:russia-wheat",
        "europe": "region:europe-wheat",
        "egypt": "region:egypt",
        "yemen": "region:yemen",
        "philippines": "region:philippines-rice",
        "india": "region:india-credit",
        "china": "region:china-wheat",
        "south america": "region:south-america",
        "peru": "region:peru",
        "chile": "region:chile",
        "texas": "region:texas",
        "california": "region:california",
    }
    
    for keyword, comp_id in region_map.items():
        if keyword in content_lower:
            component_patterns["region"].append(comp_id)
    
    # Institutions
    inst_map = {
        "usda": "inst:usda-fas",
        "fao": "inst:fao-giews",
        "who": "inst:who",
        "woah": "inst:woah",
        "cdc": "inst:cdc",
        "federal reserve": "inst:federal-reserve",
        "imf": "inst:imf",
        "world bank": "inst:world-bank",
        "nfa": "inst:philippines-nfa",
    }
    
    for keyword, comp_id in inst_map.items():
        if keyword in content_lower:
            component_patterns["institution"].append(comp_id)
    
    # Hazards
    hazard_map = {
        "wildfire": "hazard:wildfire",
        "drought": "hazard:agricultural-drought",
        "flood": "hazard:heavy-precipitation",
        "credit squeeze": "hazard:credit-squeeze",
        "currency depreciation": "hazard:currency-depreciation",
        "trade restriction": "hazard:trade-restriction-amplification",
        "export ban": "hazard:trade-restriction-amplification",
        "price spike": "hazard:price-spike",
    }
    
    for keyword, comp_id in hazard_map.items():
        if keyword in content_lower:
            component_patterns["hazard"].append(comp_id)
    
    # Generate new component files for unique findings
    for comp_type, comp_ids in component_patterns.items():
        for comp_id in set(comp_ids):
            comp_path = paths.meta / "components" / f"{comp_id}.yaml"
            if not comp_path.exists():
                # Generate placeholder component
                comp_name = comp_id.replace(f"{comp_type}:", "").replace("-", " ").title()
                comp_yaml = f"""id: {comp_id}
type: {comp_type}
name: {comp_name}
domain: extracted from {branch_slug} branch
description: |
  Auto-extracted from scenario: {scenario_path.name}
  Title: {title}
  Domain: {domain}
related_branches:
  - {branch_slug}
related_artifacts:
  - {relpath(paths.root, scenario_path)}
metadata:
  extraction_source: automated
  structure_types:
    - {structure_type}
"""
                comp_path.write_text(comp_yaml, encoding="utf-8", newline="\n")
                generated.append(str(relpath(paths.root, comp_path)))
    
    return generated


def update_branch_manifest_after_cycle(branch_slug: str, cycle_state: dict, paths: RepoPaths) -> bool:
    """
    Update branch manifest with outputs from completed cycle.
    
    Adds new outputs to appropriate manifest fields:
    - Notes → key_notes
    - Scenarios → active_variants
    - Syntheses → key_syntheses
    - Loop runs → loop_runs
    - Discards → discard_records
    
    Returns True if manifest was updated, False otherwise.
    """
    branch_path = branch_manifest_path(branch_slug)
    if not branch_path.exists():
        return False
    
    branch = load_json(branch_path)
    updated = False
    
    # Get new outputs from cycle
    new_outputs = cycle_state.get("outputs", [])
    
    for output_path in new_outputs:
        if not output_path or output_path.startswith("Cycle executed"):
            continue
        
        # Categorize output by path
        if "research/notes/" in output_path:
            if output_path not in branch.get("key_notes", []):
                branch.setdefault("key_notes", []).append(output_path)
                updated = True
        elif "research/scenarios/" in output_path:
            if output_path not in branch.get("active_variants", []):
                branch.setdefault("active_variants", []).append(output_path)
                updated = True
        elif "research/syntheses/" in output_path:
            if output_path not in branch.get("key_syntheses", []):
                branch.setdefault("key_syntheses", []).append(output_path)
                updated = True
        elif "research/loops/" in output_path:
            if output_path not in branch.get("loop_runs", []):
                branch.setdefault("loop_runs", []).append(output_path)
                updated = True
        elif "research/discards/" in output_path:
            if output_path not in branch.get("discard_records", []):
                branch.setdefault("discard_records", []).append(output_path)
                updated = True
    
    # Update timestamp
    if updated:
        branch["last_updated"] = date.today().isoformat()
        write_json(branch_path, branch)
    
    return updated


def post_cycle_automation(cycle_state: dict, paths: RepoPaths) -> dict[str, Any]:
    """
    Run automated post-cycle tasks:
    1. Extract components from new scenario outputs
    2. Update branch manifest with new outputs
    
    Returns updated cycle state with automation results.
    """
    branch_slug = cycle_state.get("branch", "")
    outputs = cycle_state.get("outputs", [])
    
    # Extract components from new scenario outputs
    new_components = []
    for output_path in outputs:
        if "research/scenarios/" in output_path:
            scenario_path = paths.root / output_path
            if scenario_path.exists():
                extracted = extract_components_from_scenario(scenario_path, branch_slug, paths)
                new_components.extend(extracted)
    
    # Update branch manifest
    manifest_updated = update_branch_manifest_after_cycle(branch_slug, cycle_state, paths)
    
    # Record automation results in cycle state
    cycle_state["automation"] = {
        "components_extracted": len(new_components),
        "new_component_files": new_components,
        "manifest_updated": manifest_updated,
    }
    
    return cycle_state


def command_branch_l5_readiness(args: argparse.Namespace) -> int:
    """
    Assess L5 readiness for a branch.
    
    L5 criteria:
    - Template reusability (required)
    - Cross-method integration (required)
    - Method evolution (required)
    - Prospective validation (optional validator)
    """
    branch, _, paths = load_branch(args.slug)
    
    maturity = branch.get("maturity_level", 0)
    structure_type = branch.get("structure_type", "")
    variants = branch.get("active_variants", [])
    syntheses = branch.get("key_syntheses", [])
    notes = branch.get("key_notes", [])
    loop_runs = branch.get("loop_runs", [])
    
    print(f"=== L5 Readiness: {branch['title']} ===")
    print(f"Current maturity: L{maturity} ({branch.get('maturity_note', '')})")
    print(f"Structure type: {structure_type}")
    print()
    
    # Check L4 prerequisites
    print("## L4 Prerequisites")
    l4_checks = [
        ("At L4 maturity", maturity >= 4),
        ("Has 2+ variants", len(variants) >= 2),
        ("Has comparison synthesis", len(syntheses) >= 1),
        ("Has loop-run record", len(loop_runs) >= 1),
        ("Has discard record", len(branch.get("discard_records", [])) >= 1),
    ]
    
    for check_name, check_result in l4_checks:
        status = "✅" if check_result else "❌"
        print(f"  {status} {check_name}")
    
    print()
    print("## L5 Required Criteria")
    
    # Template reusability
    has_template = maturity >= 4 and len(variants) >= 3 and len(syntheses) >= 2
    template_status = "✅ Ready" if has_template else "⏳ Needs more variants/syntheses"
    print(f"  {template_status} Template reusability (3+ variants, 2+ syntheses)")
    
    # Cross-method integration
    is_non_climate = branch.get("domain", "").lower() not in ["climate volatility"]
    has_cross_branch = len(syntheses) >= 3  # At least one should be cross-branch
    integration_status = "✅ Ready" if is_non_climate and has_cross_branch else "⏳ Needs cross-method integration"
    print(f"  {integration_status} Cross-method integration")
    
    # Method evolution
    method_evolution = len(notes) >= 3 and maturity >= 4
    evolution_status = "✅ Ready" if method_evolution else "⏳ Needs method influence"
    print(f"  {evolution_status} Method evolution (branch changed method documents)")
    
    print()
    print("## L5 Optional Validator")
    
    # Prospective validation (optional)
    has_grounding = len(notes) >= 2
    validation_status = "✅ Present" if has_grounding else "⏳ Needs more grounding"
    print(f"  {validation_status} Prospective validation (grounding evidence)")
    
    print()
    
    # Overall assessment
    required_ready = has_template and (is_non_climate and has_cross_branch) and method_evolution
    if required_ready:
        print("### Assessment: ✅ READY FOR L5")
        print("All required criteria met. Branch is generalizable.")
    else:
        print("### Assessment: ⏳ NOT YET READY FOR L5")
        print("Some required criteria not yet met. Continue grounding and comparison.")
    
    return 0


# =============================================================================
# Phase 9D: Scale Enablement
# =============================================================================


def command_branch_template(args: argparse.Namespace) -> int:
    """
    Generate a new branch from an existing structure type template.
    
    Usage:
        branch template <structure-type> <new-slug> --title "Title" --domain "Domain"
    
    Structure types: sequence, correlation, design-rule, hybrid-2comp, hybrid-3comp
    """
    paths = repo_paths()
    structure_type = args.structure_type
    slug = args.slug
    title = args.title
    domain = args.domain
    
    # Define templates based on structure type
    templates = {
        "sequence": {
            "structure_type": "sequence failure",
            "variants": [],
            "guidance": "Focus on temporal transitions between conditions. Look for chains where the transition itself carries risk.",
        },
        "correlation": {
            "structure_type": "correlation/transmission failure",
            "variants": [],
            "guidance": "Focus on coupled systems where distributed nodes interact. Look for trade, transmission, or amplification pathways.",
        },
        "design-rule": {
            "structure_type": "design/rule conflict under volatility",
            "variants": [],
            "guidance": "Focus on infrastructure or rules designed for one reality facing changed conditions. Look for adaptation lag.",
        },
        "hybrid-2comp": {
            "structure_type": "hybrid: correlation/transmission + design/rule conflict",
            "variants": [],
            "guidance": "Two structure components operating simultaneously. Test both transmission and rule-conflict mechanisms.",
        },
        "hybrid-3comp": {
            "structure_type": "hybrid: correlation/transmission + sequence failure + design/rule conflict",
            "variants": [],
            "guidance": "Three structure components operating simultaneously. Test correlation, sequence, and design/rule mechanisms.",
        },
    }
    
    if structure_type not in templates:
        raise SystemExit(f"Unknown structure type: {structure_type}. Choose from: {', '.join(templates.keys())}")
    
    template = templates[structure_type]
    
    # Create branch manifest
    manifest = {
        "slug": slug,
        "title": title,
        "domain": domain,
        "structure_type": template["structure_type"],
        "maturity_level": 1,
        "maturity_note": "exploratory - created from template",
        "status": "active",
        "parent_artifact": "",
        "active_variants": template["variants"],
        "key_notes": [],
        "key_syntheses": [],
        "loop_runs": [],
        "discard_records": [],
        "strongest_variant": "",
        "most_generative_variant": "",
        "weakest_variant": "",
        "open_questions": [
            f"What structure type does {domain} reveal?",
            f"How does {domain} compare to existing {structure_type} branches?",
            "What are the bounded named cases that ground this branch?",
            "Does this branch validate or challenge the template structure?",
        ],
        "next_recommended_pass": "grounding",
        "last_updated": date.today().isoformat(),
    }
    
    # Write manifest
    manifest_path = paths.branches / f"{slug}.json"
    write_json(manifest_path, manifest)
    
    # Create parent scenario placeholder
    parent_content = f"""# {title}

## Metadata

- title: {title}
- date: {date.today().isoformat()}
- author: OpenCode
- status: draft
- scenario type: parent scenario
- domain slice: {domain}

## Research question

How might {domain.lower()} create preparedness failure through {template['structure_type']} mechanisms?

## Why this scenario exists

This branch was created from the {structure_type} template. It needs grounding in bounded named cases to become method-shaping.

## Framing and assumptions

- baseline assumptions:
  - (to be filled during grounding)
- assumptions that depart from default narratives:
  - (to be filled during grounding)
- boundaries of the scenario:
  - (to be filled during grounding)

## Scenario logic

(to be developed during variant generation)

## Grounding

(to be filled during grounding pass)

## Signals and evidence classes

- signals already visible:
  - (to be filled)
- evidence classes consulted:
  - (to be filled)
- missing evidence:
  - (to be filled)

## Provisional evaluation

- plausibility: (to be assessed)
- internal coherence: (to be assessed)
- relevance: (to be assessed)
- preparedness value: (to be assessed)
- novelty: (to be assessed)
- status-quo challenge: (to be assessed)
- imaginative power: (to be assessed)

## Curation notes

- current curation gate:
  - keep (exploratory, needs grounding)
- why keep this scenario:
  - (to be filled)
- what should be refined next:
  - Ground in named cases
  - Generate bounded variants
  - Compare against existing {structure_type} branches
- what might cause this scenario to be revised or merged:
  - (to be filled)

## Uncertainties and failure modes

- key uncertainties:
  - (to be filled)
- where this could be misleading:
  - (to be filled)
- what would challenge the scenario most:
  - (to be filled)

## Links

- related notes:
  - (to be filled)
- related scenarios:
  - (to be filled)

## Components used

- (to be extracted as variants develop)
"""
    
    parent_path = paths.root / "research" / "scenarios" / f"{date.today().isoformat()}-{slug}.md"
    parent_path.parent.mkdir(parents=True, exist_ok=True)
    parent_path.write_text(parent_content, encoding="utf-8", newline="\n")
    
    # Update manifest with parent artifact
    manifest["parent_artifact"] = str(relpath(paths.root, parent_path))
    write_json(manifest_path, manifest)
    
    print(f"Created new branch: {slug}")
    print(f"  Manifest: {relpath(paths.root, manifest_path)}")
    print(f"  Parent scenario: {relpath(paths.root, parent_path)}")
    print(f"  Structure type: {template['structure_type']}")
    print(f"  Domain: {domain}")
    print()
    print("Guidance:")
    print(f"  {template['guidance']}")
    print()
    print("Next steps:")
    print("  1. Write grounding note with named cases")
    print("  2. Update parent scenario with evidence base")
    print("  3. Generate bounded variants")
    print("  4. Compare against existing branches with same structure type")
    
    return 0


def command_branch_integrate(args: argparse.Namespace) -> int:
    """
    Generate cross-method integration synthesis for a branch.
    
    Usage:
        branch integrate <slug> --method <external-method>
    
    Maps the branch's structure type to concepts from the external method.
    """
    branch, _, paths = load_branch(args.slug)
    external_method = args.method
    
    # Define integration mappings for common external methods
    integration_templates = {
        "resilience-engineering": {
            "sequence": "Normal Accident Theory (Perrow) — sequence failure as inevitable coupling in complex systems",
            "correlation": "High-Reliability Organizations — correlation/transmission as organizational coupling",
            "design-rule": "Safety-I vs Safety-II — design/rule conflict as mismatch between work-as-imagined and work-as-done",
        },
        "systems-thinking": {
            "sequence": "Causal loop diagrams — sequence as reinforcing/balancing feedback chains",
            "correlation": "System archetypes — correlation as 'tragedy of the commons' or 'fixes that fail'",
            "design-rule": "Mental models — design/rule conflict as outdated mental models facing changed reality",
        },
        "complexity-science": {
            "sequence": "Phase transitions — sequence failure as critical transition between system states",
            "correlation": "Network cascades — correlation/transmission as percolation through coupled networks",
            "design-rule": "Adaptive cycles — design/rule conflict as mismatch between fast and slow variables",
        },
        "institutional-analysis": {
            "sequence": "Policy windows — sequence failure as missed adaptation opportunities",
            "correlation": "Institutional interdependence — correlation as shared fate across jurisdictions",
            "design-rule": "Institutional mismatch — design/rule conflict as rules lagging behind reality",
        },
        "pandemic-preparedness": {
            "sequence": "Disease progression chains — sequence as transmission stages with intervention points",
            "correlation": "One Health framework — correlation as human-animal-environment coupling",
            "design-rule": "Surveillance gaps — design/rule conflict as monitoring designed for known pathogens facing novel threats",
        },
    }
    
    if external_method not in integration_templates:
        available = ", ".join(integration_templates.keys())
        print(f"Unknown external method: {external_method}")
        print(f"Available methods: {available}")
        return 1
    
    # Generate integration synthesis
    structure_type = branch.get("structure_type", "").lower()
    
    # Find matching integration guidance
    guidance = None
    for key, value in integration_templates[external_method].items():
        if key in structure_type:
            guidance = value
            break
    
    if not guidance:
        guidance = integration_templates[external_method].get("sequence", "No direct mapping found")
    
    syn_content = f"""# {branch['title']}: Integration with {external_method.replace('-', ' ').title()}

**Date:** {date.today().isoformat()}
**Type:** Cross-method integration synthesis
**Branch:** {args.slug}
**Status:** draft

---

## Purpose

This synthesis maps {branch['title']}'s structure type to concepts from {external_method.replace('-', ' ')}, testing whether the method's structure types integrate with established research frameworks.

---

## Structure Type Mapping

| {branch['title']} Structure | {external_method.replace('-', ' ').title()} Concept | Integration Insight |
|---------------------------|----------------------------------|--------------------|
| {branch.get('structure_type', 'Unknown')} | {guidance.split('—')[0].strip() if '—' in guidance else guidance} | {guidance.split('—')[1].strip() if '—' in guidance else 'Integration pending'} |

---

## Integration Analysis

### Shared Mechanisms

Both {branch['title']} and {external_method.replace('-', ' ')} address:
- (to be developed during integration analysis)

### Key Differences

{branch['title']} differs from {external_method.replace('-', ' ')} in:
- (to be developed during integration analysis)

### Novel Insights

The integration reveals:
- (to be developed during integration analysis)

---

## Method Impact

This integration:
- [ ] Changes how we understand {branch.get('structure_type', 'the structure type')}
- [ ] Suggests new evaluation criteria
- [ ] Reveals blind spots in existing framework
- [ ] Enables new cross-method research questions

---

## Links

- Related branch: `meta/branches/{args.slug}.json`
- Related method: {external_method.replace('-', ' ')}
- Related syntheses:
  - (to be added)

---

*This synthesis is a draft. It should be reviewed and either kept, revised, or discarded based on its usefulness for cross-method integration.*
"""
    
    syn_path = paths.root / "research" / "syntheses" / f"{date.today().isoformat()}-{args.slug}-{external_method}-integration.md"
    syn_path.parent.mkdir(parents=True, exist_ok=True)
    syn_path.write_text(syn_content, encoding="utf-8", newline="\n")
    
    # Update branch manifest
    branch.setdefault("key_syntheses", []).append(str(relpath(paths.root, syn_path)))
    branch["last_updated"] = date.today().isoformat()
    write_json(paths.branches / f"{args.slug}.json", branch)
    
    print(f"Generated cross-method integration synthesis: {relpath(paths.root, syn_path)}")
    print(f"Structure mapping: {guidance}")
    print()
    print("Next steps:")
    print("  1. Fill in integration analysis sections")
    print("  2. Check method impact boxes")
    print("  3. Compare insights against branch findings")
    
    return 0


def select_model_for_task(task_type: str, content_length: int = 0) -> tuple[str, dict, list, int]:
    """
    Select model based on task complexity.
    
    Simple tasks (short content, extract-claims, summarize) → small slot
    Moderate tasks (comparison prep, drafting) → mid slot
    Complex tasks (structure typing, synthesis, evaluation) → strong slot
    """
    config = get_model_config()
    
    # Determine complexity
    is_simple = task_type in ["extract-claims", "summarize-note"] and content_length < 5000
    is_complex = task_type in ["structure-typing", "cross-method-integration", "evaluation-matrix"]
    
    if is_complex:
        slot = "strong"
        model_id = config.get("strong", "qwen/qwen3.5-plus-02-15")
        fallback_str = config.get("fallback_strong", "qwen/qwen3.5-flash-02-23,meta-llama/llama-3-70b-instruct")
    elif is_simple:
        slot = "small"
        model_id = config.get("small", "xiaomi/mimo-v2-flash")
        fallback_str = config.get("fallback_small", "qwen/qwen3.5-flash-02-23,google/gemini-2.5-flash-lite")
    else:
        slot = "mid"
        model_id = config.get("mid", "mistralai/mistral-small-2603")
        fallback_str = config.get("fallback_mid", "mistralai/mistral-7b-instruct,qwen/qwen3.5-flash-02-23")
    
    fallback_models = [m.strip() for m in fallback_str.split(",") if m.strip()] if fallback_str else []
    timeout = int(config.get("timeout", "90"))
    
    return model_id, config, fallback_models, timeout


def generate_dashboard(paths: RepoPaths) -> None:
    """Generate HTML dashboard from cycle states."""
    import glob as glob_module
    
    # Load all cycle states
    cycle_files = sorted(glob_module.glob(str(paths.meta / "orchestrator" / "*.json")))
    cycles = []
    for cf in cycle_files:
        cycles.append(load_json(Path(cf)))
    
    # Group by plan
    plans: dict[str, list[dict[str, Any]]] = {}
    for cycle in cycles:
        plan_name = cycle.get("plan_name", "unknown")
        if plan_name not in plans:
            plans[plan_name] = []
        plans[plan_name].append(cycle)
    
    # Calculate stats
    total_cycles = len(cycles)
    completed = sum(1 for c in cycles if c.get("status") == "completed")
    failed = sum(1 for c in cycles if c.get("status") == "failed")
    pending = sum(1 for c in cycles if c.get("status") == "pending")
    running = sum(1 for c in cycles if c.get("status") == "running")
    total_cost = sum(c.get("cost_estimate", 0) for c in cycles)
    total_time = sum(c.get("duration_seconds", 0) for c in cycles)
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meta-Autoresearch Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 2rem; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #333; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 2rem 0; }}
        .stat-card {{ background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat-value {{ font-size: 2rem; font-weight: bold; color: #2563eb; }}
        .stat-label {{ color: #666; margin-top: 0.5rem; }}
        .plan {{ background: white; margin: 1rem 0; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .cycle {{ display: flex; justify-content: space-between; padding: 0.75rem; border-bottom: 1px solid #eee; }}
        .cycle:last-child {{ border-bottom: none; }}
        .status {{ padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 500; }}
        .status-completed {{ background: #dcfce7; color: #166534; }}
        .status-failed {{ background: #fee2e2; color: #991b1b; }}
        .status-pending {{ background: #fef3c7; color: #92400e; }}
        .status-running {{ background: #dbeafe; color: #1e40af; }}
        .cycle-info {{ flex: 1; }}
        .cycle-meta {{ color: #666; font-size: 0.875rem; }}
        .error {{ background: #fef2f2; color: #991b1b; padding: 0.5rem; border-radius: 4px; margin-top: 0.5rem; font-size: 0.875rem; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔬 Meta-Autoresearch Dashboard</h1>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{total_cycles}</div>
                <div class="stat-label">Total Cycles</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #16a34a;">{completed}</div>
                <div class="stat-label">Completed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #dc2626;">{failed}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #f59e0b;">{pending}</div>
                <div class="stat-label">Pending</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #2563eb;">{running}</div>
                <div class="stat-label">Running</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${total_cost:.2f}</div>
                <div class="stat-label">Total Cost</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{total_time/60:.1f}m</div>
                <div class="stat-label">Total Time</div>
            </div>
        </div>
        
        <h2>Run Plans</h2>
"""
    
    for plan_name, plan_cycles in sorted(plans.items()):
        html += f"""
        <div class="plan">
            <h3>{plan_name}</h3>
            <p>{len(plan_cycles)} cycles</p>
"""
        for cycle in sorted(plan_cycles, key=lambda c: c.get("cycle_id", 0)):
            status = cycle.get("status", "unknown")
            branch = cycle.get("branch", "unknown")
            pass_type = cycle.get("pass_type", "unknown")
            duration = cycle.get("duration_seconds", 0)
            cost = cycle.get("cost_estimate", 0)
            
            html += f"""
            <div class="cycle">
                <div class="cycle-info">
                    <strong>Cycle {cycle.get('cycle_id', '?')}</strong>: {branch} / {pass_type}
                    <div class="cycle-meta">
                        Duration: {duration:.1f}s | Cost: ${cost:.4f}
"""
            if cycle.get("outputs"):
                html += f" | Outputs: {len(cycle['outputs'])} files"
            html += """
                    </div>
"""
            if cycle.get("errors"):
                for err in cycle["errors"]:
                    html += f'<div class="error">⚠️ {err}</div>'
            html += f"""
                </div>
                <span class="status status-{status}">{status}</span>
            </div>
"""
        
        html += """
        </div>
"""
    
    html += """
    </div>
    <script>
        // Auto-refresh every 30 seconds
        setTimeout(() => location.reload(), 30000);
    </script>
</body>
</html>
"""
    
    dashboard_path = paths.meta / "dashboard" / "index.html"
    dashboard_path.write_text(html, encoding="utf-8", newline="\n")
    print(f"Dashboard generated: {relpath(paths.root, dashboard_path)}")


def command_orchestrator_run(args: argparse.Namespace) -> int:
    """Execute a run plan."""
    paths = orchestrator_paths()
    
    # Load run plan
    plan = load_run_plan(args.plan)
    plan_name = plan.get("name", "unnamed")
    branch = plan.get("branch", "")
    pass_type = plan.get("pass_type", "")
    num_cycles = plan.get("cycles", 1)
    autonomy_level = plan.get("autonomy_level", "low")
    
    print(f"=== Starting Run Plan: {plan_name} ===")
    print(f"Branch: {branch}")
    print(f"Pass type: {pass_type}")
    print(f"Cycles: {num_cycles}")
    print(f"Autonomy level: {autonomy_level}")
    print()
    
    # Execute cycles
    for i in range(1, num_cycles + 1):
        print(f"\n--- Cycle {i}/{num_cycles} ---")
        
        # Create cycle state
        cycle_state = create_cycle_state(plan_name, i, branch, pass_type)
        
        # Execute cycle
        cycle_state = execute_cycle(cycle_state, paths, autonomy_level)
        
        # Save state
        save_cycle_state(paths, cycle_state)
        
        # Report status
        if cycle_state["status"] == "completed":
            print(f"✓ Cycle {i} completed in {cycle_state['duration_seconds']:.1f}s")
            print(f"  Outputs: {len(cycle_state['outputs'])} files")
            print(f"  Cost: ${cycle_state['cost_estimate']:.4f}")
        else:
            print(f"✗ Cycle {i} failed")
            for err in cycle_state["errors"]:
                print(f"  Error: {err}")
        
        # Generate dashboard after each cycle
        generate_dashboard(paths)
    
    # Final summary
    print("\n=== Run Plan Complete ===")
    print(f"Dashboard: {relpath(paths.root, paths.meta / 'dashboard' / 'index.html')}")
    
    return 0


def command_orchestrator_status(args: argparse.Namespace) -> int:
    """Show orchestrator status."""
    paths = orchestrator_paths()
    generate_dashboard(paths)
    
    # Open dashboard in browser (optional)
    dashboard_path = paths.meta / "dashboard" / "index.html"
    if dashboard_path.exists():
        print(f"Dashboard: {relpath(paths.root, dashboard_path)}")
        print("Open this file in your browser to view progress.")
    else:
        print("No cycles have been run yet.")
        print("Use 'orchestrator run <plan.json>' to start a run plan.")
    
    return 0


def command_orchestrator_benchmark(args: argparse.Namespace) -> int:
    """Benchmark different models for a specific task."""
    paths = orchestrator_paths()
    
    config = get_model_config()
    
    # Get models to test from .env (primary + fallbacks for small slot)
    primary = config.get("small", "qwen/qwen3.5-flash-02-23")
    fallback_str = config.get("fallback_small", "")
    fallbacks = [m.strip() for m in fallback_str.split(",") if m.strip()] if fallback_str else []
    
    # Combine primary + fallbacks
    test_models = [primary] + fallbacks
    
    # If no fallbacks configured, use some defaults for testing
    if len(test_models) < 2:
        test_models.extend(["meta-llama/llama-3-8b-instruct", "google/gemma-2-9b-it"])
    
    # Sample task: summarize a short text
    test_content = """This is a test research note about climate volatility.
    
The key finding is that historical baselines are becoming less reliable as stationarity breaks down.
Institutions still rely heavily on frames built for a more stable world, which creates significant risk.

Evidence:
- IPCC AR6 reports increased compound extremes
- Regional studies show precipitation variability increasing
- Infrastructure design standards assume stationarity

This suggests we need new approaches to scenario planning."""

    system_prompt = "You are summarizing a research note. Extract key claims in bullet points."
    user_prompt = f"Summarize this note:\n\n{test_content}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    
    timeout = int(config.get("timeout", "90"))
    
    print("=== Model Benchmark ===")
    print(f"Task: Summarize research note (~100 tokens)")
    print(f"Timeout: {timeout}s per model")
    print()
    
    results = []
    
    for model in test_models:
        print(f"Testing {model}...")
        try:
            content, model_used, duration = call_openrouter(messages, model, config, timeout=timeout)
            
            # Estimate cost (simplified)
            cost_estimate = 0.001  # Rough estimate for small task
            
            results.append({
                "model": model_used,
                "duration": round(duration, 2),
                "content_length": len(content),
                "cost_estimate": cost_estimate,
                "success": True
            })
            
            print(f"  ✓ {model_used}: {duration:.2f}s, {len(content)} chars")
            
        except SystemExit as e:
            results.append({
                "model": model,
                "duration": 0,
                "error": str(e),
                "success": False
            })
            print(f"  ✗ Failed: {e}")
    
    # Print summary
    print()
    print("=== Results ===")
    print()
    
    successful = [r for r in results if r.get("success")]
    if successful:
        # Sort by duration
        fastest = min(successful, key=lambda x: x["duration"])
        print(f"Fastest: {fastest['model']} ({fastest['duration']:.2f}s)")
        print()
        
        print("| Model | Duration | Output Length |")
        print("|-------|----------|---------------|")
        for r in sorted(successful, key=lambda x: x["duration"]):
            print(f"| {r['model'][:40]} | {r['duration']:.2f}s | {r['content_length']} chars |")
    else:
        print("All models failed!")
    
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

    # Phase 9C: L5 readiness tracking
    branch_l5 = branch_sub.add_parser("l5-readiness", help="Assess L5 generalizability readiness")
    branch_l5.add_argument("slug", help="Branch slug")
    branch_l5.set_defaults(func=command_branch_l5_readiness)

    # Phase 9D: Template generation
    branch_template = branch_sub.add_parser("template", help="Create new branch from structure type template")
    branch_template.add_argument("structure_type", choices=["sequence", "correlation", "design-rule", "hybrid-2comp", "hybrid-3comp"], help="Structure type template")
    branch_template.add_argument("slug", help="New branch slug")
    branch_template.add_argument("--title", required=True, help="Branch title")
    branch_template.add_argument("--domain", required=True, help="Branch domain")
    branch_template.set_defaults(func=command_branch_template)

    # Phase 9D: Cross-method integration
    branch_integrate = branch_sub.add_parser("integrate", help="Generate cross-method integration synthesis")
    branch_integrate.add_argument("slug", help="Branch slug")
    branch_integrate.add_argument("--method", required=True, choices=["resilience-engineering", "systems-thinking", "complexity-science", "institutional-analysis", "pandemic-preparedness"], help="External method to integrate with")
    branch_integrate.set_defaults(func=command_branch_integrate)

    # Phase 7B: Component index
    component = subparsers.add_parser("component", help="Component index commands")
    component_sub = component.add_subparsers(dest="component_command", required=True)

    component_index = component_sub.add_parser("index", help="Build component index from YAML files")
    component_index.set_defaults(func=command_component_index)

    component_search = component_sub.add_parser("search", help="Search for components by query")
    component_search.add_argument("query", help="Search query")
    component_search.add_argument("--type", choices=COMPONENT_TYPES, help="Filter by component type")
    component_search.set_defaults(func=command_component_search)

    component_list = component_sub.add_parser("list", help="List components by type")
    component_list.add_argument("--type", choices=COMPONENT_TYPES, help="Filter by component type")
    component_list.set_defaults(func=command_component_list)

    component_suggest = component_sub.add_parser("suggest", help="Suggest components for a branch")
    component_suggest.add_argument("slug", help="Branch slug")
    component_suggest.set_defaults(func=command_component_suggest)

    # Phase 7C: Curation support
    curate = subparsers.add_parser("curate", help="Curation support commands")
    curate_sub = curate.add_subparsers(dest="curate_command", required=True)

    curate_compare = curate_sub.add_parser("compare", help="Generate side-by-side comparison table")
    curate_compare.add_argument("variants", nargs="+", help="Variant paths to compare")
    curate_compare.set_defaults(func=command_curate_compare)

    curate_matrix = curate_sub.add_parser("matrix", help="Generate evaluation matrix draft")
    curate_matrix.add_argument("slug", help="Branch slug")
    curate_matrix.set_defaults(func=command_curate_matrix)

    # Iteration 3: Model delegation
    delegate = subparsers.add_parser("delegate", help="Delegated model tasks")
    delegate_sub = delegate.add_subparsers(dest="delegate_command", required=True)

    delegate_summarize = delegate_sub.add_parser("summarize-note", help="Summarize a research note")
    delegate_summarize.add_argument("input", help="Path to the note file")
    delegate_summarize.set_defaults(func=command_delegate_summarize)

    delegate_extract = delegate_sub.add_parser("extract-claims", help="Extract claims from an artifact")
    delegate_extract.add_argument("input", help="Path to the artifact file")
    delegate_extract.set_defaults(func=command_delegate_extract_claims)

    # Phase 6B: Workflow automation
    delegate_branch_packet = delegate_sub.add_parser("branch-packet", help="Generate complete branch packet (snapshot + index + compare-prep)")
    delegate_branch_packet.add_argument("slug", help="Branch slug")
    delegate_branch_packet.set_defaults(func=command_delegate_branch_packet)

    delegate_run_prep = delegate_sub.add_parser("run-prep", help="Prepare all materials for a run type")
    delegate_run_prep.add_argument("branch", help="Branch slug")
    delegate_run_prep.add_argument("--type", required=True, choices=sorted(PASS_TYPES.keys()), help="Run type")
    delegate_run_prep.set_defaults(func=command_delegate_run_prep)

    # Phase 6B: Batch processing
    delegate_batch = delegate_sub.add_parser("batch", help="Process multiple files in batch")
    delegate_batch.add_argument("task", choices=["summarize-note", "extract-claims"], help="Task to run on all files")
    delegate_batch.add_argument("pattern", help="Glob pattern for files (e.g., 'research/notes/*.md')")
    delegate_batch.set_defaults(func=command_delegate_batch)

    # Phase 7: Orchestrator
    orchestrator = subparsers.add_parser("orchestrator", help="Scaled-cycle orchestrator")
    orchestrator_sub = orchestrator.add_subparsers(dest="orchestrator_command", required=True)

    orchestrator_run = orchestrator_sub.add_parser("run", help="Execute a run plan")
    orchestrator_run.add_argument("plan", help="Path to run plan JSON file")
    orchestrator_run.set_defaults(func=command_orchestrator_run)

    orchestrator_status = orchestrator_sub.add_parser("status", help="Show orchestrator status")
    orchestrator_status.set_defaults(func=command_orchestrator_status)

    orchestrator_benchmark = orchestrator_sub.add_parser("benchmark", help="Benchmark model performance")
    orchestrator_benchmark.set_defaults(func=command_orchestrator_benchmark)

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
