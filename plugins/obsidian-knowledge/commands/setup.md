---
description: Set up this folder as a knowledge vault — branches, learning state, a dashboard, and an Inbox
argument-hint: [optional: domains/branches you want, e.g. "ML, Quant, Research"]
---

Set up the current folder as an Obsidian Knowledge Agent vault. Be idempotent — inspect
first and never clobber anything that already exists.

1. **Look first.** List what's here (folders, `AGENTS.md`, `.agents/`, existing notes). If
   there's already a structure, match it and only fill gaps.
2. **Branches.** Create top-level branch folders — from `$ARGUMENTS` if given, otherwise
   infer a sensible starter set from existing notes; if the vault is empty, propose a
   small default (a shared `References/` plus one or two domains) and confirm with me.
   Give each branch an `_index.md`.
3. **Learning state.** Ensure `.agents/learned/` exists with `journal.md`, `conventions.md`,
   `examples.md`, and a `skills/` folder — seed empty starters, never overwrite existing.
4. **Inbox + dashboard.** Create `Inbox/` and a `Dashboard.md` map-of-content that links the
   branches and explains the workflow in a line or two.
5. **Commit** the scaffold, then point me to `/obsidian-knowledge:help` and suggest dropping
   a first source into `Inbox/`.
