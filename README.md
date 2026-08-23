<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo.svg" width="76" height="76" alt="">
  </picture>
</p>

<h1 align="center">Claude Skill Hub</h1>

<p align="center">
  A public catalog of installable <a href="https://claude.com/claude-code">Claude</a> skills —<br>
  site builders, content pipelines, design systems, video production and dev tooling.
</p>

<p align="center">
  <a href="https://skill.metacog.co.kr"><img src="https://img.shields.io/badge/Browse_the_catalog-skill.metacog.co.kr-c2410c?style=for-the-badge" alt="Browse the catalog"></a>
</p>

<p align="center">
  <a href="https://skill.metacog.co.kr"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fskill.metacog.co.kr%2Fcatalog.json&query=%24.count&label=skills&color=1b1917" alt="Skills"></a>
  <a href="https://github.com/jeonck/skill-hub/actions/workflows/deploy.yml"><img src="https://github.com/jeonck/skill-hub/actions/workflows/deploy.yml/badge.svg" alt="Deploy"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-1b1917" alt="License"></a>
</p>

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

## The skills

<!-- icons:start -->

62 skills, one glyph each. Click any name for its install command.

### Automation Pipelines

| | Skill | What it does |
| :-: | --- | --- |
| <img src="assets/icons/daily-diary-pipeline.svg" width="22" alt=""> | [**Daily Diary Pipeline**](https://skill.metacog.co.kr/s/daily-diary-pipeline/)<br>`daily-diary-pipeline` | Scaffold a pipeline where editing one line in a GitHub file triggers a scheduled Claude run that writes a post and publishes it to Hugo + GitHub Pages. |
| <img src="assets/icons/daily-insight-pipeline.svg" width="22" alt=""> | [**Daily Insight Pipeline**](https://skill.metacog.co.kr/s/daily-insight-pipeline/)<br>`daily-insight-pipeline` | Scaffold a daily collect-and-triage pipeline — pull from RSS, Reddit, HN and GitHub, have Claude rate each item act-now / backlog / learn / ignore, then ship it to a site. |
| <img src="assets/icons/term-comparison-pipeline.svg" width="22" alt=""> | [**Term Comparison Pipeline**](https://skill.metacog.co.kr/s/term-comparison-pipeline/)<br>`term-comparison-pipeline` | On-demand comparison posts — add one line like "REST vs GraphQL" to a file, and the push triggers Claude to generate an SVG diagram plus comparison table and deploy it. No cron, no fallback content. |
| <img src="assets/icons/transcript-study-pipeline.svg" width="22" alt=""> | [**Transcript Study Pipeline**](https://skill.metacog.co.kr/s/transcript-study-pipeline/)<br>`transcript-study-pipeline` | Turn pasted class transcripts into structured English-study posts — idioms with examples, vocabulary, spoken-mistake corrections, fill-in-the-blank quizzes and a mini diary — published on push. |

### Content & Writing

| | Skill | What it does |
| :-: | --- | --- |
| <img src="assets/icons/us-work-english-idiom-section.svg" width="22" alt=""> | [**Business Idiom Section**](https://skill.metacog.co.kr/s/us-work-english-idiom-section/)<br>`us-work-english-idiom-section` | Write a business-idiom section as collapsible blocks — one bold English line and a single key bullet per expression, nothing else. |
| <img src="assets/icons/ccnp-ccie-writer.svg" width="22" alt=""> | [**CCNP / CCIE Knowledge Writer**](https://skill.metacog.co.kr/s/ccnp-ccie-writer/)<br>`ccnp-ccie-writer` | Write Cisco CCNP/CCIE knowledge-base docs in a fixed structure — definition, characteristics, components, packet flow, comparison tables, config and exam points — with Mermaid diagrams. |
| <img src="assets/icons/cisa-content-writer.svg" width="22" alt=""> | [**CISA Content Writer**](https://skill.metacog.co.kr/s/cisa-content-writer/)<br>`cisa-content-writer` | Author CISA (IS audit) best-practice guides across the six ISACA domains — a standard 10-section layout with Mermaid diagrams and HTML audit checklists. |
| <img src="assets/icons/internal-comms.svg" width="22" alt=""> | [**Internal Comms**](https://skill.metacog.co.kr/s/internal-comms/)<br>`internal-comms` | Write internal communications in house formats — status reports, leadership updates, newsletters, FAQs, incident reports and project updates. |
| <img src="assets/icons/it-professional-content.svg" width="22" alt=""> | [**IT Professional Engineer Content**](https://skill.metacog.co.kr/s/it-professional-content/)<br>`it-professional-content` | Write framework and methodology content in the Korean 기술사 exam format — a 3-section structure with block diagrams, Mermaid visualizations and comparison tables. |
| <img src="assets/icons/problem-note.svg" width="22" alt=""> | [**Problem Note Writer**](https://skill.metacog.co.kr/s/problem-note/)<br>`problem-note` | Write up an ICT incident, error log or troubleshooting session as a structured problem note for a Quartz v5 second brain — plus concept notes, MOC pages and a masking check before anything goes public. |
| <img src="assets/icons/us-work-english-content.svg" width="22" alt=""> | [**US Work English Content**](https://skill.metacog.co.kr/s/us-work-english-content/)<br>`us-work-english-content` | Add expression-practice pages to a Docusaurus English-learning site — thematic collapsible groups, bold expressions with key/source/similar bullets, tip admonitions and sidebar wiring. |

### Design & UI

| | Skill | What it does |
| :-: | --- | --- |
| <img src="assets/icons/algorithmic-art.svg" width="22" alt=""> | [**Algorithmic Art**](https://skill.metacog.co.kr/s/algorithmic-art/)<br>`algorithmic-art` | Generative art with p5.js — seeded randomness, flow fields, particle systems, and an interactive parameter-exploration loop. |
| <img src="assets/icons/banner-design.svg" width="22" alt=""> | [**Banner Design**](https://skill.metacog.co.kr/s/banner-design/)<br>`banner-design` | Banners for social, ads, website heroes and print — multiple art directions per brief across Facebook, X, LinkedIn, YouTube, Instagram and Google Display sizes. |
| <img src="assets/icons/brand-guidelines.svg" width="22" alt=""> | [**Brand Guidelines**](https://skill.metacog.co.kr/s/brand-guidelines/)<br>`brand-guidelines` | Apply Anthropic's official brand colors and typography to any artifact that benefits from a consistent house look-and-feel. |
| <img src="assets/icons/brandkit.svg" width="22" alt=""> | [**Brand Kit Generator**](https://skill.metacog.co.kr/s/brandkit/)<br>`brandkit` | Premium brand-guideline boards, logo systems and identity decks — minimalist, cinematic, editorial, dark-tech and luxury systems with art-directed mockups. |
| <img src="assets/icons/brand.svg" width="22" alt=""> | [**Brand Voice & Identity**](https://skill.metacog.co.kr/s/brand/)<br>`brand` | Brand voice, visual identity, messaging frameworks and asset management, with compliance checks for branded content. |
| <img src="assets/icons/canvas-design.svg" width="22" alt=""> | [**Canvas Design**](https://skill.metacog.co.kr/s/canvas-design/)<br>`canvas-design` | Design posters, art and static pieces as .png or .pdf using a real design philosophy rather than default template output. |
| <img src="assets/icons/design.svg" width="22" alt=""> | [**Design Direction**](https://skill.metacog.co.kr/s/design/)<br>`design` | Art direction and visual design decisions for product work, backed by the Pro Max reference data. |
| <img src="assets/icons/design-system.svg" width="22" alt=""> | [**Design System Tokens**](https://skill.metacog.co.kr/s/design-system/)<br>`design-system` | Three-layer token architecture (primitive → semantic → component), CSS variables, spacing and type scales, and component specs. |
| <img src="assets/icons/taste-skill.svg" width="22" alt=""> | [**Design Taste Frontend**](https://skill.metacog.co.kr/s/taste-skill/)<br>`taste-skill` | Anti-slop frontend for landing pages, portfolios and redesigns — read the brief, infer the right direction, and ship interfaces that don't look templated. |
| <img src="assets/icons/soft-skill.svg" width="22" alt=""> | [**High-End Visual Design**](https://skill.metacog.co.kr/s/soft-skill/)<br>`soft-skill` | Design like a high-end agency — the exact fonts, spacing, shadows, card structures and animations that make a site feel expensive, with the cheap-looking defaults blocked. |
| <img src="assets/icons/brutalist-skill.svg" width="22" alt=""> | [**Industrial Brutalist UI**](https://skill.metacog.co.kr/s/brutalist-skill/)<br>`brutalist-skill` | Raw mechanical interfaces fusing Swiss typographic print with military terminal aesthetics — rigid grids, extreme type contrast, analog degradation. |
| <img src="assets/icons/minimalist-skill.svg" width="22" alt=""> | [**Minimalist UI**](https://skill.metacog.co.kr/s/minimalist-skill/)<br>`minimalist-skill` | Clean editorial interfaces — warm monochrome palette, typographic contrast, flat bento grids, muted pastels. No gradients, no heavy shadows. |
| <img src="assets/icons/imagegen-frontend-mobile.svg" width="22" alt=""> | [**Mobile UI Image Direction**](https://skill.metacog.co.kr/s/imagegen-frontend-mobile/)<br>`imagegen-frontend-mobile` | Generate premium app-native mobile screen concepts and flows — clean hierarchy, multi-screen consistency, controlled palettes, framed in a subtle phone mockup. Images only, no code. |
| <img src="assets/icons/redesign-skill.svg" width="22" alt=""> | [**Redesign Existing Projects**](https://skill.metacog.co.kr/s/redesign-skill/)<br>`redesign-skill` | Upgrade an existing site or app to premium quality — audit the current design, name the generic AI patterns, and raise the bar without breaking functionality. |
| <img src="assets/icons/stitch-skill.svg" width="22" alt=""> | [**Stitch Design Taste**](https://skill.metacog.co.kr/s/stitch-skill/)<br>`stitch-skill` | Generate agent-friendly DESIGN.md files for Google Stitch — strict typography, calibrated color, asymmetric layouts, perpetual micro-motion and GPU-friendly performance rules. |
| <img src="assets/icons/slides.svg" width="22" alt=""> | [**Strategic Slides**](https://skill.metacog.co.kr/s/slides/)<br>`slides` | Build HTML presentations with Chart.js, design tokens, responsive layouts and copywriting formulas chosen per slide's job. |
| <img src="assets/icons/theme-factory.svg" width="22" alt=""> | [**Theme Factory**](https://skill.metacog.co.kr/s/theme-factory/)<br>`theme-factory` | Style any artifact — slides, docs, reports, landing pages — with one of 10 preset color/font themes, or generate a new theme on the fly. |
| <img src="assets/icons/ui-styling.svg" width="22" alt=""> | [**UI Styling**](https://skill.metacog.co.kr/s/ui-styling/)<br>`ui-styling` | Build accessible interfaces with shadcn/ui on Radix + Tailwind — themes, dark mode, responsive layout and consistent styling patterns. |
| <img src="assets/icons/ui-ux-pro-max.svg" width="22" alt=""> | [**UI/UX Pro Max**](https://skill.metacog.co.kr/s/ui-ux-pro-max/)<br>`ui-ux-pro-max` | Design intelligence for web, mobile and desktop interfaces — a searchable local corpus of 79 styles, 192 palettes, 74 font pairings, 119 UX guidelines, GSAP presets and per-stack implementation notes. |
| <img src="assets/icons/imagegen-frontend-web.svg" width="22" alt=""> | [**Web UI Image Direction**](https://skill.metacog.co.kr/s/imagegen-frontend-web/)<br>`imagegen-frontend-web` | Generate premium landing-page design references — one horizontal image per section, enforced composition variety, a narrative concept spine and one consistent palette throughout. |

### Dev Tooling

| | Skill | What it does |
| :-: | --- | --- |
| <img src="assets/icons/andrej-karpathy-skills.svg" width="22" alt=""> | [**Andrej Karpathy Guidelines**](https://github.com/multica-ai/andrej-karpathy-skills)<br>`andrej-karpathy-skills` — link only, not mirrored | Behavioural guidelines that head off the coding mistakes Karpathy flags in LLM output — overcomplication, sprawling edits, unstated assumptions, and success criteria nobody can verify. |
| <img src="assets/icons/artifacts-builder.svg" width="22" alt=""> | [**Artifacts Builder**](https://skill.metacog.co.kr/s/artifacts-builder/)<br>`artifacts-builder` | Build elaborate multi-component claude.ai HTML artifacts with React, Tailwind and shadcn/ui — for artifacts that need state, routing or a component library. |
| <img src="assets/icons/brainstorming.svg" width="22" alt=""> | [**Brainstorming**](https://skill.metacog.co.kr/s/brainstorming/)<br>`brainstorming` | Explore intent, requirements and design before any implementation, so creative work starts from a settled brief rather than a guess. |
| <img src="assets/icons/dispatching-parallel-agents.svg" width="22" alt=""> | [**Dispatching Parallel Agents**](https://skill.metacog.co.kr/s/dispatching-parallel-agents/)<br>`dispatching-parallel-agents` | Split 2+ tasks that share no state or ordering across parallel agents instead of running them in sequence. |
| <img src="assets/icons/executing-plans.svg" width="22" alt=""> | [**Executing Plans**](https://skill.metacog.co.kr/s/executing-plans/)<br>`executing-plans` | Work through a written implementation plan in a separate session, with review checkpoints between steps. |
| <img src="assets/icons/finishing-a-development-branch.svg" width="22" alt=""> | [**Finishing a Development Branch**](https://skill.metacog.co.kr/s/finishing-a-development-branch/)<br>`finishing-a-development-branch` | Decide how to integrate finished work once implementation is complete and the tests pass. |
| <img src="assets/icons/output-skill.svg" width="22" alt=""> | [**Full Output Enforcement**](https://skill.metacog.co.kr/s/output-skill/)<br>`output-skill` | Override default truncation behavior — enforce complete code generation, ban placeholder patterns, and handle token-limit splits cleanly. |
| <img src="assets/icons/mcp-builder.svg" width="22" alt=""> | [**MCP Builder**](https://skill.metacog.co.kr/s/mcp-builder/)<br>`mcp-builder` | Build high-quality MCP servers that expose external APIs to LLMs through well-designed tools — in Python (FastMCP) or Node/TypeScript (MCP SDK). |
| <img src="assets/icons/receiving-code-review.svg" width="22" alt=""> | [**Receiving Code Review**](https://skill.metacog.co.kr/s/receiving-code-review/)<br>`receiving-code-review` | Handle review feedback with technical rigor — verify each suggestion instead of agreeing performatively or implementing blindly. |
| <img src="assets/icons/requesting-code-review.svg" width="22" alt=""> | [**Requesting Code Review**](https://skill.metacog.co.kr/s/requesting-code-review/)<br>`requesting-code-review` | Ask for review at task completion, major features and pre-merge, so work is checked against its requirements. |
| <img src="assets/icons/skill-creator.svg" width="22" alt=""> | [**Skill Creator**](https://skill.metacog.co.kr/s/skill-creator/)<br>`skill-creator` | Create and update Claude skills — the guide for packaging specialized knowledge, workflows and tool integrations into a skill. |
| <img src="assets/icons/subagent-driven-development.svg" width="22" alt=""> | [**Subagent-Driven Development**](https://skill.metacog.co.kr/s/subagent-driven-development/)<br>`subagent-driven-development` | Execute a plan's independent tasks through subagents in the current session, with task briefs and a review package. |
| <img src="assets/icons/systematic-debugging.svg" width="22" alt=""> | [**Systematic Debugging**](https://skill.metacog.co.kr/s/systematic-debugging/)<br>`systematic-debugging` | Work a bug, test failure or surprise back to its root cause before proposing any fix. |
| <img src="assets/icons/test-driven-development.svg" width="22" alt=""> | [**Test-Driven Development**](https://skill.metacog.co.kr/s/test-driven-development/)<br>`test-driven-development` | Write the failing test before the implementation, for every feature and bugfix. |
| <img src="assets/icons/using-git-worktrees.svg" width="22" alt=""> | [**Using Git Worktrees**](https://skill.metacog.co.kr/s/using-git-worktrees/)<br>`using-git-worktrees` | Get an isolated workspace before feature work or plan execution, via native tooling or a git worktree fallback. |
| <img src="assets/icons/using-superpowers.svg" width="22" alt=""> | [**Using Superpowers**](https://skill.metacog.co.kr/s/using-superpowers/)<br>`using-superpowers` | Entry point for the Superpowers framework — how to find and invoke the right skill before answering, including clarifying questions. |
| <img src="assets/icons/verification-before-completion.svg" width="22" alt=""> | [**Verification Before Completion**](https://skill.metacog.co.kr/s/verification-before-completion/)<br>`verification-before-completion` | Run the verification commands and read the output before claiming anything is done, fixed or passing — evidence before assertions. |
| <img src="assets/icons/webapp-testing.svg" width="22" alt=""> | [**Web App Testing**](https://skill.metacog.co.kr/s/webapp-testing/)<br>`webapp-testing` | Drive and test local web apps with Playwright — verify frontend behavior, debug the UI, capture screenshots and read browser logs. |
| <img src="assets/icons/writing-plans.svg" width="22" alt=""> | [**Writing Plans**](https://skill.metacog.co.kr/s/writing-plans/)<br>`writing-plans` | Turn a spec or set of requirements into a written multi-step implementation plan before touching code. |
| <img src="assets/icons/writing-skills.svg" width="22" alt=""> | [**Writing Skills**](https://skill.metacog.co.kr/s/writing-skills/)<br>`writing-skills` | Create, edit and verify Claude skills before deploying them. |

### Media & Video

| | Skill | What it does |
| :-: | --- | --- |
| <img src="assets/icons/code-explainer-video.svg" width="22" alt=""> | [**Code Explainer Video**](https://skill.metacog.co.kr/s/code-explainer-video/)<br>`code-explainer-video` | Render a cinematic chaptered explainer video for any CLI or dev tool — Remotion "Terminal Noir": code that types itself, streaming terminal output, growing dependency graphs, continuous BGM. |
| <img src="assets/icons/sync-shopshorts-higgs.svg" width="22" alt=""> | [**Shopping Shorts Workflow**](https://skill.metacog.co.kr/s/sync-shopshorts-higgs/)<br>`sync-shopshorts-higgs` | Turn a product URL into a Korean-market shopping short — crawl the product, profile the target persona, recommend script × preset, approve the scene map, then generate via Higgsfield. |
| <img src="assets/icons/slack-gif-creator.svg" width="22" alt=""> | [**Slack GIF Creator**](https://skill.metacog.co.kr/s/slack-gif-creator/)<br>`slack-gif-creator` | Build animated GIFs sized for Slack — composable animation primitives plus validators for Slack's size constraints. |

### Research

| | Skill | What it does |
| :-: | --- | --- |
| <img src="assets/icons/research-agent-team.svg" width="22" alt=""> | [**Research Agent Team**](https://skill.metacog.co.kr/s/research-agent-team/)<br>`research-agent-team` | Run an 8-agent research pipeline — Orchestrator, 3 Researchers, 2 Fact-Checkers, Writer, Gatekeeper — applying MECE and the Pyramid Principle to produce a sourced consulting-style report. |

### Sites & Docs

| | Skill | What it does |
| :-: | --- | --- |
| <img src="assets/icons/algolia-docusaurus.svg" width="22" alt=""> | [**Algolia for Docusaurus**](https://skill.metacog.co.kr/s/algolia-docusaurus/)<br>`algolia-docusaurus` | Wire Algolia DocSearch into a Docusaurus v3 site on GitHub Pages — automates every config file, then walks you through the manual Algolia account steps. |
| <img src="assets/icons/docusaurus-english-site.svg" width="22" alt=""> | [**Docusaurus Site Scaffold**](https://skill.metacog.co.kr/s/docusaurus-english-site/)<br>`docusaurus-english-site` | Stand up a Docusaurus documentation site with GitHub Pages deployment, grouped navigation, per-topic sidebars, Korean locale and Mermaid support. |
| <img src="assets/icons/github-sponsors.svg" width="22" alt=""> | [**GitHub Sponsors Button**](https://skill.metacog.co.kr/s/github-sponsors/)<br>`github-sponsors` | Add a GitHub Sponsors funding button to any static site — Hugo, Jekyll, Docusaurus or plain HTML — including the FUNDING.yml wiring. |
| <img src="assets/icons/hextra-kb-builder.svg" width="22" alt=""> | [**Hextra KB Builder**](https://skill.metacog.co.kr/s/hextra-kb-builder/)<br>`hextra-kb-builder` | Initialize a technical knowledge base on Hugo's Hextra theme with Mermaid, LaTeX and search, wired for GitHub Pages deployment. |
| <img src="assets/icons/hextra-roadmap-kb.svg" width="22" alt=""> | [**Hextra Roadmap KB**](https://skill.metacog.co.kr/s/hextra-roadmap-kb/)<br>`hextra-roadmap-kb` | Scaffold a topic learning-roadmap site on Hugo + Hextra — hero home, numbered roadmap docs by category, Labs, Tools, a Blog with RSS and a termbase-backed glossary. |
| <img src="assets/icons/hugo-blog-builder.svg" width="22" alt=""> | [**Hugo Blog Builder**](https://skill.metacog.co.kr/s/hugo-blog-builder/)<br>`hugo-blog-builder` | Build a Hugo blog or docs site with GitHub Actions deployment — PaperMod or Hextra — with every known pitfall (TOML ordering, submodules, go.mod conflicts) handled up front. |
| <img src="assets/icons/lotusdocs-kb-builder.svg" width="22" alt=""> | [**Lotus Docs KB Builder**](https://skill.metacog.co.kr/s/lotusdocs-kb-builder/)<br>`lotusdocs-kb-builder` | Build a documentation or knowledge-base site on Hugo's Lotus Docs theme (installed as a Hugo Module) and deploy it to GitHub Pages, custom domain included. Topic-agnostic. |

<!-- icons:end -->

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
tools/icons.py           the 38 SVG glyphs and the skill -> glyph mapping
tools/build.py           static site generator (standard library only)
site/                    stylesheet and catalog JavaScript
assets/icons/            generated per-skill SVGs — the table above embeds these
.github/workflows/       builds the site + per-skill zips, deploys to GitHub Pages
```

## Building locally

```bash
python3 tools/build.py     # writes _site/
python3 -m http.server 8000 --directory _site
```

No dependencies beyond Python 3.9+.

## Adding a skill

1. Drop the skill directory into `skills/`. It must contain a `SKILL.md` — uppercase,
   exactly — with `name` and `description` frontmatter.
2. Add an entry to `catalog/meta.json` with an English `title`, `summary`, `category` and
   `tags`. Without it the site falls back to the raw frontmatter description.
3. To list a skill you cannot redistribute, skip step 1 and give its meta entry an
   `external_url` instead — it renders as a link-only card with no zip and no detail
   page.
4. Map a glyph in `tools/icons.py` (`SKILL_ICONS`), reusing one of the existing shapes or
   adding a new 24×24 stroke path. Skipping this only costs you a fallback glyph.
5. Run `python3 tools/build.py`, which rewrites `assets/icons/` and the table above, then
   commit those changes alongside the skill.
6. Push to `main`. The workflow rebuilds the catalog and the zip.

Everything between the `<!-- icons:start -->` and `<!-- icons:end -->` markers in this
file is generated — edit `catalog/meta.json` or `tools/icons.py` instead, and rerun the
build.

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
