# Dhan Orderflow & Trapped Trader AI Terminal

An institutional-grade **Orderflow, Footprint, and Smart Money Concepts (SMC)** trading bot & live HUD terminal built with **DhanHQ API (v2)**.

## 🚀 Key Features

- **Trapped Trader Detection**: Real-time detection of aggressive retail sellers shorting into institutional Order Blocks, identifying the exact absorption Point of Control (POC) and short-covering squeezes.
- **Dynamic Anti-Chase Protection**: Protects against buying extended tops. If a premium runs above the maximum buy threshold, the system triggers an immediate warning: `⚠️ DO NOT CHASE - RUNAWAY`.
- **Multi-Index Second-by-Second Radar**: Continuously scans **NIFTY 50**, **BANK NIFTY**, and **BSE SENSEX** with Market Structure analysis (BOS / FVG / CHoCH) and Cumulative Volume Delta (CVD).
- **Institutional Option Greeks**: Live Delta, Gamma, Theta (daily decay), and Vega sensitivity tracking.
- **Level 3 Market Depth & Iceberg Detector**: Uncovers large resting limit orders and detects spoofing.
- **ATM ± 3 Strikes Option Chain Matrix**: Full chain coverage with Strike OI, PCR, Delta, and Trapped Flow indicators.

---

## 🛠️ Project Structure

```
.
├── config.py           # Dhan client ID, token & risk settings
├── app_ui.py           # Futuristic Streamlit Digital LED HUD Terminal
├── main_bot.py         # Autonomous Execution & Signal Engine
├── orderflow_smc.py    # Footprint Price-Ladder Engine & SMC Analyzer
├── strike_selector.py  # Dynamic ATM ± 3 Strikes Selector
└── README.md
```

---

## ⚡ Quickstart

1. **Install Dependencies:**
   ```bash
   pip install dhanhq streamlit plotly pandas numpy requests websockets
   ```

2. **Configure Credentials:**
   Edit `config.py` with your Dhan Client ID and Access Token:
   ```python
   DHAN_CLIENT_ID = "YOUR_CLIENT_ID"
   DHAN_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
   ```

3. **Launch the Live Terminal:**
   ```bash
   python -m streamlit run app_ui.py
   ```
   Open `http://localhost:8501` in your browser.
