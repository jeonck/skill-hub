"""Inline SVG glyphs for the catalog.

Each entry is the *inner* markup of a 24x24 viewBox, stroke-based so it inherits
`currentColor` and stays legible at 20px. Keep shapes geometric and open — these
render at card size, not poster size. Solid dots use an explicit fill.
"""

ICONS: dict[str, str] = {
    # ---- search / discovery
    "search": '<circle cx="11" cy="11" r="6"/><path d="M15.6 15.6L20 20"/>',
    "radar": '<path d="M12 12L18 6"/><circle cx="12" cy="12" r="3"/>'
             '<path d="M12 3a9 9 0 109 9"/><path d="M12 7a5 5 0 105 5"/>',
    "layers": '<path d="M12 3.2l8.5 4.6-8.5 4.6-8.5-4.6 8.5-4.6z"/>'
               '<path d="M3.5 12.2l8.5 4.6 8.5-4.6"/><path d="M3.5 16.4l8.5 4.6 8.5-4.6"/>',
    "orbit": '<circle cx="12" cy="12" r="2.5"/><ellipse cx="12" cy="12" rx="9.5" ry="4"/>'
             '<ellipse cx="12" cy="12" rx="9.5" ry="4" transform="rotate(60 12 12)"/>',
    "palette": '<path d="M12 3.5a8.5 8.5 0 000 17c1.3 0 2.2-.9 2.2-2 0-1.3-1-1.7-1-2.6 '
               '0-.8.7-1.4 1.6-1.4h1.6A4.1 4.1 0 0020.5 10c0-3.6-3.8-6.5-8.5-6.5z"/>'
               '<circle cx="7.8" cy="11.5" r="1" fill="currentColor" stroke="none"/>'
               '<circle cx="10.5" cy="7.8" r="1" fill="currentColor" stroke="none"/>'
               '<circle cx="15" cy="8.4" r="1" fill="currentColor" stroke="none"/>',
    "swatches": '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/>'
                '<rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/>'
                '<rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/>'
                '<rect x="13.5" y="13.5" width="7" height="7" rx="3.5"/>',
    "badge": '<path d="M12 3l2.4 1.7 2.9-.2.9 2.8 2.4 1.7-1.1 2.7 1.1 2.7-2.4 1.7-.9 2.8'
             '-2.9-.2L12 21l-2.4-1.7-2.9.2-.9-2.8L3.4 15l1.1-2.7L3.4 9.6l2.4-1.7.9-2.8'
             '2.9.2L12 3z"/><path d="M9.2 12.2l2 2 3.6-3.9"/>',
    "gem": '<path d="M6 4h12l3 5-9 11L3 9l3-5z"/><path d="M3 9h18"/><path d="M9.5 4L7.5 9l4.5 11'
           'L16.5 9 14.5 4"/>',
    "frame": '<rect x="3.5" y="3.5" width="17" height="17" rx="2"/>'
             '<path d="M3.5 15.5l4.5-4.5 4 4 3-3 5 5"/>'
             '<circle cx="9" cy="8.5" r="1.4"/>',
    "grid-hard": '<path d="M3 3h18v18H3z"/><path d="M3 9h18M3 15h18M9 3v18"/>',
    "square-min": '<rect x="3.5" y="3.5" width="17" height="17" rx="2"/><path d="M8 12h8"/>',
    "wand": '<path d="M4 20L15 9"/><path d="M13.5 4.5l1 2.5 2.5 1-2.5 1-1 2.5-1-2.5-2.5-1 2.5-1 1-2.5z"/>'
            '<path d="M19 13l.6 1.6 1.6.6-1.6.6-.6 1.6-.6-1.6-1.6-.6 1.6-.6.6-1.6z"/>',
    "needle": '<path d="M4 20l6.5-6.5"/><path d="M10.5 13.5L20 4"/>'
              '<circle cx="17.8" cy="6.2" r="1.6"/><path d="M8 17.5c1.8-1 3.2-.4 4.6.6"/>',
    "eye": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/>'
           '<circle cx="12" cy="12" r="2.8"/>',
    # ---- devices / screens
    "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M10.5 5.5h3"/>'
             '<path d="M10 18.5h4"/>',
    "browser": '<rect x="2.5" y="4" width="19" height="16" rx="2"/><path d="M2.5 8.5h19"/>'
               '<circle cx="5.8" cy="6.2" r=".7" fill="currentColor" stroke="none"/>'
               '<circle cx="8.1" cy="6.2" r=".7" fill="currentColor" stroke="none"/>',
    "browser-check": '<rect x="2.5" y="4" width="19" height="16" rx="2"/><path d="M2.5 8.5h19"/>'
                     '<path d="M8.5 14l2.4 2.4 4.6-4.8"/>',
    "motion": '<rect x="2.5" y="5" width="19" height="14" rx="2"/>'
              '<path d="M10.2 9.4l4.3 2.6-4.3 2.6V9.4z"/>'
              '<path d="M5.5 12h1.7M17.3 12h1.4"/>',

    "terminal-play": '<rect x="2.5" y="4" width="19" height="16" rx="2"/>'
                     '<path d="M6.5 9l2.6 2.6-2.6 2.6"/><path d="M12 15h5"/>',
    "clapper": '<path d="M3 9.5h18v9.5a1.5 1.5 0 01-1.5 1.5h-15A1.5 1.5 0 013 19z"/>'
               '<path d="M3.4 9.5L2.6 6l17.6-2.4.8 3.5-17.6 2.4z"/>'
               '<path d="M8.4 4.9l1 3.4M13.6 4.2l1 3.4"/>',
    # ---- docs / writing
    "book": '<path d="M3.5 5.5A2 2 0 015.5 3.5H11v17H5.5a2 2 0 01-2-2v-13z"/>'
            '<path d="M20.5 5.5a2 2 0 00-2-2H13v17h5.5a2 2 0 002-2v-13z"/>',
    "lotus": '<path d="M12 20.5c-4.5 0-8-2.8-8-6.2 1.9-.6 3.6-.3 5 .7"/>'
             '<path d="M12 20.5c4.5 0 8-2.8 8-6.2-1.9-.6-3.6-.3-5 .7"/>'
             '<path d="M12 20.5c-2.3-1.6-3.6-4-3.6-6.6S9.7 8.9 12 6.5c2.3 2.4 3.6 4.8 3.6 7.4s-1.3 5-3.6 6.6z"/>',
    "library": '<path d="M4 20V6M8 20V6M12.5 20V6"/><path d="M2.5 20h12"/>'
               '<path d="M16.5 7.5l3.8 12.1"/><path d="M15 20h6.5"/>',
    "feather": '<path d="M4 20l7-7"/><path d="M20.5 3.5c-6 0-11 3.6-11 9v3h3c5.4 0 8-5 8-12z"/>'
               '<path d="M9 15c2.5-2.5 5-4 8-5"/>',
    "notebook": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 3v18"/>'
                '<path d="M12.5 8h3.5M12.5 12h3.5"/>',
    "incident": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/>'
                '<path d="M12 11v3.5"/>'
                '<circle cx="12" cy="17.6" r=".9" fill="currentColor" stroke="none"/>',
    "quote": '<path d="M9 6.5c-2.8 0-4.5 2-4.5 4.4 0 1.9 1.3 3.1 3 3.1 1.5 0 2.6-1 2.6-2.4 '
             '0-1.3-.9-2.2-2.1-2.2-.3 0-.6 0-.8.1.2-.9 1-1.6 1.8-1.9V6.5z"/>'
             '<path d="M18.5 6.5c-2.8 0-4.5 2-4.5 4.4 0 1.9 1.3 3.1 3 3.1 1.5 0 2.6-1 2.6-2.4 '
             '0-1.3-.9-2.2-2.1-2.2-.3 0-.6 0-.8.1.2-.9 1-1.6 1.8-1.9V6.5z"/>'
             '<path d="M6 17.5h12"/>',
    "chat": '<path d="M20.5 12.5c0 3.9-3.8 7-8.5 7-1 0-2-.1-2.9-.4L4 21l1.3-3.6C4.1 16.1 3.5 14.4 '
            '3.5 12.5c0-3.9 3.8-7 8.5-7s8.5 3.1 8.5 7z"/><path d="M8.5 11h7M8.5 14h4.5"/>',
    "transcript": '<rect x="4" y="3" width="16" height="18" rx="2"/>'
                  '<path d="M8 9.5v5M11 11v2M14 8.5v7M17 10.5v3"/>',

    "megaphone": '<path d="M4 10.5v3a1.5 1.5 0 001.5 1.5H8l7 4.5V6L8 10.5H5.5A1.5 1.5 0 004 12z"/>'
                 '<path d="M18 9.5a3.5 3.5 0 010 5"/><path d="M8 15v4.5"/>',
    "compare": '<path d="M4 5.5h6.5v13H4z"/><path d="M13.5 5.5H20v13h-6.5z"/>'
               '<path d="M12 3.5v17"/>',
    "list-check": '<path d="M4 6.5l1.6 1.6L8.8 5"/><path d="M4 12.5l1.6 1.6L8.8 11"/>'
                  '<path d="M4 18.5l1.6 1.6L8.8 17"/><path d="M11.5 7h8.5M11.5 13h8.5M11.5 19h6"/>',
    # ---- dev workflow (superpowers)
    "bulb": '<path d="M9.2 17h5.6"/><path d="M10 20.5h4"/>'
            '<path d="M12 3.5a5.8 5.8 0 00-3.4 10.5c.5.4.8 1 .8 1.6h5.2c0-.6.3-1.2.8-1.6A5.8 5.8 0 0012 3.5z"/>',
    "fanout": '<circle cx="5" cy="12" r="2.2"/><circle cx="19" cy="5.5" r="2.2"/>'
              '<circle cx="19" cy="12" r="2.2"/><circle cx="19" cy="18.5" r="2.2"/>'
              '<path d="M7.2 12h9.6M7.2 11.2l9.6-4.6M7.2 12.8l9.6 4.6"/>',
    "play-list": '<path d="M4 6.5h9M4 12h9M4 17.5h5"/>'
                 '<path d="M15.5 14l5 2.8-5 2.8V14z"/>',
    "merge": '<circle cx="6.5" cy="5.5" r="2.2"/><circle cx="6.5" cy="18.5" r="2.2"/>'
             '<circle cx="17.5" cy="12" r="2.2"/><path d="M6.5 7.7v8.6"/>'
             '<path d="M8.7 5.9c.4 3.4 2.9 5.6 6.6 6"/>',
    "inbox-check": '<path d="M3.5 13.5h4l1.5 2.5h6l1.5-2.5h4"/>'
                   '<path d="M5.5 4.5h13l2 9v5a1.5 1.5 0 01-1.5 1.5h-14A1.5 1.5 0 013.5 18.5v-5z"/>'
                   '<path d="M9.5 8.5l2 2 3.5-3.5"/>',
    "send-check": '<path d="M20.5 3.5L10.5 13.5"/><path d="M20.5 3.5l-6.5 17-3.5-7-7-3.5 17-6.5z"/>',
    "agents": '<rect x="3" y="4" width="7" height="7" rx="1.6"/>'
              '<rect x="14" y="4" width="7" height="7" rx="1.6"/>'
              '<rect x="8.5" y="14" width="7" height="6.5" rx="1.6"/>'
              '<path d="M6.5 11v1.5h11V11"/><path d="M12 12.5V14"/>',
    "bug": '<rect x="8" y="7.5" width="8" height="11" rx="4"/>'
           '<path d="M9.5 6.5a2.5 2.5 0 015 0"/>'
           '<path d="M8 10.5H4.5M8 14h-4M8 17.5l-3 2M16 10.5h3.5M16 14h4M16 17.5l3 2"/>',
    "flask": '<path d="M9.5 3.5v6L4.6 18a1.6 1.6 0 001.4 2.5h12a1.6 1.6 0 001.4-2.5l-4.9-8.5v-6"/>'
             '<path d="M8 3.5h8"/><path d="M7.2 14.5h9.6"/>',
    "branch": '<circle cx="7" cy="5.5" r="2.2"/><circle cx="7" cy="18.5" r="2.2"/>'
              '<circle cx="17" cy="5.5" r="2.2"/><path d="M7 7.7v8.6"/>'
              '<path d="M17 7.7c0 4-3.4 5.5-7 6"/>',
    "bolt": '<path d="M13.5 2.5L5 13.5h6L10.5 21.5 19 10.5h-6l.5-8z"/>',
    "double-check": '<path d="M2.5 12.5l3.5 3.5 6-6.5"/><path d="M10.5 15.5l1.5 1.5 8-9"/>',
    "clipboard": '<rect x="5" y="4.5" width="14" height="16" rx="2"/>'
                 '<rect x="9" y="2.8" width="6" height="3.4" rx="1.2"/>'
                 '<path d="M8.5 11h7M8.5 15h4.5"/>',
    "hammer": '<path d="M12.5 8.5L4 17a2.1 2.1 0 003 3l8.5-8.5"/>'
              '<path d="M11 7l4-4 6 6-4 4-6-6z"/>',
    # ---- ui/ux
    "wireframe": '<rect x="2.5" y="4" width="19" height="16" rx="2"/><path d="M2.5 8.5h19"/>'
                 '<path d="M9 8.5v11.5"/><path d="M12 12h6M12 15.5h4"/>',
    "pen-nib": '<path d="M4 20l3.2-8.6L15.5 3l5.5 5.5-8.4 8.3L4 20z"/>'
               '<path d="M7.2 11.4l5.4 5.4"/><circle cx="10" cy="14" r="1.4"/>',
    "banner": '<path d="M3.5 4.5h17v10h-17z"/><path d="M3.5 14.5l4 5 4-5"/>'
              '<path d="M7 9h10"/>',
    "brush": '<path d="M14 6.5l3.5 3.5"/>'
             '<path d="M17.5 3.5l3 3-9.5 9.5-3-3L17.5 3.5z"/>'
             '<path d="M8 13c-2 0-3.5 1.6-3.5 3.6 0 1-.5 1.9-1.5 2.4 1 .9 2.4 1.5 3.8 1.5 2.3 0 4.2-1.9 4.2-4.2"/>',
    "tag": '<path d="M11.5 3.5H20v8.5l-9 9L2.5 12.5l9-9z"/>'
           '<circle cx="16" cy="8" r="1.5"/>',
    "presentation": '<path d="M3 4h18"/><rect x="4.5" y="4" width="15" height="10.5" rx="1.5"/>'
                    '<path d="M12 14.5v2.5"/><path d="M8.5 20.5L12 17l3.5 3.5"/>',
    "tokens": '<rect x="3" y="3" width="8" height="8" rx="1.6"/>'
              '<rect x="13" y="3" width="8" height="8" rx="4"/>'
              '<rect x="3" y="13" width="8" height="8" rx="4"/>'
              '<rect x="13" y="13" width="8" height="8" rx="1.6"/>',
    "guardrail": '<path d="M12 3l7.5 3v5.5c0 4.4-3 7.9-7.5 9.5-4.5-1.6-7.5-5.1-7.5-9.5V6L12 3z"/>'
                 '<path d="M9.2 12.5h5.6"/><path d="M12 9.7v5.6"/>',
    "stack-posts": '<rect x="3.5" y="3.5" width="17" height="6" rx="1.5"/>'
                   '<rect x="3.5" y="12" width="17" height="8.5" rx="1.5"/>'
                   '<path d="M7 15.5h7M7 18h4"/>',
    "blueprint": '<rect x="2.5" y="4.5" width="19" height="15" rx="2"/>'
                 '<rect x="6" y="8" width="5" height="4" rx="1"/>'
                 '<rect x="14" y="12" width="4.5" height="4" rx="1"/>'
                 '<path d="M11 10h3.2a1 1 0 011 1v1"/>',
    "lakehouse": '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.6"/>'
                 '<path d="M4.5 5.5v5.4c0 1.4 3.4 2.6 7.5 2.6s7.5-1.2 7.5-2.6V5.5"/>'
                 '<path d="M4.5 12.5v5.4c0 1.4 3.4 2.6 7.5 2.6s7.5-1.2 7.5-2.6v-5.4"/>',
    # ---- structure / infra
    "network": '<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="18.5" r="2.2"/>'
               '<circle cx="19" cy="18.5" r="2.2"/><path d="M12 7.2v4.3M12 11.5L6.4 16.7"/>'
               '<path d="M12 11.5l5.6 5.2"/>',
    "sitemap": '<rect x="9" y="3" width="6" height="4.5" rx="1"/>'
               '<rect x="2.5" y="16.5" width="6" height="4.5" rx="1"/>'
               '<rect x="15.5" y="16.5" width="6" height="4.5" rx="1"/>'
               '<path d="M12 7.5v4M5.5 16.5v-2.5h13v2.5"/>',
    "route": '<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/>'
             '<path d="M6 8.5v4a3.5 3.5 0 003.5 3.5H15"/>'
             '<path d="M13 13.5l2 2.5-2 2.5"/>',
    "server-plug": '<rect x="3.5" y="4" width="17" height="6" rx="1.5"/>'
                   '<rect x="3.5" y="14" width="17" height="6" rx="1.5"/>'
                   '<path d="M7 7h.01M7 17h.01"/><path d="M14 7h3M14 17h3"/>',
    "shield": '<path d="M12 3l7.5 3v5.5c0 4.4-3 7.9-7.5 9.5-4.5-1.6-7.5-5.1-7.5-9.5V6L12 3z"/>'
              '<path d="M9 12l2.2 2.2L15.4 10"/>',
    "puzzle": '<path d="M9.5 3.5h5v2.2a1.8 1.8 0 103.6 0V3.5h1.4v6h-2.2a1.8 1.8 0 100 3.6h2.2v7.4'
              'h-6v-2.2a1.8 1.8 0 10-3.6 0v2.2h-6v-6h2.2a1.8 1.8 0 100-3.6H3.5v-7.4h6z"/>',
    "heart": '<path d="M12 20.5S4.5 15.8 4.5 10.4A4.4 4.4 0 0112 7.8a4.4 4.4 0 017.5 2.6'
                    'c0 5.4-7.5 10.1-7.5 10.1z"/>',
    "bag-play": '<path d="M5 7.5h14l-1 13H6l-1-13z"/><path d="M9 7.5V6a3 3 0 016 0v1.5"/>'
                '<path d="M10.8 12.2l3.4 2-3.4 2v-4z"/>',
    "reel": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="1.8"/>'
            '<circle cx="12" cy="7" r="1.7"/><circle cx="16.3" cy="14.5" r="1.7"/>'
            '<circle cx="7.7" cy="14.5" r="1.7"/>',
    "users": '<circle cx="9" cy="8" r="3"/><path d="M3.5 19.5a5.5 5.5 0 0111 0"/>'
             '<path d="M16 5.6a3 3 0 010 4.8"/><path d="M17.5 14.4a5.5 5.5 0 013 5.1"/>',
}

# Skill slug -> icon key. Every skill in the catalog must appear here.
SKILL_ICONS: dict[str, str] = {
    "data-platform-architecture": "lakehouse",
    "archify": "blueprint",
    "video-shotcraft": "clapper",
    "hugo-stack-blog": "stack-posts",
    "andrej-karpathy-skills": "guardrail",
    "banner-design": "banner",
    "brand": "tag",
    "design": "pen-nib",
    "design-system": "tokens",
    "slides": "presentation",
    "ui-styling": "brush",
    "ui-ux-pro-max": "wireframe",
    "brainstorming": "bulb",
    "dispatching-parallel-agents": "fanout",
    "executing-plans": "play-list",
    "finishing-a-development-branch": "merge",
    "receiving-code-review": "inbox-check",
    "requesting-code-review": "send-check",
    "subagent-driven-development": "agents",
    "systematic-debugging": "bug",
    "test-driven-development": "flask",
    "using-git-worktrees": "branch",
    "using-superpowers": "bolt",
    "verification-before-completion": "double-check",
    "writing-plans": "clipboard",
    "writing-skills": "hammer",
    "algolia-docusaurus": "search",
    "algorithmic-art": "orbit",
    "artifacts-builder": "layers",
    "brand-guidelines": "palette",
    "brandkit": "badge",
    "brutalist-skill": "grid-hard",
    "canvas-design": "frame",
    "ccnp-ccie-writer": "network",
    "cisa-content-writer": "shield",
    "code-explainer-video": "terminal-play",
    "daily-diary-pipeline": "notebook",
    "daily-insight-pipeline": "radar",
    "docusaurus-english-site": "book",
    "github-sponsors": "heart",
    "hextra-kb-builder": "library",
    "hextra-roadmap-kb": "route",
    "hugo-blog-builder": "feather",
    "imagegen-frontend-mobile": "phone",
    "imagegen-frontend-web": "browser",
    "internal-comms": "megaphone",
    "it-professional-content": "sitemap",
    "lotusdocs-kb-builder": "lotus",
    "mcp-builder": "server-plug",
    "minimalist-skill": "square-min",
    "moneyprinter-turbo": "reel",
    "output-skill": "list-check",
    "problem-note": "incident",
    "redesign-skill": "wand",
    "research-agent-team": "users",
    "skill-creator": "puzzle",
    "slack-gif-creator": "motion",
    "soft-skill": "gem",
    "stitch-skill": "needle",
    "sync-shopshorts-higgs": "bag-play",
    "taste-skill": "eye",
    "term-comparison-pipeline": "compare",
    "theme-factory": "swatches",
    "transcript-study-pipeline": "transcript",
    "us-work-english-content": "chat",
    "us-work-english-idiom-section": "quote",
    "webapp-testing": "browser-check",
}

# Category -> slug used for the tint class on the icon tile.
CATEGORY_SLUGS: dict[str, str] = {
    "Design & UI": "design",
    "Content & Writing": "content",
    "Sites & Docs": "docs",
    "Automation Pipelines": "pipeline",
    "Media & Video": "media",
    "Dev Tooling": "dev",
    "Research": "research",
}

# Tint per category. Kept mid-tone on purpose: these same values are baked into
# the standalone SVGs the README embeds, which sit on either a white or a dark
# GitHub background with no way to react to the theme.
CATEGORY_COLORS: dict[str, str] = {
    "design": "#8b5cf6",
    "content": "#d97706",
    "docs": "#3b82f6",
    "pipeline": "#14b8a6",
    "media": "#f43f5e",
    "dev": "#6366f1",
    "research": "#22c55e",
}

FALLBACK_ICON = "puzzle"


def icon_svg(key: str, size: int = 22, extra: str = "") -> str:
    inner = ICONS.get(key) or ICONS[FALLBACK_ICON]
    return (
        f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true"{extra}>{inner}</svg>'
    )


# The site mark: a hub node wired to three satellites — the catalog in one shape.
# Deliberately heavier than the skill glyphs (solid tile, filled nodes) so it reads
# as a logo rather than as a 39th icon, and survives being shrunk to a 16px favicon.
LOGO_NODES = [(16.0, 7.4), (23.4, 20.3), (8.6, 20.3)]


def _logo_inner(tile: str, ink: str | None) -> str:
    """`ink=None` leaves the foreground unpainted so the stylesheet can drive it —
    var() is not honoured inside SVG presentation attributes, so the themed build
    styles `.logo .ink` in CSS instead of writing a colour here. currentColor *is*
    honoured, so the tile itself can still inherit."""
    paint_g = f' stroke="{ink}"' if ink else ""
    paint_c = f' fill="{ink}"' if ink else ""
    spokes = "".join(f'<path d="M16 16L{x} {y}"/>' for x, y in LOGO_NODES)
    dots = "".join(
        f'<circle class="ink" cx="{x}" cy="{y}" r="2.6"{paint_c} stroke="none"/>'
        for x, y in LOGO_NODES
    )
    # Nudged in from the tile edge: at full size the nodes crowded the corners.
    inset = 'transform="translate(16 16) scale(0.9) translate(-16 -16)"'
    return (
        f'<rect width="32" height="32" rx="8.5" fill="{tile}"/>'
        f'<g {inset}>'
        f'<g class="ink-s"{paint_g} stroke-width="2.1" stroke-linecap="round" '
        f'fill="none">{spokes}</g>'
        f'<circle class="ink" cx="16" cy="16" r="3.4"{paint_c} stroke="none"/>{dots}'
        f"</g>"
    )


def logo_svg(size: int = 30) -> str:
    """Header lockup mark. The tile inherits currentColor; `.ink`/`.ink-s` are
    painted by the stylesheet so the mark flips with the light/dark theme."""
    return (
        f'<svg class="logo" width="{size}" height="{size}" viewBox="0 0 32 32" '
        f'aria-hidden="true">{_logo_inner("currentColor", None)}</svg>'
    )


# Standalone logo files for the README, one per GitHub theme. Same pair of colours
# the stylesheet uses, since a committed SVG cannot read the viewer's theme itself.
LOGO_FILES = {
    "logo.svg": ("#c2410c", "#fbfaf9"),
    "logo-dark.svg": ("#f97b4f", "#12110f"),
}


def logo_file_svg(tile: str, ink: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" '
        f'viewBox="0 0 32 32">{_logo_inner(tile, ink)}</svg>\n'
    )


def logo_favicon() -> str:
    """Standalone copy for the favicon — no stylesheet reaches it, so it is
    painted outright."""
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'>"
        + _logo_inner("%23c2410c", "%23ffffff").replace('"', "'")
        + "</svg>"
    )
    return "data:image/svg+xml," + svg.replace("<", "%3C").replace(">", "%3E")


def icon_file_svg(key: str, color: str) -> str:
    """A self-contained .svg file for the README. `currentColor` has nothing to
    inherit from inside an <img>, so the stroke colour is written in."""
    inner = ICONS.get(key) or ICONS[FALLBACK_ICON]
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.7" '
        f'stroke-linecap="round" stroke-linejoin="round">{inner}</svg>\n'
    )


def icon_data_uri(key: str) -> str:
    """Same glyph as a favicon-ready data: URI (quotes kept single for the attribute)."""
    inner = (ICONS.get(key) or ICONS[FALLBACK_ICON]).replace('"', "'")
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' "
        "stroke='%23c2410c' stroke-width='1.8' stroke-linecap='round' "
        f"stroke-linejoin='round'>{inner}</svg>"
    )
    return "data:image/svg+xml," + svg.replace("#", "%23").replace("<", "%3C").replace(">", "%3E")
