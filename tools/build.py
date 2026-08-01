#!/usr/bin/env python3
"""Build the Skill Hub static site.

Reads every skill under skills/, merges its SKILL.md frontmatter with the
English display metadata in catalog/meta.json, and emits:

    _site/index.html            catalog page with search + filters
    _site/s/<skill>/index.html  detail page per skill
    _site/catalog.json          machine-readable index
    _site/dist/<skill>.zip      installable archive (top-level dir = skill name)
    _site/assets/style.css

Standard library only. Run:  python3 tools/build.py
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
import zipfile
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from icons import (  # noqa: E402
    CATEGORY_COLORS,
    CATEGORY_SLUGS,
    FALLBACK_ICON,
    SKILL_ICONS,
    icon_data_uri,
    icon_file_svg,
    icon_svg,
)

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
OUT = ROOT / "_site"

SITE = {
    "title": "Claude Skill Hub",
    "tagline": "A public catalog of installable Claude skills.",
    "owner": "jeonck",
    "repo": "jeonck/skill-hub",
    "base_url": "https://skill.metacog.co.kr",
    # Written to _site/CNAME on every build. Pages deploys from a workflow
    # artifact, and a deploy whose artifact has no CNAME clears the custom
    # domain -- so this file has to ship with the site, not just sit in the repo.
    "custom_domain": "skill.metacog.co.kr",
}

EXCLUDE_FROM_ZIP = {".git", ".DS_Store", "node_modules", "__pycache__", ".pytest_cache"}


# --------------------------------------------------------------------------
# frontmatter
# --------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse the leading --- YAML block. Supports scalars, quoted strings and
    `key: |` / `key: >` block scalars, which is all SKILL.md files use."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip("\n")
    body = text[end + 4 :].lstrip("\n")

    data: dict[str, object] = {}
    lines = raw.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in ("|", ">", "|-", ">-"):
            chunk: list[str] = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                chunk.append(lines[i][2:] if lines[i].startswith("  ") else "")
                i += 1
            joined = "\n".join(chunk).strip()
            data[key] = " ".join(joined.split()) if val.startswith(">") else joined
            continue
        if val == "" and i + 1 < len(lines) and lines[i + 1].startswith("  "):
            # nested mapping (e.g. metadata:) - skip its body, we don't use it
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                i += 1
            continue
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            val = val[1:-1]
        data[key] = val
        i += 1
    return data, body


# --------------------------------------------------------------------------
# minimal markdown -> html (headings, lists, fences, tables-as-code, inline)
# --------------------------------------------------------------------------

def _inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r'<img alt="\1" src="\2" loading="lazy">', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2" rel="nofollow">\1</a>', s)
    return s


def rewrite_relative_links(body_html: str, slug: str) -> str:
    """SKILL.md files link to their own bundled files (references/foo.md). Those
    aren't served by the site, so point them at the repo on GitHub instead."""
    base = f"https://github.com/{SITE['repo']}/blob/main/skills/{slug}/"

    def fix(m: re.Match) -> str:
        attr, url = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|data:|#|/)", url):
            return m.group(0)
        return f'{attr}="{base}{url.lstrip("./")}"'

    return re.sub(r'\b(href|src)="([^"]+)"', fix, body_html)


def markdown_to_html(md: str) -> str:
    out: list[str] = []
    lines = md.split("\n")
    i = 0
    list_open: str | None = None

    def close_list() -> None:
        nonlocal list_open
        if list_open:
            out.append(f"</{list_open}>")
            list_open = None

    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            close_list()
            lang = line[3:].strip()
            buf: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = f' class="lang-{html.escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{html.escape(chr(10).join(buf))}</code></pre>")
            continue

        if not line.strip():
            close_list()
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_list()
            lvl = min(len(m.group(1)) + 1, 6)  # demote: page owns <h1>
            out.append(f"<h{lvl}>{_inline(m.group(2).strip())}</h{lvl}>")
            i += 1
            continue

        m = re.match(r"^\s*[-*+]\s+(.*)$", line)
        if m:
            if list_open != "ul":
                close_list()
                out.append("<ul>")
                list_open = "ul"
            out.append(f"<li>{_inline(m.group(1))}</li>")
            i += 1
            continue

        m = re.match(r"^\s*(\d+)[.)]\s+(.*)$", line)
        if m:
            if list_open != "ol":
                close_list()
                out.append("<ol>")
                list_open = "ol"
            out.append(f"<li>{_inline(m.group(2))}</li>")
            i += 1
            continue

        if re.match(r"^\s*(---|\*\*\*|___)\s*$", line):
            close_list()
            out.append("<hr>")
            i += 1
            continue

        if line.startswith(">"):
            close_list()
            out.append(f"<blockquote>{_inline(line.lstrip('> '))}</blockquote>")
            i += 1
            continue

        close_list()
        para = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(
            r"^(#{1,6}\s|```|\s*[-*+]\s|\s*\d+[.)]\s|>)", lines[i]
        ):
            para.append(lines[i])
            i += 1
        out.append(f"<p>{_inline(' '.join(l.strip() for l in para))}</p>")

    close_list()
    return "\n".join(out)


# --------------------------------------------------------------------------
# collect
# --------------------------------------------------------------------------

def dir_stats(path: Path) -> tuple[int, int]:
    files = 0
    size = 0
    for root, dirs, names in os.walk(path):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_FROM_ZIP]
        for n in names:
            if n in EXCLUDE_FROM_ZIP:
                continue
            files += 1
            try:
                size += (Path(root) / n).stat().st_size
            except OSError:
                pass
    return files, size


def human_size(n: int) -> str:
    for unit in ("B", "KB", "MB"):
        if n < 1024 or unit == "MB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} MB"


def collect(meta: dict) -> list[dict]:
    skills = []
    broken = []
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        # Case-sensitive on purpose: macOS resolves skill.md to SKILL.md but the
        # Linux CI runner does not, which silently drops the skill from the site.
        skill_md = d / "SKILL.md"
        if "SKILL.md" not in {p.name for p in d.iterdir()}:
            broken.append(d.name)
            continue
        fm, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        m = meta["skills"].get(d.name, {})
        files, size = dir_stats(d)
        extras = sorted(
            p.name for p in d.iterdir() if p.is_dir() and p.name not in EXCLUDE_FROM_ZIP
        )
        skills.append(
            {
                "slug": d.name,
                "name": fm.get("name", d.name),
                "title": m.get("title") or fm.get("name", d.name),
                "summary": m.get("summary") or " ".join(str(fm.get("description", "")).split())[:220],
                "description": " ".join(str(fm.get("description", "")).split()),
                "category": m.get("category", "Uncategorized"),
                "tags": m.get("tags", []),
                "origin": m.get("origin", "jeonck"),
                "output_language": m.get("output_language", "en"),
                "license": "Apache-2.0" if (d / "LICENSE.txt").exists() else "MIT",
                "files": files,
                "size": size,
                "size_human": human_size(size),
                "folders": extras,
                "body_html": rewrite_relative_links(markdown_to_html(body), d.name),
                "zip": f"dist/{d.name}.zip",
                "icon": SKILL_ICONS.get(d.name, FALLBACK_ICON),
                "cat_slug": CATEGORY_SLUGS.get(m.get("category", ""), "dev"),
            }
        )
    missing_icons = [s for s in SKILLS_DIR.iterdir() if s.is_dir() and s.name not in SKILL_ICONS]
    if missing_icons:
        print("  ! no icon mapped (using fallback): " + ", ".join(p.name for p in missing_icons))
    if broken:
        raise SystemExit(
            "error: these skill directories have no SKILL.md (exact case):\n  "
            + "\n  ".join(broken)
        )
    return skills


# --------------------------------------------------------------------------
# render
# --------------------------------------------------------------------------

def page(title: str, body: str, depth: int = 0, desc: str = "", favicon: str = "") -> str:
    root = "../" * depth
    icon_href = favicon or (
        "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
        "<text y='.9em' font-size='90'>&#129526;</text></svg>"
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc or SITE['tagline'])}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc or SITE['tagline'])}">
<meta property="og:type" content="website">
<link rel="icon" href="{icon_href}">
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
{body}
</body>
</html>
"""


def install_block(slug: str, depth: int) -> str:
    url = f"{SITE['base_url']}/dist/{slug}.zip"
    cmd = (
        f"mkdir -p ~/.claude/skills && curl -fsSL {url} \\\n"
        f"  -o /tmp/{slug}.zip && unzip -oq /tmp/{slug}.zip -d ~/.claude/skills"
    )
    return f"""<div class="install">
  <div class="install-head"><span>Install</span><button class="copy" data-copy="{html.escape(cmd)}">Copy</button></div>
  <pre><code>{html.escape(cmd)}</code></pre>
</div>"""


def render_index(skills: list[dict], meta: dict) -> str:
    cats = [c for c in meta["categories"] if any(s["category"] == c for s in skills)]
    total_size = human_size(sum(s["size"] for s in skills))

    chips = "".join(
        f'<button class="chip" data-cat="{html.escape(c)}">{html.escape(c)} '
        f'<span>{sum(1 for s in skills if s["category"] == c)}</span></button>'
        for c in cats
    )

    cards = []
    for s in skills:
        tags = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in s["tags"][:4])
        origin = (
            '<span class="badge anthropic">Anthropic</span>'
            if s["origin"] == "anthropic"
            else ""
        )
        ko = '<span class="badge ko">KO output</span>' if s["output_language"] == "ko" else ""
        haystack = html.escape(
            " ".join([s["slug"], s["title"], s["summary"], s["category"], *s["tags"]]).lower()
        )
        cards.append(
            f"""<article class="card" data-cat="{html.escape(s['category'])}" data-search="{haystack}">
  <a class="card-link" href="s/{s['slug']}/">
    <div class="card-top">
      <span class="tile c-{s['cat_slug']}">{icon_svg(s['icon'], 22)}</span>
      <div>
        <h3>{html.escape(s['title'])}</h3>
        <code class="slug">{html.escape(s['slug'])}</code>
      </div>
    </div>
    <p>{html.escape(s['summary'])}</p>
  </a>
  <div class="card-foot">
    <div class="tags">{tags}{origin}{ko}</div>
    <button class="copy mini" data-copy="{html.escape(f'curl -fsSL {SITE["base_url"]}/dist/{s["slug"]}.zip -o /tmp/{s["slug"]}.zip && unzip -oq /tmp/{s["slug"]}.zip -d ~/.claude/skills')}">Copy install</button>
  </div>
</article>"""
        )

    body = f"""<header class="hero">
  <div class="wrap">
    <div class="eyebrow">github.com/{SITE['repo']}</div>
    <h1>Claude Skill Hub</h1>
    <p class="lede">{len(skills)} installable skills for Claude Code and Claude.ai — site builders,
    content pipelines, design systems, video production and dev tooling. Copy one command, drop it in
    <code>~/.claude/skills</code>, done.</p>
    <div class="stats">
      <span><b>{len(skills)}</b> skills</span>
      <span><b>{len(cats)}</b> categories</span>
      <span><b>{total_size}</b> total</span>
    </div>
    <div class="hero-actions">
      <a class="btn" href="#catalog">Browse catalog</a>
      <a class="btn ghost" href="https://github.com/{SITE['repo']}">View on GitHub</a>
    </div>
  </div>
</header>

<section class="wrap howto">
  <h2>How to install</h2>
  <div class="cols">
    <div>
      <h4>One skill</h4>
      <p>Every skill page has a copy-paste command. It downloads that skill's zip and unpacks it into your skills folder.</p>
      <pre><code>curl -fsSL {SITE['base_url']}/dist/&lt;skill&gt;.zip \\
  -o /tmp/skill.zip &amp;&amp; unzip -oq /tmp/skill.zip -d ~/.claude/skills</code></pre>
    </div>
    <div>
      <h4>All of them</h4>
      <p>Clone the repo and copy or symlink the whole <code>skills/</code> folder.</p>
      <pre><code>git clone https://github.com/{SITE['repo']}.git
cp -r skill-hub/skills/* ~/.claude/skills/</code></pre>
    </div>
  </div>
  <p class="note">Personal skills live in <code>~/.claude/skills/</code>. For a single project use
  <code>.claude/skills/</code> in the repo instead. Restart Claude Code, or start a new session, to pick them up.</p>
</section>

<main class="wrap" id="catalog">
  <div class="toolbar">
    <input id="q" type="search" placeholder="Search {len(skills)} skills…" autocomplete="off" spellcheck="false">
    <div class="chips"><button class="chip active" data-cat="all">All <span>{len(skills)}</span></button>{chips}</div>
  </div>
  <div class="grid">{''.join(cards)}</div>
  <p class="empty" hidden>No skill matches that search.</p>
</main>

<footer class="wrap">
  <p>Skills authored by <a href="https://github.com/{SITE['owner']}">{SITE['owner']}</a> are MIT licensed.
  Skills marked <span class="badge anthropic">Anthropic</span> are redistributed from
  <a href="https://github.com/anthropics/skills">anthropics/skills</a> under Apache-2.0, with their
  original <code>LICENSE.txt</code> intact.</p>
  <p><a href="catalog.json">catalog.json</a> · <a href="https://github.com/{SITE['repo']}">source</a></p>
</footer>

<script src="assets/app.js"></script>"""
    return page(SITE["title"], body, depth=0)


def render_detail(s: dict, skills: list[dict]) -> str:
    related = [
        r for r in skills if r["category"] == s["category"] and r["slug"] != s["slug"]
    ][:4]
    rel_html = "".join(
        f'<a class="rel" href="../{r["slug"]}/">'
        f'<span class="tile sm c-{r["cat_slug"]}">{icon_svg(r["icon"], 18)}</span>'
        f'<b>{html.escape(r["title"])}</b>'
        f'<span class="rel-sum">{html.escape(r["summary"][:90])}…</span></a>'
        for r in related
    )
    tags = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in s["tags"])
    folders = (
        "".join(f"<code>{html.escape(f)}/</code> " for f in s["folders"]) or "<em>none</em>"
    )
    origin_line = (
        f'Redistributed from <a href="https://github.com/anthropics/skills">anthropics/skills</a> (Apache-2.0)'
        if s["origin"] == "anthropic"
        else f'Authored by <a href="https://github.com/{SITE["owner"]}">{SITE["owner"]}</a> (MIT)'
    )
    lang_note = (
        '<p class="note">This skill produces Korean-language output by default.</p>'
        if s["output_language"] == "ko"
        else ""
    )

    body = f"""<nav class="crumb wrap"><a href="../../">← All skills</a></nav>
<header class="wrap detail-head">
  <div class="head-row">
    <span class="tile lg c-{s['cat_slug']}">{icon_svg(s['icon'], 34)}</span>
    <div>
      <div class="cat">{html.escape(s['category'])}</div>
      <h1>{html.escape(s['title'])}</h1>
      <code class="slug big">{html.escape(s['slug'])}</code>
    </div>
  </div>
  <p class="lede">{html.escape(s['summary'])}</p>
  <div class="tags">{tags}</div>
</header>

<section class="wrap">
  {install_block(s['slug'], 2)}
  <div class="facts">
    {f"<div><span>Invoke as</span><b><code>{html.escape(s['name'])}</code></b></div>" if s['name'] != s['slug'] else ""}
    <div><span>Files</span><b>{s['files']}</b></div>
    <div><span>Size</span><b>{s['size_human']}</b></div>
    <div><span>Bundled folders</span><b>{folders}</b></div>
    <div><span>License</span><b>{s['license']}</b></div>
  </div>
  {lang_note}
  <p class="note">{origin_line} ·
  <a href="https://github.com/{SITE['repo']}/tree/main/skills/{s['slug']}">Browse files on GitHub</a> ·
  <a href="../../dist/{s['slug']}.zip">Download zip</a></p>
</section>

<section class="wrap trigger">
  <h2>When Claude uses it</h2>
  <p>{html.escape(s['description'])}</p>
</section>

<article class="wrap prose">
  <h2>SKILL.md</h2>
  {s['body_html']}
</article>

{f'<section class="wrap related"><h2>More in {html.escape(s["category"])}</h2><div class="rels">{rel_html}</div></section>' if related else ''}

<footer class="wrap"><p><a href="../../">← Back to the catalog</a> · <a href="https://github.com/{SITE['repo']}">source</a></p></footer>
<script src="../../assets/app.js"></script>"""
    return page(
        f"{s['title']} — {SITE['title']}",
        body,
        depth=2,
        desc=s["summary"],
        favicon=icon_data_uri(s["icon"]),
    )


# --------------------------------------------------------------------------
# zips
# --------------------------------------------------------------------------

def build_zip(slug: str, dest: Path) -> None:
    src = SKILLS_DIR / slug
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, names in os.walk(src):
            dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_FROM_ZIP)
            for n in sorted(names):
                if n in EXCLUDE_FROM_ZIP:
                    continue
                p = Path(root) / n
                z.write(p, Path(slug) / p.relative_to(src))


# --------------------------------------------------------------------------

README_START = "<!-- icons:start -->"
README_END = "<!-- icons:end -->"


def write_repo_icons(skills: list[dict]) -> None:
    """Emit assets/icons/<slug>.svg (committed, referenced by the README) and
    regenerate the README's icon table between its marker comments."""
    icon_dir = ROOT / "assets" / "icons"
    icon_dir.mkdir(parents=True, exist_ok=True)

    keep = set()
    for s in skills:
        color = CATEGORY_COLORS.get(s["cat_slug"], "#6366f1")
        (icon_dir / f"{s['slug']}.svg").write_text(
            icon_file_svg(s["icon"], color), encoding="utf-8"
        )
        keep.add(f"{s['slug']}.svg")
    for stale in icon_dir.glob("*.svg"):
        if stale.name not in keep:
            stale.unlink()

    by_cat: dict[str, list[dict]] = {}
    for s in skills:
        by_cat.setdefault(s["category"], []).append(s)

    rows = [
        f"{len(skills)} skills, one glyph each. Click any name for its install command.",
        "",
    ]
    for cat, group in by_cat.items():
        rows += [f"### {cat}", "", "| | Skill | What it does |", "| :-: | --- | --- |"]
        for s in sorted(group, key=lambda x: x["title"].lower()):
            img = f'<img src="assets/icons/{s["slug"]}.svg" width="22" alt="">'
            link = f'[**{s["title"]}**]({SITE["base_url"]}/s/{s["slug"]}/)<br>`{s["slug"]}`'
            rows.append(f"| {img} | {link} | {s['summary']} |")
        rows.append("")

    table = "\n".join(rows).rstrip() + "\n"
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    if README_START not in text or README_END not in text:
        print("  ! README markers missing, skipped the icon table")
        return
    head, rest = text.split(README_START, 1)
    _, tail = rest.split(README_END, 1)
    readme.write_text(
        f"{head}{README_START}\n\n{table}\n{README_END}{tail}", encoding="utf-8"
    )


def main() -> None:
    meta = json.loads((ROOT / "catalog" / "meta.json").read_text(encoding="utf-8"))
    skills = collect(meta)
    skills.sort(key=lambda s: (s["category"], s["title"].lower()))

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)

    shutil.copy(ROOT / "site" / "style.css", OUT / "assets" / "style.css")
    shutil.copy(ROOT / "site" / "app.js", OUT / "assets" / "app.js")

    (OUT / "index.html").write_text(render_index(skills, meta), encoding="utf-8")
    for s in skills:
        d = OUT / "s" / s["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(render_detail(s, skills), encoding="utf-8")
        build_zip(s["slug"], OUT / "dist" / f"{s['slug']}.zip")

    (OUT / "catalog.json").write_text(
        json.dumps(
            {
                "site": SITE,
                "count": len(skills),
                "skills": [
                    {k: v for k, v in s.items() if k != "body_html"} for s in skills
                ],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    write_repo_icons(skills)

    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    if SITE.get("custom_domain"):
        (OUT / "CNAME").write_text(SITE["custom_domain"] + "\n", encoding="utf-8")

    print(f"built {len(skills)} skills -> {OUT}")


if __name__ == "__main__":
    main()
