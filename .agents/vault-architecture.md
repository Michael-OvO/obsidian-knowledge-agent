---
title: Vault Architecture Design
created: 2026-02-28
tags: [meta, architecture]
---

# Knowledge Vault Architecture Design

## Purpose

Define the stable shape of the vault: top-level folders, folder roles, and how branches relate. For note schema and syntax, defer to `.agents/obsidian-conventions.md`. For writing quality, defer to `.agents/style-guide.md`. For ingestion steps, defer to `.agents/ingestion-workflow.md`.

## Adapt to the vault you're in

The structure below is an **example** for a student/researcher vault. The *model* — a few domain branches, a shared `References/`, a transient `Inbox/` — generalizes to any vault and any subject: a work vault might use `Projects/`, `Meetings/`, `People/`; a research vault `Papers/`, `Ideas/`, `Experiments/`; a personal vault whatever its owner already uses.

**In an existing vault, detect and match what's already there before adding anything.** Read the current top-level folders, naming patterns, and frontmatter, and fit in. Only fall back to the defaults below when the vault is empty or has no clear convention. Preferences you learn about a vault's real shape are recorded in `.agents/learned/`.

## Folder Structure

```
Knowledge/
├── Inbox/                 ← Raw material staging area
├── References/            ← Shared foundational concepts
├── ML/                    ← Machine Learning branch
│   └── _index.md
├── Quant/                 ← Quantitative Finance branch
│   └── _index.md
├── School/                ← Academic courses
│   ├── _index.md
│   └── {Semester}/
│       └── {Course}/
├── Attachments/           ← Images, PDFs, non-markdown files
└── Dashboard.md           ← Vault home page
```

### Folder Roles

- **Inbox**: transient staging area for material waiting to be processed.
- **References**: shared concepts reused across branches; prefer linking here instead of duplicating.
- **ML / Quant**: domain branches for topic collections, each rooted by an `_index.md`.
- **School**: academic branch organized as `School/{Semester}/{Course}/`.
- **Attachments**: binary assets kept in the vault and referenced by notes.
- **Dashboard.md**: optional vault landing page.

## Cross-Linking Strategy

- Shared concepts that appear across branches belong in `References/`.
- Branch and collection `_index.md` files provide top-down navigation.
- Content notes should link laterally to related notes and upward to shared references.
- When a concept already exists, extend the existing note with new anchor sources instead of creating a duplicate.

## Design Decisions

- **Clean names over numeric prefixes**: folder names should read like titles, not IDs.
- **Lightweight structure**: folders and `_index.md` files provide navigation; schemas live in conventions and workflow docs.
- **Shared references over copies**: cross-branch ideas converge in `References/`.
- **Modular agent docs**: architecture, conventions, style, and workflow each have one owner.

## Future Expansion

- Add new top-level branches only when they represent a stable domain.
- Add bases, dashboards, or attachment substructure without changing the branch model.
- Put new rules in the authoritative doc instead of duplicating them here.
