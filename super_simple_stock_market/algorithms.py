import math


def calculate_gcbe_all_share_index(stocks: list) -> float:
    """
    Calculate GCBE All Share Index.

    Parameters:
        stocks: A list of Stock instances.

    Return:
        A floating point number representing the index.

    References:
        Document Section 2.b
        Table 2 Row 3
    """
    price_product = 1
    for stock in stocks:
        price_product = price_product * stock.calculate_volume_weighted_price()

    geometric_mean = math.pow(price_product, 1/len(stocks))
    return geometric_mean
