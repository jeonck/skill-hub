# hextra-roadmap-kb 사용 가이드

`hextra-roadmap-kb`는 [ai-security](https://github.com/jeonck/ai-security) 프로젝트와 동일한 구조의
**한국어 Hugo + Hextra "학습 로드맵형" 지식베이스 사이트**를 새로운 주제로 빠르게 복제 생성하는 Claude Code 스킬입니다.

이 문서는 스킬 자체의 설명(`SKILL.md`)과는 별도로, **다른 사용자가 이 스킬을 처음 접했을 때 무엇을, 어떤 순서로 준비/요청하면 되는지**를 안내하는 활용 가이드입니다.

---

## 1. 이 스킬로 만들 수 있는 것

"주제 A에 대해 체계적으로 학습할 수 있는 한국어 지식베이스 + 실습 가이드 + 도구 모음 + 블로그 + 용어집"을
GitHub Pages에 정적 사이트로 배포 가능한 형태로 한 번에 생성합니다.

생성되는 사이트는 5개 메인 섹션으로 구성됩니다.

| 섹션 | 메뉴명(예) | 역할 |
|---|---|---|
| `content/docs/` | "○○ 학습 로드맵" | 카테고리별로 나뉜 이론/개념 설명, 추천 학습 순서 |
| `content/labs/` | "실습" | 따라 하면 재현되는 단계별 실습 가이드 |
| `content/tools/` | "도구" | 관련 오픈소스 도구·공식 표준 참고자료 |
| `content/blog/` | "블로그" | 동향/업데이트 글, RSS 제공 |
| `content/glossary/` | "용어집" | `data/ko/termbase.yaml` 기반 용어 사전 |

실제 예시는 ai-security 사이트(`docs` 6개 카테고리: 기반 지식 / 공격 기법 / 방어 기법 / 인프라·공급망 보안 /
거버넌스·리스크 관리 / 레드팀·실전 경험)를 참고하세요.

---

## 2. 사전 준비물

스킬을 실행하기 전에 아래 정보를 미리 정리해두면 작업이 훨씬 빠르게 진행됩니다.
(없어도 Claude가 ai-security 예시를 참고해 초안을 제안하지만, 직접 정해두면 왔다 갔다 하는 시간이 줄어듭니다.)

1. **주제(topic)** — 예: "클라우드 보안", "재무제표 분석", "임베디드 보안" 등
2. **사이트 제목 / GitHub 사용자명 / repo 이름** → `baseURL`, GitHub 메뉴 링크 결정에 사용
   - 예: `https://<user>.github.io/<repo>/`
3. **docs 카테고리 5~6개** — 각각 한글 이름 + 1줄 설명 + 아이콘 후보
4. **추천 학습 순서**와 그 이유 (1단락)
5. **배경별 진입점 2~3개** — 예: "보안 담당자 / 개발자 / 데이터 분석가"처럼 독자 유형별 추천 경로
6. **카테고리별 토픽 페이지 목록** (카테고리당 3~4개 정도)
7. **실습(Labs) 아이템 2개 이상** — 제목, 목표, 필요 패키지/환경
8. **도구(Tools) 카테고리 2~3개** — 도구 묶음 이름 + 대표 도구들
9. **용어집 용어 10~20개** — 용어, 약어(영문), 정의

---

## 3. 호출 방법

Claude Code에서 새 프로젝트 디렉터리를 열고 다음과 같이 요청하면 스킬이 자동으로 트리거됩니다.

```text
이 프로젝트 형태로 "클라우드 보안" 주제 사이트 만들어줘 (ai-security와 동일한 구조)
```

또는 위 1~9번 정보를 미리 정리해 함께 전달하면 더 정확합니다:

```text
hextra-roadmap-kb 스킬로 새 사이트를 만들어줘.
- 주제: 클라우드 보안
- repo: my-cloud-sec, github user: myuser
- docs 카테고리: ① IAM 기초 ② 데이터 보호 ③ 네트워크/워크로드 보안 ④ 탐지·대응 ⑤ 거버넌스·컴플라이언스
- ...
```

정보가 부족한 항목은 Claude가 ai-security의 패턴을 보여주며 같은 형식으로 제안하고 확인을 받습니다.

---

## 4. 진행 절차 (Claude가 수행하는 작업)

1. **Hugo 프로젝트 초기화**: `hugo new site . --force --format toml`, `git submodule add` 로 Hextra 테마 추가
2. **`hugo.toml` 작성**: 사이트 제목/설명/baseURL/GitHub 링크 반영, 메뉴(로드맵/실습/도구/블로그/용어집/GitHub/검색) 구성
3. **홈페이지(`content/_index.md`)**: 히어로 영역 + 카테고리 수만큼 feature-card 그리드
4. **`content/docs/_index.md`**: 로드맵 개요, 추천 학습 순서, 배경별 진입점, N주 학습 플랜, 전체 섹션 카드
5. **카테고리별 섹션**(`content/docs/<category>/`): 카테고리 설명 + 토픽 페이지 카드 목록 + 각 토픽 페이지
6. **Labs 섹션**(`content/labs/`): 실습 목록 + 환경설정 안내 + 안전/권한 경고 + 실습별 페이지(목표→사전준비→단계별 실행→결과확인→체크리스트)
7. **Tools 섹션**(`content/tools/`): 도구셋별 카드 + 표준/참고문서 페이지
8. **Blog 섹션**(`content/blog/`): RSS 배지 포함 인트로 + 첫 포스트
9. **Glossary**(`content/glossary/`, `data/ko/termbase.yaml`): Hextra 내장 `layout: glossary`와 `{{< term >}}` 숏코드 활용
10. **GitHub Pages 배포 설정**(`.github/workflows/deploy.yml`, `.gitignore`)

각 단계는 `assets/*.template` 파일을 기반으로 진행되며, 플레이스홀더(`{{...}}`)를 새 주제에 맞게 채웁니다.

---

## 5. 생성 후 확인 사항

- `hugo server` 로 로컬에서 빌드/렌더링 확인
- GitHub repo의 **Settings → Pages → Source**를 **GitHub Actions**로 설정
- `hugo.toml`의 `baseURL`이 실제 GitHub Pages 주소와 일치하는지 확인
- Hugo **Extended** 버전이 설치되어 있는지 확인 (Hextra 테마 요구사항)

---

## 6. 참고 — ai-security 프로젝트와의 관계

이 스킬의 모든 템플릿은 `ai-security` 프로젝트(`/Users/mac/ws/claude/ai-security`)의 실제 구조를 일반화한 것입니다.
구체적인 작성 예시가 필요하면 해당 프로젝트의 다음 파일들을 참고하세요.

- `hugo.toml` — 메뉴/검색/테마 설정 전체 예시
- `content/_index.md` — 홈 히어로 + feature-grid 실제 예시
- `content/docs/_index.md`, `content/docs/foundations/_index.md` — 로드맵 개요 및 카테고리 섹션 실제 예시
- `content/labs/_index.md`, `content/labs/lab1-adversarial-attack.md` — 실습 섹션/페이지 실제 예시
- `content/tools/_index.md` — 도구 섹션 실제 예시
- `data/ko/termbase.yaml` — 용어집 데이터 실제 예시
- `.github/workflows/deploy.yml` — GitHub Pages 배포 워크플로우 실제 예시

새 주제에서 "이 부분은 어떻게 써야 하지?"라는 질문이 생기면, 위 파일들에서 대응되는 부분을 그대로 참고하여
같은 톤/구조로 작성하면 됩니다.
