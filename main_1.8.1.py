
import streamlit as st
from strategy import run_strategy
from filters import get_filters, reset_filters, recommend_filters
from ui import render_strategy_box
from ibkr import connect_ibkr, create_combo_contract, send_combo_order
from datetime import datetime
import requests
import traceback

# ---------- API STATUS LIGHTS ----------
def check_tradier_status():
    try:
        resp = requests.get("https://api.tradier.com/v1/markets/clock", headers={"Authorization": f"Bearer {st.secrets['TRADIER_API_KEY']}"})
        return resp.status_code == 200
    except:
        return False

# ---------- CONNECT IBKR ----------
if 'ib' not in st.session_state:
    try:
        st.session_state.ib = connect_ibkr(timeout=10)
    except Exception as e:
        st.error(f"Unable to connect to IBKR: {e}")
        st.stop()

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title='Zero Gap System Tool v1.8.1', layout='centered')
st.title("Zero Gap System Tool (v1.8.1)")

# ---------- CONNECTION STATUS LIGHTS ----------
ib_connected = st.session_state.ib.isConnected()
tradier_connected = check_tradier_status()
ib_status = '🟢' if ib_connected else '🔴'
tradier_status = '🟢' if tradier_connected else '🔴'
st.markdown(f"**IBKR Connection**: {ib_status}  **Chart Data (Tradier)**: {tradier_status}")

# ---------- CONTROLS ----------
use_live = st.checkbox("Live IBKR Mode", value=False)
symbol = st.selectbox("Select Ticker", ['XSP'], key='symbol')
expiration = st.date_input("Choose Expiration Date", value=datetime.today())

# ---------- FILTERS ----------
filters = get_filters()
if st.button("Recommend Filters"):
    recommend_filters()
if st.button("Reset Filters"):
    reset_filters()

# ---------- STRATEGY RUN ----------
if st.button("Run Strategy"):
    try:
        st.session_state.results = run_strategy(filters, symbol, expiration)
        st.success("Strategy scan complete.")
    except Exception as e:
        st.error("Error running strategy.")
        st.exception(e)

# ---------- RESULTS DISPLAY ----------
if 'results' in st.session_state:
    spread, strangle = st.session_state.results
    st.markdown("### Recommended Spread Trade")
    render_strategy_box(spread, strategy_type='spread')
    if st.button("Send Spread to IBKR"):
        try:
            legs = spread['legs']
            credit = spread['credit']
            combo = create_combo_contract(symbol, expiration, legs)
            status = send_combo_order(combo, price=credit, transmit=use_live)
            st.success(f"Order submitted: {status}")
        except Exception as e:
            st.error("Combo error:")
            st.exception(e)

    st.markdown("### Recommended Strangle")
    render_strategy_box(strangle, strategy_type='strangle')
    if st.button("Send Strangle to IBKR"):
        try:
            legs = strangle['legs']
            cost = strangle['cost']
            combo = create_combo_contract(symbol, expiration, legs)
            status = send_combo_order(combo, price=cost, transmit=use_live)
            st.success(f"Order submitted: {status}")
        except Exception as e:
            st.error("Combo error:")
            st.exception(e)
