from typing import Union
from utils.xmlutils import get_value
from utils.parse import parse_int
from lxml.etree import _Element


class Status:
    code: Union[int, None]
    status_type: Union[str, None]

    def __init__(self, code: int = None, status_type: str = None):
        """
        Args:
            code (int): status code
            status_type (str): status_type of status (INFO, WARN, and ERROR)
        """
        self.code = code
        self.status_type = status_type

    def __str__(self) -> str:
        if self.status_type != None and self.code != None:
            return '%s (%d)' % (self.status_type, self.code)

        if self.status_type != None:
            return self.status_type

        if self.code != None:
            return str(self.code)

        return ''

    @classmethod
    def parse_ofx(cls, status_el: Union[_Element, None] = None):
        if status_el is not None:
            return Status(
                code=get_value(status_el.find('CODE', None), parse_int),
                status_type=get_value(status_el.find('SEVERITY', None))
            )
        return None
