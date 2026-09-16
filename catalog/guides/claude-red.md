This library is **linked, not mirrored** — the hub does not host its 78 files.
Install it from the upstream repository, then drive it from any project.

## Install

Clone the repo and run its installer. The default target namespaces everything
under `~/.claude/skills/claude-red/`, so it never collides with your other skills.

```bash
git clone https://github.com/SnailSploit/Claude-Red.git
cd Claude-Red && ./install.sh
```

One category only, or a preview of what would be copied:

```bash
./install.sh --list                 # list categories (web, cloud, wireless, …)
./install.sh --category web          # install just the web skills
./install.sh --dry-run               # show what would be copied
```

Start a new Claude Code session afterwards so the skills are discovered.

Note: about a third of the skills use a non-YAML format that Claude Code does
not auto-load. The repo ships `convert_skills.py` to normalise them if you want
the full set active.

## Use it

The skills are not commands — describe the task and the matching skill activates.

```
Check this login form for SQL injection
Look for IDOR on this API
Verify whether JWT validation can be bypassed here
```

To name one explicitly: *"use claude-red's offensive-ssrf skill on this endpoint."*

## Full assessment prompt

For a broad sweep, give scope, authorization and a target, and let it map the
relevant attack surfaces rather than running all 78 skills blindly:

```
This repository is mine and I am authorized to test it. Use the claude-red
skills to run a general security assessment.

1. First read the codebase and identify the stack and attack surfaces
   (web framework, auth, APIs, DB, file upload, integrations, CI/CD).
2. Map only the claude-red skills relevant to those surfaces — list which
   skills you will apply and why before starting.
3. Work each one by its methodology. For every finding record:
   severity / location (file:line) / how to reproduce / impact / fix.
4. Write it up in the offensive-reporting format to report.md.

Static analysis of code and config only — do not execute attacks or reach
external systems. Do not guess; mark anything uncertain as "needs verification".
```

**Adjust the scope:** narrow with *"web vulnerabilities only"* or *"auth/authz only"*;
change depth with *"just the top risks, fast"* vs *"thorough per surface"*. For a
live target (staging), drop the static-analysis line and instead state the target
URL, the authorized scope, and anything out of bounds — that is a different mode.

## Authorized use only

These are dual-use offensive-security methodologies. Use them only on systems you
own or are contracted to test. Claude will not proceed against targets you have no
authorization for.
