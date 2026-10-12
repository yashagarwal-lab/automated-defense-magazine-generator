from typing import Dict, List, Any
from .filter import is_article_relevant, validate_date_window
from .taxonomy import categorize_article

def allocate_articles_to_sections(
    pool: Dict[str, Dict[str, Any]],
    target_counts: Dict[str, int] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """Group and allocate candidate articles across the 4 sections according to page quotas."""
    if target_counts is None:
        target_counts = {
            "Security & Strategic Affairs": 26,
            "Regional News & Development": 20,
            "Society & Youth Empowerment": 16,
            "Sports & Achievements": 12
        }

    grouped: Dict[str, List[Dict[str, Any]]] = {
        "Security & Strategic Affairs": [],
        "Regional News & Development": [],
        "Society & Youth Empowerment": [],
        "Sports & Achievements": []
    }

    for art_id, rec in pool.items():
        rec["id"] = art_id
        if not validate_date_window(rec.get("date", "")):
            continue
        if not is_article_relevant(rec):
            continue
        cat = categorize_article(rec)
        grouped[cat].append(rec)

    allocated = {}
    for cat, quota in target_counts.items():
        allocated[cat] = grouped[cat][:quota]

    return allocated
