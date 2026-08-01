# usage-profiles — cost / usage tuning (Full vs Low-usage)

The same pipeline runs at two intensity profiles. Pick one at Stage 0 (ask the
user if unsure). The lever is the same either way — it just reads differently
depending on billing:

- **API key (pay-per-token):** intensity = dollars. Low-usage ≈ 40–60% cheaper.
- **Claude subscription / Max (OAuth):** intensity = usage-budget against your
  plan's limits. Low-usage stretches your allowance further and makes big
  parallel bursts far less likely to hit a rate/usage cap. This is usually the
  more economical default for subscription users — use the subscription as the
  base and only fall back to an API key for overflow when you hit a limit.

Render + npm are **always free** (local compute) — profiles only change token/
usage spend by the agents.

## Profile matrix

| Stage | FULL (default) | LOW-USAGE (subscription-friendly) |
|---|---|---|
| Brief / design (orchestrator) | Opus, high effort | Sonnet or low effort |
| Chapter build (parallel subagents) | inherit (Opus), high | **`model: 'sonnet', effort: 'low'`** per subagent |
| Assembly (Main.tsx, BGM/SFX) | Opus | Sonnet / low effort |
| Static-frame QA (images) | 1–2 stills per beat, view most | **1 still per chapter + section boundaries only (~6–10 images total)** |
| Independent review | 1 clean-context reviewer, Opus, many frames | **1 reviewer, cap ~8–10 frames** (Sonnet reviewer OK); or skip for a draft |
| Final render | same (no tokens) | same |

### Why these levers

- **Chapter subagents on Sonnet/low effort** is the biggest single saver — 5
  parallel agents are the bulk of the spend, and chapter TSX is well-specified
  mechanical work Sonnet handles well against the templates.
- **Image QA is the sleeper cost** — each 1920×1080 still is up to ~4.8k image
  input tokens. Viewing dozens adds up fast. In low-usage mode, render stills
  but only *open* (read) the key ones: one representative frame per chapter plus
  the card↔chapter boundaries (seam check). Trust tsc + the templates for the rest.
- **Independent review is input-heavy** (a reviewer extracts and views many
  frames). Keep exactly one review; cap the frames it opens; a Sonnet reviewer
  is fine for a first pass. Skip only for a throwaway draft — never for a
  deliverable.

## Recommended hybrid (best cost/quality)

Chapters + assembly on **Sonnet/low**; the **one correctness-critical
independent review on Opus** (the review is where the C1/C2 accuracy catches
live — worth the stronger model). This keeps the fan-out cheap while protecting
the thing that most often ships wrong (invalid syntax, count mismatches).

## How to select

- User says "low-usage mode", "저사용량", "cheap/draft mode", "keep it under my
  Max limits", or names a batch ("10 videos") → run LOW-USAGE (or hybrid).
- Otherwise default to FULL for a single polished deliverable, but state the
  choice and offer LOW-USAGE if the user is on a subscription/Max plan.

## Applying it in the workflow

- **Subagents:** pass the override on each `Agent`/`Task` spawn — e.g.
  `subagent_type` default + `model: 'sonnet'`, `effort: 'low'`. See
  `chapter-subagent-prompt.md` (the override note at the top).
- **QA (workflow Stage 6):** render the full still set for your own record, but
  only Read/inspect the low-usage frame set listed above.
- **Review (Stage 7):** tell the reviewer subagent to open a capped number of
  frames (give it the exact frame list rather than "sample freely").
