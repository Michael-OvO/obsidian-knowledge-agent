---
description: Show everything the Obsidian Knowledge Agent can do, with every command and an example
argument-hint: [optional: a command name to explain in depth, e.g. "research"]
---

If `$ARGUMENTS` names a specific command, explain THAT command in depth — what it does,
when to reach for it, and a worked example — then stop. Otherwise present this guide,
clean and skimmable (keep the grouping and the examples):

# Obsidian Knowledge Agent — what I can do

I turn anything — a link, a stray thought, a PDF, a whole syllabus — into notes worth
keeping, and I learn your vault's conventions as we go. Talk to me naturally ("save
this", "research X", "organize my inbox") or use a command:

## ▸ Start here
- `/obsidian-knowledge:setup` — set this folder up as a vault (branches, learning state, a dashboard, an Inbox).
- `/obsidian-knowledge:help [command]` — this guide. Add a name for detail, e.g. `… :help research`.

## ▸ Capture & build
- `/obsidian-knowledge:capture <thing>` — save one quick, clean note. e.g. `:capture https://arxiv.org/abs/1706.03762`
- `/obsidian-knowledge:ingest [what]` — build notes from `Inbox/` (or what you point at) at the right depth.
- `/obsidian-knowledge:research <topic>` — research from the web and write teaching notes with sources. e.g. `:research how RoPE positional encoding works`
- `/obsidian-knowledge:log <text>` — append a timestamped line to today's daily log.

## ▸ Improve & maintain
- `/obsidian-knowledge:polish [note|folder]` — improve existing notes in place (defaults to recently changed).
- `/obsidian-knowledge:refactor <change>` — reorganize safely and rewire links. e.g. `:refactor split the Transformers note`
- `/obsidian-knowledge:doctor [folder]` — health check: broken links, orphans, missing frontmatter.
- `/obsidian-knowledge:clean [message]` — commit changed notes, clear processed Inbox (with approval), push.

## ▸ Learn (I improve myself)
- `/obsidian-knowledge:reflect` — capture lessons from recent work and propose rule updates.
- `/obsidian-knowledge:evolve` — review and approve my proposed rule changes.

**Try this first:** `:setup` → drop a source in `Inbox/` → `:ingest` → `:polish` → `:reflect`.

What I've learned about this vault lives in `.agents/learned/` — plain markdown you can read or prune anytime.
