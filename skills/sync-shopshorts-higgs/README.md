# sync-shopshorts-higgs

상품 URL 하나로 한국형 쇼핑 숏츠를 만드는 Claude Code 스킬입니다.
Higgsfield 마케팅 스튜디오 MCP를 사용해 상품 크롤링부터 영상 생성·검수까지 자동화합니다.

## 특징

- **한국인 전용** — 등장인물은 한국인 남녀 고정, 대사·음성·자막 모두 한국어
- **타깃 페르소나 분석** — 상품 카테고리·가격대·페이지 신호로 등장인물의 성별·나이대를 자동 추천
- **검증된 대본 템플릿 5종** — 조회수 상위 한국 쇼핑 숏츠 12편을 분해해 추출한 구조 (성능 시험형 / 가격 충격형 / 문제 해결형 / 조합형 / BEST 리스트형)
- **씬 구조도 승인 게이트** — 생성 전 씬별 표(시간/화면/대사/등장인물/생성 방식)를 보여주고 승인 후에만 실행
- **다중 영상 세트 전략** — 2개(A/B 훅 테스트), 3개(훅 다변화), 4개(페르소나 매트릭스)
- **프레임 검증 검수** — 생성 후 프레임을 추출해 한국인 여부·깨진 텍스트를 확인하고 통과/탈락 판정

## 설치

```bash
git clone https://github.com/aisyncclub/sync-shopshorts-higgs.git ~/.claude/skills/sync-shopshorts-higgs
```

Claude Code 재시작 후 `/sync-shopshorts-higgs <상품 URL>`로 호출합니다.

## 요구사항

- Claude Code + Higgsfield MCP 연결 (마케팅 스튜디오 도구 포함)
- Higgsfield 크레딧 (영상 1개당 약 75크레딧)
- 검수 단계용 `ffmpeg`

## 워크플로우

```
Phase 1. 상품 등록      상품 URL 크롤링 → 상품명·이미지 확보
Phase 2. 사실 검증      검증된 사실 / 금지 주장 분리 + 페르소나 분석
Phase 3. 개수·연출 선택  제작 개수(1~4) + 템플릿×프리셋 추천
Phase 4. 씬 구조도      대본 + 씬별 표 → ⛔ 승인 게이트
Phase 5. 생성 실행      Higgsfield marketing_studio_video 생성
Phase 6. 검수           프레임 검증 + 체크리스트 판정
```

## 파일 구조

```
sync-shopshorts-higgs/
├── SKILL.md                        # 워크플로우 본문
└── references/
    ├── script-templates.md         # 대본 템플릿 5종 + 씬 구분표
    ├── persona-mapping.md          # 카테고리별 페르소나 매핑
    ├── preset-mapping.md           # 프리셋 매핑 + 다중 영상 전략
    └── quality-checklist.md        # 검수 체크리스트
```

## License

MIT
