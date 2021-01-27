"""Module with coordinate mockups"""

import datetime
import pandas as pd
import numpy as np


def time(num=12, start=2000, end=None):
    end = start + 1 if not end else end
    start = pd.Timestamp("{}-01-01".format(start))
    end = pd.Timestamp("{}-01-01".format(end))
    t = np.linspace(start.value, end.value, num + 1)[0:-1]
    return pd.to_datetime(t)


def lat(num=11):
    return np.linspace(-90, 90, num)


def lon(num=21):
    return np.linspace(-180, 180, num)


def plev(num=4):
    return np.logspace(1, 4, num)
