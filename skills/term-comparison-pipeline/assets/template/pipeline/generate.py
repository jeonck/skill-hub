#!/usr/bin/env python3
"""Term comparison pipeline (working example domain: IT/software terms).

Reads short topics from input/term.md (one per line, inside the fenced code
block), and for each new one (not yet published — tracked by content hash in
pipeline/state.json) asks Claude to produce a structured side-by-side
comparison: a short overview, an inline SVG diagram, a comparison table, key
differences, and "when to use each". Each item becomes one Hugo post under
content/posts/. This pipeline is ON-DEMAND ONLY — it runs when input/term.md
changes (push) or via manual workflow_dispatch. There is no daily schedule and
no fallback content: an empty input file simply produces no new post.

Usage:
    python pipeline/generate.py [--dry-run]

Env:
    JUDGE_BACKEND            "claude-code" | "api" (default: auto — claude-code
                             if the claude CLI is on PATH, otherwise api)
    CLAUDE_CODE_OAUTH_TOKEN  claude-code backend auth in CI (issued via
                             `claude setup-token`; locally the logged-in
                             `claude` CLI session is used instead)
    ANTHROPIC_API_KEY        required for the api backend
    CLAUDE_MODEL             generation model (default claude-sonnet-5)

The only part to rewrite for a new comparison domain (e.g. "compare cooking
techniques" instead of "compare IT terms") is the "=== 비교 도메인 설정 ===" block
below — SYSTEM_PROMPT, GENERATE_PROMPT, and the HEADING_* section titles. If
you change the JSON schema inside GENERATE_PROMPT, update parse_result()'s
validation and write_post()'s rendering together — changing only one causes
silent JSON-parse failures in generation logs. The engine code below the
marker (dedup hashing, claude-code/api backend switch, timeout/retry handling,
Hugo post assembly) is battle-tested from a real production run and should not
need changes.
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
TERM_FILE = ROOT / "input" / "term.md"
STATE_FILE = ROOT / "pipeline" / "state.json"
CONTENT_DIR = ROOT / "content" / "posts"

KST = timezone(timedelta(hours=9))

# ============================== 비교 도메인 설정 =================================
# 이 블록만 새 비교 주제에 맞게 다시 쓴다. 아래 엔진 코드는 건드릴 필요 없다.
# 지금 채워진 내용은 "IT/소프트웨어 용어 비교" 도메인의 실제 동작 예시다.

SYSTEM_PROMPT = """You are a technical writer who creates precise, concise \
side-by-side comparisons of IT and software engineering terms/concepts for a \
developer audience. You avoid oversimplification and hand-wavy analogies \
where precision matters. You also design clean, minimal, self-contained SVG \
diagrams that visually clarify the structural or conceptual difference being \
compared (e.g. memory layout, architecture boxes, request flow, arrows \
between components). Diagrams use only basic shapes (rect, circle, line, \
path, polygon, text) — no external fonts, images, CSS classes, or scripts.

The diagram is embedded directly into the site's page, so it must use the \
site's own design system instead of inventing colors: every fill/stroke MUST \
be set via a `style` attribute referencing one of these CSS custom \
properties (never a hardcoded hex/rgb color, and never presentation \
attributes like `fill="#..."`):

- var(--primary)   — bold headings/labels (e.g. the two item names)
- var(--content)   — regular diagram body text
- var(--secondary) — muted/annotation text (small captions, "free" labels)
- var(--border)    — neutral dividers, dashed placeholder/empty boxes
- var(--compare-a) / var(--compare-a-soft) — accent stroke / soft tint fill \
for every shape belonging to the LEFT (first) compared item
- var(--compare-b) / var(--compare-b-soft) — accent stroke / soft tint fill \
for every shape belonging to the RIGHT (second) compared item

Example: <rect style="fill:var(--compare-a-soft);stroke:var(--compare-a)" \
stroke-width="1.5" .../> — <text style="fill:var(--content)" .../>. Leave the \
SVG's own background transparent (no full-bleed background rect) — the page \
already wraps it in a themed card. Use a viewBox of "0 0 640 360". These \
variables are already defined for both light and dark mode, so following \
this palette exactly is what keeps every diagram legible and visually \
consistent across the whole site."""

# {term} 자리는 반드시 단일 중괄호로 유지한다. JSON 스키마 리터럴(`{{"title": ...}}`)은
# Python str.format()이 리터럴 `{`/`}`를 출력하도록 이중 중괄호를 유지해야 한다 — 필드를
# 늘리거나 줄일 때도 이 이스케이프 규칙을 그대로 따른다. 스키마를 바꾸면 parse_result()의
# 검증 로직과 write_post()의 렌더링도 함께 맞춘다.
GENERATE_PROMPT = """Create a side-by-side comparison post for the following \
IT term/topic: "{term}"

Respond with ONLY valid JSON (no markdown code fences, no commentary before \
or after) matching exactly this schema:

{{"title": "Concise comparison title, e.g. 'X vs Y: <short descriptor>'",
 "summary": "2-3 sentence plain-English overview of what is being compared and why the distinction matters",
 "diagram_svg": "A complete, valid, self-contained '<svg>...</svg>' string (viewBox=\\"0 0 640 360\\") that visually illustrates the core structural or conceptual difference, using ONLY the var(--compare-a)/var(--compare-b)/var(--primary)/var(--content)/var(--secondary)/var(--border) design-system colors described above via style attributes (no hardcoded hex/rgb colors). Label both sides clearly with <text> elements. Escape all double quotes and newlines so the value is valid inside this JSON string.",
 "table_headers": ["Aspect", "<Left item name>", "<Right item name>"],
 "table_rows": [["<aspect 1>", "<left value>", "<right value>"], ["<aspect 2>", "<left value>", "<right value>"], "5 to 8 rows total, covering the most decision-relevant aspects"],
 "key_differences": ["3 to 5 short, specific bullet points on the most important distinctions — no filler"],
 "when_to_use_left": "1-2 sentences on when to prefer the left item",
 "when_to_use_right": "1-2 sentences on when to prefer the right item",
 "tags": ["2 to 4 kebab-case tags"]}}

Topic: {term}"""

# 포스트 본문 섹션 제목
HEADING_OVERVIEW = "Overview"
HEADING_DIAGRAM = "Comparison Diagram"
HEADING_TABLE = "Comparison Table"
HEADING_DIFFERENCES = "Key Differences"
HEADING_USAGE = "When to Use Each"

# ============================ 비교 도메인 설정 끝 =================================


def log(msg: str) -> None:
    print(msg, flush=True)


def term_hash(s: str) -> str:
    return hashlib.sha256(s.strip().lower().encode("utf-8")).hexdigest()[:16]


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
    return (slug or "comparison")[:60].rstrip("-")


def read_terms() -> list[str]:
    """Read the topics the user has queued in input/term.md. Empty if none."""
    if not TERM_FILE.exists():
        log(f"error: {TERM_FILE} does not exist")
        sys.exit(1)
    text = TERM_FILE.read_text(encoding="utf-8")
    fenced = re.search(r"```[a-zA-Z]*\n(.*?)```", text, re.DOTALL)
    body = fenced.group(1) if fenced else text
    terms = []
    for line in body.splitlines():
        line = line.strip()
        if line and not line.startswith(("<!--", "-", "#")):
            terms.append(line)
    return terms


def build_queue(terms: list[str]) -> list[dict]:
    return [{"text": t, "dedup_key": term_hash(t)} for t in terms]


class FatalAPIError(Exception):
    """Non-retryable error (out of credits, auth failure) — abort the whole run."""


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

    required = ("title", "summary", "diagram_svg")
    if not all(isinstance(data.get(k), str) and data.get(k).strip() for k in required):
        return None

    svg = data["diagram_svg"].strip()
    if "<svg" not in svg or "</svg>" not in svg:
        return None
    data["diagram_svg"] = svg

    headers = data.get("table_headers")
    rows = data.get("table_rows")
    if not isinstance(headers, list) or len(headers) < 2:
        return None
    if not isinstance(rows, list) or not rows:
        return None
    clean_rows = [r for r in rows if isinstance(r, list) and len(r) == len(headers)]
    if not clean_rows:
        return None
    data["table_headers"] = [str(h) for h in headers]
    data["table_rows"] = [[str(c) for c in r] for r in clean_rows]

    diffs = data.get("key_differences") or []
    data["key_differences"] = [str(d) for d in diffs if str(d).strip()] if isinstance(diffs, list) else []

    data["when_to_use_left"] = str(data.get("when_to_use_left", "")).strip()
    data["when_to_use_right"] = str(data.get("when_to_use_right", "")).strip()

    tags = data.get("tags") or []
    data["tags"] = [slugify(str(t)) for t in tags[:4] if str(t).strip()] or ["comparison"]
    return data


def build_prompt(term: str) -> str:
    return GENERATE_PROMPT.format(term=term)


def generate_api(client, model: str, term: str) -> dict | None:
    prompt = build_prompt(term)
    for attempt in (1, 2):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
        except Exception as exc:  # noqa: BLE001
            if is_fatal_api_error(exc):
                raise FatalAPIError(str(exc)) from exc
            log(f"  API error (attempt {attempt}): {exc}")
            if attempt == 2:
                return None
            continue
        text = next((b.text for b in response.content if b.type == "text"), "")
        result = parse_result(text)
        if result:
            return result
        log(f"  JSON parse failed (attempt {attempt}): {text[:120]!r}")
    return None


def generate_cli(model: str, term: str) -> dict | None:
    prompt = build_prompt(term)
    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)
    cmd = ["claude", "-p", "--model", model, "--tools", "",
           "--output-format", "text", "--append-system-prompt", SYSTEM_PROMPT]
    for attempt in (1, 2):
        try:
            # NOTE: 420s is not a conservative guess — a real production run measured
            # ~192s for a comparable prompt locally, and two consecutive CI attempts
            # at 240s both hit the wall with zero output. An SVG-diagram-plus-table
            # response is genuinely output-token-heavy; don't shorten this without
            # re-measuring in the target CI environment.
            result = subprocess.run(cmd, input=prompt, env=env, timeout=420,
                                     capture_output=True, text=True)
        except subprocess.TimeoutExpired as exc:
            partial = (exc.stderr or exc.stdout or b"")
            if isinstance(partial, bytes):
                partial = partial.decode("utf-8", errors="replace")
            log(f"  CLI timeout (attempt {attempt})" + (f" — partial output: {partial[:200]!r}" if partial.strip() else ""))
            continue
        if result.returncode != 0:
            err = (result.stderr or result.stdout).strip()
            if is_fatal_api_error(RuntimeError(err)):
                raise FatalAPIError(err[:300])
            log(f"  CLI error (attempt {attempt}): {err[:200]}")
            if attempt == 2:
                return None
            continue
        parsed = parse_result(result.stdout)
        if parsed:
            return parsed
        log(f"  JSON parse failed (attempt {attempt}): {result.stdout[:120]!r}")
    return None


def yaml_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    def esc(cell: str) -> str:
        return cell.replace("|", "\\|").replace("\n", " ")

    header_line = "| " + " | ".join(esc(h) for h in headers) + " |"
    sep_line = "| " + " | ".join("---" for _ in headers) + " |"
    row_lines = ["| " + " | ".join(esc(c) for c in row) + " |" for row in rows]
    return "\n".join([header_line, sep_line, *row_lines])


def write_post(term: str, result: dict, date: datetime) -> Path:
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    base = f"{date.date().isoformat()}-{slugify(result['title'])}"
    path = CONTENT_DIR / f"{base}.md"
    n = 2
    while path.exists():
        path = CONTENT_DIR / f"{base}-{n}.md"
        n += 1

    tags_str = ", ".join(yaml_quote(t) for t in result["tags"])
    table_md = render_table(result["table_headers"], result["table_rows"])

    diff_section = ""
    if result["key_differences"]:
        items = "\n".join(f"- {d}" for d in result["key_differences"])
        diff_section = f"\n## {HEADING_DIFFERENCES}\n\n{items}\n"

    usage_section = ""
    if result["when_to_use_left"] or result["when_to_use_right"]:
        left_name = result["table_headers"][1] if len(result["table_headers"]) > 1 else "the first option"
        right_name = result["table_headers"][2] if len(result["table_headers"]) > 2 else "the second option"
        usage_section = f"""
## {HEADING_USAGE}

**{left_name}** — {result['when_to_use_left']}

**{right_name}** — {result['when_to_use_right']}
"""

    # diagram_svg is wrapped in .compare-diagram (assets/css/extended/compare.css) —
    # a themed card so the SVG's var(--entry)/var(--border)-based styling has a
    # matching background instead of floating directly on the page.
    post = f"""---
title: {yaml_quote(result['title'])}
date: {date.isoformat()}
tags: [{tags_str}]
---
## {HEADING_OVERVIEW}

{result['summary']}

## {HEADING_DIAGRAM}

<div class="compare-diagram">
{result['diagram_svg']}
</div>

## {HEADING_TABLE}

{table_md}
{diff_section}{usage_section}"""
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
    parser = argparse.ArgumentParser(description="Term comparison pipeline")
    parser.add_argument("--dry-run", action="store_true",
                         help="print the result without writing files or updating state")
    args = parser.parse_args()

    backend = os.environ.get("JUDGE_BACKEND", "").strip() or (
        "claude-code" if shutil.which("claude") else "api"
    )
    client = None
    if backend == "api":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            log("error: the api backend requires the ANTHROPIC_API_KEY env var")
            return 1
        import anthropic  # lazy import

        client = anthropic.Anthropic()
    elif backend == "claude-code":
        if not shutil.which("claude"):
            log("error: the claude-code backend requires the claude CLI on PATH")
            return 1
    else:
        log(f"error: unknown JUDGE_BACKEND={backend!r} (claude-code | api)")
        return 1

    model = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")
    terms = read_terms()
    queue = build_queue(terms)
    if not queue:
        log("input/term.md has no terms queued — nothing to do")
        return 0
    log(f"{len(queue)} term(s) queued")

    state = load_state()
    processed: dict = state.get("processed", {})

    log(f"=== starting generation (backend={backend}, model={model}, dry_run={args.dry_run}) ===")

    new_count = 0
    skipped_dup = 0
    failed = 0
    fatal_error = None
    for item in queue:
        term, h = item["text"], item["dedup_key"]
        if h in processed:
            skipped_dup += 1
            continue

        log(f"\nterm: {term}")
        try:
            if backend == "claude-code":
                result = generate_cli(model, term)
            else:
                result = generate_api(client, model, term)
        except FatalAPIError as exc:
            fatal_error = exc
            break

        if result is None:
            log("  generation failed — skipping (will retry next run)")
            failed += 1
            continue

        now = datetime.now(KST)
        log(f"  -> {result['title']}")

        if args.dry_run:
            log("  --- summary ---\n  " + result["summary"])
            log("  --- table ---\n  " + render_table(result["table_headers"], result["table_rows"]))
            log("  --- diagram_svg (first 200 chars) ---\n  " + result["diagram_svg"][:200])
            continue

        path = write_post(term, result, now)
        log(f"  file written: {path.relative_to(ROOT)}")
        processed[h] = now.date().isoformat()
        new_count += 1

    log(f"\n=== result: new={new_count} / dup_skipped={skipped_dup} / failed={failed} ===")

    if args.dry_run:
        log("(dry-run — no files written, no state updated)")
        return 1 if fatal_error else 0

    if new_count:
        state["processed"] = processed
        STATE_FILE.write_text(json.dumps(state, indent=1, sort_keys=True), encoding="utf-8")

    if fatal_error:
        log(f"\naborted: unrecoverable API error — {fatal_error}")
        log("-> check Anthropic credits/API key (or CLAUDE_CODE_OAUTH_TOKEN).")
        log("-> already-successful items are committed/recorded.")
        return 1
    return 1 if failed and not new_count else 0


if __name__ == "__main__":
    sys.exit(main())
