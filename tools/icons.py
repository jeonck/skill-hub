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
    # ---- docs / writing
    "book": '<path d="M3.5 5.5A2 2 0 015.5 3.5H11v17H5.5a2 2 0 01-2-2v-13z"/>'
            '<path d="M20.5 5.5a2 2 0 00-2-2H13v17h5.5a2 2 0 002-2v-13z"/>',
    "library": '<path d="M4 20V6M8 20V6M12.5 20V6"/><path d="M2.5 20h12"/>'
               '<path d="M16.5 7.5l3.8 12.1"/><path d="M15 20h6.5"/>',
    "feather": '<path d="M4 20l7-7"/><path d="M20.5 3.5c-6 0-11 3.6-11 9v3h3c5.4 0 8-5 8-12z"/>'
               '<path d="M9 15c2.5-2.5 5-4 8-5"/>',
    "notebook": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 3v18"/>'
                '<path d="M12.5 8h3.5M12.5 12h3.5"/>',
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
    "users": '<circle cx="9" cy="8" r="3"/><path d="M3.5 19.5a5.5 5.5 0 0111 0"/>'
             '<path d="M16 5.6a3 3 0 010 4.8"/><path d="M17.5 14.4a5.5 5.5 0 013 5.1"/>',
}

# Skill slug -> icon key. Every skill in the catalog must appear here.
SKILL_ICONS: dict[str, str] = {
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
    "mcp-builder": "server-plug",
    "minimalist-skill": "square-min",
    "output-skill": "list-check",
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

FALLBACK_ICON = "puzzle"


def icon_svg(key: str, size: int = 22, extra: str = "") -> str:
    inner = ICONS.get(key) or ICONS[FALLBACK_ICON]
    return (
        f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true"{extra}>{inner}</svg>'
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
