from typing import List, Dict

def _moving_average(values: List[float], window: int) -> List[float]:
    avg = []
    for i in range(len(values)):
        if i + 1 < window:
            avg.append(None)
        else:
            avg.append(sum(values[i - window + 1 : i + 1]) / window)
    return avg

def add_technical_indicators(candles: List[Dict], window: int = 14) -> List[Dict]:
    """Add SMA and RSI indicators to candle list."""
    closes = [c["close"] for c in candles]
    sma = _moving_average(closes, window)

    gains = [0.0]
    losses = [0.0]
    for i in range(1, len(closes)):
        change = closes[i] - closes[i - 1]
        gains.append(max(change, 0))
        losses.append(max(-change, 0))

    avg_gain = _moving_average(gains, window)
    avg_loss = _moving_average(losses, window)

    rsi = []
    for g, l in zip(avg_gain, avg_loss):
        if g is None or l is None or l == 0:
            rsi.append(None)
        else:
            rs = g / l
            rsi.append(100 - (100 / (1 + rs)))

    for candle, s, r in zip(candles, sma, rsi):
        candle[f"sma_{window}"] = s
        candle[f"rsi_{window}"] = r
    return candles

def add_bollinger_bands(candles: List[Dict], window: int = 20, num_std: float = 2.0) -> List[Dict]:
    """Add Bollinger Bands around an SMA."""
    closes = [c["close"] for c in candles]
    sma = _moving_average(closes, window)
    stds = []
    for i in range(len(closes)):
        if i + 1 < window:
            stds.append(None)
        else:
            segment = closes[i - window + 1 : i + 1]
            mean = sum(segment) / window
            var = sum((p - mean) ** 2 for p in segment) / window
            stds.append(var ** 0.5)
    for candle, m, s in zip(candles, sma, stds):
        if m is None or s is None:
            candle[f"bb_upper_{window}"] = None
            candle[f"bb_lower_{window}"] = None
        else:
            candle[f"bb_upper_{window}"] = m + num_std * s
            candle[f"bb_lower_{window}"] = m - num_std * s
    return candles

def add_macd(candles: List[Dict], fast: int = 12, slow: int = 26, signal: int = 9) -> List[Dict]:
    """Add MACD, signal line and histogram."""
    closes = [c["close"] for c in candles]

    def _ema(values: List[float], span: int) -> List[float]:
        ema = []
        k = 2 / (span + 1)
        prev = None
        for v in values:
            prev = v if prev is None else v * k + prev * (1 - k)
            ema.append(prev)
        return ema

    fast_ema = _ema(closes, fast)
    slow_ema = _ema(closes, slow)
    macd_line = [f - s for f, s in zip(fast_ema, slow_ema)]
    signal_line = _ema(macd_line, signal)
    hist = [m - s for m, s in zip(macd_line, signal_line)]
    for candle, m, s, h in zip(candles, macd_line, signal_line, hist):
        candle["macd"] = m
        candle["macd_signal"] = s
        candle["macd_hist"] = h
    return candles
