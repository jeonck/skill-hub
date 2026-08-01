---
name: daily-diary-pipeline
description: 매일 GitHub에서 한 줄(또는 여러 줄) 입력을 받아 Claude로 콘텐츠를 생성하고 Hugo + GitHub Pages 블로그에 자동 게시하는 파이프라인을 스캐폴딩하는 스킬. 사용자가 GitHub 웹 UI에서 input/sentence.md 파일을 수정해두면, 매일 정해진 시각에 크론이 돌아 그 항목을 기준으로 포스트를 생성한다. 입력이 비어 있으면 명언 풀에서 대체 항목을 사용한다. "매일 영어 문장 넣으면 일기 써주는 사이트처럼 다른 주제로 만들어줘", "한 줄 입력하면 자동으로 블로그 글 써주는 파이프라인 만들어줘", "writing-diary 프로젝트 구조로 다른 주제 사이트 만들어줘" 같은 요청에 사용한다.
---

# Daily Diary Pipeline Builder

매일 사람이 GitHub에서 짧은 입력(문장/주제/글감 등)을 남겨두면 다음 파이프라인이 돈다:

GitHub 웹 UI로 `input/sentence.md` 수정 → 매일 정해진 시각 GitHub Actions 크론 →
`pipeline/generate.py`가 Claude로 콘텐츠 생성(입력이 비면 명언 풀로 대체) → Hugo 포스트
커밋 → GitHub Pages 배포.

`assets/template/`의 코드는 [jeonck/writing-diary](https://github.com/jeonck/writing-diary)
(매일 영어 문장 → 일기 + 응용문장 자동 게시)에서 실전 검증된 코드다. **로직을 새로
작성하지 말고 템플릿을 복사한 뒤 도메인 파라미터만 교체**한다. 알려진 함정은
[references/operations.md](references/operations.md)를 읽는다.

## daily-insight-pipeline 스킬과의 차이

이름이 비슷한 `daily-insight-pipeline` 스킬은 RSS/Reddit/HN/GitHub 등 **외부 소스를
자동 수집**해 Claude가 행동을 판정(즉시조치/백로그/학습/무관)하는 파이프라인이다.
이 스킬(`daily-diary-pipeline`)은 반대로 **사람이 매일 직접 입력**한 짧은 텍스트
하나를 Claude가 콘텐츠로 확장(일기, 해설, 감상 등)하는 파이프라인이다. "정보를
모아서 판단"이 아니라 "짧은 입력을 긴 콘텐츠로 부풀리는" 쪽이면 이 스킬을 쓴다.

## 1단계 — 인터뷰

다음을 파악한다 (한 번에 몰아 묻지 말 것):

1. **주제/목적**: 매일 어떤 종류의 짧은 입력을 받아 무엇으로 확장하고 싶은가
   (예: 영어 문장 → 일기 + 응용문장, 감사한 일 한 줄 → 감사일기, 오늘 배운 개념 →
   해설글 + 퀴즈, 기분 한 단어 → 감정일기 등)
2. **생성 결과물 구조**: 본문 하나만 있으면 되는지, 번역/해석이 필요한지, "응용 예시"
   같은 변형 목록이 필요한지 — 이게 `pipeline/generate.py`의 JSON 스키마와
   `write_post()`의 섹션 구성을 결정한다
3. **입력이 없는 날의 폴백**: 명언/격언 풀을 쓸지, 아니면 그냥 그날은 포스트를
   건너뛸지(FALLBACK_QUOTES를 빈 리스트로 둠). 명언 풀을 쓴다면 어떤 결의 명언/문구가
   어울리는지(예: 스토아 철학, 문학 구절, 업계 격언 등)
4. **repo 이름, 사이트 제목, 크론 시각**(기본 KST 07:00 권장), **커스텀 도메인 여부**

## 2단계 — 스캐폴딩

1. 대상 디렉토리에 `assets/template/` 전체를 복사 (`.claude/launch.json`,
   `content/posts/.gitkeep`, `pipeline/state.json` 포함)
2. Hugo PaperMod 테마를 git submodule로 추가 (템플릿에는 포함되어 있지 않음):
   ```bash
   hugo new site . --force   # hugo.toml은 아래에서 템플릿 것으로 덮어씀
   git init -b main
   git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
   ```
   PaperMod 설치/배포의 일반 함정(TOML 키 순서, socialIcons 문법 등)은
   `hugo-blog-builder` 스킬을 참고한다. 이 스킬은 PaperMod 위에 얹는 diary
   파이프라인 레이어만 담당한다.
3. **`{{TOKEN}}` 형태 placeholder 치환** — 아래 파일들에서 grep으로 전부 찾아 교체한다:
   `hugo.toml`, `README.md`, `input/sentence.md`, `.github/workflows/daily.yml`,
   `.claude/launch.json`.
   ```bash
   grep -rn '{{[A-Z_]*}}' hugo.toml README.md input/sentence.md \
     .github/workflows/daily.yml .claude/launch.json
   ```
   주요 토큰: `BASE_URL`, `SITE_TITLE`, `SITE_DESCRIPTION`, `GITHUB_USER`, `REPO_NAME`,
   `HOME_TITLE`, `HOME_DESCRIPTION`, `INPUT_BUTTON_LABEL`(예: "오늘의 문장 입력 ✏️"),
   `ITEM_LABEL`(입력 단위를 가리키는 명사, 예: "문장"/"주제"/"글감"), `EXAMPLE_ITEM`,
   `CRON_KST_TIME`, `CRON_UTC`(KST 시각 - 9시간 = UTC cron 표현식), `CRON_COMMENT`,
   `WORKFLOW_NAME`, `HUGO_VERSION`(로컬 `hugo version` 출력과 맞춤),
   `FALLBACK_DESCRIPTION`(예: "스토아 철학자들의"), `INPUT_INSTRUCTIONS_LINE1`.
4. **`pipeline/generate.py` 도메인 설정 블록을 직접 다시 쓴다** — 이건 placeholder
   치환이 아니라 코드 수정이다. 파일 상단 `=== 도메인 설정 ===` ~ `=== 도메인 설정
   끝 ===` 사이의 다음 상수들을 인터뷰 내용에 맞게 교체한다:
   - `FALLBACK_QUOTES`: `{"text": ..., "author": ...}` 목록. 폴백을 안 쓰면 `[]`
   - `SYSTEM_PROMPT`: Claude에게 부여할 역할/톤
   - `GENERATE_PROMPT`: `{sentence}`와 `{note}` 두 자리는 반드시 단일 중괄호로 유지.
     JSON 스키마 부분(`{{"title_ko": ...}}`)은 Python `str.format()`이 리터럴
     `{`/`}`를 출력하도록 이중 중괄호를 유지해야 한다 — 필드를 늘리거나 줄일 때도
     이 이스케이프 규칙을 그대로 따른다. 스키마를 바꾸면 `parse_result()`의
     `required` 튜플과 `write_post()`도 함께 맞춘다
   - `QUOTE_NOTE`: 폴백 명언을 쓸 때 프롬프트에 덧붙는 지시문
   - `HEADING_INPUT` / `HEADING_INPUT_QUOTE` / `HEADING_BODY` / `HEADING_VARIATIONS`:
     포스트 본문 섹션 제목
   - 그 아래 엔진 코드(해시 dedup, `claude-code`/`api` 백엔드 전환, Hugo 포스트
     작성 골격)는 실전 검증된 로직이므로 수정하지 않는다
5. `assets/css/extended/cards.css`는 그대로 둔다 — PaperMod의 홈 인트로 여백 버그
   수정과 카드 그리드 레이아웃이 이미 포함되어 있다(자세한 원인은 operations.md)

## 3단계 — 로컬 검증

```bash
python3 pipeline/generate.py --dry-run   # claude CLI 로그인 세션 사용, 파일 생성 없음
hugo --minify
hugo server -D    # 브라우저로 카드 그리드/여백이 의도대로 보이는지 직접 확인
```

dry-run 결과(본문/번역/변형 예시)를 사용자에게 보여주고 톤과 품질을 확인한다.
어긋나면 `SYSTEM_PROMPT`/`GENERATE_PROMPT`를 보강해 재실행한다. 입력을 비운 채로도
한 번 dry-run 해서 폴백 명언 경로가 정상 동작하는지 확인한다.

## 4단계 — 배포

1. `git add -A` → 커밋 → `gh repo create <name> --public --source . --push`
   (기존 repo면 remote add 후 push)
2. Pages 활성화: `gh api repos/<user>/<repo>/pages --method POST --field build_type=workflow`
3. (선택) 커스텀 도메인: 사용자가 DNS CNAME을 미리 설정해뒀는지 확인(`dig +short
   <domain>`) → `static/CNAME` 생성 → `hugo.toml`의 `baseURL`을 도메인으로 변경 →
   `gh api repos/<user>/<repo>/pages --method PUT --field cname=<domain>` →
   인증서 발급 대기 후 `--field https_enforced=true`
4. **사용자 안내 (에이전트가 대신 못 하는 부분)**: `claude setup-token` 실행 →
   최종 출력되는 `sk-ant-oat01-...` 토큰(브라우저의 인증 코드 아님!)을
   `gh secret set CLAUDE_CODE_OAUTH_TOKEN` 으로 등록하도록 안내
5. Secret 등록 확인 후: `gh workflow run daily.yml` → run 완료 대기 →
   사이트 홈/포스트/태그/검색 URL 전부 HTTP 200 확인. 빈 입력으로 한 번 더
   `workflow_dispatch`를 돌려 폴백 명언 경로도 실제 CI에서 검증하면 더 확실하다

## 완료 기준

- 워크플로 generate/deploy 모두 success이고 실제 생성 포스트가 사이트에 표시됨
- 입력이 있는 경우와 없는 경우(폴백) 둘 다 최소 한 번씩 실제 배포로 검증됨
- 홈 화면에서 카드 그리드가 정상 렌더링되고 인트로 아래 여백 버그가 없음
- README에 도메인에 맞는 운영 루틴과 `claude setup-token` 안내가 반영됨
