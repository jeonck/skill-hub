---
name: hextra-roadmap-kb
description: Scaffolds a Korean-language Hugo + Hextra "topic learning roadmap" knowledge-base site — the same structure as the ai-security project (hero home with feature grid, numbered docs roadmap split into categories, Labs, Tools/References, Blog with RSS, and a Glossary backed by data/ko/termbase.yaml), plus a GitHub Pages Actions deploy workflow. Use when the user asks to build a new topic-based Korean learning/knowledge-base site, or to replicate the ai-security project's structure for a different subject (e.g. "이 프로젝트 형태로 OO 주제 사이트 만들어줘").
---

# Hextra Roadmap KB Builder

새로운 주제(topic)에 대해, ai-security 프로젝트와 동일한 형태의 "학습 로드맵형" 지식베이스를 빠르게 만듭니다.

## 사이트 구조 개요

```
content/
  _index.md            # 홈 (layout: hextra-home, 히어로 + feature-grid)
  docs/
    _index.md           # 로드맵 개요 (추천 순서, 배경별 진입점, N주 플랜, 전체 섹션 카드)
    <category-1>/
      _index.md         # "① 카테고리명" weight=1, 토픽 카드 목록
      <topic-a>.md
      <topic-b>.md
    <category-2>/
      _index.md         # "② 카테고리명" weight=2
      ...
  labs/
    _index.md           # 실습 목록 + 환경설정 안내 + 안전 경고
    lab1-*.md
    lab2-*.md
  tools/
    _index.md           # 도구/표준 참고자료 개요
    *.md                 # 도구셋별 페이지
  blog/
    _index.md           # RSS 배지 + 소개
    *.md                 # 포스트
  glossary/
    _index.md           # layout: glossary
data/
  ko/
    termbase.yaml        # {{< term "용어" >}} 숏코드가 참조하는 용어집 데이터
assets/
  css/
    custom.css           # 좌측 사이드바 접기/펼치기 토글 스타일
  js/
    core/
      sidebar-toggle.js  # 좌측 사이드바 접기/펼치기 토글 스크립트
.github/workflows/
  deploy.yml             # Hugo build + GitHub Pages 배포
hugo.toml
.gitmodules
.gitignore
```

핵심 아이디어:
- **docs**: "왜/무엇을, 어떤 순서로" — 이론·로드맵
- **labs**: "그대로 따라 하면 재현되는" 단계별 실습
- **tools**: "어떤 도구로, 어디서 더 읽나" — 참고자료
- **blog** / **glossary**: 보조 콘텐츠
- 모든 섹션은 menu.main에서 1~5순위로 연결되고, 6=GitHub 링크, 7=검색

## 시작 전에 — 필요한 입력값

작업을 시작하기 전에 사용자에게서 다음 정보를 확보하거나, 합리적으로 추정해 확인받습니다:

1. **주제(topic)**: 예) "AI Security" → "클라우드 보안", "재무제표 분석" 등
2. **사이트 제목 / GitHub repo 이름 / GitHub 사용자명** → `baseURL`, `GITHUB_URL` 결정
3. **docs 카테고리 N개** (보통 5~6개): 각 카테고리의 한글명, 1줄 설명, 아이콘 후보
   - ai-security 예시: 기반 지식 / 공격 기법 / 방어 기법 / 인프라·공급망 보안 / 거버넌스·리스크 관리 / 레드팀·실전 경험
4. **추천 학습 순서**와 그 이유 (callout에 들어갈 한 단락)
5. **배경별 진입점** (예: GRC / AppSec / ML Engineer 같은 독자 유형 2~3개)
6. **각 카테고리별 토픽 페이지 목록** (카테고리당 보통 3~4개)
7. **Labs 2개 이상**: 실습 제목/목표, 필요 패키지
8. **Tools 섹션 카테고리** (보통 2~3개 도구 묶음 + "표준 및 참고 문서")
9. **용어집 용어 10~20개**

위 정보가 부족하면, ai-security 프로젝트(`content/`, `hugo.toml`, `data/ko/termbase.yaml`)를 참고용 실례로 보여주고 동일한 패턴으로 새 주제에 맞게 제안한 뒤 사용자 확인을 받습니다.

## 워크플로우

### 1. Hugo 프로젝트 초기화

```bash
hugo new site . --force --format toml
git init
mkdir -p themes
git submodule add https://github.com/imfing/hextra.git themes/hextra
```

### 2. hugo.toml 작성

`assets/hugo.toml.template`을 복사해 `hugo.toml`로 저장하고 다음 플레이스홀더를 채웁니다:
- `{{BASE_URL}}` — 예: `https://<github-user>.github.io/<repo>/`
- `{{SITE_TITLE}}`
- `{{ROADMAP_MENU_LABEL}}` — 메인 메뉴의 1번 항목 이름 (예: "AI 보안 학습 로드맵")
- `{{SITE_DESCRIPTION}}`
- `{{GITHUB_URL}}`

메뉴 구조(실습/도구/블로그/용어집/GitHub/검색)는 그대로 유지합니다.

### 3. 홈페이지 (`content/_index.md`)

`assets/home.md.template`을 기반으로:
- 히어로 배지/헤드라인/서브타이틀/CTA 버튼 채우기
- docs 카테고리 수만큼 `hextra/feature-card` 블록을 ①②③… 번호를 붙여 반복 작성 (각각 `link="docs/<slug>"`)

### 4. docs 로드맵 개요 (`content/docs/_index.md`)

`assets/docs-index.md.template` 기반으로 작성. 포함 요소:
- 카테고리 번호 목록 + 1줄 설명
- "추천 학습 순서" callout (왜 이 순서인지 근거 포함)
- "배경별 추천 진입점" 카드 (독자 유형별)
- N주 학습 플랜 표
- "전체 섹션" 카드 (홈페이지 feature-grid와 1:1 대응)

### 5. 카테고리별 섹션 (`content/docs/<category>/_index.md`)

각 카테고리마다 `assets/category-index.md.template` 기반으로:
- `title: "① 카테고리명"`, `weight: <순번>`
- 왜 이 영역이 필요한지 설명 + warning/info callout
- 이 카테고리에 속한 토픽 페이지들을 번호 목록 + 카드로 나열
- 마지막에 다음 카테고리로 연결되는 info callout

각 토픽 페이지는 `assets/topic-page.md.template` 기반 (`title`, `weight` + 자유 서술 + 다른 섹션으로의 교차 링크 callout).

### 6. Labs 섹션 (`content/labs/`)

- `_index.md`: `assets/labs-index.md.template` — docs와의 차이점 설명, 환경설정 callout, 실습 카드 목록, 권한/안전 경고
- 각 실습: `assets/lab-page.md.template` — 목표/사전준비/단계별 실행/결과 확인/체크리스트 구조 고정

### 7. Tools 섹션 (`content/tools/`)

- `_index.md`: `assets/tools-index.md.template` — docs/labs와의 역할 구분 설명, 도구셋 카드
- 각 도구셋 페이지: `assets/tool-page.md.template`

### 8. Blog 섹션 (`content/blog/`)

- `_index.md`: `assets/blog-index.md.template` (RSS 배지 포함)
- 첫 포스트: `assets/blog-post.md.template`

### 9. Glossary + termbase (`content/glossary/`, `data/ko/`)

- `content/glossary/_index.md`: `assets/glossary-index.md.template` (그대로, `layout: glossary`는 Hextra 테마 내장 기능)
- `data/ko/termbase.yaml`: `assets/termbase.yaml.template` 기반으로 새 주제의 핵심 용어 10~20개 작성. 본문에서 `{{< term "용어" >}}` 숏코드로 참조 가능.

### 10. GitHub Pages 배포

- `.github/workflows/deploy.yml`: `assets/deploy.yml.template` 그대로 복사 (HUGO_VERSION은 최신 stable로 갱신 검토)
- `.gitignore`: `assets/gitignore.template` 그대로 복사
- GitHub repo 설정에서 Pages Source를 **GitHub Actions**로 변경 필요 (사용자에게 안내)

### 11. 좌측 사이드바 접기/펼치기 토글

- `assets/custom.css.template` → `assets/css/custom.css`로 그대로 복사
- `assets/sidebar-toggle.js.template` → `assets/js/core/sidebar-toggle.js`로 그대로 복사
- 별도 설정 불필요 — Hugo가 프로젝트의 `assets/css/custom.css`와 `assets/js/core/*.js`를 Hextra 테마의 동일 경로 리소스에 자동으로 병합/오버라이드함.
- 데스크탑(md 이상) 화면에서 네비게이션 바 아래 좌측에 둥근 토글 버튼이 나타나며, 클릭 시 좌측 사이드바 전체를 숨기고 본문을 넓힘. 상태는 `localStorage`에 저장되어 페이지 이동/새로고침 후에도 유지됨.

## 주의 사항

- Hugo **Extended** 버전 필요 (Mermaid/SCSS 등 Hextra 기능 사용 시)
- `enableGitInfo = true`이므로 `displayUpdatedDate`가 git 커밋 날짜를 사용 — 처음 커밋 전에는 날짜가 비어 보일 수 있음
- 용어집 숏코드(`term`)와 `layout: glossary`는 Hextra 테마가 기본 제공하므로 커스텀 레이아웃 작성 불필요
- 모든 한글 메뉴/제목 텍스트는 주제에 맞게 새로 작성하되, **구조(카테고리 수, 카드 배치, 메뉴 순서)는 그대로 재사용**하는 것이 이 스킬의 핵심

## 알려진 함정 (ai-security 프로젝트에서 실제로 발생한 문제)

### 1. 내부 링크 404 — pretty URL의 상대 경로 깊이

Hugo는 `content/docs/<category>/<page>.md`를 leaf bundle pretty URL `/docs/<category>/<page>/`로 렌더링합니다. 즉 **렌더링된 페이지 경로는 소스 파일 경로보다 한 단계 더 깊습니다.** 본문에서 상대 링크를 쓸 때 다음 규칙을 지켜야 합니다.

- 같은 카테고리 내 다른 문서: `../other-page/` (← `./other-page/`가 아님)
- 다른 카테고리의 문서: `../../other-category/other-page/`
- 섹션 인덱스로: `../../section/` (← `../section/_index`가 아님, `_index`는 제거하고 슬래시로 끝맺음)
- `content/labs/*.md`, `content/tools/*.md`의 카드 숏코드(`{{</* card link="/docs/..." */>}}`)에서 **절대 경로(`/docs/...`, `/tools/...`)는 쓰지 말 것** — Hextra의 `card.html`은 절대 경로 `link=`에 `baseURL`의 서브패스(`/<repo>/`)를 붙이지 않아 깨짐. `link="../../docs/.../"`처럼 상대 경로로 작성.

콘텐츠 작성이 끝나면 `hugo server --disableFastRender`로 띄운 뒤, sitemap을 크롤링해 모든 `<a href>`를 실제로 요청해보는 스크립트로 깨진 링크가 0개인지 확인합니다.

### 2. LaTeX/KaTeX 수식이 렌더링되지 않음

`assets/hugo.toml.template`에는 이미 다음 설정이 포함되어 있으므로 그대로 사용하면 문제없지만, **이 설정 없이는 `$x$`, `$$...$$` 같은 수식이 원본 텍스트로 그대로 노출됩니다** (goldmark의 `passthrough` 확장이 없으면 Hextra의 `render-passthrough.html` 훅이 호출되지 않아 `hasMath`가 세팅되지 않고 KaTeX 스크립트가 로드되지 않음):

```toml
[markup.goldmark.extensions.passthrough]
  enable = true
  [markup.goldmark.extensions.passthrough.delimiters]
    block = [['\[', '\]'], ['$$', '$$']]
    inline = [['\(', '\)'], ['$', '$']]
```

수식이 포함된 페이지가 있다면, 로컬 빌드 후 렌더링 결과에 `katex`/`katex-display` 클래스가 생성되는지 확인합니다.
- 콘텐츠 작성이 끝나면 `hugo server`로 로컬에서 확인한 뒤 커밋

### 3. 한글 조사가 붙는 `**볼드**`가 렌더링되지 않음

CommonMark의 "right-flanking delimiter" 규칙 때문에, 닫는 `**` 바로 앞이 구두점(`)`, `"`, `'` 등)이고 바로 뒤에 공백 없이 한글 조사(는/은/이/가/을/를/와/과/의/에/로 등)나 영문/숫자가 붙으면 `**`가 강조를 닫지 못하고 **그대로 텍스트로 노출**됩니다.

예: `**NIST AI RMF(AI RMF)**는` → `**`가 글자 그대로 출력됨.

수정 방법은 닫는 `**` 바로 앞을 영문/한글 글자로 만들어주는 것 — 구두점을 강조 밖으로 빼냅니다:
- 영문 병기: `**텍스트(English)**는` → `**텍스트**(English)는`
- 인용구: `**"텍스트"**는` → `"**텍스트**"는` (여는/닫는 인용부호 모두 밖으로)

콘텐츠 작성 후 다음 스크립트로 모든 페이지를 스캔해 0건인지 확인합니다:
```bash
python3 - <<'EOF'
import re, glob
pattern = re.compile(r'<div class="content">(.*?)</main>', re.S)
for f in glob.glob("public/**/index.html", recursive=True):
    html = open(f, encoding="utf-8").read()
    m = pattern.search(html)
    body = m.group(1) if m else ""
    if "**" in body:
        print(f, body.count("**"))
EOF
```
