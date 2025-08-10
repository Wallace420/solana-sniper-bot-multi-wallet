import json
from pathlib import Path
from typing import Any, Optional

CACHE_DIR = Path('.cache')


def load_cache(name: str) -> Optional[Any]:
    path = CACHE_DIR / f"{name}.json"
    if path.exists():
        with path.open('r') as f:
            data = json.load(f)
        print(f"loaded {name} from cache")
        return data
    return None


def save_cache(name: str, data: Any) -> None:
    CACHE_DIR.mkdir(exist_ok=True)
    path = CACHE_DIR / f"{name}.json"
    with path.open('w') as f:
        json.dump(data, f, default=str)
    print(f"saved {name} to cache")
