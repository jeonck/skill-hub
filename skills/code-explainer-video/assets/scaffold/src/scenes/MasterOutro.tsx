// Master outro for a chaptered explainer. Chapter chips fly in and line up as a
// recap rail, then the wordmark slams in with a particle burst and a CTA, and
// holds. Energy peak, hold >= 1.5s. Prop-driven — pass chips/wordmark/cta.
import {
  AbsoluteFill,
  interpolate,
  Easing,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { Backdrop } from '../lib/Backdrop';
import { mulberry32 } from '../lib/rand';
import { T } from '../lib/theme';

const STAMP = 58;
const ROW_Y = 232;
// up to 5 evenly spaced columns; chips beyond 5 will overlap, so keep <= 5.
const COL_X = [360, 690, 1020, 1350, 1620];

const Particles: React.FC = () => {
  const frame = useCurrentFrame();
  const rnd = mulberry32(4471);
  const parts = Array.from({ length: 22 }, () => ({
    x: 620 + rnd() * 680,
    delay: rnd() * 10,
    dur: 42 + rnd() * 32,
    drift: (rnd() - 0.5) * 130,
    size: 3 + rnd() * 4,
  }));
  return (
    <>
      {parts.map((p, i) => {
        const t = interpolate(frame, [STAMP + p.delay, STAMP + p.delay + p.dur], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
        if (t <= 0 || t >= 1) return null;
        const op = interpolate(t, [0, 0.2, 1], [0, 1, 0]);
        return (
          <div key={i} style={{ position: 'absolute', left: p.x + p.drift * t, top: 540 - t * 280, width: p.size, height: p.size, borderRadius: p.size, background: T.accent, opacity: op, boxShadow: `0 0 8px ${T.accentGlow}` }} />
        );
      })}
    </>
  );
};

export const MasterOutro: React.FC<{
  chips?: string[]; // chapter recap labels, <= 5
  kicker?: string;
  wordA?: string; // wordmark plain half
  wordB?: string; // wordmark accent half
  cta?: string;
  footer?: string;
}> = ({
  chips = ['01 · one', '02 · two', '03 · three', '04 · four', '05 · five'],
  kicker = 'the complete guide',
  wordA = 'Master ',
  wordB = 'It',
  cta = 'Start now →',
  footer = 'Full course · example.dev',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

  const stampS = spring({ frame: frame - STAMP, fps, config: { damping: 13, stiffness: 150 } });
  const stampScale = interpolate(stampS, [0, 1], [1.14, 1]);
  const wordIn = interpolate(frame, [STAMP, STAMP + 8], [0, 1], clamp);
  const flash = interpolate(frame, [STAMP - 2, STAMP + 3, STAMP + 16], [0, 0.6, 0], clamp);
  const ctaIn = interpolate(frame, [STAMP + 14, STAMP + 30], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const ctaPulse = 0.5 + 0.5 * Math.sin((frame - STAMP) * 0.12);
  const subIn = interpolate(frame, [STAMP + 24, STAMP + 40], [0, 1], clamp);

  return (
    <AbsoluteFill>
      <Backdrop glow={1} glowY={46} />
      {chips.slice(0, 5).map((label, i) => {
        const start = i * 4;
        const p = spring({ frame: frame - start, fps, config: { damping: 15, stiffness: 95 } });
        const y = ROW_Y + (i % 2 === 0 ? -1 : 1) * 240 * (1 - p);
        const dim = interpolate(frame, [STAMP, STAMP + 14], [1, 0.6], clamp);
        return (
          <div key={i} style={{ position: 'absolute', left: COL_X[i], top: y, transform: `translate(-50%,-50%) scale(${p})`, opacity: p * dim, fontFamily: T.mono, fontSize: 25, color: T.cyan, background: T.surface, border: `1px solid ${T.border}`, borderRadius: 12, padding: '14px 22px', boxShadow: '0 12px 30px rgba(0,0,0,0.45)', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', gap: 12 }}>
            <span style={{ width: 10, height: 10, borderRadius: 6, background: T.ok }} />
            {label}
          </div>
        );
      })}

      <Particles />

      <AbsoluteFill style={{ background: 'radial-gradient(ellipse 50% 40% at 50% 50%, rgba(11,14,22,0.86), transparent 70%)', opacity: wordIn }} />

      <AbsoluteFill style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 20 }}>
        <div style={{ opacity: wordIn, transform: `scale(${stampScale})`, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12 }}>
          <div style={{ fontFamily: T.mono, fontSize: 24, letterSpacing: '0.36em', textTransform: 'uppercase', color: T.accent }}>{kicker}</div>
          <div style={{ fontFamily: T.sans, fontSize: 122, fontWeight: 800, letterSpacing: '-0.03em', color: T.text, lineHeight: 1 }}>
            {wordA}<span style={{ color: T.accent }}>{wordB}</span>
          </div>
        </div>
        <div style={{ marginTop: 24, opacity: ctaIn, transform: `translateY(${(1 - ctaIn) * 12}px)`, fontFamily: T.sans, fontSize: 38, fontWeight: 700, color: '#0B0E16', background: T.accent, borderRadius: 16, padding: '18px 46px', boxShadow: `0 0 ${28 + 20 * ctaPulse}px ${T.accentGlow}` }}>{cta}</div>
        <div style={{ opacity: subIn, fontFamily: T.mono, fontSize: 26, color: T.dim, marginTop: 4 }}>{footer}</div>
      </AbsoluteFill>

      <AbsoluteFill style={{ pointerEvents: 'none', opacity: flash, background: 'radial-gradient(ellipse at 50% 45%, rgba(200,196,255,0.9), rgba(139,123,255,0.35) 55%, transparent 78%)' }} />
    </AbsoluteFill>
  );
};
