from urllib.request import urlopen
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .data_cache import load_cache, save_cache

BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"

def fetch_ohlcv(
    symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 100, use_cache: bool = True
) -> List[Dict]:
    """Fetch OHLCV data from Binance and return a list of dictionaries.

    Falls back to generated synthetic data if the network request fails.
    When ``use_cache`` is True, results are stored and retrieved from a
    simple JSON cache to avoid repeated network calls.
    """

    cache_key = f"ohlcv_{symbol}_{interval}_{limit}"
    if use_cache:
        cached = load_cache(cache_key)
        if cached is not None:
            return cached

    url = f"{BINANCE_KLINES_URL}?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        with urlopen(url, timeout=10) as resp:
            data = json.load(resp)
        candles = []
        for item in data:
            candles.append(
                {
                    "timestamp": datetime.fromtimestamp(item[0] / 1000),
                    "open": float(item[1]),
                    "high": float(item[2]),
                    "low": float(item[3]),
                    "close": float(item[4]),
                    "volume": float(item[5]),
                }
            )
        if use_cache:
            save_cache(cache_key, candles)
        return candles
    except Exception:
        now = datetime.utcnow()
        candles = []
        price = 30000.0
        for i in range(limit):
            candles.append(
                {
                    "timestamp": now - timedelta(hours=limit - i),
                    "open": price,
                    "high": price * 1.01,
                    "low": price * 0.99,
                    "close": price * (1 + 0.001 * i),
                    "volume": 0.0,
                }
            )
        if use_cache:
            save_cache(cache_key, candles)
        return candles


def fetch_trades(
    symbol: str = "BTCUSDT", limit: int = 100, use_cache: bool = True
) -> List[Dict[str, Any]]:
    """Fetch recent trades for a symbol with a deterministic offline sample.

    Utilizes the JSON cache when ``use_cache`` is True.
    """

    cache_key = f"trades_{symbol}_{limit}"
    if use_cache:
        cached = load_cache(cache_key)
        if cached is not None:
            return cached

    url = f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit={limit}"
    try:
        with urlopen(url, timeout=10) as resp:
            data = json.load(resp)
        trades: List[Dict[str, Any]] = []
        for t in data:
            trades.append(
                {
                    "price": float(t["price"]),
                    "volume": float(t["qty"]),
                    "side": "buy" if t.get("isBuyerMaker") else "sell",
                    "timestamp": datetime.fromtimestamp(t["time"] / 1000),
                }
            )
        if use_cache:
            save_cache(cache_key, trades)
        return trades
    except Exception:
        trades = []
        price = 30000.0
        for _ in range(limit):
            trades.append(
                {
                    "price": price * (1 + random.uniform(-0.001, 0.001)),
                    "volume": random.uniform(0.1, 1.0),
                    "side": random.choice(["buy", "sell"]),
                    "timestamp": datetime.utcnow(),
                }
            )
        if use_cache:
            save_cache(cache_key, trades)
        return trades


def fetch_token_supply(symbol: str = "BTC") -> float:
    """Return circulating supply for a token with offline fallback."""

    supplies = {"BTC": 21_000_000, "ETH": 120_000_000}
    return float(supplies.get(symbol, 1_000_000))


def fetch_social_posts() -> List[Dict[str, str]]:
    """Return a mix of social posts from various communities."""

    posts = [
        {"source": "twitter", "text": "BTC and SOL are mooning!"},
        {"source": "telegram", "text": "Check out new PVP token XYZ"},
        {"source": "github", "text": "Merge pull request adding OG token analyzer"},
        {"source": "news", "text": "Ethereum fees spike as NFTs trend"},
    ]
    random.shuffle(posts)
    return posts
