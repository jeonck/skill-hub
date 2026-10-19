#!/usr/bin/env python3
"""Regenerate .claude/skills/ and .claude/agents/ so every skill in this repo is
live in a Claude Code session started from the repo root.

Claude Code discovers project skills at .claude/skills/<name>/SKILL.md, where the
directory name has to match the skill's frontmatter `name`. A handful of skills in
this repo use a catalog slug that differs from that name (brutalist-skill holds
industrial-brutalist-ui, and so on), so each entry is a symlink named after the
frontmatter and pointing at the slug directory.

A few skills (council, so far) also ship real Claude Code subagents — files meant
to land in .claude/agents/, not nested inside the skill directory, because that is
where Task(subagent_type: ...) looks for them. Any skills/<slug>/agents/*.md is
linked into .claude/agents/ by its own filename, flat, alongside the skill link.

Existing links are dropped first, which prunes skills (and agents) that were
renamed or removed.

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
AGENTS_DST = ROOT / ".claude" / "agents"

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

    AGENTS_DST.mkdir(parents=True, exist_ok=True)
    for stale in AGENTS_DST.iterdir():
        if stale.is_symlink():
            stale.unlink()

    taken: dict[str, str] = {}
    agents_taken: dict[str, str] = {}
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

        agents_dir = slug_dir / "agents"
        if agents_dir.is_dir():
            for agent_md in sorted(agents_dir.glob("*.md")):
                if agent_md.name in agents_taken:
                    print(
                        f"skip {slug_dir.name}/agents/{agent_md.name}: "
                        f"already provided by {agents_taken[agent_md.name]}",
                        file=sys.stderr,
                    )
                    failed = True
                    continue
                agent_link = AGENTS_DST / agent_md.name
                if agent_link.exists() and not agent_link.is_symlink():
                    print(
                        f"skip {slug_dir.name}/agents/{agent_md.name}: "
                        f"{agent_link} exists and is not a symlink",
                        file=sys.stderr,
                    )
                    failed = True
                    continue
                os.symlink(
                    os.path.join("..", "..", "skills", slug_dir.name, "agents", agent_md.name),
                    agent_link,
                )
                agents_taken[agent_md.name] = slug_dir.name

    for name, slug in sorted(taken.items()):
        print(f"{name}{'' if name == slug else f'  <- skills/{slug}'}")
    print(f"\n{len(taken)} skills linked into {DST.relative_to(ROOT)}")
    if agents_taken:
        by_slug: dict[str, int] = {}
        for slug in agents_taken.values():
            by_slug[slug] = by_slug.get(slug, 0) + 1
        summary = ", ".join(f"{n} from {slug}" for slug, n in sorted(by_slug.items()))
        print(f"{len(agents_taken)} subagents linked into {AGENTS_DST.relative_to(ROOT)} ({summary})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
