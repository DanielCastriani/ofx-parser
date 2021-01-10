from typing import Any, Union
from lxml.etree import _Element


def get_value(node_elm: Union[_Element, None] = None, parse_function=None) -> Any:
    if node_elm is not None:
        value: str = node_elm.text
        if parse_function is not None:
            return parse_function(value)
        else:
            return value.strip()
    return None


def find_value(parent:  Union[_Element, None] = None, key: str = None, parse_function=None) -> Any:
    if parent is not None:
        node_el = parent.find(key, None)
        return get_value(node_el, parse_function=parse_function)
