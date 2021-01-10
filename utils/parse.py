from datetime import datetime
from typing import Union


def parse_int(value: Union[str, None]):
    if value:
        try:
            return int(value)
        except:
            return None
    return None


def parse_datetime(value: Union[str, None], format='%Y%m%d%H%M%S'):
    if value:
        try:
            return datetime.strptime(value, format)
        except:
            return None
    return None
