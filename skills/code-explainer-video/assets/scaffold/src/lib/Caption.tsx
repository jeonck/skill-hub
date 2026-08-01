// Bottom narration caption. A small amber-square-led English info-strip (texture
// register) sits above a large Korean narration line (>=56px effective height,
// aesthetic-rules Q11). Fades/rises in over 8f, out over the last 8f.
import { interpolate, useCurrentFrame } from 'remotion';
import { T } from './theme';

export const Caption: React.FC<{
  text: string;
  label?: string;
  duration: number;
  bottom?: number;
}> = ({ text, label, duration, bottom = 84 }) => {
  const frame = useCurrentFrame();
  const inT = interpolate(frame, [0, 9], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const outT = interpolate(frame, [duration - 9, duration], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const op = inT * outT;

  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        bottom,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 14,
        opacity: op,
        transform: `translateY(${(1 - inT) * 10}px)`,
        pointerEvents: 'none',
      }}
    >
      {label && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            fontFamily: T.mono,
            fontSize: 22,
            letterSpacing: '0.22em',
            textTransform: 'uppercase',
            color: T.dim,
          }}
        >
          <span style={{ width: 8, height: 8, background: T.accent }} />
          <span>{label}</span>
        </div>
      )}
      <div
        style={{
          fontFamily: T.sans,
          fontSize: 58,
          fontWeight: 700,
          letterSpacing: '-0.01em',
          color: T.text,
          textShadow: '0 2px 24px rgba(0,0,0,0.6)',
          textAlign: 'center',
          maxWidth: 1500,
        }}
      >
        {text}
      </div>
    </div>
  );
};
