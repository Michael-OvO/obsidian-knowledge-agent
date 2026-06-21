# Teaching Note Style Guide

> **For agents:** This is the voice and quality standard for ALL reading notes and concept notes in the vault. Notes must teach, but they should read like something a human would willingly revisit.

---

## Core Principle

**Write for the future human reader, not for the ingestion pipeline.**

The body of a note should read naturally from top to bottom. Tags, dates, source paths, progress state, and other machine-ish context belong in frontmatter, hidden comments, or index files, not as visible scaffolding in the note body.

For STEM material, "natural" does not mean essayistic or humanities-shaped. The default should be a clear scientific explanation of the problem, mechanism, assumptions, evidence, and limits in the order that best teaches the topic.

For `ML/` and `Quant/` specifically, the default presentation should be short, clean, and bullet-first. The note should still teach rather than dump fragments, but the body should usually be built from tight bullet groups, short numbered sequences, equations, code blocks, and diagrams instead of long prose paragraphs.

Minimal contrast: *"Gradient clipping stabilizes training"* describes; *"Gradient clipping caps extreme updates so one bad batch does not throw optimization off course"* teaches.

---

## The Four Rules

### 1. Keep the machinery off-stage

- Put metadata in YAML or `_index.md` files.
- If agent-only annotations are unavoidable, hide them; do not turn them into reader-facing headings.
- Avoid visible scaffolds like `0) Metadata + Framing`, `Argument Map`, `Primary stakes`, or `Design`.

### 2. Write through a real question

- Open from the question, phenomenon, failure mode, or confusion a reader actually has.
- Let the answer unfold as explanation, not as a checklist.
- Bad: `This note covers vanishing gradients.`
- Better: `Why do deeper networks stop learning even when the architecture looks expressive enough?`

### 3. Make the logic feel inevitable

- The note still needs a `because`, but it should live inside readable prose or well-placed bullets.
- Prefer `X behaves this way because Y` over bare conclusions.
- If you extract a planning scaffold internally, rewrite it before it reaches the page.

### 4. Use structure that serves reading

- Prefer short sections and natural headings.
- In `ML/` and `Quant/`, default to bullet groups over paragraphs unless prose is clearly better for the passage.
- In STEM notes, let the explanation follow the science: problem -> mechanism -> math or algorithm -> implications -> limits when that fits the material.
- Good heading bank: `The Question`, `Why It Matters`, `Core Idea`, `Mechanism`, `Algorithm`, `The Math`, `Code`, `Diagram`, `Tradeoffs`, `Failure Modes`, `Related Notes`, `Sources`.

---

## Voice Targets

| Quality | What it means | Test |
|---|---|---|
| **Natural** | Reads like a human note, not a form | Would this still make sense if the scaffolding vanished? |
| **Clear** | A smart undergraduate can follow without a dictionary | Read it aloud. If you stumble, rewrite. |
| **Concise** | No line is there just because a template wanted it | Can you cut it without losing meaning? |
| **Concrete** | Abstract ideas are grounded in cases | Does the reader get at least one anchor? |
| **Honest** | Objections are real, not decorative | Does the note admit where the idea is weak or incomplete? |
| **Scannable** | Key ideas survive skim-reading | Can the reader recover the gist from headings and bullets alone? |

---

## Anti-Patterns

| Anti-pattern | Example | Fix |
|---|---|---|
| **Visible scaffold** | `## 0) Metadata + Framing` | Move metadata to frontmatter or an index file |
| **Rubric prose** | `Primary stakes: training stability` | Turn it into a sentence the reader would actually want to read |
| **Bare conclusion** | `This optimizer is better` | Add the mechanism or `because` |
| **Machine heading** | `## Argument Map` | Replace with a natural heading or fold into prose |
| **Bullet dump** | Seven bullets with no flow | Group them into labeled bullet clusters that teach one idea each |
| **Paragraph wall** | Long prose in an `ML/` lecture note | Convert it into short bullets, equations, diagrams, or numbered mechanism steps |

---

## Note Structures

Different notes serve different purposes. The structure should follow the function — not every note is a reading summary, and not every note needs the same shape. What they share is the Four Rules above. What differs is how they organize content.

### 1. Technical / STEM Notes

**Default for:** `ML/`, `Quant/`, and science, engineering, or math material in `School/`.

**Purpose:** Capture how a system, method, model, derivation, experiment, or result works.

**Tag:** `paper`, `lecture`, `reading`, or the domain-specific tag that fits the source.

**Shape:** Bullet-first technical explainer. The note should still move from problem setting to mechanism to practical consequences, but it should usually do so through compact bullet clusters, short numbered sequences, equations, code, and diagrams rather than extended prose.

- **Opening**: Start with 1 short paragraph or 2-4 bullets framing the technical question, bottleneck, or failure mode.
- **Body**: Use labeled bullet sections. Each section should teach one idea: mechanism, equations, derivation, algorithm, architecture, experiment, empirical pattern, or causal chain.
- **Headings**: Prefer scientific headings such as `The Question`, `Core Idea`, `Mechanism`, `Algorithm`, `The Math`, `Code`, `Tradeoffs`, `Failure Modes`, `Practical Implications`.
- **Technical detail — the three-artifact floor**: In `ML/` and `Quant/`, every technical lecture or concept note must include **all three** of: (1) at least one code block, (2) at least one LaTeX equation, and (3) at least one Mermaid diagram. This is a floor, not a ceiling — most notes benefit from more. For other STEM branches, at least one concrete artifact beyond plain text is still expected.
- **Runnable code, not fragments**: Code blocks should be copy-pasteable — full function definitions with imports, realistic variable names, and a usage example or print statement. Pseudocode is acceptable only when the real implementation requires infrastructure the reader cannot run locally (e.g., multi-node distributed training).
- **Bullet discipline**: Bullets must carry explanation, not fragments. Good bullets still contain the `because`.
- **Glossary-style sections**: Optional. Use them only when the note introduces enough standalone terms that collecting them actually helps.
- **Related Notes**: Link 2–4 specific vault files, each with a `—` annotation explaining *why* the link matters (e.g., `[[note]] — extends this with the engineering tradeoffs`). Bare link lists without annotations fail the "serves the reader" test.

**Typical flow options:**
- *problem -> intuition -> formal model -> derivation or algorithm -> implications -> failure modes*
- *empirical puzzle -> mechanism -> evidence -> interpretation -> caveats*
- *system bottleneck -> architecture -> tradeoffs -> operational guidance*
- *theorem or method -> setup -> assumptions -> result -> why it matters -> where it breaks*

**What makes a good STEM note:** A reader should be able to skim the headings and bullets, then reconstruct what the thing is, why it behaves that way, what assumptions it depends on, and where it stops working.

### 2. Humanities / Argumentative Reading Notes

**Use this only when the source itself is primarily argumentative.** Philosophy papers, legal analysis, normative policy pieces, and similar texts often do benefit from explicit treatment of thesis, argumentative spine, and objections.

**Purpose:** Summarize and engage with a work whose main job is to persuade through argument.

**Tag:** `paper` or `reading`

**Shape:**
- Open with the central question or tension the work addresses.
- Surface the core thesis and the main argumentative moves.
- Define the concepts the reader needs, with concrete anchors where possible.
- Include real objections, limits, or unresolved tensions.
- End with related notes or sources when they help.

**What makes a good humanities reading note:** The reader should understand the work's argument, not just its conclusions.

### 3. Concept / Reference Notes

**Purpose:** Teach a concept from scratch. These live in `References/` folders.

**Tag:** `concept`

**Shape:** A progressive explainer, usually bullet-first for technical concepts rather than paragraph-first. Start with the most concrete intuition you can, then add precision as needed.

For technical concepts, that often means *intuition -> definition -> mechanism or equation -> example -> limits*. For less technical concepts, it may mean *question -> distinction -> consequence -> caveat*. Use the shape that teaches best.

**The progression rule:** Move from accessible to deep, from intuitive to precise, from "what is this?" to "how does it work?" to "where does it break down?" Every section should earn the next one.

**Structure is emergent, not imposed.** Use headings only when the concept genuinely shifts gears — not because a template says so. A short concept note might need none. A longer one might need a few scientific signposts such as `Mechanism`, `Example`, or `Failure Modes`.

**Integration over segregation.** If a concept spans theory and practice, or math and engineering, weave those facets together rather than stapling them into separate silos.

### 4. Exam Prep Notes

**Purpose:** Prepare for a specific exam. These are working documents, not teaching notes.

**Tag:** `exam-prep`

**Shape:** Numbered structure is *appropriate here* — exams have prompts, time limits, and scoring criteria that benefit from explicit organization.

- **Exam facts**: Date, coverage, format, constraints — front-loaded for quick reference.
- **Answer strategy**: Time splits, required structural elements, scoring tips. Numbered steps and checklists are natural.
- **Prompt outlines**: One section per potential exam question. Thesis skeleton, key moves, readings to cite, example to use. Dense and scannable — this is a cheat sheet, not an essay.
- **Sample answers** (optional, can be a separate note): Fully written practice responses.

**What makes a good exam note:** Optimize for exam-day retrieval. A student scanning this at 11pm should find what they need in seconds. Beauty and narrative flow are secondary to utility.

### 5. Source Notes

**Purpose:** Raw analytical extraction from a PDF or reading — a bridge between the original text and the polished reading note.

**Tag:** `source-note`

**Shape:** Deliberately minimal. These are working artifacts, not reader-facing notes.

- **Core question or claim**: One sentence.
- **Source spine**: 3-6 bullets capturing the logical or technical backbone. For STEM sources, this is usually the setup, method, result, and limits rather than an argument map.
- **Key analytical points**: Distinctions, definitions, mechanisms, results, or framings worth preserving.
- **Linked notes**: Wikilink to the reading note and any related source notes.
- **Full text import** (optional): Link to the OCR text file.

**These notes are allowed to be ugly.** Their job is to preserve the extraction for future reference, not to teach. The reading note is where the teaching happens.

### 6. Index Files

**Purpose:** Navigation hubs for courses, weeks, or topic clusters. They orient the reader within a collection.

**Tag:** `course`, `course-week`

**Shape:**
- **Focus**: One sentence framing the week's central question.
- **Lectures/Readings table**: Date, topic, instructor — scannable reference.
- **Sources**: Wikilinks to all notes in the collection.
- **Concept spine**: Links to the reference notes that underpin this week's material.
- **Key takeaways**: 2-4 bullets — the things worth remembering even if you forget everything else.
- **Deadlines** (if applicable): Assignment due dates, releases.
- **Navigation**: Previous/next links at the bottom.

**Index files are the one place tables and bare link lists are encouraged.** Their job is wayfinding, not explanation.

### 7. Project / Research Notes

**Purpose:** Track ongoing work — a research question, implementation project, or investigation.

**Tag:** `project`

**Shape:**
- **The question**: What are you trying to figure out or build? One paragraph.
- **Current state**: Where things stand right now. Updated as work progresses.
- **Approach**: How you're tackling it — methods, architecture, key decisions and why.
- **Findings / Results**: What you've learned so far. Provisional is fine — mark what's uncertain.
- **Open threads**: What's left to do or figure out.
- **Log** (optional): Dated entries for longer-running projects, newest first.

**These notes are living documents.** Unlike reading notes (which stabilize after creation), project notes evolve. Mark provisional claims with language like "current best guess" or "needs verification."

---

## General Principles (All Note Types)

- Start with a short opening that frames the real question or purpose.
- Use headings chosen for the material, not from a fixed template.
- In `ML/` and `Quant/`, make bullet groups the default body shape unless prose is clearly doing better teaching work.
- In STEM notes, prefer scientific explanation over thesis-counterargument structure unless the source is explicitly argumentative.
- Short notes do not need every possible section.
- When using bullets, keep them explanation-rich, not telegraphic.
- End with related links or sources only when they add value.

### Heading Bank

Use these as options, not mandatory labels:

| Purpose | Natural headings |
|---|---|
| Framing | `Why This Matters`, `The Question`, `What This Is Really About` |
| Explanation | `Core Idea`, `How It Works`, `Mechanism`, `What Follows From This` |
| Technical depth | `Problem Setting`, `The Math`, `Derivation`, `Algorithm`, `Under the Hood`, `The Pipeline`, `Implementation` |
| Practical reality | `Empirical Behavior`, `What Actually Happens at Scale`, `Assumptions`, `Where This Breaks`, `Failure Modes`, `The Engineering Problem` |
| Argument (humanities only) | `Core Thesis`, `How the Argument Builds` |
| Detail | `Key Concepts`, `Key Details` |
| Limits | `Where It Gets Tricky`, `Limits`, `Open Questions`, `Failure Modes` |
| Navigation | `Related Notes`, `Sources`, `Connections` |

### Math in notes

- Use LaTeX whenever math appears. Syntax rules live in `.agents/obsidian-conventions.md`.

---

## The Ultimate Test

After writing a note, ask:

1. **Would a human reader want to read this body as written?**
2. **If I removed the hidden metadata and planning scaffold, would the note still stand on its own?**
