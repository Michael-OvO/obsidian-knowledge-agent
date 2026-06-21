#!/usr/bin/env python3
"""Validate Obsidian wikilinks under a vault or collection.

Usage:
    validate_links.py [ROOT]        # default: current directory

Scans every ``*.md`` file for ``[[wikilink]]`` references and checks that each
one resolves to a file in the tree. Understands alias pipes (``[[path|alias]]``),
heading/block anchors (``[[path#section]]``), absolute-from-root links, relative
links, and Obsidian "shortest path" links (bare note name matched anywhere).

Prints one ``BROKEN<TAB>source<TAB>link`` line per unresolved link and exits 1 if
any are broken; exits 0 when everything resolves.

Caveat: like Obsidian's own resolver, a bare ``[[Foo]]`` resolves to any ``Foo.md``
in the vault, so this checks that a link *resolves to something*, not that it points
at the intended note when two notes share a name.
"""
import re
import sys
from pathlib import Path

WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not root.exists():
        print(f"error: {root} does not exist", file=sys.stderr)
        return 2

    md_files = list(root.rglob("*.md"))
    stems = {p.stem for p in md_files}
    rels: set[str] = set()
    for p in md_files:
        rp = p.relative_to(root).as_posix()
        rels.add(rp)
        rels.add(rp[:-3] if rp.endswith(".md") else rp)

    broken = 0
    checked = 0
    for src in md_files:
        text = src.read_text(errors="ignore")
        for raw in WIKILINK.findall(text):
            # Obsidian escapes alias pipes inside tables as ``\|``; unescape before
            # splitting off the alias, then drop any heading/block anchor.
            link = raw.replace("\\|", "|").split("|", 1)[0].split("#", 1)[0].strip()
            if not link:
                continue  # pure anchor link, e.g. [[#Section]]
            checked += 1
            if _resolves(link, src, root, stems, rels):
                continue
            print(f"BROKEN\t{src.relative_to(root).as_posix()}\t{link}")
            broken += 1

    print(f"checked {checked} link(s) across {len(md_files)} file(s); "
          f"{broken} broken", file=sys.stderr)
    return 1 if broken else 0


def _resolves(link, src, root, stems, rels) -> bool:
    link_clean = link[:-3] if link.endswith(".md") else link
    # Absolute-from-root or any-relative path match.
    if link_clean in rels or link in rels:
        return True
    # Relative to the source file's folder.
    for cand in (src.parent / link, src.parent / f"{link}.md"):
        if cand.exists():
            return True
    # Obsidian shortest-path: bare note name matched anywhere in the vault.
    if "/" not in link:
        return link in stems
    return link.rsplit("/", 1)[-1] in stems


if __name__ == "__main__":
    sys.exit(main())
