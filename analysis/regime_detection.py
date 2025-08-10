from typing import List, Dict


def add_volatility_regime(candles: List[Dict], window: int = 10, iterations: int = 100) -> List[Dict]:
    """Label candles with a simple two-cluster volatility regime.

    Uses a basic 1D k-means on rolling standard deviation of returns to
    distinguish between low and high volatility environments.
    """
    closes = [c["close"] for c in candles]
    returns = [0.0]
    for i in range(1, len(closes)):
        prev = closes[i - 1]
        returns.append(0.0 if prev == 0 else (closes[i] - prev) / prev)

    vol = []
    for i in range(len(returns)):
        if i < window:
            vol.append(None)
        else:
            segment = returns[i - window + 1 : i + 1]
            mean = sum(segment) / len(segment)
            var = sum((r - mean) ** 2 for r in segment) / len(segment)
            vol.append(var ** 0.5)

    data = [v for v in vol if v is not None]
    if not data:
        for c in candles:
            c["regime"] = None
        return candles

    centers = [min(data), max(data)]
    for _ in range(iterations):
        clusters = {0: [], 1: []}
        for v in data:
            idx = 0 if abs(v - centers[0]) <= abs(v - centers[1]) else 1
            clusters[idx].append(v)
        new_centers = []
        for i in (0, 1):
            if clusters[i]:
                new_centers.append(sum(clusters[i]) / len(clusters[i]))
            else:
                new_centers.append(centers[i])
        if new_centers == centers:
            break
        centers = new_centers

    for candle, v in zip(candles, vol):
        if v is None:
            candle["regime"] = None
        else:
            candle["regime"] = 0 if abs(v - centers[0]) <= abs(v - centers[1]) else 1
    return candles
