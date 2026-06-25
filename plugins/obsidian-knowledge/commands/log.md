---
description: Append a quick timestamped entry to today's daily log
argument-hint: <what to log, e.g. "shipped the parser, started tests">
---

Append `$ARGUMENTS` as a timestamped entry to today's daily log. Keep it instant — no ceremony.

1. **Find today's log.** If the vault already uses daily notes, follow that location and
   naming. Otherwise use `Daily/{YYYY-MM-DD}.md` — create `Daily/` and the file if needed,
   with minimal frontmatter (`tags: [daily]`, `created`).
2. **Append** a line under a `## Log` section: `- HH:MM — {entry}`. Never rewrite earlier
   entries.
3. If the entry clearly refers to a note or project, add a wikilink to it. Don't expand a
   log line into a full note — that's `/obsidian-knowledge:capture`.
4. Confirm in one line where it went.
