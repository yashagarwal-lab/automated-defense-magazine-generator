from typing import Dict, List, Any
from .filter import is_article_relevant, validate_date_window
from .taxonomy import categorize_article

def allocate_articles_to_sections(
    pool: Dict[str, Dict[str, Any]],
    target_counts: Dict[str, int] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """Group and allocate candidate articles across sections according to page quotas."""
    grouped: Dict[str, List[Dict[str, Any]]] = {
        "Security & Strategic Affairs": [],
        "Regional News & Development": [],
        "Society & Youth Empowerment": [],
        "Sports & Achievements": []
    }

    for art_id, rec in pool.items():
        rec["id"] = art_id
        cat = rec.get("section") or categorize_article(rec)
        if cat in grouped:
            grouped[cat].append(rec)
        else:
            grouped["Security & Strategic Affairs"].append(rec)

    if target_counts is None:
        return grouped

    allocated = {}
    for cat, quota in target_counts.items():
        allocated[cat] = grouped.get(cat, [])[:quota]

    return allocated
