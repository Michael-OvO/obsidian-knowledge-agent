---
description: Check vault health — broken links, orphans, missing frontmatter, MISSING placeholders — and propose fixes
argument-hint: [optional: a folder to scope the check]
---

Run a health check over the vault (or the folder in `$ARGUMENTS`) and report a clean summary.

1. **Broken wikilinks** — run the bundled `scripts/validate_links.py` on the target.
2. **Orphans** — notes that nothing links to and that link to nothing (ignore indexes and
   dashboards).
3. **Frontmatter** — notes missing the minimum (`tags`, `created`) or with malformed YAML.
4. **Stubs & placeholders** — `# … — MISSING` notes and near-empty notes.
5. **Canvas** — any `.canvas` file whose file nodes point at files that no longer exist.

Report the findings grouped, with counts and the worst offenders named. Then propose concrete
fixes and apply them **only with my approval** — never delete anything without asking.
