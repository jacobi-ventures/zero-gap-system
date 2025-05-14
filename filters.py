
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
