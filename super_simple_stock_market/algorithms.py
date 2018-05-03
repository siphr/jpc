import math

import super_simple_stock_market.exceptions as exceptions


def calculate_gcbe_all_share_index(stocks: list) -> float:
    """
    Calculate GCBE All Share Index.

    Parameters:
        stocks: A list of Stock instances.

    Return:
        A floating point number representing the index.

    Exceptions:
        e_sssm_gcbe_all_share_index_empty_stock_list:
        If the provided stock list is empty.

        e_sssm_gcbe_all_share_index_calculation_failed:
        If there was some other issue during calculations.

    References:
        Document Section 2.b
        Table 2 Row 3
    """
    if len(stocks) == 0:
        raise exceptions.e_sssm_gcbe_all_share_index_empty_stock_list

    price_product = 1
    try:
        for stock in stocks:
            price_product = price_product * stock.calculate_volume_weighted_price()

        geometric_mean = math.pow(price_product, 1/len(stocks))
    except Exception as e:
        raise exceptions.e_sssm_gcbe_all_share_index_calculation_failed from e

    return geometric_mean
