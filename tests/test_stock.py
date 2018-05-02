import pytest

from super_simple_stock_market.stock import Stock
from super_simple_stock_market.stock_type import StockType

@pytest.fixture
def common_stock(mocker):
    return Stock(symbol='CMN', last_dividend=1, par_value=100)

@pytest.fixture
def preferred_stock(mocker):
    return Stock(symbol='PRF', last_dividend=10, par_value=100, fixed_dividend_percent=20, stock_type=StockType.PREFERRED)

def test_common_stock(common_stock):
    assert common_stock.calculate_dividend_yield(100) == 0.01
    assert common_stock.calculate_price_earning_ratio(8) == 64

def test_preferred_stock(preferred_stock):
    assert preferred_stock.calculate_dividend_yield(100) == 0.2
    assert preferred_stock.calculate_price_earning_ratio(8) == 3.2
