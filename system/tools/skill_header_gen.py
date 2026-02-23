# -*- coding: utf-8 -*-
"""
Copyright (c) 2026 Lukas Geiger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Tool: skill_header_gen
Version: 1.0.0
Author: BACH Team
Created: 2026-02-08
Updated: 2026-02-08
Anthropic-Compatible: True

VERSIONS-HINWEIS: Prüfe auf neuere Versionen mit: bach tools version skill_header_gen

BACH Skill Header Generator
============================
Generates and validates YAML frontmatter headers for SKILL.md files.

Usage:
    python skill_header_gen.py --all [--dry-run|--fix]
    python skill_header_gen.py --path <dir> [--dry-run|--fix]
    python skill_header_gen.py --file <skill.md> [--dry-run|--fix]

Options:
    --all       Scan all skill directories
    --path      Scan a specific directory
    --file      Process a single SKILL.md file
    --dry-run   Show what would change (default)
    --fix       Actually write changes
    --update-db Update skills DB table versions from YAML headers
    --verbose   Show detailed output

Scanned directories (with --all):
    agents/*/SKILL.md
    agents/_experts/*/SKILL.md
    hub/_services/*/SKILL.md
    partners/*/SKILL.md
"""

import sys
import os
import re
import argparse
import sqlite3
from pathlib import Path
from datetime import date

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SYSTEM_DIR = Path(__file__).resolve().parent.parent  # system/
TODAY = date.today().isoformat()

SCAN_PATTERNS = [
    "agents/*/SKILL.md",
    "agents/_experts/*/SKILL.md",
    "hub/_services/*/SKILL.md",
    "partners/*/SKILL.md",
]

# Maps parent directory name to skill type
TYPE_MAP = {
    "_agents": "agent",
    "_experts": "expert",
    "_services": "service",
    "_partners": "partner",
    "_workflows": "workflow",
}

# Standard header field order
STANDARD_FIELDS = [
    "name",
    "version",
    "type",
    "author",
    "created",
    "updated",
    "anthropic_compatible",
    "status",
    "dependencies",
    "description",
]

# Fields that are preserved but not required
OPTIONAL_FIELDS = [
    "orchestrates",
    "migrated_from",
    "migration_date",
    "metadata",
    "dist_type",
]

DEFAULT_AUTHOR = "BACH Team"
DEFAULT_VERSION = "1.0.0"


# ---------------------------------------------------------------------------
# YAML Frontmatter Parser / Writer (no external dependency beyond PyYAML)
# ---------------------------------------------------------------------------

def parse_yaml_frontmatter(content: str) -> tuple:
    """
    Parse YAML frontmatter from markdown content.

    Returns:
        (yaml_dict, body_text, had_frontmatter)
        - yaml_dict: parsed header dict (empty if none found)
        - body_text: everything after the closing ---
        - had_frontmatter: True if file had valid --- ... --- block
    """
    import yaml

    content = content.lstrip("\ufeff")  # strip BOM
    lines = content.split("\n")

    if not lines or lines[0].strip() != "---":
        return {}, content, False

    # Find closing ---
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return {}, content, False

    yaml_text = "\n".join(lines[1:end_idx])
    body_text = "\n".join(lines[end_idx + 1:])

    try:
        data = yaml.safe_load(yaml_text) or {}
    except yaml.YAMLError as e:
        print(f"  [WARN] YAML parse error: {e}")
        data = {}

    return data, body_text, True


def normalize_header(data: dict, file_path: Path) -> dict:
    """
    Normalize a parsed YAML header to the standard format.

    Handles the three known variants:
    1. Standard: name, version, type, ... at top level
    2. Nested metadata: name, metadata.version, metadata.type, ...
    3. Minimal: name, version, description only
    """
    normalized = {}

    # Handle nested metadata variant (scheduling, household, financial)
    metadata = data.get("metadata", {})
    if isinstance(metadata, dict) and metadata:
        # Flatten metadata into top level
        normalized["name"] = data.get("name", "")
        normalized["version"] = metadata.get("version", DEFAULT_VERSION)
        normalized["type"] = metadata.get("type", _detect_type(file_path))
        normalized["author"] = data.get("author", DEFAULT_AUTHOR)
        normalized["created"] = metadata.get("created", metadata.get("last_updated", TODAY))
        normalized["updated"] = metadata.get("last_updated", TODAY)
        normalized["anthropic_compatible"] = data.get("anthropic_compatible", True)
        normalized["status"] = metadata.get("status", "active")
    else:
        # Standard or minimal format
        normalized["name"] = data.get("name", "")
        normalized["version"] = data.get("version", DEFAULT_VERSION)
        normalized["type"] = data.get("type", _detect_type(file_path))
        normalized["author"] = data.get("author", DEFAULT_AUTHOR)
        normalized["created"] = data.get("created", TODAY)
        normalized["updated"] = data.get("updated", TODAY)
        normalized["anthropic_compatible"] = data.get("anthropic_compatible", True)
        normalized["status"] = data.get("status", "active")

    # Dependencies - normalize to standard structure
    deps = data.get("dependencies", {})
    if isinstance(deps, dict):
        normalized["dependencies"] = {
            "tools": deps.get("tools", []),
            "services": deps.get("services", []),
            "workflows": deps.get("workflows", []),
        }
    else:
        normalized["dependencies"] = {
            "tools": [],
            "services": [],
            "workflows": [],
        }

    # Description
    normalized["description"] = data.get("description", "")

    # Preserve optional fields
    if "orchestrates" in data:
        normalized["orchestrates"] = data["orchestrates"]

    # Ensure name is set
    if not normalized["name"]:
        normalized["name"] = _detect_name(file_path)

    # Ensure version is a string
    normalized["version"] = str(normalized["version"])

    # Ensure dates are strings
    normalized["created"] = str(normalized["created"])
    normalized["updated"] = str(normalized["updated"])

    return normalized


def generate_header_from_content(content: str, file_path: Path) -> dict:
    """
    Auto-detect header fields from markdown content when no YAML header exists.
    """
    header = {
        "name": _detect_name(file_path),
        "version": DEFAULT_VERSION,
        "type": _detect_type(file_path),
        "author": DEFAULT_AUTHOR,
        "created": TODAY,
        "updated": TODAY,
        "anthropic_compatible": True,
        "status": "active",
        "dependencies": {
            "tools": [],
            "services": [],
            "workflows": [],
        },
        "description": "",
    }

    # Try to extract description from first paragraph or heading
    lines = content.strip().split("\n")
    desc_lines = []
    in_desc = False

    for line in lines:
        stripped = line.strip()
        # Skip headings
        if stripped.startswith("#"):
            if in_desc:
                break
            continue
        # Skip empty lines before description
        if not stripped and not in_desc:
            continue
        # Skip markdown formatting
        if stripped.startswith(("```", "---", "|", ">")):
            if in_desc:
                break
            # Blockquote might be a description
            if stripped.startswith(">"):
                desc_text = stripped.lstrip("> ").strip()
                if desc_text and len(desc_text) > 10:
                    desc_lines.append(desc_text)
                    in_desc = True
            continue

        if stripped:
            desc_lines.append(stripped)
            in_desc = True
        elif in_desc:
            break

    if desc_lines:
        header["description"] = " ".join(desc_lines)[:300]

    # Try to detect version from content
    version_match = re.search(
        r"(?:Version|version|VERSION)[:\s]+v?(\d+\.\d+(?:\.\d+)?)",
        content
    )
    if version_match:
        header["version"] = version_match.group(1)

    return header


def render_yaml_header(data: dict) -> str:
    """
    Render a normalized header dict as YAML frontmatter string.
    Uses manual rendering for consistent formatting.
    """
    lines = ["---"]

    # Core fields in order
    lines.append(f"name: {data['name']}")
    lines.append(f"version: {data['version']}")
    lines.append(f"type: {data['type']}")
    lines.append(f"author: {data['author']}")
    lines.append(f"created: {data['created']}")
    lines.append(f"updated: {data['updated']}")
    lines.append(f"anthropic_compatible: {str(data.get('anthropic_compatible', True)).lower()}")
    lines.append(f"status: {data.get('status', 'active')}")

    # Orchestrates (optional, for agents)
    if "orchestrates" in data:
        orch = data["orchestrates"]
        lines.append("")
        lines.append("orchestrates:")
        experts = orch.get("experts", [])
        services = orch.get("services", [])
        lines.append(f"  experts: [{', '.join(str(e) for e in experts)}]")
        lines.append(f"  services: [{', '.join(str(s) for s in services)}]")

    # Dependencies
    deps = data.get("dependencies", {})
    lines.append("")
    lines.append("dependencies:")

    tools = deps.get("tools", [])
    services = deps.get("services", [])
    workflows = deps.get("workflows", [])

    if tools and isinstance(tools, list) and len(tools) > 0:
        # If items look like they should be on separate lines
        if any(isinstance(t, str) and len(t) > 30 for t in tools):
            lines.append("  tools:")
            for t in tools:
                lines.append(f"    - {t}")
        else:
            lines.append(f"  tools: [{', '.join(str(t) for t in tools)}]")
    else:
        lines.append("  tools: []")

    if services and isinstance(services, list) and len(services) > 0:
        lines.append(f"  services: [{', '.join(str(s) for s in services)}]")
    else:
        lines.append("  services: []")

    if workflows and isinstance(workflows, list) and len(workflows) > 0:
        lines.append("  workflows:")
        for w in workflows:
            lines.append(f"    - {w}")
    else:
        lines.append("  workflows: []")

    # Description
    desc = data.get("description", "").strip()
    if desc:
        lines.append("")
        lines.append("description: >")
        # Wrap description at ~78 chars
        words = desc.split()
        current_line = "  "
        for word in words:
            if len(current_line) + len(word) + 1 > 78:
                lines.append(current_line.rstrip())
                current_line = "  " + word
            else:
                current_line += (" " if len(current_line) > 2 else "") + word
        if current_line.strip():
            lines.append(current_line.rstrip())
    else:
        lines.append("")
        lines.append("description: >")
        lines.append("  (Beschreibung fehlt)")

    lines.append("---")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Detection helpers
# ---------------------------------------------------------------------------

def _detect_name(file_path: Path) -> str:
    """Detect skill name from directory name."""
    # SKILL.md is typically in the skill's own directory
    return file_path.parent.name


def _detect_type(file_path: Path) -> str:
    """Detect skill type from parent directory structure."""
    parts = file_path.parts
    for part in parts:
        if part in TYPE_MAP:
            return TYPE_MAP[part]
    return "skill"


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_header(data: dict) -> list:
    """
    Validate a header dict, returning a list of issues found.
    """
    issues = []

    if not data.get("name"):
        issues.append("Missing 'name' field")

    if not data.get("version"):
        issues.append("Missing 'version' field")
    elif not re.match(r"^\d+\.\d+(\.\d+)?$", str(data["version"])):
        issues.append(f"Invalid version format: {data['version']} (expected X.Y.Z)")

    if not data.get("type"):
        issues.append("Missing 'type' field")

    if not data.get("description") or data.get("description", "").strip() == "(Beschreibung fehlt)":
        issues.append("Missing or placeholder description")

    if not data.get("author"):
        issues.append("Missing 'author' field")

    if not data.get("created"):
        issues.append("Missing 'created' date")

    if not data.get("updated"):
        issues.append("Missing 'updated' date")

    deps = data.get("dependencies", {})
    if not isinstance(deps, dict):
        issues.append("'dependencies' should be a dict with tools/services/workflows")

    return issues


def diff_headers(old_data: dict, new_data: dict) -> list:
    """
    Compare old and new header dicts, returning a list of changes.
    """
    changes = []

    for key in STANDARD_FIELDS:
        old_val = old_data.get(key)
        new_val = new_data.get(key)

        if key == "dependencies":
            # Compare dependencies sub-keys
            old_deps = old_val if isinstance(old_val, dict) else {}
            new_deps = new_val if isinstance(new_val, dict) else {}
            for sub_key in ("tools", "services", "workflows"):
                ov = old_deps.get(sub_key, [])
                nv = new_deps.get(sub_key, [])
                if str(ov) != str(nv):
                    changes.append(f"  dependencies.{sub_key}: {ov} -> {nv}")
            continue

        if str(old_val) != str(new_val):
            # Don't report noise for fields we're just adding
            old_display = old_val if old_val is not None else "(missing)"
            new_display = new_val if new_val is not None else "(missing)"
            changes.append(f"  {key}: {old_display} -> {new_display}")

    # Check orchestrates
    if "orchestrates" in new_data and "orchestrates" not in old_data:
        changes.append("  + orchestrates (added)")
    elif "orchestrates" in old_data and "orchestrates" not in new_data:
        changes.append("  - orchestrates (removed)")

    return changes


# ---------------------------------------------------------------------------
# File scanning
# ---------------------------------------------------------------------------

def find_skill_files(base_dir: Path, patterns: list = None) -> list:
    """
    Find all SKILL.md files matching the scan patterns.
    """
    if patterns is None:
        patterns = SCAN_PATTERNS

    files = []
    for pattern in patterns:
        for match in sorted(base_dir.glob(pattern)):
            if match.is_file():
                files.append(match)

    return files


# ---------------------------------------------------------------------------
# DB update
# ---------------------------------------------------------------------------

def update_skills_db(base_dir: Path, headers: dict, dry_run: bool = True) -> list:
    """
    Update the skills table in bach.db with versions from YAML headers.

    Only updates DB rows whose path directly references the skill's directory
    or whose name exactly matches the SKILL.md header name. This prevents
    false positives from loose LIKE matching.

    Args:
        base_dir: system/ directory
        headers: dict mapping file_path -> normalized header dict
        dry_run: if True, only report what would change

    Returns:
        list of status messages
    """
    db_path = base_dir / "data" / "bach.db"
    if not db_path.exists():
        return ["[ERR] bach.db not found at: " + str(db_path)]

    messages = []
    conn = sqlite3.connect(str(db_path))
    conn.text_factory = str
    cur = conn.cursor()

    try:
        for file_path, header in headers.items():
            skill_name = header.get("name", "")
            version = header.get("version", DEFAULT_VERSION)
            dir_name = file_path.parent.name  # e.g. "ati", "research"

            # Build the relative path fragment for the skill directory
            # e.g. "agents/ati/" or "hub/_services/document/"
            try:
                rel_dir = str(file_path.parent.relative_to(base_dir)).replace("\\", "/")
            except ValueError:
                rel_dir = dir_name

            # Strategy 1: Match by exact SKILL.md path in DB
            cur.execute(
                "SELECT id, name, version, path FROM skills WHERE path LIKE ?",
                (f"%{dir_name}/SKILL.md",)
            )
            matches = cur.fetchall()

            # Strategy 2: Match by exact name (= header name)
            if not matches:
                cur.execute(
                    "SELECT id, name, version, path FROM skills WHERE name = ?",
                    (skill_name,)
                )
                matches = cur.fetchall()

            # Strategy 3: Match by directory-based agent/expert name patterns
            # DB often stores as "agent/dirname" or "service/dirname/SKILL"
            if not matches:
                type_prefix = header.get("type", "")
                if type_prefix in ("agent", "boss-agent"):
                    type_prefix = "agent"
                # Try "type/dirname" pattern
                cur.execute(
                    "SELECT id, name, version, path FROM skills WHERE name = ?",
                    (f"{type_prefix}/{dir_name}",)
                )
                matches = cur.fetchall()

            # Strategy 4: Match by directory name as standalone name
            if not matches and dir_name != skill_name:
                cur.execute(
                    "SELECT id, name, version, path FROM skills WHERE name = ?",
                    (dir_name,)
                )
                matches = cur.fetchall()

            if not matches:
                messages.append(
                    f"  [SKIP] No DB entry for: {skill_name} ({rel_dir})"
                )
                continue

            updated_any = False
            for row in matches:
                db_id, db_name, db_version, db_path_str = row
                if db_version != version:
                    if dry_run:
                        messages.append(
                            f"  [DRY] Would update [{db_id}] {db_name}: "
                            f"v{db_version} -> v{version}"
                        )
                    else:
                        cur.execute(
                            "UPDATE skills SET version = ?, updated_at = ? "
                            "WHERE id = ?",
                            (version, TODAY, db_id)
                        )
                        messages.append(
                            f"  [OK] Updated [{db_id}] {db_name}: "
                            f"v{db_version} -> v{version}"
                        )
                    updated_any = True

            if not updated_any and matches:
                # All matched rows already have the correct version
                pass

        if not dry_run:
            conn.commit()

    except Exception as e:
        messages.append(f"[ERR] DB error: {e}")
    finally:
        conn.close()

    return messages


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def process_file(file_path: Path, dry_run: bool = True, verbose: bool = False) -> dict:
    """
    Process a single SKILL.md file.

    Returns:
        {
            "path": file_path,
            "status": "ok" | "updated" | "created" | "error",
            "issues": [...],
            "changes": [...],
            "header": {...}  # normalized header
        }
    """
    result = {
        "path": file_path,
        "status": "ok",
        "issues": [],
        "changes": [],
        "header": {},
    }

    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = file_path.read_text(encoding="cp1252")
        except Exception as e:
            result["status"] = "error"
            result["issues"].append(f"Cannot read file: {e}")
            return result

    old_data, body, had_frontmatter = parse_yaml_frontmatter(content)

    if had_frontmatter:
        # Validate and normalize existing header
        new_data = normalize_header(old_data, file_path)
        issues = validate_header(new_data)
        changes = diff_headers(old_data, new_data)

        result["issues"] = issues
        result["changes"] = changes
        result["header"] = new_data

        if changes:
            result["status"] = "updated"
            if not dry_run:
                new_header_text = render_yaml_header(new_data)
                new_content = new_header_text + "\n" + body.lstrip("\n")
                file_path.write_text(new_content, encoding="utf-8")
        else:
            result["status"] = "ok"
    else:
        # Generate new header from content
        new_data = generate_header_from_content(content, file_path)
        issues = validate_header(new_data)

        result["issues"] = issues
        result["changes"] = ["(new header generated)"]
        result["header"] = new_data
        result["status"] = "created"

        if not dry_run:
            new_header_text = render_yaml_header(new_data)
            new_content = new_header_text + "\n\n" + content
            file_path.write_text(new_content, encoding="utf-8")

    return result


def process_files(files: list, dry_run: bool = True, verbose: bool = False) -> dict:
    """
    Process multiple SKILL.md files.

    Returns:
        {
            "total": int,
            "ok": int,
            "updated": int,
            "created": int,
            "errors": int,
            "results": [...]
        }
    """
    summary = {
        "total": len(files),
        "ok": 0,
        "updated": 0,
        "created": 0,
        "errors": 0,
        "results": [],
    }

    for file_path in files:
        result = process_file(file_path, dry_run=dry_run, verbose=verbose)
        summary["results"].append(result)
        summary[result["status"]] = summary.get(result["status"], 0) + 1

    return summary


def format_report(summary: dict, dry_run: bool, verbose: bool, base_dir: Path) -> str:
    """Format the processing summary as a human-readable report."""
    lines = []
    mode = "DRY-RUN" if dry_run else "FIX"

    lines.append("=" * 60)
    lines.append(f"SKILL HEADER GENERATOR [{mode}]")
    lines.append("=" * 60)
    lines.append("")

    for result in summary["results"]:
        rel_path = str(result["path"].relative_to(base_dir))
        status_icon = {
            "ok": "[OK]",
            "updated": "[UPD]",
            "created": "[NEW]",
            "error": "[ERR]",
        }.get(result["status"], "[???]")

        lines.append(f"{status_icon} {rel_path}")

        if result["changes"] and (verbose or result["status"] != "ok"):
            for change in result["changes"]:
                lines.append(f"      {change}")

        if result["issues"] and verbose:
            for issue in result["issues"]:
                lines.append(f"      [!] {issue}")

        if verbose and result["header"]:
            lines.append(f"      name={result['header'].get('name')} "
                         f"v={result['header'].get('version')} "
                         f"type={result['header'].get('type')}")

    lines.append("")
    lines.append("-" * 60)
    lines.append(f"Total: {summary['total']} files")
    lines.append(f"  OK (no changes needed): {summary.get('ok', 0)}")
    lines.append(f"  Updated (normalized):   {summary.get('updated', 0)}")
    lines.append(f"  Created (new header):   {summary.get('created', 0)}")
    lines.append(f"  Errors:                 {summary.get('errors', 0)}")

    if dry_run and (summary.get("updated", 0) > 0 or summary.get("created", 0) > 0):
        lines.append("")
        lines.append("Run with --fix to apply changes.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="BACH Skill Header Generator - Generate/validate YAML frontmatter for SKILL.md files"
    )
    parser.add_argument("--all", action="store_true", help="Scan all skill directories")
    parser.add_argument("--path", type=str, help="Scan a specific directory")
    parser.add_argument("--file", type=str, help="Process a single SKILL.md file")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="Show what would change (default)")
    parser.add_argument("--fix", action="store_true",
                        help="Actually write changes")
    parser.add_argument("--update-db", action="store_true",
                        help="Update skills DB table versions from YAML headers")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed output")

    args = parser.parse_args()

    # --fix overrides --dry-run
    dry_run = not args.fix

    # Determine base directory
    base_dir = SYSTEM_DIR

    # Collect files to process
    files = []

    if args.file:
        fp = Path(args.file).resolve()
        if fp.exists():
            files = [fp]
        else:
            print(f"[ERR] File not found: {args.file}")
            sys.exit(1)
    elif args.path:
        scan_dir = Path(args.path).resolve()
        if not scan_dir.exists():
            print(f"[ERR] Directory not found: {args.path}")
            sys.exit(1)
        # Find SKILL.md files in this directory and subdirectories
        files = sorted(scan_dir.rglob("SKILL.md"))
    elif args.all:
        files = find_skill_files(base_dir)
    else:
        # Default: show help
        parser.print_help()
        print("\nExample:")
        print("  python skill_header_gen.py --all --dry-run")
        print("  python skill_header_gen.py --all --fix")
        print("  python skill_header_gen.py --path agents --dry-run")
        print("  python skill_header_gen.py --file agents/ati/SKILL.md --fix")
        sys.exit(0)

    if not files:
        print("[INFO] No SKILL.md files found.")
        sys.exit(0)

    # Process files
    summary = process_files(files, dry_run=dry_run, verbose=args.verbose)

    # Print report
    report = format_report(summary, dry_run, args.verbose, base_dir)
    print(report)

    # Update DB if requested
    if args.update_db:
        print("")
        print("=" * 60)
        print("DATABASE UPDATE")
        print("=" * 60)

        headers = {}
        for result in summary["results"]:
            if result["header"] and result["status"] != "error":
                headers[result["path"]] = result["header"]

        if headers:
            db_messages = update_skills_db(base_dir, headers, dry_run=dry_run)
            for msg in db_messages:
                print(msg)
            if not db_messages:
                print("  [OK] All DB versions are up to date.")
        else:
            print("  [INFO] No valid headers to update in DB.")

    # Exit code
    if summary.get("errors", 0) > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
