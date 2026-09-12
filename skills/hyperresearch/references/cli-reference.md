# CLI reference

Two entry points, identical: `hyperresearch` and the short `hpr`.

## The 16-step pipeline

The entry skill is a thin router: it pins the canonical query, then invokes one
step skill per phase through Claude Code's `Skill` tool, so each step's
procedure enters context only when that step runs. That is what keeps a long
pipeline from dropping steps as context degrades.

| # | Step | What it does | Tiers |
| --- | --- | --- | --- |
| 1 | Decompose | Canonical query → atomic items, coverage matrix, tier classification | all |
| 1.5 | Chapter partition | Group items into 4–10 chapters; steps 2–10 then loop per chapter | dissertation |
| 2 | Width sweep | Multi-perspective search plan + parallel fetcher waves | all |
| 3 | Contradiction graph | Pair contradictions across the corpus into ranked clusters | full |
| 4 | Loci analysis | Two parallel loci-analysts → scored loci with source budgets | full |
| 5 | Depth investigation | K parallel depth-investigators → interim notes with committed positions | full |
| 6 | Cross-locus reconcile | Reconcile committed positions → `comparisons.md` | full |
| 7 | Source tensions | Extract expert disagreements → `source-tensions.json` | full |
| 8 | Corpus critic | "What source would overturn this?" + targeted gap-fill fetch | full |
| 9 | Evidence digest | Top claims + verbatim quotes → `evidence-digest.md` | full |
| 10 | Triple draft | Per-angle curation + 3 parallel draft sub-orchestrators (light: single draft) | all |
| 11 | Synthesize | Plan, outline, spawn synthesizer → `final_report.md` | full |
| 12 | Critics | 4 adversarial critics in parallel → findings JSONs | full |
| 13 | Gap-fetch | Targeted fetch wave for critic-identified vault gaps | full |
| 14 | Patcher | Surgical Edit hunks applied to the draft (tool-locked Read+Edit) | full |
| 14.5 | Cite-check | Verify citation-sentence bindings, skeptical spot-check, second patch pass | full |
| 15 | Polish | Hygiene and filler pass (tool-locked Read+Edit subagent) | all |
| 16 | Readability audit | Recommender writes JSON suggestions; orchestrator applies selectively | all |

### The four critics (step 12)

Each writes `research/runs/<vault_tag>/critic-findings-<name>.json` and never
edits the draft:

- **dialectic** — counter-evidence the draft missed or straw-manned
- **depth** — shallow spots where interim notes could add substance
- **width** — corpus clusters the draft ignores despite having evidence
- **instruction** — atomic items from the decomposition that the draft missed,
  under-covered, reordered or reformatted

Upstream's note on the last one: don't skip the instruction critic. It is the
only one measuring prompt adherence, the dimension with the widest variance. A
partial critic set still proceeds, but log the absence — the patch pass is less
robust without full coverage.

The whole of step 12 is skipped at `light` tier, which jumps from 10 to 15.

## Setup and lifecycle

| Command | Purpose |
| --- | --- |
| `hyperresearch install [PATH]` | Vault init + CLAUDE.md injection + Claude Code hooks + step skills |
| `hyperresearch install --global` | Entry skill and agents into `~/.claude/`, so `/hyperresearch` works everywhere |
| `hyperresearch install --profile <gear>` | Render the step prompts from a specific gear |
| `hyperresearch setup` | Guided configuration |
| `hyperresearch init` | Initialise a vault only |
| `hyperresearch status` | Vault status |
| `hyperresearch config …` | Read and write configuration |
| `hyperresearch profile list \| use <gear>` | Inspect and switch the scale gear |

`--steps-only` is used internally by the entry skill's bootstrap; users do not
normally invoke it.

## Runs

| Command | Purpose |
| --- | --- |
| `hyperresearch run status` | Where the current run is |
| `hyperresearch run resume -j` | Exact next step plus the Skill invocation to continue |
| `hyperresearch run init` | Start a run workspace |
| `hyperresearch archive-run` | Archive a finished run |
| `hyperresearch vault-tag` | Manage the run's vault tag |

Each run owns an isolated `research/runs/<vault_tag>/` and a manifest, so
concurrent runs do not collide and a crash resumes at the exact failed step.

## Sources and fetching

| Command | Purpose |
| --- | --- |
| `hyperresearch search <query>` | Search the vault |
| `hyperresearch fetch <url>` | Fetch one URL into the vault |
| `hyperresearch fetch-batch` | Bulk fetch |
| `hyperresearch research` | Research helper |
| `hyperresearch sources …` | Fetched web sources |
| `hyperresearch escalation …` | Browser-lane queue for blocked fetches |
| `hyperresearch assets …` | Downloaded images, screenshots, media |
| `hyperresearch claims …` | Fetcher-extracted claims: ingest and query |
| `hyperresearch citecheck …` | Citation-sentence binding verification |

### Scholarly search

```bash
hpr scholar search "Byzantine iconoclasm" -j            # every available source, merged
hpr scholar search "GLP-1 cardiovascular outcomes" --scope papers -j
hpr scholar search "credit default swaps" -s edgar -s fred -j
hpr scholar sources                                      # what is wired, what each covers
```

One query hits OpenAlex, Crossref, CORE, DOAB, ClinicalTrials.gov, SEC EDGAR
and FRED through one client layer, deduplicated by DOI and title, each result
tagged by kind so the pipeline knows what it has. Keys: `CORE_API_KEY`,
`FRED_API_KEY` (the latter is never written to the cache).

RePEc is listed by `scholar sources` but has no search API upstream — the tool
says so rather than failing silently, and points at OpenAlex and Crossref.

## Vault

| Command | Purpose |
| --- | --- |
| `hyperresearch note …` | Note CRUD |
| `hyperresearch graph …` | Knowledge graph and link analysis |
| `hyperresearch link …` | Auto-discover and insert wiki-links |
| `hyperresearch index …` | Auto-generated index pages |
| `hyperresearch topic …` | Topic hierarchy |
| `hyperresearch tag …` / `tags` | Tag management |
| `hyperresearch lint …` | Health-check the vault |
| `hyperresearch dedup` | Deduplicate |
| `hyperresearch repair` | Repair a damaged vault |
| `hyperresearch batch …` | Bulk operations |
| `hyperresearch template …` | Note templates |
| `hyperresearch embed …` | Semantic-search embeddings |
| `hyperresearch git …` | Git integration |
| `hyperresearch import` | Import into the vault |
| `hyperresearch sync` | Sync |
| `hyperresearch watch` | Watch mode |

Export:

```bash
hyperresearch export json -o out.json    # every note as structured JSON
hyperresearch export vault <dir>         # a filtered subset to another directory
```

## MCP server

```bash
pip install "hyperresearch[mcp]"
hyperresearch mcp        # stdio
```

Lets Claude Desktop, Cursor or any MCP client work the same vault. Thirteen
tools: `search_notes`, `read_note`, `read_many`, `list_notes`, `get_backlinks`,
`get_hubs`, `vault_status`, `lint_vault`, `check_source`, `list_sources`,
`fetch_url`, `create_note`, `update_note`.

`hyperresearch serve` runs the web UI instead.
