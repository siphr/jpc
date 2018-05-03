"""
All module exceptions.
"""


class e_sssm_exception(Exception):
    pass


class e_sssm_fixed_dividend_unavailable(e_sssm_exception):
    pass


class e_sssm_trade_record_buy_failed(e_sssm_exception):
    pass


class e_sssm_trade_record_sell_failed(e_sssm_exception):
    pass


class e_sssm_trade_record_empty(e_sssm_exception):
    pass


class e_sssm_gcbe_all_share_index_empty_stock_list(e_sssm_exception):
    pass


class e_sssm_gcbe_all_share_index_calculation_failed(e_sssm_exception):
    pass

