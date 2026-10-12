from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Formation:
    name: str
    hq: str
    role: str

@dataclass
class CoverLine:
    kicker: str
    text: str

@dataclass
class CoverConfig:
    image: str
    credit: str
    feature_kicker: str
    feature: str
    lines: List[CoverLine] = field(default_factory=list)

@dataclass
class PagePlan:
    layout: str
    articles: List[str]
    caption: Optional[str] = None

@dataclass
class SectionPlan:
    name: str
    blurb: str
    opener_image: str
    pages: List[Dict[str, Any]]
    number: str = ""
    inside: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class MagazineConfig:
    title: str
    subtitle: str
    issue_label: str
    edition: str
    short_title: str
    cover: Dict[str, Any]
    editor: Dict[str, Any]
    overview: Dict[str, Any]
    colophon: Dict[str, str]
    sections: List[Dict[str, Any]]
