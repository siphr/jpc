import time

from super_simple_stock_market.stock_type import StockType
from super_simple_stock_market.trade_type import TradeType
import super_simple_stock_market.exceptions as exceptions


class Stock:

    def __init__(self, symbol, last_dividend, par_value, fixed_dividend_percent=None, stock_type=StockType.COMMON):
        self._symbol = symbol
        self._last_dividend = last_dividend
        self._fixed_dividend_percent = fixed_dividend_percent
        self._par_value = par_value
        self._stock_type = stock_type
        self._trade_record = []

    def calculate_dividend_yield(self, price: int):
        if self._stock_type == StockType.PREFERRED:
            if self._fixed_dividend_percent is None:
                raise exceptions.e_sssm_fixed_dividend_unavailable
            
            dividend_yield = ((self._fixed_dividend_percent/100) * self._par_value) / price
        else:
            dividend_yield = self._last_dividend / price
            
        return dividend_yield

    def calculate_price_earning_ratio(self, price: int):
        dividend = self.calculate_dividend_yield(price)
        price_earning_ratio = price / dividend

        return price_earning_ratio

    def record_trade(self, trade_type: TradeType, quantity: int, price: int):
        try:
            self._trade_record.append({'trade': trade_type, 'quantity': quantity, 'price': price, 'timestamp': time.time()})
        except:
            if trade_type == TradeType.SELL:
                raise exceptions.e_sssm_trade_record_sell_failed
            else:
                raise exceptions.e_sssm_trade_record_buy_failed

    def get_trade_record(self):
        return self._trade_record

if __name__ == '__main__':
    s = Stock('TEA', 0, 100)
    print(s.__dict__)
