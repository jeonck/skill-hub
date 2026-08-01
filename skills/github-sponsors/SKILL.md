---
name: github-sponsors
description: "GitHub Sponsors 후원 버튼을 정적 사이트(Hugo, Jekyll, Docusaurus, 일반 HTML)에 추가하는 스킬. 트리거: '후원 버튼 추가', 'GitHub Sponsors', 'sponsor 기능', '후원 기능', 'FUNDING.yml' 등의 요청이 있을 때 사용."
---

# GitHub Sponsors 후원 버튼 추가

이 스킬은 정적 사이트에 GitHub Sponsors 후원 기능을 추가한다.  
프레임워크별 템플릿을 제공하며, 저장소 Sponsor 버튼과 사이트 내 후원 UI를 함께 구성한다.

---

## 수행 절차

### Step 1 — 정보 파악

작업 전 아래 두 가지를 확인한다.

1. **GitHub 사용자명**: `github.com/<username>` 에서 확인 (예: `jeonck`)
2. **사이트 프레임워크**: Hugo / Jekyll / Docusaurus / 일반 HTML 중 하나

정보가 없으면 사용자에게 질문한다.  
프로젝트 루트의 파일(hugo.yaml, _config.yml, package.json 등)로 프레임워크를 자동 감지해도 된다.

---

### Step 2 — FUNDING.yml 생성 (모든 프레임워크 공통)

`.github/FUNDING.yml` 파일을 생성한다.  
이 파일이 있어야 GitHub 저장소 페이지 우측에 **💛 Sponsor** 버튼이 표시된다.

```yaml
# .github/FUNDING.yml
github: <USERNAME>
```

- `.github/` 디렉토리가 없으면 생성한다.
- `<USERNAME>` 을 실제 GitHub 사용자명으로 치환한다.

---

### Step 3 — 프레임워크별 후원 UI 추가

아래 프레임워크별 지침을 따른다.

---

#### A. Hugo (Hextra / 기타 Hugo 테마)

**A-1. 메인 페이지 (`content/_index.md`) 후원 섹션 추가**

`hugo.yaml`에 `markup.goldmark.renderer.unsafe: true` 가 설정되어 있는지 확인한다.  
없으면 추가한다.

```yaml
# hugo.yaml
markup:
  goldmark:
    renderer:
      unsafe: true
```

`content/_index.md` 하단에 아래 후원 섹션을 추가한다.

```markdown
## 💛 이 자료가 도움이 되셨나요?

이 사이트는 완전 무료로 제공됩니다.  
콘텐츠 개선·유지에 도움을 주시고 싶다면 **GitHub Sponsors**를 통해 후원해 주세요.

<div style="text-align:center; padding:1.5rem; background:linear-gradient(135deg,#fff9c4 0%,#fffde7 100%); border-radius:12px; border:1px solid #f9a825; margin:1rem 0;">
  <p style="font-size:1.05rem; color:#4a4a4a; margin-bottom:1rem;">
    ☕ 커피 한 잔 값의 후원이 콘텐츠 품질 향상에 큰 힘이 됩니다.
  </p>
  <a href="https://github.com/sponsors/<USERNAME>" target="_blank" rel="noopener noreferrer"
     style="display:inline-flex;align-items:center;gap:0.5rem;background:#ea4aaa;color:#fff;padding:0.75rem 1.75rem;border-radius:8px;font-weight:700;text-decoration:none;font-size:1rem;box-shadow:0 2px 8px rgba(234,74,170,0.3);">
    <svg height="20" viewBox="0 0 16 16" fill="currentColor" style="flex-shrink:0;">
      <path d="M4.25 2.5c-1.336 0-2.75 1.164-2.75 3 0 2.15 1.58 4.144 3.365 5.682A20.565 20.565 0 008 13.393a20.561 20.561 0 003.135-2.211C12.92 9.644 14.5 7.65 14.5 5.5c0-1.836-1.414-3-2.75-3-1.373 0-2.609.986-3.029 2.456a.75.75 0 01-1.442 0C6.859 3.486 5.623 2.5 4.25 2.5z"/>
    </svg>
    GitHub Sponsors로 후원하기
  </a>
  <p style="font-size:0.85rem;color:#888;margin-top:0.75rem;">GitHub 계정이 있으면 1회 또는 매월 후원할 수 있습니다.</p>
</div>
```

**A-2. Hugo Hextra 전용 — 네비바 하트 아이콘 링크 추가**

`hugo.yaml`의 `menu.main` 섹션에 추가한다.

```yaml
menu:
  main:
    - name: Sponsor
      url: https://github.com/sponsors/<USERNAME>
      weight: 99          # 가장 우측에 배치
      params:
        icon: heart       # Hextra 내장 하트 아이콘
```

---

#### B. Jekyll

**B-1. `_config.yml` 확인**

사이트 제목·URL 등 기본 설정이 있는지 확인한다.

**B-2. 후원 include 파일 생성 (`_includes/sponsor-button.html`)**

```html
<!-- _includes/sponsor-button.html -->
<div style="text-align:center; padding:1.5rem; background:linear-gradient(135deg,#fff9c4,#fffde7); border-radius:12px; border:1px solid #f9a825; margin:1.5rem 0;">
  <p style="color:#4a4a4a; margin-bottom:1rem;">
    ☕ 이 프로젝트가 도움이 되셨다면 후원을 고려해 주세요.
  </p>
  <a href="https://github.com/sponsors/<USERNAME>" target="_blank" rel="noopener"
     style="display:inline-flex;align-items:center;gap:0.5rem;background:#ea4aaa;color:#fff;padding:0.6rem 1.5rem;border-radius:8px;font-weight:700;text-decoration:none;">
    ♥ GitHub Sponsors로 후원하기
  </a>
</div>
```

**B-3. 메인 페이지 또는 사이드바에 include 삽입**

```liquid
{% include sponsor-button.html %}
```

---

#### C. Docusaurus

**C-1. 커스텀 컴포넌트 생성 (`src/components/SponsorButton.jsx`)**

```jsx
// src/components/SponsorButton.jsx
import React from 'react';

export default function SponsorButton({ username }) {
  return (
    <div style={{
      textAlign: 'center',
      padding: '1.5rem',
      background: 'linear-gradient(135deg, #fff9c4, #fffde7)',
      borderRadius: '12px',
      border: '1px solid #f9a825',
      margin: '1.5rem 0',
    }}>
      <p style={{ color: '#4a4a4a', marginBottom: '1rem' }}>
        ☕ 이 프로젝트가 도움이 되셨다면 후원을 고려해 주세요.
      </p>
      <a
        href={`https://github.com/sponsors/${username}`}
        target="_blank"
        rel="noopener noreferrer"
        style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.5rem',
          background: '#ea4aaa',
          color: '#fff',
          padding: '0.6rem 1.5rem',
          borderRadius: '8px',
          fontWeight: 700,
          textDecoration: 'none',
        }}
      >
        ♥ GitHub Sponsors로 후원하기
      </a>
      <p style={{ fontSize: '0.85rem', color: '#888', marginTop: '0.75rem' }}>
        GitHub 계정이 있으면 1회 또는 매월 후원할 수 있습니다.
      </p>
    </div>
  );
}
```

**C-2. 메인 페이지 MDX에서 사용 (`docs/intro.mdx` 또는 `src/pages/index.js`)**

```mdx
import SponsorButton from '@site/src/components/SponsorButton';

<SponsorButton username="<USERNAME>" />
```

**C-3. Docusaurus 네비바에 후원 링크 추가 (`docusaurus.config.js`)**

```js
themeConfig: {
  navbar: {
    items: [
      // ... 기존 항목
      {
        href: 'https://github.com/sponsors/<USERNAME>',
        label: '♥ Sponsor',
        position: 'right',
      },
    ],
  },
},
```

---

#### D. 일반 HTML 사이트

후원 버튼 HTML 스니펫을 원하는 위치에 삽입한다.

```html
<!-- 후원 섹션 — 원하는 위치에 삽입 -->
<section style="text-align:center; padding:2rem; background:linear-gradient(135deg,#fff9c4,#fffde7); border-radius:12px; border:1px solid #f9a825; margin:2rem auto; max-width:600px;">
  <h3 style="color:#4a4a4a; margin-bottom:0.5rem;">이 프로젝트가 도움이 되셨나요?</h3>
  <p style="color:#666; margin-bottom:1.25rem;">
    ☕ 커피 한 잔 값의 후원이 지속적인 개선에 큰 힘이 됩니다.
  </p>
  <a href="https://github.com/sponsors/<USERNAME>"
     target="_blank" rel="noopener noreferrer"
     style="display:inline-flex;align-items:center;gap:8px;background:#ea4aaa;color:#fff;padding:12px 28px;border-radius:8px;font-weight:700;text-decoration:none;font-size:1rem;box-shadow:0 2px 8px rgba(234,74,170,0.3);">
    <svg height="18" viewBox="0 0 16 16" fill="currentColor">
      <path d="M4.25 2.5c-1.336 0-2.75 1.164-2.75 3 0 2.15 1.58 4.144 3.365 5.682A20.565 20.565 0 008 13.393a20.561 20.561 0 003.135-2.211C12.92 9.644 14.5 7.65 14.5 5.5c0-1.836-1.414-3-2.75-3-1.373 0-2.609.986-3.029 2.456a.75.75 0 01-1.442 0C6.859 3.486 5.623 2.5 4.25 2.5z"/>
    </svg>
    GitHub Sponsors로 후원하기
  </a>
  <p style="font-size:0.8rem;color:#aaa;margin-top:1rem;">
    GitHub 계정이 있으면 1회 또는 매월 후원할 수 있습니다.
  </p>
</section>
```

---

### Step 4 — 검증

아래 사항을 확인한다.

1. **FUNDING.yml 확인**: `cat .github/FUNDING.yml` 으로 내용 확인
2. **빌드 테스트**: 프레임워크별 로컬 빌드 명령어 실행 (예: `hugo`, `bundle exec jekyll serve`, `npm run build`)
3. **후원 링크 유효성**: `https://github.com/sponsors/<USERNAME>` 브라우저 접근 확인
4. **Git 커밋 & 배포**: 변경사항 커밋 후 push

---

### Step 5 — 커밋 메시지 템플릿

```
feat: GitHub Sponsors 후원 기능 추가

- .github/FUNDING.yml 생성 (github: <USERNAME>)
- [메인 페이지/컴포넌트] 후원 섹션 추가
- [네비바/헤더] Sponsor 링크 추가

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

---

## GitHub Sponsors 활성화 전제 조건

후원 링크가 실제 동작하려면 GitHub에서 Sponsors 프로그램 가입이 완료되어 있어야 한다.  
가입 경로: [github.com/sponsors](https://github.com/sponsors) → "Join the waitlist" 또는 "Get started"

가입 완료 여부는 `https://github.com/sponsors/<USERNAME>` 에 접근했을 때 후원 페이지가 표시되는지로 확인한다.

---

## 후원 티어(Tier) 설정 권장

GitHub Sponsors 설정 페이지에서 후원 티어를 만들면 후원자가 금액을 선택하기 쉬워진다.

| 티어 예시 | 금액 | 혜택 설명 |
|---|---|---|
| ☕ Coffee | $3/월 | 감사 인사 |
| 🍕 Pizza | $10/월 | 이름을 README에 표시 |
| 🚀 Supporter | $25/월 | 우선 문의 응답 |

티어는 [github.com/sponsors/<USERNAME>/dashboard](https://github.com/sponsors) 에서 설정한다.
