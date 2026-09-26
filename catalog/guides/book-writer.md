A **harness**, not one skill — 14 agents and 15 skills that take a topic all the
way to a finished EPUB: research → plan → chapter drafting → editing →
continuity and fact-checking → cover → EPUB build, with review gates between
stages. The hub links it rather than mirroring; use it from a clone.

## Install

Clone it and use it as a project — the `.claude/` directory holds the agents and
skills, so a Claude Code session started inside the clone has the whole harness.

```bash
git clone https://github.com/tobyilee/book-writer.git
cd book-writer && claude
```

The 15 skills can also be pulled into your global skills (they can be referenced
individually, but the orchestrator expects the 14 agents alongside):

```bash
cp -r book-writer/.claude/skills/* ~/.claude/skills/
cp -r book-writer/.claude/agents/* ~/.claude/agents/   # optional, global
```

## Use it

The entry point is **book-writing-orchestrator**:

```
이 주제로 책 써줘 — 대상 독자와 목차는 이렇게…   (or "write a book about …")
```

Pipeline: research (web / paper / community) → book plan → plan review →
chapter writing → editing → style and continuity review → fact-check →
manuscript acceptance → cover design → EPUB build.

## Note on voice

Chapter writing ships a default "Toby-style" voice guide
(`chapter-writing/references/toby-style-guide.md`). Point it at your own voice
sample or tell it the tone you want if you don't want that default.
