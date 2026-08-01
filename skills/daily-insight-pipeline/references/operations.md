# 운영 지식 — 검증된 함정과 해결책

이 템플릿은 jeonck/insight(기술 보안 인사이트)에서 실전 검증된 코드다.
아래 함정들은 이미 코드에 반영되어 있으므로 **수정하지 말 것**. 새 도메인 적용 시
참고용으로만 사용한다.

## 수집 소스 관련

| 함정 | 상태 |
|---|---|
| Reddit `.json` API가 클라우드 IP(GitHub Actions)에서 403 | 소스별 오류 격리로 처리됨 — 실패해도 다른 소스 정상 |
| hnrss.org 간헐적 502 | 해당 실행만 0건, 자동 회복 |
| GitHub Search `created:>N일`+스타 조건이 자주 0건 | 정상. 임계값은 `stars:>50`/14일 수준이 현실적 (>100/7일은 거의 항상 0건) |
| RSS URL 유효성 | **스캐폴딩 시 반드시 curl로 각 URL HTTP 200 확인** — 저명한 블로그도 피드가 없거나 이전된 경우 많음 (예: anthropic.com/rss.xml은 404) |

## 판정(Claude) 관련

- 백엔드 2종: `claude-code`(구독 인증, 기본) / `api`(ANTHROPIC_API_KEY 과금).
  CI에서는 `CLAUDE_CODE_OAUTH_TOKEN` Secret 존재 여부로 자동 선택됨.
- `claude setup-token`은 대화형 브라우저 인증이라 **사용자가 직접 실행**해야 한다.
  흔한 실수: 브라우저에 표시된 인증 코드를 Secret에 등록 → 401 Invalid bearer token.
  올바른 값은 코드를 터미널에 붙여넣은 **후** 출력되는 `sk-ant-oat01-...` 토큰.
- 크레딧 부족/401 등 복구 불가 오류는 첫 항목에서 fast-abort하고 exit 1
  → collect job 실패 표시 → GitHub 알림. 성공분은 커밋·배포됨.
- 판정 1건당 ~10초(claude-code 백엔드). MAX_ITEMS 기본 30 = 실행당 ~5분.

## Hugo 관련

- Hugo ≥0.146의 새 레이아웃 구조 사용 (layouts/ 바로 아래, `_default/` 아님).
- **빈 택소노미 항목은 페이지가 생성되지 않아 메뉴가 404가 된다** —
  `content/verdict/<라벨>/_index.md`, `content/status/<라벨>/_index.md` 스텁이 이를 방지.
  verdict 라벨을 변경하면 스텁 디렉토리도 반드시 함께 변경할 것.
- baseURL의 하위 경로(`/repo-name/`) 때문에 로컬 프리뷰는 `http://localhost:1313/<repo-name>/`.

## 워크플로 관련

- **GITHUB_TOKEN은 repo variable/secret 쓰기 불가** (403 Resource not accessible by
  integration, `permissions: actions: write`로도 안 됨). 워크플로에서 제어 가능한 상태는
  **repo에 커밋하는 마커 파일**로 저장할 것 — pause/resume이 `.collect-paused` 파일을
  쓰는 이유. gate job이 sparse-checkout으로 마커만 확인해 collect를 스킵한다.

- cron 실행: GitHub 러너에서 돌므로 사용자 PC 불필요.
- 봇 커밋(GITHUB_TOKEN 푸시)은 push 트리거를 재발화하지 않음(GitHub 재귀 방지) — 이중 실행 없음.
- push 트리거는 content/layouts/archetypes/hugo.toml 변경 시 배포만 수행(collect 스킵).
- `collect`는 `continue-on-error: true` + 마지막에 실패 표면화 — 판정 일부 성공 후
  치명 오류가 나도 성공분이 커밋·배포된다.
- **`git push` non-fast-forward 거부 — 이미 코드에 반영됨, 건드리지 말 것.**
  `collect.py`는 판정 건수만큼 수 분씩 걸리므로(항목당 ~10초), 그 사이 main이
  앞서나갈 수 있다(운영 루틴상 사람이 웹 UI에서 직접 정정 커밋, 다른 워크플로 실행과
  우연히 겹침 등). 실제로 jeonck/curasec에서 2주 무사고 운영 후 이 레이스로 push가
  거부되며 collect job이 실패한 사례 있음. `Commit new insights` 스텝은 push 거부 시
  `git fetch` + `git rebase origin/main` 후 최대 5회 재시도하도록 되어 있다 —
  실제 rebase 충돌(같은 파일 동시 수정)만 치명 오류로 표면화되고, 단순히 "원격이
  앞서나간" 흔한 경우는 자동 복구된다.

## verdict 라벨 변경 절차 (선택)

기본 라벨(즉시조치/백로그/학습/무관)은 행동 중심이라 대부분 도메인에 그대로 적용 가능.
변경이 꼭 필요하면 아래 위치를 **모두 일관되게** 치환:

1. `pipeline/collect.py` — `VERDICTS` 튜플, `JUDGE_PROMPT`의 라벨·판정 기준 설명
2. `layouts/baseof.html` — nav 링크 3곳, `.badge.<라벨>` CSS 클래스 3개
3. `layouts/home.html` — 섹션별 `where` 필터 값과 제목
4. `content/verdict/<라벨>/_index.md` — 스텁 디렉토리명·title
5. `README.md` — 판정 체계 표

"무관"(포스트 미생성)과 status(대기/완료)는 구조에 얽혀 있으므로 이름만 바꾸고 의미는 유지할 것.

## 스캐폴딩 후 검증 체크리스트

1. `python pipeline/collect.py --dry-run` (MAX_ITEMS=5) — 수집 건수·판정 품질 확인
2. `hugo --quiet` — 빌드 오류 없음
3. 배포 후: 홈 + verdict/status/tags 메뉴 URL 전부 HTTP 200
4. workflow 수동 실행 1회 — collect/deploy 모두 success, 포스트가 사이트에 표시
