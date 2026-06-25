---
description: Reorganize notes and folders safely — rename, move, split, merge — and rewire every affected wikilink
argument-hint: <the change, e.g. "rename ML to Machine Learning" or "split the Transformers note">
---

Carry out the restructuring in `$ARGUMENTS` without breaking the vault.

1. **Plan.** State exactly what will move, rename, split, or merge, and which files link to
   the affected notes (search for wikilinks to them). Show me the plan before changing anything.
2. **Baseline.** Validate links first (`scripts/validate_links.py`) so we know the starting
   point is clean.
3. **Execute** with `git mv` where possible (preserve history). For a split, create the new
   notes and move the relevant content; for a merge, combine and redirect. Preserve frontmatter.
4. **Rewire EVERY wikilink** that pointed at a moved/renamed/merged note — including aliased
   and table-escaped (`\|`) links — and update any indexes and concept-graph canvas.
5. **Re-validate links** (must be zero broken) and **commit**. Never delete a note without my
   explicit approval — leave a redirect stub or archive it instead.
