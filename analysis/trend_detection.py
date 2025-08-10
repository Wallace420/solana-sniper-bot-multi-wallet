"""Detect trending tokens or topics from social posts."""

import re
from typing import List, Dict


def extract_trending_tokens(posts: List[Dict[str, str]], top_n: int = 5) -> List[str]:
    """Return top mentioned tokens across posts."""
    counts: Dict[str, int] = {}
    for p in posts:
        for token in re.findall(r"[A-Z]{2,}", p.get("text", "")):
            counts[token] = counts.get(token, 0) + 1
    return sorted(counts, key=counts.get, reverse=True)[:top_n]

