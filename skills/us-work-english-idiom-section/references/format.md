# 비즈니스 관용 표현 및 실전 화법 — Format Reference

## Canonical format (from docs/workplace/meetings.md)

```md
## 비즈니스 관용 표현 및 실전 화법

<details>
<summary>N. 한글 카테고리명 (English Category Name)</summary>

이 그룹의 표현들이 어떤 상황에서 쓰이는지 한두 줄로 설명합니다.

**"First expression in English."**

- 핵심: 표현의 뉘앙스와 활용 맥락을 2–3줄로 설명합니다. 단순 번역이 아닌, 왜 이 표현이 더 자연스럽고 전문적으로 들리는지 초점을 맞춥니다.

**"Second expression / Variant expression."**

- 핵심: ...

**"Third expression."**

- 핵심: ...

</details>

<details>
<summary>N+1. 다음 카테고리 (Next Category)</summary>

...

</details>

:::tip 💡 팁
학습자에게 유용한 마무리 팁 한 문장.
:::
```

---

## Rules

### details/summary
- `<summary>` format: `N. 한글명 (English Name)` — number, Korean category, English in parentheses
- One-sentence group introduction immediately after the opening `<details>` tag
- 2–4 expressions per block; 3–4 blocks per section

### Bold expression line
- Format: `**"Exact English expression."**`
- Korean translation is NOT included in this line
- Variants are separated with ` / ` inside the same bold line: `**"Option A / Option B."**`

### 핵심 bullet
- Only ONE bullet per expression: `- 핵심:`
- 2–3 sentences: what the expression communicates + why it sounds professional/native
- Mention the Korean equivalent meaning naturally within the explanation
- Do NOT add 원문, 유사 표현, or any other bullet

### Closing admonition
- Always end the entire section with `:::tip 💡 팁` ... `:::`
- One practical learning tip for the reader

---

## Difference from meetings-expressions.md format

| Feature | 이 스킬 (meetings.md style) | us-work-english-content (expressions sub-page) |
|---|---|---|
| Korean in bold line | No | Yes, in parentheses |
| Bullets per expression | 핵심 only | 핵심 + 원문 + 유사 표현 |
| Source quote | Not included | 원문: *"..."* |
| Alternate phrases | Not included | 유사 표현: A / B |
| Typical use | Inline section in existing page | Standalone sub-page |
