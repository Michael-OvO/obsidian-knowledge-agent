#!/usr/bin/env python3
"""Adversarial tests for the wikilink and manifest validators — run in CI on every PR.

CI's other steps run the validators on the real repo / example vault, which can't
catch a validator that's subtly *wrong* (it would still report 0 problems). These
tests build hostile temporary vaults / fake repos and assert:

- the wikilink validator resolves what Obsidian resolves (embeds, anchors, partial
  paths, case-insensitively) and ignores what Obsidian doesn't render (code blocks,
  HTML comments) — while still catching genuinely broken links.
- the manifest validator covers BOTH marketplaces (Claude and Codex) plus the
  paired plugin.json files, and surfaces drift between the two marketplaces (so a
  rename / version bump / plugin set change in only one side cannot ship).

Any change to `validate_links.py` or `validate_manifests.py` (including outside
contributions) must keep these green.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VALIDATOR = REPO / "plugins" / "obsidian-knowledge" / "scripts" / "validate_links.py"
MANIFEST_VALIDATOR = REPO / "scripts" / "validate_manifests.py"

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

    _manifest_tests()

    if failures:
        print(f"\n{len(failures)} validator test(s) FAILED", file=sys.stderr)
        sys.exit(1)
    print("\nAll validator adversarial tests passed.")
    sys.exit(0)


# ---------------------------------------------------------------------------
# Manifest validator tests
# ---------------------------------------------------------------------------

def _run_manifests(repo: Path):
    p = subprocess.run([sys.executable, str(MANIFEST_VALIDATOR), str(repo)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def _make_fake_repo(d: Path, *, claude_market=None, codex_market=None,
                    claude_plugin=None, codex_plugin=None) -> None:
    """Materialize a minimal repo with the four manifests; callers pass overrides."""
    plugin_rel = "plugins/obsidian-knowledge"
    base_market = {
        "name": "obsidian-knowledge-agent",
        "owner": {"name": "tester"},
        "plugins": [{"name": "obsidian-knowledge", "source": f"./{plugin_rel}"}],
    }
    base_plugin = {"name": "obsidian-knowledge", "version": "0.0.1"}
    cm = {**base_market, **(claude_market or {})}
    xm = {**base_market, **(codex_market  or {})}
    cp = {**base_plugin, **(claude_plugin or {})}
    xp = {**base_plugin, **(codex_plugin  or {})}
    (d / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (d / ".agents" / "plugins").mkdir(parents=True, exist_ok=True)
    (d / plugin_rel / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    (d / plugin_rel / ".codex-plugin").mkdir(parents=True, exist_ok=True)
    (d / ".claude-plugin" / "marketplace.json").write_text(json.dumps(cm))
    (d / ".agents" / "plugins" / "marketplace.json").write_text(json.dumps(xm))
    (d / plugin_rel / ".claude-plugin" / "plugin.json").write_text(json.dumps(cp))
    (d / plugin_rel / ".codex-plugin"  / "plugin.json").write_text(json.dumps(xp))


def _manifest_tests() -> None:
    # 1. Well-formed minimal repo passes.
    with tempfile.TemporaryDirectory() as d:
        r = Path(d)
        _make_fake_repo(r)
        rc, out = _run_manifests(r)
        check("manifests: well-formed minimal repo passes", rc == 0)

    # 2. Codex marketplace missing -> fails with a "missing" message.
    with tempfile.TemporaryDirectory() as d:
        r = Path(d)
        _make_fake_repo(r)
        (r / ".agents" / "plugins" / "marketplace.json").unlink()
        rc, out = _run_manifests(r)
        check("manifests: missing codex marketplace fails", rc != 0 and "missing" in out)

    # 3. Marketplaces disagree on 'name' -> cross-check fires.
    with tempfile.TemporaryDirectory() as d:
        r = Path(d)
        _make_fake_repo(r, codex_market={"name": "renamed-on-codex-side"})
        rc, out = _run_manifests(r)
        check("manifests: cross-check catches a 'name' drift",
              rc != 0 and "disagree on 'name'" in out)

    # 4. Codex plugin.json name does not match its marketplace entry -> fails.
    with tempfile.TemporaryDirectory() as d:
        r = Path(d)
        _make_fake_repo(r, codex_plugin={"name": "typo-in-codex-plugin-json"})
        rc, out = _run_manifests(r)
        check("manifests: codex plugin.json name mismatch fails",
              rc != 0 and "typo-in-codex-plugin-json" in out)

    # 5. Marketplaces disagree on the (name, source) plugin set -> cross-check fires.
    with tempfile.TemporaryDirectory() as d:
        r = Path(d)
        extra_plugin = {"name": "extra", "source": "./plugins/obsidian-knowledge"}
        _make_fake_repo(r, codex_market={
            "plugins": [
                {"name": "obsidian-knowledge", "source": "./plugins/obsidian-knowledge"},
                extra_plugin,
            ],
        })
        rc, out = _run_manifests(r)
        check("manifests: cross-check catches a plugin-set drift",
              rc != 0 and "plugin (name, source) set" in out)

    # 6. A Claude hooks/commands/skills path pointing into a DOT-directory resolves
    #    (regression: lstrip("./") used to strip the dot too, falsely flagging it).
    with tempfile.TemporaryDirectory() as d:
        r = Path(d)
        _make_fake_repo(r, claude_plugin={"hooks": "./.config/hooks.json"})
        hooks_dir = r / "plugins" / "obsidian-knowledge" / ".config"
        hooks_dir.mkdir(parents=True, exist_ok=True)
        (hooks_dir / "hooks.json").write_text("{}")
        rc, out = _run_manifests(r)
        check("manifests: dot-dir hooks path resolves (no lstrip footgun)", rc == 0)


if __name__ == "__main__":
    main()
