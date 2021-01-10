from typing import Union
from ofx_parse.credit_card import CreditCard
from ofx_parse.information import Information
import os

from lxml import etree
from lxml.etree import _Element


class OFX:
    information: Union[Information, None]
    credit_card: Union[CreditCard, None]

    def __init__(self, information: Union[Information, None] = None, credit_card: Union[CreditCard, None] = None):
        self.information = information
        self.credit_card = credit_card

    @classmethod
    def read_ofx(cls, url: str):
        if not os.path.exists(url):
            raise IOError('File not exists!')

        with open(url, 'r') as file:
            lines = file.readlines()

            while '<OFX>' not in lines[0]:
                lines.pop(0)

            while '</OFX>' not in lines[-1]:
                lines.pop(-1)

            xml_str = "".join(lines)
            root = etree.fromstring(xml_str, None)

            return OFX(
                information=Information.parse_ofx(root.find("SIGNONMSGSRSV1", None)),
                credit_card=CreditCard.parse_ofx(root.find("CREDITCARDMSGSRSV1", None))
            )

    def __str__(self) -> str:
        s = ''

        if self.information:
            s += '\n=============== INFORMATION ===============\n'
            s += str(self.information)

        if self.credit_card:
            s += '\n=============== CREDIT CARD ===============\n'
            s += str(self.credit_card)

        if len(s) > 0 :
            s += '\n===========================================\n'

        return s

    def to_string(self):
        return str(self)
