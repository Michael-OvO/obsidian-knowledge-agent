# Worked Example: Self-Evolution

This shows the learning loop in action across two runs of the same input — how a
single correction becomes a durable rule the agent applies automatically next time.

## Run 1 — first ingestion (no learned state yet)

The agent ingests [`Inbox/positional-encoding-brief.md`](Inbox/positional-encoding-brief.md)
as a **Topic Build** and produces [`output/ML/Positional Encoding/`](output/ML/Positional%20Encoding).
Reasonably — but not yet knowing this vault's taste — it creates a **collection-local**
concept note at `ML/Positional Encoding/References/Positional Encoding.md`.

> The committed [`output/`](output/) tree **is** this Run 1 state — that's why the
> concept note still lives inside the collection. We don't commit a second "after"
> tree; the improvement is captured as a *rule* (below) that the agent applies on the
> next run, which is the whole point of file-based learning.

## The correction

You move that concept into the **vault-root** `References/` and link to it instead:

> "Positional encoding is foundational and reused across ML collections — it belongs
> in the shared `References/`, not duplicated inside each topic."

## Reflect (Phase 7) — the lesson is captured

The agent appends to [`learned/journal.md`](learned/journal.md):

    ## 2026-03-02 — Positional Encoding correction
    - Corrections: moved the concept note to vault-root References/ and linked to it.
    - Lesson: foundational ML concepts go in vault-root References/; collections link, not copy.

…and proposes a one-line rule in [`learned/conventions.md`](learned/conventions.md),
which you approve as a `git diff`:

```diff
+ ## Shared concepts
+ - Foundational ML concepts (positional encoding, attention, embeddings, …) live in
+   the vault-root References/. Collections LINK to them; no local copies.
```

## Run 2 — the agent applies what it learned

On the next ingestion, the Claude Code `SessionStart` hook auto-recalls
`conventions.md`, so when the agent meets another foundational concept it **links to
the vault-root `References/` from the start** — no correction needed.

That is the whole point: **the agent compounds.** Every correction becomes a durable
rule, captured transparently as a reviewable markdown diff in your git history, and
applied automatically on the next run.

> The `learned/` files here are a committed illustration. In a real vault they live at
> `.agents/learned/` and the installer seeds empty starters for you.
