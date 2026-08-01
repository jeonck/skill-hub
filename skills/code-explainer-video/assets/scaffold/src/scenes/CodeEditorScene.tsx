// TEMPLATE — a code block writes itself in an editor window under a spotlight +
// gentle 3D push, then holds. Use for "here is the code" beats. Topic-agnostic:
// pass `title` + `lines` (see lib/Code.tsx for the Line/Tok syntax-color model).
//
// Determinism: typing is a pure function of frame (no Date.now/Math.random).
// The `chars` trick — interpolate to a value ABOVE the block length, then switch
// to undefined after TYPE_END so the block fully reveals and a caret rests.
import { AbsoluteFill, interpolate, Easing, useCurrentFrame } from 'remotion';
import { Backdrop } from '../lib/Backdrop';
import { Window } from '../lib/Window';
import { Code, Line } from '../lib/Code';
import { T } from '../lib/theme';

export const CodeEditorScene: React.FC<{
  title: string; // window filename, e.g. 'main.tf'
  lines: Line[]; // syntax-colored code (Tok[][])
  step?: string; // corner badge, e.g. 'STEP · WRITE'
  duration: number;
  typeStart?: number;
  typeEnd?: number;
  charTarget?: number; // set ABOVE the block's char count; see note above
  width?: number;
  height?: number;
}> = ({ title, lines, step, duration, typeStart = 34, typeEnd = 150, charTarget = 220, width = 980, height = 560 }) => {
  const frame = useCurrentFrame();
  const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

  const chars = frame >= typeEnd ? undefined : Math.floor(interpolate(frame, [typeStart, typeEnd], [0, charTarget], { ...clamp, easing: Easing.inOut(Easing.sin) }));
  const win = interpolate(frame, [0, 22], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const rotY = interpolate(frame, [0, 90], [7, 0], { ...clamp, easing: Easing.out(Easing.cubic) });
  const scale = interpolate(frame, [0, 90], [0.93, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const sweep = interpolate(frame, [40, 96], [-30, 130], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const sweepOp = interpolate(frame, [40, 60, 96], [0, 0.5, 0], clamp);
  const fadeOut = interpolate(frame, [duration - 12, duration], [1, 0], clamp);

  return (
    <AbsoluteFill style={{ opacity: fadeOut }}>
      <Backdrop glow={0.7} glowY={46} />
      <AbsoluteFill style={{ display: 'grid', placeItems: 'center', perspective: 1600 }}>
        <div style={{ opacity: win, transform: `translateY(${(1 - win) * 26}px) rotateY(${rotY}deg) scale(${scale})`, transformStyle: 'preserve-3d' }}>
          <Window width={width} height={height} title={title} accentDot glow>
            <div style={{ padding: '34px 40px', height: '100%', boxSizing: 'border-box' }}>
              <Code lines={lines} chars={chars} fontSize={33} lineHeight={1.6} caret />
            </div>
            {/* single spotlight sweep, clipped inside the window (no group glints) */}
            <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', opacity: sweepOp, background: `linear-gradient(105deg, transparent ${sweep - 16}%, rgba(200,196,255,0.28) ${sweep}%, transparent ${sweep + 16}%)` }} />
          </Window>
        </div>
      </AbsoluteFill>
      {step && (
        <div style={{ position: 'absolute', left: 96, top: 86, fontFamily: T.mono, fontSize: 22, letterSpacing: '0.24em', textTransform: 'uppercase', color: T.dim, display: 'flex', alignItems: 'center', gap: 12, opacity: win }}>
          <span style={{ width: 8, height: 8, background: T.accent }} />
          {step}
        </div>
      )}
    </AbsoluteFill>
  );
};
