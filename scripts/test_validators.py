#!/usr/bin/env python3
"""Adversarial tests for the wikilink validator — run in CI on every PR.

CI's other step runs the validator on the clean example vault, which can't catch a
validator that's subtly *wrong* (it would still report 0 broken). These tests build
hostile temporary vaults and assert the validator resolves what Obsidian resolves
(embeds, anchors, partial/shortest paths, case-insensitively) and ignores what
Obsidian doesn't render (code blocks, HTML comments) — while still catching genuinely
broken links. Any change to `validate_links.py` (including outside contributions) must
keep these green.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VALIDATOR = REPO / "plugins" / "obsidian-knowledge" / "scripts" / "validate_links.py"

failures: list[str] = []


def run(vault: Path):
    p = subprocess.run([sys.executable, str(VALIDATOR), str(vault)],
                       capture_output=True, text=True)
    broken = {ln.split("\t")[2] for ln in p.stdout.splitlines() if ln.startswith("BROKEN")}
    return p.returncode, broken


def write(vault: Path, rel: str, content: str = "x") -> None:
    f = vault / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content)


def check(name: str, cond: bool) -> None:
    print(("ok   " if cond else "FAIL ") + name)
    if not cond:
        failures.append(name)


def main() -> None:
    if not VALIDATOR.exists():
        print(f"validator not found: {VALIDATOR}", file=sys.stderr)
        sys.exit(2)

    with tempfile.TemporaryDirectory() as d:
        v = Path(d)
        write(v, "A/Target.md", "# Target\n## Heading\n")
        write(v, "A/img.png", "")
        write(v, "Attachments/figure.pdf", "")
        note = "\n".join([
            "Plain link: [[Target]]",
            "Case-insensitive: [[target]]",
            "Partial path: [[A/Target]]",
            "Heading anchor: [[Target#Heading]]",
            "Block anchor: [[Target^abc123]]",
            "Alias: [[A/Target|the target]]",
            "Table escape: | x | [[A/Target\\|T]] |",
            "Image embed: ![[img.png]]",
            "PDF embed: ![[Attachments/figure.pdf]]",
            "```", "fenced [[GhostFenced]]", "```",
            "~~~", "tilde [[GhostTilde]]", "~~~",
            "inline `[[GhostInline]]`",
            "<!-- comment [[GhostComment]] -->",
            "Real broken: [[DefinitelyMissing]]",
        ])
        write(v, "A/note.md", note)
        rc, broken = run(v)
        check("resolves embeds/anchors/alias/case/partial — no false positives",
              broken == {"DefinitelyMissing"})
        check("ignores links in fenced/tilde/inline code and HTML comments",
              not (broken & {"GhostFenced", "GhostTilde", "GhostInline", "GhostComment"}))
        check("catches the genuinely broken link", "DefinitelyMissing" in broken)
        check("exit code 1 when something is broken", rc == 1)

    with tempfile.TemporaryDirectory() as d:
        v = Path(d)
        write(v, "ok.md", "self link: [[ok]]")
        rc, broken = run(v)
        check("exit code 0 and nothing broken on a clean vault", rc == 0 and not broken)

    rc, _ = run(Path(tempfile.gettempdir()) / "oka-does-not-exist-xyz")
    check("exit code 2 when the root is missing", rc == 2)

    if failures:
        print(f"\n{len(failures)} validator test(s) FAILED", file=sys.stderr)
        sys.exit(1)
    print("\nAll validator adversarial tests passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
