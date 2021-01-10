from typing import Union

from lxml.etree import _Element
from utils.xmlutils import find_value


class FinancialInstitution:
    id: Union[int, None]
    organization: Union[str, None]

    def __init__(self, organization: str = None, id: int = None):

        self.organization = organization
        self.id = id

    @classmethod
    def parse_ofx(cls, fi: _Element = None):
        if fi is not None:
            return FinancialInstitution(
                id=find_value(fi, 'FID'),
                organization=find_value(fi, 'ORG')
            )
        return None

    def __str__(self) -> str:
        s = ''

        if self.organization:
            s += self.organization + ' '

        if self.id:
            s += '(' + str(self.id) + ')'

        return s if len(s) else ''
