# workflow — building a chaptered code/CLI explainer video

Goal: an N-chapter (default 5) ~40–60s-per-chapter cinematic explainer for a
code/CLI/dev-tool topic, on ONE continuous timeline, English by default. Uses
Remotion (React → deterministic MP4). Read `pitfalls.md` alongside every stage.

## Stage 0 — Brief & chapter plan (do first, write it down)

Decide and record:
- **Topic** and **audience** (e.g. "Docker Compose for backend devs").
- **Chapters** — N distinct sub-topics with a natural progression (concept →
  do → connect → operate → scale). Each chapter must add NEW information (C3/P4).
- **Language** (default English; if another, every UI string follows — V1).
- **Deliverable** — one integrated cut (recommended) and/or per-chapter clips.
- **Accuracy anchor** — the real syntax/commands you'll show. Verify them (C1/C2).
  All data fictional (P4).

Example 5-chapter plan (the worked reference — Terraform):
`01 Initialize · 02 Write & Apply · 03 Variables · 04 State · 05 Modules`.

## Stage 1 — Scaffold the project

Copy `assets/scaffold/` into a working dir and install:
```
scripts/scaffold_project.sh <target-dir>     # copies scaffold + npm install
```
This gives: `src/lib/` (the engine — do NOT rewrite), `src/scenes/` (MasterIntro,
MasterOutro, ChapterCard + CodeEditorScene/TerminalScene/GraphScene templates),
`src/Main.tsx` (assembly template, renders out-of-box as a silent demo).
Design tokens live in `src/lib/theme.ts` — reuse them everywhere; do not invent a
second palette. See `scene-catalog.md` for every component's API.

## Stage 2 — Design each chapter's beats

A chapter ≈ 1440 frames (48s) with 3–4 beats. Map each beat to ONE template:
- "here's the code" → **CodeEditorScene** (a file types itself)
- "run the command" → **TerminalScene** (command + streaming output rows)
- "how it connects" → **GraphScene** (dependency graph, edges before nodes)
- concept/transition → a simple centered-text beat (see ChapterInitialize in the
  worked example, or MasterIntro's structure)
Each animation technique is the star once across the whole video (C3). Reserve
hold/rest frames up front (V5).

## Stage 3 — Build chapters IN PARALLEL

Each chapter is a self-contained `~1440f` component (root `<AbsoluteFill>` +
persistent `<Backdrop>` + internal `<Sequence>` beats + whole-scene fade-out over
the last 12f). Because chapters are independent files, delegate them to parallel
subagents — one per chapter — using the template in
`chapter-subagent-prompt.md`. Each subagent MUST self-verify with tsc (P1).
Simple chapters (reusing existing scenes) you can assemble yourself.

## Stage 4 — Assemble the timeline (Main.tsx)

Use the cumulative frame allocator (`b.at(d)`) so sections never overlap. Order:
MasterIntro → [ChapterCard + Chapter] × N → MasterOutro. Add:
- **Chapter cards** — `ChapterCard` announces each chapter (number/title/sub).
- **Captions** — one short narration line early in each chapter (`Caption`,
  bottom, ≥56px). Avoid collisions (A3).
- **FlashCut** at each chapter start (and outro) to punch the transition.
- Boundary hygiene: no dead frames (A1).

## Stage 5 — Sound

Read `pitfalls.md` §S. Copy audio into `public/audio/` (the sibling skill
`video-shotcraft` bundles free-commercial SFX + a tech-house BGM at
`~/.agents/skills/video-shotcraft/assets/audio/`; reuse those files). Lay ONE
continuous BGM bed (A2) + an SFX table pinned to relative section starts (S2).
Uncomment the AUDIO block in `Main.tsx`. Vocabulary: whoosh/impact/riser/sparkle/
pop/tick only (S1). Lock picture first (S3).

## Stage 6 — QA (continuous)

> **Usage profile:** in Low-usage mode, still render the frames, but only Read/
> inspect the key set — one representative frame per chapter + the card↔chapter
> boundaries (seam check), ~6–10 images total. Each 1080p still is up to ~4.8k
> image input tokens, so opening dozens is the sleeper cost. See
> `usage-profiles.md`. Full mode: inspect 1–2 frames per beat.

After every change: `npx remotion still src/index.ts Explainer out/qa/fN.png
--frame=N` and LOOK (P2). Then render the whole cut and extract keyframes:
```
npx remotion render src/index.ts Explainer out/video.mp4
ffmpeg -v error -i out/video.mp4 -vf "select=eq(n\,N)" -vsync 0 out/qa/rN.png -y
```
Confirm audio present: `ffprobe -v error -show_entries stream=codec_type ...`.

## Stage 7 — Independent review + deliver

Spawn a clean-context subagent that did NOT build the video (P3). Give it: the
mp4, the section→frame map, `pitfalls.md`, and ask for SHIP/FIX-FIRST with
frame-evidence findings. Prioritize correctness (C1/C2) and language (V1) first.
Apply fixes, re-render, deliver the mp4 + a short section summary.

> **Usage profile:** keep exactly ONE review for a deliverable (skip only for a
> throwaway draft). In Low-usage mode, give the reviewer an explicit capped
> frame list (~8–10) rather than "sample freely", since it opens every frame it
> checks. The recommended hybrid is chapters/assembly on Sonnet but this one
> correctness review on Opus — it's where invalid syntax and count mismatches
> get caught. See `usage-profiles.md`.

## Render economics

~1200f renders in ~25s; a 5-chapter ~8000f cut in ~2.5 min on a laptop (2 cores).
Parallel chapter authoring is the real time saver, not render.
