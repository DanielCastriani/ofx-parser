import os
from datetime import datetime

from lxml import etree
from model import information
from model.information import Information


class OFX:
    information: Information

    def __init__(self, infos: Information):
        self.information = infos

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

            info = Information.parse_ofx(root)

        return OFX(info)

    def __str__(self) -> str:
        s = ''

        if self.information:
            s += str(self.information)

        return s
