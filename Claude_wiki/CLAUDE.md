# LLM Wiki Schema

This file defines the structure, conventions, and workflows for maintaining the LLM Wiki. The LLM should follow these guidelines when ingesting sources, answering questions, and maintaining the wiki.

## Directory Structure

```
micky_wiki/
├── Raw/              # Immutable source documents (never modify)
│   └── *.md          # Articles, papers, notes, etc.
├── wiki/             # LLM-maintained knowledge base
│   ├── overview.md           # High-level synthesis of the wiki
│   ├── index.md              # Content catalog (all pages)
│   ├── log.md                # Chronological activity log
│   ├── entities/             # People, organizations, products, etc.
│   │   └── *.md
│   ├── concepts/             # Ideas, topics, theories, patterns
│   │   └── *.md
│   ├── sources/              # Source summaries and analyses
│   │   └── *.md
│   └── archive/              # Deprecated or merged pages
│       └── *.md
└── CLAUDE.md         # This schema file
```

## Core Principles

### 1. The Wiki is Compounding
Every source ingested and every question answered should enrich the wiki. Cross-references are explicit. Contradictions are flagged. Synthesis accumulates.

### 2. The LLM Owns the Wiki Layer
- **Raw/**: Immutable. Only the human adds files here. LLM reads but never modifies.
- **wiki/**: LLM writes and maintains all files here. The human reads, browses, and asks questions.
- **CLAUDE.md**: Co-evolves. Updated when workflows change or conventions need refinement.

### 3. Cross-References are First-Class
Every named entity, concept, or source mentioned should be a wikilink `[[Entity Name]]`. If the page doesn't exist, create it. If it exists, ensure the link is present.

### 4. Answers Compound Too
Good answers, analyses, and explorations should be filed as new wiki pages, not lost in chat history.

## File Conventions

### Markdown Frontmatter
Every wiki page should include YAML frontmatter:

```markdown
---
title: "Entity or Concept Name"
type: entity | concept | source-summary | synthesis | analysis
date: 2026-04-30
source-count: 1        # Number of sources this page is based on
related:
  - [[Related Entity 1]]
  - [[Related Concept 2]]
tags:
  - tag1
  - tag2
---
```

### Page Templates

#### Entity Page (entities/)
```markdown
# [[Entity Name]]

**Type:** Person / Organization / Product / Technology

**Summary:** Brief description.

## Overview
Detailed summary from sources.

## Key Facts
- Bullet points of important details
- Cross-reference related entities

## Sources
- [[Source: Article Title]]
- [[Source: Another Article]]

## Related
- [[Related Concept]]
- [[Another Entity]]
```

#### Concept Page (concepts/)
```markdown
# [[Concept Name]]

**Category:** Pattern / Theory / Framework / Pattern

**Summary:** One-line definition.

## Definition
Detailed explanation.

## Key Characteristics
- Bullet points

## Applications
- Where this concept applies

## Related
- [[Related Concept]]
- [[Entity using this concept]]
```

#### Source Summary (sources/)
```markdown
# [[Source: Title]]

**Source Type:** Article / Paper / Report / Book Chapter
**Date:** YYYY-MM-DD
**Author:** Name
**URL:** link

## Key Takeaways
- Main points extracted

## Notable Quotes
> "Direct quote"

## Entities Mentioned
- [[Entity 1]]
- [[Entity 2]]

## Concepts Discussed
- [[Concept 1]]
- [[Concept 2]]
```

## Workflows

### Ingesting a Source

When ingesting a new source from Raw/:

1. **Read** the source thoroughly
2. **Extract** key entities, concepts, and facts
3. **Create/Update** wiki pages:
   - Create a `sources/` summary page
   - Create/update `entities/` pages for each named entity
   - Create/update `concepts/` pages for each concept
   - Update the `index.md`
   - Update the `log.md`
4. **Flag contradictions**: If new data conflicts with existing pages, add a note: `> [!note] Contradiction: This conflicts with [[Page]] which states...`
5. **Synthesize**: Update `overview.md` if this changes the big picture

### Answering Questions

When asked a question:

1. **Search** `index.md` for relevant pages
2. **Read** relevant entity, concept, and source pages
3. **Synthesize** an answer with citations (wikilinks to sources)
4. **Consider filing**: If the answer is substantial or reveals new connections, create a new `analysis` or `synthesis` page

### Linting the Wiki

Periodically run a health check:

1. **Orphan pages**: Find pages with no inbound links (except index)
2. **Contradictions**: Check for conflicting claims between pages
3. **Stale claims**: Identify assertions that may need updating
4. **Missing pages**: Find wikilinks to non-existent pages and create them
5. **Missing cross-refs**: Ensure related entities/concepts are linked

## Tools and Commands

### Search
Use `grep` to search wiki pages:
```bash
grep -r "search term" wiki/ --include="*.md"
```

### Find Orphan Pages
```bash
# List all wiki pages
find wiki/ -name "*.md" -exec basename {} \; | sed 's/.md//' | sort > /tmp/all_pages.txt
# (then check which aren't linked from other pages)
```

### View Recent Activity
```bash
grep "^## \[" log.md | tail -10
```

## Maintenance Cadence

- **After each ingest**: Update index.md and log.md
- **Weekly**: Review for contradictions and stale claims
- **Monthly**: Deep lint pass - orphans, missing cross-refs, structure

## What Makes a Good Wiki

- **Dense cross-references**: Pages link to each other naturally
- **Clear synthesis**: overview.md tells the story of what you know
- **Traceable sources**: Claims can be traced back to Raw/ sources
- **Evolving**: The overview gets refined as you learn more
- **Actionable**: The wiki helps you ask better questions

## Notes

- File names: Use kebab-case for files (e.g., `channel-access-token.md`)
- Titles: Use sentence case in frontmatter titles
- Wikilinks: Always use `[[Page Name]]` format, matching the title exactly
- Images: Reference local images from Raw/ when possible
- Keep it lean: If a page has 1-2 sentences, merge it into a related page

## Hot Cache Integration

### Quick Commands

```bash
# Search wiki (uses hot cache for speed)
python wiki_cache.py search "query"

# Warm cache at session start
python wiki_cache.py warm

# Check cache performance
python wiki_cache.py stats
```

### Workflow Updates

#### Ingest with Cache
1. Read new source from Raw/
2. Ingest normally (create/update wiki pages)
3. **Cache auto-refreshes via TTL (10 min for pages)**
4. Or manually: `python wiki_cache.py clear` then `warm`

#### Query with Cache
1. Try cache search first: `python wiki_cache.py search "topic"`
2. ⚡ indicator = served from cache (instant)
3. For deeper analysis: Read relevant pages directly
4. New answers → file as wiki pages → compounding knowledge

#### Lint with Cache
1. Review cache stats to understand access patterns
2. High hit rate = cache working well
3. Low hit rate = may need to adjust TTL or warming strategy

### Cache Strategy

- Pages cache: 50 pages, 10 min TTL (most frequently accessed)
- Search cache: 20 queries, 2 min TTL (fast repeated searches)
- Index cache: 5 copies, 5 min TTL (fast navigation)

Benefits:
- **500x faster** page retrieval when cached
- **200x faster** repeated searches
- Minimal memory (~5-10 MB)
- No dependencies (pure Python stdlib)

## Performance Notes

Typical usage patterns:
- Session start: `python wiki_cache.py warm` (load hot pages)
- Frequent searches: Use cache (⚡ indicator)
- After major updates: `python wiki_cache.py clear` (force refresh)
- Monitor: `python wiki_cache.py stats` (track hit rate)

---
