---
name: omnivoice
description: Drive OmniVoice (k2-fsa/OmniVoice) to synthesise speech in 600+ languages — zero-shot voice cloning from a reference clip, voice design from a written style instruction, or an auto-picked voice — through omnivoice-infer, the JSONL batch runner, or the Python API. Use when the user asks to generate speech or a voiceover, clone or mimic a voice from a sample, design a speaker by attributes (gender, age, accent, pitch), narrate text as audio, or install and configure OmniVoice. Triggers on "OmniVoice", "음성 합성", "목소리 복제", "TTS 만들어줘", "내레이션 음성", "voice cloning", "text to speech". Not for transcribing audio (that is ASR) or for editing an existing recording.
---

# OmniVoice

Upstream: <https://github.com/k2-fsa/OmniVoice> (Apache-2.0, Python ≥3.10,
PyTorch ≥2.4). Default checkpoint `k2-fsa/OmniVoice`, pulled from Hugging Face
on first use.

A diffusion TTS model with three generation modes. Pick the mode from what the
user actually supplied — this is the first decision, and the rest follows:

| Mode | You have | How to invoke |
| --- | --- | --- |
| **Voice clone** | a reference audio clip | `--ref_audio` (+ `--ref_text`) |
| **Voice design** | a written description of a voice | `--instruct` |
| **Auto** | neither | pass neither; the model picks a voice |

## Cloning a real person's voice

Voice cloning reproduces a real person's identity, so treat the reference clip
as the consent question it is:

- The user's own voice, a synthetic sample, or a voice they hold rights to — go
  ahead.
- Someone else's voice — ask whether that person agreed before you run it.
- A named public figure, where the output would read as that person actually
  saying the words — decline the clone and offer voice design instead: an
  `--instruct` description gets a similar-sounding delivery without cloning
  anyone's identity.

Say this once, briefly, and move on. It is not a reason to refuse ordinary
narration work.

## Install

Torch must match the hardware, so install it first and let OmniVoice follow:

```bash
# NVIDIA (CUDA 12.8 wheels)
pip install torch==2.8.0+cu128 torchaudio==2.8.0+cu128 \
  --extra-index-url https://download.pytorch.org/whl/cu128
pip install omnivoice
```

From source, `uv` handles the torch pin itself:

```bash
git clone https://github.com/k2-fsa/OmniVoice.git && cd OmniVoice && uv sync
```

`--device` is auto-detected; override it with `cuda:0`, `mps` (Apple Silicon),
`xpu` (Intel Arc) or `cpu`. CPU works but is slow — warn the user rather than
letting a long render look like a hang.

The first run downloads the checkpoint. On a metered or slow connection, say so
before starting.

## Generate

Voice clone — `--ref_text` is the transcript of the reference clip, not the
text you want spoken:

```bash
omnivoice-infer \
  --text "This is the line to speak." \
  --ref_audio ref.wav --ref_text "transcript of ref.wav" \
  --language en --output out.wav
```

Voice design — no reference audio at all:

```bash
omnivoice-infer \
  --text "This is the line to speak." \
  --instruct "male, British accent, low pitch, calm" \
  --language en --output out.wav
```

`--text` and `--output` are the only required flags. Pass `--language` whenever
you know it (name `English` or code `en`) — upstream notes quality is slightly
better than the language-agnostic default.

Full flag list, the batch runner and the Python API: `references/cli-and-api.md`.

## Many clips at once

Do not loop `omnivoice-infer` — each call reloads the model. Write a JSONL list
and run the batch entry point once:

```bash
omnivoice-infer-batch --test_list test.jsonl --res_dir results/
```

Each line needs `id` and `text`; add `ref_audio` + `ref_text` for cloning or
`instruct` for design, and optionally `language_id`, `duration`, `speed`.

## Tuning

Defaults are good. Reach for these only when the output is actually wrong:

- `--num_step` (default 32) — drop to 16 for roughly twice the speed at some
  quality cost. Raise it only if quality is visibly poor.
- `--duration` (seconds) overrides `--speed`. Post-processing trims trailing
  silence, so a `--duration` clip lands slightly short; pass
  `--postprocess_output false` when the length must match exactly.
- `--position_temperature 0 --class_temperature 0` makes generation
  deterministic — use it when you need a reproducible take.

Quality traps and language-specific input rules are in
`references/tuning-and-gotchas.md`. Check it before blaming the model: short
clips, conflicting `ref_audio` + `instruct`, and Min Nan input format each fail
in ways that look like a bad checkpoint but are not.

## Interactive UI

```bash
omnivoice-demo            # Gradio UI on 0.0.0.0:7860
```

Port defaults to **7860** (an upstream README example shows `--port 8001`; that
is the example's own flag, not the default). It binds `0.0.0.0` — on a shared
machine that is reachable from the network, so pass `--ip 127.0.0.1` unless the
user wants it exposed.

Use the UI only when the user asks to try voices by hand. For anything you are
producing on their behalf, drive the CLI — you can read its output and they get
a file.

## Verify before reporting done

Check the WAV exists and is non-empty, and report its path and duration. A
render that wrote no file is a failed run regardless of how the log ended:

```bash
python3 -c "import soundfile as sf; i=sf.info('out.wav'); print(i.duration, 's', i.samplerate)"
```
