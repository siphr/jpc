import time

from super_simple_stock_market.stock_type import StockType
from super_simple_stock_market.trade_type import TradeType
import super_simple_stock_market.exceptions as exceptions


class Stock:
    """
    A class that models a stock.

    Parameters:
        symbol: Stock symbol.
        last_dividend: Last dividend.
        par_value: Par value.
        fixed_dividend_percent: Fixed dividend. Defaults to None.
        stock_type: Instance of StockType enumeration. Defaults to StockType.COMMON

    Reference:
        Document Section 2.

    Notes:
        * If the client wished we could have derived classes for individual StockTypes.
    """
    def __init__(self, symbol, last_dividend, par_value, fixed_dividend_percent=None, stock_type=StockType.COMMON):
        self._symbol = symbol
        self._last_dividend = last_dividend
        self._fixed_dividend_percent = fixed_dividend_percent
        self._par_value = par_value
        self._stock_type = stock_type
        self._trade_record = []

    def calculate_dividend_yield(self, price: float) -> float:
        """
        Given a price, calculate the dividend yield.

        Parameters:
            price: Price used for calculation.

        Reference:
            Document Section 2.a.i.
            Table 2, Row 1.

        Return:
            A floating point number representing the yield.

        Exceptions:
            e_sssm_fixed_dividend_unavailable:
            Raised if the preferred stock was missing the fixed dividend percent.

        Notes:
            As per the documentation calculate the dividend yield differently for preferred or common stock.
        """
        if self._stock_type == StockType.PREFERRED:
            if self._fixed_dividend_percent is None:
                raise exceptions.e_sssm_fixed_dividend_unavailable

            dividend_yield = ((self._fixed_dividend_percent/100) * self._par_value) / price
        else:
            dividend_yield = self._last_dividend / price

        return dividend_yield

    def calculate_price_earning_ratio(self, price: float) -> float:
        """
        Given a price, calculate the price earning ratio.

        Parameters:
            price: Price used for calculation.

        Reference:
            Document Section 2.a.ii.
            Table 2, Row 2.

        Return:
            A floating point number representing PE ratio.

        Notes:
            The specification is  a bit unclear in the formula the term Dividend is used. I was not sure whether
            this referred to the dividend yield or the last dividend or some function of the fixed dividend percent.
            I assumed it referred to dividend yield and the calculations here reflect that.

        Todo:
            * Confirm with client the use of dividend yield. Fix if necessary.
        """
        dividend = self.calculate_dividend_yield(price)
        price_earning_ratio = price / dividend

        return price_earning_ratio

    def record_trade(self, trade_type: TradeType, quantity: int, price: float):
        """
        Record a buy or sell trade for this stock.

        Parameters:
            trade_type: Instance of TradeType. Possible Values TradeType.BUY, TradeType.SELL.
            quantity: Number of shares traded.
            price: Price at which the shares were traded.

        Reference
            Document Section 2.a.iii.
        """
        try:
            self._trade_record.append({'trade': trade_type, 'quantity': quantity, 'price': price, 'timestamp': time.time()})
        except:
            if trade_type == TradeType.SELL:
                raise exceptions.e_sssm_trade_record_sell_failed
            else:
                raise exceptions.e_sssm_trade_record_buy_failed

    def calculate_volume_weighted_price(self, time_delta_minutes: int = 5) -> float:
        """
        Calculate volume weighted price of a stock.

        Parameters:
            time_delta_minutes: Number of minutes to go back in trade record history. Range 1-60.

        Returns:
            A floating point number representing the price.

        Exceptions:
            e_sssm_trade_record_empty:
            When there are no trade records available for that stock.

        Reference:
            Document Section 2.a.iv
            Table 2 Row 4

        Notes:
            * time_delta_minutes is bound within a range of 1 - 60 minutes (arbitrary).
        """
        if len(self._trade_record) == 0:
            raise exceptions.e_sssm_trade_record_empty

        if time_delta_minutes not in range(1, 61):
            raise exceptions.e_sssm_volume_weighted_time_out_of_bounds

        numerator = 0
        denominator = 0

        since_timestamp = time.time() - (time_delta_minutes * 60)
        filtered_record = self._trade_record if time_delta_minutes is None else\
            [record for record in self._trade_record if record['timestamp'] >= since_timestamp]

        for _record in filtered_record:
            quantity_scaled_price_per_trade = _record['quantity'] * _record['price']
            numerator = numerator + quantity_scaled_price_per_trade
            denominator = denominator + _record['quantity']

        volume_weighted_stock_price = numerator / denominator
        return volume_weighted_stock_price
