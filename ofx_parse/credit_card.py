from ofx_parse.status import Status
from typing import Union
from utils.parse import parse_int
from utils.xmlutils import get_value
from lxml.etree import _Element


class CreditCard:
    trnu_id: Union[int, None]
    status: Union[Status, None]
    currency: Union[str, None]
    credit_card_number: Union[str, None]

    def __init__(self, trnu_id: Union[int, None] = None,  status: Union[Status, None] = None, currency: Union[str, None] = None, credit_card_number: Union[str, None] = None) -> None:
        self.trnu_id = trnu_id
        self.status = status
        self.currency = currency
        self.credit_card_number = credit_card_number

    def __str__(self) -> str:
        str_list = []
        if self.credit_card_number is not None:
            str_list.append('credit_card_number:' + str(self.credit_card_number))

        if self.currency is not None:
            str_list.append('currency:' + str(self.currency))

        if self.trnu_id is not None:
            str_list.append('TRNUID:' + str(self.trnu_id))

        if self.status is not None:
            str_list.append('status: ' + str(self.status))

        return '\n'.join(str_list)

    @classmethod
    def parse_ofx(cls, credit_el: _Element):
        ccstmttrnrs_el: _Element = credit_el.find('CCSTMTTRNRS', None)

        if ccstmttrnrs_el is not None:
            currency = None
            credit_card_number = None

            ccstmtrs_el: _Element = ccstmttrnrs_el.find('CCSTMTRS', None)

            if ccstmtrs_el is not None:
                ccacctfrom_el: _Element = ccstmtrs_el.find('CCACCTFROM', None)
                if ccacctfrom_el is not None:
                    credit_card_number = get_value(ccacctfrom_el.find('ACCTID', None))

                currency = get_value(ccstmtrs_el.find('CURDEF', None))

            return CreditCard(
                trnu_id=get_value(ccstmttrnrs_el.find('TRNUID', None), parse_int),
                status=Status.parse_ofx(ccstmttrnrs_el.find('STATUS', None)),
                currency=currency,
                credit_card_number=credit_card_number
            )

        return None
