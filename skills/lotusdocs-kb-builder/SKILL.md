---
name: lotusdocs-kb-builder
description: Hugo Lotus Docs 테마(github.com/colinwilson/lotusdocs, Hugo Modules로 설치)를 사용하여 문서/지식베이스 사이트를 처음부터 구축하고 GitHub Actions로 GitHub Pages에 배포할 때 사용한다. 커스텀 도메인 연결까지 포함한다. 주제는 무관하다 — 보안, 개발, 자격증 공부, 사내 위키 등 어떤 지식베이스든 적용 가능한 일반화된 스킬이다. "Lotus Docs로 사이트 만들어줘", "Hugo 지식베이스를 GitHub Pages에 호스팅해줘", "이 자료로 Lotus Docs 문서 사이트 만들어줘" 같은 요청에 사용한다.
---

# Lotus Docs KB Builder

## 개요

이 스킬은 [Lotus Docs](https://github.com/colinwilson/lotusdocs) Hugo 테마로
문서/지식베이스 사이트를 구축하고, GitHub Actions를 통해 GitHub Pages에
배포하는 전체 워크플로우를 제공한다. Lotus Docs는 git submodule이 아니라
**Hugo Module**로 배포되므로 일반적인 Hugo 테마 설치 가이드와 몇 가지
지점에서 다르게 동작한다 — 이 스킬은 그 차이점(특히 GitHub Actions에서
Go 툴체인이 필요한 점, 그리고 카테고리 간 Prev/Next 네비게이션이 꼬이는
버그)을 미리 회피하도록 만들어졌다.

콘텐츠 자체(어떤 문체로 쓸지, 어떤 다이어그램 스타일을 쓸지)는 이 스킬의
범위가 아니다 — 이 스킬은 사이트 뼈대·설정·배포에 집중한다. 콘텐츠 작성
방식이 정해져 있다면 그 스킬과 이 스킬을 함께 쓰면 된다.

## 언제 사용하는가

- 새 Lotus Docs 사이트를 처음부터 만들 때
- 기존 자료(다른 리포지토리의 마크다운 문서 등)를 Lotus Docs 사이트 구조로
  옮기고 GitHub Pages에 올릴 때
- Lotus Docs 사이트의 Prev/Next 네비게이션이 이상하게 동작하거나, GitHub
  Actions 빌드가 실패하거나, 커스텀 도메인 HTTPS가 활성화되지 않는 등의
  문제를 진단할 때 (→ `references/pitfalls.md`)

## 워크플로우

### 0. 사전 확인

```bash
hugo version   # Extended 버전인지 확인 (v0.161.1+extended 등)
go version     # Hugo Modules 해석에 필요
gh auth status # GitHub Pages/리포지토리 API 호출에 필요
```

### 1. 사이트 스캐폴딩

```bash
hugo new site . --format toml --force   # 빈 디렉터리가 아니어도 진행 (pitfalls.md #8)
hugo mod init github.com/<owner>/<repo>
```

### 2. `hugo.toml` 작성

`assets/site-template/hugo.toml.template`을 프로젝트 루트에
`hugo.toml`로 복사한 뒤 `{{SITE_TITLE}}`, `{{DOMAIN}}`, `{{GITHUB_OWNER}}`,
`{{GITHUB_REPO}}` 플레이스홀더를 실제 값으로 치환한다. 커스텀 도메인이
아직 없다면 `baseURL`을 GitHub Pages 기본 URL(`https://<owner>.github.io/<repo>/`)로
설정한다.

```bash
hugo mod get -u github.com/colinwilson/lotusdocs github.com/gohugoio/hugo-mod-bootstrap-scss/v5
hugo mod tidy
```

### 3. 콘텐츠 구조 설계

카테고리(=사이드바 섹션) 목록을 먼저 확정한다. 각 카테고리마다:

- `content/docs/<category-slug>/_index.md` — `assets/site-template/content/docs/category-_index.md.template` 참고. `weight`는 사이드바 순서용으로 `10, 20, 30...`처럼 작게 부여.
- 그 안의 개별 문서 페이지들 — `assets/site-template/content/docs/item-page.md.template` 참고.

**중요**: 개별 페이지의 `weight`는 카테고리마다 `10, 20, 30...`을 반복하면
안 된다. 사이트 전체에서 유일해야 하며, `1000 * <카테고리 순번> + 10 *
<카테고리 내 순번>` 공식을 쓴다. 이유와 세부 사항은
`references/pitfalls.md` 2번 항목 참고 — 이 규칙을 건너뛰면 나중에
Prev/Next 네비게이션이 카테고리를 무작위로 넘나든다.

`content/docs/_index.md`는 `assets/site-template/content/docs/_index.md.template`
참고 — 전체 카테고리 목록을 한눈에 보여주는 개요 페이지.

콘텐츠가 많을 때(수십~수백 페이지)는 카테고리별로 서브에이전트를 병렬로
띄워 작성하는 것이 효율적이다. 이때도 위 weight 공식은 각 서브에이전트
프롬프트에 명시해서 충돌을 미리 방지한다.

### 4. 랜딩 페이지 (`data/landing.yaml`)

Lotus Docs는 `content/_index.md` 없이 `data/landing.yaml`만으로 홈페이지를
렌더링한다. `assets/site-template/data/landing.yaml.template`을
`data/landing.yaml`로 복사하고 채운다. 전체 필드 스키마(hero, featureGrid,
imageText, imageCompare)는 `references/landing-yaml-schema.md` 참고 —
이미지 에셋이 없는 새 사이트라면 `hero`(텍스트만) + `featureGrid`만으로
충분하다.

아이콘 이름은 임의 문자열이 아니라 [Google Material
Symbols](https://fonts.google.com/icons) 리거처 이름이어야 한다 (예:
`lock`, `hub`, `cloud`, `policy`, `fingerprint`). 존재하지 않는 이름을
넣으면 에러 없이 그냥 빈 자리로 렌더링되므로 브라우저로 반드시 확인한다.

### 5. `.gitignore`

`assets/site-template/gitignore.template`을 `.gitignore`로 복사한다
(`public/`, `resources/`, `.hugo_build.lock` 등 Hugo 빌드 산출물 제외).

### 6. 로컬 빌드 검증

```bash
hugo --minify   # 에러 없이 빌드되는지 확인
python3 <this-skill-dir>/scripts/check_internal_links.py content/docs
```

`hugo server`로 띄워서 브라우저로 실제 확인한다 — 최소한 홈페이지, 카테고리
페이지 1개, 개별 문서 페이지 1개(Mermaid 다이어그램이 있다면 렌더링 확인),
그리고 Prev/Next 카드가 같은 카테고리 순서로 흐르는지 확인한다.

### 7. GitHub Actions 배포 워크플로우

`assets/site-template/.github/workflows/hugo.yml.template`을
`.github/workflows/hugo.yml`로 복사한다. `HUGO_VERSION` 값을 로컬 `hugo
version`과 맞춘다. **Go 설치 스텝을 절대 지우지 않는다** — Hugo Modules
해석에 필요하며, 없으면 CI 빌드만 원인 파악이 어렵게 실패한다
(`references/pitfalls.md` 3번 항목).

### 8. 리포지토리 생성 및 푸시

```bash
git init -b main
git add -A
git commit -m "..."
gh repo create <owner>/<repo> --public --source=. --remote=origin
git push -u origin main
```

### 9. GitHub Pages 활성화 + 커스텀 도메인

```bash
./scripts/setup_github_pages.sh <owner>/<repo> [custom-domain]
```

커스텀 도메인을 쓴다면, 위 스크립트를 돌리기 전에 `static/CNAME` 파일에
도메인 문자열 한 줄을 커밋해 둔다 (`references/pitfalls.md` 5번 항목 —
Hugo가 매 빌드마다 `public/CNAME`으로 복사해줘야 GitHub Pages가 도메인
설정을 유지한다). DNS가 이미 GitHub Pages를 가리키고 있어야 스크립트의
HTTPS 인증서 대기 단계가 성공한다.

### 10. 배포 확인

```bash
gh run list --repo <owner>/<repo> --limit 1
gh run watch --repo <owner>/<repo> <run-id>
curl -s -o /dev/null -w "HTTP %{http_code}\n" https://<domain-or-github-io-url>/
```

## 콘텐츠 확장 (기존 사이트에 카테고리/페이지 추가)

기존 사이트에 새 카테고리나 대량의 새 페이지를 추가할 때는, 먼저 기존
페이지들의 weight가 새로 추가될 양을 감안해도 카테고리 블록(예: 1000단위)을
넘치지 않는지 확인한다. 넘칠 것 같으면 기존 페이지들의 weight를 더 큰
배수(예: 10000단위)로 먼저 재부여(renumber)한 뒤 새 콘텐츠를 추가한다 —
이 순서를 지키지 않으면 새 카테고리의 weight 블록이 기존 카테고리와
충돌해서 다시 Prev/Next가 꼬인다.

## 참고 자료

- `references/pitfalls.md` — 이 스킬이 회피하는 8가지 함정의 원인과 해결책 상세 설명. 문제가 생기면 먼저 여기를 확인한다.
- `references/landing-yaml-schema.md` — `data/landing.yaml`의 전체 필드 스키마 (hero, featureGrid, imageText, imageCompare).
- `assets/site-template/` — 그대로 복사해서 채워 넣는 템플릿 파일 모음.
- `scripts/check_internal_links.py` — 콘텐츠 트리 전체의 상대/절대 마크다운 링크가 실제로 존재하는 페이지를 가리키는지 검증.
- `scripts/setup_github_pages.sh` — GitHub Pages(Actions 빌드) 활성화, 커스텀 도메인 연결, HTTPS 강제 적용을 한 번에 처리.
