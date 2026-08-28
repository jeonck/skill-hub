---
name: hugo-stack-blog
description: Hugo 블로그를 Hugo Stack 테마(CaiJimmy/hugo-theme-stack v4)로 구성하고 GitHub Pages에 자동 배포하는 스킬. Hugo 0.157+의 Hugo Module 방식 설정과 GitHub Actions 배포까지 처음부터 끝까지 수행. 사용자가 Hugo 블로그, GitHub Pages 블로그, Stack 테마 블로그를 만들거나 배포하려 할 때, 혹은 "블로그 사이트 구성해서 깃헙에 배포", "Hugo 사이트 만들어줘", "깃헙 페이지에 블로그 올려" 등의 표현을 사용할 때 트리거.
---

# Hugo Stack 블로그 → GitHub Pages 배포

이 스킬은 **Hugo + Stack 테마 + GitHub Pages** 조합의 블로그를 실패 없이 한 번에 구성·배포한다. 핵심은 Hugo 0.157+에서 발생하는 설정 호환성 함정들을 우회하는 데 있다.

## 사전 점검 (빌드 실패를 막는 가장 중요한 단계)

아래 도구가 모두 있어야 한다. **하나라도 빠지면 빌드가 조용히 실패하거나 워크플로가 깨진다.** 반드시 먼저 점검한다.

```
which hugo   # extended 버전 필수. `hugo version` 출력에 "extended" 포함 여부 확인
which git
which gh     # GitHub CLI. 인증 완료 상태(`gh auth status`), `workflow` scope 보유 필수
which go     # ⚠️ 필수. 없으면 반드시 설치한다 (이 스킬의 핵심 함정 — 아래 "왜 Go가 필요한가" 참조)
```

- **Hugo가 extended가 아니면** Stack 테마의 SCSS 컴파일이 안 된다. macOS면 `brew install hugo`, extended 빌드 설치.
- **Go가 없으면** `brew install go` (또는 공식 사이트). 이 스킬은 Hugo Module 방식을 사용하므로 Go가 반드시 필요하다.
- **gh 인증의 `workflow` scope이 없으면** GitHub Actions 워크플로 푸시가 거부된다. `gh auth refresh -h github.com -s workflow` 로 추가.

사용자의 git identity도 확인: `git config --global user.name`, `git config --global user.email`.

## 왜 Go가 필요한가 (이 스킬의 존재 이유)

Hugo 0.157부터 **`theme = "..."` 키가 더 이상 테마를 로드하지 않는다.** Hugo 공식 방향은 Hugo Module(Go module) 방식뿐이다. Stack 테마 v4도 `go.mod`를 포함하며 오직 module import만 지원한다.

Go 없이 `theme = "hugo-theme-stack"`를 쓰면 **에러 없이 빌드는 되지만 모든 페이지가 "found no layout file" 경고와 함께 빈 페이지만 나온다.** (직접 겪은 함정.) 따라서 이 스킬은:

1. 로컬 개발: `go install` + `hugo mod init` 으로 프로젝트를 모듈화
2. CI: 워크플로에 `actions/setup-go` 단계 포함

두 환경 모두 Go를 요구한다. 이 점을 절대 건너뛰지 말 것.

## 배포 URL에 따른 설정 분기 (baseURL)

사용자에게 리포 이름을 먼저 확인한다. baseURL과 permalink가 여기에 의존한다.

| 리포 이름 | 배포 URL | baseURL |
|----------|---------|---------|
| `<user>.github.io` | `https://<user>.github.io/` | `https://<user>.github.io/` |
| 그 외 (예: `z-hugo`) | `https://<user>.github.io/<repo>/` | `https://<user>.github.io/<repo>/` |

GitHub Actions의 `actions/configure-pages`가 런타임에 올바른 baseURL을 주입하므로(`--baseURL "${{ steps.pages.outputs.base_url }}/"`), 로컬 `hugo.toml`의 baseURL은 대략 적어도 된다. 하지만 사이트 내부 링크 정확도를 위해 실제 URL을 적는다.

## 실행 워크플로

### 1. Hugo 사이트 생성

빈(또는 비어있는) 디렉토리에서:

```bash
hugo new site . --force
```

`hugo new site`가 만드는 기본 `hugo.toml`은 **삭제한다.** (아래 템플릿으로 교체.)

### 2. 프로젝트 모듈화 (Go 필수)

```bash
hugo mod init github.com/<user>/<repo>
```

`go.mod`와 (나중에) `go.sum`이 생성된다. 둘 다 커밋해야 한다.

### 3. hugo.toml 작성

`assets/hugo.toml` 템플릿을 복사한 뒤 변수를 치환:

| 플레이스홀더 | 의미 | 예시 |
|------------|------|------|
| `{{BASE_URL}}` | 배포 URL | `https://jeonck.github.io/z-hugo/` |
| `{{TITLE}}` | 사이트 제목 | `jeonck's blog` |
| `{{SUBTITLE}}` | 사이드바 부제목 | `Hugo로 만든 블로그` |
| `{{YEAR}}` | `params.footer.since` | `2026` |

**⚠️ 절대 사용하면 안 되는 deprecated 키들 (Hugo 0.158+ 경고/제거):**
- `languageCode` → `locale` 사용
- `languages.<lang>.languageName` → `languages.<lang>.label` 사용
- `theme = "..."` → `[[module.imports]]` 사용 (이게 전체 스킬의 핵심)

### 4. 콘텐츠 배치

아래 템플릿들을 치환해서 생성. `{{DATE}}`는 `YYYY-MM-DD` 형식 (오늘 날짜).

```
content/page/about/index.md      ← assets/content_page_about.md
content/page/search/index.md     ← assets/content_page_search.md
content/page/archives/index.md   ← assets/content_page_archives.md
content/post/hello-world.md      ← assets/content_post_hello.md
content/post/markdown-test.md    ← assets/content_post_markdown.md
```

permalink가 `post = "/p/:slug/"`이므로 포스트 URL은 `/p/<slug>/`가 된다.

### 5. .gitignore

`assets/gitignore`를 `.gitignore`로 복사.

### 6. GitHub Actions 워크플로

`assets/github-actions-hugo.yml`을 `.github/workflows/hugo.yml`로 복사. **이 워크플로는 `actions/setup-go` 단계를 포함한다 — 절대 제거하지 말 것.** Go가 없으면 CI 빌드가 "found no layout file"로 실패한다.

워크플로의 권한 블록을 유지할 것: `pages: write`, `id-token: write` (deploy-pages에 필요).

### 7. 로컬 빌드 검증 (푸시 전 필수)

```bash
hugo --gc --minify
```

**성공 기준 (둘 다 충족해야 진행):**
1. "found no layout file" 경고가 **없어야** 함. (있으면 테마가 로드 안 된 것 — Go 설치/`hugo mod init` 재확인.)
2. `public/index.html`이 생성되어야 함.

deprecated 경고(`languageCode`, `languageName`)는 빌드를 막지 않지만 위 템플릿으로 작성했다면 나오지 않아야 한다.

### 8. 커밋 + GitHub 리포 생성

```bash
git init -b main
git add -A
git commit -m "Initial Hugo blog setup with Stack theme"
gh repo create <user>/<repo> --public --source=. --remote=origin --push
```

### 9. Pages 설정 (build_type=workflow)

```bash
gh api -X POST repos/<user>/<repo>/pages -f build_type=workflow
```

**이 단계를 빠뜨리면** Pages가 "deploy from branch" 모드로 잘못 잡혀 배포가 안 된다. `build_type=workflow`가 Pages 소스를 GitHub Actions로 지정한다.

### 10. 배포 추적 + 검증

```bash
sleep 5
gh run list --repo <user>/<repo> --limit 1
gh run watch <run-id> --repo <user>/<repo> --exit-status
curl -sI -o /dev/null -w "%{http_code}" https://<user>.github.io/<repo>/
```

`200`이면 성공. 사이트 `<title>`도 확인:

```bash
curl -s https://<user>.github.io/<repo>/ | grep -oE "<title>[^<]+</title>"
```

## 함정 요약 (재발 방지)

1. **`theme` 키로는 테마가 안 로드됨** (Hugo 0.157+). 무조건 `[[module.imports]]`.
2. **Go 없으면 module import가 조용히 실패** — `hugo mod graph`가 비어있고 "found no layout file" 경고만 나옴.
3. **`config/_default/` 분산 구조에서 `[module]` 섹션이 인식 안 됨** — 단일 `hugo.toml`을 쓸 것. (이것도 직접 겪은 함정.)
4. **submodule 방식과 module import를 섞지 말 것** — 충돌로 테마 로드 실패. 이 스킬은 순수 module 방식만 사용.
5. **Pages `build_type=workflow` 설정 누락** — 리포 생성만으로는 배포가 안 됨.
6. **워크플로에서 `setup-go` 제거 금지** — CI에서 "found no layout file" 발생.

## 새 포스트 작성 (배포 후 안내)

```bash
hugo new content post/my-post.md
# 편집 후
git add . && git commit -m "new post" && git push
# main 브랜치 push 시 자동 배포
```

`draft: true`면 빌드에서 제외되니 배포하려면 `false`로 변경.

## 아티팩트

모든 템플릿은 이 스킬 디렉토리의 `assets/` 아래 있다:

- `assets/hugo.toml` — 사이트 설정 (플레이스홀더 포함)
- `assets/github-actions-hugo.yml` — 배포 워크플로 (Go setup 포함)
- `assets/gitignore` — .gitignore
- `assets/content_page_about.md` / `content_page_search.md` / `content_page_archives.md` — 페이지
- `assets/content_post_hello.md` / `content_post_markdown.md` — 샘플 포스트

각 파일의 플레이스홀더(`{{BASE_URL}}`, `{{TITLE}}`, `{{SUBTITLE}}`, `{{YEAR}}`, `{{DATE}}`)는 사용자 입력으로 치환한다.
