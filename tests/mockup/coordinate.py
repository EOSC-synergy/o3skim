"""Module with coordinate mockups"""

import datetime


def __timeline(start, end=None, step=10):
    if not end:
        end = start
    start = datetime.datetime(start, 1, 1)
    end = datetime.datetime(end, 12, 31)
    step = datetime.timedelta(days=step)
    while start < end:
        yield start
        start += step


def time(start=2000, end=2010, step=30):
    return ('time', [t for t in __timeline(start, end, step)])


def lat(delta=10):
    return ('lat', [x for x in range(-90, 90, delta)])


def lon(delta=20):
    return ('lon', [x for x in range(-180, 180, delta)])


def plev(delta=100):
    return ('plev', [x for x in range(1, 1000, delta)])
