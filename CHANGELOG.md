# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/), and the project aims to follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Fixed — validator edge cases
- **`validate_manifests.py`**: a `hooks`/`commands`/`skills` path pointing into a
  dot-directory (e.g. `./.config/hooks.json`) was mangled by `str.lstrip("./")` — which
  strips a *set of characters*, not a prefix, so it ate the leading dot of the dir — and
  the path was wrongly reported as missing even when it existed. Now strips only a single
  leading `./`. Locked in by a new adversarial test in `test_validators.py`.
- **`validate_commands.py`**: read `README.md`, `help.md`, and the command files with the
  platform-default encoding, so it crashed on Windows (cp1252) on the em-dashes/arrows they
  contain. Now forces UTF-8, matching the guard already in `validate_manifests.py`.
- **`validate_links.py`**: same UTF-8 hardening on note reads, for consistent behavior
  across platforms.

## [2.2.0] — 2026-06-25

### Changed — bolder README, adaptive setup
- **README restyle**: rewritten in a bold, product-first voice — a hero tagline, a
  before/after, an "altitude ladder", one tight command table, and a punchy FAQ. Keeps
  the self-evolution section and the any-agent install; drops nothing functional.
- **Adaptive `setup`**: now detection-first with three explicit modes — **SCAFFOLD** an
  empty folder, **ADOPT** an existing vault (read its conventions, impose nothing, fill
  only the gaps, seed detected conventions for approval), or **RESUME** an already-set-up
  vault (report status, route to work, don't re-scaffold).
- **Bootstrap-aware `ingest` / `capture`**: in a folder that isn't a vault yet, they offer
  `/obsidian-knowledge:setup` instead of failing.

### Fixed
- Caught the plugin/marketplace manifests up to the CHANGELOG: all four were still
  pinned at `2.0.0` despite the 2.1.0 command-suite release.

## [2.1.0] — 2026-06-22

### Added — a full, discoverable command suite
- Grew from 4 to **12 commands in 4 groups**, surfacing the agent's full power:
  - **Start here**: `help` (grouped in-tool guide; `:help <command>` for detail), `setup`
    (initialize a vault — branches, learning state, dashboard, Inbox).
  - **Capture & build**: `capture`, `ingest`, **`research`** (research a topic from the web
    and write teaching notes with sources), **`log`** (timestamped daily-log entry).
  - **Improve & maintain**: **`polish`** (teaching-quality pass on existing notes),
    **`refactor`** (rename/move/split/merge and rewire every wikilink), **`doctor`**
    (health check — broken links, orphans, missing frontmatter), **`clean`** (commit /
    clear processed Inbox / push).
  - **Learn**: `reflect`, `evolve`.
- A polished **Commands** section in the README, plus `validate_commands.py` in CI that
  keeps the command files, `/help`, and the README from drifting out of sync.

## [2.0.0] — 2026-06-20

### Added — natural, adaptive, general-purpose
- **Altitude tiers**: the agent matches effort to the material — **Capture** (one clean
  note), **Small collection** (a few notes + a light index), or **Full build** (the full
  scaffold + concept-graph canvas). The heavy pipeline is now opt-in by signal, not
  forced on every input.
- **Fits the vault it's in**: detects and matches an existing vault's folders, naming,
  and frontmatter instead of imposing the `School/ML/Quant` taxonomy (now just defaults
  for an empty vault). Works for any subject.
- **Natural triggers + a quick-capture command** (`/obsidian-knowledge:capture`): responds
  to plain requests like "save this", "make a note on X", "organize my inbox".
- **Softened the three-artifact floor**: technical notes use code / equations / diagrams
  where they genuinely teach, not to satisfy a quota; short and non-technical notes need
  none.

### Added — the agent now self-evolves
- **Recall → reflect learning loop** ([`.agents/self-evolution.md`](.agents/self-evolution.md)):
  the agent reads what it learned about a vault before each run (Phase 0, Step 0) and
  reflects afterward (Phase 7) to improve its own rules.
- **Per-vault learned state** under `.agents/learned/`: an append-only `journal.md`,
  a distilled `conventions.md`, few-shot `examples.md`, and generated playbooks in
  `skills/`. Seeded automatically by the installer.
- **Two-tier autonomy**: the journal is written freely; rule changes are surfaced as a
  git diff for approval, with consolidation and precedence rules to prevent drift.

### Added — official Claude Code plugin + marketplace
- This repo is now a **Claude Code marketplace** (`.claude-plugin/marketplace.json`)
  hosting the **`obsidian-knowledge` plugin** (`plugins/obsidian-knowledge/`).
- Install via `/plugin marketplace add Michael-OvO/obsidian-knowledge-agent` then
  `/plugin install obsidian-knowledge@obsidian-knowledge-agent`.
- **Slash commands**: `/obsidian-knowledge:capture`, `:ingest`, `:reflect`, `:evolve`.
- **Hooks**: `SessionStart` auto-recalls learned conventions; `Stop` nudges reflection
  when notes changed but the journal is untouched.

### Added — quality & trust
- A real **wikilink validator** (`validate_links.py`) — previously claimed, now shipped
  — plus a **manifest validator** (`validate_manifests.py`), both run in **CI**.
- `examples/EVOLUTION.md` — a worked before/after that demonstrates the loop.
- `CONTRIBUTING.md`, a CHANGELOG, and issue/PR templates.

### Changed
- The skill moved from `skills/` to `plugins/obsidian-knowledge/skills/`; the installer
  and `sync-skill.sh` paths were updated accordingly. The bare-skill and vault installs
  still work as before.

## [1.0.0] — 2026-06-20

### Added
- Initial release: the `ingest → compile → distribute` pipeline, the teaching-note
  style guide, Obsidian conventions, vault architecture, a worked example, and a
  one-line installer.
