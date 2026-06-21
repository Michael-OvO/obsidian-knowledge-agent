---
name: obsidian-knowledge-ingest
description: Use when transforming raw material (PDFs, docx, slides, syllabi, papers, transcripts, URL lists) into structured, teaching-quality Obsidian notes. Drives a self-evolving recall → ingest → compile → distribute → reflect pipeline that classifies the input, scaffolds a folder tree, writes notes that teach, builds a concept-graph canvas, wires wikilinks, runs a quality pass, then reflects on the run to improve its own rules. Trigger when the user asks to "ingest", "build notes from", or "add to the vault".
---

# Obsidian Knowledge Ingest

This skill packages a self-evolving pipeline for turning raw material in an Obsidian
vault's `Inbox/` into structured, navigable, teaching-quality notes. It **recalls**
what it learned about your vault before each run and **reflects** afterward to get
better over time — without any model training.

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
     (ML/Quant notes must hit the three-artifact floor — runnable code + LaTeX +
     Mermaid), build the concept-graph canvas.
   - **Phases 4–5 — Distribute:** wire prev/next navigation, validate all wikilinks
     (`scripts/validate_links.py`), run the teaching-quality pass.
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
