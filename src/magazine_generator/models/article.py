from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class RawArticle:
    id: str
    title: str
    url: str
    source: str
    date: str
    description: Optional[str] = ""
    text: Optional[str] = ""

@dataclass
class CuratedArticle:
    id: str
    title: str
    url: str
    source: str
    date: str
    body: List[str]
    reasoning: str
    section_name: str = ""
    image: Optional[str] = None
    date_display: str = ""

    def word_count(self) -> int:
        return sum(len(p.split()) for p in self.body)

ArticlePool = Dict[str, RawArticle]
