import math


def calculate_gcbe_all_share_index(stocks: list):
    price_product = 1
    for stock in stocks:
        price_product = price_product * stock.calculate_volume_weighted_price()

    geometric_mean = math.pow(price_product, 1/len(stocks))
    return geometric_mean
