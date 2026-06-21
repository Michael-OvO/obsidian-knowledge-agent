# Worked Example: Topic Build

This shows one run of the pipeline on a **Topic Build** input.

- **Input:** [`Inbox/positional-encoding-brief.md`](Inbox/positional-encoding-brief.md) — a short topic brief.
- **Output:** [`output/ML/Positional Encoding/`](output/ML/Positional%20Encoding) — a small collection with an index, one content note, and one shared concept note.

The content note shows the kind of **artifacts a technical note reaches for when they teach**: a runnable code block, a LaTeX equation, and a Mermaid diagram. The output here is illustrative and deliberately small — a full run would scaffold more notes and, for collections with 3+ units, a concept-graph canvas.

> This `output/` is the **Run 1 (before-correction) snapshot** used by the evolution demo below — that's why the shared concept still sits in a collection-local `References/`. See `EVOLUTION.md` for how the agent learns to file it differently next time.

## See the agent learn

[`EVOLUTION.md`](EVOLUTION.md) walks the **self-evolution loop** on this same input:
a first run, a correction, the lesson captured in [`learned/`](learned/), and a second
run where the agent applies what it learned — no correction needed.
