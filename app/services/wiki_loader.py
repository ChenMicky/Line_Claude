import os
import logging
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)

DEFAULT_WIKI_PATH = "/app/Claude_wiki"


def load_wiki_content(wiki_path: str = None, query: str = "") -> str:
    if wiki_path is None:
        wiki_path = os.getenv("WIKI_PATH", DEFAULT_WIKI_PATH)

    wiki_path = Path(wiki_path)
    logger.info(f"Loading wiki content from: {wiki_path}")

    if not wiki_path.exists() or not wiki_path.is_dir():
        logger.warning(f"Wiki directory does not exist: {wiki_path}")
        return ""

    md_files = list(wiki_path.rglob("*.md"))
    if not md_files:
        logger.info("No .md files found")
        return ""

    # 永遠載入全部 wiki
    wiki_contents = []
    for md_file in sorted(md_files):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                relative_path = md_file.relative_to(wiki_path)
                wiki_contents.append(f"--- File: {relative_path} ---\n{content}\n")
                logger.debug(f"Loaded: {relative_path}")
        except Exception as e:
            logger.error(f"Error reading file {md_file}: {e}")

    combined = "\n".join(wiki_contents)
    logger.info(f"Wiki content loaded: {len(combined)} characters")
    return combined


def get_wiki_files_info(wiki_path: str = None) -> List[Dict[str, str]]:
    if wiki_path is None:
        wiki_path = os.getenv("WIKI_PATH", DEFAULT_WIKI_PATH)

    wiki_path = Path(wiki_path)

    if not wiki_path.exists() or not wiki_path.is_dir():
        return []

    files_info = []
    for md_file in wiki_path.rglob("*.md"):
        try:
            relative_path = md_file.relative_to(wiki_path)
            stat = md_file.stat()
            files_info.append({
                "path": str(relative_path),
                "size": stat.st_size,
                "absolute_path": str(md_file)
            })
        except Exception as e:
            logger.error(f"Error getting info for {md_file}: {e}")

    return files_info