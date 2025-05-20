import asyncio
import os

# Patch for Python 3.13+ where threads don't have a default event loop
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from ib_insync import IB, Contract, ComboLeg, LimitOrder

_ib_client = None

def connect_ibkr(host='127.0.0.1', port=7497, client_id=1, timeout=10):
    global _ib_client
    if _ib_client is None or not _ib_client.isConnected():
        _ib_client = IB()
        _ib_client.connect(host, port, clientId=client_id, timeout=timeout)
    return _ib_client

def create_combo_contract(symbol, expiration, legs):
    ib = connect_ibkr()
    con_ids = []
    for leg in legs:
        c = Contract()
        c.symbol = symbol
        c.secType = "OPT"
        c.exchange = "SMART"
        c.currency = "USD"
        c.lastTradeDateOrContractMonth = expiration
        c.strike = leg["strike"]
        c.right = leg["right"]
        qualified = ib.qualifyContracts(c)
        if not qualified:
            raise ValueError(f"Could not qualify contract: {c}")
        con_ids.append(qualified[0].conId)

    combo = Contract()
    combo.symbol = symbol
    combo.secType = "BAG"
    combo.currency = "USD"
    combo.exchange = "SMART"
    combo.comboLegs = [
        ComboLeg(conId=con_ids[i], ratio=1, action=legs[i]["action"],
                 exchange="SMART") for i in range(len(legs))
    ]
    return combo

def send_combo_order(combo, price, live=False):
    ib = connect_ibkr()
    order = LimitOrder("BUY", 1, price, transmit=live)
    trade = ib.placeOrder(combo, order)
    return trade.orderStatus.status
