#!/usr/bin/env bash
# Stop hook: gently remind the agent to reflect when notes changed this session but
# the learning journal is untouched. Emitted as Stop `additionalContext` — non-blocking
# model-visible feedback (NOT decision:block, so it never forces continuation). The
# model can act on it (e.g. offer /obsidian-knowledge:reflect). Self-limiting: once
# the journal is updated (tracked + changed), the reminder goes quiet.
set -euo pipefail

PROJECT="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$PROJECT" 2>/dev/null || exit 0

# Only act inside a git repo that has been set up as an OKA vault.
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
[ -d ".agents/learned" ] || exit 0

# One status scan, reused for both checks. --untracked-files=all expands brand-new
# untracked folders into individual files (else git collapses them to "?? dir/" and
# the .md match below would miss every note in a new folder — the common first run).
STATUS="$(git status --porcelain --untracked-files=all 2>/dev/null || true)"
[ -n "$STATUS" ] || exit 0

# A changed markdown note outside .agents/learned/?  The learned/ exclusion is anchored
# to the path field (2 status chars + a space, then an optional quote) so a note that
# merely mentions that string in its name isn't excluded. git quotes paths containing
# spaces, so tolerate a closing quote / rename arrow after the .md.
if ! printf '%s\n' "$STATUS" \
     | grep -Ev '^.. "?\.agents/learned/' \
     | grep -Eq '\.md("| ->|$)'; then
  exit 0
fi

# Reflection already recorded this session? Suppress only when the journal is TRACKED
# and changed; an untracked (freshly-seeded) journal must NOT silence the nudge.
JLINE="$(printf '%s\n' "$STATUS" | grep -E '^.. "?\.agents/learned/journal\.md' | head -1 || true)"
case "$JLINE" in
  "" | "??"*) : ;;   # absent or untracked seed -> not yet reflected; allow the nudge
  *) exit 0 ;;       # tracked + changed -> reflection recorded; stay quiet
esac

MSG="obsidian-knowledge: notes changed this session but the learning journal is untouched. If anything here is worth remembering for next time, consider offering to run /obsidian-knowledge:reflect — optional."
printf '{"hookSpecificOutput": {"hookEventName": "Stop", "additionalContext": "%s"}}\n' "$MSG"
