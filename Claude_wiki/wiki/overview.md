---
title: "LLM Wiki Overview"
type: synthesis
date: 2026-04-30
source-count: 1
related:
  - [[Channel Access Token]]
  - [[LINE Platform]]
tags:
  - llm-wiki
  - knowledge-base
  - personal-wiki
---

# LLM Wiki Overview

## What This Is

This is a personal knowledge base built using the **LLM Wiki pattern**: a persistent, compounding artifact maintained by an LLM that sits between raw sources and your questions. Instead of retrieving from documents at query time (RAG), the LLM incrementally builds and maintains a structured, interlinked collection of markdown files that accumulates value with every source you add.

## The Core Pattern

### Three Layers

1. **Raw Sources** (`Raw/`) - Immutable documents: articles, papers, notes. The LLM reads but never modifies.

2. **The Wiki** (`wiki/`) - LLM-generated markdown files: summaries, entity pages, concept pages, analyses. The LLM owns this entirely.

3. **The Schema** (`CLAUDE.md`) - Conventions and workflows that make the LLM a disciplined maintainer.

### Key Difference from RAG

In traditional RAG systems, the LLM rediscovers knowledge from scratch on every question. Here, knowledge is **compiled once and kept current**. Cross-references are explicit. Contradictions are flagged. The synthesis reflects everything you've read.

### What Gets Maintained

- **Entity pages** (people, organizations, products, technologies)
- **Concept pages** (ideas, patterns, frameworks, theories)
- **Source summaries** (analyses of articles, papers, reports)
- **Synthesis pages** (big-picture overviews, comparisons, timelines)
- **Index** (content catalog for navigation)
- **Log** (chronological record of activity)

## Current State

### Sources Ingested

- 1 source in `Raw/`: LINE Channel Access Token documentation

### Wiki Pages

- 1 synthesis page (this overview)
- Core infrastructure: CLAUDE.md schema, index.md, log.md

### Key Concepts Explored

- [[Channel access token]] - Authentication mechanism for LINE Platform
- Token types and validity periods
- Security considerations for token management

## How to Use This Wiki

### As a Human

1. **Curate sources** - Add articles, papers, notes to `Raw/`
2. **Ask questions** - Direct the LLM to explore, compare, analyze
3. **Review updates** - Browse changes in Obsidian, check the graph view
4. **Guide synthesis** - Emphasize what matters to you

### As an LLM

1. **Ingest** - Read new sources, extract key entities and concepts
2. **Create/update pages** - Build entity pages, concept pages, source summaries
3. **Maintain cross-references** - Ensure wikilinks connect related pages
4. **Flag contradictions** - Note when new data conflicts with existing claims
5. **Update index and log** - Keep navigation and history current
6. **Synthesize** - Refine overview.md as the big picture evolves

## Future Directions

### Potential Expansions

- **More source types**: Papers, books, meeting notes, Slack threads, transcripts
- **Deeper analysis**: Timelines, comparison matrices, argument maps
- **Visualizations**: Graph views of concept relationships, timeline charts
- **Automation**: CLI tools for search, linting, and health checks
- **Integration**: APIs to query the wiki, generate reports, create presentations

### Workflows to Explore

- Batch ingestion with light supervision
- Scheduled linting passes
- Automated contradiction detection
- Web search to fill knowledge gaps
- Export to different formats (slides, docs, presentations)

## Why This Works

**The maintenance burden is near zero for the LLM.** It doesn't get bored updating cross-references. It remembers to check contradictions. It can touch 15 files in one pass. The wiki stays maintained because the cost of maintenance is negligible.

**Your role is higher-value:** Curate sources, ask good questions, think about synthesis, direct the analysis.

The wiki becomes a **thinking partner** - not just a repository, but an accumulated understanding that gets richer with every source and every question.

## Quick Start

### Next Actions

1. Review [[Channel access token]] page
2. Add more sources to `Raw/` to expand the knowledge base
3. Ask questions to explore connections and generate analyses
4. Review the [[Index]] and [[Log]] to see wiki evolution

### Questions to Explore

- How do different token types impact security vs. usability?
- What are common patterns across authentication systems?
- How does LINE's approach compare to other platforms?
- What security lessons apply beyond this specific implementation?

---

*Last updated: 2026-04-30*
