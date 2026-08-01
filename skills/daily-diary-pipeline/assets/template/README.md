# {{SITE_TITLE}} ({{REPO_NAME}})

{{SITE_DESCRIPTION}}

사이트: {{BASE_URL}}

## 어떻게 동작하나

```
input/sentence.md (오늘의 항목들, 한 줄에 하나씩, GitHub 웹 UI에서 수정)
        │
        ▼  매일 {{CRON_KST_TIME}} KST (GitHub Actions cron)
pipeline/generate.py
  - 코드블록 안의 각 줄을 항목 하나로 읽음
  - 이미 게시된 적 있는 항목(해시 기준)은 건너뜀 — pipeline/state.json 으로 추적
  - 입력이 비어 있으면 FALLBACK_QUOTES 풀에서 그날 순서에 맞는 항목을 대신 사용
  - 새 항목마다 claude CLI로 콘텐츠 생성
  - content/posts/YYYY-MM-DD-....md 로 항목당 포스트 1개씩 저장
        │
        ▼  변경사항 커밋 & push
Hugo build → GitHub Pages 배포
```

## 매일 사용하는 방법

1. GitHub 저장소에서 [`input/sentence.md`](input/sentence.md) 파일을 연다.
2. 연필(✏️) 아이콘을 눌러 편집 모드로 들어간다. (블로그 상단 "{{INPUT_BUTTON_LABEL}}" 버튼으로 바로 이동 가능)
3. 코드블록(```) 안에 오늘 쓰고 싶은 내용을 한 줄에 하나씩 적는다. 여러 줄을 적으면 줄마다 포스트가 하나씩 생성된다.
4. 우측 상단 "Commit changes"로 저장한다. (로컬 git 작업 불필요)
5. 다음날 {{CRON_KST_TIME}}(KST)에 자동으로 새 항목들을 기준으로 포스트가 게시된다.

이미 게시에 사용된 항목은 파일에 그대로 남아있어도(같은 날이든 다른 날이든) 다시 게시되지 않는다.

즉시 확인하고 싶다면 GitHub 저장소 → Actions 탭 → "{{WORKFLOW_NAME}}" →
"Run workflow" 로 수동 실행할 수 있다.

### 입력을 깜빡했다면 — 명언 대체

코드블록을 완전히 비워두고 그날 실행이 돌면, `pipeline/generate.py`의
`FALLBACK_QUOTES` 풀에서 그날 날짜에 해당하는 항목을 대신 사용해 포스트를 생성한다.
풀을 완전히 비워두면(`FALLBACK_QUOTES = []`) 이 기능을 끌 수 있다 — 그 경우 입력이
없는 날은 그냥 포스트가 생성되지 않는다.

## 최초 설정 (1회만, 사람이 직접 해야 하는 단계)

자동 생성 단계는 Claude Code CLI를 사용한다. GitHub Actions에서 이 CLI를 인증하려면
Claude 구독 계정으로 발급한 OAuth 토큰을 저장소 Secret으로 등록해야 한다. 이 과정은
브라우저 로그인이 필요해 에이전트가 대신할 수 없다.

```bash
claude setup-token
```

터미널에 표시되는 인증 코드를 브라우저에 붙여넣고 로그인하면, **그 다음에** 터미널에
`sk-ant-oat01-...` 로 시작하는 토큰이 출력된다. (브라우저에 표시된 인증 코드 자체가
아니라, 붙여넣은 뒤 터미널에 최종 출력되는 토큰이어야 한다.)

```bash
gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo {{GITHUB_USER}}/{{REPO_NAME}}
# 위 토큰을 붙여넣기
```

등록 후 Actions 탭에서 워크플로를 한 번 수동 실행(`workflow_dispatch`)해 정상 동작을
확인한다.

## 저장소 구조

| 경로 | 역할 |
|---|---|
| `input/sentence.md` | 오늘의 항목들 — 한 줄에 하나씩 (사람이 매일 수정) |
| `pipeline/generate.py` | 항목별 콘텐츠 생성 → Hugo 포스트 작성. 도메인 설정은 파일 상단 "도메인 설정" 블록 |
| `pipeline/state.json` | 게시에 사용된 항목 해시 목록 (중복 게시 방지) |
| `content/posts/` | 생성된 포스트 |
| `.github/workflows/daily.yml` | 매일 {{CRON_KST_TIME}} KST 생성 + 배포 워크플로 |
| `themes/PaperMod` | Hugo 테마 (git submodule) |
| `assets/css/extended/cards.css` | 카드 그리드 레이아웃 + PaperMod 여백 버그 수정 (PaperMod 공식 커스텀 CSS 훅) |
| `static/CNAME` | (선택) 커스텀 도메인 사용 시 |

## 로컬에서 테스트

```bash
hugo server -D                      # http://localhost:1313/
python3 pipeline/generate.py --dry-run   # 파일 생성 없이 결과만 확인
```

로컬에는 `claude` CLI 로그인 세션이 있으면 그대로 사용되고(`JUDGE_BACKEND=claude-code`),
없으면 `ANTHROPIC_API_KEY` 를 설정해 `JUDGE_BACKEND=api` 로 실행할 수 있다.
