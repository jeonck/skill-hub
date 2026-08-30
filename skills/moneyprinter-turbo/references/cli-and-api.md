# CLI flags and REST API

## `cli.py`

Run from the project root: `uv run python cli.py [flags]`.
A flag left unset falls back to the value in `config.toml`, so pass only what
the run needs to change.

### Script and content

| Flag | Type | Default | Notes |
| --- | --- | --- | --- |
| `--video-subject` | str | `""` | The topic. Required unless `--video-script` is given. |
| `--video-script` | str | `""` | A finished script. Skips LLM script generation entirely. |
| `--video-terms` | str | auto | Comma-separated footage search terms. Generated from the script when omitted. |
| `--video-language` | str | auto-detect | e.g. `zh-CN`, `en-US`, `ko-KR`. |
| `--paragraph-number` | int 1–10 | `1` | Script length. Drives the final duration more than any other flag. |
| `--video-script-prompt` | str | — | Extra instructions for the script LLM. |
| `--custom-system-prompt` | str | — | Replaces the default script system prompt outright. |

### Materials and pipeline

| Flag | Type | Default | Notes |
| --- | --- | --- | --- |
| `--video-source` | choice | `pexels` | `pexels`, `pixabay`, `coverr`, `volcengine_seedance`, `local`. |
| `--video-materials` | str | `""` | Comma-separated local image/video paths, for `--video-source local`. |
| `--stop-at` | choice | `video` | `script`, `terms`, `audio`, `subtitle`, `materials`, `video`. |
| `--confirm-seedance-charge` | flag | off | Required by Seedance; it creates paid Ark tasks. User consent only. |

### Output

| Flag | Type | Default | Notes |
| --- | --- | --- | --- |
| `--video-count` | int ≥1 | `1` | Multiplies every per-run cost. |
| `--video-aspect` | choice | `9:16` | `9:16` (1080×1920), `16:9` (1920×1080), `1:1`. |
| `--video-concat-mode` | choice | `random` | `random`, `sequential`. |
| `--video-transition-mode` | choice | — | `none`, `shuffle`, `fade-in`, `fade-out`, `slide-in`, `slide-out`. |
| `--video-clip-duration` | int ≥1 | `5` | Max seconds per source clip. |
| `--match-materials-to-script` | bool | — | Keeps script keyword order when picking footage. |
| `--n-threads` | int ≥1 | `2` | FFmpeg worker threads. |

### Voice and music

| Flag | Type | Default | Notes |
| --- | --- | --- | --- |
| `--voice-name` | str | config | TTS voice id. `no-voice` renders silent. |
| `--voice-volume` | float ≥0 | `1.0` | |
| `--voice-rate` | float >0 | `1.0` | |
| `--custom-audio-file` | path | — | Existing MP3/WAV/M4A/AAC/FLAC/OGG voiceover; bypasses TTS. Needs `subtitle_provider = "whisper"` for captions. |
| `--bgm-type` | choice | — | `none`, `random`, `custom`, `sonilo`. |
| `--sonilo-bgm-prompt` | str | — | Music style prompt, ≤2000 chars. |
| `--bgm-file` | path | — | File in `storage/bgm` or `resource/songs`; use with `--bgm-type custom`. |
| `--bgm-volume` | float ≥0 | `0.2` | Above ~0.3 the music starts burying the voiceover. |

### Subtitles

| Flag | Type | Default |
| --- | --- | --- |
| `--subtitle-enabled` | bool | enabled |
| `--font-name` | str | `STHeitiMedium.ttc` (from `resource/fonts`) |
| `--subtitle-position` | choice | `bottom` — `top`, `center`, `bottom`, `custom` |
| `--custom-position` | float 0–100 | `70` (percent from the top, with `--subtitle-position custom`) |
| `--font-size` | int ≥1 | `60` |
| `--text-fore-color` | `#RRGGBB` | `#FFFFFF` |
| `--stroke-color` | `#RRGGBB` | `#000000` |
| `--stroke-width` | float ≥0 | `1.5` |
| `--subtitle-background-enabled` | bool | disabled |
| `--subtitle-background-color` | `#RRGGBB` | — |
| `--rounded-subtitle-background` | bool | disabled |

Keep the stroke or a background on: white text over bright stock footage is
unreadable without one.

### Execution

| Flag | Type | Notes |
| --- | --- | --- |
| `--task-id` | UUID | Writes to `storage/tasks/<task-id>`. Mutually exclusive with `--batch-file`. |
| `--batch-file` | path | UTF-8 JSON array or JSONL manifest. |

### Output contract

Single task, on stdout:

```json
{"task_id": "<uuid>", "result": {}}
```

Batch:

```json
{
  "total": 3,
  "succeeded": 2,
  "failed": 1,
  "tasks": [
    {"index": 0, "task_id": "<uuid>", "status": "succeeded", "result": {},
     "failed_stage": null, "error": null}
  ]
}
```

Exit codes: `0` success, `1` task failure, `2` argument or manifest error.

### Batch manifest

JSON array or JSONL, ≤100 tasks, ≤1 MiB. Each object overrides `VideoParams`
fields in snake_case. Unknown fields are rejected. Every task needs
`video_subject` or `video_script`. Relative paths resolve against the manifest's
own directory, not the working directory.

```jsonl
{"video_subject": "Three habits of calm mornings", "video_aspect": "9:16", "paragraph_number": 3}
{"video_script": "Pre-written script text...", "video_terms": "coffee,sunrise", "bgm_type": "random"}
```

## REST API

`uv run python main.py` serves on `127.0.0.1:8080`. Interactive docs at `/docs`,
ReDoc at `/redoc`. All routes below are prefixed `/api/v1`.

| Method | Path | Body | Returns |
| --- | --- | --- | --- |
| POST | `/videos` | `TaskVideoRequest` | `TaskResponse` — starts a task, returns its `task_id` |
| POST | `/subtitle` | `SubtitleRequest` | `TaskResponse` |
| POST | `/audio` | `AudioRequest` | `TaskResponse` |
| GET | `/tasks` | — | `TaskListResponse` |
| GET | `/tasks/{task_id}` | — | `TaskQueryResponse` — poll for progress |
| DELETE | `/tasks/{task_id}` | — | `TaskDeletionResponse` |
| GET | `/musics` | — | `BgmRetrieveResponse` |
| POST | `/musics` | multipart file | `BgmUploadResponse` |
| GET | `/video_materials` | — | `VideoMaterialRetrieveResponse` |
| POST | `/video_materials` | multipart file | `VideoMaterialUploadResponse` |
| GET | `/stream/{file_path}` | — | streaming response |
| GET | `/download/{file_path}` | — | file download |

Generation is asynchronous: `POST /videos` returns as soon as the task is
queued. Poll `GET /tasks/{task_id}` on an interval (a render is minutes, not
seconds) with a bounded attempt count, and treat a task that stops advancing as
failed rather than polling forever.

The service binds loopback and has no authentication. Do not expose it to a
network without putting something in front of it; `MPT_WEBUI_HOST=0.0.0.0`
does the same for the WebUI and carries the same caveat.
