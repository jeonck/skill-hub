// Terminal Noir — dark IaC console design tokens.
// The whole film reuses this palette (aesthetic-rules Q1/visual-language #2):
// nothing is styled outside these tokens.

export const T = {
  // surfaces
  bg: '#0B0E16', // deep near-black indigo
  bg2: '#0E1220',
  surface: '#141A26', // panels / terminal body
  surface2: '#1B2332',
  titlebar: '#1A2130',
  border: '#273249',
  borderSoft: '#1E2740',

  // text
  text: '#E7ECF5',
  dim: '#8B96AD', // comments / secondary
  faint: '#5C6680',

  // accents
  accent: '#8B7BFF', // violet — brand / keyword
  accent2: '#7C5CFF',
  accentGlow: 'rgba(139,123,255,0.55)',
  ok: '#4BD07A', // terminal success / apply +
  add: '#57C77F', // plan +
  warn: '#E3B341', // plan ~ / string literal
  cyan: '#5FD0D6', // resource type
  pink: '#E5709B', // attribute name
  danger: '#E5606A',

  // fonts
  mono: 'ui-monospace, "SF Mono", "SFMono-Regular", Menlo, Consolas, monospace',
  sans: 'system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif',
} as const;

// syntax highlight colors for HCL tokens
export const HCL = {
  keyword: T.accent, // resource / provider / variable
  type: T.cyan, // "aws_instance"
  name: T.warn, // "web"
  attr: T.pink, // ami, instance_type
  string: T.add, // "ami-0abc..."
  number: T.warn,
  comment: T.dim,
  punct: T.dim,
  plain: T.text,
} as const;
