// Master intro for a chaptered explainer. Cold caret types a mono comment, then
// the series wordmark stamps in with subtitle + tagline, holds, fades out.
// Prop-driven so it works for any topic — pass your own text.
import { AbsoluteFill, interpolate, Easing, useCurrentFrame } from 'remotion';
import { Backdrop } from '../lib/Backdrop';
import { Code, typedChars } from '../lib/Code';
import { T, HCL } from '../lib/theme';

const TYPE_START = 16;
const HEAD_START = 84;

export const MasterIntro: React.FC<{
  duration: number;
  comment?: string; // typed mono kicker, e.g. '# infrastructure as code'
  wordA?: string; // wordmark, plain half
  wordB?: string; // wordmark, accent half
  subtitle?: string;
  tagline?: string; // small uppercase accent line
}> = ({
  duration,
  comment = '# your topic here',
  wordA = 'TOPIC',
  wordB = 'NAME',
  subtitle = 'One-line promise — what the viewer will learn',
  tagline = '5 chapters · one workflow',
}) => {
  const frame = useCurrentFrame();
  const chars = typedChars(frame, TYPE_START, 2);
  const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

  const kick = interpolate(frame, [HEAD_START, HEAD_START + 16], [1, 0.5], clamp);
  const headIn = interpolate(frame, [HEAD_START, HEAD_START + 14], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const headScale = interpolate(frame, [HEAD_START, HEAD_START + 18], [1.08, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const rule = interpolate(frame, [HEAD_START + 14, HEAD_START + 42], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const subIn = interpolate(frame, [HEAD_START + 24, HEAD_START + 40], [0, 1], clamp);
  const fadeOut = interpolate(frame, [duration - 12, duration], [1, 0], clamp);

  return (
    <AbsoluteFill style={{ opacity: fadeOut }}>
      <Backdrop glow={0.6} glowY={48} />
      <AbsoluteFill style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 26 }}>
        <div style={{ opacity: kick, transform: `translateY(${(1 - kick) * -6}px)` }}>
          <Code lines={[[{ s: comment, c: HCL.comment }]]} chars={chars} fontSize={32} caret={frame < HEAD_START} />
        </div>
        <div style={{ opacity: headIn, transform: `scale(${headScale})`, fontFamily: T.sans, fontSize: 150, fontWeight: 800, letterSpacing: '0.02em', color: T.text, lineHeight: 1 }}>
          {wordA}<span style={{ color: T.accent }}>{wordB}</span>
        </div>
        <div style={{ width: 620 * rule, height: 4, background: `linear-gradient(90deg, transparent, ${T.accent}, transparent)`, opacity: headIn }} />
        <div style={{ opacity: subIn, fontFamily: T.mono, fontSize: 34, color: T.dim }}>{subtitle}</div>
        <div style={{ opacity: subIn, fontFamily: T.mono, fontSize: 24, letterSpacing: '0.34em', textTransform: 'uppercase', color: T.accent, marginTop: 6 }}>{tagline}</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
