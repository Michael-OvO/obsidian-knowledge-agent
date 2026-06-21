# Self-Evolving Obsidian Knowledge Agent + Claude Code Plugin — Design

**Date:** 2026-06-20
**Status:** Approved (brainstorming) → implementation

## Goal

Turn the Obsidian Knowledge Agent from a static prompt-pack into a genuinely
**self-evolving** agent (Hermes-style, file-based learning) and distribute it as
an official **Claude Code plugin + marketplace**, with the polish that earns wide
adoption.

Three asks, mapped to deliverables:

1. **Self-evolving like Hermes** → a recall→reflect learning loop that rewrites the
   agent's own markdown rules (no model training).
2. **Official Claude Code marketplace** → repo becomes a marketplace hosting one
   plugin (`.claude-plugin/marketplace.json` + `plugin.json` + hooks + commands).
3. **Worth 10K stars** → a working before/after demo, an overhauled README, and
   standard trust signals (CI, CONTRIBUTING, templates, CHANGELOG).

## Decisions (from brainstorming)

- **Evolution model:** memory + skill-growth loop (both living preference memory
  AND auto-generated domain playbooks).
- **Portability:** Claude-Code-native auto-trigger via hooks, with a portable
  instruction-driven fallback so Codex/Cursor get the loop too.
- **Distribution:** full plugin + self-hosted marketplace in this repo; keep the
  curl installer for non-Claude tools.
- **Autonomy:** two-tier — free append-only journal; distilled rule changes are
  surfaced as a git diff for human approval before commit.

## Core mechanism — the learning loop

Every ingestion run becomes a training example.

- **Phase 0 (Recall)** *(new, prepended to the pipeline):* before classifying,
  read learned state and let it shape the run.
- **Phases 1–6:** the existing ingest→compile→distribute pipeline, unchanged.
- **Phase 7 (Reflect)** *(new, appended):* append raw experience to a journal;
  propose distilled rule updates / new playbooks; surface for approval.

### Learned state lives in the *vault*, not the plugin

The plugin is the engine (installed once, globally). Learned state is per-vault and
git-tracked under `.agents/learned/`:

| File | Role | Writer | Drift control |
|---|---|---|---|
| `journal.md` | Append-only experience log (input, classification, corrections, link-fixes) | Agent, automatic | Append-only |
| `conventions.md` | Distilled vault-specific rules that override defaults | Agent proposes; user approves diff | Soft size cap; reflect **consolidates**, not just appends |
| `examples.md` | Few-shot input→classification decisions | Agent proposes | Capped, recent-wins |
| `skills/<name>.md` | Generated playbooks for novel source/domain types | Agent writes on novel input | Reused on future match |

**Precedence:** user's explicit instructions > core `.agents/*.md` > learned
`conventions.md` > defaults.

### Claude-Code-native automation (+ portable fallback)

The loop is defined in instructions (portable). Two hooks add native automation:

- **`SessionStart` hook** → `recall.sh` injects the vault's `conventions.md` into
  context automatically.
- **`Stop`/`SessionEnd` hook** → `reflect-nudge.sh` detects (via `git status`) that
  notes changed but the journal wasn't updated, and emits a non-blocking nudge to
  run `/obsidian-knowledge:reflect`.

A command hook runs a shell script, not the model — it influences the agent only by
returning text (additionalContext / systemMessage). That is exactly enough: inject
memory at start, nudge reflection at stop. Reasoning stays in the instructions.

## Repo layout (target)

```
obsidian-knowledge-agent/                 # repo root = the marketplace
├── .claude-plugin/marketplace.json       # this repo IS a marketplace
├── plugins/obsidian-knowledge/           # the plugin
│   ├── .claude-plugin/plugin.json
│   ├── skills/obsidian-knowledge/SKILL.md (+ references/*.md)
│   ├── commands/ ingest.md · reflect.md · evolve.md
│   ├── hooks/hooks.json                   # SessionStart + Stop
│   └── scripts/ recall.sh · reflect-nudge.sh · validate_links.py
├── AGENTS.md                              # tool-agnostic entry (Codex/Cursor)
├── .agents/                               # source of truth
│   ├── self-evolution.md                  # NEW: portable loop spec
│   ├── ingestion-workflow.md              # + Phase 0 recall, Phase 7 reflect
│   ├── style-guide.md
│   ├── obsidian-conventions.md
│   └── vault-architecture.md
├── install.sh                             # also seeds .agents/learned/ in vault
├── scripts/sync-skill.sh                  # .agents/ -> plugin skill references
├── examples/                              # worked run + before/after evolution demo
├── .github/                               # CI, issue/PR templates
├── CONTRIBUTING.md · CHANGELOG.md
└── README.md                              # overhauled
```

The `plugins/obsidian-knowledge/skills/obsidian-knowledge/references/*.md` are kept
in sync with `.agents/*.md` by `scripts/sync-skill.sh`.

## Install UX

- Claude Code: `/plugin marketplace add Michael-OvO/obsidian-knowledge-agent` then
  `/plugin install obsidian-knowledge@obsidian-knowledge-agent`.
- Any agent / non-Claude: the existing curl one-liner (`--skill`, vault path,
  `--both`).

## Deliverables for adoption ("10K stars")

- **Demo:** `examples/` gains a before/after — a wrong classification, a user
  correction, the learned `conventions.md`, and the corrected next run. Narrated in
  `examples/EVOLUTION.md`.
- **README overhaul:** hero line, architecture diagram, both install paths,
  comparison/feature table, badges.
- **Trust signals:** `CONTRIBUTING.md`, issue/PR templates, `CHANGELOG.md`, and a
  GitHub Actions CI that (a) validates plugin.json + marketplace.json and (b) runs
  the link validator.

## Testing strategy

LLM pipelines resist full automation, so:

1. **Manifest validator** (`scripts/validate_manifests.py`) — JSON parse + required
   fields for plugin.json and marketplace.json. Runs in CI.
2. **Link validator** (`validate_links.py`) — the previously-claimed-but-missing
   validator, now real; runs on the `examples/output` tree in CI.
3. **Example structure check** — assert the sample output tree exists/round-trips.
4. **Documented evolution scenario** — `examples/EVOLUTION.md` walks a correction →
   reflect → assert `journal.md` gained an entry and `conventions.md` gained the
   lesson.

## Explicitly out of scope (YAGNI)

- Full Hermes runtime: crons, `soul.md` personality, messaging gateways.
- Offline GEPA/DSPy genetic optimizer.

Both are heavy and off-domain for an Obsidian tool; can be added later.
