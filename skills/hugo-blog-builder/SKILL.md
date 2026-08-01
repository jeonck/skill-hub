---
name: hugo-blog-builder
description: This skill should be used when building a Hugo blog or documentation site with GitHub Pages and GitHub Actions deployment. Supports PaperMod theme (blog) and Hextra theme (docs/knowledge-base). Handles all known pitfalls in one shot: TOML key ordering, date timezone, submodule checkout, Hextra go.mod conflict, icon names, and GitHub Pages source configuration.
---

# Hugo Blog Builder

## Overview

Build a Hugo site deployed to GitHub Pages via GitHub Actions — fully automated from local init to live URL.

**Theme selection:**
- **PaperMod** — for personal blogs
- **Hextra** — for documentation sites, knowledge bases, onboarding guides (search, sidebar, TOC built-in)

## Prerequisites Check

Before starting, verify:

```bash
hugo version        # if missing: brew install hugo
gh auth status      # must be logged in
git --version       # must be present
go version 2>/dev/null || echo "Go not installed"   # needed for Hugo modules
```

> **Important:** `hugo env` shows `GOVERSION` — this is Hugo's embedded compiler, NOT the `go` CLI. Always run `go version` separately. If Go is not installed, use the zip-based Hextra install (see below).

---

## PaperMod Theme (Blog)

### Step 1: Initialize Site

```bash
hugo new site . --force
git init
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

### Step 2: Write hugo.toml

See `references/hugo-toml.md` for the complete template.

**Critical rules:**
- Use `locale` not `languageCode` (deprecated since Hugo v0.158.0)
- `[[params.socialIcons]]` array syntax — never precede with `[params.socialIcons]`
- Include `[outputs]` with JSON for search to work
- **All root-level keys BEFORE any `[table]` headers** — see TOML Key Ordering rule below

### Step 3: Create Required Content Files

**Search page** (`content/search/index.md`):
```markdown
---
title: "Search"
layout: "search"
summary: "search"
placeholder: "검색어를 입력하세요"
---
```

**Sample post** (`content/posts/첫번째-포스트.md`) — see Date Timezone Rule below.

### Step 4: GitHub Actions Workflow

Place at `.github/workflows/deploy.yml`. See `references/deploy-workflow.md`.

**Critical:** `actions/checkout` must include `submodules: true`.

---

## Hextra Theme (Docs/Knowledge-Base)

Hextra provides search, collapsible sidebar, TOC, dark mode, Mermaid, and callout shortcodes out of the box.

### Step 1: Initialize Site

```bash
hugo new site . --force
git init
```

### Step 2: Install Hextra (zip method — no Go required)

**Do NOT use `git submodule add` for Hextra.** Hextra's repo contains a `go.mod` file. When Hugo detects `go.mod` in a theme directory, it attempts Hugo module resolution. This silently prevents all theme layouts (shortcodes, templates) from loading — even though the files are physically present.

```bash
# Download and extract as plain directory
curl -L https://github.com/imfing/hextra/archive/refs/heads/main.zip -o /tmp/hextra.zip
cd /tmp && unzip -q hextra.zip
mv hextra-main <PROJECT_ROOT>/themes/hextra

# CRITICAL: remove go.mod to prevent Hugo module resolution failure
rm <PROJECT_ROOT>/themes/hextra/go.mod
```

### Step 3: Write hugo.toml

See `references/hextra-config.md` for the complete template.

**Critical rules:**
- Set `theme = "hextra"` as a root key (before any `[table]` sections)
- Add `[markup.goldmark.renderer] unsafe = true` for Hextra shortcodes that use raw HTML
- **All root-level keys BEFORE any `[table]` headers** — see TOML Key Ordering rule below
- Set `defaultContentLanguage = "ko"` for Korean i18n (search placeholder, TOC, pagination labels)
- **Add a `[[menu.main]]` entry with `params.type = "search"` to show the search box in the navbar** — without this the search files are generated but no trigger button appears:
  ```toml
  [[menu.main]]
    name = "검색"
    weight = 0
    [menu.main.params]
      type = "search"
  ```

### Step 4: Create Content

Hextra uses `content/docs/` for documentation pages with automatic sidebar.

**Home page** (`content/_index.md`) — use Hextra's hero shortcodes:
```markdown
---
title: Site Title
layout: hextra-home
---
{{< hextra/hero-headline >}}Your Headline{{< /hextra/hero-headline >}}
{{< hextra/feature-grid >}}
  {{< hextra/feature-card title="Feature" icon="lightning-bolt" link="docs/section" >}}
{{< /hextra/feature-grid >}}
```

**Icon names:** Hextra uses its own icon set. Check `themes/hextra/data/icons.yaml` for valid names. Common icons:
- `lightning-bolt` (NOT `bolt`)
- `terminal` (NOT `wrench-screwdriver`)
- `academic-cap`, `cog`, `shield-check`, `user-group`, `server`, `database`, `beaker`, `chart-bar`, `globe`

### Step 5: GitHub Actions Workflow

See `references/deploy-workflow.md` Hextra section. Key differences from PaperMod:
- Uses explicit Hugo version install (not `peaceiris/actions-hugo`)
- Does NOT need `submodules: true` when using zip method
- **Must add `actions/cache` for Hugo resources** — Hextra fetches flexsearch from jsDelivr CDN during build via `resources.GetRemote`. Without caching, every build hits the network. Cache key should include the Hugo version and `hugo.toml` hash.

```yaml
- name: Cache Hugo resources
  uses: actions/cache@v4
  with:
    path: /tmp/hugo_cache
    key: hugo-resources-${{ env.HUGO_VERSION }}-${{ hashFiles('hugo.toml') }}
    restore-keys: |
      hugo-resources-${{ env.HUGO_VERSION }}-
      hugo-resources-
```

The themes/ directory must be committed to git.

### Step 6: Commit themes/ directory

Since Hextra is installed as a plain directory (not a submodule), commit it:
```bash
git add hugo.toml .gitignore .github/ content/ themes/hextra/
git commit -m "Initialize site with Hextra theme"
```

---

## Verify Local Build

```bash
hugo --minify
```

Build must complete with zero ERRORs. Then verify pages were generated:
```bash
hugo list all
```

---

## Deploy to GitHub

```bash
gh repo create <REPO_NAME> --public --description "<DESCRIPTION>"
git remote add origin https://github.com/<USERNAME>/<REPO_NAME>.git
git push -u origin main
gh api repos/<USERNAME>/<REPO_NAME>/pages --method POST --field build_type=workflow
```

The final URL: `https://<USERNAME>.github.io/<REPO_NAME>/`

---

## Known Pitfalls (must apply every time)

### TOML Key Ordering — Root Keys Must Come First

**This is the most dangerous pitfall when editing hugo.toml.**

In TOML, once a `[table]` header is opened, ALL subsequent bare key-value pairs belong to that table until the next header. If root-level keys like `title` or `theme` appear after a `[table]` section, they silently become nested keys — Hugo ignores them.

Wrong (theme fails to load, title missing):
```toml
baseURL = "https://..."

[markup]
  [markup.goldmark.renderer]
    unsafe = true
title = "My Site"        # ← parsed as markup.goldmark.renderer.title !
theme = "hextra"         # ← parsed as markup.goldmark.renderer.theme !
```

Correct (all root keys before any table sections):
```toml
baseURL = "https://..."
title = "My Site"
theme = "hextra"

[markup]
  [markup.goldmark.renderer]
    unsafe = true
```

**Rule: When inserting new table sections into an existing hugo.toml, always insert AFTER all root keys.**

### Hextra go.mod Conflict

When Hextra (or any Hugo theme with a `go.mod`) is installed as a git submodule, Hugo attempts Go module resolution for the theme. This causes all theme layouts and shortcodes to silently fail — the error is `template for shortcode "callout" not found` even though the file exists physically.

**Symptom:** `hugo build` reports missing shortcodes despite the theme files being present.

**Root cause:** Hugo detects `go.mod` in `themes/hextra/` and tries to use Go module resolution. Since the `go` CLI may not be in PATH (even if `hugo env` shows a GOVERSION — that's Hugo's embedded compiler), resolution fails and Hugo falls back to an empty theme.

**Fix:** Download as zip and remove `go.mod` from theme directory.

**Diagnostic:**
```bash
# If shortcodes from a theme are not found despite files existing:
ls themes/<THEME>/layouts/_shortcodes/  # files present?
hugo env | grep GOVERSION               # Hugo's embedded Go (not go CLI)
go version 2>/dev/null                  # actual go CLI availability
```

### Date Timezone Rule (PaperMod)

`date: 2026-05-20` is interpreted as UTC midnight. In KST (UTC+9), this is May 19 at 4pm UTC — the post appears in the **future** and is excluded from build output.

**Always use explicit timezone:**
```yaml
date: 2026-05-20T00:00:00+09:00
```

### PaperMod socialIcons Syntax

Wrong (causes `key table already exists` error):
```toml
[params.socialIcons]
  [[params.socialIcons]]
    name = 'github'
```

Correct:
```toml
[[params.socialIcons]]
  name = 'github'
  url = 'https://github.com/<USERNAME>'
```

### Markdown Bold Adjacent to Punctuation

CommonMark (Goldmark) requires that closing `**` is not immediately preceded by punctuation such as `)`, `"`, `'`. When bold text ends with these characters, the bold often fails to render.

**Wrong** (bold may not render):
```markdown
**멱등성(Idempotency)**         ← ) before **
**"quoted phrase"**             ← " before **
**나쁜 예 (count 사용)**        ← ) before **
**OIDC(OpenID Connect)**        ← ) before **
```

**Correct** — move the punctuation outside the bold markers:
```markdown
**멱등성**(Idempotency)         ← ) outside bold
"**quoted phrase**"             ← " outside bold
**나쁜 예** (count 사용)        ← ) outside bold
**OIDC**(OpenID Connect)        ← ) outside bold
```

**Rule summary:**
- `**term(English)**` → `**term**(English)` — closing paren outside
- `**"text"**` → `"**text**"` — quotes outside
- `**설명 (부연)**` → `**설명** (부연)` — trailing parens outside

To verify no violations remain after writing content:
```bash
grep -rn '\*\*[^*]*[)"'"'"']\*\*' content/ --include="*.md"
```

### GitHub Pages Source Must Be Set to "GitHub Actions"

The default source is branch-based. Always run after `git push`:
```bash
gh api repos/<USERNAME>/<REPO_NAME>/pages --method POST --field build_type=workflow
```

### submodules: true in Checkout Action (PaperMod)

Required when using git submodule for the theme. Without it, the theme directory is empty on the Actions runner.

```yaml
- uses: actions/checkout@v4
  with:
    submodules: true
    fetch-depth: 0
```

Not needed for Hextra zip-install (theme files are committed directly).

---

## References

- `references/hugo-toml.md` — PaperMod hugo.toml template
- `references/hextra-config.md` — Hextra hugo.toml template and setup
- `references/deploy-workflow.md` — GitHub Actions workflow (PaperMod + Hextra variants)
