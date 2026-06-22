#!/usr/bin/env bash
set -euo pipefail

# Keep the Claude Code skill's bundled reference docs in sync with the
# canonical instruction modules in .agents/. Run this after editing .agents/.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL="$ROOT/plugins/obsidian-knowledge/skills/obsidian-knowledge"

# 1. Mirror the canonical instruction modules into the skill's references. Recreate
#    the dir so a deleted/renamed .agents/*.md never leaves a stale reference behind.
rm -rf "$SKILL/references"
mkdir -p "$SKILL/references"
cp "$ROOT/.agents/"*.md "$SKILL/references/"
echo "Synced .agents/ -> $SKILL/references/"

# 2. Bundle the link validator alongside the skill so a bare --skill install
#    (which copies only the skill dir) is self-contained. Canonical copy lives in
#    plugins/obsidian-knowledge/scripts/.
mkdir -p "$SKILL/scripts"
cp "$ROOT/plugins/obsidian-knowledge/scripts/validate_links.py" "$SKILL/scripts/"
echo "Synced validate_links.py -> $SKILL/scripts/"
