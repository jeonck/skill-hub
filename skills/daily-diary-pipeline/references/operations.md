# 운영 지식 — 검증된 함정과 해결책

이 템플릿은 [jeonck/writing-diary](https://github.com/jeonck/writing-diary)(매일 영어
문장 → 일기 + 응용문장 자동 게시, 이후 커스텀 도메인/카드 그리드까지 적용)에서 실전
검증된 코드다. 아래 함정들은 이미 코드에 반영되어 있으므로 **수정하지 말 것**. 새
도메인 적용 시 참고용으로만 사용한다.

## PaperMod 홈 인트로 여백 버그

**증상**: 홈 화면에서 소셜 아이콘(홈 인트로 박스) 아래와 첫 포스트 카드 사이에
불필요하게 넓은 빈 공간이 생김.

**원인**: `themes/PaperMod/assets/css/common/post-entry.css`의 `.first-entry`
규칙이 콘텐츠 실제 높이와 무관하게 여백을 강제한다.

```css
.first-entry {
    min-height: 320px;                            /* 콘텐츠와 무관하게 최소 320px 강제 */
    margin: var(--gap) 0 calc(var(--gap) * 2) 0;   /* 하단 마진이 gap의 2배 */
}
```

**해결**: 테마 파일을 직접 고치지 말고 `assets/css/extended/cards.css`(PaperMod가
공식 지원하는 `assets/css/extended/*.css` 오버라이드 훅, 테마 CSS 뒤에 자동
concat됨)에서 덮어쓴다. 템플릿에 이미 포함되어 있다:

```css
.first-entry { min-height: unset; margin-bottom: 0; }
```

## 카드 그리드 레이아웃 — align-content: start 필수

PaperMod의 `.main`은 `min-height: calc(100vh - header - footer)`를 가진다.
`display: grid`로 바꾸면 이 남는 세로 공간이 각 행에 분배(stretch)되어 인트로 박스와
첫 카드 행 사이가 수십 px 벌어져 보인다 — `.first-entry`의 min-height/margin 수정만으로는
해결되지 않는 별개의 여백이다. `body.list .main`에 `align-content: start`를 넣어 행을
위쪽에 밀착시켜야 한다(템플릿 cards.css에 반영됨). 실측 방법: 인트로 bottom과 카드 top의
차이가 grid `gap` 값(1.5rem=24px)과 같으면 정상.

## 카드 그리드 레이아웃

PaperMod는 `.post-entry`를 카드처럼 스타일링하지만(둥근 모서리, 배경, hover) 기본은
세로 1열 스택이다. `assets/css/extended/cards.css`에 `body.list .main`을
`display: grid`로 바꾸는 미디어쿼리(`min-width: 768px`)가 포함되어 있다. 목록 페이지
바깥의 다른 요소(`.page-header`, `.post-content`, `.first-entry`, `.page-footer`)는
`grid-column: 1 / -1`로 전체 폭을 유지시켜야 인트로 박스와 페이지네이션이 카드
사이에 끼지 않는다. 모바일(`<768px`)은 미디어쿼리 밖이라 자동으로 1열 유지.

## pipeline/generate.py — GENERATE_PROMPT 중괄호 이스케이프

`GENERATE_PROMPT`는 런타임에 `str.format(sentence=..., note=...)`로 채워진다. JSON
스키마 리터럴(`{"title_ko": ...}`)은 이중 중괄호 `{{ }}`로 이스케이프해야 `.format()`이
문자 그대로의 `{`/`}`를 출력한다. `{sentence}`와 `{note}` 두 자리만 단일 중괄호로
남긴다. 스키마 필드를 추가/삭제하면 `parse_result()`의 `required` 튜플과
`write_post()`의 렌더링 로직도 함께 맞춰야 한다 — 셋 중 하나만 바꾸면 파싱 실패
(`JSON 파싱 실패` 로그)로 이어진다.

## 입력 dedup vs 폴백 명언 dedup — 설계가 다른 이유

- **사용자가 직접 쓴 항목**: `sentence_hash(text)` — 텍스트 자체가 키. 한 번 게시된
  문장은 파일에 그대로 남아있어도 **영구히** 다시 게시되지 않는다.
- **폴백 명언**: `sentence_hash(f"{date}::{text}")` — 날짜가 키에 포함된다. 같은
  명언이 몇 주 뒤 순환으로 다시 나와도 새 포스트로 게시된다.

두 방식을 통일해서 명언도 영구 dedup으로 만들면, 명언 풀을 한 바퀴 다 돌고 나면
그 이후로는 그 날짜에 아무 것도 게시되지 않는 조용한 구멍이 생긴다. 반드시 이
구분을 유지한다.

## 워크플로 관련

- **push 트리거의 `paths` 필터**: `content/**`, `hugo.toml`, `archetypes/**`,
  `assets/**`만 감시한다. `pipeline/generate.py`나 `README.md`처럼 필터 밖 파일만
  바꿔 push하면 자동 배포가 트리거되지 않는다 — `gh workflow run daily.yml`로
  수동 배포해야 한다. CSS만 바꿨을 때 특히 잊기 쉽다(`assets/**`를 필터에 넣어둔
  것도 이 때문).
- **CI가 커밋을 push한다 → 로컬이 뒤처지기 쉽다**: `generate` job이 매일 새 포스트를
  커밋·push한다. 로컬에서 코드를 고치고 `git push`하면 non-fast-forward로 거절되는
  일이 흔하다. push 전에 항상 `git fetch origin && git log --oneline origin/main -3`
  로 확인하고, 필요하면 `git pull --rebase origin main` 후 다시 push한다.
- 봇 커밋(`GITHUB_TOKEN`/기본 `git push`)은 push 트리거를 재발화하지 않는다(GitHub
  재귀 방지) — 이중 실행 걱정 없음.
- `generate`는 `continue-on-error: true` + 마지막에 실패 표면화 — 일부 항목 성공 후
  치명 오류(크레딧 소진 등)가 나도 성공분은 커밋·배포된다.

## 판정(Claude) 관련

- 백엔드 2종: `claude-code`(구독 인증, 기본) / `api`(`ANTHROPIC_API_KEY` 과금).
  CI에서는 `CLAUDE_CODE_OAUTH_TOKEN` Secret 존재 여부로 자동 선택된다.
- `claude setup-token`은 대화형 브라우저 인증이라 **사용자가 직접 실행**해야 한다.
  흔한 실수: 브라우저에 표시된 인증 코드를 Secret에 등록 → 401 Invalid bearer token.
  올바른 값은 코드를 터미널에 붙여넣은 **후** 출력되는 `sk-ant-oat01-...` 토큰.
- 크레딧 부족/401 등 복구 불가 오류는 첫 항목에서 fast-abort하고 exit 1 →
  generate job 실패 표시 → GitHub 알림. 성공분은 커밋·배포됨.

## 커스텀 도메인 연결

1. 사용자가 DNS에 CNAME(`서브도메인 → <user>.github.io`)을 먼저 설정해야 한다.
   `dig +short <domain>`으로 `<user>.github.io.`가 나오는지 확인 후 진행 — 반대
   순서로 진행하면 인증서 발급이 실패한다.
2. `static/CNAME` 파일에 도메인을 한 줄로 적는다(Hugo가 빌드 시 `public/CNAME`으로
   복사). `hugo.toml`의 `baseURL`을 새 도메인으로 바꾼다(서브패스 제거).
3. `gh api repos/<user>/<repo>/pages --method PUT --field cname=<domain>`
4. `gh api repos/<user>/<repo>/pages`로 `https_certificate.state`가 `"approved"`가
   될 때까지 확인(보통 몇 분 내). 승인되면
   `gh api repos/<user>/<repo>/pages --method PUT --field https_enforced=true`
5. HTTP→HTTPS 강제 리다이렉트는 GitHub Pages CDN 전파에 몇 분 걸릴 수 있다 —
   즉시 200/301이 안 나와도 재확인하면 된다.
6. GitHub Actions 워크플로는 `--baseURL "${{ steps.pages.outputs.base_url }}/"`로
   빌드하므로(`actions/configure-pages`가 Pages 설정에서 동적으로 가져옴) 커스텀
   도메인 연결 후 워크플로 파일을 따로 고칠 필요는 없다. `hugo.toml`의 baseURL은
   로컬 빌드/미리보기와 메타 태그(og:url 등)를 위해서만 맞추면 된다.

## Placeholder 치환 시 셸 이스케이프 함정

`{{TOKEN}}` 치환을 shell `sed -i` 반복문으로 하면 `CRON_UTC`처럼 `*`가 들어간 값이나
여러 `-e`를 체이닝할 때 조용히 실패하기 쉽다(에러 없이 일부 파일만 치환되지 않고
넘어감). Edit 도구로 파일별로 직접 치환하거나, 아래처럼 Python 딕셔너리 치환을
쓰는 편이 안전하다:

```python
from pathlib import Path
repl = {"BASE_URL": "...", "CRON_UTC": "0 22 * * *", ...}
for fname in ["hugo.toml", "README.md", "input/sentence.md",
              ".github/workflows/daily.yml", ".claude/launch.json"]:
    p = Path(fname)
    text = p.read_text()
    for k, v in repl.items():
        text = text.replace("{{" + k + "}}", v)
    p.write_text(text)
```

치환 후 `grep -rn '{{[A-Z_]*}}' .`로 남은 토큰이 없는지 반드시 확인한다.

## 로컬 미리보기

- `hugo server -D` 실행 후 `baseURL`에 서브패스가 없으면(커스텀 도메인/루트 배포)
  `http://localhost:1313/`, 서브패스가 있으면(`https://user.github.io/repo/` 형태)
  `http://localhost:1313/<repo>/`로 접속해야 한다 — 루트로 접속하면 CSS/링크가
  깨진 것처럼 보일 수 있다(실제로는 baseURL 문제).

## 스캐폴딩 후 검증 체크리스트

1. `python pipeline/generate.py --dry-run` — 입력 있는 경우 / 빈 경우(폴백) 둘 다
2. `hugo --minify` — 빌드 오류 없음
3. `hugo server -D`로 브라우저 확인 — 카드 그리드, 인트로 여백, 모바일 1열 폴백
4. 배포 후: 홈 + posts/tags/search 메뉴 URL 전부 HTTP 200
5. workflow 수동 실행 1회(입력 있음) + 1회(입력 비움) — 둘 다 generate/deploy
   success, 실제 포스트가 사이트에 표시
