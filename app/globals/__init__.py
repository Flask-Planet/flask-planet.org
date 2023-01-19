from datetime import datetime
from datetime import timedelta

from pytz import timezone


def pytz_datetime(ltz: str = "Europe/London", mask: str = "%Y-%m-%d %H:%M:%S", days_delta: int = 0) -> datetime:
    """
    Returns the current date and time YYYY-MM-DD HH:MM:SS for the defined local time zone,
    can also adjust the date by using a delta(days)
    :param days_delta:
    :param ltz:
    :param mask:
    :return:
    """
    local_tz = timezone(ltz)
    if days_delta < 0:
        apply_delta = (datetime.now(local_tz) - timedelta(days=abs(days_delta))).strftime(mask)
        return datetime.strptime(apply_delta, mask)
    if days_delta > 0:
        apply_delta = (datetime.now(local_tz) + timedelta(days=days_delta)).strftime(mask)
        return datetime.strptime(apply_delta, mask)
    return datetime.strptime(datetime.now(local_tz).strftime(mask), mask)
