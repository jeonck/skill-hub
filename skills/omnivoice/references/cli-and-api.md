# CLI flags and Python API

Four entry points are installed with the package:

| Command | Purpose |
| --- | --- |
| `omnivoice-infer` | one clip |
| `omnivoice-infer-batch` | many clips, multi-GPU |
| `omnivoice-demo` | Gradio web UI |
| `omnivoice-merge-lora` | fold a LoRA adapter into the base checkpoint |

## `omnivoice-infer`

`--text` and `--output` are required; everything else has a default.

| Flag | Type | Default | Notes |
| --- | --- | --- | --- |
| `--text` | str | — | **Required.** The line to speak. |
| `--output` | str | — | **Required.** Output WAV path. |
| `--model` | str | `k2-fsa/OmniVoice` | Checkpoint path or HF repo id. |
| `--ref_audio` | str | `None` | Reference clip → voice-clone mode. |
| `--ref_text` | str | `None` | Transcript **of the reference clip**, not the target text. |
| `--instruct` | str | `None` | Style description → voice-design mode. |
| `--language` | str | `None` | Name (`English`) or code (`en`). Slightly better quality when set. |
| `--lora_adapter` | str | `None` | Path to a LoRA adapter directory. |
| `--device` | str | auto | `cuda:0`, `mps`, `xpu`, `cpu`. |
| `--num_step` | int | `32` | Unmasking steps. 16 ≈ 2× faster, lower quality. |
| `--guidance_scale` | float | `2.0` | Classifier-free guidance. |
| `--speed` | float | `1.0` | >1 shorter/faster, <1 longer/slower. Ignored when `--duration` is set. |
| `--duration` | float | `None` | Fixed output length in seconds. Overrides `--speed`. |
| `--t_shift` | float | `0.1` | Noise-schedule shift; smaller emphasises early steps. |
| `--denoise` | bool | `True` | Prepends the denoise token for cleaner speech. |
| `--postprocess_output` | bool | `True` | Trims long silences from the output. |
| `--layer_penalty_factor` | float | `5.0` | Penalty on deeper codebook layers. |
| `--position_temperature` | float | `5.0` | Mask-position randomness. `0` = deterministic. |
| `--class_temperature` | float | `0.0` | Token-sampling randomness. `0` = deterministic. |

Boolean flags take an explicit value: `--denoise false`, not a bare `--denoise`.

Priority for length control: `duration` > `speed`.

## `omnivoice-infer-batch`

```bash
omnivoice-infer-batch --model k2-fsa/OmniVoice \
  --test_list test.jsonl --res_dir results/
```

`--test_list` and `--res_dir` are required. It spreads work across the visible
GPUs, so it is the right tool for more than a couple of clips — one model load
instead of one per clip.

| Flag | Default | Notes |
| --- | --- | --- |
| `--nj_per_gpu` | `1` | Worker processes per GPU. |
| `--batch_size` | `0` | `0` = size batches by duration instead of count. |
| `--batch_duration` | `1000.0` | Total seconds per batch when `--batch_size 0`. |
| `--audio_chunk_duration` | `15.0` | Chunk length for long inputs. |
| `--audio_chunk_threshold` | `30.0` | Inputs longer than this get chunked. |
| `--enable_flashinfer` | `False` | NVIDIA-only speedup; needs `flashinfer-python`. |
| `--warmup` | `0` | Warm-up iterations before timing. |
| `--preprocess_prompt` | `True` | Clean reference audio and punctuate reference text. |
| `--lang_id` | `None` | Language applied to every item. |

Shared with `omnivoice-infer`: `--num_step`, `--guidance_scale`, `--t_shift`,
`--denoise`, `--postprocess_output`, `--layer_penalty_factor`,
`--position_temperature`, `--class_temperature`.

### JSONL format

One JSON object per line. Required: `id`, `text`. Then either the cloning pair
or the design field, plus optional per-item overrides:

```jsonl
{"id": "line01", "text": "First line.", "ref_audio": "ref.wav", "ref_text": "transcript of ref.wav"}
{"id": "line02", "text": "Second line.", "instruct": "female, warm, mid pitch", "speed": 1.1}
{"id": "line03", "text": "Third line.", "language_id": "en", "duration": 4.0}
```

Optional fields: `language_id`, `duration`, `speed`.

## `omnivoice-demo`

| Flag | Default |
| --- | --- |
| `--ip` | `0.0.0.0` |
| `--port` | `7860` |
| `--model` | `k2-fsa/OmniVoice` |
| `--device` | auto |
| `--root-path` | `None` |
| `--share` | `False` (public Gradio tunnel) |
| `--no-asr` | `False` (skip auto-transcribing reference audio) |
| `--asr-model` | `openai/whisper-large-v3-turbo` |

It binds all interfaces by default. Pass `--ip 127.0.0.1` on a shared machine,
and treat `--share` as publishing — it opens a public URL to the running UI.

## Python API

Use this over the CLI when generating several lines in one process, or when
reusing one reference voice across many lines.

```python
import torch
from omnivoice import OmniVoice

model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16
)

# text accepts a list for batch generation; returns list[np.ndarray]
audio = model.generate(text="Hello", ref_audio="ref.wav", language="en")
```

`generate()` parameters: `text`, `language`, `ref_text`, `ref_audio`,
`voice_clone_prompt`, `instruct`, `duration`, `speed`, `generation_config`,
`normalize_text` (default `False`), plus the decoding keywords above.

`ref_audio` takes a path or a `(waveform, sample_rate)` tuple. `text` and most
per-item parameters accept a list for batch generation.

To reuse one voice across many lines, build the prompt once with
`model.create_voice_clone_prompt(...)` and pass it as `voice_clone_prompt`
instead of re-supplying `ref_audio`/`ref_text` each call.

Parameters can also be bundled:

```python
from omnivoice import OmniVoiceGenerationConfig

config = OmniVoiceGenerationConfig(num_step=16, guidance_scale=2.0)
audio = model.generate(text="Hello world", generation_config=config)
```

Write the result yourself — `generate()` returns arrays, not files:

```python
import soundfile as sf
sf.write("out.wav", audio[0], model.sampling_rate)
```
