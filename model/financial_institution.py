from typing import Union

from lxml.etree import _Element


class FinancialInstitution:
    id: Union[int, None]
    organization: Union[str, None]

    def __init__(self, organization: str = None, id: int = None):

        self.organization = organization
        self.id = id

    @classmethod
    def parse_ofx(cls, fi: _Element):
        organization = None
        id = None

        organization_node = fi.find('ORG', None)
        id_node = fi.find('FID', None)

        if organization_node is not None:
            organization = organization_node.text

        if id_node is not None:
            try:
                id = int(id_node.text)
            except:
                pass
        return FinancialInstitution(organization, id)

    def __str__(self) -> str:
        s = ''

        if self.organization:
            s += self.organization + ' '

        if self.id:
            s += '(' + str(self.id) + ')'

        return s if len(s) else ''
