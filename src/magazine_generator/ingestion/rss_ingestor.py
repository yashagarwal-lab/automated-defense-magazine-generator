import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any, Union
from urllib.request import urlopen, Request
from pathlib import Path
from .base import BaseIngestor

class RSSIngestor(BaseIngestor):
    """Ingest articles from RSS 2.0 / Atom XML feeds or cached XML files."""

    def ingest(self, source: Union[str, Path]) -> List[Dict[str, Any]]:
        if isinstance(source, Path) or (isinstance(source, str) and not source.startswith(("http://", "https://"))):
            xml_text = Path(source).read_text(encoding="utf-8")
        else:
            req = Request(str(source), headers={"User-Agent": "Mozilla/5.0 (Defense Intel Parser)"})
            with urlopen(req, timeout=15) as resp:
                xml_text = resp.read().decode("utf-8", errors="replace")

        root = ET.fromstring(xml_text)
        articles: List[Dict[str, Any]] = []

        # RSS 2.0 channel -> item
        channel = root.find("channel")
        items = channel.findall("item") if channel is not None else root.findall(".//item")
        if not items:
            # Try Atom feed entry
            items = root.findall(".//{http://www.w3.org/2005/Atom}entry")

        for idx, item in enumerate(items, 1):
            title = (item.findtext("title") or item.findtext("{http://www.w3.org/2005/Atom}title") or "Untitled").strip()
            link = (item.findtext("link") or item.findtext("{http://www.w3.org/2005/Atom}link") or "").strip()
            desc = (item.findtext("description") or item.findtext("summary") or item.findtext("{http://www.w3.org/2005/Atom}summary") or "").strip()
            pub_date = item.findtext("pubDate") or item.findtext("updated") or "2026-09-15"

            # Normalize date to YYYY-MM-DD
            try:
                # Common RSS date: Mon, 15 Sep 2026 12:00:00 GMT
                d_str = " ".join(pub_date.split()[:4])
                iso_date = datetime.strptime(d_str, "%a, %d %b %Y").strftime("%Y-%m-%d")
            except Exception:
                iso_date = "2026-09-15"

            articles.append({
                "id": f"rss_{idx}",
                "title": title,
                "text": desc,
                "body": [desc] if desc else [],
                "source": "RSS Intelligence Wire",
                "date": iso_date,
                "url": link,
                "kicker": "Intelligence Wire"
            })

        return articles
