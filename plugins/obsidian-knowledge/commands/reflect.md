---
description: Reflect on recent work — log lessons to the journal and propose distilled rule updates for review
---

Run Phase 7 (Reflect & Evolve) from `.agents/self-evolution.md`.

1. Review what changed this session: `git --no-pager status` and `git --no-pager
   diff` on the vault, the conversation, and especially any **corrections** the user
   made (corrections are the highest-value signal).
2. **Append** a dated entry to `.agents/learned/journal.md` (append-only — never
   rewrite past entries). Create `.agents/learned/` first if it does not exist.
3. Identify durable lessons (ones that would change a *future* run). For each, pick
   the right home:
   - a preference/override → edit `.agents/learned/conventions.md` (consolidate;
     keep it a tight rule set, not a changelog);
   - a classification judgment → add/update a row in `.agents/learned/examples.md`;
   - a whole new input shape → write a playbook to
     `.agents/learned/skills/<kebab-name>.md` with a `trigger:` line and steps.
4. The journal entry can be committed freely. For `conventions.md` / `examples.md` /
   `skills/` changes, show the proposed diff, summarize each change in one line with
   the motivating journal entry, and let me approve before committing.
