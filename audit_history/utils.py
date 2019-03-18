import datetime
from decimal import Decimal

from .settings import SUPPORTED_TIMESTAMP_FORMATS


def parse_timestamp(timestamp):
    dt = None
    for ts in SUPPORTED_TIMESTAMP_FORMATS:
        try:
            dt = datetime.datetime.strptime(
                    timestamp,
                    ts
                )
            break
        except ValueError:
            continue
    return dt


def json_formatter(o):
    if hasattr(o, 'to_json'):
        return o.to_json()
    if isinstance(o, Decimal):
        return str(o)
    if isinstance(o, datetime.datetime):
        if o.tzinfo:
            return o.strftime('%Y-%m-%dT%H:%M:%S%z')
        return o.strftime("%Y-%m-%dT%H:%M:%S")
    if isinstance(o, datetime.date):
        return o.strftime("%Y-%m-%d")
    if isinstance(o, datetime.time):
        if o.tzinfo:
            return o.strftime('%H:%M:%S%z')
        return o.strftime("%H:%M:%S")
    if isinstance(o, datetime.tzinfo):
        return o.zone
    if isinstance(o, set):
        return list(o)

    raise TypeError('Unserializable object {} of type {}'.format(o, type(o)))
