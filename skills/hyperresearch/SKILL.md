---
name: hyperresearch
description: Set up and run hyperresearch (jordan-gibbs/hyperresearch), a Claude Code harness that installs a /hyperresearch entry skill plus 16 step skills and runs deep research with adversarial review — decompose, width sweep, contradiction graph, depth investigation, synthesis, then 4 parallel critics whose findings are applied as surgical patches rather than a regenerated draft. Use when the user asks to install or configure hyperresearch, pick its search providers or scale gear, start or resume a long research run, or recover one that crashed. Triggers on "hyperresearch", "하이퍼리서치", "적대적 검증 리서치", "16단계 리서치 파이프라인", "deep research pipeline". Not for one-off web lookups — that overhead only pays off on a real research question.
---

# hyperresearch

Upstream: <https://github.com/jordan-gibbs/hyperresearch> (MIT, Python 3.11–3.13).

A research harness, not a library you call. Installing it writes a
`/hyperresearch` entry skill and 16 numbered step skills into the project, and
the pipeline then runs **inside Claude Code** — the entry skill routes, each
step skill loads only when its step runs, and steps spawn subagents.

**So your job here is setup and run management, not driving the pipeline.**
Once `/hyperresearch <query>` is invoked the harness takes over. Do not try to
reimplement the steps by hand, and do not invoke the numbered step skills
directly — they expect state the previous step wrote.

## 1. Check the Python version first

3.14 is not supported and the failure is confusing if you find out late:

```bash
python3 --version   # must be 3.11, 3.12 or 3.13
```

On 3.14, get a supported interpreter before anything else — `pyenv install 3.13`,
`uv venv -p 3.13`, or `py -3.13 -m venv .venv`.

## 2. Install

Per-project, from the project root:

```bash
pip install hyperresearch && hyperresearch install
```

That initialises the vault, injects CLAUDE.md, and installs the Claude Code
hooks and step skills. `/hyperresearch <anything>` then works in that project.

`hyperresearch install --global` instead puts the entry skill in `~/.claude/`
so `/hyperresearch` is reachable from every session anywhere. The cost is ~15
lines in every Claude Code session's system reminder, including unrelated ones.
Default to per-project; offer `--global` only if the user wants it everywhere.

`hyperresearch install --steps-only` exists for the entry skill's own bootstrap.
Don't run it yourself.

**The session must restart** to pick up newly installed skills. Say so — a user
typing `/hyperresearch` in the current session and getting nothing will assume
the install failed.

## 3. Pick a search provider

The fetch path is a real choice and the defaults are not all free:

| Extra | Key needed | Notes |
| --- | --- | --- |
| `crawl4ai` | no | Headless browser fetch, PDF extraction, browser-escalation lane. **The one the pipeline is tuned for.** |
| `parallel` | no | Search only; bulk fetch degrades to per-URL. Good search, not a fetch replacement. |
| `exa` | yes | Neural web search and extraction. |
| `tavily` | yes | Search and extraction built for agents. |

```bash
pip install "hyperresearch[crawl4ai]"
```

Start with `crawl4ai`. Add `parallel` when the user wants better search without
signing up for anything. Only reach for `exa`/`tavily` if the user already has
a key — never sign them up for a paid service to satisfy a default.

Scholarly search (`hpr scholar search`) covers OpenAlex, Crossref, CORE, DOAB,
ClinicalTrials.gov, SEC EDGAR and FRED. Most need no key; `CORE_API_KEY` and
`FRED_API_KEY` do. `hpr scholar sources` reports what is actually wired.

## 4. Agree the tier before starting

This is the step that matters most. Runs are long and spawn many subagents, so
the tier is a real commitment of time and tokens — confirm it, don't assume it:

| Tier | What runs | Typical time |
| --- | --- | --- |
| `light` | steps 1 → 2 → 10 → 15 → 16 | ~30–40 min |
| `full` (default) | all 16 steps + cite-check | ~1.5–2.5 h |
| `dissertation` | 300–450 sources, 4–10 chapters, 25K–80K words | ~4–8 h |

Step 1 auto-classifies `light` vs `full` from the query. `dissertation` is
opt-in only and has to be asked for in the prompt — never add it on your own
initiative.

Gears set the scale within a tier and persist per project:

```bash
hyperresearch profile list          # profiles + current gear
hyperresearch profile use premier   # 100–130 sources, doubled depth (~3–5 h)
hyperresearch profile use full      # back to the 55–80-source baseline
```

Tell the user the expected wall-clock before launching a `full` or heavier run.
A four-hour job started without warning is a failure even if the report is good.

## 5. Run

```
/hyperresearch <the research question>
```

Pass the user's question through as they wrote it — step 1 pins down the
canonical query itself, and upstream's lint blocks a scaffold that doesn't open
with the user's exact prompt. Don't pre-decompose it, and don't pad it with
scope the user didn't ask for.

## 6. When a run dies

Runs are resumable by design; each owns `research/runs/<vault_tag>/` and a
manifest. Never restart a crashed run from scratch before checking:

```bash
hyperresearch run status
hyperresearch run resume -j   # exact next step + the Skill invocation to continue
```

`-j` prints the precise step to resume at. Restarting instead of resuming
throws away hours of fetched sources.

## Why the output doesn't get worse after review

Worth knowing, because it shapes what you should and shouldn't do to the draft:
after synthesis (step 11) nothing regenerates the report. Step 12 spawns four
adversarial critics in parallel — dialectic, depth, width and instruction —
that only write findings JSON; they never touch the draft. Step 14 applies
those findings as surgical Edit hunks, and 14.5 does a second patch pass over
citation bindings. So a late critique can only patch, not roll back.

If you are asked to revise a finished report, patch it the same way. Rewriting
it wholesale discards exactly what the pipeline spent hours protecting.

Commands, the full step table and the vault tooling: `references/cli-reference.md`.
