from datetime import date
from collections import Counter
from html import escape
from typing import Dict, List, Any, Tuple
from ..config import DATE_WINDOW, APPENDIX2_ROWS_PER_PAGE, TARGET_PAGE_COUNT

def format_date_display(iso_str: str) -> str:
    """Format ISO date string to elegant publication format (e.g. 15 Sep 2026)."""
    try:
        d = date.fromisoformat(iso_str)
        return f"{d.day} {d.strftime('%b %Y')}"
    except Exception:
        return iso_str

def build_pages_plan(
    mag: Dict[str, Any],
    arts: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Assemble the authoritative 50-page magazine plan, resolving page references and folios."""
    for a in arts.values():
        if "date" in a:
            a["date_display"] = format_date_display(a["date"])

    pages: List[Dict[str, Any]] = [
        {"type": "cover"},
        {"type": "contents"},
        {"type": "editor"},
        {"type": "overview"}
    ]
    toc: List[Dict[str, Any]] = []
    used: List[Dict[str, Any]] = []

    # 1. Content Sections
    for i, s in enumerate(mag.get("sections", []), 1):
        s["number"] = f"{i:02d}"
        opener = {"type": "opener", "section": s}
        pages.append(opener)
        toc.append({
            "number": s["number"],
            "name": s["name"],
            "blurb": s["blurb"],
            "_ref": opener
        })
        s["inside"] = []
        for plan in s.get("pages", []):
            page_articles = [arts[art_id] for art_id in plan["articles"] if art_id in arts]
            p = {
                "type": plan["layout"],
                "section": s,
                "arts": page_articles
            }
            for a in page_articles:
                a["section_name"] = s["name"]
                used.append(a)
            pages.append(p)
            if page_articles:
                s["inside"].append({"title": page_articles[0]["title"], "_ref": p})

    # 2. Appendix 1: Sources & Count
    ap1_rows = Counter(a.get("source", "Unknown") for a in used).most_common()
    top = ap1_rows[0][1] if ap1_rows else 1
    ap1_table = [
        [
            escape(src),
            f'<span class="bar" style="width:{n / top * 28:.1f}mm"></span>',
            f'<span class="num">{n}</span>'
        ]
        for src, n in ap1_rows
    ]

    p_ap1 = {
        "type": "appendix",
        "kind": "sources",
        "first": True,
        "kicker": "Appendix 1",
        "title": "Sources & Count",
        "dek": f"{len(used)} articles from {len(ap1_rows)} publications, all published between "
               f"{format_date_display(DATE_WINDOW[0])} and {format_date_display(DATE_WINDOW[1])}.",
        "headers": ["Publication", "", "Articles"],
        "rows": ap1_table,
        "note": f"Total: {len(used)} articles. Every article carries a verified citation and source link."
    }
    pages.append(p_ap1)
    toc.append({
        "number": "A1",
        "name": "Appendix 1: Sources",
        "blurb": "Article count and distribution across regional and national media.",
        "_ref": p_ap1
    })

    # 3. Appendix 2: Reasoning for Selection
    ap2_rows = [
        [
            str(idx),
            f'<a href="{a.get("url", "#")}">{escape(a.get("title", ""))}</a> <span style="color:var(--muted);font-weight:400">'
            f'{escape(a.get("source", ""))} · {a.get("date_display", "")} · {escape(a.get("section_name", ""))}</span>',
            escape(a.get("reasoning", ""))
        ]
        for idx, a in enumerate(used, 1)
    ]

    start_idx = 0
    for k, size in enumerate(APPENDIX2_ROWS_PER_PAGE):
        chunk = ap2_rows[start_idx:start_idx + size]
        start_idx += size
        if not chunk:
            break
        p_ap2 = {
            "type": "appendix",
            "kind": "reasoning",
            "first": (k == 0),
            "kicker": "Appendix 2",
            "title": "Reasoning for Selection",
            "dek": "Editorial and strategic rationale justifying why each article was curated.",
            "headers": ["#", "Article", "Reasoning"],
            "rows": chunk
        }
        pages.append(p_ap2)
        if k == 0:
            toc.append({
                "number": "A2",
                "name": "Appendix 2: Reasoning",
                "blurb": "Strategic rationale and selection criteria for every article.",
                "_ref": p_ap2
            })

    # 4. Back Cover
    pages.append({"type": "back"})

    # 5. Number pages & resolve relative refs
    for n, p in enumerate(pages, 1):
        p["n"] = n
        p["side"] = "odd" if n % 2 else "even"

    for t in toc:
        if "_ref" in t:
            t["page"] = t.pop("_ref")["n"]

    for s in mag.get("sections", []):
        for item in s.get("inside", []):
            if isinstance(item, dict) and "_ref" in item:
                item["page"] = item.pop("_ref")["n"]

    stats = [
        {"n": len(used), "l": "Articles curated"},
        {"n": len(ap1_rows), "l": "Publications"},
        {"n": len(mag.get("sections", [])), "l": "Sections"},
        {"n": len({a.get("date") for a in used}), "l": "News days covered"}
    ]

    return pages, toc, stats, used
