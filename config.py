# Dhan API Configuration
DHAN_CLIENT_ID = "1100857857"
DHAN_ACCESS_TOKEN = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJwYXJ0bmVySWQiOiIiLCJkaGFuQ2xpZW50SWQiOiIxMTAwODU3ODU3Iiwid2ViaG9va1VybCI6IiIsImlzcyI6ImRoYW4iLCJleHAiOjE3OTY2NjY0NTZ9.wAAepke39nNh3GazGnL5tRsJDor_kJDq0f5-Pu7DE-h755B3_uMlRJt1DQmvrN5rcgqCVzPjKOl_K-WcRKJ3aw"

# Mode: Set True for Sandbox testing, False for Live trading
USE_SANDBOX = True

# Trading Configurations
INDEX_NAME = "NIFTY"  # Options: "NIFTY", "BANKNIFTY", "SENSEX"
NUM_STRIKES_ITM = 3
NUM_STRIKES_OTM = 3

# Strategy Parameters
CANDLE_TIMEFRAME_MINUTES = 5
IMBALANCE_RATIO = 2.5
RISK_REWARD_RATIO = 2.0
SL_POINTS = 15
DELTA_ENTRY_THRESHOLD = 2500  # Delta required to trigger aggressive orderflow buy/sell signal
