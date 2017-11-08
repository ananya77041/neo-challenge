from datetime import datetime, timedelta

DATE_FORMAT = '%Y-%m-%d'
DATE_STEP = timedelta(days=1)


def _strptime(string):
    return datetime.strptime(string, DATE_FORMAT)


def _strftime(date):
    return date.strftime(DATE_FORMAT)


def _date_range_parameters(start, end, span_days):
    start = _strptime(start)
    end   = _strptime(end)
    span  = timedelta(days=span_days)
    return start, end, span


def forward_date_range(start, end, span_days):
    """
    Generate tuples with intervals from given range of dates (forward).

    forward_date_range('2012-01-01', '2012-01-5', 2)

    1st yield = ('2012-01-01', '2012-01-03')
    2nd yield = ('2012-01-04', '2012-01-05')
    """
    start, end, span = _date_range_parameters(start, end, span_days)
    stop = end - span

    while start < stop:
        current = start + span
        yield _strftime(start), _strftime(current)
        start = current + DATE_STEP

    yield _strftime(start), _strftime(end)