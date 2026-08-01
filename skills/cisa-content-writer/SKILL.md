---
name: cisa-content-writer
description: |
  CISA(정보시스템 감사) 지식베이스 Docusaurus 사이트(jeonck/cisa)의 실무 문서를 작성하는 스킬.
  ISACA CISA 6대 도메인 구조에 맞는 Best Practice 가이드라인 문서를 작성할 때 트리거된다.
  각 문서는 표준화된 10섹션 구조, Mermaid 다이어그램, HTML 감사 체크리스트 테이블을 포함한다.
  "CISA 문서 작성", "도메인 X.X 내용 작성", "BP-XXX 문서", "감사 체크리스트 추가", "jeonck/cisa 콘텐츠" 등의 요청에 사용한다.
---

# CISA 지식베이스 콘텐츠 작성 스킬

## 프로젝트 기본 정보

- **레포**: `jeonck/cisa` (GitHub)
- **사이트**: `https://jeonck.github.io/cisa/`
- **로컬 경로**: `/Users/mac/ws/claude/cisa/docs/`
- **언어**: 한국어 (전문 용어는 영문 병기)
- **빌드 검증**: 문서 작성 후 반드시 `npm run build --prefix /Users/mac/ws/claude/cisa` 실행

도메인 전체 구조와 URL 매핑은 `references/domain-structure.md`를 참고하라.
완전한 빈 문서 템플릿은 `references/document-template.md`를 참고하라.

---

## 문서 작성 표준 형식

### Frontmatter

```yaml
---
sidebar_position: N   # intro=1, 하위항목=2,3,4...
title: X.X 한글 제목
---
```

### 필수 10섹션 구조 (순서 엄수)

```
# 한글 제목
**English Title**

:::info 관련 표준
CISA Domain X.X / ISO/IEC XXXXX / NIST SP 800-XXX
:::

<메타데이터 HTML 테이블>

---

## 1. 개요 및 배경
## 2. 핵심 개념 및 원칙
## 3. 프로세스 / 방법론   ← Mermaid 다이어그램 포함
## 4. CISA 감사 체크리스트  ← HTML 테이블 필수
## 5. 관련 표준 및 참고
## 관련 문서             ← 절대경로 링크
```

### 메타데이터 HTML 테이블

```html
<table>
  <colgroup>
    <col style={{width: '20%'}} />
    <col style={{width: '80%'}} />
  </colgroup>
  <tbody>
    <tr><td><strong>문서번호</strong></td><td>BP-XXX-NN</td></tr>
    <tr><td><strong>제개정일</strong></td><td>YYYY-MM-DD</td></tr>
    <tr><td><strong>관리부서</strong></td><td>IT 감사실</td></tr>
    <tr><td><strong>적용범위</strong></td><td>...</td></tr>
    <tr><td><strong>통제목적</strong></td><td>...</td></tr>
  </tbody>
</table>
```

**문서번호 체계**: `BP-AUD-01`~05 / `BP-GOV-01`~04 / `BP-DEV-01`~04 / `BP-OPS-01`~05 / `BP-SEC-01`~05 / `BP-TKT-01`~03

---

## Mermaid 다이어그램 규칙

1. **줄바꿈**: `<br/>` 사용 — `\n` 절대 금지
2. **subgraph 라벨**: 이모지 금지
3. **모든 노드·화살표 라벨**: `""` 로 감싸기
4. **`&` 체인**: 각 줄로 분리 (`A --> B` / `A --> C`)

**색상 팔레트** (모두 `color:#fff`):

| 이름 | fill | stroke |
|------|------|--------|
| 파랑 | `#2563EB` | `#1D4ED8` |
| 보라 | `#7C3AED` | `#6D28D9` |
| 주황 | `#EA580C` | `#C2410C` |
| 청록 | `#0891B2` | `#0E7490` |
| 녹색 | `#16A34A` | `#15803D` |
| 네이비 | `#1E3A5F` | `#1E3A5F` |
| 빨강 | `#DC2626` | `#B91C1C` |

---

## 감사 체크리스트 HTML 테이블

```html
<table>
  <colgroup>
    <col style={{width: '7%'}} />
    <col style={{width: '23%'}} />
    <col style={{width: '38%'}} />
    <col style={{width: '32%'}} />
  </colgroup>
  <thead>
    <tr>
      <th>ID</th>
      <th>통제 목적</th>
      <th>감사 수행 절차</th>
      <th>필수 증적 파일</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>AUD-XX-01</strong></td>
      <td>통제 목적 기술</td>
      <td>1. 첫 번째 절차<br/>2. 두 번째 절차<br/>3. 세 번째 절차</td>
      <td>증적 파일 1<br/>증적 파일 2</td>
    </tr>
  </tbody>
</table>
```

**중요**: `<td>` 여는 태그 직후 줄바꿈 금지 — MDX 파싱 오류 발생.
내용은 반드시 `<td>내용</td>` 형태로 같은 줄에 작성하고, 줄바꿈은 `<br/>` 사용.

---

## 관련 문서 링크 규칙

**반드시 절대경로 사용** — 상대경로(`./`, `../`)나 `.md` 확장자 포함 링크는 로컬 서버에서 깨진다.

```markdown
## 관련 문서

- [X.X 문서 제목](/docs/audit-process/audit-charter) — 연관 설명
- [X.X 문서 제목](/docs/it-governance/frameworks) — 연관 설명
```

**도메인별 URL 접두어:**
- Domain 1: `/docs/audit-process/`
- Domain 2: `/docs/it-governance/`
- Domain 3: `/docs/system-development/`
- Domain 4: `/docs/it-operations/`
- Domain 5: `/docs/information-security/`
- Domain 6: `/docs/audit-toolkits/`

---

## 빌드 검증 및 배포

```bash
# 빌드 검증 (문서 작성 후 필수)
npm run build --prefix /Users/mac/ws/claude/cisa

# Git 커밋 & 푸시
git add docs/경로/파일.md
git commit -m "[Domain X.X] 문서 제목 본문 작성

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push
```

에러 발생 시:
- MDX 파싱 에러: `<td>` 줄바꿈 문제 → Python으로 일괄 수정
- 깨진 링크: `grep "linking to"` 로 원인 파악 → 절대경로로 교체

---

## 대량 문서 병렬 작성 전략

여러 도메인 문서를 한 번에 작성할 때:

1. 도메인을 단위로 서브에이전트 병렬 실행 (최대 6개)
2. 각 에이전트 프롬프트에 포함할 항목:
   - 공통 형식 규칙 (Mermaid 색상, HTML 테이블 형식)
   - 담당 파일 절대경로 목록
   - 각 파일별 작성 내용 개요
   - git/npm 명령 실행 금지 지시
3. 완료 후 stub 잔존 확인: `grep -rl "작성 예정" docs/`
4. `npm run build` 로 MDX 오류 및 깨진 링크 일괄 검증

---

## 완성 문서 품질 체크리스트

- [ ] 10섹션 구조 완비
- [ ] Mermaid 다이어그램 최소 1개 (권장 2개)
- [ ] 감사 체크리스트 AUD 항목 4개 이상
- [ ] `:::info 관련 표준` 블록 포함
- [ ] 관련 문서 절대경로 링크 (`.md` 확장자 없음)
- [ ] `npm run build` 통과 확인
