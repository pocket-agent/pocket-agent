import re


def fts_query(text: str) -> str:
    terms = re.findall(r"[a-zA-Z0-9_]+", text)
    if not terms:
        return text
    return " OR ".join(terms)
