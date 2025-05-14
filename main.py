
import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from filters import get_default_filters, get_recommended_filters
from strategy import run_strategy_scan
from ui import render_strategy_results

st.set_page_config(page_title="Zero Gap Tool 1.6.3", layout="centered")

# === VERSION LOG ===
st.sidebar.title("Zero Gap System Tool — Version 1.6.3")
st.sidebar.markdown(
    """**Version History**

**1.6.3 (Current)**
- Added helper text next to each filter to explain its purpose

**1.6.2**
- Replaced deprecated rerun method
- Explained and logged recommended filter logic

**1.6.1**
- Styled strategy display boxes restored
- Added Reset Filters and Recommend Filters buttons
- IBKR Simulation button added
- Version history restored

**1.5**
- Simultaneous Spread + Strangle strategy logic
- Independent filters per strategy
- API Status indicator

**1.4**
- Added filter diagnostics when no trades are shown
- Toggle to disable slippage + fill filters
- Display count of total vs. filtered trades

**1.3**
- Added trade/export logging
- Version history sidebar

**1.2**
- Added slippage tolerance enforcement
- Added fill probability scoring

**1.1**
- IBKR paper trade simulation module
- Dark mode, clean option formatting
""",
    unsafe_allow_html=True
)

# === API SETUP ===
load_dotenv()
API_KEY = os.getenv("TRADIER_API_KEY", "s79AiKlnnbAjnSgYkkWuAwC9DnLV")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}
BASE_URL = "https://api.tradier.com/v1"

@st.cache_data(ttl=60)
def check_api_status():
    try:
        r = requests.get(f"{BASE_URL}/markets/quotes", headers=HEADERS, params={"symbols": "SPY"})
        if r.status_code == 200:
            return "Live" if "quotes" in r.json() else "Delayed"
        return "Disconnected"
    except:
        return "Disconnected"

status = check_api_status()
status_color = {"Live": "green", "Delayed": "orange", "Disconnected": "red"}[status]
st.sidebar.markdown(f"**API Status:** <span style='color:{status_color}'>{status}</span>", unsafe_allow_html=True)

st.title("Zero Gap Strategy Tool (1.6.3)")

symbol = st.selectbox("Select Ticker", ["XSP", "SPX", "QQQ", "IWM", "TSLA"])

def get_expirations(sym):
    url = f"{BASE_URL}/markets/options/expirations"
    params = {"symbol": sym, "includeAllRoots": "true", "strikes": "false"}
    r = requests.get(url, headers=HEADERS, params=params)

    if r.status_code != 200:
        st.error(f"Failed to get expirations for {sym}. Status code: {r.status_code}")
        return []

    try:
        return r.json().get("expirations", {}).get("date", [])
    except requests.exceptions.JSONDecodeError:
        st.error(f"API returned no data or invalid response for {sym}.")
        return []

expirations = get_expirations(symbol)
chosen_exp = st.selectbox("Choose Expiration Date", expirations)

filters = st.session_state.get("filters", get_default_filters())

def reset_filters():
    st.session_state.filters = get_default_filters()

def recommend_filters():
    st.session_state.filters = get_recommended_filters()

# === FILTER SLIDERS ===
st.subheader("Credit Spread Filters")

st.slider("Min Credit", 0.1, 2.0, filters["cs_min_credit"], key="cs_min_credit",
          help="Minimum credit received when selling a credit spread.")
st.slider("Max Credit", 0.3, 2.5, filters["cs_max_credit"], key="cs_max_credit",
          help="Maximum acceptable credit to avoid high risk or illiquidity.")
st.slider("Strike Gap", 1, 5, filters["cs_strike_gap"], key="cs_strike_gap",
          help="The gap between sold and bought strike prices in the spread.")

st.subheader("Strangle Filters")

st.slider("Min Distance from Price", 1, 20, filters["str_min_dist"], key="str_min_dist",
          help="Minimum number of points OTM for both strangle legs.")
st.slider("Max Total Cost", 0.2, 4.0, filters["str_max_cost"], key="str_max_cost",
          help="Maximum amount you're willing to pay for the strangle.")

col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Reset Filters"):
        reset_filters()
        st.rerun()
with col2:
    if st.button("🎯 Recommend Filters"):
        recommend_filters()
        st.rerun()

run_scan = st.button("Run Strategy Scan")

if run_scan:
    updated_filters = {
        "cs_min_credit": st.session_state.cs_min_credit,
        "cs_max_credit": st.session_state.cs_max_credit,
        "cs_strike_gap": st.session_state.cs_strike_gap,
        "str_min_dist": st.session_state.str_min_dist,
        "str_max_cost": st.session_state.str_max_cost
    }

    top_spread, top_strangle = run_strategy_scan(
        symbol,
        chosen_exp,
        updated_filters,
        HEADERS,
        BASE_URL
    )

    st.subheader("Recommended Strategy (Combined)")
    render_strategy_results(top_spread, top_strangle)
