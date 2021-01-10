from typing import Union
from lxml.etree import _Element


def get_value(node_elm: Union[_Element, None] = None, parse_function=None):
    if node_elm is not None:
        if parse_function is not None:
            return parse_function(node_elm.text)
        else:
            return node_elm.text
    return None
