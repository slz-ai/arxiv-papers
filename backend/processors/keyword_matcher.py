import re

from backend.config import KEYWORDS


def match_keywords(title: str, abstract: str) -> list[str]:
    """Return list of matched tag names based on title and abstract."""
    text = f"{title} {abstract}".lower()
    matched = []
    for tag_name, patterns in KEYWORDS.items():
        for pattern in patterns:
            if re.search(r"\b" + re.escape(pattern.lower()) + r"\b", text):
                matched.append(tag_name)
                break
    return matched
