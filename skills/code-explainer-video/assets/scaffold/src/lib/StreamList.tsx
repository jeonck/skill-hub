// Streaming output rows — adapted from ai-stream-response (StreamResponse.tsx):
// each row fades + rises + de-blurs over 12f on a staggered cue, with an
// optional status glyph resolving 3f behind the body.
import { interpolate, Easing, useCurrentFrame } from 'remotion';
import { T } from './theme';

const ease = Easing.bezier(0.2, 0.75, 0.25, 1);

export type Row = {
  glyph?: string; // e.g. '+', '-', '✓'
  glyphColor?: string;
  text: string;
  textColor?: string;
  meta?: string;
};

export const StreamList: React.FC<{
  rows: Row[];
  start: number;
  gap?: number; // frames between cues (slightly accelerating handled by caller if desired)
  rowH?: number;
  fontSize?: number;
}> = ({ rows, start, gap = 11, rowH = 52, fontSize = 27 }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: 'relative' }}>
      {rows.map((r, i) => {
        const cue = start + i * gap;
        const body = interpolate(frame, [cue, cue + 12], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: ease,
        });
        const status = interpolate(frame, [cue + 3, cue + 12], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
          easing: ease,
        });
        return (
          <div
            key={i}
            style={{
              height: rowH,
              display: 'flex',
              alignItems: 'center',
              gap: 16,
              fontFamily: T.mono,
              fontSize,
              opacity: body,
              transform: `translateY(${16 * (1 - body)}px)`,
              filter: body < 1 ? `blur(${5 * (1 - body)}px)` : undefined,
              whiteSpace: 'pre',
            }}
          >
            {r.glyph && (
              <span
                style={{
                  color: r.glyphColor ?? T.ok,
                  opacity: status,
                  width: 22,
                  display: 'inline-block',
                  fontWeight: 700,
                }}
              >
                {r.glyph}
              </span>
            )}
            <span style={{ color: r.textColor ?? T.text, flex: 1 }}>{r.text}</span>
            {r.meta && (
              <span style={{ color: T.dim, opacity: status, fontSize: fontSize - 4 }}>
                {r.meta}
              </span>
            )}
          </div>
        );
      })}
    </div>
  );
};
