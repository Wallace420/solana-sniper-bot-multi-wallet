from typing import List, Dict, Tuple, Optional
import math
from itertools import product

from .feature_engineering import add_technical_indicators
from .regime_detection import add_volatility_regime

def simple_moving_average_strategy(candles: List[Dict], window: int = 14) -> List[Dict]:
    """Create a position column based on price crossing above SMA."""
    for candle in candles:
        sma = candle.get(f"sma_{window}")
        candle["position"] = 1 if (sma is not None and candle["close"] > sma) else 0
    return candles

def regime_adaptive_strategy(candles: List[Dict], regimes_windows: Dict[int, int]) -> List[Dict]:
    """Assign positions using SMA windows that vary by regime."""
    for candle in candles:
        regime = candle.get("regime")
        window = regimes_windows.get(regime)
        if window is None:
            candle["position"] = 0
            continue
        sma = candle.get(f"sma_{window}")
        candle["position"] = 1 if (sma is not None and candle["close"] > sma) else 0
    return candles

def backtest(candles: List[Dict], start_equity: float = 1.0) -> List[Dict]:
    """Vectorized-like backtest using a simple loop.

    Parameters
    ----------
    candles : List[Dict]
        Candle data with a ``position`` field.
    start_equity : float, optional
        Starting equity for the run so walk-forward tests can chain
        sequential segments. Defaults to 1.0.
    """
    equity = start_equity
    prev_close = None
    prev_pos = 0
    for candle in candles:
        close = candle["close"]
        ret = 0.0 if prev_close is None else (close - prev_close) / prev_close
        strat = prev_pos * ret
        equity *= 1 + strat
        candle["returns"] = ret
        candle["strategy"] = strat
        candle["equity"] = equity
        prev_pos = candle["position"]
        prev_close = close
    return candles

def sharpe_ratio(candles: List[Dict], freq: int = 365) -> float:
    """Compute annualized Sharpe ratio."""
    strategies = [c["strategy"] for c in candles if "strategy" in c]
    if not strategies:
        return 0.0
    mean = sum(strategies) / len(strategies)
    var = sum((r - mean) ** 2 for r in strategies) / len(strategies)
    std = math.sqrt(var)
    if std == 0:
        return 0.0
    return (mean / std) * math.sqrt(freq)


def performance_stats(candles: List[Dict]) -> Dict[str, float]:
    """Return basic performance metrics for a backtested series."""
    equities = [c.get("equity", 1.0) for c in candles]
    final_equity = equities[-1] if equities else 1.0
    peak = equities[0] if equities else 1.0
    max_dd = 0.0
    for eq in equities:
        if eq > peak:
            peak = eq
        drawdown = (peak - eq) / peak
        if drawdown > max_dd:
            max_dd = drawdown
    wins = sum(1 for c in candles if c.get("strategy", 0) > 0)
    losses = sum(1 for c in candles if c.get("strategy", 0) < 0)
    total = wins + losses
    win_rate = wins / total if total else 0.0
    return {
        "final_equity": final_equity,
        "total_return": final_equity - 1,
        "max_drawdown": max_dd,
        "win_rate": win_rate,
        "sharpe": sharpe_ratio(candles),
    }


def optimize_regime_windows(
    candles: List[Dict], low_windows: List[int], high_windows: List[int]
) -> Tuple[Dict[int, int], List[Dict], float]:
    """Brute-force search of SMA windows for each volatility regime."""
    best_sr = -float("inf")
    best_params: Dict[int, int] = {0: low_windows[0], 1: high_windows[0]}
    best_data: List[Dict] = []
    for lw, hw in product(low_windows, high_windows):
        local = [c.copy() for c in candles]
        local = add_technical_indicators(local, window=lw)
        if hw != lw:
            local = add_technical_indicators(local, window=hw)
        local = add_volatility_regime(local)
        local = regime_adaptive_strategy(local, {0: lw, 1: hw})
        local = backtest(local)
        sr = sharpe_ratio(local)
        if sr > best_sr:
            best_sr = sr
            best_params = {0: lw, 1: hw}
            best_data = local
    return best_params, best_data, best_sr


def walk_forward_optimize(
    candles: List[Dict],
    train_size: int = 200,
    test_size: int = 50,
    windows: Optional[List[int]] = None,
) -> Tuple[List[int], List[Dict], Dict[str, float]]:
    """Run a walk-forward backtest optimizing SMA windows on each segment.

    The function repeatedly splits the data into training and testing slices,
    tunes the SMA window on the training slice via Sharpe ratio, then applies
    the best window to the subsequent test slice. Equity carries over between
    segments to approximate live trading.

    Parameters
    ----------
    candles : List[Dict]
        Full candle history.
    train_size : int
        Number of candles used for parameter selection in each fold.
    test_size : int
        Number of candles evaluated out-of-sample after optimization.
    windows : List[int]
        SMA windows to sweep during optimization.

    Returns
    -------
    Tuple[List[int], List[Dict], Dict[str, float]]
        Tuple of chosen windows per fold, combined backtest candles and
        aggregated performance statistics.
    """
    if windows is None:
        windows = [5, 10, 20, 30]
    combined: List[Dict] = []
    chosen: List[int] = []
    equity = 1.0
    for start in range(0, len(candles) - train_size - test_size + 1, test_size):
        train = [c.copy() for c in candles[start : start + train_size]]
        test = [c.copy() for c in candles[start + train_size : start + train_size + test_size]]
        best_w = windows[0]
        best_sr = -float("inf")
        for w in windows:
            tr = [c.copy() for c in train]
            tr = add_technical_indicators(tr, window=w)
            tr = simple_moving_average_strategy(tr, window=w)
            tr = backtest(tr)
            sr = sharpe_ratio(tr)
            if sr > best_sr:
                best_sr = sr
                best_w = w
        chosen.append(best_w)
        te = [c.copy() for c in test]
        te = add_technical_indicators(te, window=best_w)
        te = simple_moving_average_strategy(te, window=best_w)
        te = backtest(te, start_equity=equity)
        equity = te[-1]["equity"] if te else equity
        combined.extend(te)
    stats = performance_stats(combined)
    return chosen, combined, stats
