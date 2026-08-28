---
title: "PgBouncer 뒤에서 prepared statement already exists가 간헐적으로 뜬다"
date: 2026-03-14
tags:
  - target/pgbouncer
  - target/postgres
  - layer/config
  - symptom/intermittent-failure
status: solved
severity: P2
env: "PgBouncer 1.18 / PostgreSQL 15 / Spring Boot 3.2 + HikariCP, 앱 12 파드"
symptom: "ERROR: prepared statement \"S_3\" already exists"
root_cause: "transaction 풀링에서 서버 커넥션이 재사용되는데 드라이버가 서버 측 prepared statement를 캐시함"
---

## 증상

배포 직후가 아니라 **트래픽이 오르면** 특정 API에서 5xx가 섞여 나온다. 재현율은
전체 요청의 0.5% 안팎이고, 같은 요청을 다시 보내면 대개 성공한다.

```
org.postgresql.util.PSQLException: ERROR: prepared statement "S_3" already exists
```

부하가 낮은 새벽에는 한 건도 나오지 않는다.

## 환경

- PgBouncer 1.18, `pool_mode = transaction`
- PostgreSQL 15, `max_connections = 200`
- Spring Boot 3.2, PostgreSQL JDBC 42.7, HikariCP 파드당 10 커넥션 × 12 파드

## 조사 경로

1. 애플리케이션 로그에서 실패 요청의 공통점을 찾음 → 특정 API가 아니라 **JPA가
   같은 쿼리를 5회 이상 실행한 뒤** 발생. JDBC 드라이버의 `prepareThreshold` 기본값이 5다.
2. PgBouncer를 우회해 PostgreSQL에 직접 붙여 부하 재현 → **재현되지 않음**.
   PgBouncer 구간의 문제로 좁혀짐.
3. `SHOW POOLS` 로 확인 → `cl_active`가 `sv_active`보다 훨씬 큼. 클라이언트 커넥션
   여러 개가 서버 커넥션 하나를 돌려쓰고 있다.
4. `pool_mode`를 `session`으로 임시 변경 → 오류 사라짐. 원인 구간 확정.

## 원인

`pool_mode = transaction`은 **트랜잭션이 끝나면 서버 커넥션을 다른 클라이언트에게
넘긴다.** 그런데 JDBC 드라이버는 같은 쿼리가 `prepareThreshold`(기본 5)회를 넘으면
서버 측 prepared statement로 승격하고, 그 이름(`S_3`)을 **클라이언트 커넥션 기준으로**
기억한다.

클라이언트 A가 `S_3`을 만들어 둔 서버 커넥션이 클라이언트 B에게 넘어가면, B는 자기가
만든 적 없는 `S_3`을 다시 만들려 하고 이름이 충돌한다. 트래픽이 낮으면 서버 커넥션이
남아돌아 재사용이 거의 일어나지 않으므로 **저부하에서는 재현되지 않는다.**

## 조치

JDBC에서 서버 측 prepared statement를 끄는 쪽을 택했다. `session` 풀링은 커넥션
절약이라는 PgBouncer 도입 목적 자체를 되돌리기 때문이다.

```
jdbc:postgresql://pgbouncer:6432/app?prepareThreshold=0
```

적용 후 24시간 동안 해당 오류 0건. 응답시간 P95는 변화가 관측되지 않았다.

**대안으로 검토했던 것**

| 대안 | 채택하지 않은 이유 |
| --- | --- |
| `pool_mode = session` | 커넥션 재사용이 사라져 PgBouncer 도입 목적이 무너짐 |
| PgBouncer 1.21+ 로 올려 `max_prepared_statements` 사용 | 유효한 해법이나 업그레이드 일정이 필요해 후속 과제로 분리 |
| 애플리케이션에서 쿼리 캐시 비활성화 | 범위가 넓고 성능 영향이 큼 |

## 재발 방지

- 데이터소스 URL에 `prepareThreshold=0`을 넣는 것을 공용 설정 템플릿에 반영
- PgBouncer 앞단에 붙는 신규 서비스는 체크리스트에 이 항목 추가
- `SHOW POOLS`의 `cl_active`/`sv_active` 비율을 대시보드에 노출해 재사용 강도를 관측

## 남은 의문

- PgBouncer 1.21의 프로토콜 수준 prepared statement 지원으로 올리면 `prepareThreshold`를
  되돌려 성능 이득을 볼 수 있는지 — 벤치마크 미실시
- 같은 구조인 다른 서비스가 왜 오류를 내지 않았는지. 쿼리 반복 횟수가 임계에 못 미쳤을 것으로 추정하나 미확인

## 관련

- [[connection-pooling-modes]]
- [[postgres-max-connections-tuning]]
