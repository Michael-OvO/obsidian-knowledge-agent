---
description: Review and approve the agent's proposed updates to its own learned rules
---

Show me the pending self-evolution changes and walk me through approving them.

1. Run `git --no-pager diff -- .agents/learned/` to surface proposed changes to
   `conventions.md`, `examples.md`, and `skills/`.
2. For each change, summarize it in one line and cite the `journal.md` entry that
   motivated it (read the latest entries for context).
3. Check it against rule precedence in `.agents/self-evolution.md`: a learned rule
   must not contradict a core rule in `.agents/*.md` or the user's stated
   preferences. Flag any that do.
4. For each: ask whether to **keep**, **edit**, or **discard**.
5. Commit approved changes with `chore(learn): <one-line summary>`. Revert discarded
   ones (`git checkout -- <path>`). Leave the journal untouched — it is the record.
