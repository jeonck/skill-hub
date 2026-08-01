// Reusable dark window chrome: titlebar with three dots + a filename/label,
// then a content area. Used for both the HCL editor and the terminal.
import { T } from './theme';

export const Window: React.FC<{
  width: number;
  height: number;
  title: string;
  accentDot?: boolean;
  children: React.ReactNode;
  glow?: boolean;
}> = ({ width, height, title, accentDot = false, children, glow = false }) => (
  <div
    style={{
      width,
      height,
      background: T.surface,
      borderRadius: 16,
      border: `1px solid ${T.border}`,
      boxShadow: glow
        ? `0 40px 120px rgba(0,0,0,0.55), 0 0 0 1px ${T.borderSoft}, 0 0 90px -20px ${T.accentGlow}`
        : '0 34px 90px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.02)',
      overflow: 'hidden',
      boxSizing: 'border-box',
      display: 'flex',
      flexDirection: 'column',
    }}
  >
    {/* titlebar */}
    <div
      style={{
        height: 54,
        flex: '0 0 54px',
        background: T.titlebar,
        borderBottom: `1px solid ${T.borderSoft}`,
        display: 'flex',
        alignItems: 'center',
        gap: 11,
        padding: '0 22px',
        boxSizing: 'border-box',
      }}
    >
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          style={{
            width: 14,
            height: 14,
            borderRadius: 8,
            background: i === 0 && accentDot ? T.accent : '#39435C',
          }}
        />
      ))}
      <div
        style={{
          margin: '0 auto',
          fontFamily: T.mono,
          fontSize: 20,
          color: T.dim,
          letterSpacing: '0.02em',
        }}
      >
        {title}
      </div>
      <div style={{ width: 42 }} />
    </div>
    {/* content */}
    <div style={{ flex: 1, minHeight: 0, position: 'relative' }}>{children}</div>
  </div>
);
