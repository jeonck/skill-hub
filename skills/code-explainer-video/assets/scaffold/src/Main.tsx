// ASSEMBLY TEMPLATE — intro -> [chapter card + chapter] x N -> outro, on one
// continuous timeline. This demo wires the three template scenes as example
// chapters so `npm run render` works out-of-box (silent). Replace each chapter
// with a real self-contained ~1440f chapter component (see references/workflow.md
// and references/chapter-subagent-prompt.md), and add audio (see the AUDIO block).
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame } from 'remotion';
// import { Audio, staticFile } from 'remotion'; // <- uncomment for audio
import { T, HCL } from './lib/theme';
import { Backdrop } from './lib/Backdrop';
import { FlashCut } from './lib/FlashCut';
import { Caption } from './lib/Caption';
import { Line } from './lib/Code';
import { MasterIntro } from './scenes/MasterIntro';
import { ChapterCard } from './scenes/ChapterCard';
import { MasterOutro } from './scenes/MasterOutro';
import { CodeEditorScene } from './scenes/CodeEditorScene';
import { TerminalScene } from './scenes/TerminalScene';
import { GraphScene, GNode } from './scenes/GraphScene';

const CARD = 70;
const CH = 1440;

// cumulative frame allocator — sections never overlap, no manual math.
const b = (() => {
  let f = 0;
  const at = (d: number) => { const from = f; f += d; return { from, duration: d }; };
  return {
    intro: at(210),
    card1: at(CARD), ch1: at(CH),
    card2: at(CARD), ch2: at(CH),
    card3: at(CARD), ch3: at(CH),
    outro: at(300),
    total: f,
  };
})();
export const TOTAL = b.total;

// ---- placeholder chapter content (replace with your topic) ----
const DEMO_CODE: Line[] = [
  [{ s: 'service', c: HCL.keyword }, { s: ' ', c: HCL.plain }, { s: '"api"', c: HCL.name }, { s: ' {', c: HCL.punct }],
  [{ s: '  image', c: HCL.attr }, { s: '   = ', c: HCL.punct }, { s: '"acme/api:1.4"', c: HCL.string }],
  [{ s: '  port', c: HCL.attr }, { s: '    = ', c: HCL.punct }, { s: '8080', c: HCL.number }],
  [{ s: '  replicas', c: HCL.attr }, { s: ' = ', c: HCL.punct }, { s: '3', c: HCL.number }],
  [{ s: '}', c: HCL.punct }],
];
const DEMO_NODES: GNode[] = [
  { id: 0, x: 960, y: 300, parent: -1, level: 0, label: 'service.api', sub: 'root', root: true },
  { id: 1, x: 650, y: 560, parent: 0, level: 1, label: 'config.env' },
  { id: 2, x: 1270, y: 560, parent: 0, level: 1, label: 'secret.token' },
  { id: 3, x: 960, y: 800, parent: 1, level: 2, label: 'volume.data' },
];

const CARDS = [
  { s: b.card1, n: '01', title: 'Declare', sub: 'describe it in code' },
  { s: b.card2, n: '02', title: 'Run', sub: 'one command' },
  { s: b.card3, n: '03', title: 'Connect', sub: 'how the pieces relate' },
];

const CAPTIONS = [
  { from: b.ch1.from + 60, duration: 120, label: 'chapter 01', text: 'Describe the thing in a single file' },
  { from: b.ch2.from + 60, duration: 120, label: 'chapter 02', text: 'One command brings it to life' },
  { from: b.ch3.from + 60, duration: 120, label: 'chapter 03', text: 'Everything wires together' },
];

export const Main: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: T.bg }}>
      {/* ── AUDIO (see references/workflow.md §Sound) ───────────────────────
      <Audio src={staticFile('audio/bgm.mp3')} volume={(f) =>
        interpolate(f, [0, 30, TOTAL - 60, TOTAL], [0, 0.26, 0.26, 0],
          { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })} />
      {SFX.map((s, i) => (
        <Sequence key={i} from={s.from} durationInFrames={s.dur ?? 90}>
          <Audio src={staticFile(`audio/${s.src}`)} volume={s.volume} />
        </Sequence>
      ))}
      ──────────────────────────────────────────────────────────────────── */}

      <Backdrop glow={0} />

      <Sequence from={b.intro.from} durationInFrames={b.intro.duration}>
        <MasterIntro duration={b.intro.duration} comment="# your topic here" wordA="TOPIC" wordB="NAME" subtitle="What the viewer will be able to do" tagline="3 chapters · one workflow" />
      </Sequence>

      {CARDS.map((cd) => (
        <Sequence key={cd.n} from={cd.s.from} durationInFrames={cd.s.duration}>
          <ChapterCard n={cd.n} title={cd.title} sub={cd.sub} duration={cd.s.duration} />
        </Sequence>
      ))}

      {/* Replace these three template scenes with real multi-beat chapters. */}
      <Sequence from={b.ch1.from} durationInFrames={b.ch1.duration}>
        <CodeEditorScene title="service.hcl" lines={DEMO_CODE} step="STEP · DECLARE" duration={b.ch1.duration} charTarget={160} />
      </Sequence>
      <Sequence from={b.ch2.from} durationInFrames={b.ch2.duration}>
        <TerminalScene
          command={[{ s: '$ ', c: T.faint }, { s: 'acme', c: T.text }, { s: ' up', c: T.accent }]}
          commandLen={8}
          rows={[
            { glyph: '-', glyphColor: T.dim, text: 'Pulling acme/api:1.4', textColor: T.dim },
            { glyph: '-', glyphColor: T.dim, text: 'Starting 3 replicas', textColor: T.text },
            { glyph: '✓', glyphColor: T.ok, text: 'api is healthy', textColor: T.text, meta: 'ready' },
          ]}
          success="✓ Stack is up on http://localhost:8080"
          duration={b.ch2.duration}
        />
      </Sequence>
      <Sequence from={b.ch3.from} durationInFrames={b.ch3.duration}>
        <GraphScene nodes={DEMO_NODES} headline="how the pieces connect" banner="✓ 4 components wired" duration={b.ch3.duration} />
      </Sequence>

      <Sequence from={b.outro.from} durationInFrames={b.outro.duration}>
        <MasterOutro chips={['01 · declare', '02 · run', '03 · connect']} kicker="the complete guide" wordA="Master " wordB="Acme" cta="Start now →" footer="Full course · example.dev" />
      </Sequence>

      {CAPTIONS.map((cp) => (
        <Sequence key={cp.from} from={cp.from} durationInFrames={cp.duration}>
          <Caption text={cp.text} label={cp.label} duration={cp.duration} />
        </Sequence>
      ))}

      {[b.ch1.from, b.ch2.from, b.ch3.from, b.outro.from].map((cut) => (
        <Sequence key={cut} from={cut - 5} durationInFrames={10}>
          <FlashCut duration={10} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
