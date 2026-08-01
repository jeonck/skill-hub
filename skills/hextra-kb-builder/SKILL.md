---
name: hextra-kb-builder
description: Hugo Hextra 테마를 사용하여 Mermaid, LaTeX, 검색 기능이 포함된 기술 지식베이스를 초기화합니다. GitHub Pages 배포 설정까지 자동으로 완료합니다.
---

# Hextra KB Builder

이 스킬은 Hugo Hextra 테마를 사용하여 현대적인 기술 지식베이스(Knowledge Base)를 구축하는 워크플로우를 제공합니다.

## 주요 기능
- **Hugo Hextra 테마 설치**: Git Submodule을 통한 최신 테마 설치.
- **모던 디자인 적용**: Pretendard 폰트 및 최적화된 타이포그래피 설정.
- **수식 및 다이어그램**: LaTeX(KaTeX) 및 Mermaid 자동 설정.
- **검색 지원**: FlexSearch 기반의 오프라인 검색창 활성화.
- **커스텀 레이아웃**: 메인 페이지를 제외한 Docs 사이드바에 검색창 상시 노출.
- **GitHub Pages 배포**: 최적화된 GitHub Actions 워크플로우 구성.

## 워크플로우

### 1. 프로젝트 초기화
새 Hugo 사이트를 생성하고 Hextra 테마를 추가합니다.

```bash
hugo new site . --force --format yaml
git init
mkdir -p themes
git submodule add https://github.com/imfing/hextra.git themes/hextra
```

### 2. 설정 파일 및 디자인 구성
- `assets/hugo.yaml.template`을 참조하여 `hugo.yaml`을 작성합니다.
- `assets/custom.css.template` 내용을 `assets/css/custom.css`로 복사하여 모던한 폰트와 스타일을 적용합니다.

### 3. 레이아웃 오버라이드
사이드바 검색창 설정을 위해 `assets/sidebar.html.template` 내용을 `layouts/partials/sidebar.html`로 복사합니다.

### 4. 배포 설정
`assets/deploy.yaml.template` 내용을 `.github/workflows/deploy.yaml`로 작성합니다.

### 5. 초기 콘텐츠 생성
`content/docs/_index.md` 및 `content/_index.md`를 생성하여 기본 구조를 잡습니다.

## 주의 사항
- Hugo **Extended** 버전이 설치되어 있어야 합니다.
- GitHub Pages 설정에서 Source를 **GitHub Actions**로 변경해야 합니다.
- LaTeX 수식 작성 시 `$ ... $` 또는 `$$ ... $$`를 사용합니다.
