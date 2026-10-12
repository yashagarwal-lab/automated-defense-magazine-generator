import pytest
from magazine_generator.layout.registry import LAYOUT_REGISTRY, get_layout, suggest_layout_for_articles

def test_layout_registry_archetypes():
    assert "lead" in LAYOUT_REGISTRY
    assert "pair" in LAYOUT_REGISTRY
    assert "trio" in LAYOUT_REGISTRY
    assert "quad" in LAYOUT_REGISTRY
    assert "photo_essay" in LAYOUT_REGISTRY

def test_suggest_layout_for_articles():
    assert suggest_layout_for_articles([{"title": "1"}]) == "photo_essay"
    assert suggest_layout_for_articles([{"title": "1"}, {"title": "2"}]) == "pair"
    assert suggest_layout_for_articles([{"title": "1", "pull_quote": "A quote"}, {"title": "2"}]) == "lead"
    assert suggest_layout_for_articles([{"title": "1"}, {"title": "2"}, {"title": "3"}]) == "trio"
    assert suggest_layout_for_articles([{"title": "1"}, {"title": "2"}, {"title": "3"}, {"title": "4"}]) == "quad"
