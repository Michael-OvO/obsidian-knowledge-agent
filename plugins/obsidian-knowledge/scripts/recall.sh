#!/usr/bin/env bash
# SessionStart hook: auto-recall the vault's learned conventions into context.
#
# The agent's distilled, vault-specific rules live in .agents/learned/conventions.md
# (git-tracked, per-vault). Surfacing them at session start means the agent applies
# what it has learned without having to remember to read the file. Stays silent when
# there is nothing substantive to recall, so fresh vaults are unaffected.
set -euo pipefail

PROJECT="${CLAUDE_PROJECT_DIR:-$PWD}"
CONV="$PROJECT/.agents/learned/conventions.md"

[ -f "$CONV" ] || exit 0

# Skip unless the file has at least one substantive (non-comment, non-blank) line.
grep -qvE '^[[:space:]]*(#|>|<!--|$)' "$CONV" || exit 0

# Emit conventions as SessionStart additionalContext. Prefer python3 for safe JSON
# escaping; fall back to plain stdout (also added to context for SessionStart).
if command -v python3 >/dev/null 2>&1; then
  python3 - "$CONV" <<'PY'
import json, sys
text = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
# Guard against an oversized conventions file inflating context every session.
LIMIT = 16000
if len(text) > LIMIT:
    text = text[:LIMIT] + "\n\n…(truncated — consolidate .agents/learned/conventions.md)"
msg = (
    "# Learned vault conventions (auto-recalled by obsidian-knowledge)\n"
    "Distilled from past ingestion runs in THIS vault. They refine the default rules, "
    "but never override a core rule in .agents/*.md or your explicit instructions this "
    "session. Apply them when ingesting or editing notes.\n\n" + text
)
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": msg,
}}))
PY
else
  echo "# Learned vault conventions (obsidian-knowledge) — refine the defaults; never"
  echo "# override a core .agents/*.md rule or your explicit instructions. Apply when ingesting:"
  head -c 16000 "$CONV"
  if [ "$(wc -c < "$CONV")" -gt 16000 ]; then
    printf '\n\n…(truncated — consolidate .agents/learned/conventions.md)\n'
  fi
fi
