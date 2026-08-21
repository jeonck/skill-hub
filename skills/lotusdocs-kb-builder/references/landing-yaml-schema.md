# `data/landing.yaml` schema reference

Lotus Docs renders the homepage (`layouts/index.html`) purely from
`data/landing.yaml` — no `content/_index.md` is required. Each top-level key
is a "block"; blocks render in ascending `weight` order. Every block needs
`enable`, `weight`, and `template` at minimum.

Confirmed against `colinwilson/lotusdocs` (release branch) partials in
`layouts/partials/landing/`: `hero.html`, `feature_grid.html`,
`image_text.html`, `image_compare.html`.

## `hero`

```yaml
hero:
  enable: true
  weight: 10
  template: hero

  # optional — omit the whole `backgroundImage` block if you have no hero image assets
  backgroundImage:
    path: "images/templates/hero"
    filename:
      desktop: "gradient-desktop.webp"
      mobile: "gradient-mobile.webp"

  # optional
  badge:
    text: "v0.1.0"
    color: primary   # primary, secondary, success, danger, warning, info, light, dark
    pill: false
    soft: true

  # optional — a logo image instead of/alongside the plain title text
  titleLogo:
    path: "images/logos"
    filename: "title_logo.png"
    alt: "Logo"
    height: 80px

  title: "Site Title"
  subtitle: Supports **inline markdown bold** in this string.

  # optional — a screenshot/illustration next to the hero copy
  image:
    path: "images"
    filename: "screenshot.png"
    alt: "Screenshot"
    boxShadow: true
    rounded: true

  # optional
  ctaButton:
    icon: rocket_launch          # Material Symbols ligature name
    btnText: "Get Started"
    url: "/docs/"
  cta2Button:
    icon: hub
    btnText: "View on GitHub"
    url: "https://github.com/OWNER/REPO"

  info: "**Open Source** MIT Licensed."   # optional small print under the buttons
```

`image`, `backgroundImage`, and `titleLogo` are all independently optional —
a text-only hero (title + subtitle + buttons, no images) works fine and is
what the `assets/site-template/data/landing.yaml.template` in this skill
uses, since most new sites don't have custom illustration assets yet.

## `featureGrid`

The main "N categories" grid — usually one card per top-level docs category.

```yaml
featureGrid:
  enable: true
  weight: 20
  template: feature grid

  title: "Section title"
  subtitle: "Section subtitle"

  items:
    - title: "Category Name"
      icon: lock              # Material Symbols ligature name — see pitfalls.md #7
      description: "One or two sentence description."
      ctaLink:
        text: browse
        url: /docs/category-slug/
    # ... one entry per category
```

## `imageText` (optional)

A two-column image + text + bullet-list block. Needs a real image asset
under the configured `assets` directory — skip this block entirely if none
exists yet.

```yaml
imageText:
  enable: true
  weight: 25
  template: image text

  title: "Section title"
  subtitle: "Section subtitle"

  list:
    - text: "Bullet point"
      icon: speed            # Material Symbols ligature name

  image:
    path: "images/templates/single"
    filename: "illustration.svg"
    alt: "Illustration"

  imgOrder:
    desktop: 2   # 1 = image left, 2 = image right
    mobile: 1

  ctaButton:
    text: "Learn more"
    url: "/docs/"
```

## `imageCompare` (optional)

A before/after image slider (e.g. light/dark mode, theme comparison). Needs
two real images per item. Skip unless the site actually has comparison
screenshots to show.

```yaml
imageCompare:
  enable: true
  weight: 30
  template: image compare

  title: "Section title"
  subtitle: "Section subtitle"

  items:
    - title: "Dark Mode"
      config:
        startingPoint: 50
        addCircle: true
        showLabels: true
        labelOptions:
          before: "Dark"
          after: "Light"
      imagePath: "images/screenshots"
      imageBefore: "dark.webp"
      imageAfter: "light.webp"
```

## Minimal viable homepage

For a new site with no custom image assets yet, `hero` (text-only) +
`featureGrid` is enough — that's what
`assets/site-template/data/landing.yaml.template` provides. Add
`imageText`/`imageCompare` later once real screenshots or illustrations
exist.
