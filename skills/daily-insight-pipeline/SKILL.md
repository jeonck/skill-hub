---
name: daily-insight-pipeline
description: 임의 분야의 일일 자료수집 → Claude 행동판정 → Hugo → GitHub Pages 파이프라인을 스캐폴딩하는 스킬. RSS/Reddit/HN/GitHub에서 매일 수집하고 사용자 컨텍스트 기준으로 즉시조치/백로그/학습/무관을 판정해 사이트로 배포한다. "OO 분야 일일 수집 파이프라인 만들어줘", "insight 프로젝트처럼 다른 주제로", "매일 자동으로 뉴스/논문/자료 모아서 판정하는 사이트" 같은 요청에 사용한다.
---

# Daily Insight Pipeline Builder

임의 분야(기술, 투자, 논문, 규제 동향 등)에 대해 다음 파이프라인을 갖춘 GitHub repo를 생성한다:

매일 아침 KST 07:00 수집(RSS/Reddit/HN/GitHub) → Claude가 context.md 기준 행동 판정
(즉시조치/백로그/학습/무관) → 무관 제외 Hugo 포스트 커밋 → GitHub Pages 배포.

`assets/template/`의 코드는 실전 검증 완료본이다. **로직을 새로 작성하지 말고 템플릿을
복사한 뒤 도메인 파라미터만 교체**한다. 알려진 함정과 세부 절차는
[references/operations.md](references/operations.md)를 읽는다.

## 1단계 — 인터뷰

다음을 파악한다 (한 번에 몰아 묻지 말 것):

1. **분야와 목적**: 무엇을 수집해 어떤 행동으로 연결하고 싶은가
2. **판정 컨텍스트**: 사용자의 환경/현황(직접 이해관계), 관심 세부 주제, 명시적 제외 대상
3. **소스 후보**: 사용자가 아는 블로그/피드가 있는지. 없으면 분야 대표 소스를 제안
4. **repo 이름과 사이트 제목**

verdict 라벨은 기본(즉시조치/백로그/학습/무관)을 권장하고, 사용자가 원할 때만 변경한다
(변경 절차는 operations.md 참조).

## 2단계 — 스캐폴딩

1. 대상 디렉토리에 `assets/template/` 전체를 복사 (`.gitkeep`, 스텁 `_index.md` 포함)
2. 플레이스홀더 치환:
   - `hugo.toml`: `{{BASE_URL}}` → `https://<user>.github.io/<repo>/`, `{{SITE_TITLE}}`
   - `layouts/baseof.html`: `{{REPO_URL}}` → `https://github.com/<user>/<repo>`
   - `README.md`: `{{SITE_TITLE}}`, `{{BASE_URL}}` 치환 + 판정 체계 표의 예시를 도메인에 맞게 수정
3. `context.md`: 인터뷰 내용으로 [대괄호] 전부 교체. 대괄호가 남으면 판정 품질이 나빠진다
4. `feeds.yaml`: 도메인 소스로 교체. **각 RSS URL을 curl로 HTTP 200 확인 후에만 등록**.
   Reddit 서브레딧/HN 쿼리/GitHub 검색어도 도메인에 맞게 조정 (임계값 가이드는 operations.md)
5. `pipeline/collect.py`의 system 프롬프트 첫 줄("DevSecOps 어시스턴트")을 도메인에 맞는
   역할로 수정 — 이 한 줄 외에 collect.py는 수정하지 않는다

## 3단계 — 로컬 검증

```bash
python3 -m venv .venv && .venv/bin/pip install -r pipeline/requirements.txt
MAX_ITEMS=5 .venv/bin/python pipeline/collect.py --dry-run   # claude CLI 로그인 세션 사용
hugo --quiet
```

dry-run 판정 결과를 사용자에게 보여주고 품질(무관 필터, 액션 구체성)을 함께 확인한다.
판정이 어긋나면 context.md를 보강하고 재실행한다.

## 4단계 — 배포

1. `git init -b main` → 커밋 → `gh repo create <name> --public --source . --push`
   (기존 repo면 remote add 후 push)
2. Pages 활성화: `gh api -X POST repos/<user>/<repo>/pages -f build_type=workflow`
3. **사용자 안내 (에이전트가 대신 못 하는 부분)**: `claude setup-token` 실행 →
   최종 출력되는 `sk-ant-oat01-...` 토큰(브라우저의 인증 코드 아님!)을
   `gh secret set CLAUDE_CODE_OAUTH_TOKEN` 으로 등록하도록 안내
4. Secret 등록 확인 후: `gh workflow run daily.yml` → run 완료 대기 →
   사이트 홈과 verdict/status/tags 메뉴 URL 전부 HTTP 200 확인

## 완료 기준

- 워크플로 collect/deploy 모두 success이고 실제 판정 포스트가 사이트에 표시됨
- 메뉴 404 없음 (스텁 `_index.md`가 복사되었는지 확인)
- README에 도메인에 맞는 운영 루틴이 반영됨
