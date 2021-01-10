from ofx_parse.status import Status
from typing import Union
from utils.parse import parse_int
from utils.xmlutils import get_value
from lxml.etree import _Element


class CreditCard:
    trnu_id: Union[int, None]

    def __init__(self, trnu_id: Union[int, None] = None,  status: Union[Status, None] = None) -> None:
        self.trnu_id = trnu_id
        self.status = status

    def __str__(self) -> str:
        str_list = []
        if self.trnu_id is not None:
            str_list.append('TRNUID:' + str(self.trnu_id))
        
        if self.status is not None:
            str_list.append('status: ' + str(self.status))
        

        return '\n'.join(str_list)

    @classmethod
    def parse_ofx(cls, credit_el: _Element):
        ccstmttrnrs_el: _Element = credit_el.find('CCSTMTTRNRS', None)

        if ccstmttrnrs_el is not None:

            return CreditCard(
                get_value(ccstmttrnrs_el.find('TRNUID', None), parse_int),
                Status.parse_ofx(ccstmttrnrs_el.find('STATUS', None)),
            )

        return None
