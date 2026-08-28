#!/usr/bin/env python3
"""
Check that every relative/absolute internal markdown link under a Hugo
content directory resolves to a real page.

Usage:
    python3 check_internal_links.py [content_dir] [--base /docs]

    content_dir  Path to the Hugo content directory to scan (default: content/docs)
    --base       The URL path prefix that maps to content_dir (default: /docs)
                 Used to resolve absolute links like [text](/docs/foo/bar/).

Why this exists: relative markdown links in Hugo resolve against the PAGE'S
OWN URL, not the source file's parent directory. A leaf page
`content/docs/x/y.md` is served at `/docs/x/y/` — so `../z/` from inside it
resolves to `/docs/x/z/`, not `/docs/z/`. A naive path-join check gets this
off by one directory level. This script gets it right by treating every
non-_index.md file as if it were its own directory before resolving `../`
and `./` links.

Exits non-zero and prints every broken link if any are found; otherwise
prints a one-line OK summary and exits 0.
"""
import argparse
import os
import re
import sys

LINK_RE = re.compile(r"\]\(([^)]+)\)")


def collect_valid_targets(content_dir):
    valid = set()
    for root, _dirs, files in os.walk(content_dir):
        for f in files:
            if not f.endswith(".md"):
                continue
            if f == "_index.md":
                valid.add(os.path.normpath(root))
            else:
                valid.add(os.path.normpath(os.path.join(root, f[:-3])))
    return valid


def check(content_dir, base_url):
    valid = collect_valid_targets(content_dir)
    errors = []

    for root, _dirs, files in os.walk(content_dir):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            # A leaf page acts as its own URL directory when resolving
            # relative links; an _index.md page's URL directory is the
            # folder itself.
            page_base = root if f == "_index.md" else os.path.join(root, f[:-3])
            text = open(path, encoding="utf-8").read()

            for m in LINK_RE.finditer(text):
                url = m.group(1)
                if url.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                # A #fragment / ?query is not part of the path — strip it
                # before resolving, or every deep link reads as broken.
                link = url.split("#", 1)[0].split("?", 1)[0]
                if not link:
                    continue
                if link.startswith(base_url.rstrip("/") + "/"):
                    rel = link[len(base_url.rstrip("/")) :].strip("/")
                    target = os.path.normpath(os.path.join(content_dir, rel))
                elif link.startswith(("../", "./")):
                    target = os.path.normpath(os.path.join(page_base, link))
                else:
                    continue
                if target not in valid:
                    errors.append((path, url, target))

    return errors


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("content_dir", nargs="?", default="content/docs")
    p.add_argument("--base", default="/docs")
    args = p.parse_args()

    if not os.path.isdir(args.content_dir):
        print(f"error: {args.content_dir!r} is not a directory", file=sys.stderr)
        sys.exit(2)

    errors = check(args.content_dir, args.base)
    if errors:
        print(f"{len(errors)} broken internal link(s):")
        for path, url, target in errors:
            print(f"  {path} -> {url}  (resolved: {target})")
        sys.exit(1)

    print(f"OK: all internal links under {args.content_dir} resolve correctly.")


if __name__ == "__main__":
    main()
