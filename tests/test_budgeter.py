import pytest
from magazine_generator.layout.budgeter import compute_appendix_chunks, auto_budget_magazine
from magazine_generator.curation.allocator import allocate_articles_to_sections
from magazine_generator.rendering.engine import compile_magazine_data

def test_compute_appendix_chunks_single_page():
    assert compute_appendix_chunks(20, 1) == [20]
    assert compute_appendix_chunks(0, 1) == []

def test_compute_appendix_chunks_multiple_pages():
    chunks = compute_appendix_chunks(74, 3)
    assert len(chunks) == 3
    assert sum(chunks) == 74
    # First page title allowance check
    assert chunks[0] <= 23

def test_auto_budget_50_pages():
    mag, arts = compile_magazine_data()
    pool = allocate_articles_to_sections(arts)
    budget = auto_budget_magazine(50, pool, sections_meta=mag.get("sections", []))

    total = (4 if budget['include_overview'] else 3)
    total += sum(len(s.get("pages", [])) + 1 for s in budget['sections']) # openers + content
    total += 1 + budget['appendix2_pages'] + 1 # ap1 + ap2 + back

    assert total == 50, f"Expected 50 pages, calculated {total}"
    assert budget['appendix2_pages'] >= 1
    assert sum(budget['appendix2_chunks']) == budget['total_articles_used']

def test_auto_budget_32_pages():
    mag, arts = compile_magazine_data()
    pool = allocate_articles_to_sections(arts)
    budget = auto_budget_magazine(32, pool, sections_meta=mag.get("sections", []))

    total = (4 if budget['include_overview'] else 3)
    total += sum(len(s.get("pages", [])) + 1 for s in budget['sections'])
    total += 1 + budget['appendix2_pages'] + 1

    assert total == 32, f"Expected 32 pages, calculated {total}"

def test_auto_budget_24_pages():
    mag, arts = compile_magazine_data()
    pool = allocate_articles_to_sections(arts)
    budget = auto_budget_magazine(24, pool, sections_meta=mag.get("sections", []))

    total = (4 if budget['include_overview'] else 3)
    total += sum(len(s.get("pages", [])) + 1 for s in budget['sections'])
    total += 1 + budget['appendix2_pages'] + 1

    assert total == 24, f"Expected 24 pages, calculated {total}"
