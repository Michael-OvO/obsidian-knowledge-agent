# Contributing

Thanks for helping improve the Obsidian Knowledge Agent! This repo is small and the
contribution loop is fast.

## How the repo is organized

- **`.agents/` is the single source of truth.** The pipeline rules, style guide,
  conventions, and the self-evolution loop all live here as plain markdown.
- The Claude Code plugin lives under **`plugins/obsidian-knowledge/`**. Its skill
  references (`skills/obsidian-knowledge/references/*.md`) are **generated** from
  `.agents/` by [`scripts/sync-skill.sh`](scripts/sync-skill.sh) — never edit them by
  hand.
- The repo root doubles as a **Claude Code marketplace**
  (`.claude-plugin/marketplace.json`).

## Making a change

1. Edit the canonical file in `.agents/` (or the plugin's `commands/`, `hooks/`,
   `scripts/`).
2. If you touched `.agents/`, re-sync the skill references:
   ```bash
   bash scripts/sync-skill.sh
   ```
3. Run the checks CI runs:
   ```bash
   python3 scripts/validate_manifests.py
   python3 plugins/obsidian-knowledge/scripts/validate_links.py examples/output
   for f in install.sh scripts/*.sh plugins/obsidian-knowledge/scripts/*.sh; do bash -n "$f"; done
   ```
4. Open a PR. CI must be green.

## Guidelines

- **Keep `.agents/` and the plugin in lockstep.** A change to a rule should be one PR
  that edits `.agents/` and re-runs the sync script.
- **Don't break the manifests.** `plugin.json` and `marketplace.json` are validated in
  CI; keep `name` fields consistent.
- **Match the existing voice.** Instruction modules are terse and imperative; notes
  follow the teaching-note style guide.
- **New input types** belong as playbooks in a user's `.agents/learned/skills/`, not
  hard-coded into the workflow — unless they're broadly useful, in which case propose
  adding them to `.agents/ingestion-workflow.md`.

## Reporting bugs / ideas

Use the issue templates. For pipeline-quality issues, include the input you ingested
and what the agent produced versus what you expected.
