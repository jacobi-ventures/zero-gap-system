
import streamlit as st
from datetime import datetime

def format_leg(symbol):
    try:
        root = symbol[:3]
        date = datetime.strptime(symbol[3:9], "%y%m%d").strftime("%b %d")
        strike = str(float(symbol[13:]) / 1000)
        call_put = "C" if "C" in symbol else "P"
        return f"{root} {date} {strike}{call_put}"
    except:
        return symbol

def render_strategy_results(top_spread, top_strangle):
    if not top_spread.empty:
        top = top_spread.iloc[0]
        sell_leg = format_leg(top["symbol"])
        buy_leg = format_leg(top["symbol_buy"])
        credit = round(top["credit"], 2)
        rr = round(top["rr_ratio"], 2)

        html_box = f'''
        <div style="background-color:#222;padding:15px;border-radius:10px;color:white">
            <span style="color:red;font-weight:bold;">Sell {sell_leg}</span><br>
            <span style="color:lightgreen;font-weight:bold;">Buy {buy_leg}</span><br><br>
            <b>Credit:</b> ${credit} &nbsp;&nbsp;&nbsp; <b>R/R:</b> {rr}
        </div>
        '''
        st.markdown(html_box, unsafe_allow_html=True)

    if not top_strangle.empty:
        row = top_strangle.iloc[0]
        call_leg = format_leg(row["symbol_call"])
        put_leg = format_leg(row["symbol_put"])
        total = round(row["total_cost"], 2)

        html_box = f'''
        <div style="background-color:#222;padding:15px;border-radius:10px;color:white;margin-top:10px">
            <span style="color:lightgreen;font-weight:bold;">Buy {put_leg}</span><br>
            <span style="color:lightgreen;font-weight:bold;">Buy {call_leg}</span><br><br>
            <b>Total Strangle Cost:</b> ${total}
        </div>
        '''
        st.markdown(html_box, unsafe_allow_html=True)
