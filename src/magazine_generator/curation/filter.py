from typing import Dict, Any
from ..config import DATE_WINDOW

EXCLUSION_KEYWORDS = [
    "vandyke", "amit shah", "ucc", "ncert", "john abraham",
    "reebok", "tihar", "kerala", "tamil nadu", "18 warships",
    "blue drum murder"
]

INCLUSION_KEYWORDS = [
    "army", "rifles", "bro ", "border roads", "military",
    "security", "lac", "troop", "patrol", "militant",
    "terror", "insurgent", "ncc", "camp", "general",
    "defence", "defense", "soldier", "jawan", "hockey",
    "football", "sports", "youth"
]

def validate_date_window(date_str: str) -> bool:
    """Enforce strict publication window boundary."""
    return DATE_WINDOW[0] <= date_str <= DATE_WINDOW[1]

def is_article_relevant(rec: Dict[str, Any]) -> bool:
    """Evaluate whether an article meets domain relevance criteria."""
    title = rec.get("title", "").lower()
    desc = rec.get("description", "").lower()
    text = (title + " " + desc)

    if any(b in text for b in EXCLUSION_KEYWORDS):
        return False
    if not any(g in text for g in INCLUSION_KEYWORDS):
        return False
    return True
