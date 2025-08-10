"""Example pipeline demonstrating various data and analytics capabilities."""

from .data_ingestion import (
    fetch_ohlcv,
    fetch_trades,
    fetch_token_supply,
    fetch_social_posts,
)
from .feature_engineering import (
    add_bollinger_bands,
    add_macd,
)
from .nlp_analysis import simple_sentiment_score, extract_topics
from .backtesting import (
    optimize_regime_windows,
    performance_stats,
    walk_forward_optimize,
)
from .solana_rpc import rpc_call
from .wallet_analysis import (
    fetch_wallet_history,
    aggregate_wallet_stats,
    detect_repeating_patterns,
    wallet_performance,
    rank_wallets,
)
from .advanced_metrics import (
    market_cap,
    fee_summary,
    fibonacci_retracements,
    cumulative_volume_delta,
    holder_distribution,
    zscore_anomalies,
)
from .trend_detection import extract_trending_tokens
from .top_trader_scanner import mimic_strategy, scan_market_with_kols
from .innovative_analysis import cross_correlation_lag, hurst_exponent
from .alternative_data import analyze_github_trend

if __name__ == "__main__":
    raw = fetch_ohlcv(limit=300)
    # second call demonstrates cache retrieval
    _ = fetch_ohlcv(limit=300)
    params, data, sr = optimize_regime_windows(
        raw, low_windows=[20, 30, 40], high_windows=[5, 10, 15]
    )
    data = add_bollinger_bands(data)
    data = add_macd(data)
    stats = performance_stats(data)
    print("Optimized regime windows:", params)
    print("Performance stats:", stats)
    print("Last candles:")
    for row in data[-5:]:
        print(row)

    # Walk-forward optimization using simple SMA strategy
    wf_windows, wf_data, wf_stats = walk_forward_optimize(
        raw, train_size=100, test_size=50, windows=[5, 10, 20, 30]
    )
    print("Walk-forward windows per fold:", wf_windows)
    print("Walk-forward performance:", wf_stats)

    # Advanced metrics
    trades = fetch_trades(limit=50)
    _ = fetch_trades(limit=50)
    cvd_series = cumulative_volume_delta(trades)
    fibs = fibonacci_retracements([d["close"] for d in data])
    supply = fetch_token_supply("BTC")
    mc = market_cap(data[-1]["close"], supply)
    holder_stats = holder_distribution({"W1": 100, "W2": 50, "W3": 10})
    anomalies = zscore_anomalies([d["close"] for d in data])
    print("Fibonacci levels:", fibs)
    print("CVD last value:", cvd_series[-1] if cvd_series else 0)
    print("Market Cap estimate:", mc)
    print("Holder stats:", holder_stats)
    print("Price anomalies at indices:", anomalies)

    text = "Bitcoin sees bullish increase despite earlier loss"
    print("Sentiment score:", simple_sentiment_score(text))
    slot = rpc_call("getSlot")
    print("Latest Solana slot:", slot)

    history = fetch_wallet_history("DemoWallet1111111111111111111111111111111")
    stats = aggregate_wallet_stats(history)
    patterns = detect_repeating_patterns(history)
    perf = wallet_performance(history)
    rankings = rank_wallets({"demo": history, "other": fetch_wallet_history("OtherWallet" )})
    print("Wallet stats:", stats)
    print("Detected wallet patterns:", patterns)
    print("Wallet performance:", perf)
    print("Wallet rankings:", rankings)

    posts = fetch_social_posts()
    trending = extract_trending_tokens(posts)
    topics = extract_topics([p["text"] for p in posts])
    print("Trending tokens from social posts:", trending)
    print("Extracted social topics:", topics)

    gh_trend = analyze_github_trend("bitcoin/bitcoin")
    print("GitHub star growth:", gh_trend["star_growth"])

    sent_series = [simple_sentiment_score(p["text"]) for p in posts]
    returns = [data[i]["close"] - data[i - 1]["close"] for i in range(1, len(data))]
    lag, corr = cross_correlation_lag(returns[: len(sent_series)], sent_series)
    print("Return/sentiment best lag:", lag, "corr:", corr)
    hurst = hurst_exponent([d["close"] for d in data])
    print("Hurst exponent:", hurst)

    # KOL wallet analysis combined with social trends
    kol_wallets = [
        "CupseyWallet1111111111111111111111111111111",
        "OrangieWallet11111111111111111111111111111",
        "KingWallet11111111111111111111111111111111",
        "CentedWallet11111111111111111111111111111",
    ]
    market_view = scan_market_with_kols(kol_wallets, posts)
    print("KOL performance:", market_view["trader_info"]["performance"])
    print("KOL signals:", market_view["signals"])
    sample_history = market_view["trader_info"]["histories"][kol_wallets[0]]
    print("Mimic strategy:", mimic_strategy(sample_history))
