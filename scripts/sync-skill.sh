#!/usr/bin/env bash
set -euo pipefail

# Keep the Claude Code skill's bundled reference docs in sync with the
# canonical instruction modules in .agents/. Run this after editing .agents/.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/plugins/obsidian-knowledge/skills/obsidian-knowledge/references"
mkdir -p "$DEST"
cp "$ROOT/.agents/"*.md "$DEST/"
echo "Synced .agents/ -> plugins/obsidian-knowledge/skills/obsidian-knowledge/references/"
