"""
BBDB timestamp utilities.
"""

from datetime import datetime, timezone
from dateutil.parser import parse

# BBDB-style time formats.
DATEFORMAT = "%Y-%m-%d"
TIMEFORMAT = "%Y-%m-%d %H:%M:%S %z"


def to_datestamp(dt: datetime, time: bool = False) -> str:
    """Return a BBDB-style datestamp given a datetime.
    """

    # Add TZ info if not present.
    if not dt.tzinfo:
        dt = dt.astimezone(timezone.utc)

    return dt.strftime(TIMEFORMAT if time else DATEFORMAT)


def from_datestamp(value: str) -> datetime:
    """Parse a date stamp into a datetime.
    """

    return parse(value)


def now() -> datetime:
    """Return the time now.
    """

    return datetime.utcnow()


if __name__ == "__main__":
    print(to_datestamp(now(), time=False))
    print(to_datestamp(now(), time=True))
