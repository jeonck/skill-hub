# Tuning and gotchas

## Behaviours that look like bugs but are documented

**Short clips come out unstable without a reference.** In voice-design or auto
mode the model is unreliable for 1–2 second outputs. Supply `ref_audio` when the
target line is that short, rather than retrying with different wording.

**`ref_audio` and `instruct` together: the audio wins.** When both are given and
they disagree, the reference audio's style dominates. When they agree, the
instruct *stabilises* the attributes it names — the useful case is Chinese
dialect cloning, e.g. `--ref_audio sichuan.wav --instruct "四川话"`, which holds
the dialect more reliably than the reference alone.

**Min Nan Chinese (閩南語 / Hokkien) needs Tai-lo romanisation.** Han characters
are not supported for Min Nan in the current checkpoint. Passing them produces
wrong output with no error. Convert to Tai-lo first, or tell the user why the
text cannot be used as written.

**`--duration` output lands slightly short.** Post-processing trims trailing
silence after the fact. Pass `--postprocess_output false` when the length has to
match exactly — for example when the audio is cut to picture.

## Parameter reference

Decoding:

| Parameter | Default | Effect |
| --- | --- | --- |
| `num_step` | 32 | Unmasking steps. 16 for speed; higher for quality. |
| `denoise` | True | Prepends `<\|denoise\|>` for cleaner speech. |
| `guidance_scale` | 2.0 | Classifier-free guidance. |
| `t_shift` | 0.1 | Noise-schedule shift; smaller emphasises early steps. |

Sampling — set both temperatures to 0 for a deterministic, reproducible take:

| Parameter | Default | Effect |
| --- | --- | --- |
| `position_temperature` | 5.0 | Mask-position randomness. 0 = greedy. |
| `class_temperature` | 0.0 | Token-sampling randomness. 0 = greedy. |
| `layer_penalty_factor` | 5.0 | Pushes lower codebook layers to unmask first. |

Length — `duration` overrides `speed`:

| Parameter | Default | Effect |
| --- | --- | --- |
| `duration` | None | Fixed seconds. |
| `speed` | 1.0 | >1 faster/shorter, <1 slower/longer. |

Pre/post processing:

| Parameter | Default | Effect |
| --- | --- | --- |
| `preprocess_prompt` | True | Strips long silences from reference audio, punctuates reference text. |
| `postprocess_output` | True | Strips long silences from the output. |
| `pad_duration` | 0.1 | Silence padding per side, in seconds. 0 disables. |

## Speed

- `num_step 16` roughly halves generation time.
- `--enable_flashinfer true` on `omnivoice-infer-batch` gives a further speedup
  on NVIDIA GPUs; it needs `flashinfer-python` installed separately.
- `omnivoice-infer-batch` beats looping `omnivoice-infer` for any real workload,
  because the model loads once rather than per clip.
- CPU inference works but is slow enough that a long job looks hung. Say so up
  front instead of leaving the user watching a silent terminal.

## Reference-audio quality

The clone is only as good as the sample. A clean, single-speaker clip with
little background noise and no music clones far better than a noisy one, and
`ref_text` must be an accurate transcript of that clip — a mismatched transcript
degrades the result rather than erroring.

## Languages

600+ are supported; the full list ships upstream in `docs/languages.md` with
`docs/lang_id_name_map.tsv` mapping codes to names. `--language` accepts either
form (`English` or `en`). Leaving it unset runs language-agnostic mode, which
upstream notes is slightly worse — set it whenever the language is known.
