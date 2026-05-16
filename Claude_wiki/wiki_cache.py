#!/usr/bin/env python3
"""
Hot Cache for LLM Wiki

A simple in-memory cache that keeps frequently accessed wiki pages
and search results for faster retrieval. Integrates with the LLM Wiki
workflow for queries and ingests.

Usage:
    python wiki_cache.py search <query>       # Search cached pages
    python wiki_cache.py warm                 # Warm cache from index
    python wiki_cache.py stats                # Show cache statistics
    python wiki_cache.py clear                # Clear cache
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import re


class LRUCache:
    """Simple LRU cache with TTL support."""

    def __init__(self, max_size: int = 100, ttl_seconds: int = 300):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: OrderedDict[str, dict] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def _is_expired(self, entry: dict) -> bool:
        """Check if a cache entry has expired."""
        return time.time() - entry['timestamp'] > self.ttl_seconds

    def get(self, key: str) -> Optional[dict]:
        """Retrieve value from cache if present and not expired."""
        if key in self.cache:
            entry = self.cache[key]
            if not self._is_expired(entry):
                self.hits += 1
                # Move to end (most recently used)
                self.cache.move_to_end(key)
                return entry['value']
            else:
                # Expired, remove it
                del self.cache[key]
                self.misses += 1
        else:
            self.misses += 1
        return None

    def put(self, key: str, value: dict) -> None:
        """Add value to cache, evicting LRU if at capacity."""
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
        if len(self.cache) > self.max_size:
            # Pop first item (least recently used)
            self.cache.popitem(last=False)

    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0

    def stats(self) -> dict:
        """Return cache statistics."""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.1%}",
            'ttl_seconds': self.ttl_seconds
        }


class WikiPageCache:
    """Cache for wiki page content and search results."""

    def __init__(self, wiki_dir: str = "wiki"):
        self.wiki_dir = Path(wiki_dir)
        self.page_cache = LRUCache(max_size=50, ttl_seconds=600)  # 10 min TTL for pages
        self.search_cache = LRUCache(max_size=20, ttl_seconds=120)  # 2 min TTL for searches
        self.index_cache = LRUCache(max_size=5, ttl_seconds=300)   # 5 min TTL for index
        self._index = None

    def _make_key(self, *parts: str) -> str:
        """Create a cache key from parts."""
        return hashlib.md5('|'.join(parts).encode()).hexdigest()

    def get_page(self, rel_path: str) -> Optional[dict]:
        """Get a wiki page from cache or disk."""
        cache_key = self._make_key('page', rel_path)
        cached = self.page_cache.get(cache_key)
        if cached:
            return cached

        # Not in cache, load from disk
        page_path = self.wiki_dir / rel_path
        if not page_path.exists():
            return None

        content = page_path.read_text()
        page_data = self._parse_page(content, rel_path)

        self.page_cache.put(cache_key, page_data)
        return page_data

    def _parse_page(self, content: str, rel_path: str) -> dict:
        """Parse a wiki page, extracting frontmatter and body."""
        lines = content.split('\n')
        frontmatter = {}
        body_start = 0

        if lines[0].strip() == '---':
            for i, line in enumerate(lines[1:], start=1):
                if line.strip() == '---':
                    body_start = i + 1
                    break
                if ':' in line:
                    key, val = line.split(':', 1)
                    frontmatter[key.strip()] = val.strip()

        body = '\n'.join(lines[body_start:])

        # Extract first paragraph for preview
        preview = body.split('\n\n')[0][:200] if body else ''

        return {
            'path': rel_path,
            'title': frontmatter.get('title', Path(rel_path).stem.replace('-', ' ').title()),
            'type': frontmatter.get('type', 'page'),
            'tags': frontmatter.get('tags', []),
            'date': frontmatter.get('date', ''),
            'preview': preview,
            'content': body,
            'full_text': content
        }

    def search_pages(self, query: str, limit: int = 10) -> List[dict]:
        """Search wiki pages using cached or fresh search."""
        cache_key = self._make_key('search', query.lower(), str(limit))
        cached = self.search_cache.get(cache_key)
        if cached:
            cached['from_cache'] = True
            return cached['results']

        # Fresh search
        results = []
        query_lower = query.lower()

        for md_file in self.wiki_dir.rglob('*.md'):
            rel_path = md_file.relative_to(self.wiki_dir.parent).as_posix()
            page = self.get_page(md_file.relative_to(self.wiki_dir).as_posix())
            if not page:
                continue

            # Score based on matches in title, tags, and content
            score = 0
            matches = []

            if query_lower in page['title'].lower():
                score += 10
                matches.append('title')

            if any(query_lower in tag.lower() for tag in page.get('tags', [])):
                score += 5
                matches.append('tags')

            if query_lower in page['content'].lower():
                score += 1
                matches.append('content')

            if score > 0:
                results.append({
                    'path': page['path'],
                    'title': page['title'],
                    'type': page['type'],
                    'preview': page['preview'],
                    'score': score,
                    'matches': matches,
                    'date': page['date']
                })

        # Sort by score, then by date
        results.sort(key=lambda x: (-x['score'], x['date']), reverse=True)
        results = results[:limit]

        self.search_cache.put(cache_key, {'results': results, 'from_cache': False})
        return results

    def get_index(self) -> dict:
        """Get the wiki index from cache or disk."""
        cache_key = self._make_key('index')
        cached = self.index_cache.get(cache_key)
        if cached:
            return cached

        index_path = self.wiki_dir / 'index.md'
        if not index_path.exists():
            return {'pages': [], 'stats': {}}

        content = index_path.read_text()
        self.index_cache.put(cache_key, {'content': content, 'parsed': self._parse_index(content)})
        return self.index_cache.get(cache_key)

    def _parse_index(self, content: str) -> dict:
        """Parse index.md for quick lookups."""
        sections = {}
        current_section = None

        for line in content.split('\n'):
            if line.startswith('## '):
                current_section = line[3:].strip()
                sections[current_section] = []
            elif line.startswith('- [[') and current_section:
                sections[current_section].append(line.strip())

        return sections

    def warm_cache(self) -> dict:
        """Preload frequently accessed pages into cache."""
        warmed = []

        # Load overview
        overview = self.get_page('overview.md')
        if overview:
            warmed.append('overview.md')

        # Load index
        self.get_index()
        warmed.append('index.md')

        # Load recent pages from log
        log_path = self.wiki_dir / 'log.md'
        if log_path.exists():
            log_content = log_path.read_text()
            # Find recently modified pages from log
            for line in log_content.split('\n'):
                if 'Created:' in line or 'Updated:' in line:
                    # Extract page names
                    import re
                    pages = re.findall(r'\[\[([^\]]+)\]\]', line)
                    for page in pages:
                        # Try to find the page file
                        for md_file in self.wiki_dir.rglob('*.md'):
                            if page.lower() in md_file.stem.lower():
                                rel = md_file.relative_to(self.wiki_dir).as_posix()
                                self.get_page(rel)
                                if rel not in warmed:
                                    warmed.append(rel)

        return {
            'warmed': warmed,
            'cache_size': len(self.page_cache.cache),
            'timestamp': datetime.now().isoformat()
        }

    def clear_cache(self) -> dict:
        """Clear all caches."""
        self.page_cache.clear()
        self.search_cache.clear()
        self.index_cache.clear()
        return {'cleared': True, 'timestamp': datetime.now().isoformat()}


def main():
    """CLI entry point."""
    wiki_dir = Path(__file__).parent
    cache = WikiPageCache(wiki_dir=str(wiki_dir))

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'search':
        if len(sys.argv) < 3:
            print("Usage: wiki_cache.py search <query>")
            sys.exit(1)
        query = ' '.join(sys.argv[2:])
        results = cache.search_pages(query, limit=10)

        print(f"\n🔍 Search: '{query}'")
        print(f"   Found {len(results)} results\n")

        for i, r in enumerate(results, 1):
            cache_indicator = " ⚡" if r.get('from_cache') else ""
            print(f"{i}. [[{r['title']}]]({r['path']}){cache_indicator}")
            print(f"   Type: {r['type']} | Score: {r['score']} | Matches: {', '.join(r['matches'])}")
            if r['preview']:
                print(f"   {r['preview'][:100]}...")
            print()

    elif command == 'warm':
        print("🌡️  Warming cache...")
        result = cache.warm_cache()
        print(f"   Warmed {len(result['warmed'])} pages")
        print(f"   Cache size: {result['cache_size']}")
        for page in result['warmed']:
            print(f"   ✓ {page}")

    elif command == 'stats':
        print("\n📊 Cache Statistics")
        print("=" * 40)
        print(f"\nPage Cache:")
        for k, v in cache.page_cache.stats().items():
            print(f"  {k:15} {v}")
        print(f"\nSearch Cache:")
        for k, v in cache.search_cache.stats().items():
            print(f"  {k:15} {v}")
        print(f"\nIndex Cache:")
        for k, v in cache.index_cache.stats().items():
            print(f"  {k:15} {v}")
        print()

    elif command == 'clear':
        cache.clear_cache()
        print("✅ Cache cleared")

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
