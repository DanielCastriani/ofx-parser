from typing import Union
from datetime import datetime
from utils.parse import parse_datetime, parse_float, parse_int
from utils.xmlutils import find_value
from lxml.etree import _Element


class Transaction:

    def __init__(self, id: Union[int, None] = None, type: Union[str, None] = None, date: Union[datetime, None] = None,
                 value: Union[float, None] = None, description: Union[str, None] = None) -> None:
        self.id = id
        self.type = type
        self.date = date
        self.value = value
        self.description = description

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
        
        return "\t".join(values) 

    @classmethod
    def parse_ofx(cls, transaction_el: Union[_Element] = None):
        return Transaction(
            id=find_value(transaction_el, 'FITID', parse_int),
            date=find_value(transaction_el, 'DTPOSTED', lambda x: parse_datetime(x, '%Y%m%d')),
            value=find_value(transaction_el, 'TRNAMT', parse_float),
            description=find_value(transaction_el, 'MEMO'),
            type=find_value(transaction_el, 'TRNTYPE'),
        )
