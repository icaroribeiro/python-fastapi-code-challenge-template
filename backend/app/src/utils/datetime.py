from datetime import datetime


def datetime_to_integer_timestamp(dt: datetime) -> int:
    return int(round(dt.timestamp()))
