from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


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
    return warnings


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


def command_run_check(args: argparse.Namespace) -> int:
    run, _, paths = load_run(args.run_id)
    missing_kinds, missing_files = run_check_result(run, paths)
    print_run_check(run, missing_kinds, missing_files)
    return 1 if missing_kinds or missing_files else 0


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

    run = subparsers.add_parser("run", help="Run manifest commands")
    run_sub = run.add_subparsers(dest="run_command", required=True)

    run_new = run_sub.add_parser("new", help="Create a new run manifest")
    run_new.add_argument("branch")
    run_new.add_argument("--type", required=True, choices=sorted(PASS_TYPES.keys()))
    run_new.add_argument("--question")
    run_new.set_defaults(func=command_run_new)

    run_check = run_sub.add_parser("check", help="Validate a run manifest")
    run_check.add_argument("run_id")
    run_check.set_defaults(func=command_run_check)

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
