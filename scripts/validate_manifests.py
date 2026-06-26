#!/usr/bin/env python3
"""Validate the Claude Code + Codex plugin and marketplace manifests in this repo.

Checks, for CI:
  - .claude-plugin/marketplace.json AND .agents/plugins/marketplace.json parse,
    have name/owner/plugins, and every plugin entry has a name + a source that
    resolves to a real plugin directory.
  - Each referenced plugin has the matching manifest under
    .claude-plugin/plugin.json (Claude) and .codex-plugin/plugin.json (Codex),
    each parsing and naming the same plugin as its marketplace entry.
  - Any hooks/commands/skills paths declared in the Claude plugin.json exist.
  - The two marketplaces describe the same plugin set: they must agree on
    `name`, `owner.name`, and the (name, source) tuples in `plugins`.

Optional argument: a path to use as the repo root. With no argument the root is
inferred from this file's location. The argument lets the adversarial tests in
test_validators.py point the validator at a temp directory. Exits non-zero on
the first class of failures found.
"""
from __future__ import annotations  # keep annotations lazy so this runs on Python 3.8

import json
import sys
from pathlib import Path

errors: list[str] = []

MARKETPLACES = [
    # (marketplace file, plugin manifest file inside each plugin dir, kind)
    (".claude-plugin/marketplace.json",  ".claude-plugin/plugin.json", "claude"),
    (".agents/plugins/marketplace.json", ".codex-plugin/plugin.json",  "codex"),
]


def _rel(path: Path, repo: Path) -> str:
    try:
        return str(path.relative_to(repo))
    except ValueError:
        return str(path)


def load(path: Path, repo: Path):
    # Force UTF-8 so a future em-dash in a description does not blow up on
    # Windows, where Path.read_text() defaults to the platform code page.
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing: {_rel(path, repo)}")
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {_rel(path, repo)}: {exc}")
    return None


def require(cond: bool, msg: str):
    if not cond:
        errors.append(msg)


def _check_marketplace(repo: Path, market_path: Path, plugin_manifest_rel: str, kind: str):
    label = _rel(market_path, repo)
    market = load(market_path, repo)
    if market is None:
        return None
    require(bool(market.get("name")), f"{label}: missing 'name'")
    require(isinstance(market.get("owner"), dict) and market["owner"].get("name"),
            f"{label}: missing owner.name")
    plugins = market.get("plugins")
    require(isinstance(plugins, list) and plugins,
            f"{label}: 'plugins' must be a non-empty array")
    for i, entry in enumerate(plugins or []):
        name = entry.get("name")
        require(bool(name), f"{label}: plugins[{i}] missing 'name'")
        source = entry.get("source")
        require(bool(source), f"{label}: plugins[{i}] missing 'source'")
        if isinstance(source, str):
            _check_plugin_dir(repo, repo / source, name, plugin_manifest_rel, kind)
    return market


def _check_plugin_dir(repo: Path, plugin_dir: Path, expected_name: str,
                      plugin_manifest_rel: str, kind: str) -> None:
    manifest = plugin_dir / plugin_manifest_rel
    if not plugin_dir.is_dir():
        errors.append(f"plugin source not found: {_rel(plugin_dir, repo)}")
        return
    data = load(manifest, repo)
    if data is None:
        return
    require(data.get("name") == expected_name,
            f"{_rel(manifest, repo)}: name '{data.get('name')}' "
            f"!= marketplace entry '{expected_name}'")
    if kind == "claude":
        for key in ("hooks", "commands", "skills"):
            val = data.get(key)
            if isinstance(val, str):
                # Strip only a leading "./" prefix. NOT val.lstrip("./"), which strips a
                # *set* of chars and would eat the dot of a dot-dir (e.g. "./.config/x"
                # -> "config/x"), falsely flagging a real path as missing.
                rel = val[2:] if val.startswith("./") else val
                require((plugin_dir / rel).exists(),
                        f"{_rel(manifest, repo)}: {key} path '{val}' not found")


def _cross_check(claude: dict, codex: dict) -> None:
    """Both marketplaces describe the same plugin set; surface any drift."""
    require(claude.get("name") == codex.get("name"),
            f"marketplaces disagree on 'name': "
            f"claude='{claude.get('name')}' codex='{codex.get('name')}'")
    owner_a = (claude.get("owner") or {}).get("name")
    owner_b = (codex.get("owner") or {}).get("name")
    require(owner_a == owner_b,
            f"marketplaces disagree on owner.name: "
            f"claude='{owner_a}' codex='{owner_b}'")
    sig_a = {(p.get("name"), p.get("source")) for p in (claude.get("plugins") or [])}
    sig_b = {(p.get("name"), p.get("source")) for p in (codex.get("plugins") or [])}
    require(sig_a == sig_b,
            f"marketplaces disagree on plugin (name, source) set: "
            f"claude only={sorted(sig_a - sig_b)}, codex only={sorted(sig_b - sig_a)}")


def main() -> None:
    repo = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    claude = _check_marketplace(repo, repo / MARKETPLACES[0][0], MARKETPLACES[0][1], MARKETPLACES[0][2])
    codex  = _check_marketplace(repo, repo / MARKETPLACES[1][0], MARKETPLACES[1][1], MARKETPLACES[1][2])
    if claude and codex:
        _cross_check(claude, codex)


if __name__ == "__main__":
    main()
    if errors:
        print("Manifest validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    print("Manifests OK: claude + codex marketplaces and plugin.json files valid and consistent.")
    sys.exit(0)
