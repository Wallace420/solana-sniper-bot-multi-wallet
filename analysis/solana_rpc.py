import os
import json
from typing import Any, List, Optional
from urllib.request import Request, urlopen

# Default public RPC endpoints that do not require API keys
DEFAULT_ENDPOINTS = [
    "https://api.mainnet-beta.solana.com",
    "https://solana-api.projectserum.com",
    "https://rpc.ankr.com/solana",
]


def _build_endpoints() -> List[str]:
    """Collect RPC endpoints from environment variables with public fallbacks."""
    endpoints: List[str] = []
    helius = os.getenv("HELIUS_RPC")
    if helius:
        endpoints.append(helius)
    quicknode = os.getenv("QUICKNODE_RPC")
    if quicknode:
        endpoints.append(quicknode)
    nextblock = os.getenv("NEXTBLOCK_RPC")
    if nextblock:
        endpoints.append(nextblock)
    endpoints.extend(DEFAULT_ENDPOINTS)
    return endpoints


def rpc_call(method: str, params: Optional[List[Any]] = None, endpoints: Optional[List[str]] = None) -> Any:
    """Send a JSON-RPC request to the first healthy Solana endpoint.

    The function iterates through provided endpoints (or defaults) until one
    succeeds. If all endpoints fail, a minimal offline fallback is returned for
    a few common methods to keep pipelines functional without network access.
    """
    if params is None:
        params = []
    urls = endpoints or _build_endpoints()
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    headers = {"Content-Type": "application/json"}
    for url in urls:
        try:
            req = Request(url, data=payload, headers=headers)
            with urlopen(req, timeout=10) as resp:
                data = json.load(resp)
            if "result" in data:
                return data["result"]
        except Exception:
            continue
    # Offline fallbacks for a couple of common methods
    if method in {"getSlot", "getBlockHeight", "getBalance"}:
        return 0
    return None
