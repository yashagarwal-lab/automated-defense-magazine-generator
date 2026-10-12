from typing import List, Dict, Any
from .cleaner import clean_text, split_sentences
from .overrides import EDITORIAL_OVERRIDES

def summarize_article(rec: Dict[str, Any], max_words: int = 180) -> List[str]:
    """Synthesize a professional editorial summary paragraph with source attribution."""
    title = rec.get("title", "")
    desc = rec.get("description", "")
    raw_text = rec.get("text", "")
    source = rec.get("source", "Open Source Intelligence")
    date_val = rec.get("date", "")

    # Check explicit editorial overrides first
    for name, item in EDITORIAL_OVERRIDES.items():
        if item["match"](title, desc, raw_text):
            return [item["summary"]]

    # Otherwise construct bounded summary from body/description
    clean_body = clean_text(raw_text)
    clean_desc = clean_text(desc)

    sentences = split_sentences(clean_body) if len(clean_body) > 100 else split_sentences(clean_desc)
    if not sentences:
        sentences = [clean_desc if clean_desc else title]

    collected = []
    words_count = 0
    for s in sentences:
        sw = len(s.split())
        if collected and (words_count + sw > max_words):
            break
        collected.append(s)
        words_count += sw

    summary = " ".join(collected)
    return [summary]
