from datetime import datetime
from ofx_parse.transaction import Transaction
from ofx_parse.status import Status
from typing import List, Union
from utils.parse import parse_datetime, parse_int
from utils.xmlutils import find_value
from lxml.etree import _Element


class CreditCard:
    trnu_id: Union[int, None]
    status: Union[Status, None]
    currency: Union[str, None]
    credit_card_number: Union[str, None]
    transaction_list: Union[List[Transaction], None]
    start_date: Union[datetime, None]
    end_date: Union[datetime, None]

    def __init__(self, trnu_id: Union[int, None] = None,  status: Union[Status, None] = None, currency: Union[str, None] = None,
                 credit_card_number: Union[str, None] = None, transaction_list: Union[List[Transaction], None] = None,
                 start_date: Union[datetime, None] = None, end_date: Union[datetime, None] = None
                 ) -> None:
        self.trnu_id = trnu_id
        self.status = status
        self.currency = currency
        self.credit_card_number = credit_card_number
        self.transaction_list = transaction_list
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self) -> str:
        str_list = []
        if self.credit_card_number is not None:
            str_list.append('credit_card_number: ' + str(self.credit_card_number))

        if self.start_date is not None:
            str_list.append('start_date: ' + str(self.start_date))

        if self.end_date is not None:
            str_list.append('end_date: ' + str(self.end_date))

        if self.currency is not None:
            str_list.append('currency: ' + str(self.currency))

        if self.trnu_id is not None:
            str_list.append('TRNUID: ' + str(self.trnu_id))

        if self.status is not None:
            str_list.append('status: ' + str(self.status))

        if self.transaction_list and len(self.transaction_list) > 0:
            str_list.append(' ----------------------------------------- ')
            str_list.append('\n'.join([str(t) for t in self.transaction_list]))

        return '\n'.join(str_list)

    @classmethod
    def parse_ofx(cls, credit_el: _Element):
        ccstmttrnrs_el: _Element = credit_el.find('CCSTMTTRNRS', None)

        if ccstmttrnrs_el is not None:
            currency = None
            credit_card_number = None
            start_date = None
            end_date = None
            transaction_list: List[Transaction] = []

            ccstmtrs_el: _Element = ccstmttrnrs_el.find('CCSTMTRS', None)

            if ccstmtrs_el is not None:
                banktranlist_el: _Element = ccstmtrs_el.find('BANKTRANLIST', None)

                if banktranlist_el is not None:
                    start_date = find_value(banktranlist_el, 'DTSTART', lambda x: parse_datetime(x, '%Y%m%d'))
                    end_date = find_value(banktranlist_el, 'DTEND', lambda x: parse_datetime(x, '%Y%m%d'))

                    stmttrn_el: List[_Element] = banktranlist_el.findall('STMTTRN', None)
                    for transaction_el in stmttrn_el:
                        transaction_list.append(Transaction.parse_ofx(transaction_el))

                credit_card_number = find_value(ccstmtrs_el.find('CCACCTFROM', None), 'ACCTID')
                currency = find_value(ccstmtrs_el, 'CURDEF')

            return CreditCard(
                trnu_id=find_value(ccstmttrnrs_el, 'TRNUID', parse_int),
                status=Status.parse_ofx(ccstmttrnrs_el.find('STATUS', None)),
                currency=currency,
                credit_card_number=credit_card_number,
                transaction_list=transaction_list,
                start_date=start_date,
                end_date=end_date,
            )

        return None
