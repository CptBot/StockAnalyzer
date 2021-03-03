from datetime import date
from dataclasses import dataclass
from enum import Enum
from typing import List


class Trade(Enum):
    UNKNOWN = 0
    BUY = 1
    SELL = 2


@dataclass
class Money:
    value: float
    currency: str


@dataclass
class Tax:
    money: Money
    tax_kind: str
    exchange_rate: Money


@dataclass
class Stock:
    isin: str
    name: str
    sectors: set()


@dataclass
class Price:
    money: Money
    exchange_rate: Money


@dataclass
class StockTrade:
    stock: Stock
    amount: int
    price_per_unit: Price
    cost: Money
    valuta: date
    taxes: List[Tax]
    kind: Trade.BUY
