# CCNP/CCIE 콘텐츠 작성 상세 가이드

## 프로젝트 정보

- **레포**: https://github.com/jeonck/ccnp-ccie
- **로컬 경로**: /Users/mac/ws/claude/ccnp-ccie
- **사이트**: https://jeonck.github.io/ccnp-ccie/
- **프레임워크**: Docusaurus v3 + @docusaurus/theme-mermaid
- **배포**: main 브랜치 push → GitHub Actions → gh-pages 자동 배포

---

## 완성된 문서 예시 (intro.md 구조)

```markdown
---
sidebar_position: 1
title: 문서 제목
---

# 문서 제목
**Full English Name**

## 정의

한 문장 정의. **핵심 키워드** 볼드, 표준 번호 포함.

## 특징

- **(키워드1)** 설명 한 줄
- **(키워드2)** 설명 한 줄
- **(키워드3)** 설명 한 줄

## 왜 필요한가?

문제 상황 설명 + Mermaid Before/After 또는 공격 시나리오

## 구성 요소

Mermaid flowchart + 표/리스트 설명

## 동작 흐름

Mermaid sequenceDiagram 또는 상태 전이 flowchart

## [기술 A vs 기술 B] 비교

마크다운 표

## 설정 및 검증

```bash
! Cisco IOS 설정 예시
명령어  ! 설명
```

## CCNP/CCIE 시험 포인트

- 기본값, 타이머, 자주 틀리는 포인트 3~7개
```

---

## Mermaid 규칙 (엄수 필요)

### 1. 줄바꿈 — `<br/>` 만 허용

```
❌ A["라벨\n두 번째 줄"]
✅ A["라벨<br/>두 번째 줄"]
```

### 2. subgraph 라벨 — 이모지 금지

```
❌ subgraph GOV["🏛️ 거버넌스 영역"]
✅ subgraph GOV["거버넌스 영역"]
```

### 3. 노드 라벨 — 반드시 `""` 로 감싸기

```
❌ A --> B
✅ A["출발"] --> B["도착"]
```

### 4. `&` 체인 화살표 — 별도 줄로 분리

```
❌ OSPF --> R1 & R2 & R3
✅ OSPF --> R1
   OSPF --> R2
   OSPF --> R3
```

### 5. 볼드 텍스트 — 따옴표는 마커 밖에

```
❌ **"따옴표가 안에"**
✅ "**따옴표가 밖에**"
```

### 6. MDX 주석 — HTML 주석 금지

```
❌ <!-- HTML 주석 — MDX 오류 발생 -->
✅ {/* MDX 주석 */}
```

---

## Mermaid 다이어그램 타입 선택 기준

| 상황 | 사용 타입 | 예시 |
|------|-----------|------|
| 개념 간 관계·구조 | `flowchart TD` | 구성 요소 맵 |
| 순서·흐름·Before-After | `flowchart LR` | 스위칭 동작, 상태 전이 |
| 프로토콜 협상·핸드셰이크 | `sequenceDiagram` | LACP 협상, DHCP 흐름 |
| 상태 머신 | `flowchart LR` | STP 포트 상태 전이 |
| 네트워크 토폴로지 | `flowchart TD` 또는 `LR` | 3-Tier 구조, VPN 토폴로지 |

---

## 색상 팔레트 (역할별 일관 적용)

```mermaid
style A fill:#2563EB,stroke:#1D4ED8,color:#fff   ! 핵심/주요 요소 — 파랑
style B fill:#7C3AED,stroke:#6D28D9,color:#fff   ! 보조/연관 요소 — 보라
style C fill:#EA580C,stroke:#C2410C,color:#fff   ! 경고/장애/위협 — 주황
style D fill:#16A34A,stroke:#15803D,color:#fff   ! 정상/성공/허용 — 녹색
style E fill:#0891B2,stroke:#0E7490,color:#fff   ! 정보/서비스 — 청록
style F fill:#1E3A5F,stroke:#1E3A5F,color:#fff   ! 전체 구조/루트 — 네이비
style G fill:#DC2626,stroke:#B91C1C,color:#fff   ! 위험/차단/공격자 — 빨강
style H fill:#6B7280,stroke:#4B5563,color:#fff   ! 비활성/레거시 — 회색
```

연한 배경색 (subgraph):
- 파랑 계열: `fill:#EFF6FF,stroke:#2563EB`
- 녹색 계열: `fill:#F0FDF4,stroke:#16A34A`
- 주황 계열: `fill:#FFF7ED,stroke:#EA580C`
- 빨강 계열: `fill:#FEF2F2,stroke:#DC2626`

---

## Cisco IOS 설정 작성 규칙

1. `bash` 코드 블록 사용
2. 모드 프롬프트 표시: `SW(config)#`, `SW(config-if)#`, `SW#`
3. 인라인 주석 `!`으로 각 명령어 설명
4. 설정 뒤에 반드시 검증 명령어(`show`) 포함
5. 복잡한 설정은 섹션 코멘트(`! ===== 섹션명 =====`)로 구분

```bash
! 기본 설정 예시
SW(config)# vlan 10                      ! VLAN 생성
SW(config-vlan)# name ENGINEERING        ! 이름 지정

! 검증
SW# show vlan brief
SW# show interfaces trunk
```

---

## 토픽별 섹션 선택 가이드

### 프로토콜 (OSPF, EIGRP, BGP, STP 등)
필수: 정의, 특징, 왜 필요한가, 구성 요소, 동작 흐름, 비교, 설정·검증, 시험 포인트

### 기능/서비스 (VLAN, NAT, DHCP, QoS 등)
필수: 정의, 특징, 왜 필요한가, 동작 흐름, 설정·검증, 시험 포인트
선택: 구성 요소 (개념이 많을 때), 비교 (유사 기술 있을 때)

### 보안 기능 (Port Security, DAI, ACL 등)
필수: 정의, 특징, 왜 필요한가(공격 시나리오), 동작 흐름(방어 메커니즘), 설정·검증, 시험 포인트
선택: 비교 (여러 보안 기능 함께 설명 시)

### 아키텍처/설계 (SD-WAN, Network Design 등)
필수: 정의, 특징, 구성 요소, 비교, 활용 시나리오, 시험 포인트
선택: 동작 흐름, 설정·검증

---

## 빌드 & 배포 절차

```bash
# 1. 빌드 검증 (Mermaid/MDX 오류 확인)
cd /Users/mac/ws/claude/ccnp-ccie
npm run build

# 2. 커밋 & 푸시
git add docs/<topic>/
git commit -m "docs: <토픽> 문서 작성"
git push
# → GitHub Actions가 자동으로 gh-pages 배포
```

---

## 자주 발생하는 오류 & 해결

| 오류 | 원인 | 해결 |
|------|------|------|
| MDX parse error | `<!-- -->` 주석 사용 | `{/* */}` 로 변경 |
| Mermaid 렌더 실패 | 노드 라벨 미따옴표 | `A["라벨"]` 형식으로 수정 |
| Mermaid 렌더 실패 | `\n` 줄바꿈 | `<br/>` 로 교체 |
| Broken link | docs/ 경로 불일치 | `show broken-links` → 경로 확인 |
| Build 실패 | 잘못된 frontmatter | `---` 구분자 및 필드명 확인 |
