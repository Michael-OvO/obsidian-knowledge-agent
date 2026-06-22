#!/usr/bin/env python3
"""Validate the Claude Code plugin + marketplace manifests in this repo.

Checks, for CI:
  - .claude-plugin/marketplace.json parses, has name/owner/plugins, and every
    plugin entry has a name + a source that resolves to a real plugin directory.
  - each referenced plugin has .claude-plugin/plugin.json that parses and has a
    name matching its marketplace entry.
  - any hooks/commands/skills paths declared in plugin.json actually exist.

Exits non-zero on the first class of failures found.
"""
from __future__ import annotations  # keep annotations lazy so this runs on Python 3.8

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
errors: list[str] = []


def load(path: Path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        errors.append(f"missing: {path.relative_to(REPO)}")
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path.relative_to(REPO)}: {exc}")
    return None


def require(cond: bool, msg: str):
    if not cond:
        errors.append(msg)


def main() -> int:
    market = load(REPO / ".claude-plugin" / "marketplace.json")
    if market is not None:
        require(bool(market.get("name")), "marketplace.json: missing 'name'")
        require(isinstance(market.get("owner"), dict) and market["owner"].get("name"),
                "marketplace.json: missing owner.name")
        plugins = market.get("plugins")
        require(isinstance(plugins, list) and plugins,
                "marketplace.json: 'plugins' must be a non-empty array")
        for i, entry in enumerate(plugins or []):
            name = entry.get("name")
            require(bool(name), f"marketplace.json: plugins[{i}] missing 'name'")
            source = entry.get("source")
            require(bool(source), f"marketplace.json: plugins[{i}] missing 'source'")
            if isinstance(source, str):
                _check_plugin_dir(REPO / source, name)


def _check_plugin_dir(plugin_dir: Path, expected_name):
    manifest = plugin_dir / ".claude-plugin" / "plugin.json"
    if not plugin_dir.is_dir():
        errors.append(f"plugin source not found: {plugin_dir.relative_to(REPO)}")
        return
    data = load(manifest)
    if data is None:
        return
    require(data.get("name") == expected_name,
            f"{manifest.relative_to(REPO)}: name '{data.get('name')}' "
            f"!= marketplace entry '{expected_name}'")
    for key in ("hooks", "commands", "skills"):
        val = data.get(key)
        if isinstance(val, str):
            require((plugin_dir / val.lstrip("./")).exists(),
                    f"{manifest.relative_to(REPO)}: {key} path '{val}' not found")


if __name__ == "__main__":
    main()
    if errors:
        print("Manifest validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)
    print("Manifests OK: marketplace.json + plugin.json valid and consistent.")
    sys.exit(0)
