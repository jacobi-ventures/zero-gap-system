# filters.py

import streamlit as st

def get_filters():
    """Return the default filter settings."""
    return {
        "cs_min_credit": {"min": 0.1, "max": 2.0, "value": 0.3, "help": "Min credit for credit spreads"},
        "cs_max_credit": {"min": 0.5, "max": 2.5, "value": 1.5, "help": "Max credit for credit spreads"},
        "cs_strike_gap": {"min": 1,   "max": 5,   "value": 2,   "step": 1, "help": "Strike gap between spread legs"},
        "str_min_dist":   {"min": 1,   "max": 20,  "value": 5,   "help": "Min OTM distance for strangles"},
        "str_max_cost":   {"min": 0.1, "max": 3.0, "value": 1.5, "help": "Max total cost for strangles"},
    }

def reset_filters():
    """Reset filters in session_state to defaults."""
    st.session_state.filters = get_filters()

def recommend_filters():
    """Apply recommended filter presets."""
    st.session_state.filters = {
        "cs_min_credit": {"min": 0.1, "max": 2.0, "value": 0.2},
        "cs_max_credit": {"min": 0.5, "max": 2.5, "value": 1.2},
        "cs_strike_gap": {"min": 1,   "max": 5,   "value": 1},
        "str_min_dist":   {"min": 1,   "max": 20,  "value": 3},
        "str_max_cost":   {"min": 0.1, "max": 3.0, "value": 1.0},
    }
def get_default_filters():
    return {
        "cs_min_credit": 0.3,
        "cs_max_credit": 1.5,
        "cs_strike_gap": 2,
        "str_min_dist": 5,
        "str_max_cost": 1.5
    }

def get_recommended_filters():
    return {
        "cs_min_credit": 0.2,
        "cs_max_credit": 1.2,
        "cs_strike_gap": 1,
        "str_min_dist": 3,
        "str_max_cost": 1.0
    }
