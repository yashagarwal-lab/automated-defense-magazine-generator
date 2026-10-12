from dataclasses import dataclass
from typing import Dict, List, Optional, Any

@dataclass
class LayoutDefinition:
    id: str
    name: str
    article_count: int
    page_span: int = 1
    requires_image: bool = True
    description: str = ""
    suggested_words_per_article: int = 140

LAYOUT_REGISTRY: Dict[str, LayoutDefinition] = {
    "lead": LayoutDefinition(
        id="lead",
        name="Lead Feature & Sidebar Brief",
        article_count=2,
        requires_image=True,
        description="One dominant hero story (with 108mm photo and 2-column prose) paired with a sidebar brief.",
        suggested_words_per_article=160
    ),
    "pair": LayoutDefinition(
        id="pair",
        name="Parallel Columns Pair",
        article_count=2,
        requires_image=True,
        description="Two balanced parallel articles with top photographs and independent vertical flows.",
        suggested_words_per_article=130
    ),
    "trio": LayoutDefinition(
        id="trio",
        name="Headline & Dual Briefs Trio",
        article_count=3,
        requires_image=True,
        description="One wide top headline story accompanied by two compact briefing dispatches below.",
        suggested_words_per_article=110
    ),
    "quad": LayoutDefinition(
        id="quad",
        name="Four-Story Intelligence Grid",
        article_count=4,
        requires_image=False,
        description="Four compact perimeter dispatches in a balanced 2x2 symmetrical briefing grid.",
        suggested_words_per_article=80
    ),
    "photo_essay": LayoutDefinition(
        id="photo_essay",
        name="Visual Defense Essay",
        article_count=1,
        requires_image=True,
        description="Full-width cinematic photograph with comprehensive tactical narrative.",
        suggested_words_per_article=200
    )
}

def get_layout(layout_id: str) -> Optional[LayoutDefinition]:
    return LAYOUT_REGISTRY.get(layout_id)

def suggest_layout_for_articles(articles: List[Dict[str, Any]]) -> str:
    """Recommend the optimal layout archetype based on article count and imagery."""
    n = len(articles)
    if n == 1:
        return "photo_essay"
    elif n == 2:
        # If first has pullquote or large image, favor lead, else pair
        if articles[0].get("pull_quote"):
            return "lead"
        return "pair"
    elif n == 3:
        return "trio"
    elif n >= 4:
        return "quad"
    return "pair"
