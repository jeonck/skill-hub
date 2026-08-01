// TEMPLATE — a dependency/relationship graph builds: elbow edges GROW before
// their child node pops in (spring), nodes resolve to a "ready/created" state.
// Use for "how the pieces connect" beats (resource graph, module reuse, service
// mesh, data pipeline, import tree). Keep node boxes wide enough that the
// longest label doesn't clip (measure: ~14.4px/char at 24px mono).
import {
  AbsoluteFill,
  interpolate,
  Easing,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { Backdrop } from '../lib/Backdrop';
import { T } from '../lib/theme';

export type GNode = {
  id: number;
  x: number; // center
  y: number; // center
  parent: number; // -1 for root
  level: number;
  label: string;
  sub?: string;
  root?: boolean;
};

const NW = 372;
const NH = 96;
const CASCADE_START = 46;
const LEVEL_GAP = 22;
const SIB_STAGGER = 10;

export const GraphScene: React.FC<{
  nodes: GNode[];
  extraEdges?: [number, number][]; // non-tree cross edges [parentId, childId]
  headline?: string; // top mono line
  banner?: string; // bottom green summary
  duration: number;
}> = ({ nodes, extraEdges = [], headline, banner, duration }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

  const nodeStart = (n: GNode) => {
    if (n.level === 0) return CASCADE_START;
    const sib = nodes.filter((m) => m.level === n.level && m.id < n.id).length;
    return CASCADE_START + n.level * LEVEL_GAP + sib * SIB_STAGGER;
  };
  const ready = (n: GNode) => frame >= nodeStart(n) + 30;

  const edgePath = (p: GNode, c: GNode) => {
    const y1 = p.y + NH / 2, y2 = c.y - NH / 2, my = (y1 + y2) / 2;
    return `M ${p.x} ${y1} L ${p.x} ${my} L ${c.x} ${my} L ${c.x} ${y2}`;
  };
  const edgeLen = (p: GNode, c: GNode) => Math.abs(p.y + NH / 2 - (c.y - NH / 2)) + Math.abs(c.x - p.x);

  const lastStart = nodeStart(nodes[nodes.length - 1]);
  const breathe = interpolate(frame, [lastStart + 26, lastStart + 40, lastStart + 58], [1, 1.025, 1], { ...clamp, easing: Easing.inOut(Easing.sin) });
  const bannerIn = interpolate(frame, [lastStart + 34, lastStart + 48], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const fadeOut = interpolate(frame, [duration - 12, duration], [1, 0], clamp);

  const treeEdges = nodes.filter((n) => n.parent >= 0).map((n) => [n.parent, n.id] as [number, number]);

  return (
    <AbsoluteFill style={{ opacity: fadeOut }}>
      <Backdrop glow={0.75} glowY={52} />
      {headline && (
        <div style={{ position: 'absolute', left: 0, right: 0, top: 90, textAlign: 'center', fontFamily: T.mono, fontSize: 30, color: T.dim }}>{headline}</div>
      )}
      <AbsoluteFill style={{ transform: `scale(${breathe})`, transformOrigin: '960px 560px' }}>
        <svg width={1920} height={1080} style={{ position: 'absolute', inset: 0 }}>
          {[...treeEdges, ...extraEdges].map(([pid, cid], k) => {
            const p = nodes.find((n) => n.id === pid)!;
            const c = nodes.find((n) => n.id === cid)!;
            const start = nodeStart(c) - 8; // edge leads the node
            const len = edgeLen(p, c);
            const grow = interpolate(frame, [start, start + 16], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
            if (grow <= 0) return null;
            return <path key={k} d={edgePath(p, c)} stroke={ready(c) ? T.add : T.border} strokeWidth={3.5} fill="none" strokeLinejoin="round" strokeDasharray={len} strokeDashoffset={len * (1 - grow)} opacity={0.9} />;
          })}
        </svg>
        {nodes.map((n) => {
          const start = nodeStart(n);
          if (frame < start) return null;
          const pop = spring({ frame: frame - start, fps, config: { damping: 12, stiffness: 170 } });
          const on = ready(n);
          const statusColor = n.root ? T.accent : on ? T.ok : T.warn;
          const pulse = 0.55 + 0.45 * Math.sin(frame * 0.35);
          return (
            <div key={n.id} style={{ position: 'absolute', left: n.x - NW / 2, top: n.y - NH / 2, width: NW, height: NH, background: n.root ? T.surface2 : T.surface, border: `1.5px solid ${n.root ? T.accent : on ? T.add : T.border}`, borderRadius: 14, boxSizing: 'border-box', boxShadow: n.root ? `0 10px 40px -8px ${T.accentGlow}` : '0 12px 30px rgba(0,0,0,0.4)', transform: `scale(${pop})`, display: 'flex', alignItems: 'center', gap: 14, padding: '0 22px', fontFamily: T.mono }}>
              <span style={{ width: 14, height: 14, borderRadius: 8, background: statusColor, flex: '0 0 auto', opacity: n.root ? 1 : on ? 1 : pulse, boxShadow: `0 0 12px ${statusColor}` }} />
              <div style={{ minWidth: 0 }}>
                <div style={{ color: T.cyan, fontSize: 24, fontWeight: 600, whiteSpace: 'nowrap' }}>{n.label}</div>
                <div style={{ color: n.root ? T.dim : on ? T.ok : T.warn, fontSize: 20, fontWeight: 600, marginTop: 2 }}>{n.root ? n.sub ?? '' : on ? '✓ ready' : 'creating...'}</div>
              </div>
            </div>
          );
        })}
      </AbsoluteFill>
      {banner && (
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: 92, textAlign: 'center', fontFamily: T.mono, fontSize: 34, fontWeight: 700, color: T.ok, opacity: bannerIn, transform: `translateY(${(1 - bannerIn) * 10}px)` }}>{banner}</div>
      )}
    </AbsoluteFill>
  );
};
