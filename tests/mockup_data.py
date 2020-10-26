"""This modules creates mockup data for testing"""

import xarray as xr
import numpy as np
import datetime
import os
from o3skim import utils


base = datetime.datetime(2000, 1, 1)
indexes = {
    'time': [base + datetime.timedelta(days=10*i) for i in range(99)],
    'plev': [x for x in range(1, 1000, 100)],
    'lat':  [x for x in range(-90, 90, 10)],
    'lon':  [x for x in range(-180, 180, 20)]
}


def data_vars(coordinates):
    """Creates a mock n-array with coordinate values"""
    alias = tuple(coordinates.values())
    dim = tuple(len(indexes[c]) for c in coordinates)
    return alias, np.ones(dim),


def map_coord(coordinates):
    """Creates a mock array by coordinate"""
    return {alias: indexes[c] for c, alias in coordinates.items()}


def dataset(name, coordinates):
    """Creates a dataset according to the global module indexes"""
    return xr.Dataset(
        {name: data_vars(coordinates)},
        coords=map_coord(coordinates)
    )


def netcdf(dirname, name, coordinates, **kwarg):
    """Creates or appends data to a mock netcdf file"""
    ds = dataset(name, coordinates)
    utils.to_netcdf(dirname, name, ds, groupby="year")

