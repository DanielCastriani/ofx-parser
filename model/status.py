from typing import Union
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
            return 'Status: %s (%d)' % (self.status_type, self.code)

        if self.status_type != None:
            return 'Status: ' + self.status_type

        if self.code != None:
            return 'Status: ' + str(self.code)

        return ''

    @classmethod
    def parse_ofx(cls, status_el: _Element):
        code = None
        status_type = None

        code_el = status_el.find('CODE', None)
        if code_el is not None:
            code = int(code_el.text)

        status_type_el = status_el.find('SEVERITY', None)
        if status_type_el is not None:
            status_type = status_type_el.text

        return Status(code=code, status_type=status_type)
