// Chapter divider card: "CHAPTER 0N" + big title + one-line subtitle.
// Present from local frame 0 (no seam), holds, fades out. ~70f.
import { AbsoluteFill, interpolate, Easing, useCurrentFrame } from 'remotion';
import { Backdrop } from '../lib/Backdrop';
import { T } from '../lib/theme';

export const ChapterCard: React.FC<{
  n: string; // "01"
  title: string;
  sub: string;
  duration: number;
}> = ({ n, title, sub, duration }) => {
  const frame = useCurrentFrame();
  const inT = interpolate(frame, [0, 8], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  const out = interpolate(frame, [duration - 10, duration], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const rule = interpolate(frame, [6, 30], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  const subIn = interpolate(frame, [12, 24], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill>
      {/* backdrop always on (no dead frame at the card boundary) */}
      <Backdrop glow={0.5} glowY={50} />
      <AbsoluteFill
        style={{
          opacity: inT * out,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 22,
        }}
      >
        <div
          style={{
            fontFamily: T.mono,
            fontSize: 30,
            letterSpacing: '0.4em',
            textTransform: 'uppercase',
            color: T.accent,
            transform: `translateY(${(1 - inT) * -10}px)`,
          }}
        >
          Chapter {n}
        </div>
        <div
          style={{
            width: 360 * rule,
            height: 3,
            background: `linear-gradient(90deg, transparent, ${T.accent}, transparent)`,
          }}
        />
        <div
          style={{
            fontFamily: T.sans,
            fontSize: 108,
            fontWeight: 800,
            letterSpacing: '-0.03em',
            color: T.text,
            transform: `scale(${0.96 + 0.04 * inT})`,
          }}
        >
          {title}
        </div>
        <div
          style={{
            fontFamily: T.mono,
            fontSize: 32,
            color: T.dim,
            opacity: subIn,
          }}
        >
          {sub}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
