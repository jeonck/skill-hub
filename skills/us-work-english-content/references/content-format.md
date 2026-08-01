# Content Format Reference — us-work-english

## Canonical Expression Page Structure

### Frontmatter
```md
---
id: <section>-<slug>           # e.g. meetings-expressions
sidebar_position: <N>          # integer, order within parent category
title: 한글 제목 (English Title)
---
```

### Page Header
```md
# 한글 제목 — 부제목

한두 줄 도입 설명. 어떤 맥락에서 발췌했는지, 어떻게 활용하면 좋은지 안내합니다.

---
```

### Expression Groups — `<details>` blocks

Each `<details>` block groups 2–4 thematically related expressions.

```md
## 섹션 타이틀

<details>
<summary>N. 한글 카테고리명 (English Category Name)</summary>

이 그룹에 속한 표현들이 어떤 상황에서 쓰이는지 한두 줄로 설명합니다.

**"Expression in English"** (한국어 번역)

- 핵심: 표현의 핵심 뉘앙스·활용 맥락을 2–3줄로 설명합니다. 단순 번역이 아닌 **왜** 이 표현이 자연스럽게 들리는지 초점을 맞춥니다.
- 원문: *"...actual quote from the meeting script..."*
- 유사 표현: Similar phrase A / Similar phrase B

**"Second Expression"** (한국어 번역)

- 핵심: ...
- 원문: *"..."*
- 유사 표현: ...

</details>
```

### Closing Admonition
```md
:::tip 💡 팁
학습자에게 유용한 한 줄 팁. 발음, 연습 방법, 주의사항 등.
:::
```

---

## Sidebar Wiring (sidebars.ts)

### New top-level item (simple)
```ts
'section/page-id',
```

### Convert existing item → category with sub-pages
```ts
{
  type: 'category',
  label: '한글명 (English)',
  collapsed: true,
  items: [
    'section/parent-page',
    'section/child-page',
  ],
},
```

- Always set `collapsed: true` for sub-categories.
- The parent page stays as the first item in `items`.

---

## Grouping Guidelines

| Expressions per page | Groups (details blocks) | Expressions per group |
|---|---|---|
| 5–6 | 2–3 | 2–3 |
| 8–10 | 3–4 | 2–3 |
| 12+ | 4–5 | 2–4 |

Group by **functional theme**, not by order of appearance in the source material. Typical themes:
- 환경/단계 (environment, stages)
- 개선/실험 (improvement, experimentation)
- 협업/조율 (collaboration)
- 회의 정리/후속 (wrap-up, follow-up)
- 의지/제안 (commitment, proposing)

---

## 핵심 bullet writing rules

- Lead with the **communicative function** ("~을 전달할 때", "~상황에서"), not a dictionary definition.
- Compare to simpler alternatives to explain **why** this expression sounds more native/professional.
- Keep to 2–3 sentences maximum.
- End with a concrete usage scenario when space allows.
