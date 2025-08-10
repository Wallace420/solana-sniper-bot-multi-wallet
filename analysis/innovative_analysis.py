"""Innovative analytics utilities for exploring novel data relationships."""

from typing import Iterable, Tuple
import math


def _to_float_list(series: Iterable[float]):
    return [float(x) for x in series]


def _corr(a: Iterable[float], b: Iterable[float]) -> float:
    a = _to_float_list(a)
    b = _to_float_list(b)
    if not a or not b:
        return 0.0
    ma = sum(a) / len(a)
    mb = sum(b) / len(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((y - mb) ** 2 for y in b))
    return num / (da * db) if da and db else 0.0


def cross_correlation_lag(
    series_a: Iterable[float], series_b: Iterable[float], max_lag: int = 5
) -> Tuple[int, float]:
    """Return the lag with the strongest correlation between two series."""
    a = _to_float_list(series_a)
    b = _to_float_list(series_b)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    best_lag = 0
    best_corr = 0.0
    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            c = _corr(a[-lag:], b[:lag])
        elif lag > 0:
            c = _corr(a[:-lag], b[lag:])
        else:
            c = _corr(a, b)
        if abs(c) > abs(best_corr):
            best_corr, best_lag = c, lag
    return best_lag, best_corr


def hurst_exponent(series: Iterable[float]) -> float:
    """Estimate the Hurst exponent to gauge trend persistence."""
    ts = _to_float_list(series)
    n = len(ts)
    if n < 20:
        return float("nan")
    lags = range(2, min(100, n // 2))
    tau = []
    for lag in lags:
        diffs = [ts[i + lag] - ts[i] for i in range(n - lag)]
        if not diffs:
            continue
        mean = sum(diffs) / len(diffs)
        var = sum((d - mean) ** 2 for d in diffs) / len(diffs)
        tau.append(math.sqrt(var))
    logs = [(math.log(l), math.log(t)) for l, t in zip(lags, tau) if t > 0]
    if not logs:
        return float("nan")
    xs, ys = zip(*logs)
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in logs)
    den = sum((x - mx) ** 2 for x in xs)
    slope = num / den if den else 0.0
    return slope * 2.0
