#!/usr/bin/env python3
"""Daily diary pipeline (예시 도메인: 매일 영어 문장 일기).

input/sentence.md 에서 오늘의 항목(들)을 읽어, 항목마다 Claude로 콘텐츠를 생성해
Hugo 포스트로 저장한다. 코드블록 안에 여러 줄을 적으면 줄마다 별도 포스트가 생성된다.
이미 게시에 사용된 항목(텍스트 해시 기준)은 다시 나타나도 건너뛴다. 입력이 비어 있으면
FALLBACK_QUOTES 풀에서 그날의 항목을 대신 사용한다.

Usage:
    python pipeline/generate.py [--dry-run]

Env:
    JUDGE_BACKEND            "claude-code" | "api" (기본: 자동 — claude CLI가 있으면
                             claude-code, 없으면 api)
    CLAUDE_CODE_OAUTH_TOKEN  claude-code 백엔드 CI 인증 (claude setup-token으로 발급,
                             로컬은 claude 로그인 세션 사용)
    ANTHROPIC_API_KEY        api 백엔드 필수
    CLAUDE_MODEL             생성 모델 (기본 claude-sonnet-4-6)

새 도메인에 맞게 커스터마이즈할 곳은 아래 "=== 도메인 설정 ===" 블록 하나뿐이다.
지금 채워진 내용은 "매일 영어 문장으로 일기 쓰기" 도메인의 실제 동작 예시이므로,
새 도메인에서는 이 블록 전체를 그 도메인에 맞는 내용으로 다시 쓴다(직접 편집).
GENERATE_PROMPT 안의 JSON 스키마에서 이중 중괄호 `{{` `}}` 는 Python str.format()이
리터럴 `{` `}` 를 출력하게 하는 이스케이프이므로, 스키마 부분을 고칠 때도 이 이중
중괄호 규칙을 그대로 유지해야 한다 — `{sentence}` / `{note}` 두 자리만 단일 중괄호.
아래쪽 엔진 코드(해시 dedup, claude-code/api 백엔드 전환, Hugo 포스트 작성 골격)는
실전 검증된 로직이므로 그대로 둔다.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SENTENCE_FILE = ROOT / "input" / "sentence.md"
STATE_FILE = ROOT / "pipeline" / "state.json"
CONTENT_DIR = ROOT / "content" / "posts"

KST = timezone(timedelta(hours=9))

# ============================== 도메인 설정 =================================
# 이 블록만 새 프로젝트 주제에 맞게 교체한다. 아래 엔진 코드는 건드릴 필요 없다.

# input/sentence.md 한 줄이 비어 있을 때 대신 쓰는 항목 풀. {"text": ..., "author": ...}
# author를 빈 문자열로 두면 출처 표시 없이 순수 텍스트만 사용된다.
# 이 풀을 완전히 비워두면(= []) 폴백을 비활성화할 수 있다 — 그 경우 입력이 없는 날은
# 그냥 아무 포스트도 생성되지 않는다.
FALLBACK_QUOTES = [
    {"text": "What does not kill me makes me stronger.", "author": "Friedrich Nietzsche"},
    {"text": "He who has a why to live can bear almost any how.", "author": "Friedrich Nietzsche"},
    {"text": "You have power over your mind, not outside events. Realize this, and you will find strength.", "author": "Marcus Aurelius"},
    {"text": "Luck is what happens when preparation meets opportunity.", "author": "Seneca"},
    {"text": "It's not what happens to you, but how you react to it that matters.", "author": "Epictetus"},
    {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"},
    {"text": "A journey of a thousand miles begins with a single step.", "author": "Lao Tzu"},
    {"text": "We are what we repeatedly do. Excellence, then, is not an act, but a habit.", "author": "Aristotle"},
    {"text": "The only true wisdom is in knowing you know nothing.", "author": "Socrates"},
    {"text": "Do not go where the path may lead, go instead where there is no path and leave a trail.", "author": "Ralph Waldo Emerson"},
]

# Claude에게 부여할 역할/톤
SYSTEM_PROMPT = """당신은 영어 학습자를 위한 다이어리 작문 도우미다. 사용자가 오늘의 영어
문장을 입력하면, 그 문장을 자연스럽게 활용한 짧은 영어 일기와 학습에 도움이 되는 응용
문장을 만든다. 일기는 실제 일상적인 상황처럼 자연스럽게 쓰고, 과장하거나 억지로 늘리지
않는다."""

# {sentence} / {note} 두 자리를 반드시 유지한 채 지시문만 도메인에 맞게 바꾼다.
# 모델 응답은 반드시 아래 JSON 스키마를 그대로 따라야 한다 — write_post()가 이 키들을
# 그대로 사용한다. 필드 자체를 늘리려면 write_post()도 함께 수정한다.
GENERATE_PROMPT = """아래 "오늘의 문장"을 반드시 활용해서(그대로 포함하거나 자연스럽게
녹여서) 짧은 영어 일기를 작성하라.{note} 반드시 다음 JSON 형식으로만 답하라. 다른 텍스트
금지.

{{"title_ko": "일기 주제를 요약한 한국어 제목 한 줄",
 "body": "5~7문장 분량의 영어 일기 전체 텍스트. 자연스러운 구어체 일기 톤",
 "body_translation": "body의 자연스러운 한국어 번역",
 "variations": [
   {{"text": "오늘의 문장과 비슷한 문형/어휘를 재사용한 응용 문장 1", "translation": "한국어 해석"}},
   {{"text": "응용 문장 2 (문형은 같지만 다른 상황)", "translation": "한국어 해석"}}
 ],
 "tags": ["kebab-case-태그", "최대 3개"]}}

오늘의 문장: {sentence}"""

QUOTE_NOTE = (
    " 이 문장은 오늘 사용자가 직접 쓴 문장이 아니라 {author}의 명언이다."
    " 이 명언을 오늘 일상 속에서 문득 떠올리게 된 것처럼, 명언과 어울리는"
    " 소소한 상황을 상상해서 일기를 써라."
)

# 포스트 본문 섹션 제목
HEADING_INPUT = "오늘의 문장"
HEADING_INPUT_QUOTE = "오늘의 명언"
HEADING_BODY = "일기 (Diary)"
HEADING_VARIATIONS = "응용 문장 (Applied Sentences)"

# ============================ 도메인 설정 끝 =================================


def log(msg: str) -> None:
    print(msg, flush=True)


def sentence_hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
    return (slug or "diary")[:60].rstrip("-")


def read_sentences() -> list[str]:
    """input/sentence.md 에서 사용자가 적은 항목들을 읽는다. 없으면 빈 리스트."""
    if not SENTENCE_FILE.exists():
        log(f"오류: {SENTENCE_FILE} 파일이 없습니다")
        sys.exit(1)
    text = SENTENCE_FILE.read_text(encoding="utf-8")
    fenced = re.search(r"```[a-zA-Z]*\n(.*?)```", text, re.DOTALL)
    body = fenced.group(1) if fenced else text
    sentences = []
    for line in body.splitlines():
        line = line.strip()
        if line and not line.startswith(("<!--", "-", "#")):
            sentences.append(line)
    return sentences


def fallback_quote_item(today) -> dict | None:
    """input이 비어 있을 때 사용할 항목 — 날짜 기준으로 풀을 순환 선택."""
    if not FALLBACK_QUOTES:
        return None
    idx = today.timetuple().tm_yday % len(FALLBACK_QUOTES)
    quote = FALLBACK_QUOTES[idx]
    return {
        "text": quote["text"],
        "source": quote.get("author") or None,
        # 날짜를 해시에 포함 — 같은 항목이 몇 주 뒤 다시 나와도 새로 게시되도록
        "dedup_key": sentence_hash(f"{today.isoformat()}::{quote['text']}"),
    }


def build_queue(sentences: list[str], today) -> list[dict]:
    if sentences:
        return [
            {"text": s, "source": None, "dedup_key": sentence_hash(s)}
            for s in sentences
        ]
    fallback = fallback_quote_item(today)
    return [fallback] if fallback else []


class FatalAPIError(Exception):
    """재시도가 무의미한 오류(크레딧 부족, 인증 실패) — 실행 전체 중단."""


def is_fatal_api_error(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(marker in msg for marker in (
        "credit balance", "authenticat", "invalid x-api-key",
        "invalid api key", "invalid bearer token", "oauth token", "/login",
        "401",
    ))


def parse_result(text: str) -> dict | None:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    required = ("title_ko", "body")
    if not all(isinstance(data.get(k), str) and data.get(k) for k in required):
        return None
    variations = data.get("variations") or []
    if not isinstance(variations, list):
        variations = []
    data["variations"] = variations
    data["body_translation"] = str(data.get("body_translation", "")).strip()
    tags = data.get("tags") or []
    data["tags"] = [slugify(str(t)) for t in tags[:3] if str(t).strip()] or ["daily"]
    return data


def build_prompt(sentence: str, source: str | None) -> str:
    note = QUOTE_NOTE.format(author=source) if source else ""
    return GENERATE_PROMPT.format(sentence=sentence, note=note)


def generate_api(client, model: str, sentence: str, source: str | None = None) -> dict | None:
    prompt = build_prompt(sentence, source)
    for attempt in (1, 2):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as exc:  # noqa: BLE001
            if is_fatal_api_error(exc):
                raise FatalAPIError(str(exc)) from exc
            log(f"  API 오류 (시도 {attempt}): {exc}")
            if attempt == 2:
                return None
            continue
        text = next((b.text for b in response.content if b.type == "text"), "")
        result = parse_result(text)
        if result:
            return result
        log(f"  JSON 파싱 실패 (시도 {attempt}): {text[:120]!r}")
    return None


def generate_cli(model: str, sentence: str, source: str | None = None) -> dict | None:
    prompt = build_prompt(sentence, source)
    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)
    cmd = ["claude", "-p", "--model", model, "--tools", "",
           "--output-format", "text", "--append-system-prompt", SYSTEM_PROMPT]
    for attempt in (1, 2):
        try:
            result = subprocess.run(cmd, input=prompt, env=env, timeout=180,
                                     capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            log(f"  CLI 타임아웃 (시도 {attempt})")
            continue
        if result.returncode != 0:
            err = (result.stderr or result.stdout).strip()
            if is_fatal_api_error(RuntimeError(err)):
                raise FatalAPIError(err[:300])
            log(f"  CLI 오류 (시도 {attempt}): {err[:200]}")
            if attempt == 2:
                return None
            continue
        parsed = parse_result(result.stdout)
        if parsed:
            return parsed
        log(f"  JSON 파싱 실패 (시도 {attempt}): {result.stdout[:120]!r}")
    return None


def yaml_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_post(sentence: str, result: dict, date: datetime, source: str | None = None) -> Path:
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    base = f"{date.date().isoformat()}-{slugify(result['title_ko'])}"
    path = CONTENT_DIR / f"{base}.md"
    n = 2
    while path.exists():
        path = CONTENT_DIR / f"{base}-{n}.md"
        n += 1

    tags = list(result["tags"])
    if source:
        tags = (tags + ["quote"])[:4]
    tags_str = ", ".join(yaml_quote(t) for t in tags)

    heading_input = HEADING_INPUT_QUOTE if source else HEADING_INPUT
    quote_block = f"> {sentence}\n>\n> — {source}" if source else f"> {sentence}"

    body_section = f"## {HEADING_BODY}\n\n{result['body']}\n"
    if result.get("body_translation"):
        body_section += f"\n> {result['body_translation']}\n"

    variations_section = ""
    if result.get("variations"):
        items = "\n".join(
            f"{i}. **{v['text']}**\n   {v.get('translation', '')}"
            for i, v in enumerate(result["variations"], 1)
        )
        variations_section = f"\n## {HEADING_VARIATIONS}\n\n{items}\n"

    post = f"""---
title: {yaml_quote(f"{date.date().isoformat()} {result['title_ko']}")}
date: {date.isoformat()}
tags: [{tags_str}]
---
## {heading_input}

{quote_block}

{body_section}{variations_section}"""
    path.write_text(post, encoding="utf-8")
    return path


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily diary pipeline")
    parser.add_argument("--dry-run", action="store_true",
                         help="파일 생성/state.json 갱신 없이 결과만 출력")
    args = parser.parse_args()

    backend = os.environ.get("JUDGE_BACKEND", "").strip() or (
        "claude-code" if shutil.which("claude") else "api"
    )
    client = None
    if backend == "api":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            log("오류: api 백엔드에는 ANTHROPIC_API_KEY 환경변수가 필요합니다")
            return 1
        import anthropic  # 지연 임포트

        client = anthropic.Anthropic()
    elif backend == "claude-code":
        if not shutil.which("claude"):
            log("오류: claude-code 백엔드에는 claude CLI가 PATH에 있어야 합니다")
            return 1
    else:
        log(f"오류: 알 수 없는 JUDGE_BACKEND={backend!r} (claude-code | api)")
        return 1

    model = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
    today = datetime.now(KST).date()
    sentences = read_sentences()
    queue = build_queue(sentences, today)
    if sentences:
        log(f"입력된 항목 {len(sentences)}개")
    elif queue:
        log(f"input/sentence.md 에 항목이 없어 명언으로 대체합니다: {queue[0]['text']}"
            + (f" (— {queue[0]['source']})" if queue[0]['source'] else ""))
    else:
        log("input/sentence.md 에 항목이 없고 FALLBACK_QUOTES도 비어 있어 오늘은 건너뜁니다")
        return 0

    state = load_state()
    processed: dict = state.get("processed", {})

    log(f"=== 생성 시작 (backend={backend}, model={model}, dry_run={args.dry_run}) ===")

    new_count = 0
    skipped_dup = 0
    failed = 0
    fatal_error = None
    for item in queue:
        sentence, source, h = item["text"], item["source"], item["dedup_key"]
        if h in processed:
            skipped_dup += 1
            continue

        log(f"\n오늘의 항목: {sentence}" + (f" (— {source})" if source else ""))
        try:
            if backend == "claude-code":
                result = generate_cli(model, sentence, source)
            else:
                result = generate_api(client, model, sentence, source)
        except FatalAPIError as exc:
            fatal_error = exc
            break

        if result is None:
            log("  생성 실패 — 건너뜁니다 (다음 실행에서 재시도)")
            failed += 1
            continue

        now = datetime.now(KST)
        log(f"  → {result['title_ko']}")

        if args.dry_run:
            log("  --- body ---\n  " + result["body"])
            if result.get("body_translation"):
                log("  --- body_translation ---\n  " + result["body_translation"])
            if result.get("variations"):
                log("  --- variations ---")
                for v in result["variations"]:
                    log(f"    - {v['text']} / {v.get('translation', '')}")
            continue

        path = write_post(sentence, result, now, source)
        log(f"  생성 파일: {path.relative_to(ROOT)}")
        processed[h] = now.date().isoformat()
        new_count += 1

    log(f"\n=== 결과: 신규 {new_count} / 중복 스킵 {skipped_dup} / 생성 실패 {failed} ===")

    if args.dry_run:
        log("(dry-run — 파일 생성/기록 갱신 없음)")
        return 1 if fatal_error else 0

    if new_count:
        state["processed"] = processed
        STATE_FILE.write_text(json.dumps(state, indent=1, sort_keys=True), encoding="utf-8")

    if fatal_error:
        log(f"\n중단: 복구 불가능한 API 오류 — {fatal_error}")
        log("→ Anthropic 크레딧/API 키(또는 CLAUDE_CODE_OAUTH_TOKEN)를 확인하세요.")
        log("→ 성공한 항목은 이미 게시/기록되었습니다.")
        return 1
    return 1 if failed and not new_count else 0


if __name__ == "__main__":
    sys.exit(main())
