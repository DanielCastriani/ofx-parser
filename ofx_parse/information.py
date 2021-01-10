from datetime import datetime
from utils.xmlutils import find_value
from utils.parse import parse_datetime
from ofx_parse.status import Status
from ofx_parse.financial_institution import FinancialInstitution
from typing import Union

from lxml.etree import _Element


class Information:
    lang: Union[str, None]
    date: Union[datetime, None]
    financial_institution: Union[FinancialInstitution, None]
    status: Union[Status, None]

    def __init__(self, date: datetime = None, lang: str = None, financial_institution: FinancialInstitution = None, status: Status = None):
        self.date = date
        self.lang = lang
        self.financial_institution = financial_institution
        self.status = status

    def __str__(self) -> str:
        str_list = []

        if self.financial_institution:
            str_list.append('financial institution: ' + str(self.financial_institution))

        if self.date:
            str_list.append('dtserver: ' + str(self.date))

        if self.lang:
            str_list.append('lang: ' + self.lang)

        if self.status:
            str_list.append('status: ' + str(self.status))

        return '\n'.join(str_list)

    @classmethod
    def parse_ofx(cls, signonmsgsrsv1_elm: _Element):

        sonrs_elm: _Element = signonmsgsrsv1_elm.find("SONRS", None)
        if sonrs_elm is not None:
            return Information(
                find_value(sonrs_elm, "DTSERVER", parse_datetime),
                find_value(sonrs_elm, "LANGUAGE"),
                FinancialInstitution.parse_ofx(sonrs_elm.find("FI", None)),
                Status.parse_ofx(sonrs_elm.find("STATUS", None)),
            )

        return None
