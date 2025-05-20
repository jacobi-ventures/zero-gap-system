
import pandas as pd

def run_strategy(filters):
    """
    Stub strategy: returns dummy spread and strangle with slippage & fill_score.
    Replace with real Tradier logic later.
    """
    # Dummy spread data
    spread = {
        "sell_leg": "XSP May 14 584C",
        "buy_leg":  "XSP May 14 586C",
        "credit":   1.46,
        "rr":       0.73,
        "slippage": 0.05,
        "fill_score": 0.8
    }

    # Dummy strangle data
    strangle = {
        "put_leg":  "XSP May 14 580P",
        "call_leg": "XSP May 14 590C",
        "cost":     0.75,
        "slippage": 0.03,
        "fill_score": 0.85
    }

    return spread, strangle
