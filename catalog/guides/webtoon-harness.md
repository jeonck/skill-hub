This is a **harness**, not a single skill — 27 agents plus 6 skills that
together take a webtoon episode from trend research to a finished vertical-scroll
viewer. The hub links it rather than mirroring it; use it from a clone.

## Install

Clone it and use it as a project. The `.claude/` directory holds the agents and
skills, so any Claude Code session started inside the clone picks them up.

```bash
git clone https://github.com/jeonck/webtoon-harness.git
cd webtoon-harness && claude
```

To pull just the six skills into your global skills instead (they can be
referenced individually, but the orchestrator expects the 27 agents alongside):

```bash
cp -r webtoon-harness/.claude/skills/* ~/.claude/skills/
cp -r webtoon-harness/.claude/agents/* ~/.claude/agents/   # optional, global
```

## Use it

The entry point is **webtoon-orchestrator**. Describe the episode and it drives
the pipeline across the five stages, dispatching the agent team per stage:

```
웹툰 한 회차 만들어줘 — 로맨스 판타지, 회귀물
```

Pipeline: trend research → scenario → panel breakdown → panel render →
assembly (a vertical-scroll HTML viewer), with a quality-review agent gating
each stage.

## Skills in the harness

`webtoon-orchestrator` (entry) · `webtoon-trend-research` · `webtoon-scenario`
· `webtoon-panel-breakdown` · `webtoon-panel-render` · `webtoon-assembly`.
Each can be invoked on its own, but they are designed to run as one flow.
