#!/usr/bin/env python3
"""Validate the plugin's slash commands and keep help + README in sync.

Checks, for CI (dependency-free):
  1. Every plugins/obsidian-knowledge/commands/*.md has well-formed frontmatter
     (opening/closing ``---`` and a non-empty ``description:``).
  2. Every command is referenced (as ``obsidian-knowledge:<name>``) in BOTH the
     help command and the README — so a new command can't ship undiscoverable.
  3. Every ``obsidian-knowledge:<name>`` referenced in help.md or README.md has a
     matching command file — so the guide/README can't reference a missing command.

Exits non-zero with a list of problems.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CMD_DIR = REPO / "plugins" / "obsidian-knowledge" / "commands"
HELP = CMD_DIR / "help.md"
README = REPO / "README.md"

REF = re.compile(r"obsidian-knowledge:([a-z][a-z0-9-]*)")
errors: list[str] = []


def check_frontmatter(path: Path) -> None:
    lines = path.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        errors.append(f"{path.name}: missing opening '---' frontmatter")
        return
    try:
        close = lines.index("---", 1)
    except ValueError:
        errors.append(f"{path.name}: missing closing '---' frontmatter")
        return
    fm = lines[1:close]
    if not any(re.match(r"description:\s*\S", line) for line in fm):
        errors.append(f"{path.name}: missing or empty 'description:'")


def main() -> None:
    if not CMD_DIR.is_dir():
        errors.append(f"commands dir not found: {CMD_DIR.relative_to(REPO)}")
        return
    cmd_files = sorted(CMD_DIR.glob("*.md"))
    names = {p.stem for p in cmd_files}
    for p in cmd_files:
        check_frontmatter(p)

    help_text = HELP.read_text() if HELP.exists() else ""
    readme_text = README.read_text() if README.exists() else ""
    if not help_text:
        errors.append("help.md not found")
    if not readme_text:
        errors.append("README.md not found")

    for name in sorted(names):
        token = f"obsidian-knowledge:{name}"
        if token not in help_text:
            errors.append(f"command '{name}' is not listed in help.md")
        if token not in readme_text:
            errors.append(f"command '{name}' is not listed in README.md")

    referenced = set(REF.findall(help_text)) | set(REF.findall(readme_text))
    for name in sorted(referenced - names):
        errors.append(f"help/README reference '{name}' but no command file exists")


if __name__ == "__main__":
    main()
    if errors:
        print("Command validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    n = len(list(CMD_DIR.glob("*.md")))
    print(f"Commands OK: {n} commands, frontmatter valid, help + README in sync.")
    sys.exit(0)
