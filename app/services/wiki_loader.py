import os
import logging
from pathlib import Path
from typing import List, Dict

logger = logging.getLogger(__name__)

DEFAULT_WIKI_PATH = "./Claude_wiki"


def load_wiki_content(wiki_path: str = None) -> str:
    """
    Load all Obsidian wiki markdown files from the specified path.

    Args:
        wiki_path: Path to the Claude_wiki directory. If None, uses WIKI_PATH env var or default.

    Returns:
        Combined content of all .md files as a single string
    """
    # Get wiki path from parameter, environment variable, or default
    if wiki_path is None:
        wiki_path = os.getenv("WIKI_PATH", DEFAULT_WIKI_PATH)

    wiki_path = Path(wiki_path)
    logger.info(f"Loading wiki content from: {wiki_path}")

    # Check if directory exists
    if not wiki_path.exists():
        logger.warning(f"Wiki directory does not exist: {wiki_path}")
        return ""

    if not wiki_path.is_dir():
        logger.warning(f"Wiki path is not a directory: {wiki_path}")
        return ""

    # Recursively scan for .md files
    md_files = list(wiki_path.rglob("*.md"))

    if not md_files:
        logger.info(f"No .md files found in {wiki_path}")
        return ""

    logger.info(f"Found {len(md_files)} .md files")

    # Load and combine all markdown files
    wiki_contents = []
    for md_file in md_files:
        try:
            relative_path = md_file.relative_to(wiki_path)
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                wiki_contents.append(f"--- File: {relative_path} ---\n{content}\n")
                logger.debug(f"Loaded: {relative_path}")
        except Exception as e:
            logger.error(f"Error reading file {md_file}: {e}")

    combined_content = "\n".join(wiki_contents)
    logger.info(f"Total wiki content loaded: {len(combined_content)} characters")

    return combined_content


def get_wiki_files_info(wiki_path: str = None) -> List[Dict[str, str]]:
    """
    Get information about all wiki files without loading content.

    Args:
        wiki_path: Path to the Claude_wiki directory.

    Returns:
        List of dicts with file info (path, size, etc.)
    """
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
