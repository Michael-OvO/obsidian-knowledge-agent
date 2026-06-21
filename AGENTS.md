# AGENTS.md — Obsidian Knowledge Agent

> **For any AI agent (Codex, Claude, Cursor, …) working in this vault.** Read this file first, then follow the instruction modules in `.agents/`.

This vault has a knowledge agent that helps turn anything — a stray thought, a link, a PDF, a transcript, a whole syllabus or book — into notes worth keeping. It works for any subject and any vault: research, coursework, work projects, reading, personal knowledge. It does as much or as little structuring as the material actually needs.

The agent has one job: **leave the vault a little more useful than it found it.** Everything below is in service of that, not the other way around.

---

## How to work

Three principles sit above every rule in `.agents/`:

1. **Match the effort to the material.** A link or a one-line idea becomes a single clean note — no folders, no index, no ceremony. A small reading set becomes a few notes and a light index. Only a genuinely large, structured input (a syllabus, a book, a big paper collection) earns the full scaffold with a concept-graph canvas. Default to the lightest touch that does the job, and escalate only when the material clearly asks for it. See "Choose the altitude" in `.agents/ingestion-workflow.md`.

2. **Follow the vault you're in.** Before creating anything, look at how this vault is already organized — its folders, naming, frontmatter, link style — and fit in. The branches below are sensible defaults for an empty vault; in an existing vault, match what's there rather than imposing a new taxonomy. What the agent learns about a vault's real shape lives in `.agents/learned/`.

3. **Stay natural and low-friction.** Respond to plain requests ("save this", "make a note on X", "organize my inbox", "remember this", "research Y and write it up"), not just formal commands. Do the obvious thing; only stop to ask when an action is destructive or genuinely ambiguous.

---

## What This Vault Is

A personal knowledge base in [Obsidian](https://obsidian.md/) — structured, teaching-quality notes, organized however suits the work. The branches below are **example defaults**; rename, add, remove, or ignore them to fit your domains, and match an existing vault's structure when there is one.

| Branch | Content | Path |
|---|---|---|
| **School** | Academic coursework by semester | `School/{Semester}/{Course}/` |
| **ML** | Machine learning topics | `ML/{Topic}/` |
| **Quant** | Quantitative finance | `Quant/{Topic}/` |
| **References** | Shared foundational concepts | `References/{Concept}.md` |
| **Inbox** | Raw material staging (transient) | `Inbox/` |

These are illustrative. A work vault might use `Projects/`, `Meetings/`, `People/`; a research vault `Papers/`, `Ideas/`, `Experiments/`. See `.agents/vault-architecture.md`.

---

## Instruction Files

| File | Scope | Description |
|---|---|---|
| `.agents/style-guide.md` | All note writing | Teaching-note voice and quality standard |
| `.agents/ingestion-workflow.md` | Knowledge ingestion | Full workflow: recall → classify → scaffold → write → review → commit → reflect |
| `.agents/self-evolution.md` | Learning loop | Recall before a run, reflect after; how the agent improves its own rules |
| `.agents/obsidian-conventions.md` | All vault work | YAML frontmatter, wikilinks, file naming, canvas rules |
| `.agents/vault-architecture.md` | Vault structure | Folder roles and cross-linking strategy |

**Read order for ingestion tasks:** `style-guide.md` → `self-evolution.md` → `ingestion-workflow.md` (which references the others as needed).

**Read order for general vault work:** `obsidian-conventions.md` → `style-guide.md`.

---

## Core Rules

### 1. Teach naturally
Notes must build mental models, but the body should read like a human note rather than a template. Keep metadata in YAML or `_index.md` files, use natural headings, and make the logic visible without exposing rubric labels. In STEM domains, default to scientific explanation of problem, mechanism, assumptions, and limits rather than humanities-style argument structure. See `.agents/style-guide.md`.

### 2. YAML frontmatter on every note
Minimum: `tags` (array) and `created` (ISO date). See `.agents/obsidian-conventions.md` for field conventions.

### 3. Wikilinks for all internal links
Use `[[path/to/note]]` syntax. Inside tables, escape alias pipes as `[[path\|alias]]`. Never use bare Markdown links for internal vault files. See `.agents/obsidian-conventions.md`.

### 4. Inbox is transient
`Inbox/` is a staging area. Process material promptly and clear it by moving, archiving, or deleting with explicit user approval. Never leave processed material in Inbox.

### 5. References are shared
`References/` holds concepts that span multiple branches. Link to existing reference notes rather than duplicating. Add new anchor sources to existing notes when applicable.

### 6. Recall before, reflect after
This vault is self-evolving. **Before** a run, read `.agents/learned/` (conventions, examples, playbooks) and apply what was learned. **After** a run — and immediately whenever the user corrects you — append a journal entry and propose any durable rule updates for review. The full loop and its drift-control rules live in `.agents/self-evolution.md`. Learned state lives in `.agents/learned/` and is git-tracked; rule changes are surfaced as a diff for approval, never committed silently.

---

## Boundaries

- **Never delete files without explicit user approval** — move or archive instead
- **Never modify `.obsidian/`** — this is Obsidian's internal config directory
- **Agent-specific config dirs are not committed** — `.claude/`, `.cursor/`, `.windsurf/`, `.aider/`, etc. are gitignored. Only `.agents/` is shared and tracked.
- **Respect existing frontmatter** — add fields, don't remove or overwrite existing ones without reason

---

## Agent-Specific Configuration

Tool-specific config may live in gitignored locations such as `.claude/`, `.cursor/`, `.github/copilot-instructions.md`, or `.{agent}/`.

Shared instructions belong in `.agents/`. Agent-specific overrides should extend these rules, not replace them.
