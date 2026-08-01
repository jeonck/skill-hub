---
name: term-comparison-pipeline
description: 짧은 용어/주제를 입력하면 SVG 도식 + 비교 표로 구성된 비교 포스트를 자동 생성해 Hugo + GitHub Pages 사이트에 게시하는, 온디맨드(예약 실행 없음) 파이프라인을 스캐폴딩하는 스킬. 사용자가 GitHub 웹 UI에서 input/term.md에 "REST vs GraphQL"처럼 한 줄을 추가하고 커밋하면, 그 push가 즉시 GitHub Actions를 트리거해 Claude가 도식+표+설명을 생성하고 배포한다. 크론이나 폴백 콘텐츠는 없다. "IT 용어 비교 사이트 만들어줘", "단어 입력하면 SVG 도식이랑 표로 비교해주는 사이트", "comparison.metacog.co.kr 같은 사이트를 다른 주제로", "온디맨드 용어 비교 파이프라인" 같은 요청에 사용한다.
---

# Term Comparison Pipeline Builder

**단어/주제를 GitHub에서 입력하면(온디맨드, 예약 실행 없음)**, 그 커밋이 push
후킹을 트리거해 Claude가 SVG 도식 + 비교 표 + 설명으로 구성된 구조화 비교
포스트를 자동 생성·게시하는 사이트를 스캐폴딩한다:

```
input/term.md (예: "REST vs GraphQL" 한 줄 추가, GitHub 웹 UI에서 수정)
        │
        ▼  커밋(push) 즉시 워크플로 트리거 — 예약 실행 없음
pipeline/generate.py — Claude가 분석해 JSON으로 반환:
  title / summary / diagram_svg(사이트 CSS 변수 참조) /
  table_headers+table_rows / key_differences / when_to_use_left+right / tags
        │
        ▼  Hugo 포스트로 렌더링(도식은 .compare-diagram 카드로 감쌈) → 커밋 & push
Hugo build → GitHub Pages 배포
```

`assets/template/`의 코드는 [jeonck/comparison](https://github.com/jeonck/comparison)
(comparison.metacog.co.kr — IT 용어를 SVG 도식과 표로 비교하는 사이트)에서
실전 검증된 코드다. 타임아웃 값, CSS 색상 시스템, 표 레이아웃 수정 등은 전부
실제 프로덕션 배포 중 겪은 실패를 고치며 나온 값이다. **로직을 새로 작성하지
말고 템플릿을 복사한 뒤 `{{TOKEN}}`과 "비교 도메인 설정" 블록만 필요에 맞게
치환/수정**한다. 알려진 함정과 재현 절차는
[references/operations.md](references/operations.md)를 반드시 읽는다.

## 유사 스킬과의 구분

- `daily-diary-pipeline` / `daily-insight-pipeline`: **매일 정해진 시각에
  크론**이 돌고, 입력이 없는 날은 명언 풀 등 **폴백 콘텐츠**로 대체된다.
- `transcript-study-pipeline`: 입력이 **수천~수만 자짜리 스크립트 통짜
  텍스트**(수업/대화 STT)이고, 이디엄·어휘·퀴즈 등 어학 학습 포스트를
  만든다.
- 이 스킬(`term-comparison-pipeline`): 입력이 **짧은 단어/주제 한 줄**
  ("REST vs GraphQL", "Stack vs Heap")이고, **크론도 폴백도 없다** — 입력이
  있을 때만 동작한다(온디맨드). 결과물은 일기/학습 포스트가 아니라 **SVG
  도식 + 비교 표** 중심의 비교 콘텐츠다. "단어 하나 넣으면 두 대상을 도식과
  표로 비교해주는 사이트"면 이 스킬을 쓴다.

## 1단계 — 인터뷰

다음만 파악한다 (한 번에 몰아 묻지 말 것). 파이프라인 구조(온디맨드, 크론
없음, JSON 스키마)는 이미 실전 검증되었으므로 사용자가 명시적으로 바꿔달라고
하지 않는 한 그대로 쓴다:

1. **repo 이름, 사이트 제목/설명** (영문 사이트가 기본 — 도식 안의 라벨과
   본문이 전부 영문으로 생성됨)
2. **비교 대상 도메인이 IT 용어가 아니라면**(예: "요리 기법 비교", "역사적
   사건 비교") `pipeline/generate.py`의 "비교 도메인 설정" 블록
   (SYSTEM_PROMPT/GENERATE_PROMPT/HEADING_*)을 새 도메인에 맞게 다시 쓴다.
   JSON 스키마(title/summary/diagram_svg/table_headers/table_rows/
   key_differences/when_to_use_left+right/tags) 자체는 도메인에 무관하게
   범용적이므로 대부분 그대로 유지 가능하다.
3. **커스텀 도메인 여부** — 반드시 사용자 소유 도메인이어야 한다(`*.github.io`
   서브도메인은 GitHub이 거부한다). DNS에 CNAME이 이미 걸려 있는지
   `dig +short <domain>`으로 사전 확인한다.
4. **크론 없음을 재확인** — "매일 자동으로" 같은 요청이 섞여 있다면 이 스킬
   대신 `daily-diary-pipeline`이 맞는지 되짚어본다. 온디맨드가 맞다면 그대로
   진행한다.

## 2단계 — 스캐폴딩

1. 대상 디렉토리에서 `hugo new site . --force` 실행 후 `assets/template/`
   전체를 복사(템플릿 hugo.toml이 기본 생성본을 덮어씀). `.claude/launch.json`,
   `content/posts/.gitkeep`, `content/search/index.md`, `pipeline/state.json`
   포함 확인.
2. PaperMod 테마를 git submodule로 추가:
   ```bash
   git init -b main
   git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
   ```
3. **`{{TOKEN}}` 치환** — shell `sed` 반복문 대신 Python 딕셔너리 치환을
   쓴다(`*`가 들어간 값이나 여러 `-e` 체이닝 시 조용히 일부만 치환되지 않고
   넘어가는 함정이 있다). 대상 파일: `hugo.toml`, `README.md`, `input/term.md`,
   `.github/workflows/deploy.yml`, `.claude/launch.json`.
   토큰: `BASE_URL`, `SITE_TITLE`, `SITE_DESCRIPTION`, `GITHUB_USER`,
   `REPO_NAME`, `HOME_TITLE`, `HOME_DESCRIPTION`,
   `INPUT_BUTTON_LABEL`(예: "Compare a Term ✏️"), `WORKFLOW_NAME`,
   `HUGO_VERSION`(로컬 `hugo version`과 맞춤),
   `INPUT_INSTRUCTIONS_LINE1`(input/term.md 상단 안내 주석 첫 줄),
   `EXAMPLE_TERM`(예: "Stack vs Heap" — 첫 포스팅으로 쓸 예시 하나).
   치환 후 `grep -rn '{{[A-Z_]*}}' .`로 잔여 토큰 0개 확인.
4. `pipeline/generate.py`는 **엔진 코드(해시 dedup, claude-code/api 백엔드
   전환, 420초 타임아웃, Hugo 포스트 작성 골격)를 수정하지 않는다** — 전부
   실전에서 실패를 겪고 나온 값이다. 새 비교 도메인에 맞게 바꿀 곳은 파일
   상단의 "=== 비교 도메인 설정 ===" ~ "=== 비교 도메인 설정 끝 ===" 블록
   하나뿐이다. JSON 스키마 필드를 추가/삭제하면 `parse_result()`의 검증
   로직과 `write_post()`의 렌더링을 반드시 함께 수정한다 — 하나만 바꾸면
   생성 로그에 "JSON 파싱 실패"가 조용히 쌓인다.
5. `hugo.toml`의 goldmark `unsafe = true`는 인라인 SVG를 그대로 렌더링하기
   위해 필요하므로 제거 금지. `assets/css/extended/compare.css`(도식 카드
   래퍼 + `--compare-a`/`--compare-b` 색상 변수 + 표 반응형 수정)와
   `cards.css`(홈 카드 그리드)도 그대로 둔다.
6. `.github/workflows/deploy.yml`에는 **schedule 트리거가 없다** — push
   (`input/**`, `content/**`, `hugo.toml`, `archetypes/**`, `assets/**`
   경로만 감시)와 `workflow_dispatch`만 있다. `pipeline/**` 변경은 이 필터
   밖이므로 파이프라인 코드만 고쳤을 때는 `gh workflow run`으로 수동
   트리거해야 실제 동작을 검증할 수 있다.

## 3단계 — 로컬 검증

```bash
python3 pipeline/generate.py --dry-run   # 예시 용어 입력 경로 (claude CLI 로그인 세션 사용, 3-5분 소요될 수 있음)
hugo --minify && hugo server -D          # 도식 카드/표 레이아웃/라이트·다크 모드 직접 확인
```

dry-run은 실제 생성 호출이라 시간이 걸린다(로컬 측정 기준 유사 프롬프트가
~192초) — 240초 근처에서 멈춘 것처럼 보여도 기다린다. 검증 포인트:

- `diagram_svg`가 하드코딩된 hex가 아니라 `var(--compare-a)` 등 CSS 변수를
  `style` 속성으로 참조하는지
- 표가 브라우저 콘솔에서
  `document.querySelector('.post-content table').scrollWidth <=
  clientWidth`로 확인했을 때 가로 스크롤 없이 들어오는지
- 다크 모드 토글 시 도식 배경/강조색이 함께 전환되는지

어긋나면 SYSTEM_PROMPT를 보강하거나(색상 규칙 위반 시) `compare.css`를
확인한다(레이아웃 문제 시) — 세부 사항은 operations.md 참고.

## 4단계 — 배포

1. 커밋 → `gh repo create <name> --public --source . --push`
2. `gh api repos/<user>/<repo>/pages --method POST --field build_type=workflow`
3. (선택) 커스텀 도메인: `dig +short <domain>`으로 DNS가 `<user>.github.io.`를
   가리키는지 먼저 확인 → `static/CNAME` 생성 → `hugo.toml`의 `baseURL`
   변경 → `gh api repos/<user>/<repo>/pages --method PUT --field cname=<domain>`
   → `https_certificate.state`가 `approved`가 될 때까지 확인 후
   `--field https_enforced=true`
4. **사용자 안내 (에이전트가 대신 못 함)**: `claude setup-token` 실행 →
   브라우저 인증 **후** 터미널에 출력되는 `sk-ant-oat01-...` 토큰을
   `gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo <user>/<repo>`로 등록
5. 초기 push가 이미 워크플로를 트리거한다. Secret 등록 전에는 generate
   잡만 실패하고(예시 포스트가 로컬에서 이미 커밋되어 있다면) deploy는
   정상 — 등록 후 `input/term.md`에 실제 새 용어를 추가해 push하고, 워크플로
   generate 단계가 실제로 성공하는지(수 분 소요) 끝까지 확인한다.

## 완료 기준

- `input/term.md`에 새 용어를 추가해 push하는 온디맨드 경로가 실제 CI
  생성·배포로 검증됨 (수동 실행이 아니라 커밋만으로 게시됨)
- 도식이 라이트/다크 모드 둘 다에서 사이트 배경과 어울리게 렌더링되고,
  좌/우 비교 대상이 일관된 두 가지 강조색으로 구분됨
- 비교 표가 일반적인 데스크톱 폭에서 가로 스크롤 없이 한 화면에 들어옴
- 홈 카드 그리드에서 인트로↔첫 카드 간격이 그리드 gap과 일치
- README에 온디맨드 사용법과 `claude setup-token` 안내가 반영됨
