---
name: us-work-english-content
description: "This skill should be used when writing or adding expression-practice sub-pages to the us-work-english Docusaurus site (jeonck/us-work-english). It encodes the exact content format: thematic collapsible groups, bold expressions with 핵심/원문/유사 표현 bullets, tip admonitions, and sidebar wiring in sidebars.ts. Triggers when the user provides a list of English expressions or a meeting/presentation script excerpt and asks to turn it into a Docusaurus page on this site."
---

# us-work-english Content Skill

## Overview

Write expression-practice sub-pages for the us-work-english Docusaurus site, following
the established format used in `docs/workplace/meetings-expressions.md`.

Load `references/content-format.md` for the full template and grouping guidelines before writing any file.

## Workflow

### Step 1 — Determine target section and file path

Map the user's content to the correct `docs/` subdirectory:

| Topic | Directory | Sidebar key |
|---|---|---|
| 직장 미팅/발표 | `docs/workplace/` | `workplaceSidebar` |
| 영어 말하기 | `docs/speaking/` | `speakingSidebar` |
| 영어 듣기 | `docs/listening/` | `listeningSidebar` |
| 원서 읽기 | `docs/reading/` | `readingSidebar` |
| 표현 사전 | `docs/phrasebook/` | `phrasebookSidebar` |

File naming: `PARENT-TOPIC.md` (e.g. `meetings-expressions.md`).

### Step 2 — Write the content file

Refer to `references/content-format.md` for the exact template. Summary of rules:

1. **Frontmatter**: set `id`, `sidebar_position` (check sibling files to avoid duplicates), `title` in `한글 (English)` format.
2. **Intro paragraph**: one or two sentences on the source context and how to use the page.
3. **Group expressions** into 3–4 thematic collapsible `details` blocks (2–3 expressions each).
4. Each expression entry:
   ```
   **"Expression"** (한국어 번역)

   - 핵심: EXPLAIN communicative function — why it sounds natural/professional
   - 원문: *"VERBATIM source quote"*
   - 유사 표현: Phrase A / Phrase B
   ```
5. Close with `:::tip 💡 팁` admonition.

### Step 3 — Wire the sidebar (`sidebars.ts`)

- If the parent page is a plain string item, convert it to a category:
  ```ts
  {
    type: 'category',
    label: '한글명 (English)',
    collapsed: true,
    items: [
      'section/parent-page',
      'section/new-page',
    ],
  },
  ```
- If a category already exists, append the new item to `items`.
- Parent page always goes first inside `items`.

### Step 4 — Build, commit, push

```bash
npx docusaurus build          # must output [SUCCESS]
git add docs/SECTION/NEW-FILE.md sidebars.ts
git commit -m "Add TOPIC expressions page under PARENT"
git push
```

## Quality checklist

- [ ] 핵심 bullet explains communicative function, not just a translation
- [ ] 원문 uses *italics* with the verbatim quote (keep fillers like "uh", "like")
- [ ] 유사 표현 lists 2–3 alternatives separated by ` / `
- [ ] Every `details` block is properly closed
- [ ] `sidebar_position` does not clash with sibling files
- [ ] Build succeeds before push
