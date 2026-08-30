---
name: moneyprinter-turbo
description: Drive MoneyPrinterTurbo (harry0703/MoneyPrinterTurbo) headlessly to turn a topic into a finished short-form video — LLM script, stock or AI footage, TTS voiceover, subtitles, BGM — via its CLI, batch manifest, or REST API instead of the Streamlit WebUI. Use when the user asks to generate a short/Shorts/Reels/TikTok video from a subject or script, to install or configure MoneyPrinterTurbo, to fix its config.toml (LLM provider, Pexels/Pixabay keys, TTS voice, whisper subtitles), or to batch-render many videos. Triggers on "MoneyPrinterTurbo", "머니프린터", "숏츠 자동 생성", "주제만 주면 영상 만들어줘", "shorts generator", "faceless video". Do not use for editing an existing video file or for Higgsfield/Remotion pipelines.
---

# MoneyPrinterTurbo

Upstream: <https://github.com/harry0703/MoneyPrinterTurbo> (Python 3.11+, FFmpeg).
It takes a subject, has an LLM write a script and search terms, pulls matching
footage, synthesises a voiceover, burns subtitles, mixes BGM, and encodes an
MP4.

**Drive it through `cli.py`, not the WebUI.** The WebUI (`webui.sh`, port 8501)
is interactive and you cannot read its state. The CLI is headless, takes every
setting as a flag, and prints a JSON result to stdout. Use the REST API only
when the user explicitly wants a long-running service.

## 1. Locate or install

Look for an existing checkout before cloning anything — users usually have one:

```bash
ls config.toml cli.py webui 2>/dev/null            # already inside it?
ls ~/MoneyPrinterTurbo/cli.py 2>/dev/null
```

If there is none, ask the user where to put it, then:

```bash
git clone https://github.com/harry0703/MoneyPrinterTurbo.git
cd MoneyPrinterTurbo
uv python install 3.11
uv sync --frozen
```

Every command below runs from the project root and is prefixed `uv run`. If the
project was set up with a plain venv instead, activate it and drop the `uv run`.

Docker is the other supported path — `docker compose -f docker-compose.release.yml up`
serves the WebUI on 8501 and the API on 8080, but gives you no CLI, so prefer a
local checkout for generation work.

## 2. Configure `config.toml`

`cp config.example.toml config.toml`, then fill in only what the requested run
needs. See `references/config-reference.md` for the full key list.

Minimum for a default run:

| Setting | Why |
| --- | --- |
| `llm_provider` + `<provider>_api_key` | writes the script and search terms |
| `pexels_api_keys` | supplies the footage (free key, array of strings) |

`subtitle_provider = "edge"` and the default Edge TTS voice both cost nothing
and need no credentials — leave them alone unless asked.

**Never invent an API key, and never read one out of the user's shell history or
another project's config.** If a required key is missing, stop and ask for it.
Keys go in `config.toml`, which is gitignored upstream — do not commit it, and
do not echo key values back in your replies.

## 3. Gate anything that costs money

Free by default: Edge TTS, Pexels/Pixabay/Coverr footage, local whisper.

Billable, and each needs the user's explicit go-ahead **before** the run — say
which provider bills and roughly per what (per clip, per character):

- `--video-source volcengine_seedance` and WaveSpeed AI — paid text-to-video,
  billed per generated clip. Seedance additionally refuses to start without
  `--confirm-seedance-charge`; treat that flag as the user's consent, never as a
  box for you to tick on your own.
- ElevenLabs, Azure, Fish Audio, SiliconFlow, Gemini and MiMo TTS.
- Whichever LLM provider is configured.

`--video-count 5` multiplies every one of those by five. Confirm the count.

## 4. Preview the script before rendering

A full render spends TTS characters and minutes of FFmpeg on a script nobody has
read yet. Stop early, show the script, then continue:

```bash
uv run python cli.py --video-subject "How AI is changing everyday life" \
  --video-language en-US --paragraph-number 3 --stop-at script
```

`--stop-at` accepts `script`, `terms`, `audio`, `subtitle`, `materials`, `video`.
Show the generated script, take edits, then render with the approved text passed
verbatim through `--video-script` so the LLM does not rewrite it:

```bash
uv run python cli.py --video-script "<approved script>" \
  --video-terms "ai,technology,city" \
  --video-aspect 9:16 --video-clip-duration 5 \
  --voice-name en-US-JennyNeural --bgm-type random --bgm-volume 0.2 \
  --subtitle-position bottom --font-size 60 --stroke-width 1.5
```

Skip the preview only when the user hands you a finished script.

On success the CLI prints `{"task_id": "<uuid>", "result": {...}}` and the
artifacts land in `storage/tasks/<task_id>/`. Report the MP4 path — do not just
say it finished. Exit codes: `0` success, `1` task failure, `2` bad arguments or
manifest.

Full flag list, with defaults and choices: `references/cli-and-api.md`.

## 5. Batch

For more than two or three videos, write a manifest instead of looping the CLI —
one process, one JSON summary, and a per-task failure report:

```bash
uv run python cli.py --batch-file tasks.jsonl
```

JSON array or JSONL, up to 100 tasks and 1 MiB. Each object sets `VideoParams`
fields in snake_case (`video_subject`, `video_script`, `video_aspect`, …);
unknown fields are rejected, every task needs `video_subject` or `video_script`,
and relative paths resolve against the manifest's directory. `--batch-file` and
`--task-id` are mutually exclusive.

The summary reports `succeeded`/`failed` with a `failed_stage` per task. A batch
that reports failures has not succeeded — surface the failing tasks and their
stage rather than only the total.

## 6. API service mode

```bash
uv run python main.py     # 127.0.0.1:8080, interactive docs at /docs
```

Endpoints are under `/api/v1` — `POST /videos` starts a task and returns a
`task_id`, `GET /tasks/{task_id}` polls it, `GET /download/{file_path}` fetches
the result. Poll with a bounded number of attempts and a real interval; never
busy-loop. Endpoint table in `references/cli-and-api.md`.

## 7. When a run fails

Check `references/troubleshooting.md` before improvising — FFmpeg not found,
`Too many open files`, a stalled whisper model download, and non-ASCII project
paths on Windows cover most failures, and each has a known fix.

Two rules for failures: a render that produced no MP4 is a failed run even if the
process exited quietly, so verify the file exists before reporting success; and
if the LLM step fails, read the actual provider error rather than switching
providers blindly — an unset key and a rate limit need different fixes.
