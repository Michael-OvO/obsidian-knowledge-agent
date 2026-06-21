# Obsidian Conventions

> **For agents:** Follow these conventions throughout all vault work. This file is the source of truth for frontmatter, link syntax, file naming, math syntax, and canvas validation.

---

## Properties (YAML Frontmatter)

```yaml
---
tags: [paper, concept]          # Array format, no # prefix
created: 2026-03-02             # ISO date
authors: [Gabriel, Danks]       # Array of surnames
year: 2020                      # Integer
source: "Inbox/filename.pdf"    # Quoted path to original
---
```

- Use `tags:` as YAML array `[tag1, tag2]` — NOT `#tag` in body text
- Strings containing special characters need quotes: `theme: "AI & Society"`
- Profile-specific fields (like `course:`, `week:`) are added per profile
- Keep note-local metadata in frontmatter and collection-level metadata in `_index.md` files, not as visible body sections
- If agent-only annotations are unavoidable, prefer hidden comments like `%% hidden %%` over reader-facing scaffolds

---

## Wikilinks

| Context | Syntax | Example |
|---|---|---|
| Normal link | `[[path/to/note]]` | `[[ML/Transformers/Attention.md]]` |
| Link with alias | `[[path\|display text]]` | `[[.../_index\|W01]]` |
| **Inside a table** | Escape pipe: `\|` | `[[.../_index\|1]]` |
| Embed (transclusion) | `![[note]]` | `![[diagram.png]]` |
| Heading link | `[[note#heading]]` | `[[Attention#Self-Attention]]` |

> **Pipe rule:** Every `|` inside a `[[wikilink]]` that appears within a Markdown table MUST be escaped as `\|`. Unescaped pipes break the table parser — the link splits across columns.

---

## Link Paths

- **Cross-folder links:** Full relative path from vault root: `[[School/Spring 2026/PHIL 515 - Moral AI/References/Fairness]]`
- **Same-folder links:** Short name only: `[[Gabriel 2020 - AI Values and Alignment]]`
- When in doubt, use the full path — Obsidian resolves it either way, but full paths are unambiguous

---

## File Naming

| Type | Pattern | Example |
|---|---|---|
| Unit folder | `{Unit Type} {NN} - {Unit Label}` | `Week 06 - Distributive Justice`, `Ch 03 - Attention` |
| Content note | `{Author Year} - {Short Title}.md` | `Gabriel 2020 - AI Values and Alignment.md` |
| Source note | `{Author Year} - Source Notes.md` | `Gabriel 2020 - Source Notes.md` |
| Concept note | `{Concept}.md` | `Alignment.md` |
| Unit index | `_index.md` | `_index.md` |
| Canvas | `{LABEL} Concept Graph.canvas` | `PHIL 515 Concept Graph.canvas` |

---

## Math (LaTeX)

Obsidian renders LaTeX via MathJax. Use `$...$` for inline, `$$...$$` for display. Environments like `aligned`, `cases`, and `bmatrix` work inside display blocks.

**Rules:**
- **Variables in prose get math mode** -- `the query matrix $Q$` not `the query matrix Q`
- **`\text{}` for named operators** -- `$\text{softmax}$` not `$softmax$` (bare letters italicize as separate variables)
- **`\text{}` in subscripts** -- `$d_\text{model}$` not `$d_{model}$`
- **Promote long expressions to display math** -- if inline math exceeds ~40 characters, use `$$...$$`
- **Pipe caution in tables** -- use `\mid` or `\vert` instead of `|` inside math within Markdown tables

---

## Mermaid Diagrams

Obsidian renders Mermaid diagrams inside ` ```mermaid ` fenced code blocks. Mermaid has its own text renderer — it does **not** support MathJax.

**Rules:**
- **No LaTeX inside Mermaid** — `$...$` and `$$...$$` render as literal dollar signs. Use plain-text equivalents: `C ≈ 6ND` not `$C \approx 6ND$`
- **Line breaks in node labels** — use `<br/>`, not `\n`. Obsidian bundles Mermaid ~v10, which only recognizes `<br/>` inside `["..."]` labels. `\n` renders as literal backslash characters.
- **Node labels with special characters** — wrap in `["double quotes inside square brackets"]` to prevent Mermaid parsing errors
- **Unicode math** — for symbols needed inside diagrams, use Unicode directly: `≈`, `×`, `→`, `≤`, `∞`, `α`, `β` instead of LaTeX commands
- **Diagram type choice:**
  - `flowchart TD` or `flowchart LR` — processes, pipelines, decision trees
  - `sequenceDiagram` — interaction between components over time
  - `graph` — concept relationships
- **Keep diagrams focused** — one diagram should teach one idea. If you need 15+ nodes, consider splitting into two diagrams.

---

## Highlight Conventions

Use semantic highlights sparingly when the Highlightr plugin is available:

| Color | Class | Purpose | When to use |
|---|---|---|---|
| Amber | `hltr-Important` | Key insights, critical claims | The sentence you'd underline in a textbook |
| Blue | `hltr-Definition` | Terms, mechanisms, definitions | Formal "what is X" content worth recalling |
| Green | `hltr-Example` | Concrete examples, analogies | Cases that ground an abstraction |

**Rules:**
- Highlight *phrases*, not paragraphs -- a highlight should be scannable in isolation
- If everything looks important, nothing is -- aim for 3-5 highlights per screen of content
- Highlights are optional emphasis, not required formatting

---

## JSON Canvas Conventions

Canvas files (`.canvas`) use the [JSON Canvas](https://jsoncanvas.org/) spec:

- **Node types:** `file` (links to vault files), `text` (inline content), `group` (visual container)
- **IDs:** 16-character lowercase hex, unique across all nodes and edges
- **Edges:** Connect nodes via `fromNode`/`toNode` IDs; optional `color` and `label`
- **File paths:** Relative from vault root — must reference existing files

Validation:
1. Valid JSON — parseable without errors
2. All IDs unique across nodes + edges
3. All edge `fromNode`/`toNode` reference existing node IDs
4. No non-group node bounding boxes overlap
5. All nodes inside the group bounding box
6. All file paths in file nodes reference existing files
