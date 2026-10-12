import re
import yaml
from pathlib import Path
from typing import List, Dict, Any, Union
from .base import BaseIngestor

FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)

class MarkdownIngestor(BaseIngestor):
    """Ingest articles from Markdown files containing YAML frontmatter."""

    def parse_markdown_file(self, path: Path) -> Dict[str, Any]:
        raw = path.read_text(encoding="utf-8")
        match = FRONTMATTER_PATTERN.match(raw)
        meta = {}
        body = raw
        if match:
            fm_text, body_text = match.groups()
            try:
                meta = yaml.safe_load(fm_text) or {}
            except Exception:
                meta = {}
            body = body_text.strip()

        article_id = str(meta.get("id", path.stem))
        title = meta.get("title", path.stem.replace("-", " ").title())
        date_val = str(meta.get("date", "2026-09-15"))
        source = meta.get("source", "Field Dispatch")
        url = meta.get("url", f"file://{path.resolve()}")

        return {
            "id": article_id,
            "title": title,
            "text": body,
            "body": [p.strip() for p in body.split("\n\n") if p.strip()],
            "source": source,
            "date": date_val,
            "url": url,
            "image": meta.get("image", ""),
            "image_credit": meta.get("image_credit", f"Photo: {source}"),
            "kicker": meta.get("kicker", source),
            "section": meta.get("section", "Security & Strategic Affairs")
        }

    def ingest(self, source: Union[str, Path]) -> List[Dict[str, Any]]:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Markdown path does not exist: {path}")

        articles = []
        if path.is_file() and path.suffix.lower() in (".md", ".markdown"):
            articles.append(self.parse_markdown_file(path))
        elif path.is_dir():
            for f in sorted(path.glob("*.md")):
                articles.append(self.parse_markdown_file(f))
        return articles
