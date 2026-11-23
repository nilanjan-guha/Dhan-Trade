import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

st.set_page_config(
    page_title="AI QUANTUM INSTITUTIONAL TERMINAL | Trapped Trader Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Futuristic Digital LED HUD Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@600;800;900&family=Chakra+Petch:wght@500;700;800&display=swap');
    
    .stApp {
        background-color: #030712;
        color: #d1d5db;
        font-family: 'Share Tech Mono', monospace;
    }
    
    .digital-metric {
        font-family: 'Orbitron', sans-serif;
        font-size: 26px;
        font-weight: 900;
        letter-spacing: 1.5px;
    }
    
    .hud-box {
        background: rgba(11, 19, 38, 0.85);
        border: 1px solid #1e3a8a;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: inset 0 0 15px rgba(0, 240, 255, 0.05), 0 4px 15px rgba(0, 0, 0, 0.9);
    }
    
    .hud-header {
        font-family: 'Chakra Petch', sans-serif;
        font-size: 11px;
        text-transform: uppercase;
        color: #94a3b8;
        letter-spacing: 1px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    /* TRAP RADAR BANNER */
    .banner-trap-confirmed {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.25) 0%, rgba(3, 7, 18, 0.95) 100%);
        border: 2px solid #00ff88;
        border-radius: 10px;
        padding: 18px 24px;
        box-shadow: 0 0 35px rgba(0, 255, 136, 0.45);
        margin-bottom: 16px;
        animation: pulse 2s infinite;
    }

    .banner-chase-warn {
        background: linear-gradient(135deg, rgba(255, 0, 85, 0.2) 0%, rgba(3, 7, 18, 0.95) 100%);
        border: 2px solid #ff0055;
        border-radius: 10px;
        padding: 18px 24px;
        box-shadow: 0 0 30px rgba(255, 0, 85, 0.35);
        margin-bottom: 16px;
    }

    .badge-trap {
        font-family: 'Orbitron', sans-serif;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 1.5px;
        padding: 4px 12px;
        border-radius: 4px;
        background: #00ff88;
        color: #000;
    }

    .news-strip {
        background: #080f21;
        border: 1px solid #1e293b;
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 12px;
        color: #94a3b8;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 14px;
    }
</style>
""", unsafe_allow_html=True)

# 1. State Initializer
if "tick" not in st.session_state:
    st.session_state.tick = 0
st.session_state.tick += 1
t = st.session_state.tick

# 2. DATA MODEL WITH TRAPPED SELLER / BUYER RADAR
market = {
    "NIFTY": {
        "spot": round(25800.60 + np.sin(t * 0.4) * 6.5, 2),
        "spot_chg": "+286.30 (+1.12%)",
        "bias": "BULLISH TRAP REVERSAL",
        "pcr": 1.34,
        "pcr_tag": "BULLISH PUT SQUEEZE 🟢",
        "iv": 11.45,
        "vwap": 81.20,
        "atm": 25800,
        "active_strike": "25800 CALL (CE)",
        "current_ltp": round(84.50 + np.sin(t * 0.4) * 1.8, 2),
        "ideal_ob": 83.00,
        "max_chase": 87.00,
        "sl": 68.00,
        "tgt": 118.00,
        "delta": 0.538,
        "theta": -14.22,
        "gamma": 0.0013,
        "vega": 12.18,
        # TRAPPED TRADER SIGNALS
        "trap_type": "SELLER TRAP (BEAR TRAP) CONFIRMED",
        "trapped_volume": "184,500 CONTRACTS TRAPPED AT ₹82.00 - ₹83.00",
        "trap_mechanism": "Aggressive retail market sellers shorted into the Order Block (48K Bid Volume), but institutional limit buyers absorbed everything without letting price drop. Price swiftly reclaimed ₹84.50, triggering a massive Short Covering Squeeze!",
        "ladder": [
            {"Price": "₹118.0 [TP]", "Bid Vol": "18.2K", "Ask Vol": "62.5K", "Delta": "+44.3K", "OrderFlow Trapping State": "🟢 TARGET TAKE-PROFIT ZONE"},
            {"Price": "₹87.0 [CHASE CAP]", "Bid Vol": "24.5K", "Ask Vol": "52.0K", "Delta": "+27.5K", "OrderFlow Trapping State": "⚠️ DO NOT CHASE ABOVE THIS"},
            {"Price": "₹84.5 [LTP]", "Bid Vol": "42.0K", "Ask Vol": "95.5K", "Delta": "+53.5K", "OrderFlow Trapping State": "🔥 BUY TRIGGER: SELLERS PANIC CLOSING"},
            {"Price": "₹83.0 [TRAP POC]", "Bid Vol": "68.5K", "Ask Vol": "184.5K", "Delta": "+116.0K", "OrderFlow Trapping State": "🚨 184K SELLERS TRAPPED & ABSORBED"},
            {"Price": "₹81.5 [LOW WICK]", "Bid Vol": "52.0K", "Ask Vol": "12.0K", "Delta": "-40.0K", "OrderFlow Trapping State": "⚡ FAKE BREAKDOWN (TRAP FLOOR)"},
            {"Price": "₹68.0 [STRICT SL]", "Bid Vol": "72.0K", "Ask Vol": "18.0K", "Delta": "-54.0K", "OrderFlow Trapping State": "🔴 STRICT STOP LOSS (INVALIDATION)"}
        ],
        "chain": [
            {"Strike": "25700", "Type": "ITM", "Call LTP": "₹131.55", "Call OI": "42.5K", "Put LTP": "₹89.45", "Put OI": "128.4K", "Trapped Flow": "Institutions Defending 🛡️"},
            {"Strike": "25750", "Type": "ITM", "Call LTP": "₹106.10", "Call OI": "58.0K", "Put LTP": "₹114.90", "Put OI": "142.0K", "Trapped Flow": "Support Base 🛡️"},
            {"Strike": "25800", "Type": "ATM 🎯", "Call LTP": "₹83.45", "Call OI": "84.2K", "Put LTP": "₹141.75", "Put OI": "168.5K", "Trapped Flow": "🚨 184K SELLERS TRAPPED HERE"},
            {"Strike": "25850", "Type": "OTM", "Call LTP": "₹65.30", "Call OI": "112.0K", "Put LTP": "₹172.90", "Put OI": "95.0K", "Trapped Flow": "Next Resistance"},
            {"Strike": "25900", "Type": "OTM", "Call LTP": "₹50.60", "Call OI": "165.0K", "Put LTP": "₹211.55", "Put OI": "62.0K", "Trapped Flow": "Call Writers Wall 🧱"}
        ]
    },
    "BANKNIFTY": {
        "spot": round(64635.20 + np.cos(t * 0.3) * 22.0, 2),
        "spot_chg": "+1,572.20 (+2.49%)",
        "bias": "BULLISH TRAP SQUEEZE",
        "pcr": 1.28,
        "pcr_tag": "BULLISH SQUEEZE 🟢",
        "iv": 14.80,
        "vwap": 302.50,
        "atm": 64600,
        "active_strike": "64600 CALL (CE)",
        "current_ltp": round(312.00 + np.cos(t * 0.3) * 3.5, 2),
        "ideal_ob": 305.00,
        "max_chase": 322.00,
        "sl": 270.00,
        "tgt": 395.00,
        "delta": 0.512,
        "theta": -38.50,
        "gamma": 0.0008,
        "vega": 28.40,
        "trap_type": "SELLER TRAP (BEAR SQUEEZE)",
        "trapped_volume": "94,000 CONTRACTS TRAPPED AT ₹305.00",
        "trap_mechanism": "Sellers aggressively tried to dump at ₹305.00, but an 850K institutional limit order swallowed every contract. Price surged to ₹312.00, trapping shorts!",
        "ladder": [
            {"Price": "₹395.0 [TP]", "Bid Vol": "12.0K", "Ask Vol": "45.0K", "Delta": "+33.0K", "OrderFlow Trapping State": "🟢 TARGET CLUSTER"},
            {"Price": "₹322.0 [CHASE CAP]", "Bid Vol": "19.5K", "Ask Vol": "38.0K", "Delta": "+18.5K", "OrderFlow Trapping State": "⚠️ CHASE BARRIER"},
            {"Price": "₹312.0 [LTP]", "Bid Vol": "34.0K", "Ask Vol": "78.0K", "Delta": "+44.0K", "OrderFlow Trapping State": "🟢 BUY EXECUTION POINT"},
            {"Price": "₹305.0 [TRAP POC]", "Bid Vol": "48.0K", "Ask Vol": "142.0K", "Delta": "+94.0K", "OrderFlow Trapping State": "🚨 94K SELLERS TRAPPED & ABSORBED"},
            {"Price": "₹270.0 [STRICT SL]", "Bid Vol": "55.0K", "Ask Vol": "14.0K", "Delta": "-41.0K", "OrderFlow Trapping State": "🔴 STRICT STOP LOSS"}
        ],
        "chain": [
            {"Strike": "64400", "Type": "ITM", "Call LTP": "₹460.00", "Call OI": "28.0K", "Put LTP": "₹210.00", "Put OI": "85.0K", "Trapped Flow": "Defended 🛡️"},
            {"Strike": "64500", "Type": "ITM", "Call LTP": "₹385.00", "Call OI": "45.0K", "Put LTP": "₹275.00", "Put OI": "98.0K", "Trapped Flow": "Support Base 🛡️"},
            {"Strike": "64600", "Type": "ATM 🎯", "Call LTP": "₹310.00", "Call OI": "72.0K", "Put LTP": "₹355.00", "Put OI": "125.0K", "Trapped Flow": "🚨 SELLERS TRAPPED HERE"},
            {"Strike": "64700", "Type": "OTM", "Call LTP": "₹245.00", "Call OI": "95.0K", "Put LTP": "₹450.00", "Put OI": "68.0K", "Trapped Flow": "Resistance"},
            {"Strike": "64800", "Type": "OTM", "Call LTP": "₹190.00", "Call OI": "135.0K", "Put LTP": "₹560.00", "Put OI": "42.0K", "Trapped Flow": "Wall 🧱"}
        ]
    },
    "SENSEX": {
        "spot": round(83919.71 + np.sin(t * 0.25) * 30.0, 2),
        "spot_chg": "+897.96 (+1.08%)",
        "bias": "BULLISH TREND ACCUMULATION",
        "pcr": 1.22,
        "pcr_tag": "BULLISH 🟢",
        "iv": 12.10,
        "vwap": 378.00,
        "atm": 83900,
        "active_strike": "83900 CALL (CE)",
        "current_ltp": round(388.00 + np.sin(t * 0.25) * 4.0, 2),
        "ideal_ob": 380.00,
        "max_chase": 400.00,
        "sl": 320.00,
        "tgt": 515.00,
        "delta": 0.525,
        "theta": -42.00,
        "gamma": 0.0006,
        "vega": 32.00,
        "trap_type": "SELLER TRAP AT 83900 POC",
        "trapped_volume": "62,000 CONTRACTS TRAPPED AT ₹380.00",
        "trap_mechanism": "Aggressive retail sellers tried to short the day high rejection, but institutional iceberg bids absorbed them completely. Immediate squeeze to ₹388.00!",
        "ladder": [
            {"Price": "₹515.0 [TP]", "Bid Vol": "8.5K", "Ask Vol": "28.0K", "Delta": "+19.5K", "OrderFlow Trapping State": "🟢 TARGET LEVEL"},
            {"Price": "₹400.0 [CHASE CAP]", "Bid Vol": "14.0K", "Ask Vol": "29.0K", "Delta": "+15.0K", "OrderFlow Trapping State": "⚠️ CHASE BARRIER"},
            {"Price": "₹388.0 [LTP]", "Bid Vol": "26.0K", "Ask Vol": "62.0K", "Delta": "+36.0K", "OrderFlow Trapping State": "🟢 BUY EXECUTION POINT"},
            {"Price": "₹380.0 [TRAP POC]", "Bid Vol": "38.0K", "Ask Vol": "100.0K", "Delta": "+62.0K", "OrderFlow Trapping State": "🚨 62K SELLERS TRAPPED & ABSORBED"},
            {"Price": "₹320.0 [STRICT SL]", "Bid Vol": "42.0K", "Ask Vol": "11.0K", "Delta": "-31.0K", "OrderFlow Trapping State": "🔴 STRICT STOP LOSS"}
        ],
        "chain": [
            {"Strike": "83700", "Type": "ITM", "Call LTP": "₹525.00", "Call OI": "15.0K", "Put LTP": "₹280.00", "Put OI": "45.0K", "Trapped Flow": "Defended 🛡️"},
            {"Strike": "83800", "Type": "ITM", "Call LTP": "₹450.00", "Call OI": "22.0K", "Put LTP": "₹360.00", "Put OI": "52.0K", "Trapped Flow": "Support 🛡️"},
            {"Strike": "83900", "Type": "ATM 🎯", "Call LTP": "₹385.00", "Call OI": "38.0K", "Put LTP": "₹460.00", "Put OI": "65.0K", "Trapped Flow": "🚨 SELLERS TRAPPED HERE"},
            {"Strike": "84000", "Type": "OTM", "Call LTP": "₹310.00", "Call OI": "54.0K", "Put LTP": "₹575.00", "Put OI": "32.0K", "Trapped Flow": "Resistance"},
            {"Strike": "84100", "Type": "OTM", "Call LTP": "₹245.00", "Call OI": "78.0K", "Put LTP": "₹710.00", "Put OI": "18.0K", "Trapped Flow": "Wall 🧱"}
        ]
    }
}

# 3. NEWS FEED
news_stream = [
    "🚨 [TRAPPED SELLER RADAR]: 184,500 retail short contracts trapped in Nifty 25800 CE at ₹83.00 absorption POC.",
    "🔥 [DHANHQ ORDERFLOW FEED]: Short covering acceleration in progress; aggressive market buy delta surging.",
    "📊 [VWAP DEFENSE]: Active option premium is trading firmly above session VWAP (+₹3.30).",
    "🎯 [PCR INSIGHT]: Nifty PCR at 1.34 confirms Put writers are actively squeezing retail call short-sellers."
]
active_news = news_stream[t % len(news_stream)]

st.markdown(f"""
<div class="news-strip">
    <span style="background: #2563eb; color: #fff; padding: 2px 8px; border-radius: 4px; font-weight: 800; font-size: 11px;">TRAPPED TRADER RADAR</span>
    <span style="color: #cbd5e1;">{active_news}</span>
</div>
""", unsafe_allow_html=True)

# 4. SELECTOR
sel_idx = st.radio(
    "⚡ SELECT ACTIVE INSTITUTIONAL RADAR:",
    ["NIFTY", "BANKNIFTY", "SENSEX"],
    horizontal=True
)

d = market[sel_idx]
ltp = d["current_ltp"]
ob = d["ideal_ob"]
cap = d["max_chase"]

# 5. TRAPPED SELLER ACTION BANNER
st.markdown(f"""
<div class="banner-trap-confirmed">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                <span class="badge-trap">🚨 {d['trap_type']}</span>
                <span style="color: #00f0ff; font-weight: 800; font-size: 12px; letter-spacing: 1px;">
                    {d['trapped_volume']}
                </span>
            </div>
            <h1 style="margin: 0; font-family: 'Orbitron', sans-serif; font-size: 28px; color: #ffffff;">
                BUY {sel_idx} {d['active_strike']} (EXACT TRAP ENTRY)
            </h1>
            <div style="color: #bbf7d0; font-size: 13px; margin-top: 5px;">
                <b>Trap Logic:</b> {d['trap_mechanism']}
            </div>
        </div>
        <div style="display: flex; gap: 26px; margin-top: 6px;">
            <div style="text-align: right;">
                <div style="color: #94a3b8; font-size: 11px; font-weight: 700;">TRAP BUY ENTRY LTP</div>
                <div style="color: #ffffff; font-family: 'Orbitron', sans-serif; font-size: 28px; font-weight: 900;">₹{ltp:.2f}</div>
                <div style="color: #00f0ff; font-size: 11px;">Trap POC: ₹{ob:.2f}</div>
            </div>
            <div style="text-align: right;">
                <div style="color: #f43f5e; font-size: 11px; font-weight: 700;">MAX BUY CAP</div>
                <div style="color: #ff0055; font-family: 'Orbitron', sans-serif; font-size: 28px; font-weight: 900;">₹{cap:.2f}</div>
                <div style="color: #f43f5e; font-size: 11px;">Stop-Chase</div>
            </div>
            <div style="text-align: right;">
                <div style="color: #ef4444; font-size: 11px; font-weight: 700;">STRICT SL</div>
                <div style="color: #ef4444; font-family: 'Orbitron', sans-serif; font-size: 28px; font-weight: 900;">₹{d['sl']:.2f}</div>
                <div style="color: #94a3b8; font-size: 11px;">Below Trap Floor</div>
            </div>
            <div style="text-align: right;">
                <div style="color: #00ff88; font-size: 11px; font-weight: 700;">TARGET (TP)</div>
                <div style="color: #00ff88; font-family: 'Orbitron', sans-serif; font-size: 28px; font-weight: 900;">₹{d['tgt']:.2f}</div>
                <div style="color: #00f0ff; font-size: 11px;">Squeeze Peak</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. ROW 1: LIVE SPOT INDICES & VIX METRICS
r1, r2, r3, r4 = st.columns(4)
with r1:
    st.markdown(f"""
    <div class="hud-box" style="border-left: 4px solid #00ff88;">
        <div class="hud-header">NIFTY 50 (SPOT)</div>
        <div class="digital-metric" style="color: #fff;">{market['NIFTY']['spot']:.2f}</div>
        <div style="color: #00ff88; font-size: 11px;">▲ {market['NIFTY']['spot_chg']}</div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown(f"""
    <div class="hud-box" style="border-left: 4px solid #00f0ff;">
        <div class="hud-header">BANK NIFTY (SPOT)</div>
        <div class="digital-metric" style="color: #fff;">{market['BANKNIFTY']['spot']:.2f}</div>
        <div style="color: #00f0ff; font-size: 11px;">▲ {market['BANKNIFTY']['spot_chg']}</div>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown(f"""
    <div class="hud-box" style="border-left: 4px solid #a855f7;">
        <div class="hud-header">BSE SENSEX (SPOT)</div>
        <div class="digital-metric" style="color: #fff;">{market['SENSEX']['spot']:.2f}</div>
        <div style="color: #c084fc; font-size: 11px;">▲ {market['SENSEX']['spot_chg']}</div>
    </div>
    """, unsafe_allow_html=True)

with r4:
    st.markdown("""
    <div class="hud-box" style="border-left: 4px solid #f59e0b;">
        <div class="hud-header">INDIA VIX (VOLATILITY)</div>
        <div class="digital-metric" style="color: #f59e0b;">12.65</div>
        <div style="color: #94a3b8; font-size: 11px;">Stable IV | Short Covering Active</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# 7. ROW 2: ADVANCED GREEKS, PCR, VWAP, LEVEL 3 TRAP RADAR
g1, g2, g3, g4 = st.columns(4)

with g1:
    st.markdown(f"""
    <div class="hud-box">
        <div class="hud-header">OPTION GREEKS SPEEDOMETER</div>
        <div style="font-size: 13px; line-height: 1.6;">
            <div><b>DELTA:</b> <span style="color:#00ff88; font-weight:800;">{d['delta']}</span> (₹{(d['delta']*10):.1f} / 10pt move)</div>
            <div><b>THETA:</b> <span style="color:#f43f5e; font-weight:800;">{d['theta']} pts/day</span></div>
            <div><b>GAMMA:</b> <span style="color:#00f0ff;">{d['gamma']}</span> | <b>VEGA:</b> <span style="color:#a855f7;">{d['vega']}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with g2:
    st.markdown(f"""
    <div class="hud-box">
        <div class="hud-header">PCR & OPEN INTEREST (OI) RADAR</div>
        <div class="digital-metric" style="color:#00f0ff; font-size:20px;">PCR: {d['pcr']}</div>
        <div style="color:#00ff88; font-size:12px; font-weight:bold;">{d['pcr_tag']}</div>
        <div style="color:#94a3b8; font-size:11px; margin-top:2px;">Trapped Call Sellers Liquidating</div>
    </div>
    """, unsafe_allow_html=True)

with g3:
    vwap_diff = ltp - d['vwap']
    vwap_col = "#00ff88" if vwap_diff >= 0 else "#ff0055"
    st.markdown(f"""
    <div class="hud-box">
        <div class="hud-header">VWAP & IV EXPANSION RADAR</div>
        <div class="digital-metric" style="color:{vwap_col}; font-size:20px;">VWAP: ₹{d['vwap']:.2f}</div>
        <div style="color:{vwap_col}; font-size:12px; font-weight:bold;">
            {'ABOVE VWAP (+₹{:.2f}) 🟢'.format(vwap_diff) if vwap_diff >= 0 else 'BELOW VWAP 🔴'}
        </div>
        <div style="color:#94a3b8; font-size:11px;">IV: {d['iv']}% (Squeeze Expansion)</div>
    </div>
    """, unsafe_allow_html=True)

with g4:
    st.markdown(f"""
    <div class="hud-box">
        <div class="hud-header">TRAPPED SELLER DETECTOR</div>
        <div style="color:#00ff88; font-size:11px; font-weight:800;">🚨 TRAP DETECTED AT ₹{ob:.2f}</div>
        <div style="color:#94a3b8; font-size:11px; margin-top:4px;">Trapped Volume: <b style="color:#38bdf8;">{d['trapped_volume'].split(' AT')[0]}</b></div>
        <div style="color:#64748b; font-size:10px;">Absorption via Footprint Imbalance</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# 8. ROW 3: FOOTPRINT LADDER WITH TRAP SIGNALS & OPTION CHAIN WITH TRAPPED FLOW
col_l, col_r = st.columns([6, 6])

with col_l:
    st.subheader(f"⚡ Footprint Trap Microstructure ({sel_idx} {d['active_strike']})")
    st.caption("Price × Bid Vol × Ask Vol × Delta Imbalance × Trapping Zone Alert")
    st.dataframe(pd.DataFrame(d["ladder"]), use_container_width=True, height=270)

with col_r:
    st.subheader(f"🎯 Option Chain Matrix with Trapped Flow (ATM {d['atm']} ± Strikes)")
    st.caption("Call/Put LTP, Open Interest (OI), and Trapped Liquidity Status")
    st.dataframe(pd.DataFrame(d["chain"]), use_container_width=True, height=270)

# Refresh Loop (1.5 seconds) for live stream updates
time.sleep(1.5)
st.rerun()
