// TEMPLATE — a terminal window: a command types in, then output rows stream in
// (StreamList), and an optional green success line lands. Use for CLI beats
// (`git ...`, `docker ...`, `kubectl ...`, `terraform ...`, `npm ...`).
import { AbsoluteFill, interpolate, Easing, useCurrentFrame } from 'remotion';
import { Backdrop } from '../lib/Backdrop';
import { Window } from '../lib/Window';
import { Code, Line, typedChars } from '../lib/Code';
import { StreamList, Row } from '../lib/StreamList';
import { T, HCL } from '../lib/theme';

export const TerminalScene: React.FC<{
  cwd?: string; // dim context line, e.g. '~/project (main)'
  command: Line; // one line, e.g. [{s:'$ '},{s:'git'},{s:' status'}]
  commandLen: number; // char count of the command (for caret timing)
  rows: Row[]; // streamed output rows
  success?: string; // optional final green line
  duration: number;
  rowsStart?: number;
  width?: number;
  height?: number;
}> = ({ cwd = '~/project (main)', command, commandLen, rows, success, duration, rowsStart = 74, width = 1240, height = 640 }) => {
  const frame = useCurrentFrame();
  const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;
  const chars = typedChars(frame, 12, 2);
  const cmdDone = chars >= commandLen;
  const out = interpolate(frame, [50, 60], [0, 1], clamp);
  const succ = interpolate(frame, [rowsStart + rows.length * 12 + 8, rowsStart + rows.length * 12 + 20], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const fadeOut = interpolate(frame, [duration - 12, duration], [1, 0], clamp);

  return (
    <AbsoluteFill style={{ opacity: fadeOut }}>
      <Backdrop glow={0.4} glowY={44} />
      <AbsoluteFill style={{ display: 'grid', placeItems: 'center' }}>
        <Window width={width} height={height} title={`terminal — ${cwd}`}>
          <div style={{ padding: '32px 44px', height: '100%', boxSizing: 'border-box', fontFamily: T.mono }}>
            <div style={{ color: T.faint, fontSize: 24, marginBottom: 14 }}>{cwd}</div>
            <Code lines={[command]} chars={cmdDone ? undefined : chars} fontSize={31} caret={!cmdDone} />
            <div style={{ opacity: out, marginTop: 20 }}>
              <StreamList start={rowsStart} gap={12} rows={rows} />
              {success && (
                <div style={{ marginTop: 18, fontSize: 30, color: HCL.string, fontWeight: 600, opacity: succ, transform: `translateY(${(1 - succ) * 8}px)` }}>
                  {success}
                </div>
              )}
            </div>
          </div>
        </Window>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
