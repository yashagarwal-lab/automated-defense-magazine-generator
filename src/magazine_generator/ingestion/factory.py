from typing import Union, List, Dict, Any
from pathlib import Path
from .base import BaseIngestor
from .json_ingestor import JSONIngestor
from .markdown_ingestor import MarkdownIngestor
from .rss_ingestor import RSSIngestor

def create_ingestor(source_type: str) -> BaseIngestor:
    """Factory to instantiate ingestors by type name."""
    st = source_type.lower().strip()
    if st in ("json", "articles_json", "pool_json"):
        return JSONIngestor()
    elif st in ("markdown", "md", "frontmatter"):
        return MarkdownIngestor()
    elif st in ("rss", "atom", "feed", "xml"):
        return RSSIngestor()
    else:
        raise ValueError(f"Unknown ingestion source type: {source_type}. Supported: 'json', 'markdown', 'rss'")

def ingest_from_source(source: Union[str, Path, dict, list], source_type: str = None) -> List[Dict[str, Any]]:
    """Convenience helper to auto-detect and ingest content."""
    if source_type is None:
        if isinstance(source, (dict, list)):
            source_type = "json"
        elif isinstance(source, (str, Path)):
            p = str(source).lower()
            if p.startswith(("http://", "https://")) or p.endswith(".xml"):
                source_type = "rss"
            elif p.endswith((".md", ".markdown")) or (isinstance(source, Path) and source.is_dir()):
                source_type = "markdown"
            elif p.endswith(".json"):
                source_type = "json"
            else:
                source_type = "json"

    ingestor = create_ingestor(source_type)
    return ingestor.ingest(source)
