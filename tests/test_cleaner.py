import pytest
from magazine_generator.synthesis.cleaner import clean_text, split_sentences, clean_title

def test_clean_text_removes_artifacts():
    dirty = "Troops moved into sector. ADVERTISEMENT Stay connected Make The News Mill your preferred source Also Read: Other news."
    cleaned = clean_text(dirty)
    assert "ADVERTISEMENT" not in cleaned
    assert "Also Read" not in cleaned
    assert "Troops moved into sector." in cleaned

def test_split_sentences_joined_periods():
    joined = "Troops reached Mago area under Thingbu Circle.The awareness campaign commenced at Mago village."
    sentences = split_sentences(joined)
    assert len(sentences) == 2
    assert sentences[0] == "Troops reached Mago area under Thingbu Circle."
    assert sentences[1] == "The awareness campaign commenced at Mago village."
    # Ensure no ASCII control characters are introduced
    assert "\x01" not in sentences[0]
    assert "\x02" not in sentences[1]

def test_split_sentences_quotes_and_punctuation():
    text = 'General Kalia confirmed the deployment. "All posts are on high alert," an officer stated! The operation concluded.'
    sentences = split_sentences(text)
    assert len(sentences) == 3
    assert sentences[0].endswith(".")
    assert sentences[2] == "The operation concluded."

def test_clean_title_removes_publisher_suffix():
    assert clean_title("Manipur Police arrest 4 insurgents - India Today NE") == "Manipur Police arrest 4 insurgents"
    assert clean_title("Corps Commander talks held — The Sentinel") == "Corps Commander talks held"
    assert clean_title("Normal Headline") == "Normal Headline"
