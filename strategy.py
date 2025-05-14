
import requests
import pandas as pd

def get_option_chain(symbol, expiration, headers, base_url):
    url = f"{base_url}/markets/options/chains"
    params = {"symbol": symbol, "expiration": expiration, "greeks": "false"}
    r = requests.get(url, headers=headers, params=params)
    return pd.DataFrame(r.json()["options"]["option"])

def get_price(symbol, headers, base_url):
    url = f"{base_url}/markets/quotes"
    r = requests.get(url, headers=headers, params={"symbols": symbol})
    return r.json()["quotes"]["quote"]["last"]

def run_strategy_scan(symbol, expiration, filters, headers, base_url):
    df = get_option_chain(symbol, expiration, headers, base_url)
    price = get_price(symbol, headers, base_url)
    df["strike"] = df["strike"].astype(float)

    calls = df[df["option_type"] == "call"].copy()
    puts = df[df["option_type"] == "put"].copy()

    # Credit Spreads
    calls["partner"] = calls["strike"] + filters["cs_strike_gap"]
    spread_df = pd.merge(calls, calls[["strike", "bid", "ask", "symbol"]],
                         left_on="partner", right_on="strike", suffixes=("", "_buy"))
    spread_df["credit"] = spread_df["bid"] - spread_df["ask_buy"]
    spread_df = spread_df[
        (spread_df["credit"] >= filters["cs_min_credit"]) &
        (spread_df["credit"] <= filters["cs_max_credit"])
    ].copy()
    spread_df["rr_ratio"] = spread_df["credit"] / filters["cs_strike_gap"]
    top_spread = spread_df.sort_values("rr_ratio", ascending=False).head(1)

    # Strangles
    puts = puts[puts["strike"] < price - filters["str_min_dist"]]
    calls = calls[calls["strike"] > price + filters["str_min_dist"]]
    puts = puts.sort_values("strike", ascending=False).head(3)
    calls = calls.sort_values("strike", ascending=True).head(3)
    strangle_df = pd.merge(puts.assign(key=1), calls.assign(key=1), on="key", suffixes=("_put", "_call"))
    strangle_df["total_cost"] = strangle_df["ask_put"] + strangle_df["ask_call"]
    strangle_df = strangle_df[strangle_df["total_cost"] <= filters["str_max_cost"]]
    top_strangle = strangle_df.sort_values("total_cost").head(1)

    return top_spread, top_strangle
