from enum import Enum


class StockType(Enum):
    """
    Enum representing stock types.

    Possible Values:
        COMMON: Common stock.
        PREFERRED: Preferred stock.
    """
    COMMON = 1
    PREFERRED = 2
