# Claude Skill Hub

[![Browse the catalog](https://img.shields.io/badge/Browse_the_catalog-skill.metacog.co.kr-c2410c?style=for-the-badge)](https://skill.metacog.co.kr)

[![Skills](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fskill.metacog.co.kr%2Fcatalog.json&query=%24.count&label=skills&color=1b1917)](https://skill.metacog.co.kr)
[![Deploy](https://github.com/jeonck/skill-hub/actions/workflows/deploy.yml/badge.svg)](https://github.com/jeonck/skill-hub/actions/workflows/deploy.yml)
[![License](https://img.shields.io/badge/license-MIT-1b1917)](LICENSE)

A public catalog of installable [Claude](https://claude.com/claude-code) skills — site
builders, content pipelines, design systems, video production and dev tooling.

Every skill on the site has a copy-paste install command. Nothing to sign up for, no
package manager.

## Install one skill

```bash
mkdir -p ~/.claude/skills && curl -fsSL https://skill.metacog.co.kr/dist/hugo-blog-builder.zip \
  -o /tmp/skill.zip && unzip -oq /tmp/skill.zip -d ~/.claude/skills
```

Swap `hugo-blog-builder` for any slug in the [catalog](https://skill.metacog.co.kr).

## Install all of them

```bash
git clone https://github.com/jeonck/skill-hub.git
cp -r skill-hub/skills/* ~/.claude/skills/
```

## Where skills go

| Scope | Path |
| --- | --- |
| Personal (all projects) | `~/.claude/skills/<skill-name>/` |
| One project | `<repo>/.claude/skills/<skill-name>/` |

Start a new Claude Code session afterwards so the skill is picked up. Claude invokes a
skill automatically when your request matches its description — you can also name it
directly, e.g. *"use the hugo-blog-builder skill"*.

## Repository layout

```
skills/                  one directory per skill, each with a SKILL.md
catalog/meta.json        English titles, summaries, categories and tags for the site
site/                    stylesheet and catalog JavaScript
tools/build.py           static site generator (standard library only)
.github/workflows/       builds the site + per-skill zips, deploys to GitHub Pages
```

## Building locally

```bash
python3 tools/build.py     # writes _site/
python3 -m http.server 8000 --directory _site
```

No dependencies beyond Python 3.9+.

## Adding a skill

1. Drop the skill directory into `skills/`. It must contain a `SKILL.md` with `name` and
   `description` frontmatter.
2. Add an entry to `catalog/meta.json` with an English `title`, `summary`, `category` and
   `tags`. Without it the site falls back to the raw frontmatter description.
3. Push to `main`. The workflow rebuilds the catalog and the zip.

## Machine-readable catalog

[`catalog.json`](https://skill.metacog.co.kr/catalog.json) lists every skill with
its slug, summary, category, tags, size and zip path.

## License and attribution

Skills authored by [@jeonck](https://github.com/jeonck) are released under the
[MIT License](LICENSE).

Skills marked **Anthropic** on the site are redistributed from
[anthropics/skills](https://github.com/anthropics/skills) under Apache-2.0, with their
original `LICENSE.txt` kept inside each skill directory. See [NOTICE](NOTICE) for the
full list.

Anthropic's proprietary document skills (`docx`, `pdf`, `pptx`, `xlsx`) are **not**
included here — their license prohibits redistribution. Get them from Anthropic directly.
