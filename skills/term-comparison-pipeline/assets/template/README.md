# {{SITE_TITLE}} ({{REPO_NAME}})

{{SITE_DESCRIPTION}}

Site: {{BASE_URL}}

## How it works

```
input/term.md (queued terms, one per line, edited from the GitHub web UI)
        │
        ▼  on push to main (input/term.md, content, hugo.toml, assets changed)
pipeline/generate.py
  - reads each line inside the fenced code block as one term/topic
  - terms already published before (exact text match) are skipped —
    tracked in pipeline/state.json
  - for each new term, asks Claude for: an overview, an inline SVG diagram,
    a comparison table, key differences, and "when to use each"
  - writes content/posts/YYYY-MM-DD-....md, one post per term
        │
        ▼  commit & push
Hugo build → GitHub Pages deploy
```

This pipeline is **on-demand only** — there is no daily cron and no fallback
content. If `input/term.md` has no terms queued, the run simply does nothing.

## Requesting a comparison

1. Open [`input/term.md`](input/term.md) on GitHub.
2. Click the pencil (✏️) icon to edit. (Or use the "{{INPUT_BUTTON_LABEL}}" link
   in the site header, which jumps straight to this edit page.)
3. Inside the fenced code block (` ``` `), add a line for the term or topic,
   e.g. `REST vs GraphQL`. Multiple lines queue multiple posts.
4. Commit the change ("Commit changes" button, top right). No local git
   needed.
5. The workflow runs automatically on that commit and publishes the new
   post(s) within a few minutes (real generation calls typically take
   3-5 minutes — a full SVG diagram + table response is output-token-heavy).

Terms that have already been published stay safe to leave in the file — they
are skipped by exact-text match, so they won't be re-published.

To run it manually instead of waiting on the push trigger: GitHub repo →
Actions tab → "{{WORKFLOW_NAME}}" → "Run workflow".

## One-time setup (manual — a human must do this)

The generation step uses the Claude Code CLI. To authenticate it in GitHub
Actions, register an OAuth token issued from a Claude subscription account as
a repository secret. This requires an interactive browser login, so it can't
be done by an agent.

```bash
claude setup-token
```

Paste the code shown in your terminal into the browser and log in. **After**
that, the terminal prints a token starting with `sk-ant-oat01-...` — that
final printed token is what goes in the secret (not the browser login code).

```bash
gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo {{GITHUB_USER}}/{{REPO_NAME}}
# paste the token above
```

After registering the secret, run the workflow once manually
(`workflow_dispatch`) to confirm it works end to end.

## Repository layout

| Path | Role |
|---|---|
| `input/term.md` | Queued terms/topics — one per line (edited via GitHub web UI) |
| `pipeline/generate.py` | Generates content per term → writes Hugo posts. Comparison-domain settings are in the "비교 도메인 설정" block at the top of the file |
| `pipeline/state.json` | Hashes of already-published terms (dedup) |
| `content/posts/` | Generated posts |
| `.github/workflows/deploy.yml` | Push/manual-triggered generate + deploy workflow (no schedule) |
| `themes/PaperMod` | Hugo theme (git submodule) |
| `assets/css/extended/cards.css` | Card-grid list layout + PaperMod spacing fix |
| `assets/css/extended/compare.css` | Diagram design-system variables (`--compare-a`/`--compare-b`), themed card wrapper, and the responsive table fix |
| `static/CNAME` | Custom domain (if configured) |

## Testing locally

```bash
hugo server -D                           # http://localhost:1313/
python3 pipeline/generate.py --dry-run   # print the generated result, write nothing
```

Locally, a logged-in `claude` CLI session is used automatically
(`JUDGE_BACKEND=claude-code`); otherwise set `ANTHROPIC_API_KEY` to run with
`JUDGE_BACKEND=api`.
