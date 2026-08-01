---
name: algolia-docusaurus
description: This skill should be used when adding Algolia DocSearch to a Docusaurus v3 site deployed on GitHub Pages. It automates file creation and configuration, then guides the user through the manual Algolia account steps. Triggers when the user asks to add search functionality, integrate Algolia, or set up DocSearch on a Docusaurus site.
---

# Algolia DocSearch — Docusaurus 연동 스킬

GitHub Pages에 배포된 Docusaurus v3 사이트에 Algolia DocSearch 검색을 연동하는 전체 워크플로우를 제공합니다. GitHub Actions를 통해 문서 변경 시 자동으로 인덱스를 최신화합니다.

## 사전 확인

시작 전 반드시 확인:

```bash
gh auth status  # GitHub 사용자명 확인
```

다음 정보를 사용자에게 확인:
- `GITHUB_USERNAME` — GitHub 사용자명
- `REPO_NAME` — 저장소 이름
- `INDEX_NAME` — Algolia 인덱스 이름 (보통 REPO_NAME과 동일)
- `ALGOLIA_APP_ID` — Algolia Application ID (공개 가능)
- `ALGOLIA_SEARCH_KEY` — Algolia Search-Only API Key (공개 가능)

Algolia 크리덴셜이 없으면 **Step 0**을 먼저 안내한다.

---

## Step 0. 사용자가 직접 해야 하는 작업 (브라우저 필요)

Claude가 자동화할 수 없는 작업. 아래 안내를 제공하고 완료 후 진행:

**A. Algolia 계정 및 인덱스 생성**
1. algolia.com → Start for free 가입
2. 대시보드 → Create index → 이름 입력 (예: `ai-eng`)
3. Settings → API Keys 에서 세 가지 키 확인

**B. GitHub Repository Secrets 등록**
저장소 → Settings → Secrets and variables → Actions → Repository secrets

| Secret 이름 | 등록할 값 |
|---|---|
| `ALGOLIA_APP_ID` | Application ID |
| `ALGOLIA_ADMIN_KEY` | **Write API Key** (Admin Key, 크롤러용) |

> Search-Only API Key는 Secrets 불필요 — 코드에 직접 입력해도 안전.
> Write API Key는 반드시 Secrets에만 보관, 코드에 절대 노출 금지.

---

## Step 1. `.algolia/config.json` 생성

`references/crawler-config-template.json`을 읽어 `{{GITHUB_USERNAME}}`, `{{REPO_NAME}}`, `{{INDEX_NAME}}`을 실제 값으로 치환하여 `.algolia/config.json`으로 생성한다.

---

## Step 2. `docusaurus.config.ts` 수정

`themeConfig` 안에 `algolia` 블록을 추가한다:

```typescript
algolia: {
  appId: 'ALGOLIA_APP_ID_VALUE',
  apiKey: 'ALGOLIA_SEARCH_ONLY_KEY_VALUE',
  indexName: 'INDEX_NAME',
  contextualSearch: false,   // ← 단일 언어 사이트는 반드시 false
  searchPagePath: 'search',
},
```

### 핵심 주의사항: `contextualSearch: false`

`contextualSearch: true`(기본값)이면 Docusaurus가 검색 쿼리에 `language:ko` 필터를 자동으로 추가한다. DocSearch 크롤러가 레코드에 `language` 속성을 정확히 설정하지 않으면 검색 결과가 0건으로 나온다. **단일 언어 사이트에서는 반드시 `false`로 설정한다.**

---

## Step 3. GitHub Actions 워크플로우 생성

`references/crawl-workflow-template.yml`을 읽어 `.github/workflows/algolia-crawl.yml`로 복사한다.

워크플로우의 `workflows:` 항목이 기존 배포 워크플로우의 `name:`과 **정확히 일치**하는지 확인한다.

```yaml
on:
  workflow_run:
    workflows: ["Deploy to GitHub Pages"]  # 배포 워크플로우 name과 일치해야 함
```

일치하지 않으면 크롤러가 자동으로 트리거되지 않는다.

---

## Step 4. 빌드 검증 및 푸시

```bash
npm run build   # 에러 없이 빌드 성공 확인
git add .algolia/config.json docusaurus.config.ts .github/workflows/algolia-crawl.yml
git commit -m "Algolia DocSearch 검색 연동"
git push
```

---

## Step 5. 동작 확인

```bash
gh run list --repo GITHUB_USERNAME/REPO_NAME --limit 5
```

두 워크플로우가 순서대로 완료되면 성공:
1. `Deploy to GitHub Pages` — 사이트 빌드·배포
2. `Algolia DocSearch Crawl` — 크롤러 실행, 인덱스 업데이트

크롤 워크플로우 로그 마지막에 `Nb hits: XXX` 가 표시되면 인덱싱 완료.

---

## 자주 발생하는 문제

| 증상 | 원인 | 해결 |
|---|---|---|
| 배포 사이트에서 검색 결과 0건 | `contextualSearch: true` 상태 | `false`로 변경 후 재배포 |
| 크롤러 워크플로우가 트리거되지 않음 | `workflows:` 이름 불일치 | 배포 워크플로우의 `name:` 값과 동일하게 수정 |
| 로컬 개발 서버에서 검색 안 됨 | Docusaurus 의도적 비활성화 | `npm run build && npm run serve` 또는 배포 사이트에서 확인 |
| 크롤러 실행 후 인덱스 비어있음 | 사이트가 아직 배포 전 크롤 | `sleep 30` 대기 시간이 충분한지 확인, 필요 시 늘림 |

## 참조 파일

- `references/crawler-config-template.json` — `.algolia/config.json` 생성용 템플릿
- `references/crawl-workflow-template.yml` — GitHub Actions 워크플로우 템플릿
