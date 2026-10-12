from typing import Dict, Any

def categorize_article(rec: Dict[str, Any]) -> str:
    """Classify article into one of the 4 publication sections."""
    text = (rec.get("title", "") + " " + rec.get("description", "")).lower()
    if any(w in text for w in ["football", "hockey", "tournament", "sport", "medal", "cup", "durand"]):
        return "Sports & Achievements"
    elif any(w in text for w in ["student", "youth", "school", "ncc", "empowerment", "skill", "training", "camp", "education"]):
        return "Society & Youth Empowerment"
    elif any(w in text for w in ["development", "road", "bridge", "bro ", "infrastructure", "flood", "rescue", "village"]):
        return "Regional News & Development"
    else:
        return "Security & Strategic Affairs"
