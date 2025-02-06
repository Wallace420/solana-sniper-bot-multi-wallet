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
Telegram: https://t.me/earthzeta
###
<div style={{display:flex; justify-content:space-evenly}}> 
    <a href="https://t.me/earthzeta" target="_blank"><img alt="Telegram"
        src="https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white"/></a>
    <a href="https://discordapp.com/users/339619501081362432" target="_blank"><img alt="Discord"
        src="https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white"/></a>    
</div>
