// origin: video-shotcraft assets/lib/FlashCut.tsx — reskinned to the violet console tone.
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

/** Cool-white bloom that flashes over a hard cut between scenes. */
export const FlashCut: React.FC<{ duration?: number }> = ({ duration = 10 }) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, duration * 0.4, duration], [0, 0.7, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        opacity: o,
        background:
          'radial-gradient(ellipse at 50% 46%, rgba(200,196,255,0.92), rgba(139,123,255,0.4) 52%, transparent 78%)',
      }}
    />
  );
};
