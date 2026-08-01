# chapter-subagent-prompt — template for delegating ONE chapter in parallel

Spawn one subagent per new chapter (general-purpose). They write independent files
(`src/scenes/Chapter<Name>.tsx`), so they run concurrently with no conflict. Fill
the ⟨…⟩ slots and paste. Keep the API facts verbatim — they prevent the common
failures.

> **Usage profile (see `usage-profiles.md`):** in Low-usage mode, spawn each
> chapter subagent with `model: 'sonnet'` and `effort: 'low'` — chapter TSX is
> well-specified mechanical work against the templates, so Sonnet handles it and
> the 5-way fan-out is the biggest single cost. Full mode inherits the session
> model. Either way, keep the tsc self-verify step below.

---

Build one self-contained Remotion "chapter" scene for a dark, cinematic ⟨LANGUAGE⟩
⟨TOPIC⟩ explainer video. Project root: ⟨ABSOLUTE PROJECT PATH⟩ (Remotion 4, React
19, 30fps, 1920×1080). Determinism is mandatory: NO Date.now()/Math.random()/
new Date() — seed any randomness from index (helpers in src/lib/rand.ts).

## FIRST read these for the exact API + house style (do not skip)
- src/lib/theme.ts   → import { T, HCL }  (tokens + fonts)
- src/lib/Backdrop.tsx, src/lib/Window.tsx
- src/lib/Code.tsx   → Code, Line, Tok, typedChars, Caret.
  `lines` is Line[] where Line = Tok[] and Tok = {s:string, c?:string}; a single
  line is [[{s:'...',c:T.text}]]. `chars=undefined` shows all; to type, interpolate
  chars to a value ABOVE the block length then use undefined after TYPE_END.
- src/lib/StreamList.tsx → StreamList, Row={glyph?,glyphColor?,text,textColor?,meta?}
- src/lib/DigitRoll.tsx
- src/scenes/CodeEditorScene.tsx, TerminalScene.tsx, GraphScene.tsx  ← MIRROR
  these template scenes' structure, timing, and quality bar; you may compose them.

## Deliverable
Create ONE file: src/scenes/⟨ChapterName⟩.tsx exporting
`export const ⟨ChapterName⟩: React.FC = () => {…}` — NO props, self-contained,
`const SCENE_DUR = 1440`. Root `<AbsoluteFill>` holds a persistent `<Backdrop/>`
then ⟨3–4⟩ beats sequenced with nested `<Sequence from={..} durationInFrames={..}>`
(import Sequence, AbsoluteFill, interpolate, Easing, useCurrentFrame from 'remotion';
add spring, useVideoConfig if you build a graph). Fade the WHOLE scene out over its
last 12 frames (opacity → 0), gated on useCurrentFrame vs SCENE_DUR. Do NOT add
bottom captions (the parent adds them). Do NOT modify Root.tsx, index.ts, Main.tsx,
or any other file. ⟨LANGUAGE⟩ on-screen text only. All data fictional.

## Content — beats (each ~340–460f)
⟨SPELL OUT EACH BEAT: the exact code/HCL/commands/output/graph, verified against
the real tool. Numbers and identifiers must reconcile across beats. Highlight
cross-references (e.g. var.x, module.y.z) in T.accent. Graph node boxes ≥360px so
long labels don't clip; node labels ≥24px, status ≥20px.⟩

## Self-verify before finishing (required)
Run: cd ⟨PROJECT PATH⟩ && npx tsc --noEmit -p tsconfig.json 2>&1 | grep -i "⟨ChapterName⟩"
It MUST print nothing (ignore errors that don't name your file — other chapters are
being written in parallel). Fix until clean.

Report: the file path, each beat's frame range, and confirm tsc was clean. Be brief.

---

After all chapters return: read each file, render one still per chapter to eyeball
it (`npx remotion still src/index.ts Explainer out/qa/chN.png --frame=<mid>`), wire
them into Main.tsx, then run the independent review (workflow Stage 7).
