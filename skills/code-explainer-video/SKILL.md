---
name: code-explainer-video
description: Produce a cinematic, chaptered explainer/tutorial VIDEO for a code, CLI, or dev-tool topic — a dark "Terminal Noir" console aesthetic (Remotion + syntax-highlighted code that types itself, streaming terminal output, dependency graphs, chapter cards, continuous BGM). Use when the user asks to make a video/tutorial/explainer/promo about a developer tool or command (Terraform, Docker, Kubernetes, Git, SQL, an SDK/API/CLI), a multi-chapter "N topics in one video" cut, or to replicate the Terraform 5-chapter manual. Builds chapters in parallel via subagents and encodes hard-won production rules (technical-accuracy validation, count reconciliation, seam fades, readability floors, deterministic render, tsc self-verify, independent review).
---

# Code Explainer Video

## Overview

This skill builds a polished, chaptered explainer video for any code/CLI/dev-tool
topic and renders it to MP4. The aesthetic is a dark IaC console ("Terminal
Noir"): deep indigo, violet accent, monospace code that writes itself, terminal
output that streams in, and dependency graphs that grow edges-before-nodes. It
ships a reusable Remotion engine (`src/lib`), topic-agnostic scene templates, a
parallel chapter-build workflow, and a distilled list of the mistakes that ruin
these videos so they aren't repeated.

Default shape: a single continuous ~4–5 minute cut of N (default 5) chapters —
intro → [chapter card + chapter] × N → outro — with one continuous music bed.
Each chapter can also be rendered as a standalone clip.

## When to use

Trigger when the request is to create a video that TEACHES or PROMOTES a
developer tool, command, or codebase concept — e.g. "make a video explaining
Docker Compose", "a 5-chapter Terraform tutorial video", "an animated intro for
my Kubernetes course", "turn these git commands into a short explainer". Also use
to reproduce or extend the Terraform 5-chapter manual. Not for live-action screen
recordings, non-code marketing videos, or full-length (30-min) narrated courses
with real voiceover — this produces short-per-chapter animated cuts.

Related skill: `video-shotcraft` (cinematic PRODUCT/webpage promos, its own shot
library, and the free-commercial audio this skill reuses). Prefer THIS skill when
the subject is code/CLI/dev-tooling and the format is chaptered explanation.

## How to use it

Follow `references/workflow.md` end-to-end. Read `references/pitfalls.md`
alongside every stage — it is the point of this skill. In short:

1. **Brief & chapter plan** — pick the topic, N distinct chapters (concept → do
   → connect → operate → scale), language (English default), the REAL syntax to
   show (verify accuracy; all data fictional), and the **usage profile** (Full
   vs Low-usage — see `references/usage-profiles.md`). Default to Full for a
   single polished deliverable; use Low-usage (Sonnet chapters, minimal image
   QA, one capped review) when the user is on a Claude subscription/Max plan,
   wants a cheap draft, or is batching many videos.
2. **Scaffold** — `scripts/scaffold_project.sh <target-dir> --audio` copies the
   engine + templates and installs deps (and the reused SFX/BGM). It renders a
   silent demo out-of-box. Design tokens live in `src/lib/theme.ts` — reuse them;
   never invent a second palette.
3. **Design beats** — each ~1440f chapter = 3–4 beats, each mapped to one
   template: CodeEditorScene / TerminalScene / GraphScene / a concept beat. One
   animation technique is the star once across the whole video.
4. **Build chapters IN PARALLEL** — one subagent per chapter using
   `references/chapter-subagent-prompt.md`; each self-verifies with tsc.
5. **Assemble** — wire intro + cards + chapters + outro on ONE timeline
   (`src/Main.tsx`), add captions + flash cuts, keep boundaries seam-free.
6. **Sound** — one continuous BGM bed + an SFX table pinned to relative frames.
7. **QA continuously** — render stills, look, extract keyframes.
8. **Independent review** — a clean-context subagent checks the finished MP4
   against `pitfalls.md` with frame evidence; fix, then final render.

## Resources

- `references/workflow.md` — the 8-stage pipeline (read first).
- `references/pitfalls.md` — the production rules / lessons learned; check EVERY
  item before delivery (correctness, determinism, readability, seams, sound).
- `references/usage-profiles.md` — Full vs Low-usage cost/usage tuning (which
  agent model/effort per stage, how many QA frames to open, review scope). On a
  Max/subscription plan, run subscription-auth by default and use Low-usage to
  stay within plan limits; fall back to an API key only for overflow.
- `references/scene-catalog.md` — API of every engine component + scene template.
- `references/chapter-subagent-prompt.md` — fill-in template for delegating one
  chapter to a parallel subagent.
- `assets/scaffold/` — the runnable Remotion project: `src/lib/` (engine, reuse
  as-is), `src/scenes/` (MasterIntro, MasterOutro, ChapterCard + CodeEditorScene/
  TerminalScene/GraphScene templates), `src/Main.tsx` (assembly template).
- `scripts/scaffold_project.sh` — copy the scaffold into a working dir + install.

Requirements: Node ≥ 18, ffmpeg (for keyframe QA), ~1 min render per minute of
video on a laptop. Audio is optional but expected; the `--audio` flag reuses the
`video-shotcraft` skill's free-commercial SFX/BGM.
