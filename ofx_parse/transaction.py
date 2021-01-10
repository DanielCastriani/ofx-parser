from datetime import datetime
from typing import Union

from lxml.etree import _Element
from utils.parse import parse_datetime, parse_float, parse_int
from utils.xmlutils import find_value


class Transaction:

    id: Union[int, None]
    type: Union[str, None]
    date: Union[datetime, None]
    value: Union[float, None]
    description: Union[str, None]
    currency_rate: Union[float, None]
    currency_description: Union[str, None]

    def __init__(self, id: int = None, type: str = None, date: datetime = None, value: float = None, description: str = None,
                 currency_rate: float = None, currency_description: str = None) -> None:
        self.id = id
        self.type = type
        self.date = date
        self.value = value
        self.description = description
        self.currency_rate = currency_rate
        self.currency_description = currency_description

    def __str__(self) -> str:
        values = []

        if self.type is not None:
            values.append(str(self.type))

        if self.date is not None:
            values.append(str(self.date))

        if self.description is not None:
            values.append(str(self.description))

        if self.value is not None:
            values.append('\t\t' + str(self.value))

        if self.currency_description is not None and self.currency_rate is not None:
            values.append('[%s %f]' % (self.currency_description, self.currency_rate))
        else:
            if self.currency_description is not None:
                values.append('[%s]' % self.currency_description)

        return "\t".join(values)

    @classmethod
    def parse_ofx(cls, transaction_el: _Element = None):
        currency_el = None

        if transaction_el is not None:
            currency_el = transaction_el.find('CURRENCY', None)

        return Transaction(
            id=find_value(transaction_el, 'FITID', parse_int),
            date=find_value(transaction_el, 'DTPOSTED', lambda x: parse_datetime(x, '%Y%m%d')),
            value=find_value(transaction_el, 'TRNAMT', parse_float),
            description=find_value(transaction_el, 'MEMO'),
            type=find_value(transaction_el, 'TRNTYPE'),
            currency_rate=find_value(currency_el, 'CURRATE', parse_float),
            currency_description=find_value(currency_el, 'CURSYM')
        )
