---
description: Tidy and sync — commit changed notes, clear processed Inbox (with approval), and push
argument-hint: [optional: a commit message]
---

Tidy up and sync the vault to git. Respect every boundary — never touch `.obsidian/`, never
delete without approval.

1. **Survey.** Run `git --no-pager status` and group the changes (new notes, edits, learned-state
   changes) into a short summary.
2. **Commit.** Stage and commit the note changes with `$ARGUMENTS` as the message, or a clear
   inferred one (e.g. `notes: add 3 ML notes, fix links`). Keep any pending learned-rule changes
   as a separate `chore(learn):` commit — see `/obsidian-knowledge:evolve`.
3. **Inbox.** If `Inbox/` still holds material that has already been processed, offer to clear it
   (move, archive, or delete) — only with my explicit approval.
4. **Push** if a remote exists and I haven't said otherwise. Report what was committed and pushed.
