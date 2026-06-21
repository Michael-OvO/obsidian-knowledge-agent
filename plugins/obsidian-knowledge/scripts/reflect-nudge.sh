#!/usr/bin/env bash
# Stop hook: nudge the agent to reflect after it changed notes but left the
# learning journal untouched. Non-blocking — just a reminder. Self-limiting:
# once the agent appends to journal.md (i.e. reflection has started), the journal
# shows as dirty and the nudge goes quiet.
set -euo pipefail

PROJECT="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$PROJECT" 2>/dev/null || exit 0

# Only act inside a git repo that has been set up as an OKA vault.
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
[ -d ".agents/learned" ] || exit 0

# Did this session change any markdown notes outside the learned/ dir?
# Notes:
#  - --untracked-files=all expands untracked DIRECTORIES into individual files;
#    without it git collapses a brand-new folder to a single "?? ML/" entry and
#    the .md match below would miss every note in it (the common first-run case).
#  - git quotes paths containing spaces in porcelain output (e.g. "ML/Some Note.md"),
#    and Obsidian filenames are full of spaces — so tolerate an optional closing
#    quote (or a rename arrow) after the .md, not just end-of-line.
if ! git status --porcelain --untracked-files=all 2>/dev/null \
     | grep -v '\.agents/learned/' \
     | grep -Eq '\.md("| ->|$)'; then
  exit 0
fi

# Has reflection already been recorded this session? Suppress the nudge only when the
# journal is *tracked and changed* (staged or modified). An untracked, freshly-seeded
# journal is NOT reflection — it must not silence the nudge.
JLINE="$(git status --porcelain -- '.agents/learned/journal.md' 2>/dev/null | head -1 || true)"
case "$JLINE" in
  "" | "??"*) : ;;   # absent or untracked seed -> reflection not yet done; allow nudge
  *) exit 0 ;;       # tracked + changed -> reflection recorded; stay quiet
esac

MSG="obsidian-knowledge: you changed some notes this session. If anything is worth remembering for next time, /obsidian-knowledge:reflect will capture it — totally optional."
printf '{"systemMessage": "%s"}\n' "$MSG"
