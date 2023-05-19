from datetime import datetime
from datetime import timedelta

import mistune
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound
from pytz import timezone


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, info=None):
        if info:
            if info == "jinja2":
                info = "jinja"
            try:
                lexer = get_lexer_by_name(info, stripall=True)
            except ClassNotFound:
                lexer = get_lexer_by_name('text', stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return '<pre><code>' + mistune.escape(code) + '</code></pre>'


def pytz_datetime(ltz: str = "Europe/London", mask: str = "%Y-%m-%d %H:%M:%S.%f", days_delta: int = 0) -> datetime:
    """
    Returns the current date and time YYYY-MM-DD HH:MM:SS.MS for the defined local time zone,
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


def pytz_datetime_str(ltz: str = "Europe/London", mask: str = "%Y-%m-%d %H:%M:%S.%f", days_delta: int = 0) -> str:
    """
    Returns the current date and time YYYY-MM-DD HH:MM:SS.MS for the defined local time zone,
    can also adjust the date by using a delta(days)
    :param days_delta:
    :param ltz:
    :param mask:
    :return:
    """
    local_tz = timezone(ltz)
    if days_delta < 0:
        apply_delta = (datetime.now(local_tz) - timedelta(days=abs(days_delta))).strftime(mask)
        return datetime.strptime(apply_delta, mask).strftime(mask)
    if days_delta > 0:
        apply_delta = (datetime.now(local_tz) + timedelta(days=days_delta)).strftime(mask)
        return datetime.strptime(apply_delta, mask).strftime(mask)
    return datetime.strptime(datetime.now(local_tz).strftime(mask), mask).strftime(mask)
