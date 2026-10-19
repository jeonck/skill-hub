# council

[Council of High Intelligence](https://github.com/0xNyk/council-of-high-intelligence)
(MIT) — 18 historical-thinker personas (Socrates, Feynman, Kahneman, Torvalds,
Taleb and 14 more, each a distinct reasoning method, not just a voice) convened
as real Claude Code subagents to deliberate a hard decision: independent
analysis → anonymized cross-examination with enforced dissent → confidence-weighted
tiebreaking → a Chairman's verdict with a Minority Report.

Only the Claude Code path of the upstream project is mirrored here — it also
ships Codex, Gemini CLI and OpenCode variants, which this catalog doesn't carry.

## Install — two parts

This skill is unusual in this catalog: **it needs real subagents, not just a
SKILL.md.** `/council` spawns each member as an actual Claude Code subagent
(`Task` with `subagent_type: council-<name>`), so the 18 files under `agents/`
have to land in Claude Code's *subagent* directory, not inside the skill folder.

**If you're running Claude Code from a clone of this repo**, `.claude/skills/`
and `.claude/agents/` are already populated — `python3 tools/link_skills.py`
symlinks every skill's `SKILL.md` into `.claude/skills/`, and additionally
symlinks `skills/council/agents/*.md` into `.claude/agents/`, since those are
real subagents rather than skill content. Nothing else to do; re-run that
script after pulling if a skill was added, renamed or removed.

**If you're installing this skill elsewhere** (the catalog site's zip, or
copied out of this repo by hand), place the two pieces yourself:

```bash
mkdir -p ~/.claude/skills/council ~/.claude/agents
cp SKILL.md configs/* scripts/* ~/.claude/skills/council/   # (configs/, scripts/ as subdirs)
cp agents/council-*.md ~/.claude/agents/
chmod +x ~/.claude/skills/council/scripts/detect-providers.sh
```

Drop `~/` for a project-local install (`.claude/skills/council`,
`.claude/agents/`). Without the second `cp`, `/council` loads but has no
members to spawn.

## Use

```
/council Should we use a monorepo or polyrepo?
/council --triad architecture ...
/council --quick Should we add caching here?
/council --duo --members torvalds,ada Is this abstraction worth it?
```

Full flag and panel reference is in `SKILL.md` itself — triads, profiles,
provider routing, the enforcement rules that keep Round 2 from collapsing into
agreement, and the confidence-weighted tiebreak. Read it before the first run;
it's long because the deliberation protocol is the product.
