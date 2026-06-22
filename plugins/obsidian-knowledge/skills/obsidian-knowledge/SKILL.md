---
name: obsidian-knowledge
description: Use for any knowledge work in an Obsidian vault — capturing a quick note or link, organizing an Inbox, or turning bigger material (PDFs, docx, slides, syllabi, papers, transcripts, URL lists) into structured, teaching-quality notes. Works for any subject, adapts to the vault it's in, and does as much or as little structuring as the material needs, then reflects on each run to improve its own rules. Trigger on requests like "save this", "make a note on X", "remember this", "organize my inbox", "ingest", "build notes from", "research X and write it up", or "add this to the vault".
---

# Obsidian Knowledge Ingest

This skill helps with any knowledge work in an Obsidian vault — from saving a single
link to building a whole course's notes. It does as much or as little structuring as
the material needs, fits the vault it's in, **recalls** what it learned about that
vault before each run, and **reflects** afterward to get better over time — without
any model training.

**Match the effort to the material.** Decide the altitude first (see "Choose the
altitude" in the workflow): a **Capture** is one clean note, a **Small collection** is
a few notes plus a light index, and only a genuinely large, structured input earns the
**Full build** below. Default to the lightest touch; escalate only when the material
clearly asks for it.

## How to use it

1. **Read the rules first.** Read these bundled references in order:
   - `references/style-guide.md` — the teaching-note voice and quality bar
   - `references/self-evolution.md` — the recall → reflect learning loop
   - `references/obsidian-conventions.md` — frontmatter, wikilinks, naming, LaTeX, Mermaid, canvas
   - `references/vault-architecture.md` — folder roles and branch boundaries
   - `references/ingestion-workflow.md` — the full workflow you will execute

   If the target vault already has these files at `.agents/` in its root, prefer
   those — they may be customized for that vault.

2. **Recall (Phase 0, Step 0).** Before classifying, read `.agents/learned/` if it
   exists: apply `conventions.md`, use `examples.md` as few-shot classification
   guidance, and follow any matching playbook in `learned/skills/`. Silent on a
   fresh vault.

3. **Execute the workflow** in `references/ingestion-workflow.md`:
   - **Phase 0 — Ingest:** classify the input profile and extract a structural map.
   - **Phases 1–3 — Compile:** scaffold the tree, write content/source/concept notes
     (deep ML/Quant notes use the artifacts that teach — runnable code, a LaTeX
     equation, a diagram — where each earns its place, not to fill a quota), build the
     concept-graph canvas.
   - **Phases 4–5 — Distribute:** wire prev/next navigation, validate all wikilinks
     (run the bundled `scripts/validate_links.py` that sits next to this skill, or the
     inline check in the workflow's Phase 4), run the teaching-quality pass.
   - **Phase 6 — Commit:** commit the collection; clear `Inbox/` only with explicit
     user approval.

4. **Reflect (Phase 7).** Append a dated entry to `.agents/learned/journal.md`, and
   when there is a durable lesson, propose an update to `conventions.md` /
   `examples.md` or a new `learned/skills/` playbook. Surface rule-change diffs for
   approval before committing them. Reflect immediately whenever the user corrects
   you — corrections are the highest-value signal.

5. **Respect the boundaries:** never delete files without approval, never touch
   `.obsidian/`, keep machine metadata in frontmatter rather than visible note
   scaffolding, and never silently commit changes to the agent's own learned rules.
