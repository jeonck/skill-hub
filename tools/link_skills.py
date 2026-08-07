#!/usr/bin/env python3
"""Regenerate .claude/skills/ so every skill in this repo is a project skill.

Claude Code discovers project skills at .claude/skills/<name>/SKILL.md, where the
directory name has to match the skill's frontmatter `name`. A handful of skills in
this repo use a catalog slug that differs from that name (brutalist-skill holds
industrial-brutalist-ui, and so on), so each entry is a symlink named after the
frontmatter and pointing at the slug directory.

Existing links are dropped first, which prunes skills that were renamed or removed.

Standard library only. Run:  python3 tools/link_skills.py
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "skills"
DST = ROOT / ".claude" / "skills"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---", re.S)
NAME_RE = re.compile(r"^name:\s*(.+)$", re.M)


def skill_name(skill_md: Path) -> str | None:
    """Return the frontmatter `name` of a SKILL.md, or None if it has none."""
    match = FRONTMATTER_RE.match(skill_md.read_text(encoding="utf-8"))
    if not match:
        return None
    name = NAME_RE.search(match.group(1))
    return name.group(1).strip().strip("\"'") if name else None


def main() -> int:
    if not SRC.is_dir():
        print(f"no skills directory at {SRC}", file=sys.stderr)
        return 1

    DST.mkdir(parents=True, exist_ok=True)
    for stale in DST.iterdir():
        if stale.is_symlink():
            stale.unlink()

    taken: dict[str, str] = {}
    failed = False

    for slug_dir in sorted(p for p in SRC.iterdir() if p.is_dir()):
        skill_md = slug_dir / "SKILL.md"
        if not skill_md.is_file():
            print(f"skip {slug_dir.name}: no SKILL.md", file=sys.stderr)
            failed = True
            continue

        name = skill_name(skill_md)
        if not name:
            print(f"skip {slug_dir.name}: no `name` in frontmatter", file=sys.stderr)
            failed = True
            continue

        if name in taken:
            print(
                f"skip {slug_dir.name}: name {name!r} already used by {taken[name]}",
                file=sys.stderr,
            )
            failed = True
            continue

        link = DST / name
        if link.exists() and not link.is_symlink():
            print(f"skip {slug_dir.name}: {link} exists and is not a symlink", file=sys.stderr)
            failed = True
            continue

        os.symlink(os.path.join("..", "..", "skills", slug_dir.name), link)
        taken[name] = slug_dir.name

    for name, slug in sorted(taken.items()):
        print(f"{name}{'' if name == slug else f'  <- skills/{slug}'}")
    print(f"\n{len(taken)} skills linked into {DST.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
