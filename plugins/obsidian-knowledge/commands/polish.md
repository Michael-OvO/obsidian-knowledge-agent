---
description: Improve existing notes in place — clearer structure, bullet-first, artifacts that teach, better links
argument-hint: [a note or folder to polish; default: recently changed notes]
---

Run the teaching-quality pass on the target (`$ARGUMENTS`, or the most recently changed
notes if none is given). Read `.agents/style-guide.md` first.

1. **Select** the note(s). For a folder, polish the content and concept notes (skip indexes
   and source notes unless I ask).
2. **Review against the style guide:** does the body read naturally top to bottom? Is the
   machinery off-stage (metadata in frontmatter, no rubric headings)? For technical notes,
   is it bullet-first with the artifacts that genuinely teach (runnable code, an equation,
   a diagram)? Are related links specific and useful?
3. **Rewrite only the failing parts** — never restate a whole note and never change its
   meaning. Add a missing artifact only where it actually helps.
4. **Fix and wire wikilinks**, then validate them (the bundled `scripts/validate_links.py`,
   or the inline check in the workflow). Show me the diffs before committing.
