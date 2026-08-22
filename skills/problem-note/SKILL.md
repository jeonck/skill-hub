---
name: problem-note
description: ICT 장애·문제 기록을 ict-brain(Quartz v5 세컨드브레인) 규칙에 맞는 문제 문서로 작성/승격한다. 사용자가 장애 상황·에러 로그·트러블슈팅 내용을 던지며 "문제 노트 써줘", "이거 기록해줘", "inbox 승격", "problem 문서 만들어줘"라고 하거나, content/problems/ 아래 문서를 쓰거나 고칠 때 사용한다. 개념 노트(concepts/)·MOC(maps/) 작성과 공개 전 마스킹 점검도 포함한다.
---

# 문제 노트 작성

대상 저장소는 Quartz v5 기반 `ict-brain` 구조다. 저장소가 있으면 `content/meta/` 네 문서(capture-workflow, tag-taxonomy, note-linking-rules, publishing-checklist)가 원본 규칙이니 먼저 읽는다. 아래는 그 요약이다.

## 승격 판단

던져진 메모를 전부 문서로 만들지 않는다. 기준 하나: **6개월 뒤에 또는 다른 사람이 이 문제를 다시 만날 가능성이 있는가.** 없으면 만들지 말고 그 이유를 한 줄로 말한다. 애매하면 inbox에 두라고 하고 끝낸다.

## 파일

- 경로: `content/problems/<영문-케밥-슬러그>.md`
- 파일명은 영문 케밥케이스, **한번 정하면 바꾸지 않는다** (링크·URL이 깨진다). 제목은 한글.
- 제목은 결론이 아니라 **증상**으로 단다. 미래의 검색은 증상에서 출발한다.

## Front matter

```yaml
---
title: "증상을 한 줄로 — 검색할 때 떠올릴 말로"
date: YYYY-MM-DD
tags:
  - target/...
  - layer/...
  - symptom/...
status: investigating | solved | wontfix
severity: P1 | P2 | P3
env: "제품 버전 / 배포 형태 / 규모"
symptom: "에러 메시지 원문 한 줄"
root_cause: "한 줄 요약. 미확정이면 비워둠"
---
```

새 front matter 키를 추가하면 `quartz.config.yaml`의 `note-properties` → `includedProperties`에도 넣어야 화면에 나온다.

## 태그 — 세 축, 축마다 최대 2개

- `target/` 무엇에서 터졌나 — postgres, pgbouncer, kubernetes, nginx, kafka, redis, aws-rds, istio … (늘어나도 되는 유일한 축)
- `layer/` 원인이 최종적으로 어디였나 (증상 아님) — network, storage, database, compute, auth, config, dns, observability, capacity. 12개 초과 금지
- `symptom/` 어떤 모양이었나 — outage, intermittent-failure, latency, resource-exhaustion, data-inconsistency, silent-failure, deploy-failure

축 밖 태그는 운영 문서용 `meta` 하나만. 기존 태그로 못 덮을 때만 새로 만든다. 축마다 3개 이상 달리면 문서를 쪼개라는 신호다.

## 본문 섹션 (템플릿 `content/templates/problem-template.md`)

증상 / 환경 / 조사 경로 / 원인 / 조치 / 재발 방지 / 남은 의문 / 관련.

- **에러 메시지는 원문 그대로.** 요약·번역 금지. 코드블록에 넣는다. 검색성의 핵심.
- 증상에 "언제부터 / 재현 조건 / 재현 안 되는 조건" 세 줄을 채운다.
- 환경 표의 **"직전 변경" 칸을 비우지 않는다.** 원인의 절반이 여기서 나온다.
- 조사 경로에는 **기각된 가설도 남긴다** (가설 → 확인 방법 → 기각/채택).
- 조치는 복사해서 바로 쓸 수 있는 명령/설정으로.
- 재발 방지는 감지 / 예방 / 남은 부채 셋으로.
- **남은 의문이 비어 있으면 대개 이해가 아니라 회피다.** 모르는 건 모른다고 쓴다.

## 링크 — 문서당 최소 3개

상위 개념 1개 + 비슷한 문제 1~2개 + 허브(MOC) 1개. 상위 개념이 없으면 `content/concepts/`에 세 줄짜리라도 만든다. 허브는 역방향으로 — `content/maps/` 문서를 열어 줄을 추가한다.

- 내부 링크는 전부 위키링크 `[[slug|표시 텍스트]]`. 마크다운 링크는 외부 링크 전용.
- 링크는 하단 "관련" 목록이 아니라 **문장 안에** 건다. 왜 연결됐는지가 같이 남는다.

## 공개 전 마스킹 — 작성 시점에 한다

전체 공개 전제. 나중에 지워도 커밋 이력에 남는다.

절대 금지: 고객사·기관 실명이나 특정 가능한 조합, 자격증명 일체, 내부 호스트명·사설 IP·내부 도메인·계정 ID, 원본 로그 통짜 붙여넣기, 계약/단가/인력, 미패치 취약점 재현 방법.

지우지 말고 **모양을 유지한 채 치환한다**: `prod-db-seoul-03.internal` → `db-primary.example.internal`, `10.42.7.118` → `10.0.0.10`, `AKIA...` → `AKIA<REDACTED>`, "A사" → "국내 커머스 사업자". 에러 원문은 남기고 그 안의 호스트명·ID만 바꾼다.

판단이 애매하면: **"이 문서를 그 고객사 담당자가 읽어도 괜찮은가."** 멈칫하면 덜 된 것이다. 일반화가 불가능한 사례는 발행하지 않는다.

문서를 쓴 뒤 이걸 돌린다.

```bash
grep -rEn '(AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY|password\s*[:=]\s*\S+)' content/
```
