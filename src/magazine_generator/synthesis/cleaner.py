import re
from typing import List

ARTIFACTS = [
    "Join conversation View All Comments",
    "Share your thoughts in the comments",
    "Insightful Agree Disagree Skeptical Concerning Promising Worth Reading Big Development Post Comment",
    "Be respectful · TOI community guidelines",
    "Become an Independent member to bookmark this article",
    "Log in On The Ground newsletter: Get a weekly dispatch",
    "Email * SIGN UP I would like to be emailed about offers",
    "ADVERTISEMENT Stay connected Make The News Mill your preferred source",
    "See more TNM stories when you search for news on Google. Add TNM on Google",
    "Advertisement",
    "ADVERTISEMENT",
    "This image has been generated using AI and is for representational purposes only.",
    "Blue Drum murder case",
    "Muskan, Sahil undergo counselling",
    "Delhi Police denies permission for Oct 2 protest",
    "CEC Gyanesh Kumar must resign",
    "Wife gives supari to rape woman",
    "Advertisment",
    "Stay connected Make The News Mill your preferred source",
    "Kolkata, Sep 8 (SocialNews.XYZ)",
    "olkata, Sep 8 (SocialNews.XYZ)",
    "AR hosts friendly football match at Pallel | IMPHAL, Sep 21",
    "R hosts friendly football match at Pallel | IMPHAL, Sep 21",
    "(With agency inputs) TAWANG: "
]

def clean_text(text: str) -> str:
    """Normalize raw scraped article body text and remove news boilerplate."""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    for a in ARTIFACTS:
        text = text.replace(a, '')
    text = re.sub(r'\s*Also Read:.*?(?:\.|$)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*Read More:.*?(?:\.|$)', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*Click here to.*?(?:\.|$)', '', text, flags=re.IGNORECASE)
    return text.strip()

def split_sentences(text: str) -> List[str]:
    """Split clean text into punctuated sentences, fixing joined periods."""
    text = re.sub(r"([a-z][.!?])([A-Z])", r"\g<1> \g<2>", text)
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'“‘])", text)
    return [s.strip() for s in sentences if s.strip()]

def clean_title(title: str) -> str:
    """Clean publisher noise, dates, and clickbait suffixes from headlines."""
    if not title:
        return ""
    title = re.sub(r'\s*[-|–—]\s*(?:The Sentinel|India Today|EastMojo|Assam Tribune|NDTV|TOI|Hindustan Times).*$', '', title, flags=re.IGNORECASE)
    return title.strip()
