## Solana Sniper Bot

#### Description:
The Solana Sniper Bot aims to catch new pools on Raydium and Pumpfun, execute buy/sell transactions to make a profit. It allows for manual and automated trading, giving users the flexibility to optimize their strategies and maximize returns.

https://github.com/user-attachments/assets/bf3063e7-4eae-443a-bd04-544e65b3a25f

##### Mint: https://solscan.io/tx/QKbc9RxNZPE7peDNPnxBtPMux2HfTfn9QN2AwEr7Z5P1SS1qw42FYZcXqzkm9APVkTH88ieZU4PUaCU93yPNfGa
##### Buy: https://solscan.io/tx/5NV4oAJacFfNffAb55hkb6LEKsSTjgMd8vTzTvDKBLQvQ5XCogizBLShnpF89J8tqFrYJAHaUS5tmXtb6SBpEdNz
##### Sell: https://solscan.io/tx/5QDYSiST7KX9viNZXSeSATZYMJ5ioJrHJxqu9DVwFzREMarwwmaDXz7EYS1jC9oQq8z7V8GwTsEv94dSwdhU9s5b

#### Features:
- **Wallet Registration**: Register your own wallet for transactions.
- **Track New Pools on Raydium**: Monitor new pools and filter them based on SOL amount. Filter feature can be disabled, and if disabled, catch all pools.
- **Buy and Sell**: 
  - Manual buy and sell for each pool which tracked.
  - Show the status of buy/sell on every pools.
  - Auto buy and sell with specific amount, time delay, profit, and loss percentages.
  - Jito Mode: Execute transactions with Jito mode, allowing manual adjustment of Jito fees.

## Getting Started

To use this Solana Bot Package, you will need to have a basic understanding of Solana, Raydium, and automated trading. Follow the instructions below to get started:

1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/earthzetaorg/solana-sniper-bot
   ```
2. **Install Dependencies**:
   ```bash
   cd solana-sniper-bot
   npm install
   ```
3. **Configure Your Wallet**: Update the configuration file with your wallet details and desired settings.

4. **Run the Bots**:
     ```bash
     npm run start
     ```

## Configuration Guide

### Frontend Configuration
Update the following environment variables in your frontend `.env` file:

- `VITE_SERVER_URL=`: Set this to your backend server URL.
- `VITE_RPC_URL=`: Define your RPC URL.
- `VITE_DEV_RPC_URL=`: Define your development RPC URL.
- `VITE_PINATA_API_KEY=`: Set your Pinata API key.
- `VITE_PINATA_URL=`: Set your Pinata URL.

### Backend Configuration
Update the following environment variables in your backend `.env` file:

- `MONGO_URL=`: Your MongoDB URL.
- `RPC_ENDPOINT=`: Define your RPC endpoint.
- `WEBSOCKET_ENDPOINT=`: Define your WebSocket endpoint.
- `RPC_SUB_ENDPOINT=`: Define your RPC subscription endpoint.
- `WEBSOCKET_SUB_ENDPOINT=`: Define your WebSocket subscription endpoint.
- `DEV_NET_RPC=`: Define your development network RPC.
- `DEV_NET_WSS=`: Define your development network WebSocket.
- `DEV_NET_SUB_RPC=`: Define your development network subscription RPC.
- `DEV_NET_SUB_WSS=`: Define your development network subscription WebSocket.
- `LOG_LEVEL=info`: Set the log level.
- `BLOCKENGINE_URL=`: Define your BlockEngine URL.
- `JITO_FEE=`: Set your Jito fee.
- `JITO_KEY=`: Set your Jito key.
- `CHECK_IF_MINT_IS_MUTABLE=`: Set this to true or false to check if mint is mutable.
- `CHECK_IF_MINT_IS_BURNED=`: Set this to true or false to check if mint is burned.
- `CHECK_IF_MINT_IS_FROZEN=`: Set this to true or false to check if mint is frozen.
- `CHECK_IF_MINT_IS_RENOUNCED=`: Set this to true or false to check if mint is renounced.
- `COMMITMENT_LEVEL=`: Set the commitment level.
- `ORIGIN_URL=`: The frontend URL for allowing CORS.

If you have any questions or want more customized app for specific use cases, please feel free to contact me to below contacts.

## 👋 Contact Me

### 
Telegram:
###

## Analysis Pipeline (Experimental)

An experimental Python-based pipeline showcases data ingestion from Binance, simple feature engineering, a naive sentiment analyzer and a basic backtesting engine. Run the example to see a full workflow:

```bash
python -m analysis.example_pipeline
```

This is a starting point for integrating alternative data sources and advanced analytics into the trading stack. A lightweight
Solana RPC helper rotates across endpoints from providers such as Helius, QuickNode or public RPC nodes and falls back to
offline defaults if none respond.

The pipeline now also includes Bollinger Bands, MACD calculations and a simple volatility regime detector that adapts moving
average windows per regime for extra edge during backtests. A lightweight wallet
analysis helper fetches transaction histories, aggregates token interactions and
surfaces repeating patterns so KOL or insider wallets can be monitored for early
signals.

Recent enhancements showcase additional data dimensions for competitive edge:

- trade-based metrics such as Fibonacci retracements, cumulative volume delta and
  market-cap estimates via circulating supply fetches
- holder concentration summaries to spot whale dominance or distribution trends
- social-data aggregation across Twitter, Telegram, GitHub and news snippets to
  extract trending tokens or narratives
- wallet performance classification and ranking to highlight top traders versus
  underperformers
- KOL wallet scanner combining their recurring token patterns with social
  trends to surface mimic signals
- statistical price anomaly detection using z-scores to flag unusual moves
- topic extraction on aggregated social posts to surface emergent narratives
- grid-search optimizer that tunes regime-specific moving-average windows and
  reports metrics like Sharpe ratio, max drawdown and win rate for deeper
  backtest evaluations
- walk-forward analyzer that repeatedly optimizes SMA windows on rolling
  training sets and evaluates the best parameter out-of-sample for more robust
  backtests
- JSON cache for OHLCV and trade requests, enabling instant offline reuse of
  previously fetched market data
- cross-correlation analysis to spot leading relationships between price
  returns and social sentiment
- Hurst exponent calculation to gauge trend persistence versus
  mean-reversion

Run the example pipeline to see these analytics combined into a single flow.
