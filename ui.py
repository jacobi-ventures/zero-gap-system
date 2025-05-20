
import streamlit as st

def render_strategy_box(spread: dict, strangle: dict):
    """
    Render styled boxes for the recommended spread and strangle.
    spread: dict with keys 'sell_leg', 'buy_leg', 'credit', 'rr'
    strangle: dict with keys 'put_leg', 'call_leg', 'cost'
    """
    # Spread box
    if spread:
        st.subheader("Recommended Spread Trade")
        st.markdown(
            f"""<div style='background-color:#222;padding:15px;border-radius:10px;color:white'>
                <span style='color:red;font-weight:bold;'>Sell {spread['sell_leg']}</span><br>
                <span style='color:lightgreen;font-weight:bold;'>Buy {spread['buy_leg']}</span><br><br>
                <b>Credit:</b> ${spread['credit']} &nbsp;&nbsp;&nbsp; <b>R/R:</b> {spread['rr']}
            </div>""",
            unsafe_allow_html=True
        )

    # Strangle box
    if strangle:
        st.subheader("Recommended Strangle")
        st.markdown(
            f"""<div style='background-color:#222;padding:15px;border-radius:10px;color:white;margin-top:10px'>
                <span style='color:lightgreen;font-weight:bold;'>Buy {strangle['put_leg']}</span><br>
                <span style='color:lightgreen;font-weight:bold;'>Buy {strangle['call_leg']}</span><br><br>
                <b>Total Cost:</b> ${strangle['cost']}
            </div>""",
            unsafe_allow_html=True
        )
