---
name: transcript-study-pipeline
description: This skill should be used when building a site that turns pasted class/conversation transcripts into structured English-study posts (idioms with examples, vocabulary, spoken-mistake corrections, fill-in-the-blank toggle quizzes, and a narrative mini diary) published via Hugo + GitHub Pages with an instant push-hook pipeline. Triggers on requests like "talktime 같은 사이트 만들어줘", "수업 스크립트 올리면 학습 포스트로 만들어주는 사이트", "스크립트 입력 → 즉시 처리(후킹) 학습 블로그", or replicating the jeonck/talktime structure for a new topic, class, or user.
---

# Transcript Study Pipeline Builder

수업/회화에서 수집한 **다량의 스크립트(STT 결과물)를 통짜로 붙여넣으면**, 저장(커밋)하는
순간 push 후킹으로 Claude가 분석해 구조화된 영문 학습 포스트를 자동 게시하는 사이트를
스캐폴딩한다:

```
input/script.md (스크립트 전체를 코드블록에 붙여넣기, GitHub 웹 UI에서 수정)
        │
        ▼  저장(커밋) 즉시 push 후킹 실행 + 매일 크론(폴백용)
pipeline/generate.py — Claude가 분석해 섹션 구성:
  Session Overview / 💬 Idioms(설명+예문 2) / 📚 Vocabulary /
  🔧 Say It Better(실제 발화 vs 교정) / ✅ Check Yourself(빈칸 채우기 토글 퀴즈) /
  ✍️ Mini Diary(하나의 사건 중심 일기, 학습 표현 굵게 강조)
        │
        ▼  커밋 & push → Hugo build → GitHub Pages 배포
```

`assets/template/`의 코드는 [jeonck/talktime](https://github.com/jeonck/talktime)
(talktime.metacog.co.kr)에서 실전 검증된 코드다. **로직을 새로 작성하지 말고 템플릿을
복사한 뒤 `{{TOKEN}}`만 치환**한다. 알려진 함정과 재생성 절차는
[references/operations.md](references/operations.md)를 반드시 읽는다.

## 유사 스킬과의 구분

- `daily-diary-pipeline`: **한 줄 입력**(문장/주제) → 확장 콘텐츠. 입력이 한 줄 단위.
- 이 스킬: **스크립트 통짜 입력**(수천~수만 자 STT) → 분석·추출형 학습 포스트.
  코드블록 전체가 항목 1개이고(`---` 구분선으로 여러 개 가능), push 후킹으로
  저장 즉시 처리된다. "수업 녹취/스크립트를 넣으면 정리해주는 사이트"면 이 스킬.

## 1단계 — 인터뷰

다음만 파악한다 (한 번에 몰아 묻지 말 것). 섹션 구성 자체는 검증된 형태이므로
사용자가 명시적으로 바꿔달라고 하지 않는 한 그대로 쓴다:

1. **repo 이름, 사이트 제목/설명** (사이트는 영문 UI가 기본)
2. **크론 시각** (기본 KST 07:00 권장 — 입력 없는 날 이디엄 미니 레슨 폴백용)
3. **커스텀 도메인 여부** — 반드시 사용자 소유 도메인이어야 한다. `*.github.io`
   하위 도메인은 GitHub이 거부한다(operations.md 참고)
4. (선택) 대상 언어가 영어가 아니면 `generate.py`의 SYSTEM_PROMPT/GENERATE_PROMPT/
   FALLBACK_QUOTES를 해당 언어에 맞게 조정

## 2단계 — 스캐폴딩

1. 대상 디렉토리에서 `hugo new site . --force` 실행 후 `assets/template/` 전체를 복사
   (템플릿 hugo.toml이 기본 생성본을 덮어씀. `.claude/launch.json`,
   `content/posts/.gitkeep`, `pipeline/state.json` 포함 확인)
2. PaperMod 테마를 git submodule로 추가:
   ```bash
   git init -b main
   git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
   ```
3. **`{{TOKEN}}` 치환** — shell sed 대신 Python 딕셔너리 치환을 쓴다(operations.md의
   이스케이프 함정 참고). 대상 파일: `hugo.toml`, `README.md`, `input/script.md`,
   `.github/workflows/daily.yml`, `.claude/launch.json`.
   토큰: `BASE_URL`, `SITE_TITLE`, `SITE_DESCRIPTION`, `GITHUB_USER`, `REPO_NAME`,
   `HOME_TITLE`, `HOME_DESCRIPTION`, `INPUT_BUTTON_LABEL`(예: "Add Transcript ✏️"),
   `CRON_KST_TIME`, `CRON_UTC`(KST-9h), `CRON_COMMENT`, `WORKFLOW_NAME`,
   `HUGO_VERSION`(로컬 `hugo version`과 맞춤).
   치환 후 `grep -rn '{{[A-Z_]*}}' .`로 잔여 토큰 0개 확인.
4. `pipeline/generate.py`는 **기본적으로 수정하지 않는다** — 프롬프트(빈칸 퀴즈 규칙,
   단일 사건 일기 규칙 포함)와 엔진 모두 실전 검증본이다. 스키마를 바꿔야 한다면
   GENERATE_PROMPT의 JSON 스키마 + `parse_result()` + `write_post()` 셋을 반드시 함께
   수정한다(하나만 바꾸면 파싱 실패). **"Privacy rules" 문단은 예외 없이 그대로
   유지한다** — 실제 사람의 실명·나이·병력 등이 섞인 스크립트를 공개 사이트에
   게시하는 구조이므로 이 규칙이 없으면 개인정보 노출로 직결된다.
5. `hugo.toml`의 goldmark `unsafe = true`는 퀴즈 `<details>` 토글용이므로 제거 금지.
   `assets/css/extended/`의 cards.css(카드 그리드 + `align-content: start` 여백 수정),
   quiz.css(토글 스타일)도 그대로 둔다.

## 3단계 — 로컬 검증

```bash
python3 pipeline/generate.py --dry-run   # 스크립트 입력 경로 (claude CLI 로그인 세션 사용)
# input/script.md 코드블록을 비운 채 한 번 더 → 폴백 이디엄 경로 확인
hugo --minify && hugo server -D          # 카드 그리드/여백/퀴즈 토글 직접 확인
```

dry-run 검증 포인트: 퀴즈가 전부 빈칸(`____`) 문장이고 **선택지가 그 수업의
idioms/vocabulary 항목에서만** 나오는지, 일기가 낱개 문장 나열이 아니라 **하나의
사건을 다룬 이야기**인지. 어긋나면 프롬프트를 보강해 재실행한다. **실명·나이·병력 등이
포함된 실제(또는 유사) 스크립트로도 한 번 dry-run해서, summary/corrections/quiz/diary
어디에도 그 정보가 그대로 나오지 않는지** 반드시 확인한다 — 익명화는 결과물로
검증해야 신뢰할 수 있다.

## 4단계 — 배포

1. 커밋 → `gh repo create <name> --public --source . --push`
2. `gh api repos/<user>/<repo>/pages --method POST --field build_type=workflow`
3. **사용자 안내 (에이전트가 대신 못 함)**: `claude setup-token` 실행 → 브라우저 인증
   **후** 터미널에 출력되는 `sk-ant-oat01-...` 토큰을
   `gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo <user>/<repo>` 로 등록
4. 초기 push가 이미 워크플로를 트리거한다(후킹 검증 겸). Secret 등록 전에는 generate
   잡만 실패하고 deploy는 정상 — 등록 후 재확인
5. (선택) 커스텀 도메인: operations.md의 절차를 따른다. 사용자가 말한 도메인이
   `*.github.io` 형태면 등록 불가함을 설명하고, `dig`로 실제 CNAME이 걸린 소유
   도메인을 찾아 확인받는다

## 완료 기준

- 스크립트 입력 경로와 폴백(빈 입력) 경로 둘 다 실제 CI 배포로 검증됨
- input/script.md 커밋만으로(수동 실행 없이) 포스트가 게시되는 후킹 동작 확인
- 홈 카드 그리드에서 인트로↔첫 카드 간격이 그리드 gap(24px)과 일치
- 퀴즈: 빈칸 문장 + 학습 단어 선택지 + Show answer 토글 동작
- 익명화: 실명 포함 샘플로 dry-run해 게시물에 개인정보가 없는지 확인됨,
  README/input 안내문에 "붙여넣기 전 실명 제거 권장" 문구 포함
- README에 운영 루틴과 `claude setup-token` 안내 반영
