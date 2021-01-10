from datetime import datetime
from model.status import Status
from typing import Union

from lxml.etree import _Element

from model.financial_institution import FinancialInstitution


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
        s = ''

        if self.date:
            s += 'dtserver: ' + str(self.date) + "\n"

        if self.lang:
            s += 'lang: ' + self.lang + "\n"

        if self.financial_institution:
            s += 'financial institution: ' + str(self.financial_institution) + '\n'

        if self.status:
            s += 'status: ' + str(self.status) + '\n'

        return s

    @classmethod
    def parse_ofx(cls, root: _Element):
        signonmsgsrsv1_elm: _Element = root.find("SIGNONMSGSRSV1", None)

        date = None
        fi = None
        lang = None
        status = None

        if signonmsgsrsv1_elm is not None:
            sonrs_elm: _Element = signonmsgsrsv1_elm.find("SONRS", None)
            if sonrs_elm is not None:
                dtserver_elm: _Element = sonrs_elm.find("DTSERVER", None)
                lang_elm: _Element = sonrs_elm.find("LANGUAGE", None)
                fi_elm: _Element = sonrs_elm.find("FI", None)
                status_elm: _Element = sonrs_elm.find("STATUS", None)

                if dtserver_elm is not None:
                    date = datetime.strptime(dtserver_elm.text, '%Y%m%d%H%M%S')

                if lang_elm is not None:
                    lang = lang_elm.text

                if fi_elm is not None:
                    fi = FinancialInstitution.parse_ofx(fi_elm)

                if status_elm is not None:
                    status = Status.parse_ofx(status_elm)

        return Information(date, lang, fi, status)
