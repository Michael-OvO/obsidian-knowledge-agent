# Knowledge Ingestion Workflow

> **For agents:** This is a reusable workflow for transforming raw material in `Inbox/` into structured, navigable, teaching-quality notes.
>
> **Before Phase 0, read:**
> - `.agents/style-guide.md` for note quality
> - `.agents/obsidian-conventions.md` for frontmatter, links, naming, and canvas rules
> - `.agents/self-evolution.md` for the recall → reflect learning loop (Phase 0 recall, Phase 7 reflect)

**Purpose:** Turn raw material — anything from a single link to a whole syllabus — into notes worth keeping, with exactly as much structure as the material needs and no more.

---

## Choose the altitude

Before anything else, decide how much structure the material actually warrants. Pick the **smallest tier that fits**, and escalate only when the input clearly asks for it.

| Tier | Use when the input is… | What you produce | Phases to run |
|---|---|---|---|
| **Capture** | a link, a thought, a single article or transcript, a "save this" | one clean note in the best-fit existing folder | 0 (recall + a quick classify) → write the note → 6 (commit) → 7 (reflect) |
| **Small collection** | a handful of related sources, or a short topic | a few notes + one light `_index.md` | 0–2, a simple index, 4, 7 |
| **Full build** | a syllabus, a book, or a large/structured paper collection | the complete scaffold: indexes, source notes, navigation, quality pass, concept-graph canvas | all of 0–7 |

The phases below spell out the **full build**. For lighter tiers, running only the phases listed above — and skipping scaffolds, source notes, the canvas, prev/next chains, and the parallel quality pass — is the *correct* behavior, not a shortcut. Never impose more structure than the material or the user asked for. When torn between two tiers, choose the lighter one and offer to go deeper.

---

## Vault Branches

Every ingestion lands in one of these roots: `School/{Semester}/{Course}/`, `ML/{Topic}/`, `Quant/{Topic}/`, or `References/{Concept}.md`.

The exact target is determined in Phase 0. See `.agents/vault-architecture.md` for folder roles and branch boundaries.

---

## Phase 0: Classify and Extract

**Input:** Raw material in `Inbox/` (docx, pdf, markdown, URL list, transcript, etc.)
**Output:** Resolved input profile, target path, and structural map. No files created yet.

### Step 0: Recall learned state

Before classifying, load what this vault has taught you (see `.agents/self-evolution.md`):

- Read `.agents/learned/conventions.md` (if present) — vault-specific overrides that refine the defaults. Apply them this run.
- Read `.agents/learned/examples.md` (if present) — use the closest input→classification rows as few-shot guidance.
- Scan `.agents/learned/skills/` — if a playbook's `trigger:` matches this input, follow it instead of re-deriving the approach.

On a fresh vault these files do not exist yet; recall is silent and you proceed normally.

### Step 1: Locate input

List the files in `Inbox/`. Extract content based on format:
- **docx →** Convert to markdown using `pandoc` (pipe to stdout; avoid temp files)
- **pdf →** Read the PDF contents; use page ranges for long PDFs
- **md/txt →** Read the file directly
- **URL list →** Fetch each URL and extract to markdown

### Step 2: Classify input type

Read the extracted content and determine the **input profile**:

| Profile | Trigger | Structural Unit | Target Branch |
|---|---|---|---|
| **Course** | Syllabus with weekly schedule and readings | `Week {NN} - {Theme}/` | `School/{Semester}/{Code} - {Title}/` |
| **Book** | Table of contents with chapters | `Ch {NN} - {Chapter Title}/` | `{Branch}/{Book Title}/` |
| **Paper Collection** | Multiple papers on one topic | `{Topic}/` or flat | `{Branch}/{Collection Name}/` |
| **Single Source** | One paper, article, or transcript | none | `{Branch}/{Topic}/` or `{Branch}/` |
| **Topic Build** | Research brief, outline, or concept dump | `{Subtopic}/` | `{Branch}/{Topic}/` |

### Step 3: Extract structural map

Identify from the source material:

| Extract | Course | Book | Paper Collection | Single Source | Topic Build |
|---|---|---|---|---|---|
| **Title** | Course code + name | Book title | Collection name | Paper title | Topic name |
| **Units** | Weeks + themes | Chapters | Paper groups | N/A | Subtopics |
| **Sources** | Readings per week | Sections per chapter | Individual papers | The source itself | Sources per subtopic |
| **Concepts** | Recurring themes | Key terms across chapters | Shared concepts across papers | Key terms | Core concepts |
| **Sequence** | Week order | Chapter order | Thematic or chronological | N/A | Logical dependency |

### Step 4: Resolve variables

| Variable | Description | Example |
|---|---|---|
| `{target}` | Full path to collection root | `School/Spring 2026/PHIL 515 - Moral AI` |
| `{LABEL}` | Short identifier for commits and canvas names | `PHIL 515`, `Transformers`, `Options Pricing` |
| `{TODAY}` | Current ISO date | `2026-03-02` |
| `{NN}` | Unit number, zero-padded | `01`, `02`, `14` |
| `{Unit Label}` | Name of structural unit | `Distributive Justice`, `Attention Mechanisms` |
| `{Author}` | Source author surname(s) | `Gabriel`, `Vaswani et al` |
| `{YYYY}` | Source publication year | `2020` |
| `{Short Title}` | Abbreviated title | `AI Values and Alignment` |

**Self-check:** Can you list every structural unit, its sources, and which files are available? If not, re-read the input.

---

## Phase 1: Scaffold Structure

**Input:** Resolved profile and variables from Phase 0
**Output:** Complete folder tree with index files and placeholders ready for writing

### Generic Scaffold

Every ingestion produces this shape; only the names change:

```text
{target}/
├── _index.md
├── References/
│   └── {Concept}.md
├── Source Notes/
│   ├── _index.md
│   └── {Author Year} - Source Notes.md
├── {Unit NN} - {Unit Label}/
│   ├── _index.md
│   └── {Content Note}.md
└── {LABEL} Concept Graph.canvas
```

Exceptions:
- **Single Source**: no unit folders; content note goes directly in `{target}/`
- **Flat Paper Collection**: skip unit folders if papers do not cluster naturally
- **Canvas**: only create if the collection has 3+ structural units

### Templates

Use these as minimum section checklists. Style rules belong to `.agents/style-guide.md`; syntax rules belong to `.agents/obsidian-conventions.md`.

#### T1. Collection `_index.md` (MOC)

Frontmatter: minimum schema from `.agents/obsidian-conventions.md` plus profile-specific fields from `Input Profile Quick Reference`.

Sections: `# {Collection Title}`, `## Quick Navigation`, `## {Arc Label}`, `## Throughline`.

Rules: escape alias pipes as `\|` inside tables; keep units without content as plain-text rows.

#### T2. Unit `_index.md`

Frontmatter: minimum schema from `.agents/obsidian-conventions.md` plus profile-specific fields from `Input Profile Quick Reference`.

Sections: `# {Unit NN} — {Unit Label}`, `## Focus`, `## Sources`, `## Concept Spine`, `## Key Takeaways`.

Footer: `prev/next` navigation across adjacent non-empty units.

Rules: first unit only links forward; last unit only links back; skip empty units in the navigation chain.

#### T3. Content Note (Reading / Chapter / Topic Note)

Frontmatter: `tags`, `authors`, `year`, `source`, `created`, plus profile-specific fields when needed.

Body shape:
- short opening that frames the real question
- 2-6 natural headings chosen for the material
- optional closing section for `Related Notes` or `Sources`

Rules:
- Use an internal scaffold that matches the source. For STEM material, think in terms of problem, mechanism, assumptions, math, evidence, and limits. For argumentative material, thesis and argumentative spine may still help.
- Apply `.agents/style-guide.md` body-shape rules verbatim
- **Bullet-first default for `ML/` and `Quant/`:** the body should usually be organized as short explanatory bullet groups, short numbered sequences, equations, code blocks, and diagrams rather than paragraph-heavy prose.
- **Depth requirement for technical notes:** include enough mechanism, assumptions, tradeoffs, and implementation detail that the note stands on its own as a study resource, not just a summary.
- **Use the artifacts that teach (technical notes):** a deep `ML/` or `Quant/` note is usually clearest with a runnable code block, a LaTeX equation, and a Mermaid diagram — include each one where it earns its place, and skip any that would just be filler. Code should be copy-pasteable with imports, not fragments. A short note, an overview, or a non-technical note needs none of these. The goal is understanding, not a checklist.
- **Course:** put week/course metadata in frontmatter or unit indexes; keep the note body reader-facing
- **Book:** explain the chapter's role naturally instead of using rubric labels
- **Single Source:** link outward to shared references or related notes when useful
- **Topic Build:** structure the body around explanation rather than a visible scaffold
- **STEM default:** do not force humanities-style headings such as thesis, objections, or argument map unless the source is genuinely argumentative

#### T4. Concept Reference

Frontmatter: `tags`, `created`.

Body shape: short, explanatory sections such as `Core Idea`, `Mechanism`, `Tradeoffs`, `Related Notes`, and `Sources`, usually in bullet-first format for technical concepts.

Rules: frame the concept as a live question, phenomenon, or technical problem rather than a dictionary entry; include equations, code snippets, or diagrams when they are the clearest teaching tool; if it already exists in vault-level `References/`, extend that note instead of duplicating it.

#### T5. Source Note

Frontmatter: `tags`, `authors`, `year`, `source_file`, `created`.

Body shape: short provenance-oriented sections such as `Core Question / Claim`, `Source Spine`, `Linked Notes`, and `Full Text Import`.

Rules: source notes are shorter and drier than content notes, but they should still read naturally; use them for provenance and lookup, not as reader-facing scaffolds.

#### T6. Source Notes `_index.md`

Frontmatter: `tags`, `created`.

Content: one link per source note in the collection.

---

## Phase 2: Create Content Notes

**Input:** Source files in `Inbox/`, resolved variables, and templates T3/T5
**Output:** One content note and one source note per available source

For each source:

1. **Read the source**
   - PDF → read directly; chunk long PDFs
   - Scanned PDF → OCR first if available
   - Web source → fetch and convert to markdown
2. **Research supplementary material** (when the source is a course, tutorial, or technical topic):
   - Check for companion repositories (GitHub links in syllabus, lecture slides, or course website)
   - Fetch executable code files, notebooks, or lab materials that accompany the lectures
   - Extract **real code examples** from these sources — authentic implementations are always preferred over invented pseudocode
   - This step is especially important for `ML/` and `Quant/` notes where runnable code is a required artifact
3. **Extract the internal scaffold appropriate to the source**: for STEM, usually problem, mechanism, assumptions, derivation or procedure, results, and limits; for argumentative work, thesis, argument, concepts, and tensions
4. **Write the content note** using T3, adapted for the profile
5. **Write the source note** using T5 if source text was extracted
6. **For unavailable sources:** create a placeholder with frontmatter and `# {Title} — MISSING`

Parallelism:
- Dispatch up to 5 workers, about 6 sources each
- Give each worker the source list, target path, available concepts, profile, and the relevant template requirements
- Tell workers to read `.agents/style-guide.md`; do not paste the whole style guide into the prompt
- Make explicit that internal analysis should be rewritten into short, clean, reader-facing bullets and numbered sequences rather than hidden rubric prose
- For STEM material, tell workers to optimize for scientific explanation, not for thesis-driven rhetoric
- Tell workers on deep `ML/` and `Quant/` notes to reach for the artifacts that teach — runnable code, an equation, a diagram — using each where it genuinely helps rather than to satisfy a quota. Code should be copy-pasteable with imports.

---

## Phase 3: Build Concept Graph Canvas

**Input:** Completed folder structure with unit and concept files
**Output:** `{LABEL} Concept Graph.canvas`

**Skip condition:** If fewer than 3 structural units, skip this phase.

### Layout Grid

| Column | Content | x Range | Color |
|---|---|---|---|
| Left | Concept reference nodes | `x ≈ -240` | `"5"` (cyan) |
| Center | Unit nodes in rows of 4-5 | `x: 0–1100` | `"2"` (orange) |
| Right | How-to-Use text + Source Notes link | `x ≈ 1200` | `"1"` (red) / `"3"` (yellow) |

### Node Types

- **Unit nodes** (`type: "file"`): `{target}/{Unit NN} - {Label}/_index.md`
- **Concept nodes** (`type: "file"`): `{target}/References/{Concept}.md`
- **Source Notes node** (`type: "file"`): `{target}/Source Notes/_index.md`
- **How-to-Use node** (`type: "text"`): brief navigation instructions
- **Group node** (`type: "group"`): encloses all other nodes with padding

### Edge Types

| Edge Type | Color | Description |
|---|---|---|
| Arc edges | `"2"` (orange) | Sequential unit-to-unit chain |
| Concept edges | default | Concept node → each unit where it appears |
| Source edges | labeled `"text notes"` | Source Notes → units that have source notes |

### Spacing and IDs

- Unit nodes in rows of 4-5 with 50px gaps
- Concept nodes stacked vertically on the left with 20px gaps
- Right-column nodes stacked vertically with 20px gaps
- IDs: 16-character lowercase hex, unique across all nodes and edges

### Validation

Validate against `.agents/obsidian-conventions.md § JSON Canvas Conventions` before proceeding.

---

## Phase 4: Wire Navigation

**Input:** All files from Phases 1-3
**Output:** Navigable collection with verified links

1. Add `← prev · next →` footer to each unit `_index.md`
2. Verify pipe escaping in collection `_index.md` tables
3. Validate all wikilinks resolve:

```bash
python3 - <<'PY'
from pathlib import Path
import re

root = Path("{target}")
pattern = re.compile(r"\[\[([^\]]+)\]\]")

for src in root.rglob("*.md"):
    text = src.read_text(errors="ignore")
    for raw in pattern.findall(text):
        link = raw.split("|", 1)[0].split("#", 1)[0].strip()
        if not link:
            continue
        if "/" in link:
            candidates = [Path(link), Path(f"{link}.md")]
        else:
            candidates = [
                src.parent / link,
                src.parent / f"{link}.md",
                root / link,
                root / f"{link}.md",
            ]
        if not any(candidate.exists() for candidate in candidates):
            print(f"BROKEN\t{src}\t{link}")
PY
```

4. Fix broken links by correcting the path, creating a placeholder, or removing the link

---

## Phase 5: Teaching Quality Pass

> **Reference:** Read `.agents/style-guide.md` before this phase.

Dispatch parallel workers to review content notes. Each worker checks:

- The body reads naturally from top to bottom
- Visible section names are human-facing, not pipeline-facing
- Metadata and bookkeeping live in frontmatter, hidden comments, or indexes
- The note still makes the logic visible and grounds abstractions concretely
- In `ML/` and `Quant/`, the body is short, clean, and bullet-first rather than paragraph-heavy
- STEM notes explain mechanism, assumptions, and limits in a scientific way rather than mimicking humanities-style argument flow
- Technical notes are sufficiently deep to study from directly rather than merely reminding the reader what the source said
- Technical notes include diagrams, equations, code, or tables when those artifacts are necessary for understanding
- Related links and sources help the reader instead of satisfying a template

Rewrite only the failing sections. Do not restate the whole note.

---

## Phase 6: Commit and Clear

**Input:** All files created and validated in Phases 1-5
**Output:** Clean git history, plus Inbox clearing handled under the vault's approval policy

**Policy:** `Inbox/` should be cleared after processing, but deletion requires explicit user approval. If approval is not available, commit the collection and report that raw inputs still need manual clearing.

```bash
git add "{target}/"
git commit -m "feat({LABEL}): build knowledge structure from {input type}"
```

If the user explicitly approves Inbox clearing, make that a second, separate commit.

---

## Phase 7: Reflect and Evolve

**Input:** The completed run, plus any corrections the user made
**Output:** A journal entry, and (when there is a durable lesson) proposed updates to the vault's learned rules

> **Reference:** Follow `.agents/self-evolution.md` for the full loop and drift-control rules.

This is what makes the agent self-improving: turn the run into a reusable lesson.

1. **Always append to the journal.** Add one dated entry to `.agents/learned/journal.md` (create `.agents/learned/` if needed). Record the input, how you classified it, any corrections, recurring fixes, and the durable lesson (or "none this run"). **Never rewrite earlier entries.**
2. **Capture durable lessons.** A lesson is durable when it would change a *future* run. Route each one:
   - a preference/override → edit `.agents/learned/conventions.md` (consolidate into a tight rule set, don't just append);
   - a classification judgment → add/update a row in `.agents/learned/examples.md`;
   - a whole new input shape → write a playbook to `.agents/learned/skills/<kebab-name>.md` with a `trigger:` line and steps.
3. **Surface rule changes for approval.** The journal entry commits freely. Changes to `conventions.md` / `examples.md` / `skills/` are proposals: show the `git diff`, explain each change in one line with its motivating journal entry, and let the user approve before committing.

Corrections are the highest-value signal — when the user fixes something, reflect immediately, not just at the end of the run.

---

## Error Handling

| Problem | Detection | Resolution |
|---|---|---|
| PDF unreadable | Read returns garbled text or error | Try `pandoc`; if still unreadable, create `MISSING` placeholder |
| Large PDF (50+ pages) | Page count in read output | Read in chunks, then synthesize |
| Scanned PDF (no text layer) | Read returns image content only | OCR if available; otherwise `MISSING` placeholder |
| Source not in Inbox | File listing finds no matching file | `MISSING` placeholder |
| Duplicate concept names | Two sources define same term differently | Merge into one concept note; note divergence in `Recurring Tensions` |
| Broken wikilink | Phase 4 validation | Fix path or create target |
| Canvas overlap | Phase 3 validation | Adjust coordinates and re-validate |
| Pipe in table wikilink | Link breaks table rendering | Escape as `\|` |
| Concept exists in another branch | Search finds existing `References/{Concept}.md` | Link to existing note and add new anchor source |

---

## Input Profile Quick Reference

### Course Syllabus

| Aspect | Value |
|---|---|
| Target | `School/{Semester}/{Code} - {Title}/` |
| Unit type | `Week {NN} - {Theme}/` |
| Extra frontmatter | `course:`, `semester:`, `week:`, `theme:` |
| Tags | `course`, `course-week`, `paper` |
| Arc label | `Weekly Arc` |
| Content per unit | Multiple reading notes per week |
| Extra unit section | Day/Date/Topic table if useful |
| Navigation | Skip symposium or break weeks |

### Book / Textbook

| Aspect | Value |
|---|---|
| Target | `{Branch}/{Book Title}/` |
| Unit type | `Ch {NN} - {Chapter Title}/` |
| Extra frontmatter | `book:`, `chapter:` |
| Tags | `book-notes`, `book-chapter` |
| Arc label | `Chapter Arc` |
| Content per unit | One chapter note per chapter, or split by section if needed |
| Navigation | Sequential |

### Paper Collection

| Aspect | Value |
|---|---|
| Target | `{Branch}/{Collection Name}/` |
| Unit type | `{Subtopic}/` or flat |
| Extra frontmatter | `topic:` |
| Tags | `paper-collection`, `paper-group`, `paper` |
| Arc label | `Papers` |
| Content per unit | One reading note per paper |
| Navigation | Thematic or chronological |

### Single Source

| Aspect | Value |
|---|---|
| Target | `{Branch}/` or `{Branch}/{Topic}/` |
| Unit type | None |
| Extra frontmatter | Profile-dependent |
| Tags | `paper` or `article` |
| Canvas | Skip |
| Content | One content note + one source note |
| Navigation | Link to related vault notes only |

### Topic Build

| Aspect | Value |
|---|---|
| Target | `{Branch}/{Topic}/` |
| Unit type | `{Subtopic}/` |
| Extra frontmatter | `domain:` |
| Tags | `topic`, `topic-section` |
| Arc label | `Structure` |
| Content per unit | Mix of synthesis and source-based notes |
| §2 adaptation | Default to scientific explanation; use argument structure only when the source is actually argumentative |

---

## Checklist

For a **full build**, run through this before Phase 6. Lighter tiers only need the boxes that apply to them (a Capture, for instance, needs recall, the note itself, links resolving, commit, and reflect — nothing else).

- [ ] Recalled learned conventions / examples / playbooks (Phase 0, Step 0)
- [ ] Input classified and all variables resolved
- [ ] Target path and profile determined
- [ ] Folder scaffold and `_index.md` files created
- [ ] Content, concept, and source notes created or marked `MISSING`
- [ ] Navigation and collection tables wired correctly
- [ ] Concept graph canvas built and validated when required
- [ ] All wikilinks resolve
- [ ] Quality pass completed against `.agents/style-guide.md`
- [ ] Collection committed
- [ ] Inbox clearing handled per approval policy
- [ ] Reflected (Phase 7): journal entry appended; any rule updates proposed for review
