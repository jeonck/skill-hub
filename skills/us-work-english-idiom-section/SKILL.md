---
name: us-work-english-idiom-section
description: "This skill should be used when writing a 비즈니스 관용 표현 및 실전 화법 section for the us-work-english Docusaurus site. It produces collapsible details blocks where each expression uses a bold English line and a single 핵심 bullet only — no Korean translation inline, no 원문, no 유사 표현. Triggers when the user provides business expressions or idioms to be formatted as an inline section within an existing page such as docs/workplace/meetings.md."
---

# us-work-english 비즈니스 관용 표현 섹션 스킬

## Overview

Write the "비즈니스 관용 표현 및 실전 화법" section that appears inside existing Docusaurus pages on the us-work-english site. The canonical example is in `docs/workplace/meetings.md`.

Load `references/format.md` before writing any content — it contains the full template and the rules table.

## Format at a Glance

Each section consists of:

1. A `## 비즈니스 관용 표현 및 실전 화법` heading (or a contextual equivalent)
2. 3–4 `details` blocks, each covering one theme
3. Inside each block: 2–4 expressions, each formatted as:

```
**"Exact English expression."**

- 핵심: 2–3 sentences explaining communicative function and why it sounds professional.
```

4. A closing `:::tip 💡 팁` admonition

## Step-by-Step Workflow

### Step 1 — Receive and group the expressions

- Accept a raw list of expressions from the user
- Group them into 3–4 thematic categories (e.g., 업무 프로세스, 이슈 해결, 대화 흐름, 제안 및 설득)
- Aim for 2–4 expressions per group

### Step 2 — Write the section

Follow these rules strictly (see `references/format.md` for full detail):

- Bold line: `**"Expression."**` — no Korean translation, no parentheses
- Variants on the same line: `**"Option A / Option B."**`
- Bullet: `- 핵심:` only — never add 원문 or 유사 표현 bullets
- 핵심 content: explain the communicative function + why it's more native/professional than a simpler alternative; include the Korean meaning naturally within the prose
- Group description: one sentence after the summary tag, before the first expression

### Step 3 — Place the content

- For an existing page (e.g., `meetings.md`): append the section before any closing admonition, or after the last `---` divider
- For a new standalone page: create the file with proper frontmatter and wire the sidebar (see `us-work-english-content` skill for sidebar wiring details)
- Build and push after editing:

```bash
npx docusaurus build
git add docs/SECTION/FILE.md
git commit -m "Add 비즈니스 관용 표현 section to FILE"
git push
```

## Quality Checklist

- [ ] Bold line has no Korean translation or parenthetical
- [ ] Only one bullet per expression: `- 핵심:`
- [ ] 핵심 is 2–3 sentences and explains WHY, not just WHAT
- [ ] Each details block has a one-sentence group introduction
- [ ] Section ends with `:::tip 💡 팁`
- [ ] Build succeeds before push
