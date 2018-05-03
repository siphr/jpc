from enum import Enum


class TradeType(Enum):
    """
    Enum representing trade types.

    Possible Values:
        BUY: A buy trade.
        SELL: A sell trade.
    """
    BUY = 1
    SELL = 2
