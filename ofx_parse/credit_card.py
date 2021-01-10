from typing import Union
from lxml.etree import _Element


class CreditCard:
    client_id: Union[int, None]

    def __init__(self, client_id: Union[int, None] = None) -> None:
        pass

    def __str__(self) -> str:
        return ''

    @classmethod
    def parse_ofx(cls, credit_el: _Element):
        ccstmttrnrs_el: _Element = credit_el.find('CCSTMTTRNRS', None)

        client_id = None

        if ccstmttrnrs_el is not None:
            trnuid_el = ccstmttrnrs_el.find('TRNUID', None)
            if trnuid_el is not None:
                pass

        return CreditCard(client_id)
