import pytest
from pathlib import Path
from magazine_generator.ingestion.factory import create_ingestor, ingest_from_source
from magazine_generator.ingestion.json_ingestor import JSONIngestor
from magazine_generator.ingestion.markdown_ingestor import MarkdownIngestor
from magazine_generator.ingestion.rss_ingestor import RSSIngestor

def test_json_ingestor_dict():
    ing = JSONIngestor()
    data = {
        "art1": {"title": "Test 1", "date": "2026-09-10", "text": "Body 1"},
        "art2": {"title": "Test 2", "date": "2026-09-12", "text": "Body 2"}
    }
    res = ing.ingest(data)
    assert len(res) == 2
    assert res[0]["id"] == "art1"
    assert res[1]["id"] == "art2"

def test_markdown_ingestor_string(tmp_path):
    md_file = tmp_path / "sample.md"
    md_file.write_text("""---
title: Strategic Tunnel Operational
date: 2026-09-15
source: Border Roads Journal
---

The strategic tunnel was formally inaugurated today by defense officials.

Traffic has commenced smoothly.
""", encoding="utf-8")

    ing = MarkdownIngestor()
    res = ing.ingest(md_file)
    assert len(res) == 1
    assert res[0]["title"] == "Strategic Tunnel Operational"
    assert res[0]["source"] == "Border Roads Journal"
    assert len(res[0]["body"]) == 2

def test_factory_creation():
    assert isinstance(create_ingestor("json"), JSONIngestor)
    assert isinstance(create_ingestor("markdown"), MarkdownIngestor)
    assert isinstance(create_ingestor("rss"), RSSIngestor)
    with pytest.raises(ValueError):
        create_ingestor("invalid_format")
