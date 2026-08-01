# 운영 지식 — 검증된 함정과 해결책

이 템플릿은 [jeonck/talktime](https://github.com/jeonck/talktime)
(talktime.metacog.co.kr, 스크립트 → 학습 포스트 자동 게시)에서 실전 검증된 코드다.
아래 함정들은 이미 코드에 반영되어 있으므로 **수정하지 말 것**. 새 사이트 적용 시
참고용으로만 사용한다.

## 입력 파싱 — 통짜 스크립트 (daily-diary-pipeline과 다른 점)

`read_sentences()`는 한 줄=한 항목이 아니라 **코드블록 전체를 항목 1개**로 읽는다
(`---`만 있는 줄로 구분하면 여러 항목). 줄 단위 파싱으로 되돌리면 수만 자 스크립트가
줄 수만큼 포스트로 폭발한다. dedup 해시도 스크립트 전문 기준이므로, 공백 하나만 달라도
새 항목으로 처리된다 — 사용자에게 "처리 끝난 스크립트는 지워도 되고 놔둬도 된다"고
안내한다.

긴 입력 대응으로 api 백엔드 `max_tokens=8000`, CLI `timeout=360`으로 상향되어 있다
(기본 1024/180이면 긴 스크립트에서 잘리거나 타임아웃).

## push 후킹 — generate 잡에 push 가드가 없어야 한다

`daily.yml`의 push 트리거 paths에 `input/**`이 포함되고, generate 잡에
`if: github.event_name != 'push'` 가드가 **없다**. 이 두 가지가 "저장 즉시 처리"
후킹의 핵심이다 — daily-diary-pipeline 템플릿을 참고해 가드를 되살리면 후킹이 죽는다.
CSS/콘텐츠만 바뀐 push에서도 generate가 돌지만, 처리 완료 항목은 해시 dedup으로 즉시
스킵되므로 Claude 호출 비용이 없다. 봇 커밋(GITHUB_TOKEN push)은 워크플로를 재발화하지
않아(GitHub 재귀 방지) 무한 루프 걱정도 없다.

## 게시 후 입력 자동 초기화

`generate.py`의 `clear_input()`은 **전부 성공했을 때만**(`new_count and not failed and
not fatal_error`) `input/script.md`의 코드블록을 비우고 안내 주석은 남긴다. 일부
실패가 섞이면 재시도할 수 있도록 입력을 그대로 둔다 — 이 조건을 `new_count`만으로
느슨하게 바꾸면 실패분의 원문이 사라져 재시도가 불가능해진다. 워크플로의 commit
스텝에서 `git add`에 `input/script.md`를 반드시 포함해야 초기화가 커밋에 실린다.
봇 커밋은 push 트리거를 재발화하지 않으므로(GitHub 재귀 방지) 무한 루프 걱정 없음 —
실제로 talktime에서 이 경로로 검증됨.

## 후킹 전용 모드 (크론 끄기)

사용자가 "스크립트를 입력할 때만 돌게 해달라"고 하면(원조 talktime이 2026-07-21에
이 모드로 전환됨): ① `daily.yml`의 `schedule:` 블록 제거, ② `FALLBACK_QUOTES = []`,
③ README/input 안내에서 크론·폴백 문구 제거. 빈 입력 실행은 "건너뜁니다" 로그와
exit 0으로 끝난다. 크론을 그대로 두고 풀만 비우면 매일 빈 실행이 낭비되므로 반드시
둘 다 제거한다. 인터뷰 단계에서 "입력 없는 날 자동 게시(크론+폴백)를 원하는지"를
미리 물어보는 편이 좋다.

## 프롬프트 산출물 규칙 (품질 이슈를 겪고 보강된 것들)

- **퀴즈**: 빈칸(`____`) 문장 + 선택지는 그 수업의 idioms/vocabulary 항목에서만.
  이 제약이 없으면 오답이 너무 확연히 달라 정답이 티가 난다. "정답 삽입 시 문법적으로
  완전해야 한다" 규칙도 있다(없으면 수일치 오류 문장이 나온 사례 있음).
- **일기**: 하나의 사건을 다룬 4~6문장 이야기 + 학습 표현 2~4개를 `**굵게**`.
  "이디엄마다 한 문장씩" 방식은 이질감이 커서 폐기된 형태다.
- `parse_result()`는 diary가 옛 형식(배열)으로 와도 이어붙여 처리한다 — 방어 코드
  제거 금지.

## 스키마 3종 세트 동기화

GENERATE_PROMPT의 JSON 스키마, `parse_result()`의 검증/정규화, `write_post()`의 렌더링은
항상 함께 수정한다. 하나만 바꾸면 `JSON 파싱 실패` 로그와 함께 생성이 실패한다.
GENERATE_PROMPT는 런타임에 `str.format(sentence=..., note=...)`로 채워지므로 JSON
리터럴의 `{{` `}}` 이중 중괄호 이스케이프를 유지해야 한다 — `{sentence}`/`{note}`만
단일 중괄호.

## 게시된 포스트 재생성 절차

프롬프트/형식을 바꿔 기존 포스트를 다시 만들려면:

1. `content/posts/`에서 해당 포스트 파일 삭제
2. `pipeline/state.json`의 `processed`에서 해당 해시 제거
   (스크립트 항목: 전문 해시 / 폴백 항목: `날짜::텍스트` 해시)
3. 스크립트 포스트면 `input/script.md`에 원문 복원 후 `python3 pipeline/generate.py`
   실행, 폴백 포스트면 입력을 비운 채 실행 (같은 날짜면 같은 이디엄 선택됨)
4. 처리 후 입력을 다시 비우고 커밋 — 같은 slug면 URL이 유지된다

## 입력 dedup vs 폴백 dedup — 설계가 다른 이유

- **사용자 스크립트**: `sentence_hash(text)` — 텍스트가 키. 한 번 게시된 스크립트는
  파일에 남아 있어도 영구히 재게시되지 않는다.
- **폴백 이디엄**: `sentence_hash(f"{date}::{text}")` — 날짜 포함. 풀이 순환해 같은
  이디엄이 다시 와도 새 포스트로 게시된다. 통일하면 풀 한 바퀴 후 조용히 게시가
  끊기는 구멍이 생기므로 반드시 이 구분을 유지한다.

## 레이아웃 — align-content: start 필수

PaperMod의 `.main`은 `min-height: calc(100vh - header - footer)`를 가진다.
카드 그리드(`display: grid`)로 바꾸면 남는 세로 공간이 각 행에 분배(stretch)되어
인트로 박스와 첫 카드 사이가 수십 px 벌어져 보인다 — `.first-entry`의
min-height/margin 수정만으로는 해결되지 않는 별개의 여백이다. `body.list .main`에
`align-content: start`가 반드시 있어야 한다(템플릿 cards.css에 반영됨).
실측 방법: 인트로 bottom과 카드 top의 차이가 grid `gap`(1.5rem=24px)과 같으면 정상.
`.first-entry { min-height: unset; margin-bottom: 0; }`(PaperMod의 320px 강제 버그
수정)도 cards.css에 포함되어 있다. 테마 파일은 직접 수정하지 않는다 —
`assets/css/extended/*.css`가 PaperMod 공식 오버라이드 훅이다.

## 퀴즈 토글 렌더링

포스트의 `<details><summary>` 아코디언은 goldmark raw HTML이므로 `hugo.toml`의
`[markup.goldmark.renderer] unsafe = true`가 필수다. 지우면 토글이 통째로 사라진다.
토글 내부 텍스트는 `write_post()`에서 html_escape 처리된다. 스타일은
`assets/css/extended/quiz.css`.

## 커스텀 도메인

1. **`*.github.io` 하위 도메인은 커스텀 도메인이 될 수 없다** — GitHub API가
   "You cannot use custom domains ending with github.io..." 400으로 거부한다.
   사용자가 "talktime.jeonck.github.io로 DNS 해뒀다"처럼 말하면, 실제로는 자기 소유
   도메인에 CNAME을 걸어둔 경우가 많다. `dig +short <후보 도메인> CNAME`으로
   `<user>.github.io.`가 나오는 소유 도메인을 찾아 확인받는다.
2. 순서: DNS CNAME 확인 → `static/CNAME` 생성 + `hugo.toml` baseURL 변경(서브패스
   제거) → `gh api repos/<u>/<r>/pages --method PUT --field cname=<domain>` →
   `https_certificate.state`가 `approved`되면 `--field https_enforced=true`
3. 워크플로는 `actions/configure-pages`가 Pages 설정에서 base_url을 동적으로 가져오므로
   도메인 변경 후 워크플로 파일 수정은 불필요. `hugo.toml` baseURL은 로컬 미리보기와
   메타 태그용.
4. baseURL이 루트 도메인이 되면 로컬 미리보기는 `http://localhost:1313/`
   (서브패스 시절 `/repo/` 경로 아님). **미리보기 서버가 이미 떠 있었다면 재시작** —
   config 변경을 감지해도 서빙 경로가 갱신되지 않아 404가 나는 사례 있음.

## 판정(Claude) 관련

- 백엔드 2종: `claude-code`(구독 인증, 기본) / `api`(`ANTHROPIC_API_KEY` 과금).
  CI에서는 `CLAUDE_CODE_OAUTH_TOKEN` Secret 존재 여부로 자동 선택된다.
- `claude setup-token`은 대화형 브라우저 인증이라 **사용자가 직접 실행**해야 한다.
  흔한 실수: 브라우저에 표시된 인증 코드를 Secret에 등록 → 401 Invalid bearer token.
  올바른 값은 코드를 터미널에 붙여넣은 **후** 출력되는 `sk-ant-oat01-...` 토큰.
- Secret 등록 전에는 push마다 generate 잡이 실패 표시되지만 deploy는 정상 배포된다
  (`Surface generation failure` 단계가 실패를 드러내되 커밋된 콘텐츠는 배포됨).
- 크레딧 부족/401 등 복구 불가 오류는 fast-abort하고 exit 1 → GitHub 알림.

## CI가 커밋을 push한다 → 로컬이 뒤처지기 쉽다

generate 잡이 매일/후킹 시 새 포스트를 커밋·push한다. 로컬에서 코드를 고치고
push하기 전에 항상 `git fetch origin && git pull --rebase origin main`.

## Placeholder 치환 시 셸 이스케이프 함정

`{{TOKEN}}` 치환을 shell `sed -i` 반복문으로 하면 `CRON_UTC`처럼 `*`가 들어간 값에서
조용히 실패하기 쉽다. Python 딕셔너리 치환을 쓴다:

```python
from pathlib import Path
repl = {"BASE_URL": "...", "CRON_UTC": "0 22 * * *", ...}
for fname in ["hugo.toml", "README.md", "input/script.md",
              ".github/workflows/daily.yml", ".claude/launch.json"]:
    p = Path(fname)
    text = p.read_text()
    for k, v in repl.items():
        text = text.replace("{{" + k + "}}", v)
    p.write_text(text)
```

치환 후 `grep -rn '{{[A-Z_]*}}' .`로 남은 토큰이 없는지 반드시 확인한다.

## 스캐폴딩 후 검증 체크리스트

1. `python3 pipeline/generate.py --dry-run` — 스크립트 입력 / 빈 입력(폴백) 둘 다.
   폴백 테스트는 `pipeline/state.json`을 잠시 치우거나 코드블록을 비워서 수행
2. dry-run 산출물 확인: 빈칸 퀴즈 + 학습 단어 선택지, 단일 사건 일기
3. `hugo --minify` 빌드 오류 없음 → `hugo server -D` 브라우저 확인
   (카드 그리드, 인트로↔카드 24px, 퀴즈 토글, 모바일 1열)
4. 배포 후: 홈 + posts/tags/search + 포스트 URL 전부 HTTP 200
5. input/script.md 커밋만으로 워크플로가 트리거되어 포스트가 게시되는지(후킹) 확인
