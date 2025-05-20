
import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from strategy import run_strategy
from filters import get_filters, reset_filters, recommend_filters
from ui import render_strategy_box
from ibkr import create_combo_contract, send_combo_order

st.set_page_config(page_title="Zero Gap Tool (v1.7.5)", layout="centered")
load_dotenv()

st.title("Zero Gap System Tool (v1.7.5)")

# UI for symbol and expiration (default expiration today)
symbol = st.selectbox("Select Ticker", ["XSP","SPX","QQQ","IWM","TSLA"], key="order_symbol")
expiration = datetime.now().strftime("%Y%m%d")

# Initialize session state
if "filters" not in st.session_state:
    st.session_state.filters = get_filters()
if "last_combo" not in st.session_state:
    st.session_state.last_combo = None
if "last_price" not in st.session_state:
    st.session_state.last_price = None

# Filter controls
col1, col2 = st.columns(2)
with col1:
    if st.button("Reset Filters"):
        reset_filters()
        st.rerun()
with col2:
    if st.button("Recommend Filters"):
        recommend_filters()
        st.rerun()

# Render sliders
for key, val in st.session_state.filters.items():
    minv, maxv, default = val["min"], val["max"], val["value"]
    step = val.get("step", 1 if isinstance(minv, int) and isinstance(maxv, int) else 0.1)
    st.slider(
        label=key.replace("_", " ").title(),
        min_value=minv,
        max_value=maxv,
        value=default,
        step=step,
        key=key,
        help=val.get("help", "")
    )

# Run strategy scan
if st.button("Run Strategy Scan"):
    spread, strangle = run_strategy(st.session_state.filters)
    render_strategy_box(spread, strangle)

    # Prepare combo if valid
    if spread and strangle:
        # parse legs
        def parse_leg(leg_str):
            parts = leg_str.split()
            s_cp = parts[-1]
            return float(s_cp[:-1]), s_cp[-1]

        sell_strike, sell_right = parse_leg(spread["sell_leg"])
        buy_strike, buy_right   = parse_leg(spread["buy_leg"])
        put_strike, put_right   = parse_leg(strangle["put_leg"])
        call_strike, call_right = parse_leg(strangle["call_leg"])

        spreads = [
            {"strike": sell_strike, "right": sell_right, "action": "SELL"},
            {"strike": buy_strike,  "right": buy_right,  "action": "BUY"}
        ]
        strangles = [
            {"strike": put_strike,  "right": put_right,  "action": "BUY"},
            {"strike": call_strike, "right": call_right, "action": "BUY"}
        ]
        legs = spreads + strangles

        # Create combo and store
        try:
            combo = create_combo_contract(symbol, expiration, legs)
            st.session_state.last_combo = combo
            st.session_state.last_price = spread["credit"]
            st.success("Combo prepared and ready to send.")
        except Exception as e:
            st.error(f"Error preparing combo: {e}")

# Persistent send to IBKR button
if st.session_state.last_combo:
    st.markdown("### Ready to Send to IBKR")
    if st.button("Send to IBKR (Paper Test)", key="send_ibkr"):
        try:
            status = send_combo_order(
                st.session_state.last_combo,
                price=st.session_state.last_price,
                dry_run=True
            )
            st.success(f"IBKR Order Status: {status}")
        except Exception as e:
            st.error(f"IBKR Error: {e}")
