from urllib.request import urlopen
import json
from typing import Dict

from .data_cache import load_cache, save_cache


def fetch_github_activity(repo: str = "bitcoin/bitcoin", use_cache: bool = True) -> Dict[str, int]:
    """Fetch basic GitHub repository statistics.

    Returns a dictionary with star, fork and watcher counts. Falls back to
    zero-valued metrics if the request fails. When ``use_cache`` is True, the
    results are stored in the JSON cache for reuse across runs.
    """

    cache_key = f"github_activity_{repo.replace('/', '_')}"
    if use_cache:
        cached = load_cache(cache_key)
        if cached is not None:
            return cached

    url = f"https://api.github.com/repos/{repo}"
    try:
        with urlopen(url, timeout=10) as resp:
            data = json.load(resp)
        activity = {
            "stars": int(data.get("stargazers_count", 0)),
            "forks": int(data.get("forks_count", 0)),
            "watchers": int(data.get("subscribers_count", 0)),
        }
        if use_cache:
            save_cache(cache_key, activity)
        return activity
    except Exception:
        activity = {"stars": 0, "forks": 0, "watchers": 0}
        if use_cache:
            save_cache(cache_key, activity)
        return activity


def analyze_github_trend(repo: str = "bitcoin/bitcoin") -> Dict[str, int]:
    """Compute growth metrics for a GitHub repository.

    The function compares the current activity with the last cached snapshot to
    estimate growth in stars and forks. The latest snapshot is stored for
    future comparisons.
    """

    prev_key = f"github_prev_{repo.replace('/', '_')}"
    prev = load_cache(prev_key) or {"stars": 0, "forks": 0}
    current = fetch_github_activity(repo, use_cache=False)
    trend = {
        "star_growth": current["stars"] - prev.get("stars", 0),
        "fork_growth": current["forks"] - prev.get("forks", 0),
    }
    save_cache(prev_key, current)
    return trend
