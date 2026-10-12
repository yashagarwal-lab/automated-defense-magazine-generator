import pytest
from magazine_generator.curation.taxonomy import categorize_article
from magazine_generator.curation.filter import validate_date_window, is_article_relevant

def test_categorize_article():
    assert categorize_article({"title": "Durand Cup football match held by Assam Rifles"}) == "Sports & Achievements"
    assert categorize_article({"title": "NCC youth training camp in Kohima"}) == "Society & Youth Empowerment"
    assert categorize_article({"title": "BRO completes strategic border bridge in Tawang"}) == "Regional News & Development"
    assert categorize_article({"title": "Joint operation neutralises 2 militants in Churachandpur"}) == "Security & Strategic Affairs"

def test_validate_date_window():
    assert validate_date_window("2026-09-01") is True
    assert validate_date_window("2026-09-20") is True
    assert validate_date_window("2026-10-03") is True
    assert validate_date_window("2026-08-31") is False
    assert validate_date_window("2026-10-04") is False

def test_is_article_relevant_inclusion():
    relevant_rec = {
        "title": "Indian Army patrol encounters insurgents near border",
        "description": "Troops initiated search operation"
    }
    assert is_article_relevant(relevant_rec) is True

def test_is_article_relevant_exclusion():
    excluded_rec = {
        "title": "Bollywood celebrity John Abraham announces movie",
        "description": "Star speaks about fitness and Reebok"
    }
    assert is_article_relevant(excluded_rec) is False
