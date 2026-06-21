# Self-Evolution — The Learning Loop

> **For agents working in this vault.** This module makes the knowledge pipeline
> *self-evolving*: every ingestion run becomes a training example. You **recall**
> what was learned before you start, run the normal pipeline, then **reflect** to
> improve your own rules. No model training — you rewrite plain markdown.

This is the file-based learning model: the agent improves by editing inspectable,
git-tracked markdown, never by changing weights. Every change is a `git diff` you
(or the user) can read, approve, or revert.

---

## Where learned state lives

Per-vault, git-tracked, under `.agents/learned/`. The plugin/skill is the engine;
the vault holds what the engine learned about **this** vault.

| File | Role | Who writes it | Discipline |
|---|---|---|---|
| `journal.md` | Append-only log of every run: input, classification, corrections, fixes | You, automatically | **Append only.** Never edit or delete past entries. |
| `conventions.md` | Distilled, vault-specific rules that override defaults | You propose; user approves the diff | **Consolidate**, don't just append. Keep it tight. |
| `examples.md` | Few-shot input→classification decisions | You propose | Capped; most recent wins on conflict. |
| `skills/<name>.md` | Reusable playbooks for novel source/domain types | You write on novel input | One playbook per distinct input shape. |

If `.agents/learned/` does not exist yet, create it the first time you reflect.

---

## Rule precedence

When guidance conflicts, this is the order (highest wins):

1. **The user's explicit instructions in this session.**
2. **Core rules** in `.agents/*.md` (`style-guide`, `obsidian-conventions`,
   `vault-architecture`, `ingestion-workflow`).
3. **Learned `conventions.md`** — vault-specific overrides of defaults.
4. **Defaults** baked into the workflow.

Learned conventions refine the defaults; they never override a core rule or the
user. If a learned convention ever contradicts a core rule, prefer the core rule
and flag the contradiction in your next journal entry.

---

## Phase 0 — Recall (before you classify)

Before classifying the input in the ingestion workflow:

1. Read `.agents/learned/conventions.md` (if present) and treat it as active
   overrides for this run. *(In Claude Code this is auto-injected at session start
   by the `recall.sh` hook — but read it directly too; the hook is a convenience,
   not a guarantee.)*
2. Read `.agents/learned/examples.md` (if present) and use the closest matching
   input→classification rows as few-shot guidance.
3. Scan `.agents/learned/skills/` for a playbook whose trigger matches this input.
   If one matches, **follow it** instead of re-deriving the approach.

Recall is cheap and silent on a fresh vault (nothing to read).

---

## Phase 7 — Reflect & Evolve (after you finish)

Run this at the end of every ingestion, and immediately whenever the user
**corrects** you (a correction is the single most valuable signal — encode it).

### 1. Always: append to the journal

Append one dated entry to `.agents/learned/journal.md`. Never rewrite earlier
entries. Use this shape:

```markdown
## {ISO date} — {short label}

- **Input:** {what was ingested}
- **Classified as:** {profile} → {target path}
- **Corrections:** {what the user changed, or "none"}
- **Fixes:** {recurring link/structure/style fixes, or "none"}
- **Lesson:** {the durable, reusable takeaway — or "none this run"}
```

### 2. If there is a durable lesson: propose a rule change

A lesson is *durable* when it would change a **future** run, not just this one.
For each durable lesson, pick the right home:

- **A preference or override** ("this vault files arXiv papers under `ML/{Topic}/`,
  not `References/`"; "cap Mermaid diagrams at 2 per note") → edit
  `.agents/learned/conventions.md`. **Consolidate**: merge with related rules,
  rewrite for clarity, remove anything now contradicted. Do not let this file grow
  into a changelog — it is the current, minimal rule set.
- **A classification judgment call** (this kind of input maps to that profile) →
  add or update a row in `.agents/learned/examples.md`.
- **A whole new way to handle a novel input shape** (a source/domain type not
  covered by the workflow — e.g. legal casebooks, lab notebooks, podcast feeds) →
  write a playbook to `.agents/learned/skills/<kebab-name>.md` with a `trigger:`
  line describing when to use it and numbered steps. This is procedural memory: you
  never have to re-derive that approach again.

### 3. Surface rule changes for approval (two-tier autonomy)

- The **journal** entry is safe to write and commit freely — it is append-only.
- Changes to **`conventions.md` / `examples.md` / `skills/`** are *proposals*. Show
  the `git diff`, summarize each change in one line with the journal entry that
  motivated it, and let the user approve before committing. Do **not** silently
  commit rule changes. The `/obsidian-knowledge:evolve` command drives this review.

---

## Drift control (why this stays trustworthy)

Self-evolving agents fail by **drift**: stale, contradictory rules quietly making
output worse. Defenses, all built into the loop above:

- **Append-only journal** preserves the full history; nothing is silently lost.
- **Consolidation, not accumulation:** `conventions.md` is rewritten to stay minimal
  and consistent — it is a rule set, not a log.
- **Human-in-the-loop on rule changes:** every override is a reviewed `git diff`.
- **Core rules and the user always win** (see precedence).
- **Contradiction check:** if a learned rule fights a core rule, drop the learned
  one and note it in the journal.

---

## Portable vs. Claude-Code-native

The loop is defined here in instructions, so it works in **any** agent (Claude,
Codex, Cursor). In **Claude Code**, two hooks add automation on top:

- `SessionStart` → auto-recalls `conventions.md` into context.
- `Stop` → nudges you to reflect if notes changed but the journal is untouched.

In other tools, simply run recall at the start and reflect at the end yourself, or
invoke the `/obsidian-knowledge:reflect` equivalent. The hooks are convenience, not
correctness — the rules above are the source of truth.
