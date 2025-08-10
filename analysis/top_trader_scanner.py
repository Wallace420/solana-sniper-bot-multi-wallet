"""Tools to study and mimic behaviour of top performing wallets.

This module simulates tracking of well known KOL wallets on Solana and
extracts insights that can be used to adapt trading strategies.  The
functions operate in offline mode for deterministic examples but are
structured so that real RPC calls could be dropped in later.
"""

from typing import Any, Dict, List

from .wallet_analysis import (
    fetch_wallet_history,
    wallet_performance,
    detect_repeating_patterns,
)
from .trend_detection import extract_trending_tokens


def analyze_top_traders(wallets: List[str], offline: bool = True) -> Dict[str, Any]:
    """Collect stats and repeating patterns for a list of wallets.

    Parameters
    ----------
    wallets : List[str]
        Wallet addresses for known traders.
    offline : bool, optional
        When True, relies on deterministic sample data so the module works
        without network access.

    Returns
    -------
    Dict[str, Any]
        Mapping of wallet to history, performance metrics and detected
        token patterns.
    """

    histories = {w: fetch_wallet_history(w, offline=offline) for w in wallets}
    performance = {w: wallet_performance(h) for w, h in histories.items()}
    patterns = {w: detect_repeating_patterns(h) for w, h in histories.items()}
    return {"histories": histories, "performance": performance, "patterns": patterns}


def mimic_strategy(trader_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Propose a simple action based on a trader's dominant token activity."""

    totals: Dict[str, float] = {}
    for tx in trader_history:
        token = tx.get("token")
        amt = tx.get("amount", 0)
        if token:
            totals[token] = totals.get(token, 0.0) + amt
    if not totals:
        return {}
    # Choose token with the highest absolute net flow
    token = max(totals, key=lambda t: abs(totals[t]))
    action = "buy" if totals[token] > 0 else "sell"
    return {"token": token, "action": action}


def scan_market_with_kols(wallets: List[str], posts: List[Dict[str, str]]) -> Dict[str, Any]:
    """Combine KOL wallet patterns with social trends to surface signals.

    This emulates features from dashboards like GMGN or Axiom where
    trades of influential wallets are intersected with trending tokens.
    """

    trader_info = analyze_top_traders(wallets)
    trending = extract_trending_tokens(posts)
    signals: Dict[str, int] = {}
    for patterns in trader_info["patterns"].values():
        for token in patterns:
            if token in trending:
                signals[token] = signals.get(token, 0) + 1
    ranked = sorted(signals, key=signals.get, reverse=True)
    return {"trader_info": trader_info, "trending": trending, "signals": ranked}
