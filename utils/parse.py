from datetime import datetime
from typing import Union


def parse_int(value: str):
    if value:
        try:
            return int(value)
        except:
            return None
    return None

def parse_float(value: str):
    if value:
        try:
            return float(value)
        except:
            return None
    return None


def parse_datetime(value: str, format='%Y%m%d%H%M%S'):
    if value:
        try:
            return datetime.strptime(value, format)
        except:
            return None
    return None
