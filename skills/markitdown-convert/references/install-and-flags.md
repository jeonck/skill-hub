# MarkItDown 설치 옵션과 플래그

출처: [microsoft/markitdown](https://github.com/microsoft/markitdown) README (MIT).
버전에 따라 달라질 수 있으니 확신이 없으면 `markitdown --help`로 확인한다.

## extras — 설치 시 정해야 하는 것

`pip install markitdown` 만으로는 **대부분의 포맷이 동작하지 않는다.** 필요한 extra를 고른다.

| extra | 활성화되는 것 |
| --- | --- |
| `[all]` | 아래 전부 |
| `[pdf]` | PDF |
| `[docx]` | Word |
| `[pptx]` | PowerPoint |
| `[xlsx]` | Excel |
| `[xls]` | 구형 Excel |
| `[outlook]` | Outlook 메시지 |
| `[audio-transcription]` | wav·mp3 음성 전사 |
| `[youtube-transcription]` | YouTube 자막 가져오기 |
| `[az-doc-intel]` | Azure Document Intelligence |
| `[az-content-understanding]` | Azure Content Understanding |

```bash
pip install 'markitdown[all]'
pip install 'markitdown[pdf,docx,pptx]'
```

따옴표를 뺀 `pip install markitdown[pdf]`는 zsh에서 글롭으로 해석돼 실패한다.

소스 설치:

```bash
pip install -e 'packages/markitdown[all]'
```

## 지원 입력 포맷

PDF · PowerPoint · Word · Excel · 이미지(EXIF 메타데이터, OCR) · 오디오(EXIF, 음성 전사) ·
HTML · 텍스트 계열(CSV, JSON, XML) · ZIP(내용물 순회) · EPUB · YouTube URL.

## CLI 플래그

| 플래그 | 의미 |
| --- | --- |
| `-o <file>` | 출력 파일 지정 (없으면 stdout) |
| `-d` | Azure Document Intelligence 사용 |
| `-e <endpoint>` | Document Intelligence 엔드포인트 |
| `--use-cu` | Azure Content Understanding 사용 |
| `--cu-endpoint <url>` | Content Understanding 엔드포인트 |
| `--list-plugins` | 설치된 서드파티 플러그인 목록 |
| `--use-plugins` | 플러그인 활성화 (기본 비활성) |

```bash
markitdown in.pdf -o out.md
markitdown in.pdf -o out.md -d -e "<docintel_endpoint>"
export MARKITDOWN_DOCINTEL_ENDPOINT="<docintel_endpoint>"   # 이후 -d 만으로 충분
markitdown in.pdf --use-cu --cu-endpoint "<cu_endpoint>"
```

## Docker

로컬에 파이썬 환경을 만들고 싶지 않을 때.

```bash
docker build -t markitdown:latest .
docker run --rm -i markitdown:latest < input.pdf > output.md
```

stdin/stdout만 쓰므로 확장자 힌트가 없다. 추론이 애매한 파일은 로컬 CLI 쪽이 낫다.

## Python API

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)
result = md.convert("test.xlsx")
print(result.markdown)
```

이미지 설명·OCR에 LLM을 붙일 때 — `markitdown-ocr` 플러그인이 같은 인자 규약을 쓴다.

```python
pip install markitdown-ocr
pip install openai            # 또는 OpenAI 호환 클라이언트
```

Content Understanding은 파일 종류에 따라 분석기를 자동 선택하고, 추출된 필드를 **YAML
front matter**로 붙여 준다.

```python
md = MarkItDown(cu_endpoint="<cu_endpoint>")
md.convert("report.pdf")    # 문서 → prebuilt-documentSearch
md.convert("meeting.mp4")   # 비디오 → prebuilt-videoSearch
md.convert("call.wav")      # 오디오 → prebuilt-audioSearch
```

## 세 경로 비교

| 항목 | 기본 변환기 | Document Intelligence | Content Understanding |
| --- | --- | --- | --- |
| 방식 | 오프라인, 포맷별 추출 | 클라우드 레이아웃 추출 | 클라우드 멀티모달 추출 |
| 구조화 필드 | 없음 | 이 통합에서는 노출 안 됨 | YAML front matter로 제공 |
| 커스텀 분석기 | 없음 | 설정 불가 | `cu_analyzer_id` 지원 |
| 오디오·비디오 | 기본 오디오만, 비디오 없음 | 미지원 | 오디오·비디오 지원 |
| 비용 | 로컬 컴퓨트만 | Azure API 과금 | Azure API 과금 |

## 자주 막히는 지점

| 증상 | 원인 | 조치 |
| --- | --- | --- |
| 출력이 비었거나 수백 바이트 | 스캔 PDF(이미지 전용) | Document Intelligence 또는 markitdown-ocr |
| `No converter attempted` 류 오류 | 해당 extra 미설치 | 맞는 extra로 재설치 |
| 표가 문단으로 뭉개짐 | 원본이 표가 아니라 탭 정렬 텍스트 | 원본 확인, 변환 문제가 아님 |
| zsh에서 설치 실패 | 대괄호 글롭 | 따옴표로 감싼다 |
| 파이프 입력에서 포맷 오인 | 확장자 힌트 없음 | 파일 경로를 직접 넘긴다 |
