# config.toml reference

Copy `config.example.toml` to `config.toml`. Only the keys a run actually
touches need values; everything else can stay empty. `config.toml` holds live
credentials — it is gitignored upstream and must not be committed.

## LLM provider

```toml
llm_provider = "moonshot"
```

Every provider follows the same three-key pattern:

```toml
<provider>_api_key    = ""   # credential
<provider>_base_url   = ""   # empty = the provider's registry default
<provider>_model_name = ""   # empty = the provider's registry default
```

So `llm_provider = "openai"` reads `openai_api_key`, `openai_base_url`,
`openai_model_name`. Set the key for the selected provider only.

Direct providers: `moonshot` (Kimi), `openai`, `anthropic`, `gemini`,
`deepseek`, `qwen`, `azure`, `volcengine` (ByteDance Ark), `grok`, `minimax`,
`mimo` (Xiaomi).

Gateways and aggregators: `cloudflare`, `modelscope`, `aihubmix`, `aimlapi`,
`evolink`, `openrouter`, `oneapi`, `shengsuanyun`, `apimart`, `groq`,
`pollinations`, `litellm` (configured through environment variables rather than
these keys), and `ollama` for a local model.

`ollama` and `pollinations` are the two that can run without a paid key —
reach for `ollama` when the user wants the script generated locally.

## Footage sources

```toml
pexels_api_keys    = []   # array of strings, free registration
pixabay_api_keys   = []   # array of strings, free registration
coverr_api_keys    = []
wavespeed_api_keys = []   # AI text-to-video, billed
```

Arrays, not scalars — multiple keys rotate. `pexels` is the CLI default for
`--video-source`; `local` uses `--video-materials` and needs no key at all.

## Speech and subtitles

```toml
subtitle_provider = "edge"   # "whisper", or "" to skip subtitles entirely
ffmpeg_path       = ""       # leave empty to auto-detect
```

- `edge` derives timings from the TTS output. Fast, CPU-only, no download.
- `whisper` transcribes the rendered audio locally with `faster-whisper`. More
  accurate, and the only option that can caption a `--custom-audio-file`. First
  use downloads the model (~3 GB for `large-v3`, ~1.6 GB for
  `large-v3-turbo`) — warn the user before selecting it on a metered or slow
  connection.

```toml
[whisper]
model_size   = "large-v3"   # or "large-v3-turbo"
device       = "cpu"        # "cuda" with a GPU
compute_type = "int8"
```

Azure TTS credentials live in their own section:

```toml
[azure]
speech_key    = ""
speech_region = ""
```

## Network and UI

```toml
[proxy]
http  = ""   # "http://<user>:<pass>@<host>:<port>"
https = ""

[ui]
hide_log                       = false
open_task_folder_on_completion = true
language                       = "zh"   # WebUI locale
```

`[proxy]` is what makes Pexels and the TTS endpoints reachable from a restricted
network — check it before concluding a key is wrong.

## Resources on disk

- `resource/songs/` — BGM pool for `--bgm-type random`. Drop files in to extend it.
- `resource/fonts/` — subtitle fonts; `--font-name` takes a filename from here.
  Default `STHeitiMedium.ttc`. A font without glyphs for the script's language
  renders as blanks or boxes, so pick a font that covers it.
- `storage/tasks/<task_id>/` — per-run output, including the final MP4.
- `storage/bgm/` — the other directory `--bgm-file` accepts.
