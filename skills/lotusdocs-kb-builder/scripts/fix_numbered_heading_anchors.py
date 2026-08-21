#!/usr/bin/env python3
"""Give numbered `## N. Title` headings an explicit anchor that does not start
with a digit.

Hugo derives heading IDs from the heading text, so `## 1. Ownership` becomes
id="1-ownership". `#1-ownership` is not a valid CSS selector, and Bootstrap
ScrollSpy calls querySelector() on every table-of-contents link — the throw
aborts the rest of the page's JS. Setting the ID explicitly via Goldmark's
attribute block keeps the visible numbering and fixes both the TOC links and
the rendered heading, because Hugo's TableOfContents honours the attribute.
"""
import re
import sys
from pathlib import Path

HEADING = re.compile(r'^(?P<hashes>#{2,6}) (?P<num>\d+)\. (?P<title>.+?)(?P<attr> \{#[^}]+\})?$')


def slugify(text: str) -> str:
    text = re.sub(r'`([^`]*)`', r'\1', text)
    text = re.sub(r'\*\*([^*]*)\*\*', r'\1', text)
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return slug


def fix(path: Path) -> int:
    lines = path.read_text().split('\n')
    seen: set[str] = set()
    changed = 0
    in_fence = False

    for i, line in enumerate(lines):
        if line.lstrip().startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        m = HEADING.match(line)
        if not m or m.group('attr'):
            continue

        slug = slugify(m.group('title')) or f"section-{m.group('num')}"
        if slug[0].isdigit():
            slug = f"s-{slug}"
        if slug in seen:
            slug = f"{slug}-{m.group('num')}"
        seen.add(slug)

        lines[i] = f"{m.group('hashes')} {m.group('num')}. {m.group('title')} {{#{slug}}}"
        changed += 1

    if changed:
        path.write_text('\n'.join(lines))
    return changed


total_files = total_headings = 0
for md in sorted(Path(sys.argv[1]).rglob('*.md')):
    n = fix(md)
    if n:
        total_files += 1
        total_headings += n

print(f"rewrote {total_headings} headings across {total_files} files")
