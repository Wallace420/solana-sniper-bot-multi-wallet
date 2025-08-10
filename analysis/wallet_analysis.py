from typing import Any, Dict, List

from .solana_rpc import rpc_call


def fetch_wallet_history(address: str, limit: int = 20, offline: bool = True) -> List[Dict[str, Any]]:
    """Fetch recent transaction signatures for a wallet address.

    When ``offline`` is True, returns a deterministic sample so examples run
    without network access. Otherwise, it queries the Solana RPC using
    ``getSignaturesForAddress`` and falls back to the sample on failure.
    """
    params = [address, {"limit": limit}]
    if not offline:
        result = rpc_call("getSignaturesForAddress", params)
        if result:
            return result
    # Offline sample with token hints for pattern detection
    sample: List[Dict[str, Any]] = []
    tokens = ["OG", "KOL"]
    for i in range(limit):
        sample.append(
            {
                "signature": f"offline_sig_{i}",
                "slot": i,
                "token": tokens[i % len(tokens)],
                "amount": (-1) ** i,
            }
        )
    return sample


def aggregate_wallet_stats(history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute simple statistics about wallet activity."""
    total = len(history)
    token_counts: Dict[str, int] = {}
    for h in history:
        token = h.get("token")
        if token:
            token_counts[token] = token_counts.get(token, 0) + 1
    return {"tx_count": total, "token_counts": token_counts}


def detect_repeating_patterns(history: List[Dict[str, Any]]) -> List[str]:
    """Return tokens that appear multiple times as naive repeating patterns."""
    counts: Dict[str, int] = {}
    for h in history:
        token = h.get("token")
        if token:
            counts[token] = counts.get(token, 0) + 1
    return [t for t, c in counts.items() if c > 1]


def scan_addresses_for_patterns(addresses: List[str], reference_tokens: List[str]) -> Dict[str, List[str]]:
    """Check other addresses for overlap with reference token patterns."""
    matches: Dict[str, List[str]] = {}
    for addr in addresses:
        hist = fetch_wallet_history(addr)
        tokens = detect_repeating_patterns(hist)
        overlap = [t for t in tokens if t in reference_tokens]
        if overlap:
            matches[addr] = overlap
    return matches


def wallet_performance(history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Classify wallet performance by aggregated amount."""

    pnl = sum(h.get("amount", 0) for h in history)
    classification = "top_trader" if pnl > 0 else "loser"
    return {"pnl": pnl, "classification": classification}


def rank_wallets(histories: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[str]]:
    """Return top and bottom wallets based on PnL."""

    scores = {addr: wallet_performance(h)["pnl"] for addr, h in histories.items()}
    sorted_addrs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top = [addr for addr, _ in sorted_addrs[:3]]
    bottom = [addr for addr, _ in sorted_addrs[-3:]]
    return {"top": top, "bottom": bottom}
