# Command Suite for the Obsidian Knowledge Agent — Design

**Date:** 2026-06-22
**Status:** Approved (brainstorming) → implementation

## Goal

Surface the agent's full capability as a clear, discoverable set of slash commands so a
new user can immediately *know what it can do* and *use it effectively*. Today only 4
commands exist (`capture`, `ingest`, `reflect`, `evolve`); much of the agent's power
(web research, concept canvas, quality pass, link validation, restructuring) is implied
in the workflow but never exposed.

## Decisions (from brainstorming)

- **12 focused commands in 4 groups** (not a few overloaded ones): focused commands are
  self-documenting in the picker and in `/help`; grouping keeps the count manageable.
- **Discovery:** a rich `/help` front-door command **and** a polished Commands section in
  the README. Kept consistent by a CI check.
- `log` = quick timestamped append to today's daily note.
- `polish` with no argument targets recently-changed notes.
- Build off current `origin/main` in an isolated worktree (Codex session active);
  preserve the README badge.

## The 12 commands

Existing (kept as-is, featured in `/help` + README): `capture`, `ingest`, `reflect`, `evolve`.

New (8):

| Group | Command | Purpose |
|---|---|---|
| Start here | `help` | Grouped guide: what the agent does, every command + example, a "try this first" path. With an arg, explains one command in depth. |
| Start here | `setup` | Initialize a folder as a vault: branches, `.agents/learned/`, `Inbox/`, `Dashboard.md`. Idempotent; commits. |
| Capture & build | `research` | Research a topic from the web, gather real sources, build teaching-quality notes (+ canvas for big topics). |
| Capture & build | `log` | Append a timestamped entry to today's daily note (`Daily/YYYY-MM-DD.md` or the vault's convention). |
| Improve & maintain | `polish` | Teaching-quality pass on existing notes; improve in place; show diffs. |
| Improve & maintain | `refactor` | Rename/move/split/merge safely and rewire every affected wikilink (validated before & after). |
| Improve & maintain | `doctor` | Health check: broken links, orphans, missing frontmatter, MISSING placeholders, broken canvas refs → proposed fixes. |
| Improve & maintain | `clean` | Commit changed notes, clear processed Inbox (with approval), push. |

## Command file conventions

Each command is `plugins/obsidian-knowledge/commands/<name>.md` with:
- YAML frontmatter: `description` (required, ≤ ~120 chars), `argument-hint` (when it takes args).
- A one-line intro, then numbered steps in the existing house voice.
- `$ARGUMENTS` for user input where relevant.
- Reference the relevant `.agents/*.md` doc(s); reuse the bundled `scripts/validate_links.py`.

Safety: `refactor`/`doctor`/`clean` never delete without approval; `refactor` always
validates links before and after; learned-rule changes still flow through `reflect`/`evolve`.

## Discoverability artifacts

- `help.md` embeds the grouped command list (it is the in-tool source of truth).
- README gains a **Commands** section: a grouped table (command · what it does · example) +
  a "try this first" line. Quickstart/install reference `/obsidian-knowledge:help`.

## Testing

- `scripts/validate_commands.py` (dependency-free), run in CI:
  1. Every `commands/*.md` has valid frontmatter delimiters and a non-empty `description`.
  2. Consistency: every command name appears in both `help.md` and `README.md`, and every
     `/obsidian-knowledge:<x>` referenced in `help.md`/`README.md` has a matching file — so
     the command set, the help guide, and the README can't silently drift.
- Existing checks still pass: `validate_manifests.py`, `validate_links.py` on
  `examples/output`, `bash -n`, skill-bundle sync.

## Out of scope (YAGNI)

- A standalone `canvas` command (canvas-building stays inside `ingest`/`research`/`polish`).
- Changes to the 4 existing commands beyond featuring them in help/README.
- No `plugin.json` change — commands auto-discover from `commands/`.
