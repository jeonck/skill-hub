# hugo.toml Complete Template

Replace `<USERNAME>`, `<REPO_NAME>`, `<BLOG_TITLE>`, `<BLOG_DESCRIPTION>` before use.

```toml
baseURL = 'https://<USERNAME>.github.io/<REPO_NAME>/'
locale = 'ko-kr'
title = '<BLOG_TITLE>'
theme = 'PaperMod'
paginate = 10

[params]
  env = 'production'
  title = '<BLOG_TITLE>'
  description = '<BLOG_DESCRIPTION>'
  author = '<USERNAME>'
  defaultTheme = 'auto'
  disableThemeToggle = false
  ShowReadingTime = true
  ShowShareButtons = true
  ShowPostNavLinks = true
  ShowBreadCrumbs = true
  ShowCodeCopyButtons = true
  ShowWordCount = true
  ShowRssButtonInSectionTermList = true
  UseHugoToc = true
  disableSpecial1stPost = false
  disableScrollToTop = false
  comments = false
  hidemeta = false
  hideSummary = false
  showtoc = false
  tocopen = false

  [params.homeInfoParams]
    Title = '안녕하세요 👋'
    Content = '<BLOG_DESCRIPTION>'

  [[params.socialIcons]]
    name = 'github'
    url = 'https://github.com/<USERNAME>'

[menu]
  [[menu.main]]
    identifier = 'posts'
    name = 'Posts'
    url = '/posts/'
    weight = 10
  [[menu.main]]
    identifier = 'tags'
    name = 'Tags'
    url = '/tags/'
    weight = 20
  [[menu.main]]
    identifier = 'search'
    name = 'Search'
    url = '/search/'
    weight = 30

[outputs]
  home = ['HTML', 'RSS', 'JSON']
```

## Key Rules

| Key | Rule |
|---|---|
| `locale` | Use `locale`, NOT `languageCode` (deprecated Hugo v0.158.0+) |
| `[[params.socialIcons]]` | Must be array table syntax. Never precede with `[params.socialIcons]` |
| `[outputs]` | Must include `'JSON'` for search to work |
| `baseURL` | Must end with `/` and match the exact GitHub Pages URL |
