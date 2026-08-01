# scene-catalog — the reusable engine (src/lib) + scene templates (src/scenes)

Everything is in `assets/scaffold/`. Reuse these; do not rewrite the lib or invent
a second palette. Read the actual files for full detail — signatures below.

## Engine — `src/lib/`

- **theme.ts** — `T` (design tokens) and `HCL` (syntax colors). Key tokens:
  `T.bg T.surface T.surface2 T.titlebar T.border T.borderSoft T.text T.dim
  T.faint T.accent T.accentGlow T.ok T.add T.warn T.cyan T.pink T.danger
  T.mono T.sans`. `HCL.keyword|type|name|attr|string|number|comment|punct|plain`.
  ALL on-screen color comes from here (visual-language consistency).

- **Backdrop.tsx** — `<Backdrop glow={0.5} glowY={46} />`. Dark indigo + dot grid
  + single soft center glow + vignette. The floor of every scene.

- **Window.tsx** — `<Window width height title accentDot glow>{children}</Window>`.
  Dark window chrome (titlebar + 3 dots + filename). Content area is `position:
  relative`. Used for editor and terminal.

- **Code.tsx** — syntax-highlighted code with deterministic typing + block caret.
  Types: `Tok = {s: string, c?: string}`, `Line = Tok[]`.
  `<Code lines={Line[]} chars={number|undefined} fontSize={33} lineHeight={1.6}
  caret />`. `chars=undefined` shows all; a number reveals that many chars across
  the whole block. Helper `typedChars(frame, start, speed=2)`. `<Caret h on
  color/>` for a standalone caret. **Gotcha: `lines` is Line[] — a single line is
  `[[{s:'...'}]]` (pitfalls R2). Reveal target must exceed block length (R3).**

- **StreamList.tsx** — streamed output rows (each fades+rises+deblurs on a
  staggered cue, status glyph resolves 3f behind). `Row = {glyph?, glyphColor?,
  text, textColor?, meta?}`. `<StreamList rows={Row[]} start gap={11} rowH={52}
  fontSize={27} />`. For terminal output, plan diffs, evidence lists.

- **DigitRoll.tsx** — odometer digit roll. `<DigitRoll value="5" delay={frame}
  fontSize color />`. For counts ("5 to add", "18 added").

- **Caption.tsx** — bottom narration. `<Caption text={string} label={string?}
  duration={number} bottom={84} />`. `text` is the large ≥58px line; `label` is a
  small uppercase accent kicker. Fades in/out at its window edges.

- **FlashCut.tsx** — `<FlashCut duration={10} />`. A cool-white bloom over a hard
  cut; place at scene boundaries via a `<Sequence from={cut-5} durationInFrames={10}>`.

- **rand.ts** — `mulberry32(seed)` deterministic PRNG, `hash01(i)` index→[0,1).
  Seed every random from the element index (determinism, pitfalls R1).

## Scene templates — `src/scenes/`

Frame components. The three beat templates fade themselves out over their last
12 frames (safe to place back-to-back).

- **CodeEditorScene.tsx** — a code file writes itself under a spotlight + gentle
  3D push, then holds. `{title, lines: Line[], step?, duration, typeStart?,
  typeEnd?, charTarget?, width?, height?}`. Beat: "here's the code".

- **TerminalScene.tsx** — command types in, output rows stream, optional green
  success line. `{cwd?, command: Line, commandLen, rows: Row[], success?,
  duration, rowsStart?, width?, height?}`. Beat: "run the command".

- **GraphScene.tsx** — dependency graph; elbow edges GROW before child nodes pop
  (spring), nodes resolve to "ready". `{nodes: GNode[], extraEdges?, headline?,
  banner?, duration}`. `GNode = {id, x, y, parent, level, label, sub?, root?}`.
  Beat: "how the pieces connect". Keep boxes wide for long labels (V3).

- **ChapterCard.tsx** — chapter divider. `{n: "01", title, sub, duration}`.
  Backdrop is always-on (no boundary dead frame, A1).

- **MasterIntro.tsx** — series open. `{duration, comment?, wordA?, wordB?,
  subtitle?, tagline?}`. Typed comment → wordmark stamp → subtitle.

- **MasterOutro.tsx** — series close (energy peak). `{chips?: string[]≤5, kicker?,
  wordA?, wordB?, cta?, footer?}`. Chapter chips fly into a recap rail, wordmark
  slams in with particles, CTA holds.

## Assembly — `src/Main.tsx`

Cumulative frame allocator `b` + intro/cards/chapters/outro + captions + flashes,
plus a commented continuous-BGM + SFX block. Renders out-of-box as a silent demo;
replace the three example chapters with real ones and uncomment audio.
`Root.tsx` registers composition id `Explainer` at 1920×1080 / 30fps.
