# Lotus Docs + Hugo Modules + GitHub Pages: 알려진 함정과 해결책

이 문서는 Lotus Docs 테마로 사이트를 만들고 GitHub Pages(Actions)로 배포할 때
실제로 마주쳤던 문제와 그 원인, 해결책을 정리한다. SKILL.md의 워크플로우를
따르면 대부분 자동으로 회피되지만, 문제가 생겼을 때 원인을 진단하는 용도로도
사용한다.

## 1. Deprecated Hugo 설정 키

Hugo v0.156~0.158부터 다음 키들이 deprecated 되었다. 최신 Hugo Extended에서
그대로 쓰면 빌드는 되지만 `WARN deprecated` 경고가 뜬다.

| Deprecated | 대체 |
|---|---|
| `languageCode` (최상위) | `locale` |
| `languages.<lang>.languageName` | `languages.<lang>.label` |
| `.Site.LanguageCode` (레이아웃 내부, 테마 코드) | 테마 쪽 문제이므로 무시 가능 |
| `.Site.Data` (레이아웃 내부, 테마 코드) | 테마 쪽 문제이므로 무시 가능 |

`assets/site-template/hugo.toml.template`은 이미 `locale`/`label`로
작성되어 있다.

## 2. Prev/Next 네비게이션이 카테고리를 넘나드는 문제 (가장 중요)

**증상**: 어떤 문서 페이지에서 "이전/다음" 카드가 같은 카테고리가 아니라
전혀 다른 카테고리의 페이지를 가리킨다.

**원인**: Lotus Docs의 `layouts/partials/docs/doc-nav.html`은 다음과 같이
동작한다.

```go-html-template
{{ $pages := where .Site.RegularPages "Section" .Section -}}
{{ with $pages.Next . -}} ... {{ end -}}
{{ with $pages.Prev . -}} ... {{ end -}}
```

`.Section`은 Hugo에서 항상 콘텐츠 트리의 **최상위 섹션**(여기서는 `docs`)을
가리키며, 하위 폴더(카테고리) 이름이 아니다. 즉 `$pages`는 `/docs/` 아래의
**모든** 페이지(카테고리 불문)를 담게 되고, `.Next`/`.Prev`는 이 전체 목록을
`weight` 기준으로 정렬해 앞뒤를 고른다.

카테고리마다 `weight: 10, 20, 30...`을 반복해서 쓰면(각 카테고리 폴더 안에서만
유일하면 된다고 착각하기 쉽다) 서로 다른 카테고리의 페이지들이 같은 weight
구간에서 충돌하고, 동률일 때의 타이브레이크(제목 알파벳 순 등)에 따라
Prev/Next가 사실상 무작위로 카테고리를 넘나든다.

**해결책**: 모든 문서 페이지의 `weight`를 사이트 전체에서 유일하게, 그리고
원하는 카테고리 순서대로 단조 증가하게 부여한다. 카테고리가 최대 수십 개,
카테고리당 페이지가 최대 수십 개인 일반적인 지식베이스 규모에서는 아래
공식이 안전하다.

```
weight = 1000 * <이 페이지가 속한 카테고리의 1부터 시작하는 순번>
       +   10 * <카테고리 내에서 이 페이지의 1부터 시작하는 순번>
```

예: 3번째 카테고리의 2번째 페이지 → `weight: 3020`.
카테고리 `_index.md` 자체의 weight는 이 공식과 무관하게 `10, 20, 30...`처럼
작게 둬도 된다 (사이드바의 카테고리 순서는 별도 로직이라 이 버그의 영향을
받지 않는다 — `_index.md`는 Hugo의 "section" kind라 애초에 `RegularPages`에
포함되지 않는다).

카테고리 개수나 카테고리당 페이지 수가 100개에 근접할 만큼 아주 큰 사이트라면
1000 대신 10000 같은 더 큰 배수를 쓴다.

콘텐츠를 나중에 더 추가해서 카테고리당 페이지가 100개를 넘어갈 것 같다면,
기존 페이지들의 weight를 먼저 새 배수로 재부여(renumber)한 뒤 새 콘텐츠를
추가한다 — 자세한 절차는 SKILL.md의 "콘텐츠 확장" 절 참고.

## 3. GitHub Actions에서 Hugo Modules가 실패하는 문제

Lotus Docs는 git submodule 테마가 아니라 **Hugo Module**
(`github.com/colinwilson/lotusdocs`)로 배포된다. 즉 `go.mod`/`go.sum`이
있고, `hugo` 명령 실행 시 내부적으로 Go 모듈 시스템으로 테마를 내려받는다.

CI 러너에 Hugo 바이너리만 설치하고 Go 툴체인을 설치하지 않으면 모듈 다운로드
단계에서 빌드가 실패한다 (에러 메시지가 항상 명확하지는 않다 — "go.mod not
found" 나 모듈 다운로드 관련 에러로 나타난다).

**해결책**: 워크플로우에 `actions/setup-go@v5` 스텝을 Hugo 설치 다음,
`hugo` 빌드 스텝 이전에 반드시 넣는다. `assets/site-template/.github/workflows/hugo.yml.template`에
이미 포함되어 있다. Go 버전 자체은 사이트에 Go 코드가 없으므로 최신 안정
버전이면 무엇이든 상관없다.

## 4. `gh api`로 boolean 값을 보낼 때 `-f`가 아니라 `-F`

```bash
# 틀림 — 문자열 "true"를 보내서 422 (not of type boolean)로 거부됨
gh api -X PUT repos/OWNER/REPO/pages -f https_enforced=true

# 맞음 — 대문자 -F 는 값을 JSON 타입으로 해석한다
gh api -X PUT repos/OWNER/REPO/pages -F https_enforced=true
```

`scripts/setup_github_pages.sh`가 이 문제를 이미 회피해서 작성되어 있다.

## 5. 커스텀 도메인은 `static/CNAME`에 둔다

GitHub Pages 커스텀 도메인은 리포지토리 설정(API로 `cname` 필드)뿐 아니라
배포된 `public/` 루트에 `CNAME` 파일이 있어야 유지된다. Hugo Modules
사이트는 보통 `.gitignore`에 `public/`을 넣으므로, 도메인 문자열을
`static/CNAME`에 커밋해 두면 Hugo가 매 빌드마다 `public/CNAME`으로
복사해 준다. `assets/site-template/`에는 플레이스홀더 없이 직접
`static/CNAME`을 만들도록 SKILL.md 워크플로우에 안내되어 있다 (도메인
하나짜리 텍스트 파일이라 별도 템플릿 파일을 두지 않았다).

## 6. 랜딩 페이지는 `content/_index.md` 없이도 동작한다

Lotus Docs의 `layouts/index.html`은 `content/_index.md`의 존재 여부와
무관하게 `data/landing.yaml`을 읽어서 홈페이지를 렌더링한다
(`hero`, `featureGrid`, `imageText`, `imageCompare` 블록). 즉 홈페이지
콘텐츠는 마크다운이 아니라 YAML 데이터 파일로 관리한다. 전체 스키마는
`references/landing-yaml-schema.md` 참고.

## 7. 아이콘은 Google Material Symbols 리거처 이름이어야 한다

`icon:` 프론트매터와 `data/landing.yaml`의 `icon:` 필드는 임의 문자열이
아니라 [Google Material Symbols](https://fonts.google.com/icons)의
정확한 리거처 이름(`lock`, `hub`, `cloud`, `fingerprint`, `radar`,
`auto_awesome` 등)이어야 렌더링된다. 오타나 존재하지 않는 이름을 넣으면
그냥 빈 자리로 렌더링되고 에러는 나지 않으므로, 브라우저로 시각 확인하기
전까지는 눈치채기 어렵다.

## 8. `hugo new site` 는 빈 디렉터리를 요구한다

작업 디렉터리에 `.claude/` 같은 숨김 폴더만 있어도 `hugo new site .`가
"already exists and is not empty" 에러를 낸다. `--force` 플래그를 쓰면
기존 파일을 보존한 채(덮어쓰지 않고) 진행한다.

## 9. 숫자로 시작하는 제목은 페이지 JS 전체를 죽인다

**증상**: 배포된 사이트가 스타일이 깨진 것처럼 보인다. 사이드바 토글,
드롭다운, 검색, 스크롤스파이가 전부 동작하지 않는다. 콘솔에는
`SyntaxError: Failed to execute 'querySelector' on 'Element':
'#1-ownership-and-documentation' is not a valid selector` 가 뜬다.

**원인**: `## 1. Ownership and documentation` 처럼 번호를 붙인 제목을 쓰면
Hugo가 제목 텍스트에서 그대로 ID를 만들어 `id="1-ownership-and-documentation"`
가 된다. CSS 선택자는 숫자로 시작할 수 없으므로 `#1-...` 는 문법 오류다.
Lotus Docs의 `layouts/docs/baseof.html`은 본문에 `data-bs-spy="scroll"`을
걸어두기 때문에 Bootstrap ScrollSpy가 목차의 모든 링크에 대해
`querySelector()`를 호출하고, 여기서 던져진 예외가 같은 번들의 나머지
초기화(드롭다운, 사이드바 토글 등)를 통째로 중단시킨다.

**해결책**: Goldmark의 attribute block으로 앵커를 명시한다. `hugo.toml`에
이미 아래 설정이 있어야 한다 (`assets/site-template/hugo.toml.template`에 포함).

```toml
[markup.goldmark.parser.attribute]
  block = true
```

그러면 제목에 앵커를 직접 붙일 수 있다.

```markdown
## 1. Ownership and documentation {#ownership-and-documentation}
```

Hugo의 `.TableOfContents`도 이 attribute를 존중하므로 목차 링크와 제목
ID가 어긋나지 않는다. 화면에 보이는 번호는 그대로 유지된다.

번호 제목을 쓰지 않으면 애초에 발생하지 않는 문제지만, 체크리스트·절차서
같이 번호가 의미를 갖는 문서에서는 위 방식을 쓴다. 기존 콘텐츠를 일괄
변환해야 한다면 `scripts/fix_numbered_heading_anchors.py` 참고.

**확인 방법**: 빌드 후 아래가 아무것도 출력하지 않아야 한다.

```bash
grep -rhoE 'href="#[0-9][^"]*"' public --include='*.html' | sort -u
```

## 10. `params.social`은 전체 URL이 아니라 경로만 넣는다

**증상**: 상단 헤더의 GitHub(또는 트위터 등) 아이콘을 클릭하면 404가 뜬다.
주소창을 보면 `https://github.com/https://github.com/owner/repo` 처럼
접두사가 두 번 붙어 있다.

**원인**: 테마의 `layouts/partials/docs/top-header.html`이 링크를 이렇게
만든다.

```go-html-template
https://{{ . }}.com/{{ index site.Params.social . }}
```

즉 `https://github.com/` 를 테마가 직접 붙이므로, 값에는 그 뒤에 올
경로만 있어야 한다. 테마 exampleSite의 주석에 `# YOUR_GITHUB_ID or
YOUR_GITHUB_URL` 이라고 적혀 있지만 **URL 형식은 실제로 동작하지 않는다** —
주석이 잘못되어 있다.

```toml
# 틀림 — https://github.com/https://github.com/... 로 렌더링되어 404
[params.social]
  github = "https://github.com/owner/repo"

# 맞음
[params.social]
  github = "owner/repo"
```

같은 규칙이 `twitter`, `instagram` 등 다른 소셜 키에도 적용된다
(`rss = true` 와 `bluesky` 만 별도 분기로 처리된다).

**주의**: 같은 `hugo.toml` 안의 `params.docs.repoURL` 은 정반대로 **전체
URL**을 요구한다("이 페이지 편집" 링크에 쓰인다). 두 값의 형식이 다르다는
점이 이 실수를 유발한다.

**확인 방법**: 빌드 후 아래가 아무것도 출력하지 않아야 한다.

```bash
grep -rhoE 'href="https://[a-z]+\.com/https://[^"]*"' public --include='*.html' | sort -u
```
