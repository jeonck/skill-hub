// Shared dark backdrop: deep indigo, faint dot grid, single soft center glow,
// vignette. One glow only (aesthetic-rules Q4 — no group glints).
import { AbsoluteFill } from 'remotion';
import { T } from './theme';

export const Backdrop: React.FC<{ glow?: number; glowY?: number }> = ({
  glow = 0.5,
  glowY = 46,
}) => (
  <AbsoluteFill style={{ background: T.bg, overflow: 'hidden' }}>
    {/* dot grid */}
    <AbsoluteFill
      style={{
        backgroundImage: `radial-gradient(${T.borderSoft} 1.4px, transparent 1.4px)`,
        backgroundSize: '46px 46px',
        opacity: 0.5,
      }}
    />
    {/* single soft center glow */}
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse 60% 55% at 50% ${glowY}%, rgba(124,92,255,${
          0.16 * glow
        }), transparent 70%)`,
      }}
    />
    {/* vignette */}
    <AbsoluteFill
      style={{
        background:
          'radial-gradient(ellipse 90% 90% at 50% 50%, transparent 55%, rgba(0,0,0,0.55) 100%)',
      }}
    />
  </AbsoluteFill>
);
