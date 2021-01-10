from typing import Union
from utils.xmlutils import get_value

from lxml.etree import _Element


class FinancialInstitution:
    id: Union[int, None]
    organization: Union[str, None]

    def __init__(self, organization: str = None, id: int = None):

        self.organization = organization
        self.id = id

    @classmethod
    def parse_ofx(cls, fi: Union[_Element, None] = None):
        if fi is not None:
            return FinancialInstitution(
                id=get_value(fi.find('FID', None)),
                organization=get_value(fi.find('ORG', None))
            )
        return None

    def __str__(self) -> str:
        s = ''

        if self.organization:
            s += self.organization + ' '

        if self.id:
            s += '(' + str(self.id) + ')'

        return s if len(s) else ''
