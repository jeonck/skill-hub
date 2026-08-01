# 운영 지식 — 실전에서 발견된 함정과 해결책

이 템플릿은 jeonck/comparison(comparison.metacog.co.kr — IT 용어를 SVG 도식 +
표로 비교하는 사이트)의 실제 프로덕션 빌드·배포·버그 수정 과정에서 나온 코드다.
아래 함정들은 전부 실제로 한 번씩 실패를 겪고 나서 코드에 반영된 것이며
(가정이나 이론이 아님), 이미 템플릿에 반영되어 있으므로 **수정하지 말 것**. 새
도메인 적용 시 참고용으로만 사용한다.

## claude CLI 생성 타임아웃 — 240초는 부족하다

**증상**: 실제 프로덕션 워크플로 첫 실행에서 `generate_cli()`의 subprocess
타임아웃이 240초였는데, CI에서 두 번의 시도(attempt 1, attempt 2) 모두 정확히
240초에서 timeout으로 실패했다(`CLI timeout (attempt 1)` → `CLI timeout
(attempt 2)` → 생성 실패).

**원인**: SVG 도식 + 8행 표 + 여러 문단을 포함한 JSON 응답은 출력 토큰이 많다.
로컬에서 동일한 형태의 프롬프트를 직접 타이밍 측정한 결과 **약 192초**가
걸렸다 — 이것도 단순화된 프롬프트 기준이었다. "글자 수가 많지 않은데 오래
걸린다"는 착각이 들 수 있는데, 실제로는 도식(SVG 마크업)과 표를 포함한 전체
JSON 응답 자체의 출력 토큰량이 상당하기 때문이다. 모델을 상위 등급(Opus)으로
바꾼다고 빨라지지 않는다 — 오히려 Opus는 속도보다 깊이에 최적화되어 있어 더
느려질 수 있다. 최신 Sonnet 세대로 바꾸는 정도가 실질적으로 도움이 되는
선택이다.

**해결**: `generate_cli()`의 subprocess timeout을 **420초**로 설정했다(템플릿에
반영됨). 이 값을 다시 줄이려면 반드시 대상 CI 환경에서 재측정할 것. timeout
발생 시 부분 출력(stdout/stderr)도 로그에 남기도록 되어 있다 — 향후 디버깅에
도움이 된다.

## 워크플로 push `paths` 필터에 `pipeline/**`가 없다

**증상**: `pipeline/generate.py`를 수정해서 커밋·push했는데 워크플로가 전혀
트리거되지 않는다.

**원인**: `.github/workflows/deploy.yml`의 push 트리거 `paths`는
`input/**`, `content/**`, `hugo.toml`, `archetypes/**`, `assets/**`만
감시한다. 파이프라인 코드 변경은 이 필터 밖이다(트랜스크립트/다이어리 계열
스킬들과 동일한 설계 — CI가 매번 파이프라인 코드 자체를 재실행할 필요는
없다고 보기 때문).

**해결**: `pipeline/generate.py`나 `README.md`만 바꿔 push한 뒤 동작을
확인하려면 `gh workflow run <workflow-file> --repo <user>/<repo>`로 수동
트리거해야 한다. 코드 변경 후 실제 생성 결과를 검증하는 유일한 방법이다.

## 비교 표에 `white-space: nowrap`을 쓰면 안 된다

**증상**: 배포 후 사용자가 "표가 한 번에 안 보여서 좌우로 스크롤해야 한다"고
보고. 데스크톱 화면에서도 표를 보려면 가로 스크롤이 필요했다.

**원인**: 초기 버전의 `compare.css`가 `.post-content table th, td`에
`white-space: nowrap`을 적용했다. 표 셀에는 "Pointer decrement — O(1), no
bookkeeping"처럼 긴 문장이 들어가는데, `nowrap`이 이 문장을 한 줄로 강제하면서
행 전체 너비가 뷰포트를 훨씬 초과해 버렸다. `overflow-x: auto`가 걸려 있어도
근본 원인(각 셀이 줄바꿈되지 않음)은 해결되지 않는다.

**해결**: 템플릿의 `compare.css`는 `white-space: normal` +
`overflow-wrap: break-word` + `table-layout: fixed`(첫 번째 "Aspect" 열만
22% 너비 고정, 나머지 두 열이 남은 폭을 균등 분배)를 쓴다. 이렇게 하면
일반적인 데스크톱 폭에서는 가로 스크롤 없이 표가 한 화면에 들어간다. 실측
방법: 브라우저 JS 콘솔에서
`document.querySelector('.post-content table').scrollWidth <=
document.querySelector('.post-content table').clientWidth`가 `true`인지
확인. (매우 좁은 모바일 뷰포트(<400px)에서는 3열짜리 표 자체가 물리적으로
못 들어갈 수 있어 표 내부 스크롤이 남을 수 있다 — 이건 정상이며, 페이지
전체가 가로로 밀리는 것과는 다른 문제다.)

## SVG 도식에 하드코딩된 색상을 쓰면 안 된다 — 사이트 CSS 변수를 참조해야 한다

**증상**: 초기 버전은 매 포스트마다 Claude가 임의의 색상 팔레트(예: 어두운
네이비 배경에 파스텔 텍스트)를 즉흥적으로 만들어냈다. 결과: 밝은 라이트
모드 페이지 위에 어두운 상자가 붕 떠 있는 모습이 되어 사용자가 "도식을
디자인시스템을 좀 더 적용해서 가시성 있고 밝게 개선 가능할까?"라고 요청.
또한 포스트마다 색상 언어가 달라 사이트 전체의 시각적 일관성이 없었다.

**해결**: `generate.py`의 `SYSTEM_PROMPT`가 도식의 모든 fill/stroke를
`style="fill:var(--compare-a)"`처럼 **사이트 자체 CSS 커스텀 프로퍼티**로만
지정하도록 강제한다(하드코딩된 hex/rgb 금지). 사용 가능한 변수:

- `var(--primary)` — 굵은 제목/레이블
- `var(--content)` — 도식 본문 텍스트
- `var(--secondary)` — 흐린 주석/캡션 텍스트
- `var(--border)` — 중립적 구분선, 빈 슬롯 점선 박스
- `var(--compare-a)` / `var(--compare-a-soft)` — 왼쪽(첫 번째) 비교 대상 전용
  강조색/연한 배경색
- `var(--compare-b)` / `var(--compare-b-soft)` — 오른쪽(두 번째) 비교 대상
  전용 강조색/연한 배경색

이 변수들은 `assets/css/extended/compare.css`에 라이트/다크 모드 각각
정의되어 있다(PaperMod의 `theme-vars.css` 패턴을 그대로 따름:
`:root { ... }` / `:root[data-theme="dark"] { ... }`). 인라인 SVG는 문서
DOM에 직접 삽입되므로 이 CSS 커스텀 프로퍼티를 정상적으로 상속·참조할 수
있다 — 결과적으로 도식이 라이트/다크 테마 전환에 자동으로 대응하고, 모든
포스트가 동일한 두 가지 강조색(왼쪽=파랑 계열, 오른쪽=주황 계열) 언어를
공유하게 된다.

도식 자체의 배경은 투명하게 두고(`.compare-diagram` 래퍼 div가 이미
`var(--entry)` 배경 + `var(--border)` 테두리 + `var(--radius)`로 카드
모양을 제공함), 도식 내부에서 전체 배경을 채우는 `<rect>`를 그리지 않는다.

## 커스텀 도메인 연결 — DNS가 먼저다

`static/CNAME` 파일과 `gh api .../pages --method PUT --field cname=<domain>`
호출 전에 반드시 `dig +short <domain>`으로 CNAME이 `<user>.github.io.`를
가리키는지 확인한다. 순서가 바뀌면(도메인 API 호출 → 나중에 DNS 설정)
인증서 발급이 실패한다. 실제 이 세션에서는 사용자가 이미 DNS를 설정해둔
상태였고, `gh api` 호출 직후 인증서가 "approved" 상태가 되기까지 몇 분도
걸리지 않았다.

## `claude setup-token`은 에이전트가 대신할 수 없다

브라우저 로그인이 필요한 대화형 명령이므로 사용자가 직접 실행해야 한다.
등록해야 할 값은 브라우저에 뜨는 로그인 코드가 아니라, 그 코드를 붙여넣은
**이후** 터미널에 최종 출력되는 `sk-ant-oat01-...` 토큰이다. 이 세션에서는
사용자가 이 단계를 스스로 완료한 뒤 실제 온디맨드 파이프라인(`REST vs
GraphQL` 요청)이 CI에서 성공적으로 돌아가는 것까지 확인했다.

## 배포 후 다시 확인해야 할 체크리스트

1. `python pipeline/generate.py --dry-run` — 입력 있는 경우로 최소 1회
   (claude CLI 로그인 세션 사용)
2. `hugo --minify` — 빌드 오류 없음
3. `hugo server -D`로 브라우저 확인 — 카드 그리드, 도식 카드 배경, 표가
   가로 스크롤 없이 한 화면에 들어오는지, 라이트/다크 모드 토글 둘 다
4. 배포 후: 홈 + posts/tags/search 메뉴 URL 전부 HTTP 200
5. `input/term.md`에 실제 새 항목을 추가해 push한 뒤 워크플로가 자동으로
   트리거되고, 생성이 완료되고(수 분 소요될 수 있음), 배포까지 성공하는지
   실제 CI에서 1회 이상 검증
