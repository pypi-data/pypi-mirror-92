from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional, overload


@overload
def cents_to_decimal(amount: None) -> None:
    ...


@overload
def cents_to_decimal(amount: str) -> Decimal:
    ...


def cents_to_decimal(amount: Optional[str]) -> Optional[Decimal]:
    if amount is None:
        return None
    return Decimal(amount) / 100


def decimal_to_cents(amount: Decimal) -> str:
    return str((amount * 100).quantize(Decimal("1")))


def parse_datetime(d: str) -> datetime:
    """
    A very naive Zulu time parser that returns a time zone aware datetime

    :param d: A datetime string in Zulu time with optional microseconds e.g.: "2019-04-15T13:40:19.151Z"
    """
    # TODO: Replace this datetime.fromisoformat when only Python 3.7 is supported
    if "." in d:
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    else:
        date_format = "%Y-%m-%dT%H:%M:%SZ"
    return datetime.strptime(d, date_format).replace(tzinfo=timezone.utc)


def format_datetime(d: datetime) -> str:
    """
    Converts a timezone aware datetime object into a UTC ISO 8601 (Zulu time) string
    """
    if not d.tzinfo:
        raise Exception("Naive datetime not supported")
    return d.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
