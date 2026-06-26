#!/usr/bin/env bash
# Adversarial tests for the plugin hooks — run in CI. Locks in recall.sh and
# reflect-nudge.sh behavior so changes (including outside contributions) can't quietly
# regress them: the wrong Stop-hook output field, the journal.md.bak false-negative,
# the untracked-folder miss, etc. Uses subshells for cwd so the parent stays valid.
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RECALL="$ROOT/plugins/obsidian-knowledge/scripts/recall.sh"
NUDGE="$ROOT/plugins/obsidian-knowledge/scripts/reflect-nudge.sh"
fail=0
ok()  { printf 'ok   %s\n' "$1"; }
bad() { printf 'FAIL %s\n' "$1"; fail=1; }

newrepo() {
  local d; d="$(mktemp -d)"
  ( cd "$d" && git init -q && git config user.email t@t.co && git config user.name t \
      && mkdir -p .agents/learned && printf '# j\n' > .agents/learned/journal.md \
      && git add -A && git commit -qm base )
  printf '%s' "$d"
}

# ---------- recall.sh ----------
R="$(mktemp -d)"; mkdir -p "$R/.agents/learned"
printf '# Conventions\n> only comments\n' > "$R/.agents/learned/conventions.md"
out="$(CLAUDE_PROJECT_DIR="$R" bash "$RECALL")"
[ -z "$out" ] && ok "recall: silent on comment-only conventions" || bad "recall: should be silent on comment-only"

printf '## Rule\n- arXiv papers -> Papers/\n' >> "$R/.agents/learned/conventions.md"
out="$(CLAUDE_PROJECT_DIR="$R" bash "$RECALL")"
ev="$(printf '%s' "$out" | python3 -c "import json,sys;print(json.load(sys.stdin)['hookSpecificOutput']['hookEventName'])" 2>/dev/null || true)"
[ "$ev" = "SessionStart" ] && ok "recall: emits SessionStart additionalContext JSON" || bad "recall: missing/!SessionStart JSON ('$ev')"

python3 - "$R/.agents/learned/conventions.md" <<'PY'
import sys
open(sys.argv[1], "w").write("## big\n" + "x" * 20000 + "\n")
PY
out="$(CLAUDE_PROJECT_DIR="$R" bash "$RECALL")"
printf '%s' "$out" | grep -q 'truncated' && ok "recall: truncates an oversized conventions file" || bad "recall: missing size guard"
rm -rf "$R"

# ---------- reflect-nudge.sh ----------
fires() { printf '%s' "$1" | grep -q 'additionalContext'; }

# brand-new untracked folder -> fires
T="$(newrepo)"; ( cd "$T" && mkdir -p "ML/New Folder" && printf '# n\n' > "ML/New Folder/A Note.md" )
out="$(cd "$T" && bash "$NUDGE")"; fires "$out" && ok "nudge: fires for a brand-new untracked folder" || bad "nudge: missed brand-new untracked folder"
rm -rf "$T"

# clean tree -> silent
T="$(newrepo)"
out="$(cd "$T" && bash "$NUDGE")"; [ -z "$out" ] && ok "nudge: silent on a clean tree" || bad "nudge: should be silent on clean tree"
rm -rf "$T"

# note changed + journal.md modified -> silent (reflection recorded)
T="$(newrepo)"; ( cd "$T" && mkdir -p ML && printf '# n\n' > "ML/N.md" && git add -A && git commit -qm work \
   && printf 'edit\n' >> "ML/N.md" && printf 'entry\n' >> .agents/learned/journal.md )
out="$(cd "$T" && bash "$NUDGE")"; [ -z "$out" ] && ok "nudge: silent once journal.md is modified" || bad "nudge: should be silent when journal.md modified"
rm -rf "$T"

# note changed + journal.md.bak modified but journal.md clean -> still fires (the regression case)
T="$(newrepo)"; ( cd "$T" && mkdir -p ML && printf '# n\n' > "ML/N.md" && printf '# b\n' > .agents/learned/journal.md.bak \
   && git add -A && git commit -qm work && printf 'edit\n' >> "ML/N.md" && printf 'edit\n' >> .agents/learned/journal.md.bak )
out="$(cd "$T" && bash "$NUDGE")"; fires "$out" && ok "nudge: journal.md.bak does NOT silence the nudge" || bad "nudge: journal.md.bak wrongly silenced it"
rm -rf "$T"

[ "$fail" -eq 0 ] && echo && echo "All hook adversarial tests passed." || { echo; echo "Hook tests FAILED" >&2; }
exit "$fail"
