import math
from typing import Dict, List, Any, Tuple
from .registry import suggest_layout_for_articles

def compute_appendix_chunks(total_articles: int, num_pages: int) -> List[int]:
    """Dynamically compute rows per appendix page given total articles and allocated pages.

    First page has title block (effective capacity ~23 rows).
    Subsequent pages have continuation headers (~26 rows).
    """
    if num_pages <= 0 or total_articles <= 0:
        return []
    if num_pages == 1:
        return [total_articles]

    # Calculate optimal distribution
    # Target: first page gets up to 23, remaining divided evenly
    first_target = min(23, max(15, total_articles // num_pages))
    remaining = total_articles - first_target
    cont_pages = num_pages - 1

    chunks = [first_target]
    base = remaining // cont_pages
    extra = remaining % cont_pages

    for i in range(cont_pages):
        chunks.append(base + (1 if i < extra else 0))

    return chunks

def auto_budget_magazine(
    target_pages: int,
    curated_pool: Dict[str, List[Dict[str, Any]]],
    sections_meta: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Dynamically compute publication page budget and generate section page layout plans.

    Guarantees:
      Total pages = Cover (1) + Contents (1) + Editor (1) + [Overview (1)] +
                    Sections (Openers + Content) + Appendix 1 (1) + Appendix 2 (K) + Back (1)
                  == target_pages
    """
    if target_pages < 12:
        raise ValueError(f"Target page count ({target_pages}) must be at least 12.")

    # 1. Front Matter Allocation
    include_overview = (target_pages >= 24)
    front_pages = 4 if include_overview else 3

    # 2. Back Matter Fixed: Back Cover (1) + Appendix 1 Sources (1)
    back_fixed = 2

    # 3. Available pages for sections + Appendix 2
    budget_available = target_pages - (front_pages + back_fixed)

    # 4. Determine number of sections
    num_sections = len(curated_pool)
    if num_sections == 0:
        num_sections = 4

    # Each section requires 1 opener page
    openers_count = num_sections

    # Estimate articles and appendix pages
    # First estimate: ~2 articles per content page
    # Approximate content pages: budget_available - openers_count - (estimated appendix)
    est_article_pages = max(num_sections, budget_available - openers_count - 2)
    est_total_articles = est_article_pages * 2

    # Appendix 2 pages needed for est_total_articles:
    if est_total_articles <= 23:
        ap2_pages = 1
    elif est_total_articles <= 48:
        ap2_pages = 2
    elif est_total_articles <= 74:
        ap2_pages = 3
    else:
        ap2_pages = max(1, math.ceil((est_total_articles - 23) / 26) + 1)

    # Ensure valid content pages
    content_pages_total = budget_available - openers_count - ap2_pages
    while content_pages_total < num_sections and ap2_pages > 1:
        ap2_pages -= 1
        content_pages_total = budget_available - openers_count - ap2_pages

    # 5. Distribute content pages across sections
    section_names = list(curated_pool.keys())
    pool_sizes = [len(curated_pool[s]) for s in section_names]
    total_pool_avail = sum(pool_sizes)

    # Distribute proportionally according to available articles in pool
    alloc_pages = {}
    base_per_sec = content_pages_total // num_sections
    rem_pages = content_pages_total % num_sections

    for i, s_name in enumerate(section_names):
        alloc_pages[s_name] = base_per_sec + (1 if i < rem_pages else 0)

    # 6. Generate page plans for each section using registry suggestions
    section_plans = []
    used_articles_count = 0
    selected_articles_by_sec = {}

    for s_name in section_names:
        p_count = alloc_pages[s_name]
        avail_arts = curated_pool[s_name]
        pages_plan = []
        art_idx = 0

        for p_idx in range(p_count):
            remaining_pages = p_count - p_idx
            remaining_arts = max(0, len(avail_arts) - art_idx)

            if remaining_pages == 1:
                bundle_size = max(1, min(3, remaining_arts))
                layout_choice = "trio" if bundle_size == 3 else ("lead" if (p_idx == 0) else ("pair" if bundle_size == 2 else "photo_essay"))
            else:
                max_allowed = max(1, remaining_arts - (remaining_pages - 1))
                if remaining_arts >= remaining_pages * 3:
                    bundle_size = min(3, max_allowed)
                    layout_choice = "trio"
                elif remaining_arts >= remaining_pages * 2:
                    bundle_size = min(2, max_allowed)
                    layout_choice = "lead" if (p_idx == 0) else "pair"
                else:
                    bundle_size = min(2, max_allowed) if max_allowed >= 2 else 1
                    layout_choice = "pair" if bundle_size == 2 else "photo_essay"

            if art_idx < len(avail_arts):
                bundle = avail_arts[art_idx:art_idx + bundle_size]
            else:
                # Wrap-around fallback if articles exhausted
                bundle = [avail_arts[art_idx % len(avail_arts)]]

            art_idx += len(bundle)

            pages_plan.append({
                "layout": layout_choice,
                "articles": [a["id"] for a in bundle]
            })

        selected_articles_by_sec[s_name] = avail_arts[:min(art_idx, len(avail_arts))]
        used_articles_count += min(art_idx, len(avail_arts))

        # Find or construct section meta
        s_meta = {}
        if sections_meta:
            for sm in sections_meta:
                if sm.get("name") == s_name:
                    s_meta = dict(sm)
                    break
        if not s_meta:
            s_meta = {
                "name": s_name,
                "blurb": f"Reports and strategic intelligence on {s_name}.",
                "intro": [f"This section covers key developments in {s_name}."]
            }

        s_meta["pages"] = pages_plan
        section_plans.append(s_meta)

    # 7. Compute exact Appendix 2 chunks
    ap2_chunks = compute_appendix_chunks(used_articles_count, ap2_pages)

    return {
        "target_pages": target_pages,
        "include_overview": include_overview,
        "sections": section_plans,
        "appendix2_pages": ap2_pages,
        "appendix2_chunks": ap2_chunks,
        "total_articles_used": used_articles_count,
        "selected_articles": selected_articles_by_sec
    }
