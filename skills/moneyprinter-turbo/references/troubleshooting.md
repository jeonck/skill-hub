# Troubleshooting

Work down this list before changing providers or reinstalling. Most failures
here are environmental, not configuration errors.

## `No ffmpeg exe could be found`

The bundled auto-download failed — usual causes are a firewall, an offline box,
or a proxy. Install FFmpeg yourself and point the config at the binary:

```toml
ffmpeg_path = "C:\\ffmpeg\\bin\\ffmpeg.exe"   # Windows, escaped backslashes
```

On macOS `brew install ffmpeg`, on Debian/Ubuntu `apt install ffmpeg`; once it
is on `PATH`, leave `ffmpeg_path` empty. Verify with `ffmpeg -version` before
re-running.

## `Too many open files`

Linux and macOS only, and it usually strikes partway through the concat stage
with many source clips. Raise the descriptor limit in the same shell that runs
the render:

```bash
ulimit -n 10240
```

`ulimit` applies to the current shell and its children only, so set it in the
shell that launches `cli.py` — not in a separate one. Lowering
`--video-count` or `--n-threads` reduces the pressure if the limit cannot be
raised.

## Whisper model download stalls or fails

`subtitle_provider = "whisper"` pulls the model on first use — ~3 GB for
`large-v3`, ~1.6 GB for `large-v3-turbo`. On a failure, fetch it from Hugging
Face by hand and extract into:

```
./models/whisper-large-v3/
```

Switching `subtitle_provider` back to `edge` sidesteps the download entirely and
is the right call unless the run needs whisper's accuracy or is captioning a
`--custom-audio-file`.

## Windows path problems

Keep the checkout at a path with no spaces, no non-ASCII characters, and no
shell metacharacters. `C:\MoneyPrinterTurbo` works; a project under a Korean or
Chinese user directory fails in ways that surface much later as FFmpeg or font
errors rather than as a path error.

## Subtitles render as boxes or blanks

The font in `resource/fonts` has no glyphs for the script's language. Drop a
font that covers it into that directory and pass its filename via
`--font-name`. The default `STHeitiMedium.ttc` covers CJK and Latin.

## Empty, black, or too-short output

- No footage matched the search terms — pass `--video-terms` explicitly with
  broader, more generic English nouns. Stock libraries index in English, so
  terms in other languages return little regardless of `--video-language`.
- `--paragraph-number` too low: one paragraph can be a handful of seconds.
- Rate-limited or invalid Pexels/Pixabay key: check the run log for the HTTP
  status before assuming the terms were at fault. Behind a corporate network,
  fill in `[proxy]` — an unreachable API looks identical to a bad key.

## LLM step fails

Read the provider's actual error rather than switching providers:

- 401/403 — key unset, or set on a provider other than the one `llm_provider`
  selects.
- 429 — rate limit; retry with backoff.
- Connection errors — network or `[proxy]`, not credentials.

Confirm `llm_provider` matches the `<provider>_api_key` that is actually
populated. Mismatched pairs are the single most common cause here.

## The run "finished" but there is no MP4

Check `storage/tasks/<task_id>/` for the output. A non-zero exit code, or an
empty task directory, means the run failed even if the log looks calm — read
the tail of the log for the failing stage. In batch mode the per-task
`failed_stage` field names it directly.
