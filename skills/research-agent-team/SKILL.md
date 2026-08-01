---
name: research-agent-team
description: This skill should be used when the user requests deep research on a topic, asks for a structured analysis report, or wants comprehensive investigation with fact-checking. Triggers when researching companies, industries, markets, or technologies; creating business intelligence reports; performing competitive analysis; verifying statistics with credible sources; or producing consulting-style reports. Applies MECE, Logical Thinking, and Pyramid Principle frameworks through an 8-agent virtual team pipeline: Orchestrator → 3 Researchers → 2 Fact-Checkers → Writer → Gatekeeper. Outputs a structured Markdown report with verified sources.
---

# 8-Agent Research Team

## Overview

Simulate an 8-member specialist research team to produce deep, fact-checked, structured Markdown research reports. The pipeline runs in 5 sequential phases: scope framing → parallel research → fact verification → report writing → quality gate. Load `references/agent-personas.md` for detailed agent personas, thinking frameworks, and source credibility rubrics.

## Pipeline

### PHASE 0 — Orchestrator: Frame the Problem

Perform MECE decomposition of the research topic:
- Define 3–5 core questions the report must answer
- Assign each to the correct research axis (Market / Finance / Technology)
- Set credibility standards: prefer primary sources (filings, official stats, company IR) over secondary

Output a structured brief with 3 axes and core questions, then announce:
> "PHASE 0 완료 — 리서처 3명 병렬 조사 시작"

### PHASE 1 — 3 Researchers: Parallel Investigation

Run three researchers in sequence. Each uses WebSearch for real-time data, records every source URL and publication date, and flags uncertain statistics as `[요확인]`.

**Researcher A — Market/Industry**
- Market size (TAM, CAGR, forecasts), competitive landscape, demand drivers, regulatory environment
- Minimum 2 WebSearch queries

**Researcher B — Company/Finance**
- Revenue, growth rates, margins, key partnerships, hyperscaler relationships
- Prefer: earnings calls, SEC filings, official IR pages
- Minimum 2 WebSearch queries

**Researcher C — Technology/Trends**
- Core tech stack, product roadmap, emerging standards, R&D investments
- Minimum 2 WebSearch queries

After all three complete, announce:
> "PHASE 1 완료 — 팩트체커 교차검증 시작"

### PHASE 2 — 2 Fact-Checkers: Cross-Verification

Run independently after PHASE 1:

**Fact-Checker A — Number Verification**
- Verify every key statistic against a primary or authoritative secondary source
- Unverifiable items: mark `[미검증]` with a note on the discrepancy

**Fact-Checker B — Source Credibility**
- Rate each source: ✅ Primary | ✅ Tier-1 Research | ⚠️ Secondary
- Flag any source that cannot be traced to a credible origin

See `references/agent-personas.md` for the full source credibility rubric.

Announce:
> "PHASE 2 완료 — 구성작가 보고서 작성 시작"

### PHASE 3 — Writer: Compose the Report

Apply the Pyramid Principle — conclusion first, then supporting evidence.

**Mandatory report structure (Markdown):**
1. **Executive Summary** — 3–5 bullet key conclusions with "so what"
2. **Section 1: Market/Industry** — Researcher A findings
3. **Section 2: Company/Finance** — Researcher B findings
4. **Section 3: Technology/Trends** — Researcher C findings
5. **Section 4: Investment/Strategy** — synthesized (include if topic warrants)
6. **Risk Factors** — key risks with mitigating context
7. **Source Table** — numbered, with credibility rating per row

**Formatting rules:**
- `##` for sections, `###` for subsections
- Tables for all multi-item comparisons (stocks, metrics, timelines)
- All `[미검증]` items clearly marked inline
- Investment disclaimer at the end if financial content is present

Announce:
> "PHASE 3 완료 — 게이트키퍼 최종 승인 시작"

### PHASE 4 — Gatekeeper: Quality Gate

Run both checklists before releasing the final report:

**Logical Thinking Check**
- [ ] Every conclusion is backed by at least one verified source
- [ ] No logical leap between evidence and conclusion
- [ ] Conflicting data points are acknowledged and reconciled

**MECE Check**
- [ ] All 3 axes (Market / Finance / Technology) are covered
- [ ] No major overlap between sections
- [ ] All PHASE 0 core questions are answered

If any item fails: return to the relevant phase, fix, then re-run the checklist. Output the final report only after all items pass.

## Output Format

- **Language:** Match the user's language (Korean if user writes in Korean)
- **Format:** Markdown — headers, tables, bullet points
- **Source table:** Always included at the end
- **Length:** Proportional to topic complexity — thorough over brief

## Resources

- `references/agent-personas.md` — Detailed personas, MECE / Logical Thinking / Pyramid Principle frameworks, source credibility rubric
