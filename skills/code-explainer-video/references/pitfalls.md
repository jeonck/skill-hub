# pitfalls — hard-won lessons (check every one before delivery)

These are distilled from real review cycles. Each is a rule + why + how to self-check.
Numbered by category: C(correctness) R(render/determinism) V(visual) A(assembly) S(sound) P(process).

## Correctness — the code on screen must be REAL

- **C1. Validate every argument, block, and command against the real tool.** The
  video teaches; wrong syntax destroys credibility with the exact audience.
  *Real failure:* used `region` as an argument on a `aws_instance` resource —
  it is a provider-level setting, `terraform validate` errors. Fixed to
  `availability_zone`. *Check:* mentally run `<tool> validate`/`--help` on every
  snippet; if unsure, say so rather than invent.

- **C2. Numbers and counts must reconcile ACROSS beats.** If a plan says "5 to
  add" the graph must show 5, the summary must say 5, and the code must plausibly
  produce 5. *Real failures:* plan diff showed 1 resource but summary said "5 to
  add" and the graph built 5 nodes; a var set `count = 5` but the output list
  showed 4 IPs; a single `module "web"` block but apply addressed it as
  `module.web["dev"]` (for_each keys that can't exist without `for_each`). *Check:*
  pick every number/identifier shown and trace it to the code that justifies it.

- **C3. Don't repeat the same information as the "star" twice (P4).** One
  animation technique (typing / streaming rows / graph growth) is the lead once.
  If the hero already showed the attributes, the plan should show the resource
  SET, not repeat attributes. New beat = new information.

## Render / determinism

- **R1. No `Date.now()` / `Math.random()` / argless `new Date()`.** They break
  frame-reproducible rendering. Seed all pseudo-randomness from the element index
  (`mulberry32(seed)`, `hash01(i)` in lib/rand.ts).

- **R2. `Code` `lines` prop is `Line[]` (array of LINES), where each `Line` is
  `Tok[]`.** A single line is `[[{s:'...'}]]`, NOT `[{s:'...'}]`. Passing a bare
  `Line` throws `l.reduce is not a function`. *Check:* one line = doubly nested.

- **R3. Typing must fully reveal.** Compute `chars` by interpolating to a target
  ABOVE the block's character count, then switch to `undefined` after `TYPE_END`
  so the block shows fully and a caret rests. A target below the true length
  freezes typing mid-block forever. *Real failure:* capped `chars` at 150 on a
  ~168-char block — last lines never appeared.

## Visual

- **V1. Language consistency.** If the video is "all English", every UI label,
  badge, and caption is English — audit reused components for leftover text from
  a previous language. *Real failure:* one reused scene kept a Korean "STEP ·
  작성" badge in an otherwise-English cut. Make such text a prop with a default.

- **V2. Readability floors (Q11), measured in rendered pixels not fontSize.**
  Narration captions ≥ 56px (~5.2% of 1080). Auxiliary/label/URL ≥ 32px. Graph
  node labels ≥ 24px, status text ≥ 20px. Shrink a frame to 480px wide (phone
  test): every "meant-to-be-read" line must survive.

- **V3. Node/box width vs label length.** Fixed-width boxes clip long labels.
  Mono is ~0.6em/char; at 24px that's ~14.4px/char. Size boxes for the LONGEST
  label (e.g. `aws_security_group.web` = 22 chars ≈ 320px of text) plus padding.

- **V4. One glow / one spotlight sweep per hero, clipped to the element.** No
  group glints on batches of elements — batch entrances read through motion, not
  per-element light. Decorative sweeps must be clipped inside the border-radius.

- **V5. Hold key moments (R1/R3).** Wordmarks and landed hero code hold ≥ 1.5s.
  Batch entrances rest ~0.5s at the end. First cut is almost always too fast;
  slowing down was never once regretted. But avoid a fully static, caption-less
  stretch > ~3s (add a second narration caption or a subtle move).

## Assembly (multi-chapter cohesion)

- **A1. No dead frame at section boundaries (Q9).** Each outgoing scene fades its
  root to 0 over its last ~12f; each incoming scene must present content from
  local frame 0 (ramp in), and its persistent `Backdrop` must live OUTSIDE the
  content's opacity wrapper so at least the backdrop is always on. *Real failure:*
  chapter cards faded their whole root (backdrop included) from 0, so the boundary
  frame showed only the darker root backdrop → a 1-frame glow-drop flicker. Fix:
  backdrop always opaque; only the content fades.

- **A2. ONE continuous BGM track across the whole cut** — never restart music
  per chapter. Assemble all chapters into a SINGLE composition/timeline and lay
  one `<Audio>` bed with `volume={(f)=>interpolate(...)}` fade in/out.

- **A3. Captions sit at the bottom (`bottom: 84`), below centered windows.**
  Verify they don't collide with a scene's own bottom banner (e.g. an apply
  "complete" line) — offset the caption earlier in time if so.

- **A4. Reused scenes carry their old timings.** A scene with a self-fade tuned
  for a 40s cut can't simply be padded longer — it will fade out mid-hold. Either
  reuse at native duration with a cut, or remove the self-fade for the new
  context. Only scenes WITHOUT self-fades compose freely inside a longer chapter.

## Sound

- **S1. Cinematic vocabulary only** — whoosh (camera/transition), impact
  (landing), riser (build), sparkle (reveal), pop/tick (per-item). NEVER game-UI
  click/pluck/glass. BGM = strong-beat electronic (tech-house), ducked ~0.26 to
  leave headroom, auditioned inside the cut (not solo).

- **S2. Pin every SFX to a RELATIVE frame** (`section.from + offset`), never a
  bare absolute number — timelines shift and the whole table must follow. Ladder
  the volume on repeated hits (0.40→0.25) and alternate/space them so a volley
  doesn't machine-gun.

- **S3. Lock the picture before sound.** Any change to a scene's length/order
  means re-checking the whole SFX table for drift.

## Process

- **P1. Self-verify each parallel build in isolation.** When delegating chapters
  to subagents, each must run `npx tsc --noEmit -p tsconfig.json 2>&1 | grep -i
  <SceneName>` and get zero lines before reporting (other agents' in-flight files
  produce transient errors — grep to your own file).

- **P2. Static-frame QA is continuous, not final.** After each change render
  `npx remotion still ... --frame=N` and LOOK. Then render the whole cut and
  extract keyframes with ffmpeg (`select=eq(n\,N)`). Never ship a first render.

- **P3. Independent clean-context review before delivery.** Spawn a fresh
  subagent that did NOT build the video; give it the mp4, the frame map, and the
  rubric; have it report defects with frame-number evidence. The builder always
  has confirmation bias. Fix findings, then final render.

- **P4. Data safety.** All identifiers fictional — no real account IDs, keys,
  public IPs, or customer names. Use RFC-1918 IPs, `acme`/`example.dev`, obvious
  placeholders.
