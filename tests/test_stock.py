import pytest

from super_simple_stock_market.algorithms import calculate_gcbe_all_share_index
from super_simple_stock_market.stock import Stock
from super_simple_stock_market.stock_type import StockType
from super_simple_stock_market.trade_type import TradeType
import super_simple_stock_market.exceptions as exceptions


@pytest.fixture
def common_stock(mocker):
    return Stock(symbol='CMN', last_dividend=1, par_value=100)


@pytest.fixture
def preferred_stock(mocker):
    return Stock(symbol='PRF', last_dividend=10, par_value=100, fixed_dividend_percent=20, stock_type=StockType.PREFERRED)


@pytest.fixture
def bad_preferred_stock(mocker):
    return Stock(symbol='PRF', last_dividend=10, par_value=100, stock_type=StockType.PREFERRED)


@pytest.fixture
def stock_list(common_stock, preferred_stock):
    return [common_stock, preferred_stock]


def test_common_stock(common_stock):
    assert common_stock.calculate_dividend_yield(100) == 0.01
    assert common_stock.calculate_price_earning_ratio(8) == 64


def test_preferred_stock(preferred_stock):
    assert preferred_stock.calculate_dividend_yield(100) == 0.2
    assert preferred_stock.calculate_price_earning_ratio(8) == 3.2


def test_bad_preferred_stock_throws(bad_preferred_stock):
    with pytest.raises(exceptions.e_sssm_fixed_dividend_unavailable):
        bad_preferred_stock.calculate_dividend_yield(10)


def test_volume_weight_price_without_trade_record_empty(common_stock):
    with pytest.raises(exceptions.e_sssm_trade_record_empty):
        common_stock.calculate_volume_weighted_price()


def test_volume_weighted_price_with_trade_record(common_stock):
    common_stock.record_trade(TradeType.BUY, 10, 23)
    common_stock.record_trade(TradeType.BUY, 10, 23)
    common_stock.record_trade(TradeType.SELL, 10, 32)
    common_stock.record_trade(TradeType.SELL, 10, 21)
    common_stock.record_trade(TradeType.SELL, 10, 28)

    assert common_stock.calculate_volume_weighted_price() == 25.4


def test_volume_weighted_price_with_bad_time_delta(common_stock):
    common_stock.record_trade(TradeType.BUY, 10, 23)

    with pytest.raises(exceptions.e_sssm_volume_weighted_time_out_of_bounds):
        common_stock.calculate_volume_weighted_price(time_delta_minutes=0)

    with pytest.raises(exceptions.e_sssm_volume_weighted_time_out_of_bounds):
        common_stock.calculate_volume_weighted_price(time_delta_minutes=61)


def test_calculate_gcbe_all_share_index_stock_list_empty_throws():
    with pytest.raises(exceptions.e_sssm_gcbe_all_share_index_empty_stock_list):
        calculate_gcbe_all_share_index([])


def test_calculate_gcbe_all_share_index(stock_list):
    for stock in stock_list:
        stock.record_trade(TradeType.BUY, 10, 43)
        stock.record_trade(TradeType.BUY, 10, 27)
        stock.record_trade(TradeType.SELL, 10, 32)
        stock.record_trade(TradeType.SELL, 10, 21)
        stock.record_trade(TradeType.SELL, 10, 88)

    assert calculate_gcbe_all_share_index(stock_list) == 42.2
