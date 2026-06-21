#!/usr/bin/env bash
set -euo pipefail

# Obsidian Knowledge Agent - installer
#
# Works two ways:
#   1) From a cloned repo:   ./install.sh [--skill | --both] [/path/to/vault]
#   2) Remotely (no clone):  curl -fsSL <raw>/install.sh | bash -s -- [args]
#
# Modes:
#   (default)  install AGENTS.md + .agents/ into an Obsidian vault   (needs a vault path)
#   --skill    install the Claude Code skill into ~/.claude/skills/  (no vault path needed)
#   --both     do both                                               (needs a vault path)

REPO="Michael-OvO/obsidian-knowledge-agent"
TARBALL="https://codeload.github.com/${REPO}/tar.gz/refs/heads/main"

usage() {
  cat <<'EOF'
Obsidian Knowledge Agent installer

Usage:
  install.sh [--skill | --both] [/path/to/your/vault]

  (no flag)   Install AGENTS.md + .agents/ into the given Obsidian vault.
  --skill     Install the Claude Code skill into ~/.claude/skills/ (no vault path).
  --both      Install the skill AND the vault files (vault path required).

Examples:
  ./install.sh ~/Vaults/Knowledge
  curl -fsSL https://raw.githubusercontent.com/Michael-OvO/obsidian-knowledge-agent/main/install.sh | bash -s -- --skill
  curl -fsSL https://raw.githubusercontent.com/Michael-OvO/obsidian-knowledge-agent/main/install.sh | bash -s -- ~/Vaults/Knowledge
EOF
}

# ---- parse args ----
MODE="vault"
VAULT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --skill) MODE="skill" ;;
    --both)  MODE="both" ;;
    --vault) MODE="vault" ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "Unknown option: $1" >&2; usage; exit 1 ;;
    *) VAULT="$1" ;;
  esac
  shift
done

# ---- resolve source: local checkout if present, else download the repo ----
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || true)"
CLEANUP=""
if [[ -n "$SELF_DIR" && -f "$SELF_DIR/AGENTS.md" && -d "$SELF_DIR/.agents" ]]; then
  SRC="$SELF_DIR"
else
  command -v curl >/dev/null 2>&1 || { echo "Error: curl is required for remote install." >&2; exit 1; }
  command -v tar  >/dev/null 2>&1 || { echo "Error: tar is required for remote install."  >&2; exit 1; }
  TMP="$(mktemp -d)"; CLEANUP="$TMP"
  echo "Fetching $REPO ..."
  curl -fsSL "$TARBALL" | tar -xz -C "$TMP"
  SRC="$(find "$TMP" -maxdepth 1 -type d -name 'obsidian-knowledge-agent-*')"
  [[ -n "$SRC" && -f "$SRC/AGENTS.md" ]] || { echo "Error: download failed." >&2; exit 1; }
fi
cleanup() { [[ -n "$CLEANUP" ]] && rm -rf "$CLEANUP"; return 0; }
trap cleanup EXIT

install_vault() {
  local vault="$1"
  if [[ -z "$vault" ]]; then
    echo "Error: a vault path is required for this mode." >&2
    echo "       e.g. install.sh ~/Vaults/Knowledge   (or use --skill for the skill only)" >&2
    exit 1
  fi
  if [[ ! -d "$vault" ]]; then
    echo "Error: '$vault' is not a directory." >&2
    exit 1
  fi
  cp "$SRC/AGENTS.md" "$vault/AGENTS.md"
  mkdir -p "$vault/.agents"
  cp "$SRC/.agents/"*.md "$vault/.agents/"
  mkdir -p "$vault/Inbox"
  seed_learned "$vault"
  echo "Installed vault files (AGENTS.md, .agents/, .agents/learned/, Inbox/) into: $vault"
}

# Seed the per-vault self-evolution state. Never clobbers existing learned files.
seed_learned() {
  local vault="$1"
  mkdir -p "$vault/.agents/learned/skills"
  [[ -e "$vault/.agents/learned/skills/.gitkeep" ]] || : > "$vault/.agents/learned/skills/.gitkeep"

  if [[ ! -f "$vault/.agents/learned/journal.md" ]]; then
    cat > "$vault/.agents/learned/journal.md" <<'EOF'
# Learning Journal

> Append-only log of every ingestion run. The agent adds one dated entry per run;
> past entries are never edited or deleted. See `.agents/self-evolution.md`.
EOF
  fi

  if [[ ! -f "$vault/.agents/learned/conventions.md" ]]; then
    cat > "$vault/.agents/learned/conventions.md" <<'EOF'
# Learned Conventions

> Distilled, vault-specific rules the agent has learned. These override the
> defaults in `.agents/*.md`, but never the core rules or your explicit
> instructions. The agent proposes changes here as a git diff for you to approve.
>
> Empty for now — the agent fills this in as it learns your vault.
EOF
  fi

  if [[ ! -f "$vault/.agents/learned/examples.md" ]]; then
    cat > "$vault/.agents/learned/examples.md" <<'EOF'
# Classification Examples

> Few-shot input -> classification decisions the agent has learned, so it
> classifies new material the way you prefer. The agent appends rows here.

| Input signature | Classified as | Target |
|---|---|---|
EOF
  fi
}

install_skill() {
  local dest="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
  mkdir -p "$dest"
  rm -rf "$dest/obsidian-knowledge"
  cp -R "$SRC/plugins/obsidian-knowledge/skills/obsidian-knowledge" "$dest/"
  echo "Installed Claude Code skill 'obsidian-knowledge-ingest' into: $dest/obsidian-knowledge"
  echo
  echo "Tip: for slash commands (/obsidian-knowledge:ingest, :reflect, :evolve) and the"
  echo "self-evolution hooks, install the full plugin instead of the bare skill:"
  echo "  /plugin marketplace add Michael-OvO/obsidian-knowledge-agent"
  echo "  /plugin install obsidian-knowledge@obsidian-knowledge-agent"
}

case "$MODE" in
  vault) install_vault "$VAULT" ;;
  skill) install_skill ;;
  both)  install_vault "$VAULT"; install_skill ;;
esac

echo
echo "Done. Drop a syllabus, paper set, book TOC, or topic brief into your vault's Inbox/,"
echo "then ask your agent to \"ingest the material in Inbox into the vault\"."
echo
echo "The agent recalls what it learned at the start of each run and reflects at the end —"
echo "watch .agents/learned/ grow as it adapts to your vault."
