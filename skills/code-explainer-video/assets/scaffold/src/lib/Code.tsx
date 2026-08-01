// HCL / terminal code renderer with syntax highlighting, deterministic
// character-typing reveal, and a block caret.
import { useCurrentFrame } from 'remotion';
import { T } from './theme';

export type Tok = { s: string; c?: string };
export type Line = Tok[];

// square block caret, 12f square-wave blink (terminal-typewriter tuning)
export const Caret: React.FC<{ h?: number; on?: boolean; color?: string }> = ({
  h = 30,
  on,
  color = T.text,
}) => {
  const frame = useCurrentFrame();
  const blink = on ?? frame % 12 < 6;
  return (
    <span
      style={{
        display: 'inline-block',
        width: 13,
        height: h,
        marginLeft: 2,
        transform: 'translateY(4px)',
        background: color,
        opacity: blink ? 1 : 0,
      }}
    />
  );
};

const lineLen = (l: Line) => l.reduce((n, t) => n + t.s.length, 0);

/** Render `lines`, revealing up to `chars` characters across the whole block
 * (typing). If `chars` is undefined the block is fully shown. A caret is drawn
 * at the current typing head when `caret` is true and typing is incomplete. */
export const Code: React.FC<{
  lines: Line[];
  chars?: number;
  fontSize?: number;
  lineHeight?: number;
  caret?: boolean;
}> = ({ lines, chars, fontSize = 31, lineHeight = 1.55, caret = false }) => {
  const total = lines.reduce((n, l) => n + lineLen(l) + 1, 0); // +1 newline each
  const reveal = chars === undefined ? total : chars;
  const done = reveal >= total - 1;

  let consumed = 0;
  return (
    <div
      style={{
        fontFamily: T.mono,
        fontSize,
        lineHeight,
        color: T.text,
        whiteSpace: 'pre',
        fontVariantLigatures: 'none',
      }}
    >
      {lines.map((line, li) => {
        const before = consumed;
        const len = lineLen(line);
        const lineStart = before;
        consumed += len + 1;
        // how many chars of THIS line are visible
        const visIn = Math.max(0, Math.min(len, reveal - lineStart));
        if (reveal <= lineStart && li > 0 && chars !== undefined) {
          // line not started yet — keep vertical space
          return <div key={li} style={{ height: `${fontSize * lineHeight}px` }} />;
        }
        // caret sits on the line currently being typed
        const typingHere =
          chars !== undefined && reveal > lineStart && reveal <= lineStart + len;
        let acc = 0;
        return (
          <div key={li} style={{ minHeight: `${fontSize * lineHeight}px` }}>
            {line.map((tok, ti) => {
              const startAt = acc;
              acc += tok.s.length;
              const show = Math.max(0, Math.min(tok.s.length, visIn - startAt));
              if (show <= 0) return null;
              return (
                <span key={ti} style={{ color: tok.c ?? T.text }}>
                  {tok.s.slice(0, show)}
                </span>
              );
            })}
            {caret && typingHere && <Caret h={fontSize} />}
          </div>
        );
      })}
      {caret && done && (
        <div style={{ minHeight: `${fontSize * lineHeight}px` }}>
          <Caret h={fontSize} />
        </div>
      )}
    </div>
  );
};

/** frame-deterministic typing count: `speed` frames per character. */
export const typedChars = (frame: number, start: number, speed = 2) =>
  Math.max(0, Math.floor((frame - start) / speed));
