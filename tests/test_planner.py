import pytest
from magazine_generator.rendering.engine import compile_magazine_data
from magazine_generator.layout.planner import build_pages_plan

def test_build_pages_plan_page_count():
    mag, arts = compile_magazine_data()
    pages, toc, stats, used = build_pages_plan(mag, arts)

    # Invariant: exactly 50 pages
    assert len(pages) == 50, f"Expected 50 pages, got {len(pages)}"
    assert pages[0]["type"] == "cover"
    assert pages[1]["type"] == "contents"
    assert pages[2]["type"] == "editor"
    assert pages[3]["type"] == "overview"
    assert pages[-1]["type"] == "back"

def test_toc_page_numbers_resolved():
    mag, arts = compile_magazine_data()
    pages, toc, stats, used = build_pages_plan(mag, arts)

    assert len(toc) > 0
    for item in toc:
        assert "page" in item
        assert isinstance(item["page"], int)
        assert 1 <= item["page"] <= 50

def test_article_usage_count():
    mag, arts = compile_magazine_data()
    pages, toc, stats, used = build_pages_plan(mag, arts)

    # Invariant: exactly 74 curated articles used in the issue
    assert len(used) == 74
    for a in used:
        assert "section_name" in a
        assert a["section_name"] in [s["name"] for s in mag["sections"]]
