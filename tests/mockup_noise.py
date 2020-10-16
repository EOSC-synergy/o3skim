"""This modules creates mockup data for testing"""

import xarray as xr
import numpy as np
import datetime
import random


base = datetime.datetime(2000, 1, 1)
indexes = {
    'time': [base + datetime.timedelta(days=9*i) for i in range(99)],
    'plev': [x for x in range(1, 1000, 100)],
    'lat':  [x for x in range(-90, 90, 10)],
    'lon':  [x for x in range(-180, 180, 20)]
}


def data_vars():
    """Creates a mock n-array with coordinade values"""
    dim = [len(axis) for _, axis in indexes.items()]
    return tuple(indexes), np.ones(dim),


def data_coord(): 
    """Creates a mock coordinades"""
    return indexes


def dataset(name):
    """Creates a dataset acording to the global module indexes"""
    return xr.Dataset(
        {name: data_vars()},
        coords = data_coord()
    )


def netcdf(path, name, **kwarg):
    """Creates or appends data to a noise netcdf file"""
    ds=dataset(name)
    ds.to_netcdf(path)
