#!/usr/bin/env python3
"""Validate Obsidian wikilinks under a vault or collection.

Usage:
    validate_links.py [ROOT]        # default: current directory

Scans every ``*.md`` file for ``[[wikilink]]`` and ``![[embed]]`` references and
checks that each resolves to a file in the tree. Resolution mirrors Obsidian:

- indexes **all** files (not just notes), so image/PDF/attachment embeds like
  ``![[diagram.png]]`` resolve to the real file;
- understands alias pipes (``[[path|alias]]`` and table-escaped ``[[path\\|alias]]``),
  heading anchors (``[[note#Section]]``), and block anchors (``[[note^id]]``);
- supports absolute-from-root, partial, and "shortest path" (bare name) links;
- matches case-insensitively, as Obsidian does;
- ignores links inside fenced/inline code, which Obsidian does not render.

Prints one ``BROKEN<TAB>source<TAB>link`` line per unresolved link and exits 1 if
any are broken; exits 0 when everything resolves; exits 2 if ROOT is missing.

Caveat: like Obsidian's own resolver, a bare ``[[Foo]]`` resolves to any ``Foo``
anywhere in the vault, so this confirms a link resolves to *something*, not that it
points at the intended note when two notes share a name.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
FENCED_CODE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.exists():
        print(f"error: {root} does not exist", file=sys.stderr)
        return 2

    all_files = [p for p in root.rglob("*") if p.is_file()]
    md_files = [p for p in all_files if p.suffix.lower() == ".md"]

    # All indexes are case-folded, mirroring Obsidian's case-insensitive resolution.
    stems = {p.stem.casefold() for p in all_files}          # bare name, no extension
    names = {p.name.casefold() for p in all_files}          # bare name, with extension
    rels: set[str] = set()                                  # relative paths from root
    for p in all_files:
        rel = p.relative_to(root).as_posix().casefold()
        rels.add(rel)
        if rel.endswith(".md"):
            rels.add(rel[:-3])

    broken = 0
    checked = 0
    for src in md_files:
        text = src.read_text(errors="ignore")
        text = FENCED_CODE.sub("", text)
        text = INLINE_CODE.sub("", text)
        for raw in WIKILINK.findall(text):
            link = _clean(raw)
            if not link:
                continue  # pure anchor link, e.g. [[#Section]]
            checked += 1
            if not _resolves(link, stems, names, rels):
                print(f"BROKEN\t{src.relative_to(root).as_posix()}\t{link}")
                broken += 1

    print(f"checked {checked} link(s) across {len(md_files)} note(s) "
          f"({len(all_files)} files indexed); {broken} broken", file=sys.stderr)
    return 1 if broken else 0


def _clean(raw: str) -> str:
    """Reduce a raw ``[[...]]`` body to the target path: drop alias, heading, block."""
    link = raw.replace("\\|", "|").split("|", 1)[0]   # strip alias (and table-escape)
    link = link.split("#", 1)[0]                        # strip heading anchor
    link = link.split("^", 1)[0]                        # strip block anchor
    return link.strip()


def _resolves(link: str, stems: set[str], names: set[str], rels: set[str]) -> bool:
    lk = link.casefold()
    lk_noext = lk[:-3] if lk.endswith(".md") else lk

    # Exact path from vault root (with or without the .md suffix).
    if lk in rels or lk_noext in rels:
        return True

    if "/" not in lk:
        # Bare name: shortest-path note match, or a file referenced with extension.
        return lk_noext in stems or lk in names

    # Partial path (e.g. [[Topic/Note]]): match any indexed path ending with it.
    tail = "/" + lk
    tail_noext = "/" + lk_noext
    return any(r.endswith(tail) or r.endswith(tail_noext) for r in rels)


if __name__ == "__main__":
    sys.exit(main())
