import json
from pathlib import Path
from typing import List, Dict, Any, Union
from .base import BaseIngestor

class JSONIngestor(BaseIngestor):
    """Ingest articles from structured JSON files or in-memory dicts/lists."""

    def ingest(self, source: Union[str, Path, dict, list]) -> List[Dict[str, Any]]:
        if isinstance(source, (str, Path)):
            path = Path(source)
            if not path.exists():
                raise FileNotFoundError(f"JSON source file not found: {path}")
            data = json.loads(path.read_text(encoding="utf-8"))
        elif isinstance(source, (dict, list)):
            data = source
        else:
            raise TypeError(f"Unsupported JSON source type: {type(source)}")

        articles: List[Dict[str, Any]] = []
        if isinstance(data, dict):
            for art_id, item in data.items():
                if isinstance(item, dict):
                    rec = dict(item)
                    if "id" not in rec:
                        rec["id"] = str(art_id)
                    articles.append(rec)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, dict):
                    rec = dict(item)
                    if "id" not in rec:
                        rec["id"] = str(i + 1)
                    articles.append(rec)
        return articles
