---
name: markitdown-convert
description: microsoft/markitdown으로 PDF·Word·PowerPoint·Excel·이미지·오디오·HTML·CSV/JSON/XML·ZIP·EPUB·YouTube URL을 LLM이 읽기 좋은 Markdown으로 변환한다. CLI, 파이프, Python API, 폴더 일괄 변환, Azure Document Intelligence·Content Understanding 경로까지 다룬다. "이 PDF 마크다운으로", "문서 텍스트만 뽑아줘", "docx/pptx/xlsx를 md로", "스캔 PDF에서 표 추출", "RAG 넣게 문서 변환해줘", "markitdown 설치/설정", "폴더 통째로 변환" 같은 요청에 사용한다. 설치는 extras 선택이 핵심이다 — references/install-and-flags.md 참조. 이미 마크다운인 파일 편집, 웹페이지 스크래핑(WebFetch 사용), 마크다운을 다른 포맷으로 되돌리는 변환은 대상이 아니다.
---

# MarkItDown 문서 변환

[microsoft/markitdown](https://github.com/microsoft/markitdown)은 문서를 **LLM이 소비할**
Markdown으로 바꾸는 Python 도구다. 사람이 읽을 고품질 변환이 아니라 **구조(제목·목록·표·링크)
보존**이 목적이다. 이 차이가 기대치를 정한다 — 레이아웃이 흐트러져도 표의 셀 값이 살아 있으면
성공이다.

설치 옵션·CLI 플래그 전체·포맷별 함정은 [`references/install-and-flags.md`](references/install-and-flags.md)에 있다.

## 먼저 확인

```bash
markitdown --version 2>/dev/null || echo "미설치"
```

미설치면 **extras를 먼저 정한다.** `pip install markitdown` 만으로는 PDF·docx가 안 된다.

```bash
pip install 'markitdown[all]'          # 전부 (권장, 무겁다)
pip install 'markitdown[pdf,docx,xlsx]' # 필요한 것만
```

## 기본 변환

```bash
markitdown report.pdf -o report.md     # 파일로
markitdown report.pdf > report.md      # 리다이렉트도 동일
cat report.pdf | markitdown            # 파이프 (확장자 힌트가 없어 추론이 약해진다)
```

`-o`를 쓴다. 리다이렉트는 변환이 실패해도 빈 파일이 남아 성공처럼 보인다.

## 폴더 일괄 변환

markitdown에는 재귀 옵션이 없다. 셸에서 돈다.

```bash
find docs -type f \( -name '*.pdf' -o -name '*.docx' -o -name '*.pptx' \) -print0 |
  while IFS= read -r -d '' f; do
    out="${f%.*}.md"
    markitdown "$f" -o "$out" || echo "FAILED: $f" >&2
  done
```

`|| echo FAILED`를 반드시 붙인다. 한 파일이 깨져도 나머지를 계속 돌리고, 실패 목록이 남는다.

## 변환 후 반드시 확인할 것

변환은 자주 **조용히 열화된다.** 성공 종료 코드는 품질을 보증하지 않는다.

| 확인 | 방법 | 실패 신호 |
| --- | --- | --- |
| 빈 출력 | `wc -c out.md` | 수백 바이트 → 스캔 PDF일 가능성 |
| 표 보존 | `grep -c '^|' out.md` | 원본에 표가 있는데 0 |
| 이미지 텍스트 | 본문 검색 | 스캔 문서인데 텍스트가 없음 |

스캔 PDF(이미지만 있는 PDF)는 기본 변환기가 **텍스트를 하나도 못 뽑는다.** 이때가
Document Intelligence나 OCR 플러그인을 꺼낼 지점이지, 재시도할 지점이 아니다.

## 품질을 올려야 할 때

| 상황 | 수단 |
| --- | --- |
| 스캔 PDF·복잡한 표 | Azure Document Intelligence (`-d -e <endpoint>`) |
| 오디오·비디오, 필드 추출 | Azure Content Understanding (`--use-cu`) |
| 문서 속 이미지의 텍스트 | `markitdown-ocr` 플러그인 + LLM 비전 |
| 이미지 설명 필요 | Python API에 `llm_client`·`llm_model` 전달 |

Azure 경로는 **과금되는 클라우드 호출**이다. 먼저 로컬 변환을 시도해 부족함을 확인한 뒤에
제안한다. 엔드포인트·키를 사용자에게 임의로 요구하지 않는다.

## Python API

셸 한 줄로 끝나면 CLI를 쓴다. 다음일 때만 Python으로 간다 — 결과를 바로 후처리, 이미지 설명
LLM 연결, 스트림·바이트 처리.

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)
result = md.convert("report.xlsx")
print(result.markdown)
```

## 보안 — 신뢰할 수 없는 입력

markitdown은 **현재 프로세스 권한으로 I/O를 수행한다.** `convert()`는 로컬 파일, 원격 URI,
바이트 스트림을 모두 받는 관대한 함수라, 입력 경로를 통제하지 못하면 의도치 않은 곳을 읽는다.

- 로컬 파일만 다루면 `convert()` 대신 **`convert_local()`** 을 쓴다
- URI를 직접 통제하려면 `requests.get()`을 직접 호출하고 `convert_response()`에 넘긴다
- 최대 통제가 필요하면 스트림을 열어 `convert_stream()`에 넘긴다
- 사용자·외부 시스템이 경로를 정하는 상황이면 변환 전에 경로·스킴·네트워크 목적지를 제한한다

플러그인은 기본 비활성이다. `--use-plugins`로 켜는 것은 **서드파티 코드 실행**이므로,
설치된 플러그인을 `markitdown --list-plugins`로 확인하고 사용자에게 알린 뒤 켠다.

## 하지 말 것

- 실패를 재시도로 덮지 않는다. 빈 출력은 대개 포맷 문제(스캔 PDF·미설치 extra)이지 일시 오류가 아니다
- `pip install markitdown`만 하고 PDF 변환을 시도하지 않는다 — `[pdf]` extra가 필요하다
- 변환 결과를 확인 없이 "완료"라고 보고하지 않는다. 위 표 세 줄은 항상 돌린다
- 이미 텍스트인 `.md`·`.txt`를 굳이 통과시키지 않는다
