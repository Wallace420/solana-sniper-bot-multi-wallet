"""Advanced metrics for on-chain and market analysis."""

from typing import List, Dict, Any


def market_cap(price: float, supply: float) -> float:
    """Compute simple market capitalization."""
    return price * supply


def fee_summary(transactions: List[Dict[str, Any]]) -> float:
    """Aggregate fees from a list of transactions."""
    return sum(tx.get("fee", 0.0) for tx in transactions)


def fibonacci_retracements(prices: List[float]) -> Dict[str, float]:
    """Return common Fibonacci retracement levels for a price series."""
    if not prices:
        return {}
    low, high = min(prices), max(prices)
    diff = high - low
    return {
        "0.236": high - diff * 0.236,
        "0.382": high - diff * 0.382,
        "0.5": high - diff * 0.5,
        "0.618": high - diff * 0.618,
    }


def cumulative_volume_delta(trades: List[Dict[str, Any]]) -> List[float]:
    """Compute the CVD series from trade data."""
    cvd = 0.0
    series = []
    for t in trades:
        vol = t.get("volume", 0.0)
        if t.get("side") == "buy":
            cvd += vol
        else:
            cvd -= vol
        series.append(cvd)
    return series


def holder_distribution(balances: Dict[str, float]) -> Dict[str, Any]:
    """Summarise holder concentration for a token."""
    total = sum(balances.values())
    if total == 0:
        return {"total_holders": 0, "top5_concentration": 0, "top_holders": []}
    sorted_bal = sorted(balances.items(), key=lambda x: x[1], reverse=True)
    top5 = sorted_bal[:5]
    concentration = sum(v for _, v in top5) / total
    return {"total_holders": len(balances), "top5_concentration": concentration, "top_holders": top5}


def zscore_anomalies(prices: List[float], threshold: float = 3.0) -> List[int]:
    """Return indices of price points whose z-score exceeds the threshold."""
    if not prices:
        return []
    mean = sum(prices) / len(prices)
    variance = sum((p - mean) ** 2 for p in prices) / len(prices)
    std = variance ** 0.5
    if std == 0:
        return []
    return [i for i, p in enumerate(prices) if abs((p - mean) / std) > threshold]

