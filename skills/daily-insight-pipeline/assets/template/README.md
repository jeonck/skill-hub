# {{SITE_TITLE}}

매일 아침(KST 07:00) RSS · Reddit · Hacker News · GitHub에서 새 글을 수집하고,
Claude API가 [context.md](context.md)(내 기술 스택/환경) 기준으로 **행동 판정**을 내린 뒤,
무관 판정을 제외한 항목만 Hugo 포스트로 커밋하여 GitHub Pages에 배포한다.

**사이트:** {{BASE_URL}}

## 판정 체계

| 판정 | 의미 | 예 |
|---|---|---|
| 🔥 즉시조치 | 내 스택에 직접 해당하는 보안 이슈 / breaking change | EKS 대상 CVE, GitHub Actions 공급망 공격 |
| 📌 백로그 | 스택 해당, 긴급하지 않음 | 사용 도구의 deprecation, 개선 도구 |
| 📚 학습 | 스택 무관이나 관심 분야(LLM 보안, eBPF 등) 해당 | 신규 공격 기법 분석 |
| 무관 | 그 외 전부 → **포스트 생성 안 함** | 마케팅, 타 스택 이슈 |

각 포스트는 `근거`(내 스택 어디에 해당하는지)와 `액션`(이번 주 안에 할 구체적 작업 1개)을 담는다.

## 구조

```
.
├── context.md                  # 내 기술 스택/환경 = 판정 기준 (여기를 고치면 판정이 바뀜)
├── feeds.yaml                  # 수집 소스 정의 (RSS/Reddit/HN/GitHub)
├── pipeline/
│   ├── collect.py              # 수집 → 판정 → 포스트 생성
│   ├── requirements.txt
│   ├── processed.json          # 처리한 URL 해시 기록 (중복 방지, 90일 보존)
│   ├── expire.py               # 학습 항목 14일 경과 시 자동 완료 (EXPIRE_DAYS로 조정)
│   └── done.sh                 # 주간 리뷰: status 대기 → 완료
├── content/insights/           # 생성된 포스트
├── layouts/                    # 자체 Hugo 레이아웃 (외부 테마 없음)
├── hugo.toml                   # taxonomy: verdict / status / tags
└── .github/workflows/daily.yml # cron 수집 + Pages 배포
```

## 최초 세팅

1. **판정 인증 등록** — 둘 중 하나 (repo Settings → Secrets and variables → Actions)
   - **권장: Claude 구독 (Pro/Max)** — 로컬에서 `claude setup-token` 실행 → 브라우저 인증 →
     출력된 토큰을 `CLAUDE_CODE_OAUTH_TOKEN` Secret으로 등록.
     API 크레딧 불필요, 구독 사용량으로 차감됨.
   - **대안: Claude API 키** — `ANTHROPIC_API_KEY` Secret 등록 (계정에 크레딧 필요).
     `CLAUDE_CODE_OAUTH_TOKEN`이 없을 때만 사용됨.
2. **Pages 활성화** — Settings → Pages → Source: **GitHub Actions**
3. **첫 실행** — Actions 탭 → `Daily Insights` → Run workflow (수동 실행은 신규 항목이 없어도 배포함)

이후 매일 UTC 22:00 (KST 07:00) 자동 실행.

## 로컬 실행

```bash
pip install -r pipeline/requirements.txt

# claude CLI가 로그인돼 있으면 그대로 동작 (구독 인증, API 키 불필요)
# dry-run: 파일 생성/기록 갱신 없이 판정 결과만 stdout 출력
python pipeline/collect.py --dry-run

# 판정 건수 제한 (기본 30, 비용 안전장치)
MAX_ITEMS=5 python pipeline/collect.py --dry-run

# 실제 생성 후 로컬 미리보기
python pipeline/collect.py
hugo server        # → http://localhost:1313/insight/
```

환경변수:
- `JUDGE_BACKEND`: `claude-code`(구독, 기본 — claude CLI가 PATH에 있을 때) | `api`(API 키 과금)
- `CLAUDE_MODEL`(기본 `claude-sonnet-4-6`), `MAX_ITEMS`(기본 30), `GITHUB_TOKEN`(선택, rate limit 완화)

## 운영 루틴

**매일 아침 (2분)**
1. 사이트 접속 → 🔥 즉시조치 · 대기 확인 → 있으면 액션 항목 그대로 실행
2. 📌 백로그는 눈으로만 훑기

**자동 정리**
- 학습 항목은 14일이 지나면 자동으로 완료 처리됨 (매일 아침 실행, `EXPIRE_DAYS`로 조정)
- 즉시조치·백로그는 자동 만료 없음 — 사람이 처리 여부를 결정

**수집 일시중지/재개** (휴가, 소스 점검 등)
- 웹/모바일: Actions 탭 → **Pipeline Control** → Run workflow → pause / resume / status 선택
- 터미널:
  ```bash
  ./pipeline/pause.sh    # cron의 수집·판정만 중지 (완료 처리 푸시 배포는 계속 동작)
  ./pipeline/resume.sh   # 재개
  ```

**매주 금요일 (15분)**
1. 백로그/학습 중 처리한 항목 완료 처리:
   ```bash
   ./pipeline/done.sh content/insights/2026-07-09-some-post.md
   git commit -am "review: weekly done" && git push
   # push 시 배포 전용 워크플로가 돌아 1~2분 내 사이트 반영됨
   ```
2. 판정 품질이 어긋나면 **context.md를 수정** (스택 변경, 관심 분야 추가/삭제, 명시적 제외 보강)
   — 다음 실행부터 반영됨
3. 소스가 노이즈만 내면 feeds.yaml에서 제거

## 비용

- 항목당 1회 Claude 호출 (입력 ~2K 토큰 · 출력 ~200 토큰), 실행당 최대 `MAX_ITEMS`(30)건
- **claude-code 백엔드(기본)**: 별도 과금 없음 — Claude 구독(Pro/Max) 사용량으로 차감.
  판정 1건당 ~10초, 30건 ≈ 5분
- **api 백엔드**: context.md prompt cache 적용, 일 30건 × sonnet 기준 ≈ $0.05~0.1/일

## 알려진 제약

- **Reddit**: GitHub Actions 등 클라우드 IP에서 `.json` API가 403으로 차단되는 경우가 많음.
  실패해도 다른 소스는 정상 수집됨 (소스별 오류 격리).
- **hnrss.org**: 간헐적 502 — 해당 실행만 0건, 다음 실행에서 자동 회복.
- **GitHub Search**: `created:>N일` + 스타 조건이라 결과가 0건인 날이 흔함 (정상).
- **크레딧 부족/인증 오류**: 즉시 중단하고 워크플로를 실패로 표시함 (의도된 동작 —
  Actions 실패 알림으로 인지). 인증 복구 후 다음 실행에서 미처리 항목 자동 재시도.
- **OAuth 토큰 만료**: `claude setup-token`으로 재발급 후 Secret 갱신.
